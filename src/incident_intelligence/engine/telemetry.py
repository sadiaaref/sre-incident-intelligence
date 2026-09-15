"""Small, dependency-free anomaly detection over metric samples."""
from dataclasses import dataclass

@dataclass(frozen=True)
class MetricAnomaly:
    metric: str
    latest: float
    baseline: float
    deviation_pct: float
    severity: str


def detect_anomalies(samples: dict[str, list[float]], deviation_threshold: float = 50.0) -> tuple[MetricAnomaly, ...]:
    """Compare the newest sample with the mean of preceding samples.

    This intentionally stays transparent: operators can inspect baseline and
    deviation instead of receiving an opaque anomaly score.
    """
    results = []
    for metric, values in samples.items():
        if len(values) < 3:
            continue
        baseline = sum(values[:-1]) / len(values[:-1])
        latest = values[-1]
        if baseline == 0:
            deviation = 100.0 if latest else 0.0
        else:
            deviation = abs(latest - baseline) / abs(baseline) * 100
        if deviation >= deviation_threshold:
            severity = "HIGH" if deviation >= deviation_threshold * 2 else "MEDIUM"
            results.append(MetricAnomaly(metric, latest, round(baseline, 4), round(deviation, 2), severity))
    return tuple(sorted(results, key=lambda x: x.deviation_pct, reverse=True))
