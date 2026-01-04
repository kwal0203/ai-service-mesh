#!/usr/bin/env python3
import json
import os
import sys

import httpx


def main() -> int:
    base_url = os.getenv("BASE_URL", "http://localhost:8000").rstrip("/")
    question = os.getenv("QUESTION", "How does this demo port to EKS?")
    top_k = int(os.getenv("TOP_K", "2"))
    timeout = float(os.getenv("TIMEOUT_SECONDS", "300"))

    payload = {"question": question, "top_k": top_k}
    response = httpx.post(f"{base_url}/rag-lite", json=payload, timeout=timeout)
    response.raise_for_status()
    print(json.dumps(response.json(), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
