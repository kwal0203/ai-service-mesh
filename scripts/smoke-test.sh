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

if [[ "${RUN_ML_SMOKE:-0}" == "1" ]]; then
  RUN_PREDICT_SMOKE=1
  RUN_RAG_SMOKE=1
  RUN_COMPARE_SMOKE=1
  RUN_LLM_SMOKE=1
  RUN_CAPTION_SMOKE=1
  RUN_VISION_SMOKE=1
fi

if [[ "${RUN_PREDICT_SMOKE:-0}" == "1" ]]; then
  printf "Checking gateway predict... "
  curl -fsS -X POST "$base_url:8000/predict" \
    -H "Content-Type: application/json" \
    -d '{"text":"quick brown fox"}' >/dev/null
  printf "ok\n"
fi

if [[ "${RUN_RAG_SMOKE:-0}" == "1" ]]; then
  printf "Checking RAG-lite... "
  curl -fsS -X POST "$base_url:8000/rag-lite" \
    -H "Content-Type: application/json" \
    -d '{"question":"How does this demo port to EKS?","top_k":2}' >/dev/null
  printf "ok\n"
fi

if [[ "${RUN_COMPARE_SMOKE:-0}" == "1" ]]; then
  printf "Checking compare... "
  curl -fsS -X POST "$base_url:8000/compare" \
    -H "Content-Type: application/json" \
    -d '{"text_a":"Proxmox cluster for local demos.","text_b":"EKS cluster in the cloud."}' >/dev/null
  printf "ok\n"
fi

if [[ "${RUN_LLM_SMOKE:-0}" == "1" ]]; then
  printf "Checking LLM generate... "
  curl -fsS -X POST "$base_url:8000/generate" \
    -H "Content-Type: application/json" \
    -d '{"prompt":"Write a one-sentence summary about edge AI."}' >/dev/null
  printf "ok\n"
fi

if [[ "${RUN_CAPTION_SMOKE:-0}" == "1" ]]; then
  printf "Checking caption... "
  curl -fsS -X POST "$base_url:8000/caption" \
    -H "Content-Type: application/json" \
    -d '{"image_base64":"iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR4nGNgYAAAAAMAASsJTYQAAAAASUVORK5CYII=","top_k":3}' \
    >/dev/null
  printf "ok\n"
fi

if [[ "${RUN_VISION_SMOKE:-0}" == "1" ]]; then
  printf "Checking vision classify... "
  curl -fsS -X POST "$base_url:8000/classify-image" \
    -H "Content-Type: application/json" \
    -d '{"image_base64":"iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR4nGNgYAAAAAMAASsJTYQAAAAASUVORK5CYII=","top_k":3}' \
    >/dev/null
  printf "ok\n"
fi
