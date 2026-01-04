# Testing Options

## Option 1: Local Python (uv)
Use this if you do not have Docker installed.

1. Install dependencies:
   - `uv sync`
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

Notes
- On Ubuntu, `sudo apt install docker.io` is the simplest Docker install.
- If you use Podman, `sudo apt install podman-docker` is an option, but behavior can differ.

## Helm Validation
These checks verify that both local and EKS values render cleanly without a cluster.

- `scripts/validate-helm.sh`

## Resource Isolation Verification
If resource isolation is enabled in values, verify the namespace controls:

```
kubectl -n ai-mesh get resourcequota,limitrange,networkpolicy
```
