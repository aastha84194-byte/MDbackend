from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.api import deps
from app.db.session import get_db
from app.services.notification_service import notification_service
from app.schemas.notifications import AnnouncementCreate, AnnouncementOut
from app.models.role import RoleName

router = APIRouter()

@router.post("/", response_model=AnnouncementOut)
def create_announcement(
    *,
    db: Session = Depends(get_db),
    announcement_in: AnnouncementCreate,
    current_user = Depends(deps.PermissionChecker([RoleName.ADMIN, RoleName.INCHARGE]))
) -> Any:
    """
    Create a new announcement. (Admin or Incharge only)
    """
    return notification_service.create_announcement(db, obj_in=announcement_in, author_id=current_user.id)

@router.get("/", response_model=List[AnnouncementOut])
def read_announcements(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 50,
    current_user = Depends(deps.get_current_active_user)
) -> Any:
    """
    Retrieve announcements. (All active users)
    """
    return notification_service.get_announcements(db, skip=skip, limit=limit)
