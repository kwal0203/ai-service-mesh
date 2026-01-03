#!/usr/bin/env bash
set -euo pipefail

node_ip="${INGRESS_NODE_IP:-}"
if [ -z "$node_ip" ]; then
  echo "Set INGRESS_NODE_IP to a node IP (e.g., 192.168.6.4)." >&2
  exit 1
fi

node_port="${INGRESS_NODE_PORT:-}"
if [ -z "$node_port" ]; then
  node_port=$(kubectl get svc ingress-nginx-controller -n ingress-nginx \
    -o jsonpath='{.spec.ports[?(@.port==80)].nodePort}')
fi

if [ -z "$node_port" ]; then
  echo "Could not determine NodePort for ingress-nginx-controller port 80." >&2
  exit 1
fi

curl -fsS -H "Host: echo.local" "http://$node_ip:$node_port/" | rg -q "echo-ok"

echo "Echo ingress OK"
