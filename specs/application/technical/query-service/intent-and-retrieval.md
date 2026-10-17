## Dynamic Retrieval and Weighting (when the question is asked)

This is the part of the live path that only the query service runs: handling an incoming question and fanning out its retrieval calls. Everything downstream of intent resolution (forecasting, triangulation, driver attribution, and confidence packaging) is shared with the materialization service and lives in [`specs/application/technical/predict-computation.md § Predict Computation`](/specs/application/technical/predict-computation.md#predict-computation). It lives there because the materialization service's batch path runs the identical computation without ever parsing a question or constructing a Question Intent. The batch path iterates a configured grid instead.

### Intent parsing and decoupling

The incoming question is parsed into a Question Intent ([`specs/application/technical/data-model.md § Core Data Model § Pipeline and Answer Artifacts § Question Intent`](/specs/application/technical/data-model.md#question-intent)): business unit, metric (price), entities (Competitor Brand, Brand A), geography (Texas), horizon (6 months), implied granularity, and decision type (the session's, strategic). Business unit is resolved first, because which glossary and competitor set apply depends on it ([`§ Dynamic Retrieval and Weighting (when the question is asked) § Intent parsing and decoupling § Business unit`](#business-unit)). Decision type is resolved last ([`§ Dynamic Retrieval and Weighting (when the question is asked) § Intent parsing and decoupling § Decision type`](#decision-type)).

Once its business unit is resolved, the rest of the plan is validated against that business unit's glossary before anything executes. An unresolvable entity stops the pipeline and asks for clarification instead of proceeding on a guess. Resolving the business unit follows the same rule.

The business units the user's IdP-asserted access contains are not merely used to guess intent. They also bound every retrieval this query makes, which is filtered to the business units the IdP granted. A clarification prompt can never reveal a business unit outside that set. Someone with access to one business unit is never told a second one exists only because the installation happens to host it.

[`specs/application/technical/architecture.md § Architecture Overview § Diagrams § Trust Boundaries`](/specs/application/technical/architecture.md#trust-boundaries) and [`specs/application/technical/architecture.md § Architecture Overview § Diagrams § The Answer`](/specs/application/technical/architecture.md#the-answer) render this.

#### Business unit

A Decision Table resolves business unit from the access the user's IdP asserts ([`specs/application/technical/identity-and-access.md § Business unit access, federated`](/specs/application/technical/identity-and-access.md#business-unit-access-federated)), asking its questions in turn. `Business units granted` is how many business units the user's IdP-asserted access contains. `Resolves against one glossary?` reads true where a brand or competitor in the question resolves uniquely against one business unit's glossary, and false where it resolves against more than one or against none. `Session business unit granted?` reads true where the request carries a session business unit ([`§ Dynamic Retrieval and Weighting (when the question is asked) § Session context`](#session-context)) that the IdP-asserted access includes. The table's outcome is the query's business unit, `denied` or `unsettled`. `denied` means no claim mapping grants this identity access to any business unit, and the query is denied. `unsettled` means the pipeline stops and asks for clarification.

**Construct:** `specs/methodology/modeling-constructs.md § Constructs § Decision Table`

**Hit Policy:** First

**Conditions:** Business units granted, Resolves against one glossary?, Session business unit granted?

| Name | Business units granted | Resolves against one glossary? | Session business unit granted? | Business unit |
|---|---|---|---|---|
| No Business Unit | 0 | - | - | denied |
| One Business Unit | 1 | - | - | the one business unit granted |
| Glossary | - | true | - | the business unit whose glossary the brand or competitor resolves against |
| Session | - | - | true | the session's business unit |
| Unsettled | - | - | - | unsettled |

#### Decision type

Decision type is settled once the plan is validated, as [`specs/application/product/answer-engine/decision-context.md § Decision Context`](/specs/application/product/answer-engine/decision-context.md#decision-context) promises, because the positioning engine seeds its candidates by it ([`specs/application/technical/query-service/layered-output-synthesis.md § Layered Output Synthesis (producing the answer) § Positioning engine § Seeding`](/specs/application/technical/query-service/layered-output-synthesis.md#seeding)). `A kind of decision for this question alone?` reads Yes where the request carries one, which is the answer to an earlier clarification about it. A cue is one of a fixed set of decision words, held here and never extended by a business unit: "promotion", "promo", "retailer" and "retail account" for tactical; "list price", "price position", "brand-wide" and "national price" for strategic. A cue counts in any grammatical form: "promotional" or "promotions" as well as "promotion". A cue counts only where it describes Brand A's own decision, never the competitor's price. Intent parsing tells the two apart by what the word refers to in the question. Neither a retailer's name nor a time the question gives for its forecast, its horizon, is ever a cue. A decision word is never itself an unresolved term needing clarification. `A tactical cue?` reads Yes where any tactical cue counts, and `A strategic cue?` where any strategic cue does.

**Construct:** `specs/methodology/modeling-constructs.md § Constructs § Decision Table`

**Conditions:** A kind of decision for this question alone?, A tactical cue?, A strategic cue?, A session kind of decision?

| A kind of decision for this question alone? | A tactical cue? | A strategic cue? | A session kind of decision? | Decision type |
|---|---|---|---|---|
| Yes | - | - | - | The kind of decision the request carries for this question alone |
| No | Yes | No | - | Tactical, for this question only |
| No | No | Yes | - | Strategic, for this question only |
| No | No | No | Yes | The session's kind of decision, which the request carries ([`§ Dynamic Retrieval and Weighting (when the question is asked) § Session context`](#session-context)) |
| No | No | No | No | Stop the pipeline and ask for clarification |
| No | Yes | Yes | - | Stop the pipeline and ask for clarification |

### Session context

A question request carries the session's business unit and kind of decision, where set. After a clarification about a question that used decision words of both kinds, the request also carries the kind of decision chosen for that question alone. The app keeps a Query user's session choices from sign-in to sign-out, as [`specs/application/product/answer-engine/decision-context.md § Decision Context`](/specs/application/product/answer-engine/decision-context.md#decision-context) describes. The app sends them with each question and changes them only when the Query user does. An API caller sends them itself. A clarifying question names what it asks for, so the app knows what to keep. A clarifying question asked because the request carried no business unit or kind of decision is answered as a session choice, which the app keeps. One asked because the question used both kinds is answered for that question alone. Either way, the app resends the original question with the answer, and nothing was computed before it. Every answer returns the business unit and kind of decision it was given for, which is what the app shows.

### Parallel evidence retrieval

The Question Intent fans out into simultaneous, independent retrieval tasks:

- call the elasticity model and the list-price and promotional-depth forecast components described in [`specs/application/technical/predict-computation.md § Predict Computation § Effective price forecasting`](/specs/application/technical/predict-computation.md#effective-price-forecasting)
- pull the competitor's historical effective price series
- run a filtered vector search of the qualitative corpus scoped to Texas and the relevant time window (tax changes, macro commentary, known competitor plans)
- retrieve Brand A's current price and margin targets

These tasks run in parallel because they are independent. Running them in parallel is what keeps a multi-source answer fast.

[`specs/application/technical/architecture.md § Architecture Overview § Diagrams § Layer Composition`](/specs/application/technical/architecture.md#layer-composition) renders this.
