from pydantic import BaseModel
from typing import Optional, List
from app.schemas.user import UserOut

class TeacherBase(BaseModel):
    employee_id: str
    designation: Optional[str] = None
    department: Optional[str] = None
    salary: Optional[float] = 0.0

class TeacherCreate(TeacherBase):
    user_id: Optional[int] = None # Optional if creating user simultaneously
    username: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None
    full_name: Optional[str] = None

class TeacherUpdate(TeacherBase):
    employee_id: Optional[str] = None

class TeacherOut(TeacherBase):
    id: int
    user_id: int
    user: Optional[UserOut] = None # Return nested user details

    class Config:
        from_attributes = True
