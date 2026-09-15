def recommendations(i, rca_confidence, change_score):
    actions=[]
    if change_score >= 60: actions.append("Confirm blast radius, then pause or roll back the correlated change")
    if i.dependency_failures: actions.append("Validate dependency health, saturation and error-budget impact")
    if i.error_rate >= 20: actions.append("Reduce customer impact with a reversible traffic-control or rollback action")
    if not i.remediation_verified: actions.append("Verify remediation using error-rate, latency and dependency checks")
    if rca_confidence < 60: actions.append("Collect additional logs, traces and deployment evidence before declaring RCA")
    return tuple(dict.fromkeys(actions))
