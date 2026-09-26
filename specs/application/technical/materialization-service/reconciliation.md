## Product and Geography Reconciliation

The harmonized foundation (`specs/application/technical/data-model.md § Core Data Model § Harmonized quantitative foundation`) lands two independently-sourced views of the market, the competitor's syndicated data and Brand A's own internal data, and neither the forecast, the price gap, nor the simulated outcomes mean anything until the two are reconciled to a common product and geography reference. Product matching is the following Algorithm.

| Step | Action |
|---|---|
| 1 | Attempt structured attribute matching between the competitor's product and Brand A's catalog (category, pack size, unit count, formulation, wherever both sources report comparable attributes) |
| 2 | If step 1 finds a match, set match_method to structured attribute matching and record its confidence, go to step 4 |
| 3 | If step 1 finds no match, attempt semantic matching as a fallback; set match_method to semantic matching and record its confidence |
| 4 | If match_confidence falls below the review threshold, flag the match for review rather than accepting it silently, the same governance discipline the business glossary (`specs/application/technical/glossary-and-grounding.md § Guaranteed grounding`) applies to an unresolvable term |
| 5 | If neither pass finds a match, record the competitor product as a whitespace signal, not an error |

A whitespace signal is kept rather than silently dropped or forced into a false match, though deciding what Brand A should add to its own lineup is an assortment decision outside what this system answers. Each match is recorded as a Product and Geography Match (`specs/application/technical/data-model.md § Core Data Model § Pipeline and Answer Artifacts § Product and Geography Match`).

`specs/application/technical/architecture.md § Architecture Overview § Diagrams § From Evidence to Answer` renders this.

### Geography normalization

Geography normalization solves the equivalent problem on geography, mapping each source's own regional codes onto a shared hierarchy. This is what actually sets the materialized grid's geography ceiling (`specs/application/technical/materialization-service/forecast-materialization.md § Forecast materialization`), more precisely than the competitor data's raw reporting granularity alone: the ceiling is the coarser of what the competitor data reports and how finely that reporting can be reliably normalized against Brand A's own geography. That ceiling is a statement about which data sources are currently ingested, not a fixed architectural limit: a store-level scanner panel, a geo-tagged competitive price-scraping service, or a retailer-specific POS feed would each lower it, if licensed and ingested. What cannot go below the ceiling is any claim of a grounded, sourced number, an allocation is the honest answer until better data closes that gap, not a wall this architecture imposes on its own.

### Currency normalization

Once a price observation's geography is resolved by geography normalization above, its own reported currency, a property of the feed itself, not something this pipeline assigns, is checked against that geography's own resolved currency (`specs/application/technical/data-model.md § Core Data Model § Reference and Master Data § Geography`); a mismatch is converted using the exchange rate captured in the same Data Vintage (`specs/application/technical/data-model.md § Core Data Model § Reference and Master Data § Data Vintage`) the observation itself was ingested under, the same versioning discipline already applied to every other macroeconomic indicator in the harmonized foundation, so re-computing against an unchanged vintage always uses the same rate, never today's, the same reproducibility discipline Realized Outcome's own `realized_data_vintage_id` (`specs/application/technical/data-model.md § Core Data Model § Pipeline and Answer Artifacts § Realized Outcome`) already applies to a comparably dated fact. This is the mechanism behind `specs/application/product/answer-engine/position.md § Position — where Brand A should sit`'s promise that a price gap is always in the geography's own local currency. Currency normalization happens exactly once, here, immediately after the geography it depends on is known, never before it and never again afterward.

`specs/application/technical/architecture.md § Architecture Overview § Diagrams § From Evidence to Answer` renders this.
