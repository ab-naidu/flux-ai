# Flux AI

**Tagline:** Zero-shot autonomous auditor for physical-to-digital receiving workflows.

---

## The problem

Warehouse and retail receiving still depend on a slow, error-prone loop: a person reads a paper invoice or packing list, eyeballs what is on the pallet, and manually types quantities into an ERP or inventory system. That creates a **reality–data gap**—what physically arrived does not reliably match what the system believes—plus delays, silos, and weak audit trails.

## What Flux AI does

Flux AI is a **multimodal cognitive bridge** between the dock and your digital inventory:

1. **Perception** — An operator uploads a photo (or your app sends camera capture) showing the delivery and its paperwork in frame.
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
| **Frontend (Lovable + Assistant UI)** | Enterprise-style dashboard, upload, discrepancy table, conversational approval. *Wire your Lovable app to the API URLs below.* |
| **Infrastructure** | Container in `backend/Dockerfile`; intended to run on **DigitalOcean** (or any host) with secrets in env—never in git. |

## Hackathon sponsor tools (how they show up)

| Sponsor | Role in Flux AI |
|---------|------------------|
| **Google Gemini** | Vision + structured extraction from invoice + pallet imagery. |
| **Unkey** | Validates `X-API-Key` before agent run and inventory sync. |
| **Railtracks-style traces** | `trace_id` on responses; optional `RAILTRACKS_WEBHOOK_URL` for span JSON. |
| **DigitalOcean** | Production hosting for the API container. |
| **Lovable** | UI shell for the operator experience. |
| **Assistant UI** | Chat UX for natural-language approve / sync intents. |

Response header **`X-Flux-Sponsor-Tools`** summarizes integrations for demos.

**Submission:** see [`SUBMISSION_CHECKLIST.md`](SUBMISSION_CHECKLIST.md) (Devpost + Shipables + 3-minute video).

### What you do vs what’s already in this repo

| You (account / actions) | Already in repo (I/we shipped) |
|---------------------------|-------------------------------|
| Google AI Studio API key | Gemini integration + `.env.example` |
| Unkey root key + client API key | Verify v2 + gated routes |
| Run server, open URLs | FastAPI, `/docs`, **`/ui` demo** |
| Lovable + Assistant UI (optional for extra sponsor points) | API contract in README |
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
| **Tool use** | Gemini, Unkey, traces, DO deploy path, Lovable + Assistant UI (frontend). |
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

### Bundled demo UI (record a video without Lovable)

1. Start the API (see above).  
2. Open **http://localhost:8000/ui/** in your browser.  
3. Paste **X-API-Key**, choose an image, **Run agent**. If variances block autonomy, click **Approve & sync**.  
   Same origin as the API, so no CORS configuration for this page.

### API summary

| Endpoint | Purpose |
|----------|---------|
| `GET /health` | Liveness |
| `POST /api/agent/run` | **Full agent path** — multipart `file`, form `auto_sync_when_clean`, header `X-API-Key` when Unkey enabled |
| `POST /api/analyze` | Multimodal analysis only (no auto sync) |
| `POST /api/inventory/sync` | HITL-approved sync — JSON body + `X-API-Key` |
| `POST /mock/vori/receiving` | Stand-in grocery/ERP webhook |

### Lovable + Assistant UI

1. Set **`CORS_ORIGINS`** to your Lovable preview/production URL in server `.env`.  
2. **Upload** → `POST /api/agent/run` or `/api/analyze`.  
3. **Chat** → on approve intent, `POST /api/inventory/sync` with the same `X-API-Key` and `line_items` from the last response.

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
