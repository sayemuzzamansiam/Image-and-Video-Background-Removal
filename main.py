# app/main.py

from fastapi import FastAPI
from app.api.endpoints import image, video
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(
    
    docs_url="/ui",
    redoc_url="/swagger",
    title="BG Removal API",
    description="API for removing background from images and videos",
    version="0.0.1",
)

# CORS configuration: Cross Origin Resource Sharing
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],    # Allows requests from any origin (any domain)
    allow_credentials=True, # Allows cookies, authorization headers, or TLS client certificates to be included in requests
    allow_methods=["*"],    # Allows all HTTP methods (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],    # Allows all headers to be sent by the client
    expose_headers=["*"]    # Allows all headers to be exposed to the client in the response
)


# Include routers for different API endpoints:
# app.include_router(health.router, prefix="/health")
app.include_router(image.router, prefix="/remove-bg")
app.include_router(video.router, prefix="/remove-bg")


@app.get("/")
async def root():
    return {"message": "Welcome to the Background Removal API. Visit /ui for the interactive docs."}

# Run the application: change host and port as needed
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.122.0.0", port=7000, reload=True)