"""Hardware-safe readiness and progress helpers for the first-run setup wizard."""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Mapping

CHECKS = ("api_key", "model", "microphone", "speaker", "plugins", "permissions")


def _result(status: str, detail: str, repair: str = "") -> dict[str, str]:
    return {"status": status, "detail": detail, "repair": repair}


def collect_setup_state(
    config_path: Path,
    *,
    audio_devices: Mapping[str, list[str]] | None = None,
    plugin_counts: tuple[int, int] | None = None,
    permission_status: str = "manual review",
) -> dict[str, dict[str, str]]:
    """Return display-safe readiness states without exposing configuration values."""
    try:
        config = json.loads(config_path.read_text(encoding="utf-8")) if config_path.exists() else {}
    except (OSError, json.JSONDecodeError):
        config = {}

    has_key = bool(str(config.get("gemini_api_key", "")).strip())
    states = {
        "api_key": _result("ready" if has_key else "blocked",
                            "API key configured" if has_key else "API key required",
                            "focus_api_key" if not has_key else ""),
        "model": _result("ready" if has_key else "blocked",
                          "Model configuration is ready" if has_key else "Waiting for API key",
                          "focus_api_key" if not has_key else ""),
    }

    devices = audio_devices or {}
    for key, label in (("input_device", "microphone"), ("output_device", "speaker")):
        selected = str(config.get(key, "")).strip()
        available = {str(name).strip() for name in devices.get("input" if label == "microphone" else "output", [])}
        if not selected:
            states[label] = _result("ready", "Using system default", "open_audio")
        elif available and selected not in available:
            states[label] = _result("attention", "Saved device is unavailable", "open_audio")
        else:
            states[label] = _result("ready", "Selected device configured", "")

    if plugin_counts is None:
        states["plugins"] = _result("pending", "Plugin scan starts after initialisation", "open_plugins")
    else:
        active, rejected = plugin_counts
        states["plugins"] = _result(
            "ready" if rejected == 0 else "attention",
            f"{active} active, {rejected} rejected",
            "open_plugins" if rejected else "",
        )
    permission_status = str(permission_status).strip().lower() or "manual review"
    states["permissions"] = _result(
        "ready" if permission_status == "ready" else "manual",
        "Permissions verified" if permission_status == "ready" else "Review desktop permissions",
        "review_permissions",
    )
    return states


def load_progress(path: Path) -> dict[str, object]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {"completed": {}}
    completed = data.get("completed") if isinstance(data, dict) else None
    if not isinstance(completed, dict):
        completed = {}
    return {"completed": {key: bool(completed.get(key)) for key in CHECKS}}


def save_progress(path: Path, completed: Mapping[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    data = {
        "completed": {key: bool(completed.get(key)) for key in CHECKS},
        "updated_at": datetime.now(timezone.utc).isoformat(),
    }
    path.write_text(json.dumps(data, indent=2), encoding="utf-8")
