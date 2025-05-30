FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN apt-get update && apt-get install -y ffmpeg && \
    pip install -r requirements.txt
COPY app /app/app
EXPOSE 8080
EXPOSE 8501
CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port 8080 & streamlit run app/streamlit_app.py --server.port 8501 --server.address 0.0.0.0"]
