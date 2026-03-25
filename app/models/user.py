from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.db.session import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=True)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    role_id = Column(Integer, ForeignKey("roles.id"))

    role = relationship("Role", back_populates="users")
    
    # One-to-one relationships for specific profiles
    student_profile = relationship("Student", back_populates="user", uselist=False)
    teacher_profile = relationship("Teacher", back_populates="user", uselist=False)
    incharge_profile = relationship("Incharge", back_populates="user", uselist=False)
