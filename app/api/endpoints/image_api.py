# app/api/endpoints/image_api.py

import requests
from fastapi import APIRouter, UploadFile, File, HTTPException, Response
from pydantic import ValidationError
from PIL import Image
from io import BytesIO

# 1. Import your settings object and Pydantic model
from app.core.config import settings
from app.api.models.image_model import ImageSize

router = APIRouter()


@router.post("/image")
async def remove_bg_image_endpoint(file: UploadFile = File(...)):
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image.")

    contents = await file.read()

    # 2. Your input validation logic remains the same
    try:
        img = Image.open(BytesIO(contents))
        width, height = img.size
        ImageSize(width=width, height=height)
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid or corrupt image file.")

    # 3. Call the ClipDrop external API using your settings
    api_url = f"{settings.CLIPDROP_API_BASE_URL}/remove-background/v1"
    try:
        response = requests.post(
            api_url,
            files={
                'image_file': BytesIO(contents)
            },
            headers={
                # Use the API key loaded from your .env file
                'x-api-key': settings.CLIPDROP_API_KEY
            },
        )
        response.raise_for_status() # Raise an exception for errors (e.g., 403 Forbidden)

        # 4. Return the processed image from ClipDrop
        return Response(content=response.content, media_type="image/png")

    except requests.exceptions.HTTPError as e:
        # Provide a detailed error if the API call fails
        error_detail = f"ClipDrop API Error ({e.response.status_code}): {e.response.text}"
        raise HTTPException(status_code=e.response.status_code, detail=error_detail)
    except requests.exceptions.RequestException as e:
        # Handle network-related errors
        raise HTTPException(status_code=502, detail=f"Error contacting the background removal service: {e}")