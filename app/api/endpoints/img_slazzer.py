from fastapi import APIRouter, File, UploadFile
from fastapi.responses import StreamingResponse
from io import BytesIO
from app.service.img_slazzer_service import remove_bg_and_center_with_slazzer

router = APIRouter()

@router.post("/remove-bg-api/image")
async def remove_bg_api_image(file: UploadFile = File(...)):
    image_bytes = await file.read()

    try:
        out_bytes = remove_bg_and_center_with_slazzer(image_bytes)
        return StreamingResponse(BytesIO(out_bytes), media_type="image/png")
    except Exception as e:
        return {"error": str(e)}
