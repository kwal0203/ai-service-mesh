#!/usr/bin/env bash
set -euo pipefail

docker compose build ml-base
docker compose build embedding llm vision
docker compose build
