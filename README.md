# Flux AI

**Zero-shot autonomous auditor** for physical-to-digital warehouse receiving.

Many systems only see what someone types after a truck arrives. **Flux AI** starts from **one photo** with **paperwork and freight in the same frame**: a vision model extracts structured lines, compares **what the document claims** to **what the image suggests is on the load**, then **syncs inventory automatically** when variance is clean or **stops for human approval** before a **key-protected** inventory API.

---

## Integrations

| Component | Role |
|-----------|------|
| **Google Gemini** | Multimodal extraction from dock imagery (`backend/app/services/gemini_service.py`). |
| **Unkey** | `X-API-Key` on agent run and inventory sync; server uses `UNKEY_ROOT_KEY` for verify. |
| **Railtracks** | `Flow` + `function_node` receiving pipeline (`backend/app/services/receiving_flow.py`). |
| **Docker** | `backend/Dockerfile`, `docker-compose.yml` for deployment (e.g. cloud VPS or App Platform). |
| **Senso Shipables** | Optional packaged skill under `shipables/flux-ai-receiving/`. |

Responses include header **`X-Flux-Sponsor-Tools`** and **`GET /api/about`** for a machine-readable summary.

---

## Quick start

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
# Set GEMINI_API_KEY; if UNKEY_ENABLED=true, set UNKEY_ROOT_KEY and use a valid X-API-Key from the client
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

- **Operator UI:** http://localhost:8000/ui/
- **OpenAPI:** http://localhost:8000/docs
- **Readiness:** `GET /health/ready`

## Docker

```powershell
docker compose up --build
```

Serve with the same environment variables as local `.env` (never commit `.env`).

---

## How it works

1. **Input** — Photo of dock + invoice/packing list in frame.
2. **Extraction (Gemini)** — Structured line items, expected vs. inferred actual quantities.
3. **Policy (Railtracks)** — Zero variance and auto-sync allowed → gated sync; otherwise paused for HITL and **`POST /api/inventory/sync`** with Unkey.

---

## What belongs in Git

Commit **source and config templates**: `backend/` application code, `requirements.txt`, `Dockerfile`, `docker-compose.yml`, `.env.example`, `.gitignore`, and this `README.md`.

Do **not** commit: `.env` (secrets), `.venv/` or other virtualenvs, `__pycache__/`, IDE junk, or API keys. Optional local notes (`DEMO_SCRIPT.md`, `SUBMISSION_CHECKLIST.md`, etc.) can stay untracked with `.gitignore` if you prefer, or remain in the repo as non-runtime documentation.
