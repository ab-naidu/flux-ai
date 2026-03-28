import logging
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

from app.config import settings
from app.routers import agent, analyze, inventory, mock_target

logging.basicConfig(level=logging.INFO)

SPONSOR_TOOL_HEADER = (
    "google-gemini; unkey; railtracks-traces; digitalocean-ready; "
    "lovable-frontend; assistant-ui-chat"
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
    app.include_router(agent.router)
    app.include_router(analyze.router)
    app.include_router(inventory.router)
    app.include_router(mock_target.router)

    @app.get("/health")
    async def health() -> dict:
        return {"status": "ok"}

    return app


app = create_app()
