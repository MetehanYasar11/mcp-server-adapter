

# MCP Vision Adapter

<p align="center">
  <img src="https://img.shields.io/badge/YOLOv8-Powered-blue" alt="YOLOv8 Powered"/>
  <img src="https://img.shields.io/badge/REST%20API-Ready-green" alt="REST API Ready"/>
  <img src="https://img.shields.io/badge/VS%20Code%20Copilot-Agent%20Mode-orange" alt="VS Code Copilot Agent Mode"/>
  <img src="https://img.shields.io/badge/License-MIT-yellow" alt="MIT License"/>
</p>

**MCP Vision Adapter** is a modern, open-source visual perception platform powered by Ultralytics YOLOv8, supporting REST/STDIO APIs, full VS Code Copilot Agent Mode integration, and a built-in web UI for model management and live results.

---

## 🚀 Key Features

- **Ultralytics YOLOv8 Integration:** Fast and accurate object detection, segmentation, and pose estimation.
- **REST & STDIO API:** Easy integration via both HTTP/REST and stdio.
- **Web UI for Model Management:** Built-in Streamlit interface to load, swap, manage models, and view live results.
- **VS Code Copilot Agent Mode:** Native integration with VS Code, automated tests, and code assistant support.
- **Easy Docker & Compose Setup:** Spin up all services with a single command.
- **Fully Open Source & MIT Licensed:** Free for commercial and personal use, easy to extend.
- **Comprehensive Testing:** End-to-end tests with pytest, sample images, and automation.
- **Video & Image Support:** Analyze videos by time range or frame, as well as images.
- **Model Hot-Swap:** Swap model files on a running service without downtime.
- **Extensible API:** Easily add new endpoints and capabilities.

---

## 🚦 Quick Start

### Docker Compose (YOLOv8 + Adapter)
```powershell
docker-compose up --build
```

- YOLOv8 service: [http://localhost:8080](http://localhost:8080)
- Adapter: [http://localhost:3000](http://localhost:3000)

#### Test YOLOv8 Service
```powershell
curl -F file=@test.jpg http://localhost:8080/detect
```

#### Test Adapter (proxies to YOLO)
```powershell
Invoke-RestMethod -Uri "http://localhost:3000/execute" -Method Post -ContentType "application/json" -Body '{"tool":"detect_objects","input":{"image_path":"test.jpg"}}'
```

### STDIO Mode
```
python -m mcp_vision_adapter.main
```

### HTTP/SSE Mode
```
uvicorn mcp_vision_adapter.main:app --port 3000
```

---

## 🦾 YOLOv8 Microservice

See [`yolov8_service/README.md`](yolov8_service/README.md) for advanced usage and details.

**Mount your model folder:**
```powershell
docker run -v ${PWD}/models:/weights ...
```
Default weights file: `/weights/yolov8n.pt`

---

## 🧩 VS Code MCP Integration

Example `.vscode/mcp.json`:
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

## 🧪 Testing

```powershell
pip install fastapi uvicorn pytest
pytest -q
```

Tests:
- `test_service_detect.py`: YOLOv8 service (direct)
- `test_adapter_proxy.py`: Adapter → YOLOv8 service
- `test_stdio_exec.py`, `test_exec_env.py`: STDIO and env tests
- All tests are automated and end-to-end

---

## 📝 Notes

- For video, use `start`/`end` (e.g. `?start=2s&end=5s`) or `frame` params.
- If neither `manual_result` nor `MANUAL_RESULT` is set and the adapter is not running in a TTY, a placeholder is returned.

---

### ⚠️ Port Clash

If Uvicorn port 3000 is busy, stop the previous process (CTRL-C) or run with `--port 3001` and update `mcp.json` accordingly.

---

## 🌍 Open Source & License

This project is open source under the MIT license. Contributions are welcome!

---

## Security & Privacy

- No secret keys, passwords, or access tokens are included in the codebase.
- Example values like `GITHUB_PERSONAL_ACCESS_TOKEN` are for documentation and test purposes only. Always use your own keys securely.

---

## 🇹🇷 Türkçe Dokümantasyon

Bu projenin Türkçe dokümantasyonu da mevcuttur. [README.tr.md](README.tr.md) dosyasına göz atabilirsiniz.
