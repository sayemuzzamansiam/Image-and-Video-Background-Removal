# app/api/endpoints/image.py

from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import StreamingResponse
from app.service.image_service import remove_bg_image
from app.api.models.image_model import ImageSize # Import the model
from pydantic import ValidationError # Import Pydantic's error
from io import BytesIO
from PIL import Image


router = APIRouter()


@router.post("/image")
async def remove_bg_image_endpoint(file: UploadFile = File(...)):
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image.")

    contents = await file.read()

    # --- Pydantic Validation for Image Size ---
    try:
        # Open the image to get its dimensions
        img = Image.open(BytesIO(contents))
        width, height = img.size
        
        # Validate the dimensions using the Pydantic model
        ImageSize(width=width, height=height)

    except ValidationError as e:
        # If validation fails, return a 400 error with Pydantic's message
        raise HTTPException(status_code=400, detail=str(e))
    except Exception:
        # Catch other potential errors like corrupt image files
        raise HTTPException(status_code=400, detail="Invalid or corrupt image file.")
    # --- End of Validation ---

    out_bytes = remove_bg_image(contents)
    return StreamingResponse(BytesIO(out_bytes), media_type="image/png")