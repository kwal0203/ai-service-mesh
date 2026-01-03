FROM python:3.11-slim

WORKDIR /app

COPY pyproject.toml /app/pyproject.toml
RUN pip install --no-cache-dir uv && \
    uv pip install --system fastapi uvicorn pydantic

COPY services /app/services

EXPOSE 8001
CMD ["uvicorn", "services.embedding.main:app", "--host", "0.0.0.0", "--port", "8001"]
