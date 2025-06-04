import os
import sys
import pytest
from fastapi.testclient import TestClient

# Ensure package import
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import mcp_vision_adapter.main as main_mod

client = TestClient(main_mod.app)


def test_initialize_http_protocol_version():
    resp = client.post("/initialize")
    assert resp.status_code == 200
    data = resp.json()
    assert data["result"]["protocolVersion"].startswith("2024-")


def test_manifest_includes_detect_objects():
    resp = client.get("/manifest")
    assert resp.status_code == 200
    data = resp.json()
    assert "tools" in data
    assert any(t.get("name") == "detect_objects" for t in data["tools"])
