from src.incident_intelligence.storage.in_memory import IncidentHistory
from src.incident_intelligence.adapters.json_io import load_incident

def test_history_repository_round_trip():
    h=IncidentHistory(); incident=load_incident("examples/payment_incident.json")
    h.upsert(incident)
    assert h.get(incident.incident_id) == incident
    assert len(h.all()) == 1
