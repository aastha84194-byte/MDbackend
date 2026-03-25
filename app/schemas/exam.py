from pydantic import BaseModel
from typing import Optional, List
from app.models.exam import ExamType

class ExamBase(BaseModel):
    title: str
    exam_type: ExamType
    max_marks: float
    date: Optional[str] = None

class ExamCreate(ExamBase):
    pass

class ExamOut(ExamBase):
    id: int

    class Config:
        from_attributes = True

class MarkBase(BaseModel):
    obtained_marks: float
    remarks: Optional[str] = None

class MarkCreate(MarkBase):
    student_id: int
    subject_id: int
    exam_id: int
    teacher_id: int

class MarkUpdate(MarkBase):
    obtained_marks: Optional[float] = None

class MarkOut(MarkBase):
    id: int
    student_id: int
    subject_id: int
    exam_id: int
    teacher_id: int

    class Config:
        from_attributes = True

class ResultSummary(BaseModel):
    student_id: int
    total_marks: float
    percentage: float
    grade: str
