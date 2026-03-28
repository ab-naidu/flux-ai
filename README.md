# 📦 Flux AI: The Multimodal Receiving Auditor

**Zero-shot autonomous auditor** for physical-to-digital warehouse receiving. Built for the **Multimodal Frontier Hackathon**.

Most agents only read text prompts. **Flux AI sees the real world.** We are targeting the massive **reality-data gap** in global supply chains, where physical pallets arrive but inventory systems rely on manual, error-prone data entry. 

**Flux AI** uses **one photo** (paperwork + physical freight in the same frame): a vision model extracts structured lines, compares **expected paperwork vs. what’s physically visible**, then **auto-syncs** when clean or **pauses for human-in-the-loop (HITL) approval** before hitting an API-key protected inventory endpoint.

---

## 🏆 Judging Criteria Alignment

Flux AI was built specifically to max out the Multimodal Frontier rubric (20% each):

1. **Idea:** Addresses a massive real-world problem—grocery store and warehouse shrinkage—by using multimodal vision on physical cargo, rather than chat interfaces.
2. **Autonomy:** Evaluates variance dynamically. If Expected = Actual (Zero Variance), the agent acts autonomously and syncs the ledger. If there's a discrepancy, it enforces policy by stopping and requesting human review.
3. **Tool Use:** Integrates **5** distinct sponsor technologies (Gemini, Unkey, DigitalOcean, Railtracks, Shipables).
4. **Technical Implementation:** A production-ready FastAPI backend using the `Railtracks` observability flow, secured by `Unkey`, and easily deployable via Docker (`DigitalOcean`).
5. **Presentation:** Built alongside a bundled `/ui/` to visually explain the agent's cognitive path in 3 minutes.

---

## 🛠️ Sponsor Integrations (Tool Use)

| Sponsor | How we used it |
|---------|----------------|
| **Google Gemini** | True multimodal vision (`gemini-1.5-pro`). It reads the invoice text and counts the physical boxes in a single pass. (`app/services/gemini_service.py`) |
| **Unkey** | Enforces zero-trust mutations. The agent and human approvals must pass an `X-API-Key` check to sync to inventory. (`app/services/inventory_service.py`) |
| **Railtracks** | Agentic workflows. We use `Flow` and `function_node` to break the agent's path into observable, traceable blocks. (`app/services/receiving_flow.py`) |
| **DigitalOcean** | Production inference. The entire backend is containerized (`backend/Dockerfile`) and ready for App Platform or a Droplet. |
| **Shipables** | Packaged and published as the `flux-ai-receiving-auditor` skill on `shipables.dev` for 1-click installation. (`shipables/flux-ai-receiving/`) |

*Note: The API returns an `X-Flux-Sponsor-Tools` header on all requests as proof of integration.*

---

## 🚀 Quick Start (Local Dev)

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
# Fill in your GEMINI_API_KEY and UNKEY_ROOT_KEY in the .env file
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

- **Built-in UI:** [http://localhost:8000/ui/](http://localhost:8000/ui/)
- **API Docs:** [http://localhost:8000/docs](http://localhost:8000/docs)
- **Health Check:** `GET /health/ready`

## 🐳 Docker (DigitalOcean Deploy)

```bash
docker compose up --build
```
Then navigate to `http://<your-droplet-ip>:8000/ui/`.

---

## 🧬 How the Agent Works (The Flow)

1. **Physical Input:** Operator uploads a photo of the loading dock (invoice taped to a pallet).
2. **Cognitive Pass (Gemini):** Extracts line items: `SKU`, `expected_qty`, and determines `actual_qty` from visual counting.
3. **Variance Policy Engine (Railtracks):**
   - **Zero Variance:** Agent bypasses UI, authenticates with Unkey, and updates the ERP automatically.
   - **Variance Detected:** Agent halts execution (`autonomy: paused_for_hitl`) and returns the discrepancy table to the operator.
4. **Governed Write (Unkey):** Operator clicks "Approve & Sync", triggering the final secure `POST /api/inventory/sync`.

This ensures autonomy where possible, and strict human safety where necessary.
