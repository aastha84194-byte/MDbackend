from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from app.api import deps
from app.db.session import get_db
from app.db.base import User
from app.models.role import Role, RoleName
from app.core.security import get_password_hash
from app.schemas.user import UserCreate, UserOut
from app.schemas.incharge import InchargeCreate

router = APIRouter()

@router.post("/import/students")
async def import_students_from_excel(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user = Depends(deps.PermissionChecker([RoleName.ADMIN]))
) -> Any:
    """
    Import students from Excel file. (Admin only)
    """
    content = await file.read()
    try:
        data = parse_excel_to_dict(content)
        return admin_service.bulk_import_students(db, data=data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to parse Excel: {str(e)}")

@router.post("/import/teachers")
# ... (existing import_teachers_from_excel) ...

@router.get("/staff", response_model=List[UserOut])
def get_staff_list(
    db: Session = Depends(get_db),
    current_user = Depends(deps.PermissionChecker([RoleName.ADMIN]))
):
    """
    Get all users with Teacher or Incharge roles.
    """
    staff_roles = [RoleName.TEACHER.value, RoleName.INCHARGE.value, RoleName.FINANCIAL_ADMIN.value]
    return db.query(User).join(Role).filter(Role.name.in_(staff_roles)).all()

@router.post("/staff", response_model=UserOut)
def create_staff_user(
    obj_in: Any,
    db: Session = Depends(get_db),
    current_user = Depends(deps.PermissionChecker([RoleName.ADMIN]))
):
    """
    Create a new staff user (Teacher, Incharge, or Financial Admin).
    """
    role_name = obj_in.get("role")
    role = db.query(Role).filter(Role.name == role_name).first()
    if not role:
        raise HTTPException(status_code=400, detail="Invalid role")
        
    db_user = User(
        username=obj_in["username"],
        email=obj_in.get("email"),
        full_name=obj_in.get("full_name"),
        hashed_password=get_password_hash(obj_in["password"]),
        role_id=role.id,
        is_active=True
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    # If it's a teacher, create the profile
    if role_name == RoleName.TEACHER:
        from app.models.teacher import Teacher
        db_teacher = Teacher(
            user_id=db_user.id,
            employee_id=obj_in.get("employee_id") or f"EMP{db_user.id}",
            department=obj_in.get("department"),
            salary=obj_in.get("salary") or 0.0
        )
        db.add(db_teacher)
        db.commit()
    
    # If it's an incharge, create the profile with permissions
    elif role_name == RoleName.INCHARGE:
        from app.models.incharge import Incharge
        perms = obj_in.get("permissions", [])
        if isinstance(perms, str):
            perms = [p.strip() for p in perms.split(",") if p.strip()]
            
        db_incharge = Incharge(
            user_id=db_user.id,
            employee_id=obj_in.get("employee_id") or f"INC{db_user.id}",
            department=obj_in.get("department"),
            salary=obj_in.get("salary") or 0.0,
            permissions=perms
        )
        db.add(db_incharge)
        db.commit()
    
    return db_user
