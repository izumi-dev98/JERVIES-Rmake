"""Safe startup readiness reporting without reading or exposing secret values."""
from __future__ import annotations

import json
from pathlib import Path


def collect_startup_health(
    config_path: Path,
    *,
    action_count: int,
    plugin_count: int,
    model_connection: str = "configured",
    dashboard_status: str = "available",
) -> dict[str, str]:
    try:
        config = json.loads(config_path.read_text(encoding="utf-8")) if config_path.exists() else {}
    except (OSError, json.JSONDecodeError):
        config = {}
    key = str(config.get("gemini_api_key", "")).strip()
    return {
        "api_key": "configured" if key else "missing",
        "model": "configured" if key else "unavailable until API key is configured",
        "input_audio": "selected" if str(config.get("input_device", "")).strip() else "system default",
        "output_audio": "selected" if str(config.get("output_device", "")).strip() else "system default",
        "actions": str(action_count),
        "plugins": str(plugin_count),
        "model_connection": model_connection,
        "dashboard": dashboard_status,
    }


def format_startup_health(health: dict[str, str]) -> str:
    return (
        "Startup health - "
        f"API key: {health['api_key']}; model: {health['model']}; "
        f"input: {health['input_audio']}; output: {health['output_audio']}; "
        f"actions: {health['actions']}; plugins: {health['plugins']}."
    )
