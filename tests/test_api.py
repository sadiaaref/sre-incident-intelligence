import json
from src.incident_intelligence.adapters.json_io import load_incident
from src.incident_intelligence.api.service import IncidentIntelligenceService

def test_service_boundary_reuses_engine():
    incident = load_incident("examples/payment_incident.json")
    result = IncidentIntelligenceService().analyze(incident)
    assert result.incident_id == incident.incident_id
    assert 0 <= result.risk_score <= 100
