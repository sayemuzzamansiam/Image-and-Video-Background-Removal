# app/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Import routers
from app.api.endpoints import image, video, img_slazzer  # Removed image_api (ClipDrop)

app = FastAPI(
    docs_url="/ui",
    redoc_url="/swagger",
    title="BG Removal API",
    description="API for removing background from images and videos",
    version="0.0.1",
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"]
)

# Include routers
app.include_router(image.router, prefix="/remove-bg")  # Local model for images
app.include_router(video.router, prefix="/remove-bg")  # Local model for videos
app.include_router(img_slazzer.router, prefix="/remove-bg-api")  # Slazzer API integration

@app.get("/")
async def root():
    return {"message": "Welcome to the Background Removal API. Visit /ui for the interactive docs."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="127.0.0.1", port=7000, reload=True)
