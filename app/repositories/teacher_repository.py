from app.repositories.base import BaseRepository
from app.models.teacher import Teacher
from app.schemas.teacher import TeacherCreate, TeacherUpdate

class TeacherRepository(BaseRepository[Teacher, TeacherCreate, TeacherUpdate]):
    pass

teacher_repo = TeacherRepository(Teacher)
