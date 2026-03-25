from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.api import deps
from app.db.session import get_db
from app.services.teacher_service import teacher_service
from app.schemas.teacher import TeacherCreate, TeacherUpdate, TeacherOut
from app.models.role import RoleName

router = APIRouter()

@router.post("/", response_model=TeacherOut)
def create_teacher(
    *,
    db: Session = Depends(get_db),
    teacher_in: TeacherCreate,
    current_user = Depends(deps.PermissionChecker([RoleName.ADMIN]))
) -> Any:
    """
    Create new teacher. (Admin only)
    """
    return teacher_service.create_teacher(db, obj_in=teacher_in)

@router.get("/", response_model=List[TeacherOut])
def read_teachers(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_user = Depends(deps.PermissionChecker([RoleName.ADMIN, RoleName.INCHARGE], required_permission="teachers"))
) -> Any:
    """
    Retrieve teachers. (Admin or Incharge only)
    """
    return teacher_service.get_teachers(db, skip=skip, limit=limit)

@router.get("/me", response_model=TeacherOut)
def read_teacher_me(
    db: Session = Depends(get_db),
    current_user = Depends(deps.get_current_active_user)
) -> Any:
    """
    Get current user's teacher profile.
    """
    if current_user.role.name != RoleName.TEACHER:
        raise HTTPException(status_code=400, detail="User is not a teacher")
    if not current_user.teacher_profile:
        raise HTTPException(status_code=404, detail="Teacher profile not found")
    return current_user.teacher_profile

@router.post("/{teacher_id}/subjects/{subject_id}")
def assign_subject_to_teacher(
    teacher_id: int,
    subject_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(deps.PermissionChecker([RoleName.ADMIN, RoleName.INCHARGE]))
) -> Any:
    """
    Assign a subject to a teacher.
    """
    teacher = teacher_service.assign_subject(db, teacher_id=teacher_id, subject_id=subject_id)
    if not teacher:
        raise HTTPException(status_code=404, detail="Teacher or Subject not found")
    return {"message": "Subject assigned successfully"}
