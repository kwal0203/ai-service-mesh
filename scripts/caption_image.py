#!/usr/bin/env python3
import json
import os

import httpx

SAMPLE_IMAGE = (
    "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR4nGNgYAAAAAMA"
    "ASsJTYQAAAAASUVORK5CYII="
)


def main() -> int:
    base_url = os.getenv("BASE_URL", "http://localhost:8000").rstrip("/")
    image_base64 = os.getenv("IMAGE_BASE64", SAMPLE_IMAGE)
    top_k = int(os.getenv("TOP_K", "3"))
    timeout = float(os.getenv("TIMEOUT_SECONDS", "120"))

    payload = {"image_base64": image_base64, "top_k": top_k}
    response = httpx.post(f"{base_url}/caption", json=payload, timeout=timeout)
    response.raise_for_status()
    print(json.dumps(response.json(), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
