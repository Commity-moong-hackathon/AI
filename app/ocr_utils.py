import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "credentials/gcp.json"

from google.cloud import vision
from google.cloud.vision_v1 import types
from PIL import Image

def resize_image(input_path, output_path, max_width=2000):
    with Image.open(input_path) as img:
        if img.mode == "RGBA":
            img = img.convert("RGB")

        if img.width > max_width:
            ratio = max_width / float(img.width)
            new_height = int(float(img.height) * ratio)
            img = img.resize((max_width, new_height), Image.LANCZOS)
        img.save(output_path, format='JPEG', optimize=True)


def extract_text(image_path: str) -> str:
    resized_path = "resized_" + os.path.basename(image_path)
    resize_image(image_path, resized_path)

    client = vision.ImageAnnotatorClient()
    with open(resized_path, "rb") as img_file:
        content = img_file.read()

    image = types.Image(content=content)
    response = client.document_text_detection(image=image)

    os.remove(resized_path)

    if response.error.message:
        raise Exception(f"Vision API Error: {response.error.message}")

    return response.full_text_annotation.text if response.full_text_annotation else ""
