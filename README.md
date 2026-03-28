# Flux AI

**Tagline:** Zero-shot autonomous auditor for physical-to-digital receiving workflows.

### Multimodal Frontier — theme alignment

The hackathon centers on agents that **see, hear, and understand the real world**—not agents that only consume text prompts. **Flux AI** fits that brief directly: the agent’s primary input is **real camera / photo evidence** from the loading dock (invoice + pallet in frame). It **reasons over pixels and document layout**, extracts structured facts, compares “what the paperwork claims” to “what’s visible,” and only then acts through gated APIs. This is **visual understanding of physical operations**, not a chat wrapper around a spreadsheet.

### For judges (20% × 5 at a glance)

| Bucket | Where to look |
|--------|----------------|
| **Idea** | *Multimodal Frontier* theme: real-world **vision** input + receiving use case — see section *Multimodal Frontier* + *The problem* below |
| **Autonomy** | `POST /api/agent/run` — auto sync when variance is zero; else HITL + `/api/inventory/sync`. **UI:** colored banner on **`/ui/`** states the mode. |
| **Technical** | **`/docs`** OpenAPI; **`/health/ready`** shows config flags (no secrets); end-to-end POST to mock ERP |
| **Tool use** | **`GET /api/about`** lists sponsors + evidence; response header **`X-Flux-Sponsor-Tools`** |
| **Presentation** | Record **`/ui/`** walkthrough — script: **[`DEMO_SCRIPT.md`](DEMO_SCRIPT.md)** |

Quick links (when API is running): **`/`** → demo UI · **`/api/about`** · **`/docs`**

---

## The problem

Warehouse and retail receiving still depend on a slow, error-prone loop: a person reads a paper invoice or packing list, eyeballs what is on the pallet, and manually types quantities into an ERP or inventory system. That creates a **reality–data gap**—what physically arrived does not reliably match what the system believes—plus delays, silos, and weak audit trails. Fixing that requires **understanding the scene**, not retyping a text summary of it.

## What Flux AI does

Flux AI is a **multimodal cognitive bridge** between the dock and your digital inventory—the agent **looks** at the same visual evidence a receiver would:

1. **Perception (real-world input)** — An operator uploads a photo (or your app sends **live or captured camera** feed) showing the delivery and its paperwork in frame—not a text description of the delivery.
2. **Reasoning** — A vision-language model reads expected quantities from document text and estimates what is visible on the pallet, then computes **line-level variances** (e.g. invoice says 50 cases, scene suggests 48).
3. **Human-in-the-loop when it matters** — If everything matches, the system can **finish the workflow automatically**. If there is a discrepancy, it **stops** and waits for an explicit approval path (e.g. chat: “approve and sync”).
4. **Gated execution** — Inventory mutations go through **API key verification** (Unkey) so automated runs cannot silently write to downstream systems without authorized credentials.
5. **Auditability** — Each run carries **trace IDs** (and optional webhook spans) so you can show *what* was inferred and *when* sync was attempted—aligned with enterprise receiving audits.

In short: **one image in → structured variance out → safe sync when policy allows.**

## Who it is for

- **3PL / DC receiving** teams tired of double data entry  
- **Grocery / retail** flows where pallet + invoice photos are already common  
- **Hackathon / pilot** demos that must show **autonomy**, **multimodal AI**, and **real API execution** without hand-waving

## System shape (this repo)

| Layer | Role |
|-------|------|
| **This backend (FastAPI)** | Image ingest, Gemini multimodal JSON extraction, variance logic, Unkey-gated sync, mock ERP webhook, trace emission. |
| **Frontend** | Operator UI is served at **`/ui`** from this service. A separate client (e.g. React + Assistant UI) can call the same REST API; set **`CORS_ORIGINS`** for non–same-origin hosts. |
| **Infrastructure** | Container in `backend/Dockerfile`; intended to run on **DigitalOcean** (or any host) with secrets in env—never in git. |

## Hackathon sponsor tools (how they show up)

