from sqlalchemy import Column, Integer, String, ForeignKey, Float, Date, Enum, Text
from sqlalchemy.orm import relationship
from app.db.session import Base
import enum

class LeaveStatus(str, enum.Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"

class Leave(Base):
    __tablename__ = "leaves"

    id = Column(Integer, primary_key=True, index=True)
    teacher_id = Column(Integer, ForeignKey("teachers.id"))
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    reason = Column(Text, nullable=False)
    status = Column(Enum(LeaveStatus), default=LeaveStatus.PENDING)

    teacher = relationship("Teacher", back_populates="leaves")

class Salary(Base):
    __tablename__ = "salaries"

    id = Column(Integer, primary_key=True, index=True)
    teacher_id = Column(Integer, ForeignKey("teachers.id"))
    amount = Column(Float, nullable=False)
    month = Column(String, nullable=False)  # e.g., "2024-03"
    payment_date = Column(Date, nullable=True)
    status = Column(String, default="pending")  # e.g., "paid", "pending"
