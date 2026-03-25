from pydantic import BaseModel, EmailStr
from datetime import date, datetime
from typing import Optional
from app.models.staff_management import LeaveStatus

class LeaveBase(BaseModel):
    teacher_id: int
    start_date: date
    end_date: date
    reason: str

class LeaveCreate(LeaveBase):
    pass

class LeaveOut(LeaveBase):
    id: int
    status: LeaveStatus

    class Config:
        from_attributes = True

class SalaryBase(BaseModel):
    teacher_id: int
    amount: float
    month: str

class SalaryCreate(SalaryBase):
    pass

class SalaryOut(SalaryBase):
    id: int
    payment_date: Optional[date] = None
    status: str

    class Config:
        from_attributes = True

class AdmissionFormCreate(BaseModel):
    student_name: str
    parent_name: str
    email: EmailStr
    phone: str
    previous_school: Optional[str] = None
    requested_class: str

class ContactUsCreate(BaseModel):
    name: str
    email: EmailStr
    subject: str
    message: str
