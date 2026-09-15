from .models import Incident

def validate_incident(i: Incident) -> list[str]:
    errors: list[str] = []
    if not i.incident_id.strip(): errors.append("incident_id is required")
    if not i.title.strip(): errors.append("title is required")
    if not i.service.strip(): errors.append("service is required")
    if not 1 <= i.severity <= 10: errors.append("severity must be 1..10")
    if not 1 <= i.urgency <= 10: errors.append("urgency must be 1..10")
    if not 0 <= i.error_rate <= 100: errors.append("error_rate must be 0..100")
    if i.duration_minutes < 0: errors.append("duration_minutes cannot be negative")
    if i.affected_services < 0 or i.affected_users < 0: errors.append("impact counts cannot be negative")
    if not 0 <= i.customer_impact <= 100: errors.append("customer_impact must be 0..100")
    if i.dependency_failures < 0 or i.recurrence_count < 0: errors.append("counts cannot be negative")
    if i.days_since_last_occurrence < 0: errors.append("days_since_last_occurrence cannot be negative")
    for e in i.evidence:
        if not 0 <= e.strength <= 1: errors.append(f"evidence strength must be 0..1: {e.signal}")
    return errors
