"""Voice controls for the embedded Knowledge Galaxy view."""

from __future__ import annotations


def _schedule_ui(player, callback) -> bool:
    if player is None:
        return False
    try:
        from PyQt6.QtCore import QTimer
        QTimer.singleShot(0, callback)
        return True
    except Exception:
        return False


def open_galaxy_view(parameters=None, player=None, **_context) -> str:
    if not _schedule_ui(player, player._open_galaxy if player else None):
        return "Galaxy View is unavailable."
    return "Opening Galaxy View."


TOOL = {
    "name": "open_galaxy_view",
    "description": (
        "Opens the interactive Knowledge Galaxy view inside Mark LIII. "
        "Use this tool directly when the user says Galaxy View, knowledge galaxy, "
        "open the galaxy, or show my notes. Do not use file_processor or open_app "
        "and do not search for a filename such as anydesk.md."
    ),
    "parameters": {"type": "OBJECT", "properties": {}},
    "handler": open_galaxy_view,
}
