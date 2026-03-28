import json
import logging
import time
import uuid
from contextlib import contextmanager
from typing import Any, Iterator

import httpx

from app.config import settings

logger = logging.getLogger(__name__)


def _emit_webhook(name: str, trace_id: str, ms: float, phase: str) -> None:
    url = (settings.railtracks_webhook_url or "").strip()
    if not url:
        return
    payload = {
        "source": "flux-ai",
        "span": name,
        "trace_id": trace_id,
        "phase": phase,
        "duration_ms": round(ms, 2),
        "railtracks_enabled": settings.railtracks_enabled,
    }
    try:
        with httpx.Client(timeout=3.0) as client:
            client.post(url, json=payload)
    except Exception:
        logger.warning("railtracks webhook failed for %s", trace_id, exc_info=False)


@contextmanager
def trace(name: str, input_payload: dict[str, Any] | None = None) -> Iterator[str]:
    """
    Audit trace IDs for every multimodal / sync step.
    Set RAILTRACKS_WEBHOOK_URL to forward spans to your Railtracks-compatible sink.
    """
    trace_id = str(uuid.uuid4())
    t0 = time.perf_counter()
    if settings.railtracks_enabled:
        logger.info(
            "railtracks.trace start %s trace_id=%s input=%s",
            name,
            trace_id,
            json.dumps(input_payload or {}, default=str)[:2000],
        )
    else:
        logger.info("audit.trace start %s trace_id=%s", name, trace_id)
    _emit_webhook(name, trace_id, 0.0, "start")
    try:
        yield trace_id
    finally:
        ms = (time.perf_counter() - t0) * 1000
        if settings.railtracks_enabled:
            logger.info("railtracks.trace end %s trace_id=%s ms=%.1f", name, trace_id, ms)
        else:
            logger.info("audit.trace end %s trace_id=%s ms=%.1f", name, trace_id, ms)
        _emit_webhook(name, trace_id, ms, "end")
