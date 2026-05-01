FROM python:3.11-slim

WORKDIR /app

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/

# Install CPU-only PyTorch first to avoid pulling CUDA wheels (~7GB)
RUN uv pip install --system --no-cache \
    torch torchvision \
    --index-url https://download.pytorch.org/whl/cpu

COPY pyproject.toml .
RUN uv pip install --system --no-cache .

COPY src/ ./src/

EXPOSE 8000
CMD ["uvicorn", "src.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
