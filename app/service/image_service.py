# Uses `rembg` under the hood (U2-Net wrapper). See requirements.txt.

# app/service/image_service.py

from rembg import remove


def remove_bg_image(image_bytes: bytes) -> bytes:
    """Return PNG bytes with transparent background."""
    output = remove(image_bytes)
    return output