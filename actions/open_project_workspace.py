"""Open the current Mark LIII project in a desktop workspace."""

from __future__ import annotations

import os
import platform
import shutil
import subprocess
from pathlib import Path


PROJECT_DIR = Path(__file__).resolve().parent.parent


def _open_explorer() -> None:
    if platform.system() == "Windows":
        os.startfile(str(PROJECT_DIR))
    elif platform.system() == "Darwin":
        subprocess.Popen(["open", str(PROJECT_DIR)])
    else:
        subprocess.Popen(["xdg-open", str(PROJECT_DIR)])


def _open_vscode() -> None:
    code = shutil.which("code") or shutil.which("code.cmd")
    if code:
        subprocess.Popen([code, "--reuse-window", str(PROJECT_DIR)])
        return

    if platform.system() == "Windows":
        candidates = [
            Path.home() / "AppData/Local/Programs/Microsoft VS Code/bin/code.cmd",
            Path("C:/Program Files/Microsoft VS Code/bin/code.cmd"),
        ]
        for candidate in candidates:
            if candidate.is_file():
                subprocess.Popen([str(candidate), "--reuse-window", str(PROJECT_DIR)])
                return
    raise FileNotFoundError("VS Code command was not found")


def open_project_workspace(parameters=None, player=None, **_context) -> str:
    target = str((parameters or {}).get("target", "vscode")).lower().strip()
    if target in {"folder", "explorer", "file explorer", "files"}:
        targets = {"explorer"}
    elif target in {"both", "all", "screen"}:
        targets = {"vscode", "explorer"}
    else:
        targets = {"vscode"}

    opened = []
    errors = []
    for item in targets:
        try:
            _open_vscode() if item == "vscode" else _open_explorer()
            opened.append("VS Code" if item == "vscode" else "File Explorer")
        except Exception as error:
            errors.append(f"{item}: {error}")

    if player:
        player.write_log(f"[Workspace] {PROJECT_DIR}")
        if hasattr(player, "show_workspace_status"):
            player.show_workspace_status(str(PROJECT_DIR), opened, errors)
    if not opened:
        return "Could not open the Mark LIII project. " + "; ".join(errors)
    result = f"Opened Mark LIII in {' and '.join(opened)}."
    if errors:
        result += " Could not open: " + "; ".join(errors)
    return result


TOOL = {
    "name": "open_project_workspace",
    "description": (
        "Opens the current Mark LIII project folder on the user's machine. "
        "Use when the user asks to show this project, open the current workspace, "
        "open Mark LIII, or display the project on screen. For 'full workspace', "
        "'show everything', or 'show the project on screen', use target 'both'. "
        "Default is VS Code. "
        "Use target 'explorer' for the folder, or 'both' for VS Code and File Explorer."
    ),
    "parameters": {
        "type": "OBJECT",
        "properties": {
            "target": {
                "type": "STRING",
                "description": "vscode (default), explorer, or both"
            }
        }
    },
    "handler": open_project_workspace,
}
