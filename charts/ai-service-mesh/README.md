# ai-service-mesh Helm Chart

## Install (local Proxmox)
```
helm install ai-mesh charts/ai-service-mesh -f charts/ai-service-mesh/values-local.yaml
```

## Install (EKS)
```
helm install ai-mesh charts/ai-service-mesh -f charts/ai-service-mesh/values-eks.yaml
```

## Traffic Split (Linkerd SMI)
To enable a canary split, add a second service entry for the canary and enable the split in values:

```
trafficSplit:
  enabled: true
  service: classifier
  backends:
    - name: classifier-stable
      serviceSuffix: classifier
      weight: 90
    - name: classifier-canary
      serviceSuffix: classifier-canary
      weight: 10
```

This assumes you have two Services named `<release>-classifier` and `<release>-classifier-canary`.
