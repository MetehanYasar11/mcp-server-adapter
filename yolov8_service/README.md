
# YOLOv8 Microservice

A FastAPI-based microservice for running Ultralytics YOLOv8 detection, segmentation, and pose estimation.

---

## 🖥️ Streamlit Model Manager UI

This service includes a built-in Streamlit web interface for managing YOLOv8 model weights. You can:
- View available YOLOv8 `.pt` models in the `/models` directory
- Upload new YOLOv8 weights via the browser
- See and set the current default model

**How to use:**
1. Start the YOLOv8 microservice (see Docker instructions below)
2. Open your browser and go to: [http://localhost:8501](http://localhost:8501)
3. You will see a model manager interface:

![YOLOv8 Model Manager UI](../yolov8_service_ui.png)

See [USAGE.md](USAGE.md) for more details.

---

## Endpoints
- `POST /detect` — Object detection
- `POST /segment` — Instance segmentation
- `POST /pose` — Pose estimation

### Request
- Accepts `multipart/form-data` with `file` (image/video) **or** JSON with `image_url`/`video_url`.
- Query params:
  - `weights` (default: `/weights/yolov8n.pt`)
  - `start`, `end` (e.g. `5s`, `8s`) or `frame` (for video)

### Response
- JSON: `{ "results": [ { "class": "person", "conf": 0.97, "bbox": [...] } ] }`
- Annotated output saved to `/outputs/<uuid>.*` (debug only)

## Docker Usage
```sh
# Build
cd yolov8_service
 docker build -t yolov8_service .

# Run (mount models)
docker run -it -p 8080:8080 -v $(pwd)/models:/weights yolov8_service
```

## Example: Detect via curl
```sh
curl -F file=@../test.jpg http://localhost:8080/detect
```

## Postman
Import the included `docs/postman_collection.json` for ready-to-use requests.

## Time Slicing
- For video, use `start`/`end` (e.g. `?start=2s&end=5s`) to process a segment.
- Or use `frame` to process a specific frame.

## Requirements
- Mount your YOLO weights: `-v /path/to/models:/weights`
- Default weights: `/weights/yolov8n.pt`
