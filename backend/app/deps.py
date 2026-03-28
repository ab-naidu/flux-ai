import httpx
from fastapi import Header, HTTPException

from app.config import settings


async def ensure_unkey_validated(api_key: str | None) -> str:
    if not settings.unkey_enabled:
        return api_key or "dev-local"
    if not api_key:
        raise HTTPException(status_code=401, detail="Missing X-API-Key")
    async with httpx.AsyncClient(timeout=10.0) as client:
        r = await client.post(
            settings.unkey_verify_url,
            json={"key": api_key},
        )
    if r.status_code != 200:
        raise HTTPException(status_code=502, detail="Unkey verification failed")
    body = r.json()
    if not body.get("valid"):
        raise HTTPException(status_code=403, detail="Invalid API key")
    return api_key


async def verify_unkey_key(x_api_key: str | None = Header(default=None, alias="X-API-Key")) -> str:
    return await ensure_unkey_validated(x_api_key)
