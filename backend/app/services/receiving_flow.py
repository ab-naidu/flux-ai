"""
Receiving pipeline implemented with the Railtracks agentic framework.

- Project: https://github.com/RailtownAI/railtracks
- Flow + function_node + async ``call()`` composition for observability-friendly structure.
"""

from __future__ import annotations

from railtracks import Flow, call, function_node

from app.schemas import InventorySyncRequest
from app.services.operator_brief import brief_for_agent


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


@function_node
def rt_step_multimodal_extract(raw_image: bytes, mime_type: str) -> dict:
    """Tool node: Gemini vision + JSON extraction (invoice + pallet)."""
    from app.services.gemini_service import analyze_delivery_image

    return analyze_delivery_image(raw_image, mime_type=mime_type)


@function_node
async def rt_step_post_inventory(sync_payload: dict) -> dict:
    """Tool node: Unkey-gated inventory sync (async I/O)."""
    from app.services.inventory_service import perform_inventory_sync

    body = InventorySyncRequest(**sync_payload)
    res = await perform_inventory_sync(body)
    return res.model_dump()


@function_node
async def rt_flux_receiving_agent(
    raw_image: bytes,
    mime_type: str,
    auto_sync_when_clean: bool,
    master_trace_id: str,
) -> dict:
    """
    Entry node: orchestrates multimodal read → variance policy → optional sync via ``rt.call``.
    """
    cognitive = await call(rt_step_multimodal_extract, raw_image, mime_type)
    line_items = cognitive.get("line_items") or []
    notes = cognitive.get("notes") or ""
    hitl = _needs_hitl(line_items)

    out: dict = {
        "trace_id": master_trace_id,
        "autonomy": "paused_for_hitl" if hitl else "completed_without_manual_steps",
        "line_items": line_items,
        "notes": notes,
        "sync": None,
        "railtracks": {
            "framework": "https://github.com/RailtownAI/railtracks",
            "flow_name": "Flux AI — Multimodal Receiving",
            "entry_node": "rt_flux_receiving_agent",
            "tool_nodes": ["rt_step_multimodal_extract", "rt_step_post_inventory"],
        },
    }

    if hitl or not auto_sync_when_clean:
        out["next_step"] = (
            "Review the variance table, then confirm inventory update in the app (or POST /api/inventory/sync)."
        )
        out["operator_brief"] = brief_for_agent(
            hitl=hitl,
            auto_sync_when_clean=auto_sync_when_clean,
            autonomy=str(out["autonomy"]),
            sync_ok=None,
        )
        return out

    sync_body = InventorySyncRequest(
        approved=True,
        line_items=line_items,
        notes=notes or None,
        trace_id=master_trace_id,
    )
    sync_dump = await call(rt_step_post_inventory, sync_body.model_dump(mode="json"))
    out["sync"] = sync_dump
    out["autonomy"] = "auto_executed_inventory_sync"
    sync_ok = bool(sync_dump.get("ok"))
    if sync_ok:
        out["operator_brief"] = brief_for_agent(
            hitl=False,
            auto_sync_when_clean=True,
            autonomy="auto_executed_inventory_sync",
            sync_ok=True,
        )
    else:
        out["operator_brief"] = {
            "headline": "Vision succeeded — inventory update failed",
            "subtext": (
                "The agent compared invoice to scene and attempted a gated write, but the downstream "
                "system did not accept it. Check API logs or mock URL configuration."
            ),
            "next_action": "Inspect the sync block in the response or fix the target endpoint.",
            "steps": [
                {"id": "upload", "label": "Photo received", "state": "done"},
                {"id": "vision", "label": "Gemini read invoice + scene", "state": "done"},
                {"id": "compare", "label": "Variance check", "state": "done"},
                {"id": "sync", "label": "Inventory update", "state": "error"},
            ],
        }
    return out


_flux_receiving_flow = Flow(
    name="Flux AI — Multimodal Receiving",
    entry_point=rt_flux_receiving_agent,
)


async def execute_receiving_flow(
    raw_image: bytes,
    mime_type: str,
    auto_sync_when_clean: bool,
    master_trace_id: str,
) -> dict:
    """Run the Railtracks Flow inside FastAPI (uses ``ainvoke`` — no nested asyncio.run)."""
    return await _flux_receiving_flow.ainvoke(
        raw_image,
        mime_type,
        auto_sync_when_clean,
        master_trace_id,
    )
