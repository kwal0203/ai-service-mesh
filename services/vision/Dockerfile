FROM ai-mesh-ml-base:dev

WORKDIR /app
ENV PIP_PROGRESS_BAR=on

RUN pip install --no-cache-dir --timeout 120 --retries 5 \
    fastapi uvicorn pydantic

COPY services /app/services

EXPOSE 8005
CMD ["uvicorn", "services.vision.main:app", "--host", "0.0.0.0", "--port", "8005"]
