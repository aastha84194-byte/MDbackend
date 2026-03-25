from typing import Optional, List
from pydantic import BaseModel

class ClassBase(BaseModel):
    class_number: int
    name: str
    section: Optional[str] = None
    room_number: Optional[str] = None

class ClassCreate(ClassBase):
    pass

class ClassUpdate(ClassBase):
    name: Optional[str] = None

class ClassOut(ClassBase):
    id: int
    student_count: Optional[int] = 0

    class Config:
        from_attributes = True

class SubjectBase(BaseModel):
    name: str
    code: str
    class_id: int

class SubjectCreate(SubjectBase):
    pass

class SubjectUpdate(SubjectBase):
    name: Optional[str] = None
    code: Optional[str] = None
    class_id: Optional[int] = None

class SubjectOut(SubjectBase):
    id: int

    class Config:
        from_attributes = True
