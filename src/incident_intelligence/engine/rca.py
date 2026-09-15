def rca(i, change_score):
    if not i.evidence:
        return 10.0, f"{i.service} failure pattern requires additional evidence before causal attribution"
    evidence_strength = min(100.0, sum(e.strength for e in i.evidence) / len(i.evidence) * 100)
    consistency = min(100.0, len(i.evidence) * 30)
    confidence = round(evidence_strength*.45 + consistency*.25 + change_score*.30, 2)
    if i.dependency_failures and change_score >= 60:
        hypothesis = f"Recent change is the leading contributor to {i.service} dependency failures"
    elif i.dependency_failures:
        hypothesis = f"Dependency degradation is the leading hypothesis for {i.service}"
    else:
        hypothesis = f"{i.service} failure pattern requires additional evidence before causal attribution"
    return confidence, hypothesis
