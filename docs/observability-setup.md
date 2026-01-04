# Observability Setup (Prometheus + Grafana)

This chunk installs Prometheus and Grafana for metrics visibility.

## Install (kube-prometheus-stack)
```bash
kubectl create namespace monitoring
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update
helm upgrade --install kube-prometheus-stack prometheus-community/kube-prometheus-stack \
  --namespace monitoring --create-namespace
```

## Verify
```bash
kubectl -n monitoring get pods
kubectl -n monitoring get svc
```

## Access Grafana
```bash
kubectl -n monitoring port-forward svc/kube-prometheus-stack-grafana 3000:80
```
Then open `http://127.0.0.1:3000` in your browser.

Admin credentials:
```bash
kubectl -n monitoring get secret kube-prometheus-stack-grafana \
  -o jsonpath="{.data.admin-password}" | base64 -d
```
User is `admin`. The password comes from the secret above.

## Optional: Linkerd Metrics
If Linkerd viz is installed, you can add Prometheus as a data source and explore
Linkerd dashboards in Grafana.
