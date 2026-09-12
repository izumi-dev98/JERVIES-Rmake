"""Local viewer server and note-grounded chat endpoint."""
from __future__ import annotations

import json
import re
import urllib.error
import urllib.request
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

ROOT = Path(__file__).resolve().parent
VIEWER = ROOT / "viewer"
MARK_CONFIG = ROOT / "config" / "api_keys.json"
PORT = 4700
HISTORY: dict[str, list[dict[str, str]]] = {}


def load_graph() -> dict:
    source = (VIEWER / "graph-data.js").read_text(encoding="utf-8")
    return json.loads(source.removeprefix("const GRAPH = ").rstrip(";\n"))


def terms(text: str) -> set[str]:
    return {word for word in re.findall(r"[a-z0-9]{3,}", text.casefold())}


def select_notes(question: str, graph: dict) -> list[dict]:
    question_terms = terms(question)
    ranked = []
    for node in graph["nodes"]:
        title_terms = terms(node["label"])
        body_terms = terms(node["excerpt"])
        score = len(question_terms & body_terms) + 3 * len(question_terms & title_terms)
        ranked.append((score, node))
    ranked.sort(key=lambda item: (-item[0], item[1]["id"]))
    return [node for score, node in ranked[:6] if score > 0] or [node for _, node in ranked[:6]]


def build_prompt(question: str, selected: list[dict], history: list[dict[str, str]]) -> str:
    notes = "\n\n".join(f"[{node['id']}] {node['label']}\n{node['excerpt']}" for node in selected)
    instruction = ("Answer ONLY from these notes, in 2-3 sentences. Admit it when the notes do not cover the answer.\n\n"
                   "NOTES:\n" + notes)
    conversation = "\n".join(f"{item['role'].upper()}: {item['content']}" for item in history[-6:])
    return f"{instruction}\n\nCONVERSATION:\n{conversation}\nUSER: {question}"


def ask_ollama(question: str, selected: list[dict], history: list[dict[str, str]], config: dict) -> str:
    prompt = build_prompt(question, selected, history)
    base_url = str(config.get("ollama_base_url", "http://127.0.0.1:11434")).rstrip("/")
    model = str(config.get("ollama_model", "llama3.2")).strip()
    payload = json.dumps({"model": model, "messages": [{"role": "user", "content": prompt}], "stream": False}).encode("utf-8")
    request = urllib.request.Request(f"{base_url}/api/chat", data=payload,
                                     headers={"content-type": "application/json"}, method="POST")
    try:
        with urllib.request.urlopen(request, timeout=90) as response:
            data = json.loads(response.read().decode("utf-8"))
        return data["message"]["content"].strip()
    except urllib.error.HTTPError as error:
        detail = error.read().decode("utf-8", errors="replace")[:220]
        return f"Ollama error HTTP {error.code}: {detail}"
    except (urllib.error.URLError, TimeoutError) as error:
        return f"Ollama is not running at {base_url}. Start Ollama and install model '{model}'. ({error})"


def ask_gemini(question: str, selected: list[dict], history: list[dict[str, str]], config: dict) -> str:
    api_key = config.get("gemini_api_key", "").strip()
    if not api_key:
        return "Add a Gemini API key to config/api_keys.json to ask the galaxy questions."
    prompt = build_prompt(question, selected, history)
    payload = json.dumps({"contents": [{"role": "user", "parts": [{"text": prompt}]}]}).encode("utf-8")
    errors = []
    configured_model = str(config.get("gemini_model", "gemini-3.6-flash")).strip()
    models = [configured_model] + [model for model in ("gemini-2.5-flash", "gemini-3.6-flash")
                                   if model != configured_model]
    for model in models:
        endpoint = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"
        request = urllib.request.Request(endpoint, data=payload,
                                         headers={"content-type": "application/json"}, method="POST")
        try:
            with urllib.request.urlopen(request, timeout=45) as response:
                data = json.loads(response.read().decode("utf-8"))
            return data["candidates"][0]["content"]["parts"][0]["text"].strip()
        except urllib.error.HTTPError as error:
            detail = error.read().decode("utf-8", errors="replace")[:240]
            if error.code == 429:
                return "Gemini quota exceeded for this API key. Check Gemini billing or rate limits, then try again."
            errors.append(f"{model}: HTTP {error.code} ({detail})")
        except (urllib.error.URLError, TimeoutError) as error:
            errors.append(f"{model}: {error}")
    return "Gemini is unavailable. " + " | ".join(errors)


class Handler(BaseHTTPRequestHandler):
    def log_message(self, format: str, *args) -> None:
        print(f"{self.address_string()} - {format % args}")

    def send_json(self, status: int, body: dict) -> None:
        raw = json.dumps(body).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(raw)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(raw)

    def do_GET(self) -> None:
        path = self.path.split("?", 1)[0]
        if path == "/" or path == "/index.html":
            path = "/index.html"
        requested = (VIEWER / path.lstrip("/")).resolve()
        if requested.parent != VIEWER.resolve() or not requested.is_file():
            self.send_error(404)
            return
        content_type = "text/html; charset=utf-8" if requested.suffix == ".html" else "application/javascript; charset=utf-8"
        raw = requested.read_bytes()
        self.send_response(200)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(raw)))
        self.end_headers()
        self.wfile.write(raw)

    def do_POST(self) -> None:
        if self.path != "/chat":
            self.send_error(404)
            return
        try:
            body = json.loads(self.rfile.read(int(self.headers.get("Content-Length", "0"))))
            question = str(body.get("question", "")).strip()
            if not question:
                raise ValueError("question is required")
            session = str(body.get("session", self.client_address[0]))
            graph = load_graph()
            selected = select_notes(question, graph)
            history = HISTORY.setdefault(session, [])
            config = json.loads(MARK_CONFIG.read_text(encoding="utf-8"))
            provider = str(config.get("galaxy_provider", "ollama")).strip().lower()
            if provider == "gemini":
                answer = ask_gemini(question, selected, history, config)
            elif provider == "auto":
                answer = ask_ollama(question, selected, history, config)
                if answer.startswith("Ollama is not running") or answer.startswith("Ollama error"):
                    answer = ask_gemini(question, selected, history, config)
            else:
                answer = ask_ollama(question, selected, history, config)
            history.extend([{"role": "user", "content": question}, {"role": "assistant", "content": answer}])
            del history[:-6]
            self.send_json(200, {"answer": answer, "nodes": [node["id"] for node in selected]})
        except (ValueError, json.JSONDecodeError) as error:
            self.send_json(400, {"error": str(error)})


if __name__ == "__main__":
    print(f"MARK galaxy at http://localhost:{PORT}")
    ThreadingHTTPServer(("127.0.0.1", PORT), Handler).serve_forever()