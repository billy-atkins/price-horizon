## Product and Geography Reconciliation

Match the syndicated product to Brand A's catalog. Both matchers inspect the same product and catalog from the reconciliation run. The structured matcher uses category, pack size, unit count and formulation where both sources supply them. The semantic matcher uses product names and records the model version. Each returns the selected catalog identifier and confidence, or null when it finds no candidate.

**Construct:** `specs/methodology/modeling-constructs.md § Constructs § Algorithm` \
**Inputs:**
  - competitor product
  - brand catalog
  - review threshold

**Output:**
  - product match

**Runs When:**
  - the reconciliation service matches a competitor product from an incoming data vintage against Brand A's catalog

| Step | Action |
|---|---|
| 1 | Set candidate to structured match(competitor product, brand catalog) |
| 2 | If candidate != null, Set method to "structured attribute matching", Go to step 5; otherwise, continue |
| 3 | Set candidate to semantic match(competitor product, brand catalog) |
| 4 | If candidate = null, Set product match to {competitor: competitor product.id, brand: null, method: null, matcher version: null, confidence: null, status: "whitespace"}, Go to step 6; otherwise, Set method to "semantic matching" |
| 5 | Set product match to {competitor: competitor product.id, brand: candidate.id, method: method, matcher version: if method = "semantic matching" then candidate.matcher version else null, confidence: candidate.confidence, status: if candidate.confidence < review threshold then "flagged" else "accepted"} |
| 6 | Persist the result for this product and vintage. End |

