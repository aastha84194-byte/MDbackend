from pydantic import BaseModel, EmailStr
from typing import Optional

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenPayload(BaseModel):
    sub: Optional[int] = None

class UserBase(BaseModel):
    username: str
    email: EmailStr
    full_name: Optional[str] = None
    is_active: Optional[bool] = True

class UserCreate(UserBase):
    password: str
    role_id: int

class UserUpdate(UserBase):
    password: Optional[str] = None

class RoleOut(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True

class UserOut(UserBase):
    id: int
    role_id: int
    role: Optional[RoleOut] = None

    class Config:
        from_attributes = True

class LoginRequest(BaseModel):
    username_or_email: str
    password: str
