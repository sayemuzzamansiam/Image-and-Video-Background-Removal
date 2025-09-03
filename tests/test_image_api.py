from fastapi.testclient import TestClient
from app.main import app


client = TestClient(app)


def test_health():
    r = client.get('/health/')
    assert r.status_code == 200
    assert r.json()['status'] == 'ok'


# Basic image upload smoke test (requires sample file during real run)
# def test_remove_image():
# with open('tests/sample.jpg', 'rb') as f:
# r = client.post('/remove-bg/image', files={'file': ('sample.jpg', f, 'image/jpeg')})
# assert r.status_code == 200