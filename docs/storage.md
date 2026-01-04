# Storage (MVP: local-path)

This project uses the local-path provisioner for local Proxmox clusters.

## Verify StorageClass
```
kubectl get storageclass
kubectl get storageclass local-path -o wide
```

If `local-path` is not present, install it:
```
kubectl apply -f https://raw.githubusercontent.com/rancher/local-path-provisioner/master/deploy/local-path-storage.yaml
```

## Quick PVC Test (Optional)
```
kubectl apply -f k8s/pvc-smoke.yaml
kubectl get pvc -n demo
kubectl delete -f k8s/pvc-smoke.yaml
```
