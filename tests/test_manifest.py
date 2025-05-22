import requests
import os
import sys
import importlib.util
import pytest


# Ensure parent dir is in sys.path so mcp_vision_adapter is importable as a package
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import mcp_vision_adapter.main as main_mod

def test_manifest_lists_detect_objects():
    manifest = main_mod.get_manifest()
    tools = manifest["tools"]
    tool_names = [t["name"] for t in tools]
    assert "detect_objects" in tool_names
    # Check inputSchema key exists for detect_objects
    detect_tool = next(t for t in tools if t["name"] == "detect_objects")
    assert "inputSchema" in detect_tool

def test_tools_list_http():
    from fastapi.testclient import TestClient
    import mcp_vision_adapter.main as main_mod
    client = TestClient(main_mod.app)
    # Test both with and without trailing slash
    for url in ["/tools/list", "/tools/list/"]:
        resp = client.post(url)
        if resp.status_code == 200:
            data = resp.json()
            assert "tools" in data
            return
    pytest.fail("Neither /tools/list nor /tools/list/ returned 200")
    assert any(t["name"] == "detect_objects" for t in data["tools"])
