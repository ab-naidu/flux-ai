"""
Optional stand-in for a grocery OS / ERP webhook (e.g. Vori-style).
Point MOCK_INVENTORY_URL to this server's public URL + /mock/vori/receiving if you want HTTP hops visible in logs.
"""

from fastapi import APIRouter

router = APIRouter(prefix="/mock", tags=["mock"])


@router.post("/vori/receiving")
async def vori_receiving(payload: dict) -> dict:
    return {"ok": True, "system": "vori-style-mock", "echo": payload}
