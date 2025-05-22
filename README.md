# MCP Vision Adapter

A minimal MCP adapter for VS Code Copilot Agent Mode (REST + STDIO).

## Quick Start


### STDIO mode
```
python -m mcp_vision_adapter.main
```

- **JSON-RPC 2.0:** Tüm STDIO yanıtları artık `{ "jsonrpc": "2.0", "id": <istek_id>, ... }` formatında döner. Hatalar da aynı şekilde JSON-RPC error objesiyle döner.
- On Windows, if prompted for manual input, type your answer and press Enter. If `/dev/tty` is unavailable, the adapter will use a Windows-compatible fallback (character input or stdin).
- Input/output is newline-delimited JSON (one JSON object per line, per MCP spec).


### HTTP/SSE mode
```
uvicorn mcp_vision_adapter.main:app --port 3000
```

- Endpoints: `/` (root JSON-RPC), `/initialize`, `/manifest`, `/execute` (legacy), `/tools/list`, `/tools/call`, `/sse`, `/ui`
- `/` (POST): Universal JSON-RPC endpoint. Accepts `{ "jsonrpc": "2.0", "id": 1, "method": "tools/list", ... }` etc. Used by VS Code MCP Agent Mode.
- `/ui`: Tiny browser test UI for manual tool calls. You can enter both `image_path` and `manual_result` (optional override).
- `/ui` is a minimal HTML page for quick manual testing.
- If neither `manual_result` nor `MANUAL_RESULT` env is set and the adapter is not running in a TTY (e.g. Uvicorn), it returns a placeholder string instead of blocking for input.
- See `.vscode/mcp.json` for VS Code integration.

## Testing


```
pip install fastapi uvicorn pytest
pytest -q
```

Tests:
- `test_manifest.py`: manifest and schema keys
- `test_exec_env.py`: HTTP execute with env var
- `test_stdio_exec.py`: STDIO mode, env var/manual input
- `test_sse_ping.py`: SSE endpoint emits listChanged
- `test_root_rpc.py`: root JSON-RPC endpoint (`/`) for initialize, tools/list, tools/call, error

## VS Code Integration

Sample `.vscode/mcp.json`:
```jsonc
{
  "servers": {
    "vision-http": {
      "type": "http",
      "url": "http://127.0.0.1:3000"
    },
    "vision-stdio": {
      "type": "stdio",
      "command": "python",
      "args": ["-m", "mcp_vision_adapter.main"]
    }
  }
}
```

After saving, use *Command Palette → “MCP: List Servers”* to start/connect.

## Notes

- STDIO: Each request/response is a single line of JSON. No extra whitespace.
- Windows: If `/dev/tty` is not available, the adapter will prompt using Windows console input.

### Port Clash

If Uvicorn port 3000 is busy, stop the previous process (CTRL-C) or run with `--port 3001` and update `mcp.json` accordingly.
