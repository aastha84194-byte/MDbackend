# School Management System Backend

A robust, scalable backend for a school management system built with FastAPI, PostgreSQL, and Clean Architecture.

## Features
- **RBAC Authentication**: Secure login via username or email with roles (Admin, Teacher, Student, Financial Admin, Incharge).
- **Academic Core**: Class and Subject management with teacher-subject allocation.
- **Student & Teacher Management**: Comprehensive profiles and CRUD operations.
- **Attendance**: Marking and reporting for both students and staff.
- **Exams & Results**: Support for different exam types (Class Tests, Finals) with mark aggregation.
- **Fees**: Class-wise fee structures and payment tracking.
- **Public Forms**: Admission and Contact Us inquiries.
- **Staff Management**: Leave tracking and salary management.
- **Notifications**: School-wide announcement system.

## Project Structure
```text
app/
├── main.py          # Entry point
├── core/            # Config, Security
├── models/          # SQLAlchemy Models
├── schemas/         # Pydantic Schemas
├── api/             # Routes & Dependencies
├── services/        # Business Logic
├── repositories/    # Database Access
├── db/              # Session Management
└── utils/           # Utilities (Media, etc.)
```

## Setup & Running
1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
2. **Configure Database**:
   Update `app/core/config.py` with your PostgreSQL credentials.
3. **Run Migrations**:
   ```bash
   alembic upgrade head
   ```
4. **Start Application**:
   ```bash
   uvicorn app.main:app --reload
   ```
5. **API Documentation**:
   Visit `http://localhost:8000/docs` for interactive Swagger UI.

## Security
- Password hashing with Bcrypt.
- JWT-based authorization.
- Role-based middleware for endpoint protection.
