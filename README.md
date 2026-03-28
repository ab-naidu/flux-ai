# Flux AI

**Tagline:** Zero-shot autonomous auditor for physical-to-digital receiving workflows.

> **Note:** On github.com, everything above the README (nav, Copilot banners, file browser) is **GitHub’s UI**, not this file. To copy docs, use **Raw** or clone the repo.

## What it is

**Multimodal Frontier fit:** the agent’s main input is **real dock photos** (invoice + pallet)—not a text-only prompt. It reads layout and pixels, extracts structured quantities, compares paperwork to what’s visible, computes **line-level variance**, then either **auto-syncs** (when clean) or **stops for HITL** and gated **`/api/inventory/sync`**.

**Stack:** FastAPI backend (`backend/`) with bundled operator UI at **`/ui/`**, Gemini vision, Unkey on mutate routes, Railtracks Flow in `receiving_flow.py`, mock ERP webhook, Docker for deploy (e.g. DigitalOcean).

## For judges (rubric map)

| Bucket | Where to look |
|--------|----------------|
| **Idea** | Multimodal receiving + reality–data gap (above). |
| **Autonomy** | `POST /api/agent/run` — auto sync when variance is zero; else HITL + `/api/inventory/sync`. Banner on **`/ui/`**. |
| **Technical** | **`/docs`**, **`/health/ready`** (flags only), end-to-end mock ERP. |
| **Tool use** | **`GET /api/about`**; header **`X-Flux-Sponsor-Tools`**. |
| **Presentation** | **`/ui/`** walkthrough — **[`DEMO_SCRIPT.md`](DEMO_SCRIPT.md)** |

Live when running: **`/`** → **`/ui/`** · **`/api/about`** · **`/docs`**

## Sponsor tools

| Sponsor | In this repo |
|---------|----------------|
| **Google Gemini** | Multimodal extraction (`gemini_service`). |
| **Unkey** | `X-API-Key` on agent run + inventory sync; server uses **`UNKEY_ROOT_KEY`** for verify v2. |
| **Railtracks** | [railtracks](https://github.com/RailtownAI/railtracks) Flow + `function_node`; JSON on `/api/agent/run`. |
| **DigitalOcean** | `backend/Dockerfile`, `docker-compose.yml`. |
| **Lovable / Assistant UI** | Optional; bundled **`/ui/`** is enough for demo. |

**Submission:** [`SUBMISSION_CHECKLIST.md`](SUBMISSION_CHECKLIST.md) · **Shipables:** [`shipables/flux-ai-receiving/`](shipables/flux-ai-receiving/) · Optional: [Senso.ai](https://docs.senso.ai)

## Quick start

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
# Edit .env — see table below. After pull, always re-run pip install (pins in requirements.txt).
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

- **Docs:** http://localhost:8000/docs  
- **Demo UI:** http://localhost:8000/ui/  
- **Sanity check:** `GET /health/ready` → `gemini_configured`, `unkey_server_ready` (booleans only)

**You supply:** Google AI Studio key; Unkey root + an API key for clients when `UNKEY_ENABLED=true`; optional DO host + env mirroring `.env`.

## Configuration (`backend/.env`)

Copy **`backend/.env.example`** → **`backend/.env`**. **Do not commit `.env`** (gitignored). Rotate keys if leaked.

| Variable | Notes |
|----------|--------|
| `GEMINI_API_KEY` | Required for analyze / agent. |
| `GEMINI_MODEL` | Default `gemini-1.5-pro`. |
| `CORS_ORIGINS` | Comma-separated if front end is not same-origin. |
| `UNKEY_ENABLED` | `false` = skip verify locally. |
| `UNKEY_VERIFY_URL` | Default `https://api.unkey.com/v2/keys.verifyKey` (avoid `api.unkey.dev` if DNS fails). |
| `UNKEY_ROOT_KEY` | Server-only; clients use **`X-API-Key`**. |
| `RAILTRACKS_*`, `MOCK_INVENTORY_URL` | Optional; see `.env.example`. |

## API (summary)

| Method | Path | Purpose |
|--------|------|---------|
| GET | `/` | → `/ui/` |
| GET | `/health`, `/health/ready` | Liveness + config flags |
| GET | `/api/about` | Sponsors / rubric JSON |
| POST | `/api/agent/run` | Multipart image; `operator_brief`; Unkey if enabled |
| POST | `/api/analyze` | Analysis only |
| POST | `/api/inventory/sync` | HITL sync + `X-API-Key` |
| POST | `/mock/vori/receiving` | Mock ERP |

**Custom front end:** set `CORS_ORIGINS`; same endpoints and `X-API-Key` as above.

## Docker

```powershell
docker build -t flux-ai-api -f backend/Dockerfile backend
docker run -p 8000:8000 --env-file backend/.env flux-ai-api
```

From repo root: `docker compose up --build` (needs `backend/.env`). Then open **`https://YOUR_HOST/ui/`**.

## Shipables

```bash
cd shipables/flux-ai-receiving
npx @senso-ai/shipables login
shipables publish
```

`shipables publish --dry-run` validates the package.
