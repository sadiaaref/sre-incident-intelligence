from src.incident_intelligence.engine.telemetry import detect_anomalies


def test_detects_metric_spike_against_baseline():
    anomalies = detect_anomalies({"error_rate": [2, 2, 3, 12]})
    assert anomalies[0].metric == "error_rate"
    assert anomalies[0].deviation_pct > 50
    assert anomalies[0].severity == "HIGH"


def test_ignores_stable_metric():
    assert detect_anomalies({"latency": [100, 101, 99, 102]}) == ()


def test_handles_zero_baseline():
    anomalies = detect_anomalies({"errors": [0, 0, 0, 4]})
    assert anomalies[0].deviation_pct == 100


def test_requires_enough_samples():
    assert detect_anomalies({"errors": [1, 10]}) == ()
