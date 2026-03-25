import app.db.base as _ # This MUST be imported to register models
from app.db.session import engine, Base
from app.core.seed import seed_db

def recreate_and_seed():
    print("Dropping all tables...")
    Base.metadata.drop_all(bind=engine)
    print("Creating all tables with new schema...")
    Base.metadata.create_all(bind=engine)
    print("Seeding initial data...")
    seed_db()
    print("Success! Database schema is now aligned with models.")

if __name__ == "__main__":
    recreate_and_seed()
