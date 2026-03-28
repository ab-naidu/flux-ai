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
            "tool_use": (
                "Gemini + Unkey + Railtracks Flow (github.com/RailtownAI/railtracks) "
                "+ trace IDs / webhook + DO + bundled /ui"
            ),
            "presentation": (
                "GET / or /ui/ — guided operator UI with loading narrative, outcome copy (operator_brief), "
                "and collapsible JSON; DEMO_SCRIPT.md for video"
            ),
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
                "sponsor": "Railtracks (agentic framework)",
                "evidence": (
                    "Receiving pipeline is a Railtracks Flow with function_node tools "
                    "(rt_step_multimodal_extract, rt_step_post_inventory); response.railtracks meta"
                ),
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
