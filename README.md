


# MCP Vision Adapter

<p align="center">
  <img src="https://img.shields.io/badge/MCP%20Protocol-2024--03--26-blue" alt="MCP Protocol Version"/>
  <img src="https://img.shields.io/badge/Universal%20CLI%20Adapter-hub%20for%20LLMs-orange" alt="Universal CLI Adapter"/>
  <img src="https://img.shields.io/badge/REST%20%2B%20STDIO-API-green" alt="REST + STDIO API"/>
  <img src="https://img.shields.io/badge/License-MIT-yellow" alt="MIT License"/>
</p>

<h3 align="center">MCP Service for Oldies but Goldies</h3>

**MCP Vision Adapter** is a universal, open-source MCP (Model Context Protocol) adapter for all CLI projects. It is designed to modernize and connect your classic automations, scripts, and detection tools to LLM/agent ecosystems—no matter how old or gold they are!

> "Turn your legacy CLI automations into LLM/agent tools. If your software has a CLI, you can make it an agent tool—no rewrite required."

This repo demonstrates a reference implementation using Ultralytics YOLOv8 (with CLI support) as an example service. You can register your own custom YOLOv8 models or any CLI-based tool as an agent tool and get detection results, comments, or outputs directly in your LLM workflows.

**MCP Protocol Version:** `2024-03-26`  
**Standard:** [Model Context Protocol (MCP)](https://github.com/microsoft/model-context-protocol)

---

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

You can run the MCP Adapter and YOLOv8 service in three ways:

### 1. Virtual Environment (Recommended for Dev)

**Step 1:** Create and activate a virtual environment (venv or conda)
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
# or with conda
conda create -n mcp python=3.10
conda activate mcp
```
**Step 2:** Install dependencies
```powershell
pip install -r yolov8_service/requirements.txt
pip install -e .
```
**Step 3:** Start YOLOv8 service
```powershell
cd yolov8_service
uvicorn app.main:app --host 0.0.0.0 --port 8080
# (Optional) Streamlit UI: streamlit run app/streamlit_app.py --server.port 8501 --server.address 0.0.0.0
```
**Step 4:** Start MCP Adapter
```powershell
cd ..
uvicorn mcp_vision_adapter.main:app --port 3000
```

### 2. Docker Based (YOLOv8 + Adapter)

**Step 1:** Build and run both services with Docker Compose
```powershell
docker-compose up --build
```
- YOLOv8 service: [http://localhost:8080](http://localhost:8080)
- Adapter: [http://localhost:3000](http://localhost:3000)
- Streamlit UI: [http://localhost:8501](http://localhost:8501)

### 3. All-in-One: Just Docker Compose!

The provided `docker-compose.yml` launches both YOLOv8 and MCP Adapter, with all ports mapped and model management UI enabled. Just run:
```powershell
docker-compose up --build
```

---

#### Test YOLOv8 Service
```powershell
curl -F file=@test.jpg http://localhost:8080/detect
```

#### Test Adapter (proxies to YOLO)
```powershell
Invoke-RestMethod -Uri "http://localhost:3000/execute" -Method Post -ContentType "application/json" -Body '{"tool":"detect_objects","input":{"image_path":"test.jpg"}}'
```

---

### STDIO Mode (Currently not supported for VS Code Copilot tool execution)
```
python -m mcp_vision_adapter.main
```
> ⚠️ **Note:** VS Code Copilot tool execution via STDIO is currently not supported. Please use the HTTP API for full integration. This will be fixed in an upcoming update.
## 🤝 Contributing

We welcome contributions! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines. The goal is to make this repo a hub for connecting classic automations and tools to modern LLM/agent environments. Contact [Metehan Yaşar on LinkedIn](https://www.linkedin.com/in/metehan-y-16475a164/) for questions or collaboration.

---

## 🛣️ Roadmap & Future Updates

- **Hotfix:** VS Code Copilot tool execution via STDIO is currently not supported. Use HTTP API for now. This will be fixed soon.
- **Upcoming:**
  - **n8n Example Automation:** A ready-to-use n8n template and a short usage video will be added.
  - **Complete Ultralytics Service:** Full support for pose and segmentation tasks, including time-sliced video analysis, coming within 2 weeks. This repo is a reference CLI-to-MCP service.
  - **v2: Automation Agent:** An OpenAI model will be integrated, enabling agent-based automation as a service. This will allow connecting automations as services—stay tuned!

---

## 🛠️ Custom Service Integration Tutorial

To connect your own service or tool as an adapter:

1. Implement a REST or STDIO interface that matches the MCP protocol (see `mcp_vision_adapter/main.py`).
2. Register your service in `.vscode/mcp.json` or your orchestrator.
3. Use the HTTP API for best compatibility:
   ```powershell
   Invoke-RestMethod -Uri "http://localhost:3000/execute" -Method Post -ContentType "application/json" -Body '{"tool":"your_tool","input":{...}}'
   ```
4. For advanced use, see the test suite and example adapters.

---

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
