#!/usr/bin/env bash
set -euo pipefail

base_url="${BASE_URL:-http://localhost}"

check() {
  local name="$1"
  local url="$2"
  printf "Checking %s at %s... " "$name" "$url"
  curl -fsS "$url" >/dev/null
  printf "ok\n"
}

check "gateway" "$base_url:8000/healthz"
check "embedding" "$base_url:8001/healthz"
check "classifier" "$base_url:8002/healthz"
check "eval" "$base_url:8003/healthz"
