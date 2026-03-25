from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.api import deps
from app.db.session import get_db
from app.services.academic_service import academic_service
from app.schemas.academic import ClassCreate, ClassUpdate, ClassOut, SubjectCreate, SubjectOut
from app.models.role import RoleName

router = APIRouter()

@router.get("/classes/", response_model=List[ClassOut])
def read_classes(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_user = Depends(deps.get_current_active_user)
) -> Any:
    return academic_service.get_classes(db, skip=skip, limit=limit)

@router.post("/classes/", response_model=ClassOut)
def create_class(
    *,
    db: Session = Depends(get_db),
    class_in: ClassCreate,
    current_user = Depends(deps.PermissionChecker([RoleName.ADMIN]))
) -> Any:
    return academic_service.create_class(db, obj_in=class_in.dict())

@router.get("/subjects/", response_model=List[SubjectOut])
def read_subjects(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    return academic_service.get_subjects(db, skip=skip, limit=limit)

@router.post("/subjects/", response_model=SubjectOut)
def create_subject(
    *,
    db: Session = Depends(get_db),
    subject_in: SubjectCreate,
    current_user = Depends(deps.PermissionChecker([RoleName.ADMIN]))
) -> Any:
    return academic_service.create_subject(db, obj_in=subject_in.dict())
