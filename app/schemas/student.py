from pydantic import BaseModel
from typing import Optional, List

class GuardianBase(BaseModel):
    father_name: Optional[str] = None
    mother_name: Optional[str] = None
    guardian_name: Optional[str] = None
    aadhaar_number: Optional[str] = None
    contact_number: Optional[str] = None
    email: Optional[str] = None

class GuardianCreate(GuardianBase):
    pass

class GuardianOut(GuardianBase):
    id: int
    student_id: int
    class Config:
        from_attributes = True

class StudentBase(BaseModel):
    admission_number: str
    full_name: str
    date_of_birth: Optional[str] = None
    gender: Optional[str] = None
    aadhaar_number: Optional[str] = None
    religion: Optional[str] = None
    social_category: Optional[str] = None
    mother_tongue: Optional[str] = None
    date_of_admission: Optional[str] = None
    is_bpl: bool = False
    habitation: Optional[str] = None
    address: Optional[str] = None
    class_id: Optional[int] = None

class StudentCreate(StudentBase):
    guardian: Optional[GuardianCreate] = None

class StudentUpdate(StudentBase):
    admission_number: Optional[str] = None
    full_name: Optional[str] = None
    guardian: Optional[GuardianCreate] = None

class StudentOut(StudentBase):
    id: int
    user_id: int
    guardian: Optional[GuardianOut] = None

    class Config:
        from_attributes = True
