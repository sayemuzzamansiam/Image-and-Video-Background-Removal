# app/api/endpoints/image.py

from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import StreamingResponse
from app.service.image_service import remove_bg_image
from io import BytesIO


router = APIRouter()


@router.post("/image")
async def remove_bg_image_endpoint(file: UploadFile = File(...)):
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image")

    contents = await file.read()
    out_bytes = remove_bg_image(contents)
    return StreamingResponse(BytesIO(out_bytes), media_type="image/png")