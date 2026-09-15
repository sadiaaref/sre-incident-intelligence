# Engineering Decisions

### Why deterministic scoring instead of an opaque ML model?
Incident response needs an explanation an engineer can challenge during an outage. The current model exposes its inputs and weights, so a team can tune policy and reproduce the result.

### Why separate impact from risk?
Customer impact and operational risk are related but not identical. Keeping them separate makes the final decision easier to inspect and prevents a single score from hiding important context.

### Why label deployment correlation carefully?
A deployment close to incident onset is useful evidence, but temporal proximity alone does not establish causation. The engine therefore reports correlation and combines it with dependency and evidence signals.

### Why return evidence gaps?
A useful incident assistant should identify what is still unknown, not only produce a score. Gaps turn uncertainty into concrete investigation work.
