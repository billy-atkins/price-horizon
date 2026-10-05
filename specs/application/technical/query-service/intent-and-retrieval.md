## Dynamic Retrieval and Weighting (when the question is asked)

The genuinely query-service-only part of the live path: handling an incoming question and fanning out its retrieval calls. Everything downstream of intent resolution, forecasting, triangulation, driver attribution, and confidence packaging, is shared with the materialization service and lives in `specs/application/technical/predict-computation.md § Predict Computation`, since the materialization service's batch path runs the identical computation without ever parsing a question or constructing a Question Intent, it iterates a configured grid instead.

### Intent parsing and decoupling

The incoming question is parsed into a Question Intent (`specs/application/technical/data-model.md § Core Data Model § Pipeline and Answer Artifacts § Question Intent`): business unit, metric (price), entities (Competitor Brand, Brand A), geography (Texas), horizon (6 months), implied granularity, and decision type (the session's, strategic). Business unit is resolved first, since which glossary and competitor set apply depends on it (`§ Dynamic Retrieval and Weighting (when the question is asked) § Intent parsing and decoupling § Business unit`), and decision type last (`§ Dynamic Retrieval and Weighting (when the question is asked) § Intent parsing and decoupling § Decision type`).

Once its business unit is resolved, the rest of the plan is validated against that business unit's glossary before anything executes. An unresolvable entity stops the pipeline and asks for clarification instead of proceeding on a guess, the same rule business unit's own resolution applies.

The business units the user's IdP-asserted access contains also bound every retrieval this query makes, filtered to business units the IdP actually granted, not merely used to guess intent, and a clarification prompt can never reveal a business unit outside that set, someone with access to one business unit is never told a second one exists just because the installation happens to host it.

`specs/application/technical/architecture.md § Architecture Overview § Diagrams § Trust Boundaries` and `specs/application/technical/architecture.md § Architecture Overview § Diagrams § The Answer` render this.

#### Business unit

Business unit is resolved from the access the user's IdP asserts (`specs/application/technical/identity-and-access.md § Business unit access, federated`), by a Decision Tree:

**Construct:** Decision Tree

| Step | Question | Answer | Result |
|---|---|---|---|
| 1.1 | How many business units does the user's IdP-asserted access contain? | None | Deny the query; no claim mapping grants this identity access to any business unit |
| 1.2 | | Exactly one | Use it as the query's business unit |
| 1.3 | | More than one | Go to step 2 |
| 2.1 | Does a brand or competitor in the question resolve uniquely against one business unit's glossary? | Yes | Use that business unit |
| 2.2 | | No, it resolves against more than one or against none | Go to step 3 |
| 3.1 | Does the request carry a session business unit (`§ Dynamic Retrieval and Weighting (when the question is asked) § Session context`) that the IdP-asserted access includes? | Yes | Use the session's business unit |
| 3.2 | | No | Stop the pipeline and ask for clarification |

#### Decision type

Decision type is settled once the plan is validated, as `specs/application/product/answer-engine/decision-context.md § Decision Context` promises, since the positioning engine seeds its candidates by it (`specs/application/technical/query-service/layered-output-synthesis.md § Layered Output Synthesis (producing the answer) § Positioning engine § Seeding`). `A kind of decision for this question alone?` reads Yes where the request carries one, the answer to an earlier clarification about it. A cue is one of a fixed set of decision words, held here and never extended by a business unit: "promotion", "promo", "retailer" and "retail account" for tactical; "list price", "price position", "brand-wide" and "national price" for strategic. A cue counts in any grammatical form, "promotional" or "promotions" as well as "promotion", and only where it describes Brand A's own decision, never the competitor's price, which intent parsing tells apart by what the word refers to in the question. Neither a retailer's name nor a time the question gives for its forecast, its horizon, is ever a cue, and a decision word is never itself an unresolved term needing clarification. `A tactical cue?` reads Yes where any tactical cue counts, and `A strategic cue?` where any strategic cue does.

**Construct:** Decision Table

**Conditions:** A kind of decision for this question alone?, A tactical cue?, A strategic cue?, A session kind of decision?

| A kind of decision for this question alone? | A tactical cue? | A strategic cue? | A session kind of decision? | Decision type |
|---|---|---|---|---|
| Yes | - | - | - | The kind of decision the request carries for this question alone |
| No | Yes | No | - | Tactical, for this question only |
| No | No | Yes | - | Strategic, for this question only |
| No | No | No | Yes | The session's kind of decision, which the request carries (`§ Dynamic Retrieval and Weighting (when the question is asked) § Session context`) |
| No | No | No | No | Stop the pipeline and ask for clarification |
| No | Yes | Yes | - | Stop the pipeline and ask for clarification |

### Session context

A question request carries, where set, the session's business unit and kind of decision, and, after a clarification about a question that used decision words of both kinds, the kind of decision chosen for that question alone. The app keeps a Query user's session choices from sign-in to sign-out, as `specs/application/product/answer-engine/decision-context.md § Decision Context` describes, sends them with each question, and changes them only when the Query user does; an API caller sends them itself. A clarifying question names what it asks for, so the app knows what to keep: one asked because the request carried no business unit or kind of decision is answered as a session choice, which the app keeps; one asked because the question used both kinds is answered for that question alone. Either way the app resends the original question with the answer, and nothing was computed before it. Every answer returns the business unit and kind of decision it was given for, which is what the app shows.

### Parallel evidence retrieval

The Question Intent fans out into simultaneous, independent retrieval tasks: call the elasticity model and the list-price and promotional-depth forecast components described in `specs/application/technical/predict-computation.md § Predict Computation § Effective price forecasting`, pull the competitor's historical effective price series, run a filtered vector search of the qualitative corpus scoped to Texas and the relevant time window (tax changes, macro commentary, known competitor plans), and retrieve Brand A's current price and margin targets. These run in parallel because they are independent, this is what keeps a multi-source answer fast.

`specs/application/technical/architecture.md § Architecture Overview § Diagrams § Layer Composition` renders this.
