from fastapi import APIRouter, Depends

from app.deps import verify_unkey_key
from app.schemas import InventorySyncRequest, InventorySyncResponse
from app.services.inventory_service import perform_inventory_sync

router = APIRouter(prefix="/api/inventory", tags=["inventory"])


@router.post("/sync", response_model=InventorySyncResponse)
async def sync_inventory(
    body: InventorySyncRequest,
    _key: str = Depends(verify_unkey_key),
) -> InventorySyncResponse:
    return await perform_inventory_sync(body)
