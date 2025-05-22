import os
import sys
import pytest
from fastapi.testclient import TestClient

# Ensure mcp_vision_adapter is importable
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import mcp_vision_adapter.main as main_mod

client = TestClient(main_mod.app)

def test_detect_objects_proxy(monkeypatch):
    # Point to local YOLO service (assume running on 8080)
    monkeypatch.setenv("YOLO_SERVICE_URL", "http://localhost:8080")
    # Ensure MANUAL_RESULT is not set so fallback is not triggered
    monkeypatch.delenv("MANUAL_RESULT", raising=False)
    test_img = os.path.join(os.path.dirname(__file__), '../test.jpg')
    if not os.path.exists(test_img):
        pytest.skip("test.jpg not found")
    resp = client.post("/", json={
        "jsonrpc": "2.0",
        "id": 1,
        "method": "tools/call",
        "params": {
            "tool": "detect_objects",
            "input": {"image_path": test_img}
        }
    })
    assert resp.status_code == 200
    result = resp.json()["result"]
    assert isinstance(result, str)
    assert any(cls in result for cls in ["person", "sports ball", "car", "cat", "dog"]) or "No objects detected" in result
