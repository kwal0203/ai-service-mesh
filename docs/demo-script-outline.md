# Demo Script Outline

## 1) Baseline Deploy
- Install Linkerd, NGINX Ingress, Prometheus, Grafana.
- Deploy Helm chart with local values.
- Verify all services are healthy.

## 2) Traffic Split
- Introduce a canary version of one service (e.g., classifier).
- Apply Linkerd TrafficSplit to send 90/10 traffic.
- Show live split in Linkerd dashboard.

## 3) Autoscaling
- Apply load to /predict endpoint.
- Observe HPA scaling on the target service.
- Show CPU metrics and replica counts in Grafana.

## 4) Observability Story
- Use Prometheus/Grafana to show request latency and error rate.
- Show Linkerd per-service success rate.

## 5) EKS Portability
- Deploy with values-eks.yaml.
- Show that only values changed, not chart or services.
