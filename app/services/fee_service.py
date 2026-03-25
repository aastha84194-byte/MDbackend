from sqlalchemy.orm import Session
from app.models.fee import FeeStructure, FeePayment
from app.schemas.fee import FeeStructureCreate, FeePaymentCreate

class FeeService:
    def create_fee_structure(self, db: Session, *, obj_in: FeeStructureCreate):
        db_obj = FeeStructure(**obj_in.model_dump())
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_class_fee_structure(self, db: Session, class_id: int):
        return db.query(FeeStructure).filter(FeeStructure.class_id == class_id).all()

    def get_fee_structures(self, db: Session, skip: int = 0, limit: int = 100):
        return db.query(FeeStructure).offset(skip).limit(limit).all()

    def update_fee_structure(self, db: Session, id: int, obj_in: FeeStructureCreate):
        db_obj = db.query(FeeStructure).filter(FeeStructure.id == id).first()
        if not db_obj:
            raise Exception("Fee structure not found")
        update_data = obj_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_obj, field, value)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def delete_fee_structure(self, db: Session, id: int):
        db_obj = db.query(FeeStructure).filter(FeeStructure.id == id).first()
        if not db_obj:
            raise Exception("Fee structure not found")
        db.delete(db_obj)
        db.commit()
        return db_obj

    def record_payment(self, db: Session, *, obj_in: FeePaymentCreate):
        # Calculate expected amount based on structure
        student = db.query(Student).filter(Student.id == obj_in.student_id).first()
        if not student:
            raise Exception("Student not found")
            
        structure = db.query(FeeStructure).filter(
            FeeStructure.class_id == student.class_id,
            FeeStructure.month == obj_in.month
        ).first()
        
        total_due = structure.amount if structure else 0.0
        expected = total_due + obj_in.fine_amount - obj_in.scholarship_amount
        
        # Determine status
        status = "paid"
        if obj_in.amount_paid < expected:
            status = "partially_paid"
        elif obj_in.amount_paid == 0:
            status = "pending"
            
        db_obj = FeePayment(
            **obj_in.model_dump(exclude={"status"}),
            status=status
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_payments(self, db: Session, skip: int = 0, limit: int = 100):
        return db.query(FeePayment).offset(skip).limit(limit).all()

    def delete_payment(self, db: Session, id: int):
        db_obj = db.query(FeePayment).filter(FeePayment.id == id).first()
        if db_obj:
            db.delete(db_obj)
            db.commit()
        return db_obj

    def get_student_payments(self, db: Session, student_id: int):
        return db.query(FeePayment).filter(FeePayment.student_id == student_id).all()

fee_service = FeeService()
