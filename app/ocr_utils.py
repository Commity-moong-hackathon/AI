import app.config

from google.cloud import vision
from PIL import Image
import io
import os
import re

# 이미지 리사이즈
def resize_image(input_path, output_path, max_width=2000):
    with Image.open(input_path) as img:
        if img.width > max_width:
            ratio = max_width / float(img.width)
            new_height = int((float(img.height) * float(ratio)))
            img = img.resize((max_width, new_height), Image.LANCZOS)
        img.save(output_path, format='JPEG', optimize=True)

# OCR + 파싱
def process_student_card(image_path):
    resized_path = image_path.replace(".jpg", "_resized.jpg")
    resize_image(image_path, resized_path)

    client = vision.ImageAnnotatorClient()
    with io.open(resized_path, "rb") as image_file:
        content = image_file.read()

    image = vision.Image(content=content)
    response = client.text_detection(image=image)
    texts = response.text_annotations

    full_text = texts[0].description if texts else ""

    return extract_student_info(full_text)

# 텍스트 정보 
def extract_student_info(text):
    lines = text.strip().split("\n")

    info = {
        "univ": None,
        "major": None,
        "name": None,
        "student_number": None
    }

    for line in lines:
        if re.fullmatch(r'\d{7,10}', line):
            info["student_number"] = line

        elif "학교" in line:
            tokens = line.split()
            for token in tokens:
                if token.endswith("대학교총장"):
                    info["univ"] = token.replace("총장", "")
                    break
                elif token.endswith("대학교"):
                    info["univ"] = token
                    break

        elif "과" in line:
            tokens = line.split()
            for token in tokens:
                if (
                    token.endswith("학과")
                    and "학부" not in token
                    and "/" not in token
                    and all('\uac00' <= c <= '\ud7a3' for c in token)
                ):
                    info["major"] = token
                    break
                
        elif len(line.strip()) == 3 and all('\uac00' <= c <= '\ud7a3' for c in line.strip()):
            info["name"] = line.strip()

    return info