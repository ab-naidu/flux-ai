"""
Autonomous receiving pipeline for hackathon Autonomy rubric:
one upload → multimodal analyze → if no variance, sync without extra UI steps.
If variance exists, return HITL state (frontend + Assistant UI approves, then POST /api/inventory/sync).
"""

from typing import Annotated

from fastapi import APIRouter, File, Form, Header, HTTPException, UploadFile

from app.deps import ensure_unkey_validated
from app.schemas import InventorySyncRequest, InventorySyncResponse
from app.services.gemini_service import analyze_delivery_image
from app.services.inventory_service import perform_inventory_sync
from app.services.railtracks import trace

router = APIRouter(prefix="/api/agent", tags=["agent"])


def _needs_hitl(line_items: list[dict]) -> bool:
    for row in line_items:
        v = row.get("variance")
        if v is None:
            continue
        try:
            if int(v) != 0:
                return True
        except (TypeError, ValueError):
            return True
    return False


@router.post("/run")
async def agent_run(
    file: Annotated[UploadFile, File(description="Pallet + invoice image")],
    x_api_key: Annotated[str | None, Header(alias="X-API-Key")] = None,
    auto_sync_when_clean: Annotated[bool, Form()] = True,
) -> dict:
    """
    Validates Unkey first (NFR: no mutation path without Unkey when enabled).
    When variances are all zero (or null), optionally performs inventory sync automatically.
    """
    await ensure_unkey_validated(x_api_key)

    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Upload an image (jpg/png/webp)")
    raw = await file.read()
    if len(raw) > 12 * 1024 * 1024:
        raise HTTPException(status_code=413, detail="Image too large (max 12MB)")
    mime = file.content_type.split(";")[0].strip()

    with trace(
        "agent.receiving_pipeline",
        {"filename": file.filename, "bytes": len(raw), "auto_sync": auto_sync_when_clean},
    ) as master_trace_id:
        try:
            cognitive = analyze_delivery_image(raw, mime_type=mime)
        except RuntimeError as e:
            raise HTTPException(status_code=503, detail=str(e)) from e
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Analysis failed: {e!s}") from e

        line_items = cognitive.get("line_items") or []
        hitl = _needs_hitl(line_items)

        out: dict = {
            "trace_id": master_trace_id,
            "autonomy": "paused_for_hitl" if hitl else "completed_without_manual_steps",
            "line_items": line_items,
            "notes": cognitive.get("notes") or "",
            "sync": None,
        }

        if hitl or not auto_sync_when_clean:
            out["next_step"] = (
                "Use Assistant UI to approve; then POST /api/inventory/sync with the same X-API-Key."
            )
            return out

        sync_body = InventorySyncRequest(
            approved=True,
            line_items=line_items,
            notes=cognitive.get("notes"),
            trace_id=master_trace_id,
        )
        sync_result: InventorySyncResponse = await perform_inventory_sync(sync_body)
        out["sync"] = sync_result.model_dump()
        out["autonomy"] = "auto_executed_inventory_sync"
        return out
