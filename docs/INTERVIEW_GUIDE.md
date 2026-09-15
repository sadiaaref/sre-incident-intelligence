# Interview Guide

Be able to explain these five flows without reading the code:

1. How an incident is validated and normalized.
2. How impact, blast radius and risk differ.
3. How change correlation is calculated and why it is not proof of causation.
4. How historical similarity is ranked and converted into a known-pattern signal.
5. How evidence gaps and remediation verification prevent premature RCA closure.

### Honest production discussion

The current repository is a deterministic engine, not a complete distributed production service. A production architecture would add an HTTP boundary, durable storage, asynchronous event ingestion, authentication, telemetry and operational deployment. Being explicit about this trade-off is stronger in an interview than overstating the implementation.
