import json
import threading
from http.client import HTTPConnection
from http.server import ThreadingHTTPServer
from pathlib import Path

from src.incident_intelligence.adapters.json_io import load_incident
from src.incident_intelligence.api.http import Handler
from src.incident_intelligence.engine.analyzer import IncidentAnalyzer
from src.incident_intelligence.engine.rules import rank_hypotheses
from src.incident_intelligence.storage.sqlite import SQLiteIncidentHistory


def test_hypothesis_engine_returns_ranked_explanations():
    i = load_incident("examples/payment_incident.json")
    ranked = rank_hypotheses(i, 90)
    assert len(ranked) >= 3
    assert ranked[0].confidence >= ranked[-1].confidence
    assert ranked[0].evidence


def test_similarity_normalizes_text_variants():
    a = load_incident("examples/payment_incident.json")
    b = load_incident("examples/payment_incident.json")
    b.incident_id = "DIFFERENT"
    b.symptoms = ["Payment timeout"]
    a.symptoms = ["payment timeouts"]
    assert IncidentAnalyzer([a]).analyze(b).history_matches


def test_history_excludes_current_incident():
    i = load_incident("examples/payment_incident.json")
    result = IncidentAnalyzer([i]).analyze(i)
    assert not result.history_matches


def test_empty_history_is_supported():
    i = load_incident("examples/payment_incident.json")
    assert IncidentAnalyzer().analyze(i).history_matches == ()


def test_sqlite_history_round_trip(tmp_path):
    db = SQLiteIncidentHistory(str(tmp_path / "incidents.db"))
    i = load_incident("examples/payment_incident.json")
    db.upsert(i)
    assert db.get(i.incident_id) == i
    assert len(db.all()) == 1


def test_sqlite_upsert_replaces_existing_incident(tmp_path):
    db = SQLiteIncidentHistory(str(tmp_path / "incidents.db"))
    i = load_incident("examples/payment_incident.json")
    db.upsert(i)
    i.title = "Updated incident"
    db.upsert(i)
    assert db.get(i.incident_id).title == "Updated incident"
    assert len(db.all()) == 1


def test_api_health_endpoint():
    server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        c = HTTPConnection(*server.server_address)
        c.request("GET", "/health")
        r = c.getresponse()
        assert r.status == 200
        assert json.loads(r.read())["status"] == "ok"
    finally:
        server.shutdown()
        server.server_close()


def test_api_rejects_unknown_route():
    server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        c = HTTPConnection(*server.server_address)
        c.request("GET", "/missing")
        assert c.getresponse().status == 404
    finally:
        server.shutdown()
        server.server_close()


def test_api_analyze_happy_path():
    payload = json.loads(Path("examples/payment_incident.json").read_text())
    server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        c = HTTPConnection(*server.server_address)
        body = json.dumps(payload)
        c.request("POST", "/analyze", body, {"Content-Type": "application/json"})
        r = c.getresponse()
        data = json.loads(r.read())
        assert r.status == 200
        assert data["incident_id"] == payload["incident_id"]
        assert data["report"]
    finally:
        server.shutdown()
        server.server_close()


def test_api_rejects_invalid_incident():
    payload = json.loads(Path("examples/payment_incident.json").read_text())
    payload["severity"] = 99
    server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        c = HTTPConnection(*server.server_address)
        c.request("POST", "/analyze", json.dumps(payload), {"Content-Type": "application/json"})
        assert c.getresponse().status == 400
    finally:
        server.shutdown()
        server.server_close()
