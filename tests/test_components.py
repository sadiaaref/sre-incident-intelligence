from src.incident_intelligence.engine.scoring import impact_score, blast_radius
from src.incident_intelligence.engine.similarity import similarity
from src.incident_intelligence.adapters.json_io import load_incident

def test_scoring_bounds():
    assert 0 <= impact_score(100,1000,100000,100) <= 100
    assert 0 <= blast_radius(100,100) <= 100

def test_similarity_identical_is_high():
    a=load_incident("examples/payment_incident.json")
    assert similarity(a,a)==100
