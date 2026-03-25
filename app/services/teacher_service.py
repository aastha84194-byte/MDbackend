from sqlalchemy.orm import Session
from app.repositories.teacher_repository import teacher_repo
from app.models.teacher import Teacher
from app.models.academic import Subject
from app.schemas.teacher import TeacherCreate, TeacherUpdate

from app.db.base import User
from app.models.role import Role, RoleName
from app.core.security import get_password_hash

class TeacherService:
    def create_teacher(self, db: Session, *, obj_in: TeacherCreate):
        # Create user if user data provided
        if obj_in.username and obj_in.password:
            role = db.query(Role).filter(Role.name == RoleName.TEACHER).first()
            if not role:
                # Create role if doesn't exist (safety)
                role = Role(name=RoleName.TEACHER)
                db.add(role)
                db.commit()
                db.refresh(role)
            
            db_user = User(
                username=obj_in.username,
                email=obj_in.email,
                full_name=obj_in.full_name,
                hashed_password=get_password_hash(obj_in.password),
                role_id=role.id,
                is_active=True
            )
            db.add(db_user)
            db.commit()
            db.refresh(db_user)
            
            teacher_data = obj_in.model_dump(exclude={"username", "email", "password", "full_name", "user_id"})
            db_teacher = Teacher(**teacher_data, user_id=db_user.id)
            db.add(db_teacher)
            db.commit()
            db.refresh(db_teacher)
            return db_teacher
        
        return teacher_repo.create(db, obj_in=obj_in)

    def get_teacher(self, db: Session, id: int):
        return teacher_repo.get(db, id=id)

    def get_teachers(self, db: Session, skip: int = 0, limit: int = 100):
        return teacher_repo.get_multi(db, skip=skip, limit=limit)

    def assign_subject(self, db: Session, *, teacher_id: int, subject_id: int):
        teacher = teacher_repo.get(db, id=teacher_id)
        subject = db.query(Subject).filter(Subject.id == subject_id).first()
        if teacher and subject:
            if subject not in teacher.subjects:
                teacher.subjects.append(subject)
                db.add(teacher)
                db.commit()
                db.refresh(teacher)
        return teacher

teacher_service = TeacherService()
