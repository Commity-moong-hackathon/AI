import app.config
from fastapi import FastAPI, UploadFile, File, Form
from app.ocr_utils import extract_text
from app.parser.factory import parse_by_type 
import uuid
import os

app = FastAPI(title ='OCR Uplaod API', description='양식별 ocr 추출')


@app.post("/ocr/upload")
async def upload_ocr_img(
    file: UploadFile = File(...),
    form_type: str = Form(...)
):
    try:
        temp_path = f"temp_{file.filename}"
        with open(temp_path, "wb") as f:
            f.write(await file.read())

        from app.ocr_utils import extract_text
        text = extract_text(temp_path)

        from app.parser.factory import parse_by_type
        parsed = parse_by_type(form_type, text)

        os.remove(temp_path)

        return {"parsed": parsed}
    except Exception as e:
        import traceback
        return {
            "error": str(e),
            "trace": traceback.format_exc()
        }
