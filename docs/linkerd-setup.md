# Linkerd Setup (Local Cluster)

This chunk installs Linkerd on the local Proxmox Kubernetes cluster and verifies health.

## Prereqs
- `kubectl` configured to talk to the local cluster.
- Cluster nodes reachable and Ready.

## Install Linkerd CLI
```bash
curl -sL https://run.linkerd.io/install | sh
export PATH="$PATH:$HOME/.linkerd2/bin"
linkerd version
```

## Preflight Checks
```bash
linkerd check --pre
```

## Install CRDs and Control Plane
```bash
linkerd install --crds | kubectl apply -f -
linkerd install | kubectl apply -f -
```

## Verify
```bash
linkerd check
```

## Optional: Linkerd Viz (Dashboard)
```bash
linkerd viz install | kubectl apply -f -
linkerd viz check
linkerd viz dashboard
```
