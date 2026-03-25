from sqlalchemy.orm import Session
from typing import List, Dict, Any
from app.models.student import Student
from app.models.teacher import Teacher
from app.models.user import User
from app.models.role import Role, RoleName
from app.core.security import get_password_hash
from app.schemas.student import StudentCreate
from app.schemas.teacher import TeacherCreate

class AdminService:
    def bulk_import_students(self, db: Session, data: List[Dict[str, Any]]):
        student_role = db.query(Role).filter(Role.name == RoleName.STUDENT.value).first()
        results = {"success": 0, "failed": 0, "errors": []}

        for row in data:
            try:
                # 1. Create User
                username = str(row.get("admission_number", row.get("username")))
                email = row.get("email", f"{username}@mdpic.edu.in")
                password = str(row.get("password", "student123"))
                
                user = User(
                    username=username,
                    email=email,
                    hashed_password=get_password_hash(password),
                    full_name=row.get("full_name"),
                    role_id=student_role.id
                )
                db.add(user)
                db.flush()

                # 2. Create Student Profile
                student = Student(
                    user_id=user.id,
                    class_id=row.get("class_id"),
                    admission_number=username,
                    date_of_birth=str(row.get("date_of_birth")),
                    address=row.get("address")
                )
                db.add(student)
                results["success"] += 1
            except Exception as e:
                db.rollback()
                results["failed"] += 1
                results["errors"].append(f"Error importing {row.get('full_name')}: {str(e)}")
        
        db.commit()
        return results

    def bulk_import_teachers(self, db: Session, data: List[Dict[str, Any]]):
        teacher_role = db.query(Role).filter(Role.name == RoleName.TEACHER.value).first()
        results = {"success": 0, "failed": 0, "errors": []}

        for row in data:
            try:
                # 1. Create User
                emp_id = str(row.get("employee_id"))
                email = row.get("email", f"{emp_id}@mdpic.edu.in")
                password = str(row.get("password", "teacher123"))

                user = User(
                    username=emp_id,
                    email=email,
                    hashed_password=get_password_hash(password),
                    full_name=row.get("full_name"),
                    role_id=teacher_role.id
                )
                db.add(user)
                db.flush()

                # 2. Create Teacher Profile
                teacher = Teacher(
                    user_id=user.id,
                    employee_id=emp_id,
                    designation=row.get("designation")
                )
                db.add(teacher)
                results["success"] += 1
            except Exception as e:
                db.rollback()
                results["failed"] += 1
                results["errors"].append(f"Error importing {row.get('full_name')}: {str(e)}")

        db.commit()
        return results

admin_service = AdminService()
