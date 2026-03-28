import logging
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import RedirectResponse, Response

from app.config import settings
from app.routers import agent, analyze, inventory, meta, mock_target

logging.basicConfig(level=logging.INFO)

SPONSOR_TOOL_HEADER = (
    "google-gemini; unkey; railtracks-traces; digitalocean-ready; "
    "bundled-ui-/ui"
)


class FluxSponsorMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next) -> Response:
        resp = await call_next(request)
        resp.headers["X-Flux-Sponsor-Tools"] = SPONSOR_TOOL_HEADER
        return resp


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    yield


def create_app() -> FastAPI:
    app = FastAPI(title="Flux AI API", version="0.1.0", lifespan=lifespan)
    origins = [o.strip() for o in settings.cors_origins.split(",") if o.strip()]
    use_all = not origins or origins == ["*"]
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"] if use_all else origins,
        allow_credentials=not use_all,
        allow_methods=["*"],
        allow_headers=["*"],
        expose_headers=["X-Flux-Sponsor-Tools"],
    )
    app.add_middleware(FluxSponsorMiddleware)
    app.include_router(meta.router)
    app.include_router(agent.router)
    app.include_router(analyze.router)
    app.include_router(inventory.router)
    app.include_router(mock_target.router)

    @app.get("/")
    async def root() -> RedirectResponse:
        return RedirectResponse(url="/ui/", status_code=302)

    @app.get("/health")
    async def health() -> dict:
        return {"status": "ok"}

    @app.get("/health/ready")
    async def health_ready() -> dict:
        gk = (settings.gemini_api_key or "").strip()
        rk = (settings.unkey_root_key or "").strip()
        return {
            "gemini_configured": bool(gk),
            "unkey_server_ready": bool(not settings.unkey_enabled or rk),
            "unkey_enabled": settings.unkey_enabled,
        }

    static_dir = Path(__file__).resolve().parent / "static"
    if static_dir.is_dir():
        app.mount("/ui", StaticFiles(directory=str(static_dir), html=True), name="ui")

    return app


app = create_app()
