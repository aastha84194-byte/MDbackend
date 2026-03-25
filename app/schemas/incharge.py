from pydantic import BaseModel
from typing import Optional, List, Any

class InchargeBase(BaseModel):
    employee_id: str
    department: Optional[str] = None
    salary: Optional[float] = 0.0
    permissions: Optional[List[str]] = []

class InchargeCreate(InchargeBase):
    user_id: Optional[int] = None
    username: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None
    full_name: Optional[str] = None

class InchargeUpdate(InchargeBase):
    employee_id: Optional[str] = None
    permissions: Optional[List[str]] = None

class InchargeOut(InchargeBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True
