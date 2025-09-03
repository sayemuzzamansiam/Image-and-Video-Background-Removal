# Uses `rembg` under the hood (U2-Net wrapper). See requirements.txt.

# app/service/image_service.py

from rembg import remove
from PIL import Image  # <-- Import the Image module from Pillow
from io import BytesIO # <-- Import BytesIO to handle bytes as files


# Define the fixed output size you want (width, height)
FIXED_SIZE = (500, 500)


def remove_bg_image(image_bytes: bytes) -> bytes:
    """Return PNG bytes with transparent background."""
    output_bytes_with_bg_removed = remove(image_bytes)

    # Step 2: Open the resulting image with Pillow
    # We use BytesIO to treat the bytes as a file-like object
    img = Image.open(BytesIO(output_bytes_with_bg_removed))

    # Step 3: Resize the image to the fixed size.
    # Image.Resampling.LANCZOS is a high-quality filter for downscaling.
    img_resized = img.resize(FIXED_SIZE, Image.Resampling.LANCZOS)

    # Step 4: Save the resized image back to a bytes buffer
    # We must specify the format as PNG to preserve the transparency.
    out_buffer = BytesIO()
    img_resized.save(out_buffer, format="PNG")
    
    # Get the bytes value from the buffer and return it
    final_bytes = out_buffer.getvalue()
    
    return final_bytes
