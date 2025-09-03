# app/workers/video_tasks.py

# Optional: run heavy video tasks in background using Celery.
# Save but you can ignore if not using Celery now.
from celery import Celery
from app.core.config import settings
from app.service.video_service import remove_bg_video_bytes


celery = Celery('worker', broker=settings.redis_url, backend=settings.redis_url)


@celery.task(bind=True)
def process_video(self, video_bytes):
    out = remove_bg_video_bytes(video_bytes)
    return out