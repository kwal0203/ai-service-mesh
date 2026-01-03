#!/usr/bin/env bash
set -euo pipefail

kubectl get pods -n ingress-nginx
kubectl get svc -n ingress-nginx
