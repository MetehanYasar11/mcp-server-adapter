
















import os
import sys
import json
import logging
from typing import Any, Dict



from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.responses import StreamingResponse


# --- Logging setup ---
LOG_FILE = os.environ.get("MCP_VISION_LOG", "mcp_vision_adapter.log")
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s %(levelname)s %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE, encoding="utf-8"),
        logging.StreamHandler(sys.stderr)
    ]
)

app = FastAPI()

MANIFEST = {
    "tools": [
        {
            "name": "detect_objects",
            "description": "Ask the user to describe what objects are in the given image/video.",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "image_path": {"type": "string"},
                    "manual_result": {"type": "string", "description": "Optional manual result override."}
                },
                "required": ["image_path"]
            }
        }
    ]
}

PROTOCOL_VERSION = "2024-03-26"

# --- STDIO/REST shared logic ---
def get_manifest() -> Dict[str, Any]:
    return {"tools": MANIFEST["tools"]}

def get_initialize_response() -> Dict[str, Any]:
    return {
        "result": {
            "protocolVersion": PROTOCOL_VERSION,
            "capabilities": {
                "tools": {
                    "listChanged": True
                }
            }
        }
    }

def read_manual_line(prompt: str) -> str:
    import sys, os
    sys.stderr.write(prompt)
    sys.stderr.flush()
    try:
        if os.name == "nt":
            import msvcrt
            chars = []
            while True:
                ch = msvcrt.getwch()
                if ch in ('\r', '\n'):
                    break
                chars.append(ch)
            return ''.join(chars)
        else:
            return sys.__stdin__.readline().rstrip("\n")
    except Exception:
        return input()

def detect_objects_impl(image_path: str, root: str = None, manual_result: str = None) -> str:
    logging.info(f"[detect_objects_impl] Called with image_path={image_path}, root={root}, manual_result={manual_result}")
    # MANUAL_RESULT ve manual_result sadece DEBUG/TEST için, prod'da devre dışı
    # if manual_result:
    #     return manual_result
    # env_result = os.environ.get("MANUAL_RESULT")
    # if env_result:
    #     return env_result
    # If root is set and image_path is relative, resolve it

    if root and not os.path.isabs(image_path):
        image_path = os.path.abspath(os.path.join(root, image_path))
    logging.info(f"[detect_objects_impl] Resolved image_path: {image_path}")
    if not os.path.exists(image_path):
        logging.error(f"[detect_objects_impl] File not found: {image_path}")
        return f"[error: file not found: {image_path}]"

    # --- YOLOv8 service integration ---
    import requests
    YOLO_SERVICE = os.getenv("YOLO_SERVICE_URL", "http://localhost:8080")
    logging.info(f"[detect_objects_impl] Sending to YOLO_SERVICE: {YOLO_SERVICE}/detect")
    try:
        with open(image_path, "rb") as f:
            files = {"file": (os.path.basename(image_path), f, "application/octet-stream")}
            resp = requests.post(f"{YOLO_SERVICE}/detect", files=files, timeout=60)
        resp.raise_for_status()
        data = resp.json()
        logging.info(f"[detect_objects_impl] YOLO response: {data}")
        # Return summary text: class list
        classes = [r.get("class_", r.get("class", "?")) for r in data.get("results", [])]
        if not classes:
            logging.info("[detect_objects_impl] No objects detected.")
            return "No objects detected."
        return ", ".join(sorted(set(classes)))
    except Exception as e:
        logging.error(f"[detect_objects_impl] Exception: {e}", exc_info=True)
        # Fallback: manual/placeholder
        pass

    # No more manual input or placeholder, return real error
    return "[error: object detection failed]"


def execute_tool(tool_name: str, params: Dict[str, Any], root: str = None) -> Any:
    logging.info(f"[execute_tool] tool_name={tool_name}, params={params}, root={root}")
    if tool_name == "detect_objects":
        manual_result = params.get("manual_result")
        return detect_objects_impl(params["image_path"], root, manual_result)
    logging.error(f"[execute_tool] Unknown tool: {tool_name}")
    raise Exception(f"Unknown tool: {tool_name}")

# --- JSON-RPC universal dispatcher for POST / ---
def handle_call(payload, root=None):
    logging.info(f"[handle_call] payload={payload}, root={root}")
    tool = payload["tool"]
    params = payload["input"]
    result = execute_tool(tool, params, root)
    logging.info(f"[handle_call] result={result}")
    return {"result": result}



