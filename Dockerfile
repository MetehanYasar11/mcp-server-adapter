# MCP Vision Adapter Dockerfile
FROM python:3.10-slim
WORKDIR /app
COPY setup.py setup.cfg pyproject.toml README.md ./
COPY mcp_vision_adapter ./mcp_vision_adapter
RUN pip install --upgrade pip && pip install uvicorn[standard] fastapi requests && pip install .
EXPOSE 3000
CMD ["uvicorn", "mcp_vision_adapter.main:app", "--host", "0.0.0.0", "--port", "3000"]
