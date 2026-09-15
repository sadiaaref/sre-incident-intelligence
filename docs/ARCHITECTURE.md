# Architecture

```text
                 +----------------------+
                 | JSON / future events |
                 +----------+-----------+
                            |
                       Validation
                            |
                    Normalization
                            |
        +-------------------+-------------------+
        |                   |                   |
     Impact/Risk        History             Changes
        |              Similarity         Correlation
        +-------------------+-------------------+
                            |
                     Evidence-weighted RCA
                            |
                  Recurrence + Quality
                            |
                   Remediation Gates
                            |
                 Operator / JSON Report
```

## Engineering decisions

- **Pure domain models:** no web framework or database dependency in the core analysis path.
- **Bounded scoring:** every operational score is normalized to 0–100 so downstream systems can reason about it consistently.
- **Evidence vs. hypothesis:** the RCA module reports confidence and labels temporal change correlation as correlation rather than proof.
- **History as an interface:** the engine accepts any iterable of historical incidents; `IncidentHistory` is a reference repository implementation.
- **Policy injection:** thresholds and time windows live in `ScoringPolicy`, avoiding hard-coded operational policy in orchestration.
- **Verification gates:** remediation suggestions include explicit post-change verification rather than assuming the incident is fixed.
- **Deterministic by design:** identical input produces identical output, making regression testing and incident review reproducible.

## Production evolution

A production deployment would place the engine behind an API, persist incidents in PostgreSQL/object storage, consume alert/log/metric/trace events asynchronously, and add authentication, rate limiting, structured telemetry, and durable audit records. Those integrations are intentionally separated from the domain engine so they do not contaminate the analysis logic.
