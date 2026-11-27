## Dynamic Retrieval and Weighting (when the question is asked)

This is the part of the live path that only the query service runs: handling an incoming question and fanning out its retrieval calls. Everything downstream of intent resolution (forecasting, triangulation, driver attribution, and confidence packaging) is shared with the materialization service and lives in [`specs/application/technical/predict-computation.md § Predict Computation`](/specs/application/technical/predict-computation.md#predict-computation). It lives there because the materialization service's batch path runs the identical computation without ever parsing a question or constructing a Question Intent. The batch path iterates a configured grid instead.

### Intent parsing and decoupling

The incoming question is parsed into a Question Intent ([`specs/application/technical/data-model.md § Core Data Model § Pipeline and Answer Artifacts § Question Intent`](/specs/application/technical/data-model.md#question-intent)): business unit, metric (price), entities (Competitor Brand, Brand A), geography (Texas), horizon (6 months), implied granularity, and decision type (the session's, strategic). Business unit is resolved first, because which glossary and competitor set apply depends on it ([`§ Dynamic Retrieval and Weighting (when the question is asked) § Intent parsing and decoupling § Business unit`](#business-unit)). Decision type is resolved last ([`§ Dynamic Retrieval and Weighting (when the question is asked) § Intent parsing and decoupling § Decision type`](#decision-type)).

Once its business unit is resolved, the rest of the plan is validated against that business unit's glossary before anything executes. An unresolvable entity stops the pipeline and asks for clarification instead of proceeding on a guess. Resolving the business unit follows the same rule.

Each request resolves the units in which the current mappings grant the authenticated person the Query user role. A greeting or clarification offers only those units. After unit selection, retrieval uses only the selected unit.

[`specs/application/technical/architecture.md § Architecture Overview § Diagrams § Trust Boundaries`](/specs/application/technical/architecture.md#trust-boundaries) and [`specs/application/technical/architecture.md § Architecture Overview § Diagrams § The Answer`](/specs/application/technical/architecture.md#the-answer) render this.

#### Business unit

The Decision Table uses the queryable units identified through [`specs/application/technical/identity-and-access.md § Business unit access, federated`](/specs/application/technical/identity-and-access.md#business-unit-access-federated). Count each such unit once. Match the question’s entities against only those glossaries and accept a session unit only if it still belongs to that set. With no queryable unit, deny the question. An unsettled unit requires clarification before retrieval.

**Construct:** `specs/methodology/modeling-constructs.md § Constructs § Decision Table` \
**Hit Policy:** First \
**Conditions:** Business units granted, Resolves against one glossary?, Session business unit granted? \
**Computed:** Business unit

| Name | Business units granted | Resolves against one glossary? | Session business unit granted? | Business unit |
|---|---|---|---|---|
| No Business Unit | 0 | - | - | "denied" |
| One Business Unit | 1 | - | - | granted business unit |
| Glossary | - | true | - | glossary business unit |
| Session | - | - | true | session business unit |
| Unsettled | - | - | - | "unsettled" |

#### Decision type

Decision type is settled once the plan is validated, as [`specs/application/product/answer-engine/decision-context.md § Decision Context`](/specs/application/product/answer-engine/decision-context.md#decision-context) promises, because the positioning engine seeds its candidates by it ([`specs/application/technical/query-service/layered-output-synthesis.md § Layered Output Synthesis (producing the answer) § Positioning engine § Archetype seeds`](/specs/application/technical/query-service/layered-output-synthesis.md#archetype-seeds)). `A kind of decision for this question alone?` reads true where the request carries one, which is the answer to an earlier clarification about it. A cue is one of a fixed set of decision words, held here and never extended by a business unit: "promotion", "promo", "retailer" and "retail account" for tactical; "list price", "price position", "brand-wide" and "national price" for strategic. A cue counts in any grammatical form: "promotional" or "promotions" as well as "promotion". A cue counts only where it describes Brand A's own decision, never the competitor's price. Intent parsing tells the two apart by what the word refers to in the question. Neither a retailer's name nor a time the question gives for its forecast, its horizon, is ever a cue. A decision word is never itself an unresolved term needing clarification. `A tactical cue?` reads true where any tactical cue counts, and `A strategic cue?` where any strategic cue does.

**Construct:** `specs/methodology/modeling-constructs.md § Constructs § Decision Table` \
**Conditions:** A kind of decision for this question alone?, A tactical cue?, A strategic cue?, A session kind of decision? \
**Computed:** Decision type

| A kind of decision for this question alone? | A tactical cue? | A strategic cue? | A session kind of decision? | Decision type |
|---|---|---|---|---|
| true | - | - | - | question kind of decision |
| false | true | false | - | "Tactical" |
| false | false | true | - | "Strategic" |
| false | false | false | true | session kind of decision |
| false | false | false | false | "unsettled" |
| false | true | true | - | "unsettled" |

### Session context

A question request carries the session's business unit and kind of decision, where set. After a clarification about a question that used decision words of both kinds, the request also carries the kind of decision chosen for that question alone. The app keeps a Query user's session choices from sign-in to sign-out, as [`specs/application/product/answer-engine/decision-context.md § Decision Context`](/specs/application/product/answer-engine/decision-context.md#decision-context) describes. The app sends the selections with each question. The service checks the saved unit against current query access before using it. An API caller sends them itself. A clarifying question names what it asks for, so the app knows what to keep. A clarifying question asked because the request carried no business unit or kind of decision is answered as a session choice, which the app keeps. One asked because the question used both kinds is answered for that question alone. Either way, the app resends the original question with the answer, and nothing was computed before it. Every answer returns the business unit and kind of decision it was given for, which is what the app shows.

### Parallel evidence retrieval

Capture the resolved unit’s current publication after authorization and intent resolution. Use the [`§ Dynamic Retrieval and Weighting (when the question is asked) § Parallel evidence retrieval § Forecast source`](#forecast-source) decision to select the market and forecast. A missing scheduled row or failed read follows the existing retrieval retry and failure path. A unit awaiting its first publication receives the specific reason, with no forecast or delivery created.

For a live lookup, match unit, competitor, brand, geography, horizon, metric, resolved period and basis, publication ID, data vintage, complete forecast model map, application and business-unit configuration versions. Pin the question’s applicable settings and application version on entry. Look up committed forecasts by this unique key. The model call trace records only invoked versions. On either path retrieve Brand A’s current price and margin targets. Positioning uses the selected forecast and the current positioning settings. Show the forecast’s origin and target window from its immutable record on each delivery.

For an eligible live request that has no exact committed match, retrieve the forecast inputs in parallel:
- retrieve the competitor’s observed list prices, trade-promotion depths, rebates and surcharges per unit from the pinned snapshot
- read the rebate and surcharge terms for that competitor, brand and geography effective in the target period, as known at the same data vintage. For each adjustment supply its applicable per-unit term and source, or its latest observed per-unit amount and observation date when the future term is unspecified
- retrieve the signals eligible for this forecast. Both the scheduled cell and the live question use the resolved business-unit namespace, applicable geography and time window. A Competitor signal must match the competitor code and cover the resolved brand through its recorded brand set or explicit portfolio-wide scope. A Business Unit signal must match the unit, market and product scope. An unresolved scope cannot match. Apply this rule before event routing on both paths

The forecast algorithms call their models when they consume these inputs. Confidence packaging stages the complete forecast and rationale for this request under the pinned key before Position starts. The answer transaction makes the live bundle reusable under [`specs/application/technical/engineering-and-production-considerations.md § Engineering and Production Considerations § Security and governance`](/specs/application/technical/engineering-and-production-considerations.md#security-and-governance). Brand A's current price is retrieved as a reference point, not modeled or converted into a price gap or relative price index at this stage.

[`specs/application/technical/architecture.md § Architecture Overview § Diagrams § Layer Composition`](/specs/application/technical/architecture.md#layer-composition) renders this.

#### Forecast source

Resolve each authorized request against its captured publication. A drill-down uses the same selector as a direct question for the narrower market, as [`specs/application/product/answer-engine/drill-down.md § Drill-down: cross-cutting, available at every stage § What a granularity drill-down shows`](/specs/application/product/answer-engine/drill-down.md#what-a-granularity-drill-down-shows) requires. For a below-grid request, run this same selection at the nearest grounded ancestor. If its forecast is unavailable, return the reason. Its forecast, when available, supplies the basis for [`specs/application/technical/query-service/layered-output-synthesis.md § Layered Output Synthesis (producing the answer) § Drill-down mechanics`](/specs/application/technical/query-service/layered-output-synthesis.md#drill-down-mechanics). For a rejected request, return the reason selected below. Identify the target window or the affected published model and requested lead time so the user can see which check failed. Reopening a retained delivery retrieves its original forecast by identity. An exact eligible live match fulfills the reuse promise in [`specs/application/product/answer-engine/predict.md § Predict: what will the competitor do`](/specs/application/product/answer-engine/predict.md#predict-what-will-the-competitor-do).

**Construct:** `specs/methodology/modeling-constructs.md § Constructs § Decision Table` \
**Conditions:** Publication available?, Tracked brand?, Requested market grounded?, Grounded ancestor?, Scheduled horizon?, One observation window?, Support declarations known?, Lead time supported?, Exact live match? \
**Computed:** Lookup result

| Publication available? | Tracked brand? | Requested market grounded? | Grounded ancestor? | Scheduled horizon? | One observation window? | Support declarations known? | Lead time supported? | Exact live match? | Lookup result |
|---|---|---|---|---|---|---|---|---|---|
| false | - | - | - | - | - | - | - | - | "awaiting publication" |
| true | false | - | - | - | - | - | - | - | "untracked" |
| true | true | false | false | - | - | - | - | - | "no grounded market" |
| true | true | false | true | - | - | - | - | - | "use grounded parent" |
| true | true | true | - | true | - | - | - | - | "published cell" |
| true | true | true | - | false | false | - | - | - | "unresolved observation window" |
| true | true | true | - | false | true | false | - | - | "unknown model support" |
| true | true | true | - | false | true | true | false | - | "unsupported lead time" |
| true | true | true | - | false | true | true | true | true | "stored live" |
| true | true | true | - | false | true | true | true | false | "compute live" |

[`specs/application/technical/architecture.md § Architecture Overview § Diagrams § Layer Composition`](/specs/application/technical/architecture.md#layer-composition) shows how a published cell, an exact live match and a newly computed forecast reach synthesis.

## Facts

**Records:**
  - **Name:** IdP-asserted access \
    **Type:** list<context<business_unit: string, role: string>> \
    **Means:** the effective business-unit and role pairs for the authenticated claims under the current mappings

  - **Name:** question entities \
    **Type:** list<string> \
    **Means:** the brand and competitor named in the question

  - **Name:** business units granted \
    **Type:** number \
    **Means:** the number of distinct units where those pairs grant the Query user role

  - **Name:** granted business unit \
    **Type:** string \
    **May Be Absent:** Yes \
    **Means:** the sole queryable business unit when exactly one qualifies

  - **Name:** glossary business unit \
    **Type:** string \
    **May Be Absent:** Yes \
    **Means:** the unique queryable business unit whose glossary resolves the question's brand or competitor, where exactly one does

  - **Name:** resolves against one glossary? \
    **Type:** boolean \
    **Means:** whether exactly one queryable unit’s glossary resolves the brand or competitor

  - **Name:** session business unit granted? \
    **Type:** boolean \
    **Means:** whether the request’s session unit still belongs to the set of queryable units

  - **Name:** business unit \
    **Type:** string \
    **Means:** the selected queryable unit, denied when none grants the Query user role, or unsettled when clarification is needed

  - **Name:** a kind of decision for this question alone? \
    **Type:** boolean \
    **Means:** whether the request carries a kind of decision chosen for this question alone

  - **Name:** a tactical cue? \
    **Type:** boolean \
    **Means:** whether a tactical decision word describes Brand A's own decision

  - **Name:** a strategic cue? \
    **Type:** boolean \
    **Means:** whether a strategic decision word describes Brand A's own decision

  - **Name:** a session kind of decision? \
    **Type:** boolean \
    **Means:** whether the request carries a kind of decision for the session

  - **Name:** session business unit \
    **Type:** string \
    **May Be Absent:** Yes \
    **Means:** the business unit chosen for the session, where one has been chosen

  - **Name:** question kind of decision \
    **Type:** string \
    **Values:** "Strategic", "Tactical" \
    **May Be Absent:** Yes \
    **Means:** the kind of decision chosen for this question alone, where one has been chosen

  - **Name:** session kind of decision \
    **Type:** string \
    **Values:** "Strategic", "Tactical" \
    **May Be Absent:** Yes \
    **Means:** the kind of decision chosen for the session, where one has been chosen

  - **Name:** decision type \
    **Type:** string \
    **Values:** "Strategic", "Tactical", "unsettled" \
    **Means:** the kind of decision the question is given for, or `unsettled` when clarification is needed

  - **Name:** publication available? \
    **Type:** boolean \
    **Means:** whether the unit has published a complete grid

  - **Name:** tracked brand? \
    **Type:** boolean \
    **Means:** whether the selected competitor and brand belong to the captured published membership

  - **Name:** requested market grounded? \
    **Type:** boolean \
    **Means:** whether the requested market itself belongs to the captured publication’s reconciled geography grid

  - **Name:** grounded ancestor? \
    **Type:** boolean \
    **Means:** whether a strict ancestor of the requested market in the reconciled geography hierarchy belongs to that grid

  - **Name:** scheduled horizon? \
    **Type:** boolean \
    **Means:** whether the requested lead time belongs to the captured publication’s schedule, regardless of whether its cell can be read

  - **Name:** one observation window? \
    **Type:** boolean \
    **Means:** whether the requested lead time resolves to exactly one supported observation period for the published series and price basis

  - **Name:** support declarations known? \
    **Type:** boolean \
    **Means:** whether each horizon-consuming forecast call in [`specs/application/technical/predict-computation.md § Predict Computation § Baseline forecast`](/specs/application/technical/predict-computation.md#baseline-forecast) has an identifiable published model version with a readable declaration under [`specs/application/technical/model-registry.md § Model registry`](/specs/application/technical/model-registry.md#model-registry)

  - **Name:** lead time supported? \
    **Type:** boolean \
    **Means:** whether the requested lead time belongs to every required version’s declared set after normalization within the same duration family

  - **Name:** exact live match? \
    **Type:** boolean \
    **Means:** whether a committed live forecast and rationale match the complete pinned key

  - **Name:** lookup result \
    **Type:** string \
    **Means:** the selected route and availability decision for this resolved request
