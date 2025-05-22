from pydantic import BaseModel
from typing import List, Optional, Any

class Detection(BaseModel):
    class_: str
    conf: float
    bbox: Optional[list]
    mask: Optional[Any] = None
    keypoints: Optional[Any] = None

class DetectionResponse(BaseModel):
    results: List[Detection]
