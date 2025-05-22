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
    monkeypatch.setenv("MANUAL_RESULT", "stub")
    resp = client.post("/execute", json={
        "tool": "detect_objects",
        "input": {"image_path": "test.jpg"}
    })
    assert resp.status_code == 200
    assert resp.json()["result"] == "stub"
