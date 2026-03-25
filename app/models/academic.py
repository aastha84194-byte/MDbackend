from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from app.db.session import Base

# Association table for Teachers and Subjects
teacher_subjects = Table(
    "teacher_subjects",
    Base.metadata,
    Column("teacher_id", Integer, ForeignKey("teachers.id"), primary_key=True),
    Column("subject_id", Integer, ForeignKey("subjects.id"), primary_key=True),
)

class SchoolClass(Base):
    __tablename__ = "classes"

    id = Column(Integer, primary_key=True, index=True)
    class_number = Column(Integer, nullable=False) # e.g. 1, 2, 3
    section = Column(String, nullable=True) # e.g. "A", "B"
    name = Column(String, unique=True, index=True, nullable=False)  # e.g., "10-A"
    room_number = Column(String, nullable=True)

    students = relationship("Student", back_populates="school_class")
    subjects = relationship("Subject", back_populates="school_class")

class Subject(Base):
    __tablename__ = "subjects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    code = Column(String, unique=True, index=True, nullable=False)  # e.g., "MATH101"
    class_id = Column(Integer, ForeignKey("classes.id"))

    school_class = relationship("SchoolClass", back_populates="subjects")
    teachers = relationship("Teacher", secondary=teacher_subjects, back_populates="subjects")
    marks = relationship("Mark", back_populates="subject")
