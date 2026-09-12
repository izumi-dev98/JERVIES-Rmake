"""Search the generated Knowledge Galaxy graph from voice commands."""

from __future__ import annotations

import re
from pathlib import Path

from server import load_graph, terms


ROOT = Path(__file__).resolve().parent.parent


def search_galaxy_notes(parameters=None, player=None, **_context) -> str:
    query = str((parameters or {}).get("query", "")).strip()
    if not query:
        return "Tell me what to find in Galaxy Notes."

    try:
        graph = load_graph()
    except Exception as error:
        return f"Galaxy Notes are unavailable: {error}"

    query_terms = terms(query)
    ranked = []
    for node in graph.get("nodes", []):
        haystack = f"{node.get('label', '')} {node.get('excerpt', '')}"
        score = len(query_terms & terms(haystack))
        if query.casefold() in haystack.casefold():
            score += 5
        if score:
            ranked.append((score, node))

    ranked.sort(key=lambda item: (-item[0], item[1].get("id", 0)))
    if not ranked:
        return f"I could not find '{query}' in Galaxy Notes."

    lines = []
    for _, node in ranked[:5]:
        excerpt = re.sub(r"\s+", " ", str(node.get("excerpt", ""))).strip()
        lines.append(f"{node.get('label', 'Untitled')} [{node.get('group', 'General')}]: {excerpt[:500]}")
    result = "Found in Galaxy Notes:\n" + "\n\n".join(lines)
    if player:
        player.write_log(f"[Galaxy Search] {query}")
    return result


TOOL = {
    "name": "search_galaxy_notes",
    "description": (
        "Searches the Knowledge Galaxy notes and returns matching note names and content. "
        "Use directly when the user says find, search, look up, or check something in "
        "Galaxy Notes, Galaxy View, or my saved notes. Do not search the desktop filesystem."
    ),
    "parameters": {
        "type": "OBJECT",
        "properties": {
            "query": {
                "type": "STRING",
                "description": "The note name, person, topic, or text to find in Galaxy Notes"
            }
        },
        "required": ["query"]
    },
    "handler": search_galaxy_notes,
}
