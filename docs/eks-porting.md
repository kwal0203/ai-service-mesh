# EKS Porting Notes

This demo is designed to run on Proxmox and EKS with minimal changes.
Keep the chart identical and swap values files.

## Minimal Values Diff
- Proxmox: `ingress.className=nginx`, `storageClass=local-path`
- EKS: `ingress.className=alb`, `storageClass=gp3`

## Prereqs (EKS)
- AWS Load Balancer Controller installed.
- A `gp3` StorageClass available (default on most EKS clusters).
- Cluster has access to the image registry you use.

## Install (EKS)
```
helm upgrade --install ai-mesh charts/ai-service-mesh \
  -f charts/ai-service-mesh/values-eks.yaml \
  --namespace ai-mesh --create-namespace
```

## Verify
```
kubectl -n ai-mesh get ingress
kubectl -n ai-mesh get svc
```
