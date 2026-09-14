"""Secret-free model lifecycle states used by the desktop and dashboard."""
from __future__ import annotations

MODEL_STATES = ("starting", "connected", "offline", "reconnecting", "stopped")


def normalize_model_state(state: str) -> str:
    value = str(state or "").strip().lower()
    return value if value in MODEL_STATES else "offline"


def model_status(state: str) -> dict[str, str]:
    normalized = normalize_model_state(state)
    return {
        "state": normalized,
        "local_features": "available",
        "natural_language": "available" if normalized == "connected" else "unavailable",
    }
