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
