"""
Autonomous receiving pipeline for hackathon Autonomy rubric:
one upload → Railtracks Flow (multimodal node → policy → optional sync node).
"""

from typing import Annotated

from fastapi import APIRouter, File, Form, Header, HTTPException, UploadFile

from app.deps import ensure_unkey_validated
from app.services.receiving_flow import execute_receiving_flow
from app.services.railtracks import trace

router = APIRouter(prefix="/api/agent", tags=["agent"])


@router.post("/run")
async def agent_run(
    file: Annotated[UploadFile, File(description="Pallet + invoice image")],
    x_api_key: Annotated[str | None, Header(alias="X-API-Key")] = None,
    auto_sync_when_clean: Annotated[bool, Form()] = True,
) -> dict:
    """
    Validates Unkey first (NFR: no mutation path without Unkey when enabled).
    Runs the receiving agent as a Railtracks Flow (see ``app.services.receiving_flow``).
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
            return await execute_receiving_flow(
                raw,
                mime,
                auto_sync_when_clean,
                master_trace_id,
            )
        except RuntimeError as e:
            raise HTTPException(status_code=503, detail=str(e)) from e
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Agent run failed: {e!s}") from e
