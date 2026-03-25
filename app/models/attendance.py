from sqlalchemy import Column, Integer, String, ForeignKey, Date, Boolean, Enum
from sqlalchemy.orm import relationship
from app.db.session import Base
import enum

class AttendanceStatus(str, enum.Enum):
    PRESENT = "present"
    ABSENT = "absent"
    LATE = "late"
    EXCUSED = "excused"

class Attendance(Base):
    __tablename__ = "attendance"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"))
    date = Column(Date, nullable=False)
    status = Column(Enum(AttendanceStatus), nullable=False)
    remarks = Column(String, nullable=True)

    student = relationship("Student", back_populates="attendance")

class TeacherAttendance(Base):
    __tablename__ = "teacher_attendance"

    id = Column(Integer, primary_key=True, index=True)
    teacher_id = Column(Integer, ForeignKey("teachers.id"))
    date = Column(Date, nullable=False)
    status = Column(Enum(AttendanceStatus), nullable=False)
    check_in = Column(String, nullable=True)
    check_out = Column(String, nullable=True)

    teacher = relationship("Teacher", back_populates="attendance")
