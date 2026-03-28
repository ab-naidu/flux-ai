from typing import Any

from pydantic import BaseModel, Field


class InventorySyncRequest(BaseModel):
    trace_id: str | None = None
    approved: bool = True
    line_items: list[dict[str, Any]] = Field(default_factory=list)
    notes: str | None = None


class InventorySyncResponse(BaseModel):
    ok: bool
    trace_id: str
    downstream_status: int | None = None
    downstream_body: str | None = None
