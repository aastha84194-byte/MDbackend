from sqlalchemy.orm import Session
from app.models.attendance import Attendance, TeacherAttendance
from app.schemas.attendance import AttendanceCreate, TeacherAttendanceCreate
from datetime import date

class AttendanceService:
    def mark_student_attendance(self, db: Session, *, obj_in: AttendanceCreate):
        db_obj = Attendance(**obj_in.model_dump())
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_student_attendance(self, db: Session, student_id: int):
        return db.query(Attendance).filter(Attendance.student_id == student_id).all()

    def mark_teacher_attendance(self, db: Session, *, obj_in: TeacherAttendanceCreate):
        db_obj = TeacherAttendance(**obj_in.model_dump())
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

attendance_service = AttendanceService()
