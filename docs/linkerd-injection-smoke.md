# Linkerd Injection Smoke Test

This chunk enables Linkerd injection on a demo namespace and confirms sidecars and mTLS.
Run these commands on the control-plane node or any host with `kubectl` configured to the cluster.

## Create Namespace With Injection
```bash
kubectl create namespace demo
kubectl annotate namespace demo linkerd.io/inject=enabled
```

## Deploy a Minimal App
```bash
cat <<'EOF' | kubectl -n demo apply -f -
apiVersion: apps/v1
kind: Deployment
metadata:
  name: web
spec:
  replicas: 1
  selector:
    matchLabels:
      app: web
  template:
    metadata:
      labels:
        app: web
    spec:
      containers:
        - name: web
          image: nginx:alpine
          ports:
            - containerPort: 80
---
apiVersion: v1
kind: Service
metadata:
  name: web
spec:
  selector:
    app: web
  ports:
    - port: 80
      targetPort: 80
EOF
```

## Verify Sidecar Injection
```bash
kubectl -n demo get pods
kubectl -n demo get pod -l app=web -o jsonpath='{.items[0].spec.containers[*].name}{"\n"}'
```
You should see `linkerd-proxy` alongside `web`.

## Verify Linkerd Proxy Health
```bash
linkerd -n demo check --proxy
```

## (Optional) mTLS Probe
```bash
kubectl -n demo run curl --image=curlimages/curl --command -- sleep 3600
kubectl -n demo exec curl -- curl -sS web
```
