# Flux AI

**Zero-shot autonomous auditor** for physical-to-digital receiving.

**Warehouse receiving** is the instant global inventory becomes data: staff face **real pallets, cases, and paperwork** (invoice or packing list), but the **ERP / WMS** usually only sees **what someone types later**—rushed, error-prone, and a weak basis for audits or disputes across partners.

**Flux AI** shortens that path: you take **one photo** with **both the paperwork and the freight in frame**. A vision model extracts structured quantities and line items, compares **what the paper says** to **what the image suggests is on the load**, and then either **posts a clean receipt automatically** or **stops for human approval** before calling a **key-protected** inventory API.

---

### What you get

- **Vision-first intake** — One image with **invoice + freight in frame**; no dependency on someone summarizing the scene in text.
- **Line-level variance** — Expected quantities from the paperwork vs. what the model infers from the **physical load**, surfaced clearly for operators.
- **Policy-aware execution** — **Auto-post** when numbers reconcile; **stop and require approval** when they don’t—then a **key-gated** sync so automation cannot silently corrupt the ledger.
- **Operator-readable output** — `operator_brief` and the bundled **`/ui/`** turn JSON into language a receiving lead can act on, with full technical detail available when needed.

### The problem (why this matters at global scale)

Global supply chains move **billions of tons** of goods through **millions** of dock doors every year. Planning systems, carriers, and finance all assume the **digital record** matches **what physically crossed the threshold**. Often it does not. The gap shows up as **inventory distortion** (phantom stock, overstated availability), **disputes with suppliers and 3PLs**, **slower fulfillment**, **recall and compliance risk** when lineage is fuzzy, and **labor** stuck on low-value data entry instead of exception handling. Fixing “the spreadsheet” upstream never helps if **the moment of truth—the receiving line—still depends on brittle manual transcription**.

**Receiving is where the physical world enters the ledger.** Yet most organizations still bridge that boundary with **human rekeying** from paper or PDFs into ERP/WMS rows: high latency, error-prone, and a weak audit trail when operations, finance, or regulators ask what was actually accepted.

Flux AI attacks that **systemic reality–data gap** with **multimodal perception**: a single photo with **document + freight in frame** feeds structured extraction and **line-level variance** (paper vs. scene). Automation can **post clean receipts**; discrepancies **surface to humans** before **key-gated** APIs change inventory—so scale does not have to mean silent, un-auditable writes.

### How it works (end-to-end)

1. **Capture** — Upload a photo (or integrate your app’s camera) showing **document + goods** together.  
2. **Understand** — **Gemini** performs multimodal extraction: structured line items, quantities, and scene-grounded estimates.  
3. **Decide** — The service compares **paper vs. scene**, exposes variances, and populates **`operator_brief`** for humans scanning the outcome.  
4. **Act** — If policy allows and the run is clean, **`/api/agent/run`** can complete inventory sync automatically. If not, the **bundled UI** or your client collects **explicit approval**, then **`/api/inventory/sync`** runs behind **Unkey**-verified **`X-API-Key`**.  
5. **Trace** — **Railtracks** Flow + `function_node` in `receiving_flow.py` structures the pipeline; optional webhook and response payloads support audit-style follow-up.

The same contract is available from **`/ui/`** or any HTTP client—no lock-in to a single front end.

### Stack

| Piece | Role |
|-------|------|
| **FastAPI** | `backend/` — REST API, static **`/ui/`**, health and metadata routes. |
| **Google Gemini** | Multimodal JSON extraction from dock imagery. |
| **Unkey** | Verifies client keys before agent run and inventory sync. |
| **Railtracks** | Agent orchestration (`Flow`, `function_node`). |
| **Mock ERP** | **`/mock/vori/receiving`** for end-to-end demos without a real WMS. |
| **Docker / compose** | Ship to **DigitalOcean** or any container host with env-based secrets. |

---

## Multimodal Frontier alignment

| Theme | Evidence in this repo |
|--------|------------------------|
| **Idea** | Systemic **reality–data gap** (inventory, disputes, compliance); vision on physical receiving, not text-only agents. |
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
