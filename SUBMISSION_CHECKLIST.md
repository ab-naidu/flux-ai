# Multimodal Frontier — submission checklist (rules-aligned)

This checklist maps **Devpost requirements** and **judging (20% × 5)** to what you must show.

## Hard requirements (disqualify if missed)

- [ ] **Public GitHub repo** (no previous-project reuse; build during the sprint).
- [ ] **Devpost submission** with all requested fields + **3-minute demo video**.
- [ ] **≥ 3 sponsor tools** used *effectively* (name them explicitly in README + video).
- [ ] **Shipables.dev**: publish the skill in `shipables/flux-ai-receiving/` (`shipables login` → `shipables publish`). Author metadata is set to **ab-naidu**; bump version before republishing.
- [ ] **Luma / ID** per venue rules (in-person).

## Judging rubric — what to prove in the video

### 1. Autonomy (20%)

- [ ] Show **one action** from the user (upload image on Lovable or call API once).
- [ ] Narrate: system **derives** expected vs actual, computes variance **without manual data entry**.
- [ ] Show **auto path**: when variance is zero, `POST /api/agent/run` completes sync (response `autonomy: auto_executed_inventory_sync`).
- [ ] Show **HITL path**: when variance ≠ 0, system **stops** and chat (Assistant UI) + `/api/inventory/sync` completes the story.

### 2. Idea (20%)

- [ ] 20 seconds: **reality–data gap** in receiving; cost (time/errors/safety).
- [ ] Tie to **one vertical** (e.g. grocery DC) if you use Vori-style mock.

### 3. Technical implementation (20%)

- [ ] **End-to-end works** on deployed URL (DigitalOcean): health check, analyze or agent run, sync.
- [ ] Show **evidence** of downstream call (response body or server log snippet in video).

### 4. Tool use (20%)

Call out at least three, visibly:

- [ ] **Gemini** — multimodal extraction (file reference: `backend/app/services/gemini_service.py`).
- [ ] **Unkey** — `X-API-Key` rejected when invalid; accepted when valid on `/api/agent/run` and `/api/inventory/sync`.
- [ ] **Railtracks** — trace IDs in JSON **or** webhook sink if configured (`RAILTRACKS_WEBHOOK_URL`).
- [ ] **DigitalOcean** — “API hosted on DO” + Dockerfile slide or deploy screen.
- [ ] **Lovable + Assistant UI** — dashboard + embedded chat driving sync.

Optional extra tracks: **Senso.ai** (install official Senso skills / API if you have time), **WorkOS** (SSO on approve route), **Augment Code** (state you built with Augment in Cursor).

### 5. Presentation / demo (20%)

- [ ] **Script ≤ 3:00** — rehearse twice; record clean audio.
- [ ] **Live or crisp recording** of: upload → table → (variance) → chat approve → success.
- [ ] End with **one sentence** recap + sponsor names.

## 3-minute script (template)

1. **0:00–0:25** — Problem + who hurts (receiver / inventory clerk).
2. **0:25–1:45** — **Live demo**: upload pallet+invoice → variances appear → Assistant UI: “Approve and sync” → 200 OK / success state. Mention **agent run** path for zero-variance autonomy.
3. **1:45–2:40** — **Tools**: Gemini vision, Unkey on mutate, Railtracks traces, DO hosting, Lovable UI.
4. **2:40–3:00** — Repo + Shipables skill name; what you’d pilot next.

## Pre-flight commands

```bash
cd backend
uvicorn app.main:app --host 0.0.0.0 --port 8000
curl -s http://localhost:8000/health
```

Local Unkey off: `UNKEY_ENABLED=false` in `.env` for dry runs; **turn on** for the final demo recording if judges expect live verification.
