"""Explainable hypothesis and evidence rules.

The engine does not claim to prove root cause. It ranks hypotheses from explicit
signals so an engineer can challenge the conclusion and collect more evidence.
"""
from dataclasses import dataclass
from ..domain.models import Incident

@dataclass(frozen=True)
class Hypothesis:
    name: str
    confidence: float
    evidence: tuple[str, ...]
    rationale: str


def rank_hypotheses(i: Incident, change_score: float) -> tuple[Hypothesis, ...]:
    candidates: list[Hypothesis] = []
    dep = min(100.0, i.dependency_failures * 25.0)
    change = change_score
    customer = min(100.0, i.customer_impact)
    error = min(100.0, i.error_rate * 2.0)

    candidates.append(Hypothesis(
        "DEPENDENCY_DEGRADATION",
        round(min(100, dep * .55 + error * .20 + customer * .25), 2),
        tuple(["dependency failures"] if i.dependency_failures else []) + (("elevated error rate",) if i.error_rate >= 10 else ()),
        "Dependency failures are directly observed and can explain downstream errors." if i.dependency_failures else "No dependency failures were supplied, so this hypothesis has weak support.",
    ))
    candidates.append(Hypothesis(
        "RECENT_CHANGE",
        round(min(100, change * .70 + error * .15 + (25 if i.changes else 0) * .15), 2),
        tuple(f"change {c.change_id}" for c in i.changes[:3]),
        "A recent service-local change is temporally associated with the incident; correlation is not proof of causation." if i.changes else "No recent service-local change was supplied.",
    ))
    candidates.append(Hypothesis(
        "TRAFFIC_OR_CAPACITY",
        round(min(100, max(0, i.affected_users / 10000 * 100) * .45 + error * .35 + min(100, i.duration_minutes / 120 * 100) * .20), 2),
        tuple(["affected users"] if i.affected_users else []) + (("elevated error rate",) if i.error_rate >= 10 else ()),
        "User impact and sustained errors are consistent with a capacity or traffic pressure hypothesis, but telemetry is needed to confirm it.",
    ))
    return tuple(sorted(candidates, key=lambda h: h.confidence, reverse=True))
