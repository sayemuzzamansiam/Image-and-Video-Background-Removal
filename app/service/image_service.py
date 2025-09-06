# app/service/image_service.py

from rembg import remove
from PIL import Image
from io import BytesIO

ID_CARD_SIZE = (300, 400)  # Custom size for ID card (width, height), adjustable as needed

def remove_bg_image(image_bytes: bytes) -> bytes:
    """Return PNG bytes with transparent background and centered subject for ID card."""
    # Remove background using rembg
    output_bytes_with_bg_removed = remove(image_bytes)

    # Open the image
    img = Image.open(BytesIO(output_bytes_with_bg_removed))
    if img.mode != 'RGBA':
        img = img.convert('RGBA')  # Ensure RGBA for transparency

    # Step 1: Get bounding box of non-transparent area (auto detection)
    bbox = img.getbbox()  # Returns (left, upper, right, lower) or None if empty
    if not bbox:
        raise ValueError("No subject detected after background removal.")

    # Step 2: Crop to the subject
    subject = img.crop(bbox)

    # Step 3: Resize subject to fit within ID_CARD_SIZE, preserving aspect ratio
    # Calculate the scaling factor to fit the larger dimension of the canvas
    subject_ratio = subject.width / subject.height
    canvas_ratio = ID_CARD_SIZE[0] / ID_CARD_SIZE[1]
    if subject_ratio > canvas_ratio:
        # Fit to width
        scale = ID_CARD_SIZE[0] / subject.width
    else:
        # Fit to height
        scale = ID_CARD_SIZE[1] / subject.height
    new_width = int(subject.width * scale)
    new_height = int(subject.height * scale)
    subject_resized = subject.resize((new_width, new_height), Image.Resampling.LANCZOS)

    # Debug: Print dimensions to verify
    print(f"Original subject size: {subject.width}x{subject.height}")
    print(f"Resized subject size: {subject_resized.width}x{subject_resized.height}")
    print(f"Canvas size: {ID_CARD_SIZE[0]}x{ID_CARD_SIZE[1]}")
    print(f"Calculated offsets: x={(ID_CARD_SIZE[0] - subject_resized.width) // 2}, y={(ID_CARD_SIZE[1] - subject_resized.height) // 2}")

    # Step 4: Create a new canvas (white background for ID card)
    canvas = Image.new('RGBA', ID_CARD_SIZE, (255, 255, 255, 255))  # White background

    # Step 5: Calculate exact center position with padding
    x_offset = (ID_CARD_SIZE[0] - subject_resized.width) // 2
    y_offset = (ID_CARD_SIZE[1] - subject_resized.height) // 2

    # Step 6: Paste subject onto canvas at the center
    canvas.paste(subject_resized, (x_offset, y_offset), subject_resized)  # Use subject as mask for transparency

    # Step 7: Save to bytes
    out_buffer = BytesIO()
    canvas.save(out_buffer, format="PNG")
    final_bytes = out_buffer.getvalue()

    return final_bytes