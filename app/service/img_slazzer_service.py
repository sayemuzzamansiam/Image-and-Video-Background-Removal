# app/service/img_slazzer_service.py

import requests
from io import BytesIO
from PIL import Image
from app.core.config import settings

ID_CARD_SIZE = (300, 400)  

def remove_bg_and_center_with_slazzer(image_bytes: bytes) -> bytes:
    """Remove background using Slazzer API v2.0 and center subject on canvas."""
    url = "https://api.slazzer.com/v2.0/remove_image_background"
    
    headers = {
        "API-KEY": settings.SLAZZER_API_KEY
    }

    files = {
        "source_image_file": ("input.jpg", image_bytes, "image/jpeg")
    }

    try:
        response = requests.post(url, headers=headers, files=files, timeout=30)
        response.raise_for_status()
        api_output_bytes = response.content
    except requests.HTTPError as http_err:
        print("Status:", response.status_code)
        print("Error:", response.text)
        raise ValueError(f"HTTP error: {response.text}")
    except requests.RequestException as e:
        raise ValueError(f"Request failed: {str(e)}")

    img = Image.open(BytesIO(api_output_bytes))
    if img.mode != 'RGBA':
        img = img.convert('RGBA')

    bbox = img.getbbox()
    if not bbox:
        raise ValueError("No subject detected after background removal.")

    subject = img.crop(bbox)
    subject_ratio = subject.width / subject.height
    canvas_ratio = ID_CARD_SIZE[0] / ID_CARD_SIZE[1]
    scale = ID_CARD_SIZE[0] / subject.width if subject_ratio > canvas_ratio else ID_CARD_SIZE[1] / subject.height
    new_width = int(subject.width * scale)
    new_height = int(subject.height * scale)
    subject_resized = subject.resize((new_width, new_height), Image.Resampling.LANCZOS)

    canvas = Image.new('RGBA', ID_CARD_SIZE, (255, 255, 255, 255))
    x_offset = (ID_CARD_SIZE[0] - subject_resized.width) // 2
    y_offset = (ID_CARD_SIZE[1] - subject_resized.height) // 2
    canvas.paste(subject_resized, (x_offset, y_offset), subject_resized)

    out_buffer = BytesIO()
    canvas.save(out_buffer, format="PNG")
    return out_buffer.getvalue()
