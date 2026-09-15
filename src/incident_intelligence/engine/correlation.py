from ..config.policy import ScoringPolicy

def change_correlation(i, policy: ScoringPolicy):
    relevant = [c for c in i.changes if 0 <= c.minutes_before_incident <= policy.change_window_minutes and c.service.casefold() == i.service.casefold()]
    if not relevant:
        return 0.0, "NO_RECENT_SERVICE_CHANGE", None
    best = max(relevant, key=lambda c: (c.risk_level.casefold() == "high", -c.minutes_before_incident))
    proximity = max(0.0, 1 - best.minutes_before_incident / policy.change_window_minutes)
    risk = {"low": .55, "medium": .75, "high": .95}.get(best.risk_level.casefold(), .65)
    score = round((proximity * .45 + risk * .55) * 100, 2)
    note = f"{best.change_type.upper()} {best.change_id} is temporally associated with onset; correlation is not proof of causation"
    return score, note, best
