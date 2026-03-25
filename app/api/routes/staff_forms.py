from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.api import deps
from app.db.session import get_db
from app.services.staff_form_service import staff_form_service
from app.schemas.staff_forms import (
    LeaveCreate, LeaveOut, SalaryCreate, SalaryOut, 
    AdmissionFormCreate, ContactUsCreate
)
from app.models.role import RoleName
from app.models.staff_management import Leave, Salary, LeaveStatus

router = APIRouter()

# Staff Routes
@router.post("/leaves", response_model=LeaveOut)
def apply_leave(
    *,
    db: Session = Depends(get_db),
    leave_in: LeaveCreate,
    current_user = Depends(deps.PermissionChecker([RoleName.TEACHER]))
) -> Any:
    """
    Apply for leave. (Teachers only, must be for themselves)
    """
    if not current_user.teacher_profile or current_user.teacher_profile.id != leave_in.teacher_id:
        raise HTTPException(status_code=403, detail="You can only apply for your own leave")
    return staff_form_service.apply_leave(db, obj_in=leave_in)

@router.get("/leaves/me", response_model=List[LeaveOut])
def read_my_leaves(
    db: Session = Depends(get_db),
    current_user = Depends(deps.PermissionChecker([RoleName.TEACHER]))
) -> Any:
    """
    Get current teacher's leave history.
    """
    return db.query(Leave).filter(Leave.teacher_id == current_user.teacher_profile.id).all()

@router.patch("/leaves/{leave_id}/status")
def update_leave_status(
    leave_id: int,
    status: LeaveStatus,
    db: Session = Depends(get_db),
    current_user = Depends(deps.PermissionChecker([RoleName.ADMIN]))
) -> Any:
    return staff_form_service.update_leave_status(db, leave_id=leave_id, status=status)

@router.post("/salaries", response_model=SalaryOut)
def create_salary(
    *,
    db: Session = Depends(get_db),
    salary_in: SalaryCreate,
    current_user = Depends(deps.PermissionChecker([RoleName.ADMIN, RoleName.FINANCIAL_ADMIN]))
) -> Any:
    """
    Record salary payment. (Admin or Financial Admin only)
    """
    return staff_form_service.create_salary(db, obj_in=salary_in)

@router.get("/salaries/me", response_model=List[SalaryOut])
def read_my_salaries(
    db: Session = Depends(get_db),
    current_user = Depends(deps.PermissionChecker([RoleName.TEACHER]))
) -> Any:
    """
    Get current teacher's salary history.
    """
    return db.query(Salary).filter(Salary.teacher_id == current_user.teacher_profile.id).all()

# Public Form Routes
@router.post("/public/admission")
def submit_admission_form(
    *,
    db: Session = Depends(get_db),
    form_in: AdmissionFormCreate
) -> Any:
    return staff_form_service.create_admission_form(db, obj_in=form_in)

@router.post("/public/contact")
def submit_contact_inquiry(
    *,
    db: Session = Depends(get_db),
    form_in: ContactUsCreate
) -> Any:
    return staff_form_service.create_contact_inquiry(db, obj_in=form_in)
