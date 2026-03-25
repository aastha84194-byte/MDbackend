from sqlalchemy import Column, Integer, String, ForeignKey, Float
from sqlalchemy.orm import relationship
from app.db.session import Base
from app.models.academic import teacher_subjects

class Teacher(Base):
    __tablename__ = "teachers"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    employee_id = Column(String, unique=True, index=True)
    designation = Column(String)
    department = Column(String, nullable=True)
    salary = Column(Float, nullable=True)

    user = relationship("User", back_populates="teacher_profile")
    subjects = relationship("Subject", secondary=teacher_subjects, back_populates="teachers")
    attendance = relationship("TeacherAttendance", back_populates="teacher")
    leaves = relationship("Leave", back_populates="teacher")
