FROM python:3.11-slim

WORKDIR /app
ENV PIP_PROGRESS_BAR=on

COPY pyproject.toml /app/pyproject.toml
RUN pip install --no-cache-dir --timeout 120 --retries 5 \
    fastapi uvicorn pydantic numpy

COPY services /app/services

EXPOSE 8002
CMD ["uvicorn", "services.classifier.main:app", "--host", "0.0.0.0", "--port", "8002"]
