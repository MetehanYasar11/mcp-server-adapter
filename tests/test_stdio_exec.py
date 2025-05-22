import os
import sys
import json
import subprocess
import time
import pytest

def test_stdio_detect_objects_env(monkeypatch):
    # Set env var for subprocess
    env = os.environ.copy()
    env["MANUAL_RESULT"] = "cli"
    proc = subprocess.Popen(
        [sys.executable, "-m", "mcp_vision_adapter.main"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        env=env,
        cwd=os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    )
    # Compose newline-delimited JSON requests
    reqs = [
        {"id": 1, "jsonrpc": "2.0", "method": "initialize"},
        {"id": 2, "jsonrpc": "2.0", "method": "manifest"},
        {"id": 3, "jsonrpc": "2.0", "method": "execute", "params": {"tool": "detect_objects", "input": {"image_path": "dummy"}}}
    ]
    input_data = "\n".join(json.dumps(r) for r in reqs) + "\n"
    out, err = proc.communicate(input=input_data, timeout=5)
    lines = [l for l in out.splitlines() if l.strip()]
    def assert_jsonrpc_ok(line):
        obj = json.loads(line)
        assert obj["jsonrpc"] == "2.0" and "result" in obj
        if "result" in obj and isinstance(obj["result"], dict) and "tools" in obj["result"]:
            assert any(t["name"] == "detect_objects" for t in obj["result"]["tools"])
    # Check initialize and execute responses
    assert_jsonrpc_ok(lines[0])
    assert_jsonrpc_ok(lines[2])
    assert any("cli" in l for l in lines), f"No 'cli' in output: {lines}"
