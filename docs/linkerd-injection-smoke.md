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
kubectl apply -f k8s/linkerd-injection-smoke.yaml
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
