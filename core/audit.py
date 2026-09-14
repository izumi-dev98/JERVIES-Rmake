"""Privacy-preserving local audit events for sensitive assistant actions."""
from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from pathlib import Path


def _safe_label(value: str) -> str:
    """Keep audit labels bounded and free of control characters or payloads."""
    return re.sub(r"[^a-zA-Z0-9_.:-]+", "_", str(value))[:120] or "unknown"


def default_log_path(base_dir: Path | None = None) -> Path:
    root = base_dir or Path(__file__).resolve().parent.parent
    return root / "logs" / "audit.jsonl"


def write_event(event: str, action: str, status: str, *, path: Path | None = None) -> None:
    """Append metadata only; arguments, user content, and secrets are never logged."""
    record = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "event": _safe_label(event),
        "action": _safe_label(action),
        "status": _safe_label(status),
    }
    try:
        target = path or default_log_path()
        target.parent.mkdir(parents=True, exist_ok=True)
        with target.open("a", encoding="utf-8") as stream:
            stream.write(json.dumps(record, separators=(",", ":")) + "\n")
    except OSError:
        pass


def read_events(
    path: Path | None = None,
    *,
    event: str = "",
    action: str = "",
    status: str = "",
    since: str = "",
    until: str = "",
    limit: int = 100,
) -> list[dict]:
    """Read bounded, metadata-only records matching simple dashboard filters."""
    try:
        lines = (path or default_log_path()).read_text(encoding="utf-8").splitlines()
    except OSError:
        return []
    limit = max(1, min(int(limit), 500))
    records = []
    for line in lines[-5000:]:
        try:
            record = json.loads(line)
        except (TypeError, ValueError):
            continue
        if event and record.get("event") != _safe_label(event):
            continue
        if action and record.get("action") != _safe_label(action):
            continue
        if status and record.get("status") != _safe_label(status):
            continue
        timestamp = str(record.get("timestamp", ""))
        if since and timestamp < since:
            continue
        if until and timestamp > until:
            continue
        records.append(record)
    return records[-limit:]


def clear_events(path: Path | None = None) -> bool:
    try:
        target = path or default_log_path()
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text("", encoding="utf-8")
        return True
    except OSError:
        return False
