def clamp(x: float) -> float:
    return max(0.0, min(100.0, x))

def impact_score(error_rate, duration, affected_users, customer_impact):
    user_component = min(100.0, affected_users / 10000 * 100)
    return round(clamp(error_rate * .35 + min(duration / 120 * 100, 100) * .20 + user_component * .20 + customer_impact * .25), 2)

def blast_radius(affected_services, dependency_failures):
    return round(clamp(affected_services * 12 + dependency_failures * 18), 2)

def risk_score(i, impact, blast):
    recurrence = min(i.recurrence_count * 10, 30)
    return round(clamp(i.severity * 5 + i.urgency * 4 + impact * .32 + blast * .14 + recurrence), 2)
