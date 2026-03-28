# 🎙️ The 3-Minute Winning Demo Script

**Theme Hook:** *"Our agent operates on the physical world, not just text."*

This script is strictly timed to 3 minutes and physically maps to the **5 Judging Criteria (Idea, Autonomy, Tech, Tool Use, Presentation)**. Have two sample photos ready on your desktop:
1. **"Clean Image"**: Invoice matches the boxes exactly. (Variance = 0)
2. **"Messy Image"**: The invoice says 10 cases, but only 8 are visibly on the pallet. (Variance = -2)

---

### Phase 1: The Idea (0:00 – 0:30)
*(Screen: Show the `/ui/` interface on your deployed server, or a slider showing a messy warehouse dock.)*

**Spoken:**  
> "Hi, we’re team Flux AI. Most agents today are powerful, but they operate purely on text prompts. The **Multimodal Frontier** is about agents that see the real, physical world.  
> 
> "In global supply chains, specifically grocery and warehouse receiving, there is a massive reality-data gap. Physical pallets arrive, but the ERP system relies on slow, error-prone human data entry to verify it against the paperwork. That gap costs millions in shrinkage and disputes.
>  
> "Flux AI fixes this. We built a zero-shot autonomous auditor. One photo of the dock is all it needs."

---

### Phase 2: Autonomy — The Happy Path (0:30 – 1:30)
*(Screen: Click to upload the **"Clean Image"**. (The API Key is already pre-filled). Click "Run agent".)*

**Spoken:**  
> "Let’s look at a live receive. I’m uploading a single, messy photo showing both the paper invoice and the physical goods on the pallet.  
> 
> *(Wait for the UI to return the Green 'FULL SYNCHED' banner)*  
> 
> "Notice what just happened. The agent used **Google Gemini's vision model** to read the expected quantities off the paper, and then visually counted the physical boxes on the pallet. Because the variance was precisely zero, the agent acted autonomously. It bypassed human approval and automatically synced the ledger to our inventory API. No data entry required."

---

### Phase 3: Technical Implementation & HITL (1:30 – 2:30)
*(Screen: Upload the **"Messy Image"**. Click "Run agent". A Yellow 'Variance Detected' banner appears.)*

**Spoken:**  
> "But what happens when things don't match? Here, the invoice says 10 cases, but Gemini only sees 8.  
> 
> "Real autonomy requires governed policy. Because variance was detected, the agent halted execution. This pipeline is fully observable because we built it using the **Railtracks framework**, mapping the cognitive path into discrete, traceable nodes. 
>  
> "The agent requests a Human-in-the-Loop review. As the operator, I see the discrepancy. If I agree, I click 'Approve & Sync'. But notice this: changing the ledger requires zero-trust security. The inventory sync is strictly gated by **Unkey**. Without a valid API key, the agent is powerless."

*(Screen: Click 'Approve & Sync'. Show the success JSON or terminal output.)*

---

### Phase 4: Tool Use & The Close (2:30 – 3:00)
*(Screen: Open the Devpost/GitHub page, or show the Dropet dashboard from DigitalOcean.)*

**Spoken:**  
> "We heavily utilized our sponsor stack to make this production-ready today.  
> 1. We used **Google DeepMind's Gemini** for the core multimodal extraction.
> 2. We enforced secure ledger mutations using **Unkey**.
> 3. We built the agent's logic flow using **Railtracks**.
> 4. We containerized the entire backend and it is deployed live right now on **DigitalOcean**.
> 5. And finally, you can install our entire workflow via **Shipables** right now as the `flux-ai-receiving-auditor` skill.
>
> "Flux AI: Agents that see the world. Thank you."

---

### ⚠️ Before Recording:
- Ensure your backend is running (`uvicorn` or Docker).
- Have your `X-API-Key` (from Unkey) generated and copied.
- Do a dry run of the script with a stopwatch. If you go over 3:15, cut adjectives, not the sponsor names!
