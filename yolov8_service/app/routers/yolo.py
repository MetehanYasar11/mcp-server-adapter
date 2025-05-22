from fastapi import APIRouter, UploadFile, File, Form, Query, HTTPException, Request
from fastapi.responses import JSONResponse
from app.schemas.yolo import DetectionResponse
from app.services.yolov8 import run_yolo
from typing import Optional

router = APIRouter()

@router.post("/detect", response_model=DetectionResponse)
def detect(
    file: Optional[UploadFile] = File(None),
    image_url: Optional[str] = None,
    video_url: Optional[str] = None,
    weights: str = Query("/weights/yolov8n.pt"),
    start: Optional[str] = Query(None),
    end: Optional[str] = Query(None),
    frame: Optional[int] = Query(None)
):
    try:
        results = run_yolo(
            task="detect",
            file=file,
            image_url=image_url,
            video_url=video_url,
            weights=weights,
            start=start,
            end=end,
            frame=frame
        )
        return {"results": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/segment", response_model=DetectionResponse)
def segment(
    file: Optional[UploadFile] = File(None),
    image_url: Optional[str] = None,
    video_url: Optional[str] = None,
    weights: str = Query("/weights/yolov8n.pt"),
    start: Optional[str] = Query(None),
    end: Optional[str] = Query(None),
    frame: Optional[int] = Query(None)
):
    try:
        results = run_yolo(
            task="segment",
            file=file,
            image_url=image_url,
            video_url=video_url,
            weights=weights,
            start=start,
            end=end,
            frame=frame
        )
        return {"results": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/pose", response_model=DetectionResponse)
def pose(
    file: Optional[UploadFile] = File(None),
    image_url: Optional[str] = None,
    video_url: Optional[str] = None,
    weights: str = Query("/weights/yolov8n.pt"),
    start: Optional[str] = Query(None),
    end: Optional[str] = Query(None),
    frame: Optional[int] = Query(None)
):
    try:
        results = run_yolo(
            task="pose",
            file=file,
            image_url=image_url,
            video_url=video_url,
            weights=weights,
            start=start,
            end=end,
            frame=frame
        )
        return {"results": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
