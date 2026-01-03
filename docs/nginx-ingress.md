# NGINX Ingress (Local Cluster)

This step installs the NGINX Ingress Controller for local access on Proxmox.

## Install (Helm)
1. Add the Helm repo and update:
   - `helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx`
   - `helm repo update`

2. Install the controller:
   - `helm install ingress-nginx ingress-nginx/ingress-nginx \
       --namespace ingress-nginx \
       --create-namespace`

## Validate
- `kubectl get pods -n ingress-nginx`
- `kubectl get svc -n ingress-nginx`
- Confirm the `ingress-nginx-controller` Service has a reachable IP/NodePort.

## Test Routing (Echo Service)
1. Deploy a small echo service + ingress:
   - `scripts/deploy-echo-test.sh`
2. Run the validation (set a node IP):
   - `INGRESS_NODE_IP=192.168.6.4 scripts/validate-echo-test.sh`

## Notes
- For Proxmox, NodePort is often easiest for local testing.
- The chart defaults to `ingressClass=nginx`, which matches this repo's Helm values.
