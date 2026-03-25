from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.api import deps
from app.db.session import get_db
from app.services.fee_service import fee_service
from app.schemas.fee import FeeStructureCreate, FeeStructureOut, FeePaymentCreate, FeePaymentOut
from app.models.role import RoleName

router = APIRouter()

@router.post("/structures", response_model=FeeStructureOut)
def create_fee_structure(
    *,
    db: Session = Depends(get_db),
    fee_in: FeeStructureCreate,
    current_user = Depends(deps.PermissionChecker([RoleName.ADMIN, RoleName.FINANCIAL_ADMIN, RoleName.INCHARGE], required_permission="fees"))
) -> Any:
    """
    Create a fee structure for a class. (Admin or Financial Admin only)
    """
    return fee_service.create_fee_structure(db, obj_in=fee_in)

@router.get("/structures", response_model=List[FeeStructureOut])
def read_fee_structures(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_user = Depends(deps.PermissionChecker([RoleName.ADMIN, RoleName.FINANCIAL_ADMIN, RoleName.TEACHER]))
) -> Any:
    return fee_service.get_fee_structures(db, skip=skip, limit=limit)

@router.get("/structures/class/{class_id}", response_model=List[FeeStructureOut])
def read_class_fee_structures(
    class_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(deps.get_current_active_user)
) -> Any:
    return fee_service.get_class_fee_structure(db, class_id=class_id)

@router.put("/structures/{id}", response_model=FeeStructureOut)
def update_fee_structure(
    id: int,
    fee_in: FeeStructureCreate, # Reusing create schema as it's simple
    db: Session = Depends(get_db),
    current_user = Depends(deps.PermissionChecker([RoleName.ADMIN, RoleName.FINANCIAL_ADMIN, RoleName.INCHARGE], required_permission="fees"))
) -> Any:
    return fee_service.update_fee_structure(db, id=id, obj_in=fee_in)

@router.delete("/structures/{id}")
def delete_fee_structure(
    id: int,
    db: Session = Depends(get_db),
    current_user = Depends(deps.PermissionChecker([RoleName.ADMIN]))
) -> Any:
    return fee_service.delete_fee_structure(db, id=id)

@router.post("/payments", response_model=FeePaymentOut)
def record_payment(
    *,
    db: Session = Depends(get_db),
    payment_in: FeePaymentCreate,
    current_user = Depends(deps.PermissionChecker([RoleName.ADMIN, RoleName.FINANCIAL_ADMIN, RoleName.INCHARGE], required_permission="fees"))
) -> Any:
    """
    Record a fee payment. (Admin or Financial Admin only)
    """
    return fee_service.record_payment(db, obj_in=payment_in)

@router.get("/payments/", response_model=List[FeePaymentOut])
def read_payments(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_user = Depends(deps.PermissionChecker([RoleName.ADMIN, RoleName.FINANCIAL_ADMIN, RoleName.INCHARGE], required_permission="fees"))
) -> Any:
    """
    Get all fee payments. (Staff only)
    """
    return fee_service.get_payments(db, skip=skip, limit=limit)

@router.delete("/payments/{id}")
def delete_payment(
    id: int,
    db: Session = Depends(get_db),
    current_user = Depends(deps.PermissionChecker([RoleName.ADMIN]))
) -> Any:
    return fee_service.delete_payment(db, id=id)

@router.get("/payments/student/{student_id}", response_model=List[FeePaymentOut])
def read_student_payments(
    student_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(deps.get_current_active_user)
) -> Any:
    """
    Get payment history for a student. (Staff or the student themselves)
    """
    # Check if user is staff or the student themselves
    if current_user.role.name not in [RoleName.ADMIN, RoleName.FINANCIAL_ADMIN]:
        if not current_user.student_profile or current_user.student_profile.id != student_id:
            raise HTTPException(status_code=403, detail="Not enough permissions")
            
    return fee_service.get_student_payments(db, student_id=student_id)
