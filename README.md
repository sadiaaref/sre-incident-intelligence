# SRE Incident Intelligence Engine

An explainable incident triage and investigation-assistance engine. It does **not** automatically fix production systems. Its job is to turn structured incident signals into a ranked, auditable investigation view for engineers.

## What is implemented

- Multi-factor risk, customer-impact and blast-radius scoring
- Explainable hypothesis ranking across dependency, recent-change, and traffic/capacity signals
- Recent deployment/change correlation with an explicit correlation-vs-causation warning
- Historical incident similarity with normalized token fingerprints
- Recurrence-risk scoring and investigation-quality assessment
- Evidence-gap detection and investigation recommendations
- Lightweight metric anomaly detection from time-series samples
- In-memory and durable SQLite incident-history adapters
- Dependency-free HTTP API with `/health` and `/analyze`, payload validation, and size limits
- CLI with human-readable and JSON output
- Unit and HTTP integration tests
- GitHub Actions CI across multiple Python versions
- Docker image for local API execution

## Architecture

```text
                    +-----------------------+
                    | CLI / HTTP adapters   |
                    +-----------+-----------+
                                |
                                v
                    +-----------------------+
                    | IncidentAnalyzer       |
                    +-----------+-----------+
                                |
          +---------------------+----------------------+
          |          |           |         |            |
          v          v           v         v            v
       Scoring   Correlation   Rules   Similarity   Recurrence
          |          |           |         |            |
          +----------+-----------+---------+------------+
                                |
                                v
                    +-----------------------+
                    | AnalysisResult/report |
                    +-----------------------+
                                ^
                                |
                 +--------------+--------------+
                 |                             |
          In-memory history             SQLite history
```

The core engine is deterministic and intentionally explainable. It consumes already-structured incident signals rather than pretending to ingest raw logs, traces, or a production observability platform.

## Quick start

```powershell
python -m pytest -v
python -m src.incident_intelligence examples/payment_incident.json
python -m src.incident_intelligence examples/payment_incident.json --json
```

Run the API:

```powershell
python -m incident_intelligence.api
```

Then `GET /health` or `POST /analyze` with the example incident JSON.

## Engineering focus

The project demonstrates ports/adapters-style separation, dependency injection, immutable result models, deterministic scoring, persistence abstraction, HTTP integration testing, and CI. The system is intentionally decision support: a human engineer remains responsible for diagnosis and remediation.
