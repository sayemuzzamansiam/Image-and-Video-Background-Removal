# app/api/endpoints/image.py

from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import StreamingResponse
from app.service.image_service import remove_bg_image_fixed_output  
from io import BytesIO
from PIL import Image, UnidentifiedImageError

router = APIRouter()

@router.post("/image")
async def remove_bg_image_endpoint(file: UploadFile = File(...)):
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image.")

    contents = await file.read()

    try:
        Image.open(BytesIO(contents))
    except UnidentifiedImageError:
        raise HTTPException(status_code=400, detail="Invalid or corrupt image file.")

    try:
        out_bytes = remove_bg_image_fixed_output(contents)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Image processing failed: {str(e)}")

    return StreamingResponse(BytesIO(out_bytes), media_type="image/png")
