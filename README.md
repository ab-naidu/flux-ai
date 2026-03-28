# Flux AI

**Zero-shot autonomous auditor** for physical-to-digital receiving—the kind of workflow where a wrong number in the system is a wrong number on the shelf.

---

### Why anyone should care

Receivers already **see** the truth: the invoice, the pallet, the case count. The painful part is **translating sight into ERP rows**—slow, error-prone, and almost never replayable for an audit. Flux AI flips that: **one photo** (invoice + freight in frame) drives structured extraction, **line-level variance** against what’s visible, and a clear fork—**auto-sync when the math is clean**, **human-in-the-loop + gated API** when it isn’t. No “describe the pallet in chat”; the model works from **pixels and layout**, the way the dock actually works.

### What you’ll see in a demo

Upload → Gemini reads document + scene → variances surface in plain language (`operator_brief`) → either the run **finishes with sync** or the UI asks for **explicit approve** before **`/api/inventory/sync`**. Unkey guards the mutations; Railtracks structures the agent pipeline; you can ship the same story from **`/ui/`** or your own client.

### Under the hood

FastAPI in **`backend/`**, bundled operator UI at **`/ui/`**, **Google Gemini** for multimodal JSON extraction, **Unkey** on agent run and sync routes, **Railtracks** Flow + `function_node` in `receiving_flow.py`, mock ERP at **`/mock/vori/receiving`**, **Docker** + compose for deployment (e.g. **DigitalOcean**).

---

## For judges (rubric map)

| Bucket | Where to look |
|--------|----------------|
| **Idea** | Multimodal receiving + **reality–data gap** (above)—vision on physical ops, not text-only agents. |
| **Autonomy** | `POST /api/agent/run` — auto sync when variance is zero; else HITL + `/api/inventory/sync`. Status banner on **`/ui/`**. |
| **Technical** | **`/docs`**, **`/health/ready`** (flags only, no secrets), end-to-end POST to mock ERP. |
| **Tool use** | **`GET /api/about`**; response header **`X-Flux-Sponsor-Tools`**. |
| **Presentation** | **`/ui/`** walkthrough — **[`DEMO_SCRIPT.md`](DEMO_SCRIPT.md)** |

**When the API is running:** **`/`** → **`/ui/`** · **`/api/about`** · **`/docs`**

## Sponsor tools (where they land)

| Sponsor | In this repo |
|---------|----------------|
| **Google Gemini** | Multimodal extraction (`gemini_service`). |
| **Unkey** | `X-API-Key` on agent run + inventory sync; server **`UNKEY_ROOT_KEY`** for verify v2. |
| **Railtracks** | [RailtownAI/railtracks](https://github.com/RailtownAI/railtracks) Flow + `function_node`; trace payload on `/api/agent/run`. |
| **DigitalOcean** | `backend/Dockerfile`, `docker-compose.yml`. |
| **Lovable / Assistant UI** | Optional; bundled **`/ui/`** is enough for a full demo. |

**Hackathon submission:** [`SUBMISSION_CHECKLIST.md`](SUBMISSION_CHECKLIST.md) · **Shipables skill:** [`shipables/flux-ai-receiving/`](shipables/flux-ai-receiving/) · Optional track: [Senso.ai](https://docs.senso.ai)

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

- **Interactive API:** http://localhost:8000/docs  
- **Operator demo:** http://localhost:8000/ui/  
- **Config smoke test:** `GET /health/ready` → `gemini_configured`, `unkey_server_ready` (booleans only)

**Bring your own:** Google AI Studio key; Unkey root key + a client API key when `UNKEY_ENABLED=true`; optional DO app + env vars mirroring `.env`.

## Configuration (`backend/.env`)

Copy **`backend/.env.example`** → **`backend/.env`**. **Never commit `.env`** (gitignored). Rotate keys if they leak.

| Variable | Notes |
|----------|--------|
| `GEMINI_API_KEY` | Required for `/api/analyze` and `/api/agent/run`. |
| `GEMINI_MODEL` | Default `gemini-1.5-pro`. |
| `CORS_ORIGINS` | Comma-separated origins if the UI is not same-host. |
| `UNKEY_ENABLED` | `false` = skip verification for local hacking. |
| `UNKEY_VERIFY_URL` | Default `https://api.unkey.com/v2/keys.verifyKey` (avoid `api.unkey.dev` if DNS fails). |
| `UNKEY_ROOT_KEY` | Server-only; browsers/clients send **`X-API-Key`**. |
| `RAILTRACKS_*`, `MOCK_INVENTORY_URL` | Optional — see `.env.example`. |

## API (summary)

| Method | Path | Purpose |
|--------|------|---------|
| GET | `/` | Redirect → **`/ui/`** |
| GET | `/health`, `/health/ready` | Liveness + config flags |
| GET | `/api/about` | Sponsors / rubric JSON |
| POST | `/api/agent/run` | Multipart image, `operator_brief`, Unkey when enabled |
| POST | `/api/analyze` | Analysis-only path |
| POST | `/api/inventory/sync` | HITL-approved sync + `X-API-Key` |
| POST | `/mock/vori/receiving` | Stand-in ERP webhook |

**Custom front end:** add origins to `CORS_ORIGINS`; same routes and `X-API-Key` contract as above.

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
