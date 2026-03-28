"""
Judge- and demo-facing metadata (no secrets). Helps Tool Use + Presentation scoring.
"""

from fastapi import APIRouter

router = APIRouter(tags=["meta"])


@router.get("/api/about")
async def about() -> dict:
    return {
        "project": "Flux AI",
        "tagline": "Zero-shot autonomous auditor for physical-to-digital receiving workflows",
        "multimodal_frontier_theme": (
            "Hackathon focus: agents that see / hear / understand the real world—not only text prompts. "
            "Flux AI: primary signal is camera or photo of dock + paperwork; vision-language reasoning; "
            "then gated actions. Visual ops, not chat-only."
        ),
        "judging_hooks": {
            "autonomy": (
                "POST /api/agent/run — one upload; if all variances are zero, inventory sync runs "
                "automatically; otherwise autonomy pauses for HITL then POST /api/inventory/sync"
            ),
            "idea": (
                "Aligns with Multimodal Frontier: real-world visual input (invoice + pallet imagery), "
                "not text-only agents; closes receiving reality–data gap with vision + gated ERP write"
            ),
            "technical": "FastAPI end-to-end, structured JSON from Gemini, Unkey-gated mutations, mock ERP webhook",
            "tool_use": "Gemini + Unkey + trace IDs (Railtracks-style webhook optional) + DO container + bundled /ui",
            "presentation": "Open GET / or /ui/ for operator demo; GET /docs for Swagger; 3-minute video script in repo DEMO_SCRIPT.md",
        },
        "sponsor_integration": [
            {
                "sponsor": "Google Gemini",
                "evidence": "POST /api/analyze and /api/agent/run — multimodal extraction from image",
            },
            {
                "sponsor": "Unkey",
                "evidence": "X-API-Key on /api/agent/run and /api/inventory/sync; server UNKEY_ROOT_KEY for verify API",
            },
            {
                "sponsor": "Railtracks (agent traces)",
                "evidence": "trace_id on responses; optional RAILTRACKS_WEBHOOK_URL JSON spans",
            },
            {
                "sponsor": "DigitalOcean",
                "evidence": "backend/Dockerfile + docker-compose.yml for production deploy",
            },
            {
                "sponsor": "Operator UI",
                "evidence": "Bundled /ui on same origin; HITL approve path without extra CORS setup",
            },
        ],
        "links": {
            "demo_ui": "/ui/",
            "openapi": "/docs",
            "health": "/health",
            "readiness": "/health/ready",
        },
    }
