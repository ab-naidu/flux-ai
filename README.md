# Flux AI — Multimodal Frontier build

**Repository:** [github.com/ab-naidu/flux-ai](https://github.com/ab-naidu/flux-ai)

Backend: **FastAPI** + **Google Gemini** (vision JSON) + **Unkey**-gated mutations + **Railtracks-style** trace IDs / optional webhook + **DigitalOcean**-ready container. Pair with **Lovable** + **Assistant UI** on the frontend.

**Before you submit:** follow [`SUBMISSION_CHECKLIST.md`](SUBMISSION_CHECKLIST.md) (Devpost rules + 20% × 5 rubric).

## Winning rubric alignment

| Criterion | What we implemented |
|-----------|---------------------|
| **Autonomy** | `POST /api/agent/run` — one image upload; auto inventory sync when variances are zero; otherwise pauses for HITL + `/api/inventory/sync`. |
| **Tool use** | Response header `X-Flux-Sponsor-Tools` lists integrations; Unkey on agent + sync; Gemini in `gemini_service.py`; Railtracks hooks in `railtracks.py`. |
| **Shipables** | Publish [`shipables/flux-ai-receiving/`](shipables/flux-ai-receiving/) (`author: ab-naidu` in `SKILL.md` / `shipables.json`). |

## Quick start (local)

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
# Set GEMINI_API_KEY=... ; use UNKEY_ENABLED=false for local dry runs
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Endpoints

| Endpoint | Purpose |
|----------|---------|
| `GET /health` | Liveness |
| `POST /api/agent/run` | **Autonomous pipeline** — multipart `file`, form `auto_sync_when_clean` (default true), header `X-API-Key` |
| `POST /api/analyze` | Multimodal only (no auto sync) |
| `POST /api/inventory/sync` | HITL-approved sync — JSON body, `X-API-Key` |
| `POST /mock/vori/receiving` | ERP-style mock target |

## Lovable + Assistant UI

1. Set `CORS_ORIGINS` to your Lovable preview URL in production `.env`.
2. **Upload** → call `/api/agent/run` or `/api/analyze`.
3. **Chat** → on “approve and sync”, `POST /api/inventory/sync` with the same `X-API-Key` and the `line_items` from the last analyze response.

## DigitalOcean

Build/run: `docker build -t flux-ai ./backend` then `docker run -p 8000:8000 --env-file backend/.env flux-ai`

## Publish Shipables skill

```bash
cd shipables/flux-ai-receiving
npx @senso-ai/shipables login
shipables publish
```

Use `shipables publish --dry-run` first if you want to validate packaging.
