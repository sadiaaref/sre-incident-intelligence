"""Durable SQLite history adapter using only the Python standard library."""
import json
import sqlite3
from dataclasses import asdict
from ..domain.models import Incident, Evidence, ChangeEvent

class SQLiteIncidentHistory:
    def __init__(self, path: str = "incidents.db"):
        self.path = path
        self._init()

    def _connect(self):
        return sqlite3.connect(self.path)

    def _init(self):
        with self._connect() as db:
            db.execute("CREATE TABLE IF NOT EXISTS incidents (incident_id TEXT PRIMARY KEY, payload TEXT NOT NULL)")

    def upsert(self, incident: Incident) -> None:
        payload = json.dumps(asdict(incident))
        with self._connect() as db:
            db.execute("INSERT INTO incidents(incident_id,payload) VALUES(?,?) ON CONFLICT(incident_id) DO UPDATE SET payload=excluded.payload", (incident.incident_id, payload))

    def get(self, incident_id: str):
        with self._connect() as db:
            row = db.execute("SELECT payload FROM incidents WHERE incident_id=?", (incident_id,)).fetchone()
        return _from_payload(row[0]) if row else None

    def all(self):
        with self._connect() as db:
            rows = db.execute("SELECT payload FROM incidents ORDER BY incident_id").fetchall()
        return tuple(_from_payload(r[0]) for r in rows)

def _from_payload(payload: str) -> Incident:
    d = json.loads(payload)
    d["evidence"] = [Evidence(**e) for e in d.get("evidence", [])]
    d["changes"] = [ChangeEvent(**c) for c in d.get("changes", [])]
    return Incident(**d)