The disposition of a comparison awaiting review follows [`§ Open Questions [Name: Flagged Matches]`](#open-questions). A whitespace result retains the competitor product even though it has no Brand A counterpart. Independently grounded prices remain available in either case. Assortment decisions remain outside the product scope. Each match is recorded as a Product and Geography Match ([`specs/application/technical/data-model.md § Core Data Model § Pipeline and Answer Artifacts § Product and Geography Match`](/specs/application/technical/data-model.md#product-and-geography-match)).

[`specs/application/technical/architecture.md § Architecture Overview § Diagrams § From Evidence to Answer`](/specs/application/technical/architecture.md#from-evidence-to-answer) renders this.

### Geography normalization

Geography normalization solves the equivalent problem for geography. It maps each source's own regional codes onto a shared hierarchy. Geography normalization, not the competitor data's raw reporting granularity alone, sets the materialized grid's geography ceiling ([`specs/application/technical/materialization-service/forecast-materialization.md § Forecast materialization`](/specs/application/technical/materialization-service/forecast-materialization.md#forecast-materialization)). The ceiling is the coarser of what the competitor data reports and how finely that reporting can be reliably normalized against Brand A's own geography.

The ceiling follows the licensed sources and the reliability of their alignment. Finer data can extend it. Below it, the answer identifies a qualified estimate, a parent reference or unavailability as specified in [`specs/application/technical/query-service/layered-output-synthesis.md § Layered Output Synthesis (producing the answer) § Drill-down mechanics`](/specs/application/technical/query-service/layered-output-synthesis.md#drill-down-mechanics).

### Source geography review

During ingestion resolve the source observation at its reported level under [`specs/application/technical/data-model.md § Core Data Model § Reference and Master Data § Entity Alias`](/specs/application/technical/data-model.md#entity-alias). A unique, reliable mapping supports that level. An unknown or ambiguous mapping enters the observation's unit review queue. A request below the source's reported coverage follows the drill-down rule and creates no review item. An independently grounded parent can still support comparisons at the parent level.

**Construct:** `specs/methodology/modeling-constructs.md § Constructs § Decision Table` \
**Conditions:** Reliable mapping at reported level?, Review disposition \
**Input Values:**
  - Review disposition: "new", "open", "dismissed"

| Reliable mapping at reported level? | Review disposition | Comparison at this level | Review action |
|---|---|---|---|
| true | - | Eligible when the other required inputs exist | Use the reliable mapping |
| false | "new" | Unavailable | Flag the affected source record once in its unit |
| false | "open" | Unavailable | Keep the existing item |
| false | "dismissed" | Unavailable | Keep the decision for this evidence |

Key a geography review item by unit, source, code, source observation identifier and vintage. Concurrent deliveries or retries of the same evidence reuse that item. A reviewer can confirm a reliable mapping or register a correction under the scoped registration rule. Resolve the item only when the mapping succeeds. A conflicting correction leaves the original mapping and the open item intact. Dismissal keeps this evidence unused at the unresolved level. Future eligible computations use a successful resolution when they next read the evidence. A published result changes only on subsequent publication, and earlier deliveries retain their original geography.

### Currency normalization

Once geography normalization resolves a price observation's geography, the observation's reported currency is checked against that geography's resolved currency ([`specs/application/technical/data-model.md § Core Data Model § Reference and Master Data § Geography`](/specs/application/technical/data-model.md#geography)). The reported currency is a property of the feed itself, not something this pipeline assigns. A mismatch is converted using the exchange rate captured in the same Data Vintage ([`specs/application/technical/data-model.md § Core Data Model § Reference and Master Data § Data Vintage`](/specs/application/technical/data-model.md#data-vintage)) the observation was ingested under. That is the same versioning discipline already applied to every other macroeconomic indicator in the harmonized foundation, so re-computing against an unchanged vintage always uses the same rate, never today's. Realized Outcome's `realized_data_vintage_id` ([`specs/application/technical/data-model.md § Core Data Model § Pipeline and Answer Artifacts § Realized Outcome`](/specs/application/technical/data-model.md#realized-outcome)) already applies the same reproducibility discipline to a comparably dated fact. This is the mechanism behind [`specs/application/product/answer-engine/position.md § Position: where Brand A should sit`](/specs/application/product/answer-engine/position.md#position-where-brand-a-should-sit)'s promise that a price gap is always in the geography's own local currency. Currency normalization happens exactly once, here, immediately after the geography it depends on is known, never before it and never again afterward.

A normalized observation retains its source reference and data vintage. A forecast using it links to that observation so the original ingestion work can be traced during operational retention. Reuse at another horizon leaves that evidence intact.

[`specs/application/technical/architecture.md § Architecture Overview § Diagrams § From Evidence to Answer`](/specs/application/technical/architecture.md#from-evidence-to-answer) renders this.

## Facts

**Records:**
  - **Name:** competitor product \
    **Type:** context \
    **Means:** the source product, its stable identifier, name and reported attributes in this data vintage

  - **Name:** brand catalog \
    **Type:** list<context> \
    **Means:** the unit's Brand A products with stable identifiers, names and available attributes at that vintage

  - **Name:** review threshold \
    **Type:** number \
    **Means:** the minimum candidate confidence for automatic acceptance

  - **Name:** candidate \
    **Type:** context<id: string, confidence: number, matcher version: string> \
    **May Be Absent:** Yes \
    **Means:** the chosen catalog product and confidence returned by the matcher, absent on a miss

  - **Name:** method \
    **Type:** string \
    **Means:** the matcher that produced the selected catalog candidate

  - **Name:** product match \
    **Type:** context<competitor: string, brand: string, method: string, matcher version: string, confidence: number, status: string> \
    **Means:** the persisted disposition of the source product and the candidate evidence when one exists

  - **Name:** structured match \
    **Type:** function<context, list<context>> -> context \
    **Means:** the reconciliation service's candidate and confidence from comparable structured attributes, or null when no candidate is found

  - **Name:** semantic match \
    **Type:** function<context, list<context>> -> context \
    **Means:** the registered semantic matcher's candidate, confidence and actual invoked registry version from product names, or null when no candidate is found

## Open Questions

**Records:**
  - **Name:** Flagged Matches \
    **Open Question:** What does a match flagged for review ([`§ Product and Geography Reconciliation [Step: 5]`](#product-and-geography-reconciliation)) do to a price gap or comparison before a reviewer resolves it? What catches a match that is wrong but scored as confident? \
    **Provisional Answer:** A flagged match is held back from every price gap, relative price index and comparison until a reviewer resolves it. The comparison is shown as unavailable rather than computed on the flagged match. Nothing catches a wrong match scored as confident. \
    **Impacts:** the flag [`§ Product and Geography Reconciliation [Step: 5]`](#product-and-geography-reconciliation) sets; the price gap and relative price index ([`specs/application/technical/query-service/layered-output-synthesis.md § Layered Output Synthesis (producing the answer) § Price gap and relative price index, defined`](/specs/application/technical/query-service/layered-output-synthesis.md#price-gap-and-relative-price-index-defined)); and the review queue a flagged match goes to ([`specs/application/product/tenant-administration/review-queues.md § Review Queues`](/specs/application/product/tenant-administration/review-queues.md#review-queues)).
