import httpx
from fastapi import Header, HTTPException

from app.config import settings


def _unkey_valid_from_body(body: dict) -> bool:
    """Support v2 envelope { data: { valid } } and legacy { valid }."""
    if not isinstance(body, dict):
        return False
    data = body.get("data")
    if isinstance(data, dict) and "valid" in data:
        return bool(data.get("valid"))
    return bool(body.get("valid"))


async def ensure_unkey_validated(api_key: str | None) -> str:
    if not settings.unkey_enabled:
        return api_key or "dev-local"
    if not api_key:
        raise HTTPException(status_code=401, detail="Missing X-API-Key")
    root = (settings.unkey_root_key or "").strip()
    if not root:
        raise HTTPException(
            status_code=503,
            detail="Server missing UNKEY_ROOT_KEY — add your Unkey root key to backend/.env",
        )
    headers = {
        "Authorization": f"Bearer {root}",
        "Content-Type": "application/json",
    }
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            r = await client.post(
                settings.unkey_verify_url,
                headers=headers,
                json={"key": api_key},
            )
    except httpx.ConnectError as e:
        raise HTTPException(
            status_code=503,
            detail=f"Cannot reach Unkey API ({settings.unkey_verify_url}). Check internet/DNS/firewall. {e!s}",
        ) from e
    except httpx.TimeoutException as e:
        raise HTTPException(status_code=504, detail="Unkey verification timed out") from e

    if r.status_code != 200:
        raise HTTPException(
            status_code=502,
            detail=f"Unkey verification failed (HTTP {r.status_code}): {r.text[:300]}",
        )
    try:
        body = r.json()
    except Exception:
        raise HTTPException(status_code=502, detail="Unkey returned non-JSON") from None

    if not _unkey_valid_from_body(body):
        raise HTTPException(status_code=403, detail="Invalid API key")
    return api_key


async def verify_unkey_key(x_api_key: str | None = Header(default=None, alias="X-API-Key")) -> str:
    return await ensure_unkey_validated(x_api_key)