@app.post("/")
async def root_rpc(request: Request):
    try:
        body = await request.json()
        method = body.get("method")
        params = body.get("params", {})
        jsonrpc_id = body.get("id")
        if method == "initialize":
            result = get_initialize_response()["result"]
            return {"jsonrpc": "2.0", "id": jsonrpc_id, "result": result}
        elif method == "tools/list":
            result = get_manifest()
            return {"jsonrpc": "2.0", "id": jsonrpc_id, "result": result}
        elif method == "tools/call":
            # params: {tool, input}
            try:
                call_result = handle_call(params)
                return {"jsonrpc": "2.0", "id": jsonrpc_id, **call_result}
            except Exception as e:
                return {"jsonrpc": "2.0", "id": jsonrpc_id, "error": {"code": -32000, "message": str(e)}}
        else:
            return {"jsonrpc": "2.0", "id": jsonrpc_id, "error": {"code": -32601, "message": f"Unknown method: {method}"}}
    except Exception as e:
        return {"jsonrpc": "2.0", "error": {"code": -32603, "message": str(e)}}

@app.post("/initialize")
async def http_initialize():
    return get_initialize_response()

@app.get("/manifest")
async def http_manifest():
    return get_manifest()

@app.post("/execute")
async def http_execute(request: Request):
    body = await request.json()
    tool = body.get("tool") or body.get("params", {}).get("tool")
    params = body.get("input") or body.get("params", {}).get("input")
    try:
        call_result = handle_call({"tool": tool, "input": params})
        return call_result
    except Exception as e:
        return JSONResponse(status_code=400, content={"error": str(e)})

@app.api_route("/tools/list", methods=["POST"])
@app.api_route("/tools/list/", methods=["POST"])
async def http_tools_list():
    return get_manifest()

@app.post("/tools/call")
async def http_tools_call(request: Request):
    body = await request.json()
    tool = body["params"]["tool"]
    params = body["params"]["input"]
    try:
        call_result = handle_call({"tool": tool, "input": params})
        return call_result
    except Exception as e:
        return JSONResponse(status_code=400, content={"error": str(e)})

@app.get("/sse")
async def http_sse():
    async def event_stream():
        yield "event: listChanged\ndata: {}\n\n"
    return StreamingResponse(event_stream(), media_type="text/event-stream")

@app.get("/ui")
async def http_ui():
    html = '''
    <!DOCTYPE html>
    <html lang="en">
    <head><meta charset="utf-8"><title>MCP Vision Adapter UI</title></head>
    <body>
    <h2>detect_objects Tool Test UI</h2>
    <input id="file" placeholder="image_path" value="test.jpg">
    <input id="manual" placeholder="manual_result (optional)">
    <button onclick="callTool()">Run detect_objects</button>
    <pre id="out"></pre>
    <script>
    async function callTool() {
        const path = document.getElementById('file').value;
        const manual = document.getElementById('manual').value;
        const input = {image_path: path};
        if (manual) input.manual_result = manual;
        const resp = await fetch('/execute', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({tool: 'detect_objects', input})
        });
        document.getElementById('out').textContent = await resp.text();
    }
    </script>
    </body></html>
    '''
    return JSONResponse(content=html, media_type="text/html")


def stdio_main():
    session_id = None
    root = None
    logging.info("[stdio_main] MCP Vision Adapter stdio_main started.")
    while True:
        line = sys.stdin.readline()
        if not line:
            break
        try:
            logging.info(f"[stdio_main] Received line: {line.strip()}")
            req = json.loads(line)
            method = req.get("method")
            req_id = req.get("id")
            if method == "initialize":
                session_id = None
                roots = req.get("params", {}).get("roots")
                if roots and isinstance(roots, list) and roots:
                    root = roots[0]
                payload = get_initialize_response()["result"]
                resp = {"jsonrpc": "2.0", "id": req_id, "result": payload}
            elif method == "tools/list":
                payload = get_manifest()
                resp = {"jsonrpc": "2.0", "id": req_id, "result": payload}
            elif method == "manifest":
                payload = get_manifest()
                resp = {"jsonrpc": "2.0", "id": req_id, "result": payload}
            elif method in ("execute", "tools/call"):
                tool = req["params"]["tool"]
                params = req["params"]["input"]
                try:
                    logging.info(f"[stdio_main] Calling tool: {tool} with params: {params} and root: {root}")
                    result = execute_tool(tool, params, root)
                    resp = {"jsonrpc": "2.0", "id": req_id, "result": result}
                    logging.info(f"[stdio_main] Tool result: {result}")
                except Exception as e:
                    logging.error(f"[stdio_main] Tool execution error: {e}", exc_info=True)
                    resp = {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32000, "message": str(e)}}
            else:
                logging.error(f"[stdio_main] Unknown method: {method}")
                resp = {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32601, "message": "Unknown method"}}
        except Exception as e:
            logging.error(f"[stdio_main] Exception: {e}", exc_info=True)
            resp = {"jsonrpc": "2.0", "id": None, "error": {"code": -32603, "message": str(e)}}
        print(json.dumps(resp), flush=True)



# Only run stdio_main if this file is executed as a script, not on import (e.g. by pytest)
if __name__ == "__main__":
    stdio_main()
