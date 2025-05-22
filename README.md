# MCP Vision Adapter

A minimal MCP adapter for VS Code Copilot Agent Mode (REST + STDIO).


## Quick Start

### Docker Compose (YOLOv8 + Adapter)
```powershell
docker-compose up --build
```

- YOLOv8 service: [http://localhost:8080](http://localhost:8080)
- Adapter: [http://localhost:3000](http://localhost:3000)

#### Test YOLOv8 service
```powershell
curl -F file=@test.jpg http://localhost:8080/detect
```

#### Test Adapter (proxies to YOLO)
```powershell
curl -X POST http://localhost:3000/execute -H "Content-Type: application/json" -d '{"tool":"detect_objects","input":{"image_path":"test.jpg"}}'
```

### STDIO mode
```
python -m mcp_vision_adapter.main
```

### HTTP/SSE mode
```
uvicorn mcp_vision_adapter.main:app --port 3000
```

---

## YOLOv8 Microservice

See [`yolov8_service/README.md`](yolov8_service/README.md) for endpoints, Docker usage, and time slicing params.

**Mount your models:**
```powershell
docker run -v ${PWD}/models:/weights ...
```
Default weights: `/weights/yolov8n.pt`

---

## VS Code MCP Integration

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

---

## Testing

```powershell
pip install fastapi uvicorn pytest
pytest -q
```

Tests:
- `test_service_detect.py`: YOLOv8 service (direct)
- `test_adapter_proxy.py`: Adapter → YOLOv8 service
- All existing adapter tests remain green

---

## Notes

- For video, use `start`/`end` (e.g. `?start=2s&end=5s`) or `frame` for slicing.
- If neither `manual_result` nor `MANUAL_RESULT` env is set and the adapter is not running in a TTY, it returns a placeholder string.

---

### Port Clash

If Uvicorn port 3000 is busy, stop the previous process (CTRL-C) or run with `--port 3001` and update `mcp.json` accordingly.
