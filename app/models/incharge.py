from sqlalchemy import Column, Integer, String, ForeignKey, Float, JSON
from sqlalchemy.orm import relationship
from app.db.session import Base

class Incharge(Base):
    __tablename__ = "incharges"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    employee_id = Column(String, unique=True, index=True)
    department = Column(String, nullable=True)
    salary = Column(Float, nullable=True)
    # Permissions stored as a list of strings: ["fees", "attendance", "exams", "students", "staff"]
    permissions = Column(JSON, default=[])

    user = relationship("User", back_populates="incharge_profile")
