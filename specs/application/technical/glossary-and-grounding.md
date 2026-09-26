## Guaranteed grounding

A governed business glossary maps natural language phrasing (Competitor Brand, Brand A, effective price, price gap, relative price index, category growth) directly to trusted schema fields and callable model endpoints. This is the single most important design decision in the whole system: the language model is never allowed to compute a number itself. It orchestrates calls to versioned quantitative models and cites retrieved facts. If a term in the question cannot be resolved against the glossary, the system asks a clarifying question rather than guessing. This is what programmatically prevents hallucination, not a prompt instruction, an architectural constraint.

`specs/application/technical/architecture.md § Architecture Overview § Diagrams § Layer Composition` renders this.

## Effective price, defined

Not list or shelf price, the net price actually realized: list price minus trade promotion depth and rebates, plus any surcharges, per unit, over a stated time window. This is the metric Predict actually forecasts, defined for a business reader in `specs/application/product/answer-engine/predict.md § Predict — what will the competitor do`. List price and promotional depth move on entirely different cadences, list price rarely and deliberately, promotional depth tactically and often, so a competitor's effective price can swing month to month while list price sits still for a year. The harmonized foundation carries both components separately, list price series and promotional depth series, rather than only the blended effective price, because the forecasting mechanism in `specs/application/technical/predict-computation.md § Predict Computation § Effective price forecasting` needs to reason about each on its own terms.
