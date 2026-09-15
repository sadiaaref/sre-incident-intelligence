from ..config.policy import ScoringPolicy
from ..domain.models import AnalysisResult, HistoryMatch
from ..domain.validation import validate_incident
from .scoring import impact_score, blast_radius, risk_score
from .correlation import change_correlation
from .rules import rank_hypotheses
from .recurrence import recurrence_risk
from .quality import investigation_quality, evidence_gaps
from .remediation import recommendations
from .similarity import similarity
from .timeline import timeline

class IncidentAnalyzer:
    """Deterministic, explainable incident triage and investigation engine."""
    def __init__(self, history=(), policy: ScoringPolicy | None = None):
        self.history = tuple(history)
        self.policy = policy or ScoringPolicy()

    def analyze(self, incident):
        errors = validate_incident(incident)
        if errors:
            raise ValueError("; ".join(errors))
        impact = impact_score(incident.error_rate, incident.duration_minutes, incident.affected_users, incident.customer_impact)
        blast = blast_radius(incident.affected_services, incident.dependency_failures)
        risk = risk_score(incident, impact, blast)
        change_score, change_note, _ = change_correlation(incident, self.policy)
        hypotheses = rank_hypotheses(incident, change_score)
        best = hypotheses[0]
        confidence = best.confidence
        hypothesis = best.name
        recurrence, recurrence_level = recurrence_risk(incident)
        quality = investigation_quality(incident, confidence, change_score)
        ranked = sorted(((similarity(incident, h), h.incident_id) for h in self.history if h.incident_id != incident.incident_id), reverse=True)[:self.policy.max_history_matches]
        matches = tuple(HistoryMatch(incident_id=hid, score=score) for score, hid in ranked)
        known = bool(matches and matches[0].score >= self.policy.known_pattern_threshold)
        recs = recommendations(incident, confidence, change_score)
        gaps = evidence_gaps(incident, confidence, change_score)
        priority_name = self.policy.priority(risk)
        report = self._report(incident, priority_name, risk, impact, blast, confidence, hypothesis, recurrence, recurrence_level, quality, known, change_score, change_note, recs, gaps, matches, timeline(incident), hypotheses)
        return AnalysisResult(incident.incident_id, priority_name, risk, impact, blast, confidence, hypothesis, recurrence, quality, known, change_score, recs, matches, gaps, report)

    @staticmethod
    def _report(i, priority, risk, impact, blast, confidence, hypothesis, recurrence, level, quality, known, change, note, recs, gaps, matches, events, hypotheses):
        lines = ["SRE INCIDENT INTELLIGENCE REPORT", "=" * 34, f"Incident: {i.title}", f"Service: {i.service}", f"Priority: {priority}", f"Risk: {risk}/100", f"Impact: {impact}/100", f"Blast radius: {blast}/100", f"Known pattern: {'YES' if known else 'NO'}", f"Investigation confidence: {confidence}%", f"Recurrence risk: {recurrence}/100 ({level})", f"Investigation quality: {quality}/100", f"Change correlation: {change}/100", "", f"Leading hypothesis: {hypothesis}", f"Change assessment: {note}", "", "Hypothesis ranking:"]
        lines += [f"- {h.name}: {h.confidence}/100 | {', '.join(h.evidence) if h.evidence else 'limited evidence'}" for h in hypotheses]
        if matches:
            lines += ["", "Historical matches:"] + [f"- {m.incident_id}: {m.score}/100" for m in matches]
        lines += ["", "Recommended actions:"] + ([f"- {r}" for r in recs] if recs else ["- Continue evidence collection"])
        if gaps: lines += ["", "Evidence gaps:"] + [f"- {g}" for g in gaps]
        if events: lines += ["", "Timeline signals:"] + [f"- {e}" for e in events]
        return "\n".join(lines)
