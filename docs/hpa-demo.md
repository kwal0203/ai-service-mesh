# HPA Demo (CPU Autoscaling)

This chunk deploys a minimal app and HPA, then generates load to observe scaling.

## Prereqs
- Metrics Server installed (`kubectl top nodes` works).
- `demo` namespace exists.

If Metrics Server is missing:
```bash
kubectl apply -f https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml
```

## Deploy the Demo + HPA
If the demo image fails to pull, switch the image in `k8s/hpa-demo.yaml` to a
reachable registry before re-applying.
```bash
kubectl apply -f k8s/hpa-demo.yaml
kubectl -n demo get deploy,hpa,svc
```
If HPA reports missing CPU requests for the Linkerd proxy, ensure the
`config.linkerd.io/proxy-cpu-request` annotation is set on the pod template in
`k8s/hpa-demo.yaml`.

## Generate Load
```bash
kubectl -n demo delete pod hpa-load --ignore-not-found
kubectl -n demo run hpa-load --image=busybox --command -- \
  /bin/sh -c "while true; do wget -q -O- http://hpa-demo; done"
```

## Watch Scaling
```bash
kubectl -n demo get hpa hpa-demo --watch
```
If `TARGETS` stays `<unknown>`, ensure the `hpa-demo` pod is Running and
`kubectl -n demo top pods` shows metrics.

## Cleanup
```bash
kubectl -n demo delete pod hpa-load --ignore-not-found
```
