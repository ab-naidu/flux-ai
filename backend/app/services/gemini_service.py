import io
import json
import logging
from typing import Any

import google.generativeai as genai
from PIL import Image

from app.config import settings

logger = logging.getLogger(__name__)

AUDIT_PROMPT = """You are Flux AI, a receiving dock auditor.
The image may show a paper invoice/packing list AND physical goods (e.g. cases on a pallet).

Tasks:
1. From any visible invoice text, extract line items: sku or description, expected quantity, unit (e.g. cases).
2. From the visible physical goods, estimate actual counts for those line items (integer).
3. If you cannot read a value, use null and explain in notes.

Return ONLY valid JSON matching this shape:
{
  "line_items": [
    {
      "line_id": 1,
      "description": "string",
      "sku": "string or null",
      "expected_qty": number or null,
      "actual_qty": number or null,
      "unit": "cases" | "units" | "pallets" | "unknown",
      "variance": number or null
    }
  ],
  "notes": "short string"
}

variance = actual_qty - expected_qty when both are numbers; else null.
"""


def _ensure_client() -> None:
    if not settings.gemini_api_key:
        raise RuntimeError("GEMINI_API_KEY is not set")
    genai.configure(api_key=settings.gemini_api_key)


def analyze_delivery_image(image_bytes: bytes, mime_type: str = "image/jpeg") -> dict[str, Any]:
    _ensure_client()
    img = Image.open(io.BytesIO(image_bytes))
    model = genai.GenerativeModel(settings.gemini_model)
    response = model.generate_content(
        [AUDIT_PROMPT, img],
        generation_config=genai.GenerationConfig(
            response_mime_type="application/json",
        ),
    )
    text = (response.text or "").strip()
    try:
        data = json.loads(text)
    except json.JSONDecodeError:
        logger.exception("Gemini returned non-JSON: %s", text[:500])
        raise
    return _normalize_result(data)


def _normalize_result(data: dict[str, Any]) -> dict[str, Any]:
    items = data.get("line_items") or []
    out_items = []
    for row in items:
        exp = row.get("expected_qty")
        act = row.get("actual_qty")
        var = row.get("variance")
        if var is None and isinstance(exp, (int, float)) and isinstance(act, (int, float)):
            var = int(act) - int(exp)
        out_items.append(
            {
                "line_id": row.get("line_id"),
                "description": row.get("description"),
                "sku": row.get("sku"),
                "expected_qty": exp,
                "actual_qty": act,
                "unit": row.get("unit") or "unknown",
                "variance": var,
            }
        )
    return {"line_items": out_items, "notes": data.get("notes") or ""}
