from rembg import remove
from PIL import Image, ImageOps
from io import BytesIO

OUTPUT_SIZE = (170, 170)  

def resize_and_pad(image: Image.Image, size: tuple[int, int], color=(255, 255, 255)) -> Image.Image:
    """Resize image with aspect ratio preserved and pad to fit desired size."""
    image.thumbnail(size, Image.Resampling.LANCZOS)
    delta_w = size[0] - image.width
    delta_h = size[1] - image.height
    padding = (delta_w // 2, delta_h // 2, delta_w - (delta_w // 2), delta_h - (delta_h // 2))
    return ImageOps.expand(image, padding, fill=color)

def remove_bg_image_fixed_output(image_bytes: bytes) -> bytes:
    from rembg import remove
    from PIL import Image, ImageOps
    from io import BytesIO

    OUTPUT_SIZE = (500, 500)

    # Open original image
    img = Image.open(BytesIO(image_bytes)).convert('RGBA')

    # Resize and pad to fit OUTPUT_SIZE
    img.thumbnail(OUTPUT_SIZE, Image.Resampling.LANCZOS)
    delta_w = OUTPUT_SIZE[0] - img.width
    delta_h = OUTPUT_SIZE[1] - img.height
    padding = (delta_w // 2, delta_h // 2, delta_w - delta_w // 2, delta_h - delta_h // 2)
    padded_img = ImageOps.expand(img, padding, fill=(255, 255, 255, 255))

    #  Convert resized+padded image to bytes before passing to rembg
    buffer = BytesIO()
    padded_img.save(buffer, format="PNG")
    resized_bytes = buffer.getvalue()

    output_bytes = remove(resized_bytes)

    img_no_bg = Image.open(BytesIO(output_bytes)).convert('RGBA')

    bbox = img_no_bg.getbbox()
    if not bbox:
        raise ValueError("No subject detected after background removal.")
    subject = img_no_bg.crop(bbox)

    subject.thumbnail(OUTPUT_SIZE, Image.Resampling.LANCZOS)

    canvas = Image.new('RGBA', OUTPUT_SIZE, (255, 255, 255, 255))
    x_offset = (OUTPUT_SIZE[0] - subject.width) // 2
    y_offset = (OUTPUT_SIZE[1] - subject.height) // 2
    canvas.paste(subject, (x_offset, y_offset), subject)

    output_buffer = BytesIO()
    canvas.save(output_buffer, format="PNG")
    return output_buffer.getvalue()
