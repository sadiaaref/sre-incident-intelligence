import pytest
from src.incident_intelligence.adapters.json_io import load_incident
from src.incident_intelligence.engine.analyzer import IncidentAnalyzer
from src.incident_intelligence.domain.models import Incident

def test_end_to_end():
    r=IncidentAnalyzer().analyze(load_incident("examples/payment_incident.json"))
    assert r.priority in {"HIGH","CRITICAL"}
    assert 0 <= r.risk_score <= 100
    assert r.change_correlation > 60
    assert r.rca_confidence > 70
    assert r.recommendations
    assert r.evidence_gaps

def test_history_is_ranked():
    a=load_incident("examples/payment_incident.json")
    b=load_incident("examples/payment_incident.json"); b.incident_id="INC-2049"
    r=IncidentAnalyzer([a]).analyze(b)
    assert r.known_pattern is True
    assert r.history_matches[0].incident_id == a.incident_id

def test_invalid_input_rejected():
    i=load_incident("examples/payment_incident.json"); i.severity=11
    with pytest.raises(ValueError): IncidentAnalyzer().analyze(i)

def test_low_signal_incident_is_not_overconfident():
    i=Incident("X","Unknown issue","search",3,3,2,5,1,10,5,0,0,100,True,symptoms=["latency"])
    r=IncidentAnalyzer().analyze(i)
    assert r.rca_confidence < 60
