from sqlalchemy import Column, Integer, String, ForeignKey, Float, Enum
from sqlalchemy.orm import relationship
from app.db.session import Base
import enum

class ExamType(str, enum.Enum):
    CLASS_TEST = "class_test"
    MID_TERM = "mid_term"
    FINAL = "final"
    ASSIGNMENT = "assignment"

class Exam(Base):
    __tablename__ = "exams"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    exam_type = Column(Enum(ExamType), nullable=False)
    max_marks = Column(Float, nullable=False)
    date = Column(String, nullable=True)

    marks = relationship("Mark", back_populates="exam")

class Mark(Base):
    __tablename__ = "marks"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"))
    subject_id = Column(Integer, ForeignKey("subjects.id"))
    exam_id = Column(Integer, ForeignKey("exams.id"))
    teacher_id = Column(Integer, ForeignKey("teachers.id"))
    obtained_marks = Column(Float, nullable=False)
    remarks = Column(String, nullable=True)

    student = relationship("Student", back_populates="marks")
    subject = relationship("Subject", back_populates="marks")
    exam = relationship("Exam", back_populates="marks")
