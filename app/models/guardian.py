from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db.session import Base

class Guardian(Base):
    __tablename__ = "guardians"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"))
    
    father_name = Column(String)
    mother_name = Column(String)
    guardian_name = Column(String)
    aadhaar_number = Column(String)
    contact_number = Column(String)
    email = Column(String, nullable=True)

    student = relationship("Student", back_populates="guardian")
