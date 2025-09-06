# app/api/endpoints/image.py

from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import StreamingResponse
from app.service.image_service import remove_bg_image_fixed_output  # Updated import
from io import BytesIO
from PIL import Image, UnidentifiedImageError

router = APIRouter()

@router.post("/image")
async def remove_bg_image_endpoint(file: UploadFile = File(...)):
    # Step 1: Check if the file is an image
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image.")

    contents = await file.read()

    # Step 2: Validate image file (not corrupt)
    try:
        Image.open(BytesIO(contents))
    except UnidentifiedImageError:
        raise HTTPException(status_code=400, detail="Invalid or corrupt image file.")

    # Step 3: Process image (resize -> remove BG -> center on fixed canvas)
    try:
        out_bytes = remove_bg_image_fixed_output(contents)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Image processing failed: {str(e)}")

    # Step 4: Return processed image as PNG
    return StreamingResponse(BytesIO(out_bytes), media_type="image/png")
