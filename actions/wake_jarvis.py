"""Voice action for waking JARVIS when wake-word mode is enabled."""

from __future__ import annotations


def wake_jarvis(parameters=None, player=None, **_context) -> str:
    if player is None:
        return "Wake control is unavailable."
    try:
        callback = player.on_wake_now
        if callback is None:
            return "Wake control is unavailable."
        callback()
        return "JARVIS is awake."
    except Exception:
        return "Wake control is unavailable."


TOOL = {
    "name": "wake_jarvis",
    "description": (
        "Wakes JARVIS when the user says wake up, wake Jarvis, or start listening. "
        "Call this for an explicit wake request."
    ),
    "parameters": {"type": "OBJECT", "properties": {}},
    "handler": wake_jarvis,
}