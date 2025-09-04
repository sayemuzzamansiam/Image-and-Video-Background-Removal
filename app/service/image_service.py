
# app/service/image_service.py

from rembg import remove
from PIL import Image  
from io import BytesIO 


FIXED_SIZE = (170, 170)

def remove_bg_image(image_bytes: bytes) -> bytes:
    """Return PNG bytes with transparent background."""
    output_bytes_with_bg_removed = remove(image_bytes)

    img = Image.open(BytesIO(output_bytes_with_bg_removed))
    img_resized = img.resize(FIXED_SIZE, Image.Resampling.LANCZOS)

    out_buffer = BytesIO()
    img_resized.save(out_buffer, format="PNG")
    
    final_bytes = out_buffer.getvalue()
    
    return final_bytes
