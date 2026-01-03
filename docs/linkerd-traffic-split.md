# Linkerd Traffic Split (Canary)

This chunk deploys two versions of a simple service and splits traffic 90/10 using Gateway API HTTPRoute.

## Prereqs
- Linkerd is installed and `linkerd check` passes.
- The `demo` namespace exists and is annotated for injection.

## Ensure Gateway API CRDs Exist
```bash
kubectl apply -f https://github.com/kubernetes-sigs/gateway-api/releases/download/v1.2.1/standard-install.yaml
kubectl get crd httproutes.gateway.networking.k8s.io
```

## Deploy the Split Demo
```bash
kubectl -n demo delete deployment/web service/web --ignore-not-found
kubectl -n demo delete trafficsplit web-split --ignore-not-found
kubectl apply -f k8s/linkerd-traffic-split.yaml
kubectl -n demo get httproute
```

## Generate Traffic
```bash
kubectl -n demo delete pod curl --ignore-not-found
kubectl -n demo run curl --image=curlimages/curl --command -- sleep 3600
for i in $(seq 1 50); do kubectl -n demo exec -c curl curl -- curl -sS web; done
```

## Observe the Split
```bash
linkerd viz stat deploy -n demo
```
You should see most traffic on `web-v1` and a smaller share on `web-v2`
(roughly 90/10 after a few dozen requests).
