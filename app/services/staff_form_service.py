from sqlalchemy.orm import Session
from app.models.staff_management import Leave, Salary, LeaveStatus
from app.models.form_requests import AdmissionForm, ContactUs
from app.schemas.staff_forms import LeaveCreate, SalaryCreate, AdmissionFormCreate, ContactUsCreate

class StaffFormService:
    # Leave logic
    def apply_leave(self, db: Session, *, obj_in: LeaveCreate):
        db_obj = Leave(**obj_in.model_dump())
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update_leave_status(self, db: Session, *, leave_id: int, status: LeaveStatus):
        leave = db.query(Leave).filter(Leave.id == leave_id).first()
        if leave:
            leave.status = status
            db.add(leave)
            db.commit()
            db.refresh(leave)
        return leave

    # Salary logic
    def create_salary(self, db: Session, *, obj_in: SalaryCreate):
        db_obj = Salary(**obj_in.model_dump())
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    # Inquiry logic
    def create_admission_form(self, db: Session, *, obj_in: AdmissionFormCreate):
        db_obj = AdmissionForm(**obj_in.model_dump())
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def create_contact_inquiry(self, db: Session, *, obj_in: ContactUsCreate):
        db_obj = ContactUs(**obj_in.model_dump())
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

staff_form_service = StaffFormService()
