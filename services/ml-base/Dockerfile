FROM python:3.11-slim

WORKDIR /app
ENV PIP_PROGRESS_BAR=on

COPY pyproject.toml /app/pyproject.toml
RUN pip install --no-cache-dir --timeout 120 --retries 5 \
    --index-url https://download.pytorch.org/whl/cpu \
    torch==2.2.2 torchvision==0.17.2 && \
    pip install --no-cache-dir --timeout 120 --retries 5 \
    transformers sentence-transformers numpy==1.26.4 pillow
