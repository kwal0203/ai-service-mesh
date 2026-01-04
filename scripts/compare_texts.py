#!/usr/bin/env python3
import json
import os

import httpx


def main() -> int:
    base_url = os.getenv("BASE_URL", "http://localhost:8000").rstrip("/")
    text_a = os.getenv("TEXT_A", "Proxmox cluster for local demos.")
    text_b = os.getenv("TEXT_B", "EKS cluster in the cloud.")
    timeout = float(os.getenv("TIMEOUT_SECONDS", "120"))

    payload = {"text_a": text_a, "text_b": text_b}
    response = httpx.post(f"{base_url}/compare", json=payload, timeout=timeout)
    response.raise_for_status()
    print(json.dumps(response.json(), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
