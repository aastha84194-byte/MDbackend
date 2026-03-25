from sqlalchemy import Column, Integer, String, ForeignKey, Float, Date, Enum
from sqlalchemy.orm import relationship
from app.db.session import Base
import enum

class FeeType(str, enum.Enum):
    TUITION = "tuition"
    EXAM = "exam"
    TRANSPORT = "transport"
    LIBRARY = "library"
    OTHER = "other"

class FeeStructure(Base):
    __tablename__ = "fee_structures"

    id = Column(Integer, primary_key=True, index=True)
    class_id = Column(Integer, ForeignKey("classes.id"))
    fee_type = Column(Enum(FeeType), nullable=False)
    amount = Column(Float, nullable=False)
    month = Column(String, nullable=True) # e.g., "January"

class FeePayment(Base):
    __tablename__ = "fee_payments"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"))
    amount_paid = Column(Float, nullable=False)
    fine_amount = Column(Float, default=0.0)
    scholarship_amount = Column(Float, default=0.0)
    month = Column(String, nullable=False)
    payment_date = Column(Date, nullable=False)
    transaction_id = Column(String, unique=True, index=True)
    status = Column(String, default="pending")  # e.g., "paid", "partially_paid", "pending"
