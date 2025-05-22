import threading
import time
import random
import socket
import requests
import sys
import os
import pytest

from fastapi.testclient import TestClient
import mcp_vision_adapter.main as main_mod



def get_free_port():
    s = socket.socket()
    s.bind(('', 0))
    port = s.getsockname()[1]
    s.close()
    return port

def run_server_in_thread(port):
    import uvicorn
    def run():
        uvicorn.run("mcp_vision_adapter.main:app", host="127.0.0.1", port=port, log_level="error")
    t = threading.Thread(target=run, daemon=True)
    t.start()
    time.sleep(1.5)  # Give server time to start
    return t

def test_sse_ping():
    port = get_free_port()
    run_server_in_thread(port)
    url = f"http://127.0.0.1:{port}/sse"
    resp = requests.get(url, stream=True, timeout=5)
    found = False
    for line in resp.iter_lines():
        if b"listChanged" in line:
            found = True
            break
    assert found, "No listChanged event received"
