# app/main.py

from fastapi import FastAPI
from app.api.endpoints import health, image, video


app = FastAPI(title="BG Removal API")


app.include_router(health.router, prefix="/health")
app.include_router(image.router, prefix="/remove-bg")
app.include_router(video.router, prefix="/remove-bg")


@app.get("/")
async def root():
    return {"message": "BG Removal API — healthy"}