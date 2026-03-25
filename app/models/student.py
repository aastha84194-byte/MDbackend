from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from app.db.session import Base

class Student(Base):
    __tablename__ = "students"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    class_id = Column(Integer, ForeignKey("classes.id"))
    # Additional student specific info
    # Basic Details (Extended)
    admission_number = Column(String, unique=True, index=True)
    aadhaar_number = Column(String, nullable=True)
    date_of_birth = Column(String)
    gender = Column(String)
    religion = Column(String, nullable=True)
    social_category = Column(String, nullable=True)
    mother_tongue = Column(String, nullable=True)
    date_of_admission = Column(String, nullable=True)
    is_bpl = Column(Boolean, default=False)
    habitation = Column(String, nullable=True)
    address = Column(String)

    user = relationship("User", back_populates="student_profile")
    school_class = relationship("SchoolClass", back_populates="students")
    guardian = relationship("Guardian", back_populates="student", uselist=False)
    attendance = relationship("Attendance", back_populates="student")
    marks = relationship("Mark", back_populates="student")
