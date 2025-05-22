import pytest
from fastapi.testclient import TestClient
import mcp_vision_adapter.main as main_mod

client = TestClient(main_mod.app)

def test_tools_list_root_http():
    data = {"jsonrpc": "2.0", "id": 1, "method": "tools/list", "params": {}}
    r = client.post("/", json=data)
    assert r.status_code == 200
    body = r.json()
    assert "tools" in body["result"]
    assert any(t["name"] == "detect_objects" for t in body["result"]["tools"])

def test_initialize_root_http():
    data = {"jsonrpc": "2.0", "id": 2, "method": "initialize", "params": {}}
    r = client.post("/", json=data)
    assert r.status_code == 200
    assert r.json()["result"]["protocolVersion"].startswith("2024-")

def test_tools_call_root_http():
    data = {
        "jsonrpc": "2.0",
        "id": 3,
        "method": "tools/call",
        "params": {"tool": "detect_objects", "input": {"image_path": "test.jpg", "manual_result": "rpc_test"}}
    }
    r = client.post("/", json=data)
    assert r.status_code == 200
    assert r.json()["result"] == "rpc_test"

def test_unknown_method_root_http():
    data = {"jsonrpc": "2.0", "id": 4, "method": "nope", "params": {}}
    r = client.post("/", json=data)
    assert r.status_code == 200
    assert "error" in r.json()
    assert r.json()["error"]["code"] == -32601
