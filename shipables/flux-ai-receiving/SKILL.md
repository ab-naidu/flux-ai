---
name: flux-ai-receiving-auditor
description: >
  Build and operate Flux AI — aligned with Multimodal Frontier: agents that see real-world inputs
  (dock photos: invoice + pallet), not text-only prompts. Uses Google Gemini vision for extraction,
  Unkey-gated sync, Railtracks-style traces, bundled /ui demo. Use for warehouse
  receiving, variance detection, HITL approval, or Multimodal Frontier hackathon submissions.
license: MIT
compatibility: Requires network access for Gemini, Unkey verify, and optional webhooks.
metadata:
  author: ab-naidu
  version: "1.0.2"
---

# Flux AI — Multimodal receiving auditor

**Event theme:** Agents that **see / hear / understand the real world**—Flux uses **vision on physical receiving** (camera or photo of paperwork + goods) as the primary signal, then structured reasoning and gated API execution.

## Sponsor tools (minimum 3 for Multimodal Frontier)

1. **Google Gemini** — `POST /api/analyze` or autonomous `POST /api/agent/run` (vision + JSON extraction).
2. **Unkey** — `X-API-Key` on `/api/inventory/sync` and `/api/agent/run` (verify via Unkey API when enabled).
3. **Railtracks** — span IDs + optional `RAILTRACKS_WEBHOOK_URL` JSON events for agent auditability.
4. **DigitalOcean** — deploy `backend/Dockerfile` (Droplet / App Platform).
5. **Custom frontend (optional)** — any SPA calling the same API; set `CORS_ORIGINS` for that origin.

## Autonomy story (judging)

- **Happy path:** `POST /api/agent/run` with image + `X-API-Key` → if all variances are zero, the server **auto-executes** sync without further UI.
- **Exception path:** non-zero variance → response `autonomy: paused_for_hitl` → operator approves (e.g. **Approve & sync** on `/ui`) → `POST /api/inventory/sync`.

## API contract

| Method | Path | Headers | Body |
|--------|------|---------|------|
| POST | `/api/agent/run` | `X-API-Key` | multipart `file`, optional `auto_sync_when_clean=true` |
| POST | `/api/analyze` | — | multipart `file` |
| POST | `/api/inventory/sync` | `X-API-Key` | JSON `{ approved, line_items, notes, trace_id? }` |
| GET | `/health` | — | — |

Responses include `X-Flux-Sponsor-Tools` for demo narration.

## Environment (backend)

See repo `backend/.env.example`: `GEMINI_API_KEY`, `UNKEY_ENABLED`, `CORS_ORIGINS`, `RAILTRACKS_WEBHOOK_URL`, `MOCK_INVENTORY_URL`.

## Publish this skill

From this directory:

```bash
npx @senso-ai/shipables login
shipables publish
```

Bump `metadata.version` in this file and `version` in `shipables.json` before each publish.
