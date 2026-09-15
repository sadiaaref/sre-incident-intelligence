import json
from dataclasses import asdict
from pathlib import Path
from ..domain.models import Incident, Evidence, ChangeEvent, AnalysisResult

def load_incident(path):
    d=json.loads(Path(path).read_text(encoding="utf-8"))
    return Incident(incident_id=d["incident_id"], title=d["title"], service=d["service"], severity=d["severity"], urgency=d["urgency"], error_rate=d["error_rate"], duration_minutes=d["duration_minutes"], affected_services=d["affected_services"], affected_users=d["affected_users"], customer_impact=d["customer_impact"], dependency_failures=d["dependency_failures"], recurrence_count=d["recurrence_count"], days_since_last_occurrence=d["days_since_last_occurrence"], remediation_verified=d["remediation_verified"], symptoms=d.get("symptoms",[]), evidence=[Evidence(**e) for e in d.get("evidence",[])], changes=[ChangeEvent(**c) for c in d.get("changes",[])], metadata=d.get("metadata",{}))

def result_to_dict(result: AnalysisResult):
    return asdict(result)
