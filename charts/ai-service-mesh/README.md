# ai-service-mesh Helm Chart

## Install (local Proxmox)
```
helm install ai-mesh charts/ai-service-mesh -f charts/ai-service-mesh/values-local.yaml --create-namespace
```

If an install fails partway through, remove the release before retrying:
```
helm uninstall ai-mesh
```

## Local Images (Proxmox)
Build and tag images to match `values-local.yaml` on a node that can load images
into the cluster's container runtime:
```
docker build -t ai-mesh/gateway:dev -f services/gateway/Dockerfile .
docker build -t ai-mesh/embedding:dev -f services/embedding/Dockerfile .
docker build -t ai-mesh/classifier:dev -f services/classifier/Dockerfile .
docker build -t ai-mesh/eval:dev -f services/eval/Dockerfile .
docker build -t ai-mesh/llm:dev -f services/llm/Dockerfile .
docker build -t ai-mesh/vision:dev -f services/vision/Dockerfile .
```

## GHCR Images (Option 2)
To use GitHub Container Registry (public), build and push:
```
docker build -t ghcr.io/kwal0203/ai-mesh-gateway:dev -f services/gateway/Dockerfile .
docker build -t ghcr.io/kwal0203/ai-mesh-embedding:dev -f services/embedding/Dockerfile .
docker build -t ghcr.io/kwal0203/ai-mesh-classifier:dev -f services/classifier/Dockerfile .
docker build -t ghcr.io/kwal0203/ai-mesh-eval:dev -f services/eval/Dockerfile .
docker build -t ghcr.io/kwal0203/ai-mesh-llm:dev -f services/llm/Dockerfile .
docker build -t ghcr.io/kwal0203/ai-mesh-vision:dev -f services/vision/Dockerfile .

docker push ghcr.io/kwal0203/ai-mesh-gateway:dev
docker push ghcr.io/kwal0203/ai-mesh-embedding:dev
docker push ghcr.io/kwal0203/ai-mesh-classifier:dev
docker push ghcr.io/kwal0203/ai-mesh-eval:dev
docker push ghcr.io/kwal0203/ai-mesh-llm:dev
docker push ghcr.io/kwal0203/ai-mesh-vision:dev
```

## Install (EKS)
```
helm install ai-mesh charts/ai-service-mesh -f charts/ai-service-mesh/values-eks.yaml
```

## HPA + Linkerd
When HPA is enabled with Linkerd injection, the chart sets proxy CPU requests
via `mesh.proxyResources` to avoid `<unknown>` HPA targets.

## Resource Isolation (Quota + LimitRange)
Enable namespace-level resource isolation with a ResourceQuota and LimitRange:
```
resourceIsolation:
  enabled: true
  quota:
    pods: "12"
    requestsCpu: "2"
    requestsMemory: "4Gi"
    limitsCpu: "4"
    limitsMemory: "8Gi"
  limitRange:
    default:
      cpu: 500m
      memory: 512Mi
    defaultRequest:
      cpu: 100m
      memory: 256Mi
```

## NetworkPolicy (Ingress Isolation)
Restrict ingress to same-namespace pods plus selected namespaces:
```
networkPolicy:
  enabled: true
  allowIngressFromNamespaces:
    - ingress-nginx
    - monitoring
```
This uses the `kubernetes.io/metadata.name` namespace label.

## Traffic Split (Gateway API HTTPRoute)
To enable a canary split with Gateway API HTTPRoute, add a second service entry
for the canary and enable the split in values:

```
trafficSplit:
  enabled: true
  service: classifier
  port: 8002
  backends:
    - name: classifier-stable
      serviceSuffix: classifier
      port: 8002
      weight: 90
    - name: classifier-canary
      serviceSuffix: classifier-canary
      port: 8002
      weight: 10
```

This assumes you have two Services named `<release>-classifier` and `<release>-classifier-canary`.
Gateway API CRDs must be installed in the cluster.

Example:
```
helm upgrade --install ai-mesh charts/ai-service-mesh \
  -f charts/ai-service-mesh/values-local.yaml \
  -f charts/ai-service-mesh/values-canary.yaml
```

`values-canary.yaml` adds a `classifier-canary` deployment via `canaryServices`.
Override the canary image tag to match your registry if needed.
