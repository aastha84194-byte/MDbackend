from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.exam import Exam, Mark, ExamType
from app.schemas.exam import ExamCreate, MarkCreate
from typing import List

class ExamService:
    def create_exam(self, db: Session, *, obj_in: ExamCreate):
        db_obj = Exam(**obj_in.model_dump())
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def upload_marks(self, db: Session, *, marks_in: List[MarkCreate]):
        db_objs = [Mark(**m.model_dump()) for m in marks_in]
        db.add_all(db_objs)
        db.commit()
        return db_objs

    def get_student_results(self, db: Session, student_id: int):
        # Basic aggregation logic: Sum marks across all exams/subjects
        results = db.query(
            Mark.student_id,
            func.sum(Mark.obtained_marks).label("total_marks"),
            func.avg(Mark.obtained_marks).label("average_marks")
        ).filter(Mark.student_id == student_id).group_by(Mark.student_id).first()
        return results

    def get_exams(self, db: Session, skip: int = 0, limit: int = 100):
        return db.query(Exam).offset(skip).limit(limit).all()

    def delete_exam(self, db: Session, id: int):
        db_obj = db.query(Exam).filter(Exam.id == id).first()
        if db_obj:
            db.delete(db_obj)
            db.commit()
        return db_obj

    def update_exam(self, db: Session, id: int, obj_in: dict):
        db_obj = db.query(Exam).filter(Exam.id == id).first()
        if db_obj:
            for field in obj_in:
                if hasattr(db_obj, field):
                    setattr(db_obj, field, obj_in[field])
            db.add(db_obj)
            db.commit()
            db.refresh(db_obj)
        return db_obj

exam_service = ExamService()
