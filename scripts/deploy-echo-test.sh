#!/usr/bin/env bash
set -euo pipefail

kubectl apply -f k8s/echo-test.yaml
kubectl rollout status deployment/echo-test
