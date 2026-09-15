def evidence_gaps(i, rca_confidence, change_score):
    gaps=[]
    if len(i.evidence) < 3: gaps.append("collect at least three independent evidence signals")
    if not any(e.observed_at for e in i.evidence): gaps.append("attach timestamps to evidence for timeline reconstruction")
    if not i.changes: gaps.append("check recent deployments/configuration changes")
    if not i.dependency_failures: gaps.append("verify dependency health before attributing root cause")
    if not i.remediation_verified: gaps.append("define and execute post-remediation verification")
    if rca_confidence < 60: gaps.append("avoid declaring RCA until evidence confidence improves")
    return tuple(dict.fromkeys(gaps))

def investigation_quality(i, rca_confidence, change_score):
    evidence = min(30, len(i.evidence) * 8)
    timestamps = 15 if any(e.observed_at for e in i.evidence) else 5
    change = 20 if change_score else 0
    hypothesis = 20 if i.dependency_failures or i.changes else 8
    verification = 15 if i.remediation_verified else 5
    return round(min(100, evidence + timestamps + change + hypothesis + verification + rca_confidence*.15), 2)
