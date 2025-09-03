# app/api/endpoints/video.py

from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import StreamingResponse
from app.service.video_service import remove_bg_video_bytes
from io import BytesIO


router = APIRouter()


@router.post("/video")
async def remove_bg_video_endpoint(file: UploadFile = File(...)):
    if not file.content_type.startswith("video/"):
        raise HTTPException(status_code=400, detail="File must be a video")

    contents = await file.read()
    out_bytes = remove_bg_video_bytes(contents)

    # --- THIS IS THE LINE TO CHANGE ---
    # We are adding the headers argument to suggest a filename
    headers = {
        'Content-Disposition': 'attachment; filename="processed_video.mp4"'
    }
    
    return StreamingResponse(BytesIO(out_bytes), media_type="video/mp4", headers=headers)