from typing import List
from pydantic_settings import BaseSettings
from pydantic import AnyHttpUrl

class Settings(BaseSettings):
    PROJECT_NAME: str = "School Management System"
    API_V1_STR: str = "/api/v1"
    
    # DATABASE
    # Example: postgresql://user:password@localhost:5432/dbname
    DATABASE_URL: str = "postgresql://neondb_owner:npg_vhDAxHuYd39C@ep-fancy-poetry-an7klqaq-pooler.c-6.us-east-1.aws.neon.tech/neondb?sslmode=require"
    
    # SECURITY
    SECRET_KEY: str = "bde10063b255b2a323a75c3bbf6e2dab01f6e436b91640ccda7d9b5131f386ce02bb463d"  # Change in production
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days
    
    # CORS
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

    class Config:
        case_sensitive = True
        env_file = ".env"

settings = Settings()
