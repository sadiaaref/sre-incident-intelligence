from ..domain.models import Incident

class IncidentHistory:
    """Small repository abstraction; swap with Postgres/object storage without changing the engine."""
    def __init__(self): self._items = {}
    def upsert(self, incident: Incident) -> None: self._items[incident.incident_id] = incident
    def get(self, incident_id: str): return self._items.get(incident_id)
    def all(self): return tuple(self._items.values())
