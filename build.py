"""Build viewer/graph-data.js from a folder of markdown notes."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DEFAULT_NOTES = ROOT / "notes"
OUTPUT = ROOT / "viewer" / "graph-data.js"
WIKILINK = re.compile(r"\[\[([^\]|#]+)(?:#[^\]|]+)?(?:\|[^\]]+)?\]\]")


def clean_text(text: str) -> str:
    text = re.sub(r"```.*?```", " ", text, flags=re.DOTALL)
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"[#*_>`~-]+", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def title_for(path: Path) -> str:
    return path.stem.replace("_", " ").replace("-", " ").strip().title()


def build(notes_dir: Path = DEFAULT_NOTES) -> dict:
    files = sorted(notes_dir.rglob("*.md"), key=lambda p: p.relative_to(notes_dir).as_posix().lower())
    nodes = []
    by_title = {}
    for path in files:
        relative = path.relative_to(notes_dir)
        title = title_for(path)
        excerpt = clean_text(path.read_text(encoding="utf-8", errors="replace"))[:700]
        folder = relative.parent.as_posix() if relative.parent != Path(".") else "General"
        node = {"id": len(nodes), "label": title, "group": folder, "excerpt": excerpt}
        nodes.append(node)
        by_title[title.casefold()] = node["id"]
        by_title[path.stem.casefold()] = node["id"]

    links = set()
    for source, path in enumerate(files):
        text = path.read_text(encoding="utf-8", errors="replace")
        body = clean_text(text).casefold()
        mentioned = {match.strip().casefold() for match in WIKILINK.findall(text)}
        for key, target in by_title.items():
            if target == source:
                continue
            title_hit = key in body
            wiki_hit = key in mentioned
            if title_hit or wiki_hit:
                links.add(tuple(sorted((source, target))))

    return {"nodes": nodes, "links": [{"source": a, "target": b} for a, b in sorted(links)]}


def main() -> None:
    notes_dir = Path(sys.argv[1]).expanduser() if len(sys.argv) > 1 else DEFAULT_NOTES
    graph = build(notes_dir.resolve())
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    payload = json.dumps(graph, ensure_ascii=True, separators=(",", ":"))
    OUTPUT.write_text("const GRAPH = " + payload + ";\n", encoding="utf-8")
    print(f"Built {len(graph['nodes'])} nodes and {len(graph['links'])} links from {notes_dir}")


if __name__ == "__main__":
    main()