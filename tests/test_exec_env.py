import os
import requests
import subprocess
import sys
import time
import pytest

import threading
from fastapi import FastAPI
from fastapi.testclient import TestClient


# Ensure parent dir is in sys.path so mcp_vision_adapter is importable as a package
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import mcp_vision_adapter.main as main_mod

app = main_mod.app
client = TestClient(app)

def test_execute_env_var(monkeypatch):
    resp = client.post("/", json={
        "jsonrpc": "2.0",
        "id": 1,
        "method": "tools/call",
        "params": {
            "tool": "detect_objects",
            "input": {"image_path": "test.jpg"}
        }
    })
    assert resp.status_code == 200
    # Artık override yok, gerçek nesne tespiti sonucu beklenir
    assert isinstance(resp.json()["result"], str)
