#!/usr/bin/env bash
set -euo pipefail

chart_dir="charts/ai-service-mesh"

printf "Helm lint (local values)\n"
helm lint "$chart_dir" -f "$chart_dir/values-local.yaml"

printf "Helm lint (eks values)\n"
helm lint "$chart_dir" -f "$chart_dir/values-eks.yaml"

printf "Helm template (local values)\n"
helm template ai-mesh "$chart_dir" -f "$chart_dir/values-local.yaml" >/dev/null

printf "Helm template (eks values)\n"
helm template ai-mesh "$chart_dir" -f "$chart_dir/values-eks.yaml" >/dev/null
