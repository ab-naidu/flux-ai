"""
Human-readable copy for operators and demo video (no secrets).
"""


def brief_for_analyze(notes: str) -> dict:
    return {
        "headline": "Photo read complete",
        "subtext": (
            "Gemini extracted line items from your invoice and estimated what’s visible on the pallet. "
            "This step does not update inventory—use “Run full audit” for the autonomous agent."
        ),
        "next_action": "Run full audit to compare, then auto-update or ask for approval.",
        "steps": [
            {"id": "upload", "label": "Photo received", "state": "done"},
            {"id": "vision", "label": "Gemini multimodal read", "state": "done"},
            {"id": "compare", "label": "Variance vs ERP", "state": "skipped"},
            {"id": "sync", "label": "Inventory update", "state": "skipped"},
        ],
        "notes_hint": (notes or "").strip() or None,
    }


def brief_for_agent(
    *,
    hitl: bool,
    auto_sync_when_clean: bool,
    autonomy: str,
    sync_ok: bool | None,
) -> dict:
    if hitl:
        return {
            "headline": "Mismatch — human check required",
            "subtext": (
                "The model found a difference between what the paperwork shows and what it sees in the image. "
                "That’s intentional: we don’t silently write wrong quantities to inventory."
            ),
            "next_action": "Review the table, then tap **Confirm inventory update** if you accept the numbers.",
            "steps": [
                {"id": "upload", "label": "Photo received", "state": "done"},
                {"id": "vision", "label": "Gemini read invoice + scene", "state": "done"},
                {"id": "compare", "label": "Variance check", "state": "done"},
                {"id": "sync", "label": "Inventory update", "state": "blocked"},
            ],
        }

    if autonomy == "auto_executed_inventory_sync" and sync_ok is True:
        return {
            "headline": "Receiving closed automatically",
            "subtext": (
                "All lines matched within tolerance. The agent updated the downstream inventory endpoint "
                "without asking for a second click — full autonomy path."
            ),
            "next_action": "None for this shipment. Capture another photo for the next delivery.",
            "steps": [
                {"id": "upload", "label": "Photo received", "state": "done"},
                {"id": "vision", "label": "Gemini read invoice + scene", "state": "done"},
                {"id": "compare", "label": "Variance check", "state": "done"},
                {"id": "sync", "label": "Inventory update (Unkey-gated)", "state": "done"},
            ],
        }

    if not auto_sync_when_clean:
        return {
            "headline": "Lines match — auto-update is off",
            "subtext": (
                "The model did not find a blocking variance, but “Update inventory automatically” was disabled, "
                "so nothing was posted yet."
            ),
            "next_action": "Turn on automatic update and run again, or push an approval flow from your client.",
            "steps": [
                {"id": "upload", "label": "Photo received", "state": "done"},
                {"id": "vision", "label": "Gemini read invoice + scene", "state": "done"},
                {"id": "compare", "label": "Variance check", "state": "done"},
                {"id": "sync", "label": "Inventory update", "state": "skipped"},
            ],
        }

    return {
        "headline": "Analysis finished",
        "subtext": "Review JSON or UI details for this run.",
        "next_action": "See trace_id for audit.",
        "steps": [
            {"id": "upload", "label": "Photo received", "state": "done"},
            {"id": "vision", "label": "Gemini read invoice + scene", "state": "done"},
            {"id": "compare", "label": "Variance check", "state": "done"},
            {"id": "sync", "label": "Inventory update", "state": "unknown"},
        ],
    }
