from typing import Generator, List
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session

from app.core import security
from app.core.config import settings
from app.db.session import get_db
from app.db.base import User
from app.models.role import RoleName
from app.schemas.user import TokenPayload

reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/auth/login"
)

def get_current_user(
    db: Session = Depends(get_db), token: str = Depends(reusable_oauth2)
) -> User:
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        token_data = TokenPayload(**payload)
    except (JWTError, Exception):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    user = db.query(User).filter(User.id == token_data.sub).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

def get_current_active_user(
    current_user: User = Depends(get_current_user),
) -> User:
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

class PermissionChecker:
    def __init__(self, allowed_roles: List[RoleName], required_permission: str = None):
        self.allowed_roles = allowed_roles
        self.required_permission = required_permission

    def __call__(self, user: User = Depends(get_current_active_user)):
        # Admin has full access
        if user.role.name == RoleName.ADMIN:
            return user
            
        # Check role permission
        if user.role.name not in [role.value for role in self.allowed_roles]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="The user doesn't have enough privileges",
            )
            
        # Check granular permission for Incharges
        if user.role.name == RoleName.INCHARGE and self.required_permission:
            if not user.incharge_profile or self.required_permission not in (user.incharge_profile.permissions or []):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"User is missing granular permission: {self.required_permission}",
                )
                
        return user
