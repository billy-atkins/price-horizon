## Dynamic Retrieval and Weighting (when the question is asked)

This is the part of the live path that only the query service runs: handling an incoming question and fanning out its retrieval calls. Everything downstream of intent resolution (forecasting, triangulation, driver attribution, and confidence packaging) is shared with the materialization service and lives in [`specs/application/technical/predict-computation.md § Predict Computation`](/specs/application/technical/predict-computation.md#predict-computation). It lives there because the materialization service's batch path runs the identical computation without ever parsing a question or constructing a Question Intent. The batch path iterates a configured grid instead.

### Intent parsing and decoupling

The incoming question is parsed into a Question Intent ([`specs/application/technical/data-model.md § Core Data Model § Pipeline and Answer Artifacts § Question Intent`](/specs/application/technical/data-model.md#question-intent)): business unit, metric (price), entities (Competitor Brand, Brand A), geography (Texas), horizon (6 months), implied granularity, and decision type (the session's, strategic). Business unit is resolved first, because which glossary and competitor set apply depends on it ([`§ Dynamic Retrieval and Weighting (when the question is asked) § Intent parsing and decoupling § Business unit`](#business-unit)). Decision type is resolved last ([`§ Dynamic Retrieval and Weighting (when the question is asked) § Intent parsing and decoupling § Decision type`](#decision-type)).

Once its business unit is resolved, the rest of the plan is validated against that business unit's glossary before anything executes. An unresolvable entity stops the pipeline and asks for clarification instead of proceeding on a guess. Resolving the business unit follows the same rule.

The business units the user's IdP-asserted access contains are not merely used to guess intent. They also bound every retrieval this query makes, which is filtered to the business units the IdP granted. A clarification prompt can never reveal a business unit outside that set. Someone with access to one business unit is never told a second one exists only because the installation happens to host it.

[`specs/application/technical/architecture.md § Architecture Overview § Diagrams § Trust Boundaries`](/specs/application/technical/architecture.md#trust-boundaries) and [`specs/application/technical/architecture.md § Architecture Overview § Diagrams § The Answer`](/specs/application/technical/architecture.md#the-answer) render this.

#### Business unit

A Decision Table resolves business unit from the access the user's IdP asserts ([`specs/application/technical/identity-and-access.md § Business unit access, federated`](/specs/application/technical/identity-and-access.md#business-unit-access-federated)), asking its questions in turn. `Business units granted` is how many business units the user's IdP-asserted access contains. `Resolves against one glossary?` reads true where a brand or competitor in the question resolves uniquely against the glossary of exactly one business unit the IdP-asserted access grants, and false where it resolves against more than one granted business unit or against none. `Session business unit granted?` reads true where the request carries a session business unit ([`§ Dynamic Retrieval and Weighting (when the question is asked) § Session context`](#session-context)) that the IdP-asserted access includes. The table's outcome is the query's business unit, `denied` or `unsettled`. `denied` means no claim mapping grants this identity access to any business unit, and the query is denied. `unsettled` means the pipeline stops and asks for clarification.

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

A question request carries the session's business unit and kind of decision, where set. After a clarification about a question that used decision words of both kinds, the request also carries the kind of decision chosen for that question alone. The app keeps a Query user's session choices from sign-in to sign-out, as [`specs/application/product/answer-engine/decision-context.md § Decision Context`](/specs/application/product/answer-engine/decision-context.md#decision-context) describes. The app sends them with each question and changes them only when the Query user does. An API caller sends them itself. A clarifying question names what it asks for, so the app knows what to keep. A clarifying question asked because the request carried no business unit or kind of decision is answered as a session choice, which the app keeps. One asked because the question used both kinds is answered for that question alone. Either way, the app resends the original question with the answer, and nothing was computed before it. Every answer returns the business unit and kind of decision it was given for, which is what the app shows.

### Parallel evidence retrieval

Capture the resolved unit’s current publication after authorization and intent resolution. Classify a requested geography below the grid’s resolution for allocation from its grounded parent. Other unsupported geographies are unavailable. Only a tracked brand at a grounded market and supported horizon can take the live route. A scheduled key must read its own published bundle. A missing scheduled row or failed read follows the existing retrieval retry and failure path. A unit awaiting its first publication returns the specific unavailability reason. No forecast or delivery is created.

For a live lookup, match unit, competitor, brand, geography, horizon, metric, resolved period and basis, publication ID, data vintage, complete forecast model map, application and business-unit configuration versions. Pin the question’s applicable settings and application version on entry. Persist on this unique key so concurrent misses return the same forecast and rationale. The model call trace records only invoked versions. On either path retrieve Brand A’s current price and margin targets. Positioning uses the selected forecast and the current positioning settings. Show the forecast’s origin and target window from its immutable record on each delivery.

When the lookup returns no matching record for an outside-grid request, retrieve the forecast inputs in parallel:
- retrieve the competitor’s observed list prices, trade-promotion depths, rebates and surcharges per unit from the pinned snapshot
- read the rebate and surcharge terms for that competitor, brand and geography effective in the target period, as known at the same data vintage. For each adjustment supply its applicable per-unit term and source, or its latest observed per-unit amount and observation date when the future term is unspecified
- retrieve the signals eligible for this forecast. Both the scheduled cell and the live question use the resolved business-unit namespace, applicable geography and time window. A Competitor signal must match the competitor code and cover the resolved brand through its recorded brand set or explicit portfolio-wide scope. A Business Unit signal must match the unit, market and product scope. An unresolved scope cannot match. Apply this rule before event routing on both paths

The forecast algorithms call their models when they consume these inputs. Confidence packaging persists the resulting bundle under the same pinned key before positioning begins. Brand A's current price is retrieved as a reference point, not modeled or converted into a price gap or relative price index at this stage.

[`specs/application/technical/architecture.md § Architecture Overview § Diagrams § Layer Composition`](/specs/application/technical/architecture.md#layer-composition) renders this.

#### Select a forecast

Resolve the source for an authorized forecast request against the captured publication. A finer geographic estimate selects the grounded parent and applies the existing allocation rule.

**Construct:** `specs/methodology/modeling-constructs.md § Constructs § Decision Table` \
**Conditions:** Publication available?, Tracked brand?, Forecast route, Exact live match? \
**Computed:** Lookup result

| Publication available? | Tracked brand? | Forecast route | Exact live match? | Lookup result |
|---|---|---|---|---|
| false | - | - | - | "awaiting publication" |
| true | false | - | - | "untracked" |
| true | true | "cell" | - | "published cell" |
| true | true | "allocation" | - | "use grounded parent" |
| true | true | "unsupported" | - | "unavailable" |
| true | true | "live" | true | "stored live" |
| true | true | "live" | false | "compute live" |

## Facts

**Records:**
  - **Name:** IdP-asserted access \
    **Type:** list<context<business_unit: string, role: string>> \
    **Means:** the business units and roles the user's identity provider grants

  - **Name:** question entities \
    **Type:** list<string> \
    **Means:** the brand and competitor named in the question

  - **Name:** business units granted \
    **Type:** number \
    **Means:** how many business units the IdP-asserted access contains

  - **Name:** granted business unit \
    **Type:** string \
    **May Be Absent:** Yes \
    **Means:** the one business unit in the IdP-asserted access where exactly one is granted

  - **Name:** glossary business unit \
    **Type:** string \
    **May Be Absent:** Yes \
    **Means:** the unique granted business unit whose glossary resolves the question's brand or competitor, where exactly one does

  - **Name:** resolves against one glossary? \
    **Type:** boolean \
    **Means:** whether the brand or competitor resolves uniquely against the glossary of exactly one business unit the IdP-asserted access grants

  - **Name:** session business unit granted? \
    **Type:** boolean \
    **Means:** whether the request carries a session business unit included in the IdP-asserted access

  - **Name:** business unit \
    **Type:** string \
    **Means:** the business unit the query is given for, `denied` when no mapping grants access or `unsettled` when clarification is needed

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

  - **Name:** forecast route \
    **Type:** string \
    **Values:** "cell", "live", "allocation", "unsupported" \
    **Means:** requested scope classified using the captured publication and geographic grounding rules

  - **Name:** exact live match? \
    **Type:** boolean \
    **Means:** whether a stored forecast and rationale match the complete pinned key

  - **Name:** lookup result \
    **Type:** string \
    **Means:** the selected route and availability decision for this resolved request
