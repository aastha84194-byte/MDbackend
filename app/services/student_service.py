import pandas as pd
import io
from sqlalchemy.orm import Session
from app.repositories.student_repository import student_repo
from app.models.user import User
from app.models.role import Role, RoleName
from app.models.guardian import Guardian
from app.models.academic import SchoolClass
from app.schemas.student import StudentCreate, StudentUpdate
from app.core import security

class StudentService:
    def create_student(self, db: Session, *, obj_in: StudentCreate):
        # 1. Get student role
        role = db.query(Role).filter(Role.name == RoleName.STUDENT).first()
        if not role:
            # Fallback or create role if doesn't exist (though it should be seeded)
            role = Role(name=RoleName.STUDENT)
            db.add(role)
            db.commit()
            db.refresh(role)
        
        # 2. Generate username: name + admission_no
        # Remove spaces and lowercase name
        clean_name = obj_in.full_name.lower().replace(" ", "")
        username = f"{clean_name}{obj_in.admission_number}"
        
        # 3. Create User
        user_db = User(
            username=username,
            hashed_password=security.get_password_hash("user1"),
            full_name=obj_in.full_name,
            role_id=role.id,
            email=None # Email is now optional
        )
        db.add(user_db)
        db.commit()
        db.refresh(user_db)
        
        # 4. Create Student linked to User
        student_data = obj_in.model_dump(exclude={"guardian"})
        student_data.pop("full_name", None)
        
        db_student = student_repo.model(
            **student_data,
            user_id=user_db.id
        )
        db.add(db_student)
        db.commit()
        db.refresh(db_student)

        # 5. Create Guardian linked to Student
        if obj_in.guardian:
            guardian_data = obj_in.guardian.model_dump()
            db_guardian = Guardian(**guardian_data, student_id=db_student.id)
            db.add(db_guardian)
            db.commit()
            db.refresh(db_guardian)
            
        return db_student

    def import_students_from_excel(self, db: Session, *, file_content: bytes):
        df = pd.read_excel(io.BytesIO(file_content), engine='openpyxl')
        
        results = {"total": 0, "imported": 0, "errors": []}
        
        for index, row in df.iterrows():
            try:
                # 1. Basic Identity
                full_name = str(row.get('Name of the Student\n(Mandatory)', '')).strip()
                admission_number = str(row.get('Admission Number\n(Mandatory)', '')).strip()
                if not full_name or not admission_number or full_name == 'nan' or admission_number == 'nan':
                    continue
                
                results["total"] += 1
                
                # 2. Student Details
                dob = str(row.get('Date of Birth\n(DD/MM/YYYY) (Mandatory)', ''))
                gender = str(row.get('Gender\n(Mandatory)\n\n', ''))
                aadhaar = str(row.get("Student's  AADHAAR Number\n\n", ''))
                religion = str(row.get('Religion (Mandatory)', ''))
                social_cat = str(row.get('Social Category\n(Mandatory)\n\n', ''))
                mother_tongue = str(row.get('Mother Tongue (Mandatory)', ''))
                admission_date = str(row.get('Date of Admission (DD/MM/YYYY)\n(Mandatory)', ''))
                habitation = str(row.get('Habitation or Locality\n', ''))
                is_bpl_str = str(row.get('Whether belong to BPL\n(Mandatory)', '')).lower()
                is_bpl = 'yes' in is_bpl_str or '1' in is_bpl_str
                
                class_info = str(row.get('Studying in Class\n', ''))
                class_id = None
                if class_info and class_info != 'nan':
                    class_nums = "".join(filter(str.isdigit, class_info))
                    if class_nums:
                        class_obj = db.query(SchoolClass).filter(SchoolClass.class_number == int(class_nums)).first()
                        if class_obj:
                            class_id = class_obj.id
                
                # 3. Guardian Details
                father_name = str(row.get("Father's Name\n(Mandatory)", ''))
                mother_name = str(row.get("Mother's Name (Mandatory)", ''))
                guardian_name = str(row.get('Guardian Name', ''))
                parent_aadhaar = str(row.get('Aadhaar Number of Parent / Guardian', ''))
                parent_contact = str(row.get('Contact Number (of Parent / Guardian)', ''))
                parent_email = str(row.get('Email Address (of Parent / Guardian)', ''))
                
                # Clean 'nan' values
                def clean(v): return v if v != 'nan' and v else None

                guardian_in = GuardianCreate(
                    father_name=clean(father_name),
                    mother_name=clean(mother_name),
                    guardian_name=clean(guardian_name),
                    aadhaar_number=clean(parent_aadhaar),
                    contact_number=clean(parent_contact),
                    email=clean(parent_email)
                )

                student_in = StudentCreate(
                    admission_number=admission_number,
                    full_name=full_name,
                    date_of_birth=clean(dob),
                    gender=clean(gender),
                    aadhaar_number=clean(aadhaar),
                    religion=clean(religion),
                    social_category=clean(social_cat),
                    mother_tongue=clean(mother_tongue),
                    date_of_admission=clean(admission_date),
                    is_bpl=is_bpl,
                    habitation=clean(habitation),
                    address=clean(habitation), # Fallback address to habitation
                    class_id=class_id,
                    guardian=guardian_in
                )
                
                self.create_student(db, obj_in=student_in)
                results["imported"] += 1
                
            except Exception as e:
                results["errors"].append(f"Row {index + 1}: {str(e)}")
        
        return results

    def get_student(self, db: Session, id: int):
        return student_repo.get(db, id=id)

    def get_students(self, db: Session, skip: int = 0, limit: int = 100):
        return student_repo.get_multi(db, skip=skip, limit=limit)

student_service = StudentService()
