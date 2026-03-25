from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.academic import SchoolClass, Subject

class AcademicService:
    def get_classes(self, db: Session, skip: int = 0, limit: int = 100) -> List[SchoolClass]:
        return db.query(SchoolClass).offset(skip).limit(limit).all()

    def create_class(self, db: Session, *, obj_in: dict) -> SchoolClass:
        db_obj = SchoolClass(**obj_in)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_class(self, db: Session, id: int) -> Optional[SchoolClass]:
        return db.query(SchoolClass).filter(SchoolClass.id == id).first()

    def update_class(self, db: Session, *, db_obj: SchoolClass, obj_in: dict) -> SchoolClass:
        for field in obj_in:
            if hasattr(db_obj, field):
                setattr(db_obj, field, obj_in[field])
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def delete_class(self, db: Session, *, id: int) -> Optional[SchoolClass]:
        obj = db.query(SchoolClass).filter(SchoolClass.id == id).first()
        if obj:
            db.delete(obj)
            db.commit()
        return obj

    # Subjects
    def get_subjects(self, db: Session, skip: int = 0, limit: int = 100) -> List[Subject]:
        return db.query(Subject).offset(skip).limit(limit).all()

    def create_subject(self, db: Session, *, obj_in: dict) -> Subject:
        db_obj = Subject(**obj_in)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

academic_service = AcademicService()
