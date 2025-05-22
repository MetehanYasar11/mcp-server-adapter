from fastapi import FastAPI
from app.routers import yolo
import os

app = FastAPI(title="YOLOv8 Microservice")

app.include_router(yolo.router)

@app.get("/")
def root():
    return {"status": "YOLOv8 service running"}
