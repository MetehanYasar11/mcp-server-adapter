import os
import sys
import json
import subprocess
import pytest

def test_exec_manual_param():
    from fastapi.testclient import TestClient
    import mcp_vision_adapter.main as main_mod
    client = TestClient(main_mod.app)
    resp = client.post("/execute", json={
        "tool": "detect_objects",
        "input": {"image_path": "test.jpg", "manual_result": "from_param"}
    })
    assert resp.status_code == 200
    assert resp.json()["result"] == "from_param"

def test_stdio_stdin_branch():
    # No MANUAL_RESULT, no tty, should return placeholder
    env = os.environ.copy()
    proc = subprocess.Popen(
        [sys.executable, "-m", "mcp_vision_adapter.main"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        env=env,
        cwd=os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    )
    reqs = [
        {"id": 1, "jsonrpc": "2.0", "method": "initialize"},
        {"id": 2, "jsonrpc": "2.0", "method": "tools/call", "params": {"tool": "detect_objects", "input": {"image_path": "dummy"}}}
    ]
    input_data = "\n".join(json.dumps(r) for r in reqs) + "\n"
    out, err = proc.communicate(input=input_data, timeout=5)
    lines = [l for l in out.splitlines() if l.strip()]
    def assert_jsonrpc_ok(line):
        obj = json.loads(line)
        assert obj["jsonrpc"] == "2.0" and ("result" in obj or "error" in obj)
        if "result" in obj and isinstance(obj["result"], dict) and "tools" in obj["result"]:
            assert any(t["name"] == "detect_objects" for t in obj["result"]["tools"])
    # Check initialize and tools/call responses
    assert_jsonrpc_ok(lines[0])
    assert_jsonrpc_ok(lines[1])
    assert any("[manual input required" in l for l in lines), f"No placeholder in output: {lines}"
