from app.db.base import Base # Ensure all models are registered
from app.db.session import SessionLocal
from app.models.role import Role, RoleName
from app.db.base import User
from app.core.security import get_password_hash

def seed_db():
    db = SessionLocal()
    try:
        # 1. Create Roles
        for role_name in RoleName:
            role = db.query(Role).filter(Role.name == role_name.value).first()
            if not role:
                role = Role(name=role_name.value, description=f"{role_name.value.capitalize()} role")
                db.add(role)
        db.commit()

        # 2. Create Default Admin
        admin_role = db.query(Role).filter(Role.name == RoleName.ADMIN.value).first()
        admin_user = db.query(User).filter(User.username == "admin").first()
        if not admin_user:
            admin_user = User(
                username="admin",
                email="admin@mdpic.edu.in",
                hashed_password=get_password_hash("admin123"),
                full_name="System Administrator",
                role_id=admin_role.id
            )
            db.add(admin_user)
            db.commit()
            print("Admin user created successfully!")
        else:
            print("Admin user already exists.")

    finally:
        db.close()

if __name__ == "__main__":
    seed_db()
