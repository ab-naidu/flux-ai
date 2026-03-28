# Flux AI

**Zero-shot autonomous auditor** for physical-to-digital receiving—the kind of workflow where a wrong number in the system is a wrong number on the shelf.

---

### The problem

**Receiving staff** at a warehouse or DC—dock check-in, receiving clerks, inventory associates—already **see** what arrived: the invoice or packing list, the pallet, the case count. The painful part is **retyping that into the ERP** from memory or notes: slow, error-prone, and hard to reconstruct later for an audit. Flux AI closes that loop: **one photo** (paperwork + freight in the same frame) drives structured extraction, **line-level variance** against what’s visible, and a clear fork—**auto-sync when the math is clean**, **human-in-the-loop + gated API** when it isn’t. The model works from **pixels and layout**, not a chat summary of the dock.

### How it works

Upload → Gemini reads document + scene → variances surface in plain language (`operator_brief`) → either the run **finishes with sync** or the UI requires **explicit approval** before **`/api/inventory/sync`**. Unkey guards inventory mutations; Railtracks structures the agent pipeline. The same flow is available from **`/ui/`** or any client that calls the API.

### Stack

FastAPI in **`backend/`**, operator UI at **`/ui/`**, **Google Gemini** for multimodal JSON extraction, **Unkey** on agent run and sync routes, **Railtracks** Flow + `function_node` in `receiving_flow.py`, mock ERP at **`/mock/vori/receiving`**, **Docker** + compose for deployment (e.g. **DigitalOcean**).

---

## Multimodal Frontier alignment

| Theme | Evidence in this repo |
|--------|------------------------|
| **Idea** | Receiving **reality–data gap**; vision on physical ops, not text-only agents. |
| **Autonomy** | `POST /api/agent/run` — auto sync when variance is zero; else HITL + `/api/inventory/sync`. Status on **`/ui/`**. |
| **Technical** | **`/docs`**, **`/health/ready`** (flags only, no secrets), end-to-end POST to mock ERP. |
| **Tool use** | **`GET /api/about`**; response header **`X-Flux-Sponsor-Tools`**. |
| **Presentation** | **`/ui/`** operator flow — narrated outline in **[`DEMO_SCRIPT.md`](DEMO_SCRIPT.md)** |

## Integrations

| Sponsor | Role |
|---------|------|
| **Google Gemini** | Multimodal extraction (`gemini_service`). |
| **Unkey** | `X-API-Key` on agent run + inventory sync; server **`UNKEY_ROOT_KEY`** for verify v2. |
| **Railtracks** | [RailtownAI/railtracks](https://github.com/RailtownAI/railtracks) Flow + `function_node`; trace payload on `/api/agent/run`. |
| **DigitalOcean** | `backend/Dockerfile`, `docker-compose.yml`. |
| **Lovable / Assistant UI** | Optional; **`/ui/`** ships with the API. |

**Submission & packaging:** [`SUBMISSION_CHECKLIST.md`](SUBMISSION_CHECKLIST.md) · Shipables skill [`shipables/flux-ai-receiving/`](shipables/flux-ai-receiving/) · Optional: [Senso.ai](https://docs.senso.ai)

---

## Quick start

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
# Edit .env — see table below. After git pull, re-run pip install (version pins in requirements.txt).
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

With the server up: http://localhost:8000/docs · http://localhost:8000/ui/ · **`GET /health/ready`** (`gemini_configured`, `unkey_server_ready` — booleans only).

**Credentials you configure:** Google AI Studio key; Unkey root key + client API key when `UNKEY_ENABLED=true`; optional cloud host + env mirroring `.env`.

## Configuration (`backend/.env`)

Copy **`backend/.env.example`** → **`backend/.env`**. **Never commit `.env`** (gitignored). Rotate keys if they leak.

| Variable | Notes |
|----------|--------|
| `GEMINI_API_KEY` | Required for `/api/analyze` and `/api/agent/run`. |
| `GEMINI_MODEL` | Default `gemini-1.5-pro`. |
| `CORS_ORIGINS` | Comma-separated origins if the UI is not same-host. |
| `UNKEY_ENABLED` | `false` = skip verification locally. |
| `UNKEY_VERIFY_URL` | Default `https://api.unkey.com/v2/keys.verifyKey` (avoid `api.unkey.dev` if DNS fails). |
| `UNKEY_ROOT_KEY` | Server-only; clients send **`X-API-Key`**. |
| `RAILTRACKS_*`, `MOCK_INVENTORY_URL` | Optional — see `.env.example`. |

## API (summary)

| Method | Path | Purpose |
|--------|------|---------|
| GET | `/` | Redirect → **`/ui/`** |
| GET | `/health`, `/health/ready` | Liveness + config flags |
| GET | `/api/about` | Metadata JSON (sponsors, integration summary) |
| POST | `/api/agent/run` | Multipart image, `operator_brief`, Unkey when enabled |
| POST | `/api/analyze` | Analysis-only path |
| POST | `/api/inventory/sync` | HITL-approved sync + `X-API-Key` |
| POST | `/mock/vori/receiving` | Stand-in ERP webhook |

**Custom front end:** set `CORS_ORIGINS`; same routes and `X-API-Key` contract as above.

## Docker

```powershell
docker build -t flux-ai-api -f backend/Dockerfile backend
docker run -p 8000:8000 --env-file backend/.env flux-ai-api
```

From repo root: `docker compose up --build` (expects `backend/.env`). Then open **`https://YOUR_HOST/ui/`**.

## Shipables

```bash
cd shipables/flux-ai-receiving
npx @senso-ai/shipables login
shipables publish
```

Use `shipables publish --dry-run` to validate the package before publishing.
