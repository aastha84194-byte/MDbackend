from pydantic import BaseModel
from typing import Optional
from datetime import date
from app.models.fee import FeeType

class FeeStructureBase(BaseModel):
    class_id: int
    fee_type: FeeType
    amount: float
    month: Optional[str] = None

class FeeStructureCreate(FeeStructureBase):
    pass

class FeeStructureOut(FeeStructureBase):
    id: int

    class Config:
        from_attributes = True

class FeePaymentBase(BaseModel):
    student_id: int
    amount_paid: float
    fine_amount: Optional[float] = 0.0
    scholarship_amount: Optional[float] = 0.0
    month: str
    payment_date: date
    transaction_id: str
    status: Optional[str] = "pending"

class FeePaymentCreate(FeePaymentBase):
    pass

class FeePaymentOut(FeePaymentBase):
    id: int

    class Config:
        from_attributes = True
