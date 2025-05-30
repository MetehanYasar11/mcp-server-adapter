def test_detect_video_time_slice():
    """Test detection on a video file with time slicing (start/end)."""
    video_path = os.path.join(os.path.dirname(__file__), '../test.mp4')
    if not os.path.exists(video_path):
        pytest.skip("test.mp4 not found")
    with open(video_path, 'rb') as f:
        # Only detect objects in the first 2 seconds
        resp = client.post('/detect?start=0&end=2', files={'file': ('test.mp4', f, 'video/mp4')})
        assert resp.status_code == 200
        data = resp.json()
        assert 'results' in data
        assert isinstance(data['results'], list)
        # There should be at least one detection or an empty list
import os
import sys
import pytest
from fastapi.testclient import TestClient

# Ensure yolov8_service/app is importable as a package
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../yolov8_service')))
from app.main import app

client = TestClient(app)

def test_detect_jpg():
    with open(os.path.join(os.path.dirname(__file__), '../test.jpg'), 'rb') as f:
        resp = client.post('/detect', files={'file': ('test.jpg', f, 'image/jpeg')})
        assert resp.status_code == 200
        data = resp.json()
        assert 'results' in data
        assert isinstance(data['results'], list)
        assert len(data['results']) >= 1
