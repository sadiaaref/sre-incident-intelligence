def timeline(i):
    events=[]
    for c in i.changes:
        events.append((c.minutes_before_incident, f"change {c.change_id} ({c.change_type})"))
    for e in i.evidence:
        if e.observed_at:
            events.append((0, f"evidence: {e.signal}"))
    return tuple(text for _, text in sorted(events, key=lambda x: x[0], reverse=True))
