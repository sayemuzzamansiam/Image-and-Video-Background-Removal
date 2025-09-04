# app/api/models/image_model.py

from pydantic import BaseModel, field_validator, ValidationError

# Define the required dimensions
REQUIRED_WIDTH = 500
REQUIRED_HEIGHT = 500

class ImageSize(BaseModel):
    width: int
    height: int

    @field_validator('width')
    def width_must_be_valid(cls, v):
        if v != REQUIRED_WIDTH:
            raise ValueError(f'Image width must be {REQUIRED_WIDTH} pixels')
        return v

    @field_validator('height')
    def height_must_be_valid(cls, v):
        if v != REQUIRED_HEIGHT:
            raise ValueError(f'Image height must be {REQUIRED_HEIGHT} pixels')
        return v