from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import auth, students, teachers, attendance, exams, fees, staff_forms, notifications, admin, academic
from app.core.config import settings

app = FastAPI(
    title="School Management System API",
    description="Backend for School Management System with RBAC, Exam, and Attendance modules.",
    version="1.0.0",
)

# Set all CORS enabled origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix=f"{settings.API_V1_STR}/auth", tags=["auth"])
app.include_router(admin.router, prefix=f"{settings.API_V1_STR}/admin", tags=["admin"])
app.include_router(students.router, prefix=f"{settings.API_V1_STR}/students", tags=["students"])
app.include_router(teachers.router, prefix=f"{settings.API_V1_STR}/teachers", tags=["teachers"])
app.include_router(attendance.router, prefix=f"{settings.API_V1_STR}/attendance", tags=["attendance"])
app.include_router(exams.router, prefix=f"{settings.API_V1_STR}/exams", tags=["exams"])
app.include_router(fees.router, prefix=f"{settings.API_V1_STR}/fees", tags=["fees"])
app.include_router(staff_forms.router, prefix=f"{settings.API_V1_STR}/staff-forms", tags=["staff-forms"])
app.include_router(academic.router, prefix=f"{settings.API_V1_STR}/academic", tags=["academic"])
app.include_router(notifications.router, prefix=f"{settings.API_V1_STR}/notifications", tags=["notifications"])

@app.get("/")
async def root():
    return {"message": "Welcome to the School Management System API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
