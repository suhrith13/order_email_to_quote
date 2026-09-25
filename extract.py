"""Calls a local Ollama model and validates its output against ExtractedOrder.

Ollama is free and runs locally: https://ollama.com
Start it with `ollama serve` and make sure you've run `ollama pull llama3.2`.
"""

import json

import requests
from pydantic import ValidationError

from schema import ExtractedOrder

OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL = "llama3.2"  # swap for any model you've pulled, e.g. "qwen2.5:7b"

SYSTEM_PROMPT = (
    "You extract structured order data from messy free-text order emails for a "
    "plumbing/electrical/HVAC distributor. Extract every line item with its "
    "quantity and any size/spec mentioned. Only output the JSON object requested."
)


def _call_ollama(email_text: str, repair_note: str | None = None) -> dict:
    prompt = f"Order email:\n---\n{email_text}\n---\nExtract the structured order."
    if repair_note:
        prompt += f"\n\nYour previous output was invalid: {repair_note}\nFix it and return valid JSON only."

    resp = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL,
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt},
            ],
            "format": ExtractedOrder.model_json_schema(),
            "stream": False,
        },
        timeout=120,
    )
    resp.raise_for_status()
    content = resp.json()["message"]["content"]
    return json.loads(content)


def extract_order(email_text: str) -> ExtractedOrder | None:
    """Returns a validated ExtractedOrder, or None if extraction fails twice.

    This is the fallback path: a caller MUST handle the None case (e.g. queue
    the email for a human) rather than assume extraction always succeeds.
    """
    last_error = None
    for attempt in range(2):
        try:
            raw = _call_ollama(email_text, repair_note=last_error)
            return ExtractedOrder.model_validate(raw)
        except (ValidationError, json.JSONDecodeError, requests.RequestException) as e:
            last_error = str(e)
    print(f"  ! extraction failed after retry: {last_error}")
    return None


if __name__ == "__main__":
    sample = """Hi, need 10x 1/2" copper elbow and 4 ea 3/4 in PVC coupling. Rush please."""
    result = extract_order(sample)
    print(result.model_dump_json(indent=2) if result else "extraction failed")
