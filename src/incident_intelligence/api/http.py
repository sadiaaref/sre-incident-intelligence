"""Dependency-free HTTP adapter with payload limits and JSON responses."""
import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from ..engine.analyzer import IncidentAnalyzer
from ..adapters.json_io import result_to_dict
from ..domain.models import Incident, Evidence, ChangeEvent

MAX_BODY = 1_000_000

class Handler(BaseHTTPRequestHandler):
    analyzer = IncidentAnalyzer()

    def _json(self, status, payload):
        encoded = json.dumps(payload).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(encoded)))
        self.end_headers()
        self.wfile.write(encoded)

    def do_GET(self):
        if self.path == "/health":
            self._json(200, {"status": "ok"})
        else:
            self._json(404, {"error": "not found"})

    def do_POST(self):
        if self.path != "/analyze":
            self._json(404, {"error": "not found"})
            return
        try:
            length = int(self.headers.get("Content-Length", "0"))
            if length <= 0 or length > MAX_BODY:
                raise ValueError("request body must be between 1 byte and 1 MB")
            body = json.loads(self.rfile.read(length))
            if not isinstance(body, dict):
                raise ValueError("request JSON must be an object")
            incident = Incident(**{**body, "evidence": [Evidence(**e) for e in body.get("evidence", [])], "changes": [ChangeEvent(**c) for c in body.get("changes", [])]})
            self._json(200, result_to_dict(self.analyzer.analyze(incident)))
        except (ValueError, KeyError, TypeError, json.JSONDecodeError) as exc:
            self._json(400, {"error": str(exc)})

    def log_message(self, fmt, *args):
        return

def serve(host="127.0.0.1", port=8080):
    server = ThreadingHTTPServer((host, port), Handler)
    print(f"Incident Intelligence API listening on http://{host}:{port}")
    server.serve_forever()
