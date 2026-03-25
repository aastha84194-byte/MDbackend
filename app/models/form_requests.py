from sqlalchemy import Column, Integer, String, Text, DateTime
from app.db.session import Base
from datetime import datetime

class AdmissionForm(Base):
    __tablename__ = "admission_forms"

    id = Column(Integer, primary_key=True, index=True)
    student_name = Column(String, nullable=False)
    parent_name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    previous_school = Column(String, nullable=True)
    requested_class = Column(String, nullable=False)
    status = Column(String, default="pending")  # "pending", "reviewed", "accepted", "rejected"
    created_at = Column(DateTime, default=datetime.utcnow)

class ContactUs(Base):
    __tablename__ = "contact_us"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    subject = Column(String, nullable=False)
    message = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
