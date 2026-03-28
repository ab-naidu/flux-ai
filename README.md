# Flux AI

**Zero-shot autonomous auditor** for physical-to-digital receiving.

**Warehouse receiving** is where global inventory becomes data: staff see **pallets, paperwork, and labels** on the floor, but the **ERP / WMS** often only gets **what someone types later**—slow, error-prone, weak for audits and partner disputes.

**Flux AI** uses **one photo** (paperwork + freight in frame): a vision model extracts structured lines, compares **paper vs. what’s visible**, then **auto-syncs** when clean or **stops for approval** before a **key-protected** inventory API.

### Why this isn’t already a commodity

WMS portals, template OCR, and barcode apps are real—but they skew toward **clean scans and fixed forms**, not **one messy dock frame** (glare, skew, document + load together). Few combine **joint multimodal read → variance → policy fork → verifiable write**.

**What’s different here is the stack and the pattern:**

| Layer | Why it matters |
|--------|----------------|
| **Google Gemini (multimodal)** | One **vision-language** pass over **document + scene**—clutter and layout shift without per-customer parsers. `backend/app/services/gemini_service.py` · **`POST /api/analyze`**. |
| **Railtracks** | **Flow** + **`function_node`** — inspectable agent path (`receiving_flow.py`), not one opaque script. |
| **Unkey** | Only **verified `X-API-Key`** on agent run and sync — **reject vs. accept** is demoable in seconds. |
| **DigitalOcean** | **Same container** dev → prod: `backend/Dockerfile`, `docker-compose.yml`, env-based secrets (no keys in git). |
| **Observable integration** | **`/docs`**, **`/health/ready`**, **`GET /api/about`**, header **`X-Flux-Sponsor-Tools`** — sponsors are **checkable**, not slide claims. |

---

### Problem (one paragraph)

Global receiving still leans on **manual rekeying** into ERP/WMS rows. That fuels **inventory distortion**, **supplier/3PL disputes**, and **thin audit trails** when the question is “what did we actually accept?” Flux AI targets that **reality–data gap** with **multimodal perception** and **gated** inventory writes so automation does not mean silent ledger changes.

### How it runs

**Photo in** → **Gemini** extracts + compares paper vs. scene → **`operator_brief`** + **`/ui/`** for operators → **`/api/agent/run`** may finish sync, or **approve** then **`/api/inventory/sync`** (Unkey). **Railtracks** structures the pipeline. Same API from **`/ui/`** or any HTTP client.

---

## Multimodal Frontier alignment

| Theme | Evidence in this repo |
|--------|------------------------|
| **Idea** | Systemic **reality–data gap**; vision on physical receiving, not text-only agents. |
| **Autonomy** | `POST /api/agent/run` — auto sync when variance is zero; else HITL + `/api/inventory/sync`. **`/ui/`** status. |
| **Technical** | **`/docs`**, **`/health/ready`**, mock ERP **`POST /mock/vori/receiving`**. |
| **Tool use** | **`GET /api/about`**; **`X-Flux-Sponsor-Tools`**. |
| **Presentation** | **`/ui/`** — outline in **[`DEMO_SCRIPT.md`](DEMO_SCRIPT.md)** |

## Integrations

| Sponsor | In repo |
|---------|---------|
| **Google Gemini** | `gemini_service` |
| **Unkey** | Verify v2 + `X-API-Key` on mutate routes |
| **Railtracks** | [railtracks](https://github.com/RailtownAI/railtracks) Flow in `receiving_flow.py` |
| **DigitalOcean** | Docker + compose (deploy target) |
| **Lovable / Assistant UI** | Optional extra UIs; bundled **`/ui/`** included |

**Also:** [`SUBMISSION_CHECKLIST.md`](SUBMISSION_CHECKLIST.md) · [`shipables/flux-ai-receiving/`](shipables/flux-ai-receiving/) · optional [Senso.ai](https://docs.senso.ai)

---

## Quick start

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
# Edit .env — table below. After git pull: pip install -r requirements.txt again.
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

http://localhost:8000/docs · http://localhost:8000/ui/ · **`GET /health/ready`**

**Keys:** `GEMINI_API_KEY`; when `UNKEY_ENABLED=true` → `UNKEY_ROOT_KEY` + client **`X-API-Key`**. Optional: cloud host + same env as `.env`.

## Configuration (`backend/.env`)

Copy **`backend/.env.example`** → **`backend/.env`**. Never commit `.env`.

| Variable | Notes |
|----------|--------|
| `GEMINI_API_KEY` | Required for `/api/analyze`, `/api/agent/run` |
| `GEMINI_MODEL` | Default `gemini-1.5-pro` |
| `CORS_ORIGINS` | Comma-separated if UI is not same-host |
| `UNKEY_ENABLED` | `false` = skip verify locally |
| `UNKEY_VERIFY_URL` | Default `https://api.unkey.com/v2/keys.verifyKey` |
| `UNKEY_ROOT_KEY` | Server only; clients send **`X-API-Key`** |
| `RAILTRACKS_*`, `MOCK_INVENTORY_URL` | Optional — `.env.example` |

## API (summary)

| Method | Path | Purpose |
|--------|------|---------|
| GET | `/` | → **`/ui/`** |
| GET | `/health`, `/health/ready` | Liveness + flags |
| GET | `/api/about` | Metadata + sponsors |
| POST | `/api/agent/run` | Multipart image, `operator_brief`, Unkey if on |
| POST | `/api/analyze` | Analysis only |
| POST | `/api/inventory/sync` | HITL sync + `X-API-Key` |
| POST | `/mock/vori/receiving` | Mock ERP |

Custom front end: `CORS_ORIGINS` + same routes / `X-API-Key`.

## Docker (→ DigitalOcean or any host)

```powershell
docker build -t flux-ai-api -f backend/Dockerfile backend
docker run -p 8000:8000 --env-file backend/.env flux-ai-api
```

Repo root: `docker compose up --build` · then **`https://YOUR_HOST/ui/`**

## Shipables

```bash
cd shipables/flux-ai-receiving
npx @senso-ai/shipables login
shipables publish
```

`shipables publish --dry-run` — validate package first.
