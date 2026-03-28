---
name: flux-ai-receiving-auditor
description: >
  Build and operate Flux AI — a multimodal receiving auditor that compares invoice/pallet
  images (Google Gemini), gates inventory sync with Unkey, emits Railtracks-style trace spans,
  and pairs with a Lovable + Assistant UI dashboard. Use when implementing warehouse receiving,
  variance detection, HITL approval chat, or hackathon Multimodal Frontier submissions.
license: MIT
compatibility: Requires network access for Gemini, Unkey verify, and optional webhooks.
metadata:
  author: ab-naidu
  version: "1.0.0"
---

# Flux AI — Multimodal receiving auditor

## Sponsor tools (minimum 3 for Multimodal Frontier)

1. **Google Gemini** — `POST /api/analyze` or autonomous `POST /api/agent/run` (vision + JSON extraction).
2. **Unkey** — `X-API-Key` on `/api/inventory/sync` and `/api/agent/run` (verify via Unkey API when enabled).
3. **Railtracks** — span IDs + optional `RAILTRACKS_WEBHOOK_URL` JSON events for agent auditability.
4. **DigitalOcean** — deploy `backend/Dockerfile` (Droplet / App Platform).
5. **Lovable** — host the React/Next dashboard; set `CORS_ORIGINS` to the preview URL.
6. **Assistant UI** — embed chat; map “approve and sync” to `POST /api/inventory/sync`.

## Autonomy story (judging)

- **Happy path:** `POST /api/agent/run` with image + `X-API-Key` → if all variances are zero, the server **auto-executes** sync without further UI.
- **Exception path:** non-zero variance → response `autonomy: paused_for_hitl` → operator approves in chat → `POST /api/inventory/sync`.

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
