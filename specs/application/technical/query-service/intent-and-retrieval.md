## Dynamic Retrieval and Weighting (when the question is asked)

The genuinely query-service-only part of the live path: handling an incoming question and fanning out its retrieval calls. Everything downstream of intent resolution, forecasting, triangulation, driver attribution, and confidence packaging, is shared with the materialization service and lives in `specs/application/technical/predict-computation.md § Predict Computation`, since the materialization service's batch path runs the identical computation without ever parsing a question or constructing a Question Intent, it iterates a configured grid instead.

### Intent parsing and decoupling

The incoming question is parsed into a Question Intent (`specs/application/technical/data-model.md § Core Data Model § Pipeline and Answer Artifacts § Question Intent`): business unit, metric (price), entities (Competitor Brand, Brand A), geography (Texas), horizon (6 months), implied granularity, and decision type (the session's, strategic). Business unit is resolved first, since which glossary and competitor set apply depends on it, by a Decision Tree.

| Step | Question | Answer | Result |
|---|---|---|---|
| 1.1 | How many business units does the user's IdP-asserted access (`specs/application/technical/identity-and-access.md § Business unit access, federated`) contain? | None | Deny the query; no claim mapping grants this identity access to any business unit |
| 1.2 | | Exactly one | Use it as the query's business unit |
| 1.3 | | More than one | Go to step 2 |
| 2.1 | Does a brand or competitor in the question resolve uniquely against one business unit's glossary? | Yes | Use that business unit |
| 2.2 | | No, it resolves against more than one or against none | Use the session's business unit the request carries (`§ Dynamic Retrieval and Weighting (when the question is asked) § Session context`), if the access the IdP grants includes it; otherwise stop the pipeline and ask for clarification |

The rest of the plan is then validated against the resolved business unit's glossary before anything executes. An unresolvable entity stops the pipeline and asks for clarification instead of proceeding on a guess, the same rule this section's Decision Tree applies to business unit itself.

The access set also enforces that every retrieval this query makes is filtered to business units the IdP actually granted, not merely used to guess intent, and a clarification prompt can never reveal a business unit outside that set, someone with access to one business unit is never told a second one exists just because the installation happens to host it.

Decision type is settled next, as `specs/application/product/answer-engine/decision-context.md § Decision Context` promises, since the positioning engine seeds its candidates by it (`specs/application/technical/query-service/layered-output-synthesis.md § Layered Output Synthesis (producing the answer) § Positioning engine`). A kind of decision the request carries for this question alone, the answer to an earlier clarification about it, settles it first; otherwise this section's table of cues does. A cue is one of a fixed set of decision words, held here and never extended by a business unit: "promotion", "promo", "retailer" and "retail account" for tactical; "list price", "price position", "brand-wide" and "national price" for strategic. A cue counts in any grammatical form, "promotional" or "promotions" as well as "promotion", and only where it describes Brand A's own decision, never the competitor's price, which intent parsing tells apart by what the word refers to in the question. Neither a retailer's name nor a time the question gives for its forecast, its horizon, is ever a cue, and a decision word is never itself an unresolved term needing clarification. A column reads Yes when any cue of that kind counts, and a row applies when both its columns match.

| Tactical cue | Strategic cue | Decision type |
|---|---|---|
| Yes | No | Tactical, for this question only |
| No | Yes | Strategic, for this question only |
| No | No | The session's kind of decision, where the request carries one (`§ Dynamic Retrieval and Weighting (when the question is asked) § Session context`); with none, stop the pipeline and ask for clarification |
| Yes | Yes | Stop the pipeline and ask for clarification |

`specs/application/technical/architecture.md § Architecture Overview § Diagrams § Trust Boundaries` and `specs/application/technical/architecture.md § Architecture Overview § Diagrams § The Answer` render this.

### Session context

A question request carries, where set, the session's business unit and kind of decision, and, after a clarification about a question that used decision words of both kinds, the kind of decision chosen for that question alone. The app keeps a Query user's session choices from sign-in to sign-out, as `specs/application/product/answer-engine/decision-context.md § Decision Context` describes, sends them with each question, and changes them only when the Query user does; an API caller sends them itself. A clarifying question names what it asks for, so the app knows what to keep: one asked because the request carried no business unit or kind of decision is answered as a session choice, which the app keeps; one asked because the question used both kinds is answered for that question alone. Either way the app resends the original question with the answer, and nothing was computed before it. Every answer returns the business unit and kind of decision it was given for, which is what the app shows.

### Parallel evidence retrieval

The Question Intent fans out into simultaneous, independent retrieval tasks: call the elasticity model and the list-price and promotional-depth forecast components described in `specs/application/technical/predict-computation.md § Predict Computation § Effective price forecasting`, pull the competitor's historical effective price series, run a filtered vector search of the qualitative corpus scoped to Texas and the relevant time window (tax changes, macro commentary, known competitor plans), and retrieve Brand A's current price and margin targets. These run in parallel because they are independent, this is what keeps a multi-source answer fast.

`specs/application/technical/architecture.md § Architecture Overview § Diagrams § Layer Composition` renders this.