| Sponsor | Role in Flux AI |
|---------|------------------|
| **Google Gemini** | Vision + structured extraction from invoice + pallet imagery. |
| **Unkey** | Validates `X-API-Key` before agent run and inventory sync. |
| **Railtracks** | [RailtownAI/railtracks](https://github.com/RailtownAI/railtracks) **Flow** + `function_node` tools (`receiving_flow.py`); `railtracks` object on `/api/agent/run`; plus `trace_id` / optional `RAILTRACKS_WEBHOOK_URL`. |
| **DigitalOcean** | Production hosting for the API container. |
| **Lovable** | Optional external UI scaffold (not required for the bundled demo). |
| **Assistant UI** | Optional embedded chat UX on a separate frontend. |

Response header **`X-Flux-Sponsor-Tools`** summarizes integrations for demos.

**Extra prize track (optional):** [Senso.ai](https://docs.senso.ai) — only if you have time to ground copy or policies in a Senso KB; not required for the core demo.

**Submission:** see [`SUBMISSION_CHECKLIST.md`](SUBMISSION_CHECKLIST.md) (Devpost + Shipables + 3-minute video).

### What you do vs what’s already in this repo

| You (account / actions) | Already in repo (I/we shipped) |
|---------------------------|-------------------------------|
| Google AI Studio API key | Gemini integration + `.env.example` |
| Unkey root key + client API key | Verify v2 + gated routes |
| Run server, open URLs | FastAPI, `/docs`, **`/ui` demo** |
| Optional custom frontend | Same API as `/ui`; configure `CORS_ORIGINS` |
| DigitalOcean account, create Droplet/App, set env | `Dockerfile`, `docker-compose.yml` |
| `shipables login` + `publish` | Skill under `shipables/flux-ai-receiving/` |
| Record video, submit Devpost | `SUBMISSION_CHECKLIST.md` |

---

## Rubric alignment (Multimodal Frontier)

| Criterion | What judges can see |
|-----------|---------------------|
| **Idea** | Receiving reality–data gap + multimodal audit story (above). |
| **Autonomy** | `POST /api/agent/run` — auto sync when variances are zero; otherwise paused for HITL + `/api/inventory/sync`. |
| **Technical** | End-to-end API, JSON contracts, gated POST to mock ERP. |
| **Tool use** | Gemini, Unkey, traces, DO deploy path; optional second frontend if you add one. |
| **Shipables** | Skill package in [`shipables/flux-ai-receiving/`](shipables/flux-ai-receiving/). |

---

## Unkey (server setup)

- Browsers and clients send **`X-API-Key`** = the **API key you issue** for the app/user.  
- The server must set **`UNKEY_ROOT_KEY`** in `backend/.env` (Unkey **root key**) to call Unkey’s verify API.  
- Use **`UNKEY_VERIFY_URL=https://api.unkey.com/v2/keys.verifyKey`** (avoid `api.unkey.dev` if DNS fails).

---

## Quick start (local)

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
# Edit .env: GEMINI_API_KEY=... ; UNKEY_ROOT_KEY=... when UNKEY_ENABLED=true
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Open **http://localhost:8000/docs** for interactive API docs.

After editing `.env`, call **`GET /health/ready`** — it reports `gemini_configured` and `unkey_server_ready` (boolean flags only, no secret values).

### Environment variables (`backend/.env`)

Copy **`backend/.env.example`** → **`backend/.env`** and fill values. **Never commit `.env`** (it is listed in `.gitignore`).

| Variable | Purpose |
|----------|---------|
| `GEMINI_API_KEY` | Required for `/api/analyze` and `/api/agent/run` (Google AI Studio). |
| `GEMINI_MODEL` | Optional; defaults to `gemini-1.5-pro`. |
| `CORS_ORIGINS` | Comma-separated browser origins if the UI or another front end is not same-origin. |
| `UNKEY_ENABLED` | Set `false` to skip key verification locally; `true` for production-style gating. |
| `UNKEY_VERIFY_URL` | Default `https://api.unkey.com/v2/keys.verifyKey` (prefer over `api.unkey.dev` if DNS fails). |
| `UNKEY_ROOT_KEY` | Unkey **root** key (server only). Required when `UNKEY_ENABLED=true`. Clients still send **`X-API-Key`** (an API key you create in Unkey). |
| `RAILTRACKS_ENABLED` | Feature flag for Railtracks integration paths in config. |
| `RAILTRACKS_WEBHOOK_URL` | Optional JSON trace webhook. |
| `MOCK_INVENTORY_URL` | Empty = in-process mock ERP; or set to your deployed `/mock/vori/receiving` URL. |

### Python dependencies (important after `git pull`)

- **`starlette`** is pinned to the **0.41.x** line (below 0.42) so FastAPI **0.115.x** is not broken by transitive **mcp** pulling Starlette **1.x**.
- **`pydantic`** is **2.12.x** (not 2.10.x) so **`railtracks`** imports cleanly.

Always reinstall after pulling: `pip install -r backend/requirements.txt`.

### Bundled demo UI

1. Start the API (see above).  
2. Open **http://localhost:8000/ui/** (or **`/`**, which redirects there).  
3. The UI is **step-based** for recordings: secure session → capture photo → full audit, with a **loading narrative** while Gemini runs, plain-language **outcomes** from `operator_brief`, and **technical JSON** tucked under “Technical details”.  
4. If variances block autonomy, use **Confirm inventory update**. Same origin as the API — no CORS setup.

### API summary

| Endpoint | Purpose |
|----------|---------|
| `GET /` | Redirects to **`/ui/`** (demo first) |
| `GET /health` | Liveness |
| `GET /health/ready` | `gemini_configured` / `unkey_server_ready` flags (no secret values) |
| `GET /api/about` | Judge-facing sponsor + rubric hooks (JSON) |
| `POST /api/agent/run` | **Full agent path** — multipart `file`, form `auto_sync_when_clean`, header `X-API-Key` when Unkey enabled; includes **`operator_brief`** (human copy + step states) for UIs |
| `POST /api/analyze` | Multimodal analysis only; includes **`operator_brief`** |
| `POST /api/inventory/sync` | HITL-approved sync — JSON body + `X-API-Key` |
| `POST /mock/vori/receiving` | Stand-in grocery/ERP webhook |

### Custom frontend (same API)

1. Add your site’s origin(s) to **`CORS_ORIGINS`** in server `.env`.  
2. **Upload** → `POST /api/agent/run` or `/api/analyze`.  
3. **Approve / sync** → `POST /api/inventory/sync` with the same `X-API-Key` and `line_items` from the last analysis response.

---

## Secrets and Git

- **Never commit** `backend/.env`. It is gitignored; use **`.env.example`** as the template only.
- If keys are exposed (e.g. pasted in a ticket, screenshot, or accidental commit), **rotate** them in [Google AI Studio](https://aistudio.google.com/) and the [Unkey dashboard](https://unkey.dev/) immediately.

---

## DigitalOcean

```powershell
docker build -t flux-ai-api -f backend/Dockerfile backend
docker run -p 8000:8000 --env-file backend/.env flux-ai-api
```

Or from repo root (requires `backend/.env` present):

```powershell
docker compose up --build
```

Set the same secrets on the host as in local `.env` (never commit `.env`). After deploy, open **`https://YOUR_HOST/ui/`** for the same demo UI.

---

## Publish Shipables skill

```bash
cd shipables/flux-ai-receiving
npx @senso-ai/shipables login
shipables publish
```

Use `shipables publish --dry-run` to validate packaging first.
