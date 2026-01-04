# Services Overview

This demo uses 2–3 FastAPI services plus a lightweight gateway. Each service should expose `/healthz` and `/metrics` endpoints.

## Gateway
- Purpose: fan-out and route requests to downstream services
- Port: 8000
- Endpoints:
  - POST /predict: accepts a request and calls embedding + classifier
  - POST /rag-lite: question answering with local corpus
  - POST /route: semantic routing with scoped context
  - POST /compare: semantic similarity + summary (style/format controls)
  - POST /generate: proxy to the LLM service
  - POST /caption: image labels + caption
  - POST /classify-image: proxy to the vision service
  - GET /healthz
  - GET /metrics
- Config:
  - EMBEDDING_URL (default: http://embedding:8001/embedding)
  - CLASSIFIER_URL (default: http://classifier:8002/classifier)
  - EVAL_URL (default: http://eval:8003/eval)
  - LLM_URL (default: http://llm:8004/generate)
  - VISION_URL (default: http://vision:8005/classify-image)

## Embedding API
- Purpose: generate embeddings from text (CPU-only model)
- Port: 8001
- Endpoints:
  - POST /embedding: {"text": "..."} -> {"vector": [..]}
  - GET /healthz
  - GET /metrics

## Classifier API
- Purpose: run a lightweight classifier on an embedding
- Port: 8002
- Endpoints:
  - POST /classifier: {"vector": [..]} -> {"label": "...", "score": 0.0}
  - GET /healthz
  - GET /metrics

## Eval API
- Purpose: rule-based checks for output validation
- Port: 8003
- Endpoints:
  - POST /eval: {"label": "...", "score": 0.0} -> {"pass": true}
  - GET /healthz
  - GET /metrics

## LLM API
- Purpose: small text generation (CPU-only)
- Port: 8004
- Endpoints:
  - POST /generate: {"prompt": "..."} -> {"text": "..."}
  - GET /healthz
  - GET /metrics

## Vision API
- Purpose: pretrained CNN image classification
- Port: 8005
- Endpoints:
  - POST /classify-image: {"image_base64": "..."} -> {"predictions": [...]}
  - GET /healthz
  - GET /metrics

## Resource Budgets (CPU-only)
- Default requests: 100m CPU, 256Mi memory
- Default limits: 500m CPU, 512Mi memory
- HPA target: 70% CPU
