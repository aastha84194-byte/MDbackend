import os
import shutil
from fastapi import UploadFile
from app.core.config import settings

UPLOAD_DIR = "static/media"

def save_upload_file(upload_file: UploadFile, destination: str) -> str:
    if not os.path.exists(UPLOAD_DIR):
        os.makedirs(UPLOAD_DIR)
    
    file_path = os.path.join(UPLOAD_DIR, upload_file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(upload_file.file, buffer)
    
    return file_path
