#!/usr/bin/env python3
import json
import os

import httpx


def main() -> int:
    base_url = os.getenv("BASE_URL", "http://localhost:8000").rstrip("/")
    query = os.getenv("QUERY", "How do you monitor latency and errors?")
    timeout = float(os.getenv("TIMEOUT_SECONDS", "120"))

    payload = {"query": query}
    response = httpx.post(f"{base_url}/route", json=payload, timeout=timeout)
    response.raise_for_status()
    print(json.dumps(response.json(), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
