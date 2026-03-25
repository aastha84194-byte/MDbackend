from sqlalchemy.orm import Session
from app.models.notifications import Announcement
from app.schemas.notifications import AnnouncementCreate

class NotificationService:
    def create_announcement(self, db: Session, *, obj_in: AnnouncementCreate, author_id: int):
        db_obj = Announcement(**obj_in.model_dump(), author_id=author_id)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_announcements(self, db: Session, skip: int = 0, limit: int = 10):
        return db.query(Announcement).order_by(Announcement.created_at.desc()).offset(skip).limit(limit).all()

notification_service = NotificationService()
