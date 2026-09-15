def recurrence_risk(i):
    frequency = min(i.recurrence_count / 5 * 45, 45)
    freshness = max(0, 30 - i.days_since_last_occurrence) if i.recurrence_count else 0
    unverified = 25 if not i.remediation_verified else 0
    score = round(min(100, frequency + freshness + unverified), 2)
    level = "HIGH" if score >= 70 else "MEDIUM" if score >= 40 else "LOW"
    return score, level
