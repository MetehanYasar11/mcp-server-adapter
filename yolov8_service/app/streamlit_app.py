import streamlit as st
import os
from pathlib import Path

MODELS_DIR = Path(__file__).parent.parent.parent / "models"

st.set_page_config(page_title="YOLOv8 Model Manager", layout="centered")
st.title("YOLOv8 Model Manager")

# Show current default model
DEFAULT_MODEL = os.environ.get("DEFAULT_MODEL", "yolov8n.pt")
st.info(f"Current default model: {DEFAULT_MODEL}")

# List available models
st.subheader("Available Models")
models = [f for f in os.listdir(MODELS_DIR) if f.endswith(".pt")]
if models:
    st.write(models)
else:
    st.write("No models found in models/ directory.")

# File uploader for new weights
st.subheader("Upload New YOLOv8 Weights (.pt)")
uploaded_file = st.file_uploader("Drag and drop or select a .pt file", type=["pt"])
if uploaded_file is not None:
    save_path = MODELS_DIR / uploaded_file.name
    with open(save_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    st.success(f"Uploaded {uploaded_file.name} to models/ directory.")
    st.experimental_rerun()
