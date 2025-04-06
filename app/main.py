import app.config
from fastapi import FastAPI, UploadFile, File
from app.ocr_utils import process_student_card
import uuid
import os

app = FastAPI()

UPLOAD_DIR = "temp"

@app.post("/upload-student-card")
async def upload_student_card(file: UploadFile = File(...)):
    os.makedirs(UPLOAD_DIR, exist_ok=True)

    filename = f"{uuid.uuid4()}.jpeg"
    file_path = os.path.join(UPLOAD_DIR, filename)

    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())

    result = process_student_card(file_path)
    return result