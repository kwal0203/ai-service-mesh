FROM python:3.11-slim

WORKDIR /app
ENV PIP_PROGRESS_BAR=on

COPY pyproject.toml /app/pyproject.toml
RUN pip install --no-cache-dir --timeout 120 --retries 5 \
    fastapi uvicorn pydantic httpx

COPY services /app/services

EXPOSE 8000
CMD ["uvicorn", "services.gateway.main:app", "--host", "0.0.0.0", "--port", "8000"]
