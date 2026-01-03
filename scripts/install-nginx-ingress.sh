#!/usr/bin/env bash
set -euo pipefail

if ! kubectl config current-context >/dev/null 2>&1; then
  echo "No kubeconfig context found. Set KUBECONFIG or run kubectl config use-context." >&2
  exit 1
fi

helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx
helm repo update

helm install ingress-nginx ingress-nginx/ingress-nginx \
  --namespace ingress-nginx \
  --create-namespace
