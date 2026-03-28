import json

import httpx

from app.config import settings
from app.schemas import InventorySyncRequest, InventorySyncResponse
from app.services.railtracks import trace


async def perform_inventory_sync(body: InventorySyncRequest) -> InventorySyncResponse:
    with trace(
        "inventory.sync",
        {"approved": body.approved, "lines": len(body.line_items)},
    ) as trace_id:
        if not body.approved:
            return InventorySyncResponse(ok=False, trace_id=trace_id)

        payload = {
            "trace_id": trace_id,
            "line_items": body.line_items,
            "notes": body.notes,
        }
        if not settings.mock_inventory_url.strip():
            body_txt = json.dumps({"ok": True, "target": "in_process_mock", "received": payload})
            return InventorySyncResponse(
                ok=True,
                trace_id=trace_id,
                downstream_status=200,
                downstream_body=body_txt,
            )

        async with httpx.AsyncClient(timeout=15.0) as client:
            try:
                r = await client.post(settings.mock_inventory_url, json=payload)
                text = r.text[:4000]
                return InventorySyncResponse(
                    ok=200 <= r.status_code < 300,
                    trace_id=trace_id,
                    downstream_status=r.status_code,
                    downstream_body=text,
                )
            except httpx.RequestError as e:
                return InventorySyncResponse(
                    ok=False,
                    trace_id=trace_id,
                    downstream_status=None,
                    downstream_body=str(e),
                )
