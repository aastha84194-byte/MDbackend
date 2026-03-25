from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.api import deps
from app.db.session import get_db
from app.services.exam_service import exam_service
from app.schemas.exam import ExamCreate, ExamOut, MarkCreate, MarkOut
from app.models.role import RoleName

router = APIRouter()

@router.get("/", response_model=List[ExamOut])
def read_exams(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_user = Depends(deps.PermissionChecker([RoleName.ADMIN, RoleName.TEACHER, RoleName.INCHARGE], required_permission="exams"))
) -> Any:
    return exam_service.get_exams(db, skip=skip, limit=limit)

@router.delete("/{id}")
def delete_exam(
    id: int,
    db: Session = Depends(get_db),
    current_user = Depends(deps.PermissionChecker([RoleName.ADMIN]))
) -> Any:
    return exam_service.delete_exam(db, id=id)

@router.put("/{id}", response_model=ExamOut)
def update_exam(
    id: int,
    *,
    db: Session = Depends(get_db),
    exam_in: ExamCreate, # Reusing create schema for simplicity
    current_user = Depends(deps.PermissionChecker([RoleName.ADMIN, RoleName.INCHARGE], required_permission="exams"))
) -> Any:
    return exam_service.update_exam(db, id=id, obj_in=exam_in.dict())

@router.post("/", response_model=ExamOut)
def create_exam(
    *,
    db: Session = Depends(get_db),
    exam_in: ExamCreate,
    current_user = Depends(deps.PermissionChecker([RoleName.ADMIN, RoleName.INCHARGE], required_permission="exams"))
) -> Any:
    """
    Create new exam. (Admin only)
    """
    return exam_service.create_exam(db, obj_in=exam_in)

@router.post("/marks", response_model=List[MarkOut])
def upload_marks(
    *,
    db: Session = Depends(get_db),
    marks_in: List[MarkCreate],
    current_user = Depends(deps.PermissionChecker([RoleName.ADMIN, RoleName.TEACHER, RoleName.INCHARGE], required_permission="exams"))
) -> Any:
    """
    Upload marks for students. (Admin or Teacher only)
    """
    return exam_service.upload_marks(db, marks_in=marks_in)

@router.get("/results/{student_id}")
def read_student_results(
    student_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(deps.get_current_active_user)
) -> Any:
    """
    Get aggregated results for a student. (Staff or the student themselves)
    """
    # Check if user is staff or the student themselves
    if current_user.role.name not in [RoleName.ADMIN, RoleName.TEACHER, RoleName.INCHARGE]:
        if not current_user.student_profile or current_user.student_profile.id != student_id:
            raise HTTPException(status_code=403, detail="Not enough permissions")
            
    results = exam_service.get_student_results(db, student_id=student_id)
    if not results:
        raise HTTPException(status_code=404, detail="Results not found")
    return results
