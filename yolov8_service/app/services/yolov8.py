import os
import uuid
import tempfile
import shutil
import requests
from ultralytics import YOLO
import cv2
from typing import Optional

# Helper: Download file from URL
def download_to_tmp(url: str) -> str:
    r = requests.get(url, stream=True)
    ext = os.path.splitext(url)[-1] or ".jpg"
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=ext)
    for chunk in r.iter_content(1024):
        tmp.write(chunk)
    tmp.close()
    return tmp.name

def run_yolo(task: str, file=None, image_url=None, video_url=None, weights="/weights/yolov8n.pt", start=None, end=None, frame=None):
    # Prepare input
    input_path = None
    cleanup = []
    if file:
        tmp = tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file.filename)[-1])
        tmp.write(file.file.read())
        tmp.close()
        input_path = tmp.name
        cleanup.append(input_path)
    elif image_url:
        input_path = download_to_tmp(image_url)
        cleanup.append(input_path)
    elif video_url:
        input_path = download_to_tmp(video_url)
        cleanup.append(input_path)
    else:
        raise ValueError("No input file or URL provided.")

    # Video slicing
    if (start or end) and input_path and input_path.lower().endswith(('.mp4', '.avi', '.mov', '.mkv')):
        out_path = f"/tmp/{uuid.uuid4()}.mp4"
        start_opt = f"-ss {start}" if start else ""
        end_opt = f"-to {end}" if end else ""
        cmd = f"ffmpeg {start_opt} -i {input_path} {end_opt} -c copy {out_path} -y"
        os.system(cmd)
        input_path = out_path
        cleanup.append(out_path)
    elif frame is not None and input_path and input_path.lower().endswith(('.mp4', '.avi', '.mov', '.mkv')):
        # Extract frame as image
        cap = cv2.VideoCapture(input_path)
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame)
        ret, img = cap.read()
        if not ret:
            raise ValueError("Could not extract frame.")
        frame_path = f"/tmp/{uuid.uuid4()}.jpg"
        cv2.imwrite(frame_path, img)
        input_path = frame_path
        cleanup.append(frame_path)
        cap.release()

    # Load model
    model = YOLO(weights)
    results = model(input_path, task=task)

    # Save annotated output (debug)
    out_dir = "/outputs"
    os.makedirs(out_dir, exist_ok=True)
    out_file = os.path.join(out_dir, f"{uuid.uuid4()}{os.path.splitext(input_path)[-1]}")
    results[0].save(filename=out_file)

    # Parse results
    parsed = []
    for r in results:
        start_index = len(parsed)
        for box in r.boxes:
            parsed.append({
                "class_": r.names[int(box.cls[0])],
                "conf": float(box.conf[0]),
                "bbox": box.xyxy[0].tolist()
            })
        if hasattr(r, "masks") and r.masks is not None:
            for i, mask in enumerate(r.masks.data):
                if start_index + i < len(parsed):
                    parsed[start_index + i]["mask"] = mask.cpu().numpy().tolist()
        if hasattr(r, "keypoints") and r.keypoints is not None:
            for i, kps in enumerate(r.keypoints.data):
                if start_index + i < len(parsed):
                    parsed[start_index + i]["keypoints"] = kps.cpu().numpy().tolist()

    # Cleanup
    for f in cleanup:
        try:
            os.remove(f)
        except Exception:
            pass
    return parsed
