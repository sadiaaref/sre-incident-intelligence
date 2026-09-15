from dataclasses import dataclass, field
from typing import Any

@dataclass(frozen=True)
class Evidence:
    source: str
    signal: str
    strength: float = 1.0
    observed_at: str | None = None

@dataclass(frozen=True)
class ChangeEvent:
    change_id: str
    service: str
    change_type: str
    minutes_before_incident: int
    risk_level: str = "medium"

@dataclass
class Incident:
    incident_id: str
    title: str
    service: str
    severity: int
    urgency: int
    error_rate: float
    duration_minutes: float
    affected_services: int
    affected_users: int
    customer_impact: float
    dependency_failures: int
    recurrence_count: int
    days_since_last_occurrence: int
    remediation_verified: bool
    symptoms: list[str] = field(default_factory=list)
    evidence: list[Evidence] = field(default_factory=list)
    changes: list[ChangeEvent] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass(frozen=True)
class EvidenceItem:
    kind: str
    text: str
    weight: float

@dataclass(frozen=True)
class HistoryMatch:
    incident_id: str
    score: float

@dataclass(frozen=True)
class AnalysisResult:
    incident_id: str
    priority: str
    risk_score: float
    impact_score: float
    blast_radius: float
    rca_confidence: float
    rca_hypothesis: str
    recurrence_risk: float
    investigation_quality: float
    known_pattern: bool
    change_correlation: float
    recommendations: tuple[str, ...]
    history_matches: tuple[HistoryMatch, ...]
    evidence_gaps: tuple[str, ...]
    report: str
