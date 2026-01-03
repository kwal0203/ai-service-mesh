#!/usr/bin/env bash
set -euo pipefail

helm template ai-mesh charts/ai-service-mesh -f charts/ai-service-mesh/values-local.yaml
