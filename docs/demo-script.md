# Demo Script (5–7 minutes)

## 0) Setup (pre-demo)
- Cluster is healthy (`kubectl get nodes`).
- Linkerd, NGINX Ingress, Prometheus, Grafana already installed.
- Helm release deployed with local values.

## 1) Baseline Deploy
- Show services are up:
```
kubectl -n ai-mesh get deploy,svc
```
- Quick health checks:
```
curl -fsS http://localhost:8000/healthz
```

## 2) Traffic Split (Canary)
- Apply canary values:
```
helm upgrade --install ai-mesh charts/ai-service-mesh \
  -f charts/ai-service-mesh/values-local.yaml \
  -f charts/ai-service-mesh/values-canary.yaml \
  --namespace ai-mesh --create-namespace
```
- Show live split in Linkerd dashboard.
- Capture screenshot: `docs/screenshots/linkerd-viz-dashboard.png`.

## 3) Autoscaling
- Apply HPA demo:
```
kubectl create namespace demo
kubectl apply -f k8s/hpa-demo.yaml
scripts/hpa-load.sh run demo
```
- Watch scale events:
```
kubectl -n demo get hpa hpa-demo --watch
```
- Stop load:
```
scripts/hpa-load.sh cleanup demo
```

## 4) Workflow Demos (Real ML)
- RAG-lite:
```
./scripts/rag_lite.py
```
- Compare:
```
./scripts/compare_texts.py
```
- Caption:
```
./scripts/caption_image.py
```
- Semantic routing:
```
./scripts/route_query.py
```

## 5) Observability Story
- Grafana: show request latency + error rate.
- Linkerd: show per-service success rates.

## 6) EKS Portability
- Show values-only diff:
  - `charts/ai-service-mesh/values-local.yaml`
  - `charts/ai-service-mesh/values-eks.yaml`

## Capture Checklist
- Linkerd traffic split screenshot:
  - `docs/screenshots/linkerd-viz-dashboard.png`
