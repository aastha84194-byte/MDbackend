from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from app.api import deps
from app.db.session import get_db
from app.services.student_service import student_service
from app.schemas.student import StudentCreate, StudentUpdate, StudentOut
from app.models.role import RoleName

router = APIRouter()

@router.post("/import")
async def import_students(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user = Depends(deps.PermissionChecker([RoleName.ADMIN, RoleName.INCHARGE], required_permission="students"))
) -> Any:
    """
    Import students from Excel file.
    """
    if not file.filename.endswith((".xlsx", ".xlsm")):
        raise HTTPException(status_code=400, detail="Invalid file format. Please upload an Excel file.")
    
    try:
        content = await file.read()
        return student_service.import_students_from_excel(db, file_content=content)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/", response_model=StudentOut)
def create_student(
    *,
    db: Session = Depends(get_db),
    student_in: StudentCreate,
    current_user = Depends(deps.PermissionChecker([RoleName.ADMIN, RoleName.INCHARGE], required_permission="students"))
) -> Any:
    """
    Create new student. (Admin or Incharge only)
    """
    return student_service.create_student(db, obj_in=student_in)

@router.get("/", response_model=List[StudentOut])
def read_students(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_user = Depends(deps.PermissionChecker([RoleName.ADMIN, RoleName.TEACHER, RoleName.INCHARGE]))
) -> Any:
    """
    Retrieve students. (Staff only)
    """
    return student_service.get_students(db, skip=skip, limit=limit)

@router.get("/me", response_model=StudentOut)
def read_student_me(
    db: Session = Depends(get_db),
    current_user = Depends(deps.get_current_active_user)
) -> Any:
    """
    Get current user's student profile.
    """
    if current_user.role.name != RoleName.STUDENT:
        raise HTTPException(status_code=400, detail="User is not a student")
    if not current_user.student_profile:
        raise HTTPException(status_code=404, detail="Student profile not found")
    return current_user.student_profile

@router.get("/{id}", response_model=StudentOut)
def read_student_by_id(
    id: int,
    db: Session = Depends(get_db),
    current_user = Depends(deps.get_current_active_user)
) -> Any:
    """
    Get student by ID. (Staff or the student themselves)
    """
    student = student_service.get_student(db, id=id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    # Check if user is staff or the student themselves
    if current_user.role.name not in [RoleName.ADMIN, RoleName.TEACHER, RoleName.INCHARGE]:
        if not current_user.student_profile or current_user.student_profile.id != id:
            raise HTTPException(status_code=403, detail="Not enough permissions")
            
    return student
