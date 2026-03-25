from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.api import deps
from app.db.session import get_db
from app.services.attendance_service import attendance_service
from app.schemas.attendance import AttendanceCreate, AttendanceOut, TeacherAttendanceCreate, TeacherAttendanceOut
from app.models.role import RoleName

router = APIRouter()

@router.post("/student", response_model=AttendanceOut)
def mark_student_attendance(
    *,
    db: Session = Depends(get_db),
    attendance_in: AttendanceCreate,
    current_user = Depends(deps.PermissionChecker([RoleName.ADMIN, RoleName.TEACHER, RoleName.INCHARGE], required_permission="attendance"))
) -> Any:
    """
    Mark student attendance. (Admin or Teacher only)
    """
    return attendance_service.mark_student_attendance(db, obj_in=attendance_in)

@router.get("/student/{student_id}", response_model=List[AttendanceOut])
def read_student_attendance(
    student_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(deps.get_current_active_user)
) -> Any:
    """
    Get attendance records for a student. (Staff or the student themselves)
    """
    # Check if user is staff or the student themselves
    if current_user.role.name not in [RoleName.ADMIN, RoleName.TEACHER, RoleName.INCHARGE]:
        if not current_user.student_profile or current_user.student_profile.id != student_id:
            raise HTTPException(status_code=403, detail="Not enough permissions")
            
    return attendance_service.get_student_attendance(db, student_id=student_id)

@router.post("/teacher", response_model=TeacherAttendanceOut)
def mark_teacher_attendance(
    *,
    db: Session = Depends(get_db),
    attendance_in: TeacherAttendanceCreate,
    current_user = Depends(deps.PermissionChecker([RoleName.ADMIN]))
) -> Any:
    """
    Mark teacher attendance. (Admin only)
    """
    return attendance_service.mark_teacher_attendance(db, obj_in=attendance_in)
