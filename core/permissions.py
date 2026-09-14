"""Local action permission policy with conservative defaults."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Mapping

LEVELS = ("safe", "confirm", "blocked")
DEFAULT_LEVEL = "confirm"
_POLICY_KEY = "permissions"


def default_config_path() -> Path:
    return Path(__file__).resolve().parent.parent / "config" / "api_keys.json"


def _load_config(path: Path) -> dict:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        return data if isinstance(data, dict) else {}
    except (OSError, json.JSONDecodeError):
        return {}


def load_policy(config_path: Path) -> dict[str, str]:
    raw = _load_config(config_path).get(_POLICY_KEY, {})
    if not isinstance(raw, Mapping):
        return {}
    return {str(key): str(value) for key, value in raw.items() if value in LEVELS}


def save_level(config_path: Path, action: str, level: str) -> None:
    if level not in LEVELS:
        raise ValueError(f"Unknown permission level: {level}")
    data = _load_config(config_path)
    policy = data.get(_POLICY_KEY)
    if not isinstance(policy, dict):
        policy = {}
    policy[str(action)] = level
    data[_POLICY_KEY] = policy
    config_path.parent.mkdir(parents=True, exist_ok=True)
    config_path.write_text(json.dumps(data, indent=4), encoding="utf-8")


def permission_key(action: str, parameters: Mapping | None = None) -> str:
    params = parameters or {}
    subaction = str(params.get("action", "")).strip().lower().replace("-", "_")
    if action == "file_controller" and subaction == "delete":
        return "file_delete"
    if action == "computer_settings" and subaction in {"shutdown", "restart", "toggle_wifi"}:
        return f"computer_{subaction}"
    if action == "send_message":
        return "messaging"
    if action == "computer_control":
        return "computer_control"
    return str(action)


def level_for(config_path: Path, action: str, parameters: Mapping | None = None) -> str:
    key = permission_key(action, parameters)
    policy = load_policy(config_path)
    if key in policy:
        return policy[key]
    if key in {"file_delete", "messaging", "computer_control", "computer_shutdown", "computer_restart", "computer_toggle_wifi"}:
        return DEFAULT_LEVEL
    return "safe"


def policy_view(config_path: Path) -> dict[str, str]:
    """Return configured values plus the risk-sensitive defaults users can edit."""
    policy = load_policy(config_path)
    keys = (
        "computer_control", "file_delete", "computer_shutdown",
        "computer_restart", "computer_toggle_wifi", "messaging",
    )
    return {key: policy.get(key, level_for(config_path, key)) for key in keys}
