import os
import json
import requests

SCALEDOWN_URL = "https://api.scaledown.xyz/compress/raw/"


def compress_prompt(context: str, question: str, model="gpt-4o"):
    api_key = os.getenv("SCALEDOWN_API_KEY")

    if not api_key:
        raise RuntimeError("SCALEDOWN_API_KEY not set")

    headers = {
        "x-api-key": api_key,
        "Content-Type": "application/json"
    }

    payload = {
        "context": context,
        "prompt": question,
        "model": model,
        "scaledown": {
            "rate": "auto"
        }
    }

    res = requests.post(
        SCALEDOWN_URL,
        headers=headers,
        data=json.dumps(payload)
    )

    res.raise_for_status()

    data = res.json()
    print("\n[SCALEDOWN RESPONSE]", data)

    # Handle ScaleDown response structure
    if not data.get("successful") and not data.get("results", {}).get("success"):
        raise RuntimeError(f"ScaleDown failed: {data}")

    return data["results"]["compressed_prompt"]
