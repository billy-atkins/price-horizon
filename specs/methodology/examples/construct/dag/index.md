# Spec of Record: DAGs, Worked Examples

**Reference Key:** File

**Required:** Description

| File | Description |
|---|---|
| `nightly-pricing.md` | A nightly pricing run. Two extracts are free at once. A check of the margins they give has a timeout. A person makes a review only where a margin is flagged. A load waits for the check and the review. A report runs however the load ended, and the run tolerates the report's own failure |
