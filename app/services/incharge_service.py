from sqlalchemy.orm import Session
from app.models.incharge import Incharge
from app.models.user import User
from app.models.role import Role, RoleName
from app.core.security import get_password_hash
from app.schemas.incharge import InchargeCreate, InchargeUpdate

class InchargeService:
    def create_incharge(self, db: Session, *, obj_in: InchargeCreate):
        # Create user if user data provided
        if obj_in.username and obj_in.password:
            role = db.query(Role).filter(Role.name == RoleName.INCHARGE).first()
            if not role:
                role = Role(name=RoleName.INCHARGE)
                db.add(role)
                db.commit()
                db.refresh(role)
            
            db_user = User(
                username=obj_in.username,
                email=obj_in.email,
                full_name=obj_in.full_name,
                hashed_password=get_password_hash(obj_in.password),
                role_id=role.id,
                is_active=True
            )
            db.add(db_user)
            db.commit()
            db.refresh(db_user)
            
            incharge_data = obj_in.model_dump(exclude={"username", "email", "password", "full_name", "user_id"})
            db_incharge = Incharge(**incharge_data, user_id=db_user.id)
            db.add(db_incharge)
            db.commit()
            db.refresh(db_incharge)
            return db_incharge
        
        # Else just create profile if user_id linked
        db_obj = Incharge(**obj_in.model_dump())
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_incharge(self, db: Session, id: int):
        return db.query(Incharge).filter(Incharge.id == id).first()

    def get_incharges(self, db: Session, skip: int = 0, limit: int = 100):
        return db.query(Incharge).offset(skip).limit(limit).all()

incharge_service = InchargeService()
