"""Voice control for leaving the embedded Knowledge Galaxy view."""

from __future__ import annotations


def close_galaxy_view(parameters=None, player=None, **_context) -> str:
    if player is None:
        return "Galaxy View is unavailable."
    try:
        from PyQt6.QtCore import QTimer
        QTimer.singleShot(0, player._leave_galaxy)
    except Exception:
        return "Galaxy View is unavailable."
    return "Returning to Mark LIII."


TOOL = {
    "name": "close_galaxy_view",
    "description": "Closes Galaxy View and returns to the main Mark LIII HUD.",
    "parameters": {"type": "OBJECT", "properties": {}},
    "handler": close_galaxy_view,
}