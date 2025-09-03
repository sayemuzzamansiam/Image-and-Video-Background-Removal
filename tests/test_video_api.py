from fastapi.testclient import TestClient
from app.main import app


client = TestClient(app)


# Video endpoint smoke test:
# def test_remove_video():
# with open('tests/sample.mp4', 'rb') as f:
# r = client.post('/remove-bg/video', files={'file': ('sample.mp4', f, 'video/mp4')})
# assert r.status_code == 200