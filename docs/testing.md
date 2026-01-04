# Testing Options

## Option 1: Local Python (uv)
Use this if you do not have Docker installed.

1. Install dependencies:
   - `uv sync`
   - This uses CPU-only PyTorch wheels to avoid CUDA downloads.
2. Run a service:
   - `uv run uvicorn services.gateway.main:app --reload --port 8000`
3. Verify:
   - `http://localhost:8000/healthz`

Repeat with other services by changing the module path and port:
- `services.embedding.main:app` on 8001
- `services.classifier.main:app` on 8002
- `services.eval.main:app` on 8003

You can then run a quick smoke test:
- `scripts/smoke-test.sh`
Set `RUN_ML_SMOKE=1` to exercise all ML endpoints via the gateway (may download models).
To run a subset, use one or more of:
- `RUN_PREDICT_SMOKE=1`
- `RUN_RAG_SMOKE=1`
- `RUN_COMPARE_SMOKE=1`
- `RUN_LLM_SMOKE=1`
- `RUN_CAPTION_SMOKE=1`
- `RUN_VISION_SMOKE=1`
If the first request times out, increase `REQUEST_TIMEOUT_SECONDS` for the gateway.
Docker Compose builds a shared `ml-base` image once to avoid repeated downloads.
Build order for Docker Compose:
```
docker compose build ml-base
docker compose build embedding llm vision
docker compose build
```
The ML smoke test now includes `/rag-lite`, `/compare`, and `/caption`.
Standalone workflow scripts:
- `scripts/rag_lite.py`
- `scripts/compare_texts.py`
- `scripts/caption_image.py`
Use `TIMEOUT_SECONDS=300` for `scripts/rag_lite.py` if the first call is slow.

## Option 2: Docker Compose
Use this if you have Docker installed.

1. Start all services:
   - `docker compose up --build`
2. Verify:
   - `http://localhost:8000/healthz`
   - `http://localhost:8001/healthz`
   - `http://localhost:8002/healthz`
   - `http://localhost:8003/healthz`

You can also use:
- `scripts/smoke-test.sh`
Set `RUN_ML_SMOKE=1` to exercise ML endpoints via the gateway (may download models).

Notes
- On Ubuntu, `sudo apt install docker.io` is the simplest Docker install.
- If you use Podman, `sudo apt install podman-docker` is an option, but behavior can differ.

## Helm Validation
These checks verify that both local and EKS values render cleanly without a cluster.

- `scripts/validate-helm.sh`

## Storage (local-path)
```
kubectl get storageclass
kubectl apply -f k8s/pvc-smoke.yaml
kubectl get pvc -n demo
kubectl delete -f k8s/pvc-smoke.yaml
```

## Resource Isolation Verification
If resource isolation is enabled in values, verify the namespace controls:

```
kubectl -n ai-mesh get resourcequota,limitrange,networkpolicy
```
