from pydantic import BaseModel
from datetime import date
from typing import Optional
from app.models.attendance import AttendanceStatus

class AttendanceBase(BaseModel):
    date: date
    status: AttendanceStatus
    remarks: Optional[str] = None

class AttendanceCreate(AttendanceBase):
    student_id: int

class AttendanceOut(AttendanceBase):
    id: int
    student_id: int

    class Config:
        from_attributes = True

class TeacherAttendanceCreate(AttendanceBase):
    teacher_id: int
    check_in: Optional[str] = None
    check_out: Optional[str] = None

class TeacherAttendanceOut(AttendanceBase):
    id: int
    teacher_id: int
    check_in: Optional[str] = None
    check_out: Optional[str] = None

    class Config:
        from_attributes = True
