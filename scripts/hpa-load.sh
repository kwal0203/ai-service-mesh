#!/usr/bin/env bash
set -euo pipefail

action="${1:-run}"
namespace="${2:-demo}"
pod_name="${3:-hpa-load}"

if [[ "$action" == "cleanup" ]]; then
  kubectl -n "$namespace" delete pod "$pod_name" --ignore-not-found
  exit 0
fi

kubectl -n "$namespace" delete pod "$pod_name" --ignore-not-found
kubectl -n "$namespace" run "$pod_name" --image=busybox --command -- \
  /bin/sh -c "while true; do wget -q -O- http://hpa-demo; done"
