A single PriceHorizon installation can host several business units side by side. Each business unit has its own brand, competitor set, category, and geography, and its own glossary terms and thresholds. Almost everything this file describes is scoped to a business unit: the answers a person may ask for, the configuration they may change, and the records they may see.

PriceHorizon's roles distinguish everyday use from administration. A Query user asks questions and explores the answer, in whichever business units their identity grants. A Control plane admin manages a business unit's own configuration, reference data, thresholds and review queues. The Control plane admin also reviews the business unit's forecast evidence and accuracy, and sees the record of who has done what within it. All of this is scoped to that business unit alone. An Identity admin maps the customer's own identity claims to business units and roles, and sees the record of every such change. The Identity admin works across the whole installation rather than the business units a person is granted, since a mistake there could affect access across all of them. The Platform admin described under [`§ Platform & Compliance Operations`](#platform--compliance-operations) likewise works across every business unit an installation hosts. Every domain relies on these roles, and no domain holds them. They are set out in [`specs/application/product/roles.md § Roles`](/specs/application/product/roles.md#roles).

## Answer Engine

PriceHorizon answers one executive question: what will a competitor do on price, where should Brand A sit in response, and what happens to the business as a result. It answers through capabilities that compose in a fixed order, plus one lens that cuts across all of them. Each question is asked in a decision context: the kind of decision the Query user is working on, and the business unit they are working in. PriceHorizon asks for the kind of decision when the session starts, and for the business unit too where the Query user has more than one. The decision context is shown with every answer and can be changed where it is shown. A question's own words can override it for that question alone ([`specs/application/product/answer-engine/decision-context.md § Decision Context`](/specs/application/product/answer-engine/decision-context.md#decision-context)).

The price being forecast is effective price, the net price actually realized per unit over the period being asked about. Effective price is list price minus trade promotions and rebates, plus any surcharges. That is why a competitor's price can move materially while their shelf tag does not.

**Predict.** It turns the question into a forecast: the direction and magnitude of the competitor's likely move in effective price. The forecast is always delivered with a plain-language rationale and distinct measures of certainty attached, never as a bare number. It arrives as a scorecard of the forecast and its confidence, a plain-language account of the expected impact and the KPIs it moves, a map of how the figure breaks down from country to metro, and a chart of the baseline and the drivers behind it. A confidence band gives the range around the forecast itself, drawn from how much uncertainty the underlying forecasting models carry. A confidence score is a separate read of how well-founded the evidence behind the forecast is, explained under [`§ Trust & Explainability`](#trust--explainability). The two can diverge without contradicting each other, as when a precise forecast rests on a weakly sourced fact. The answer shows both without flagging either as an error. Nothing downstream exists without Predict: Position and Simulate both take its output as their starting point. A positioning option carries the forecast's own confidence unchanged. A simulated outcome computes its own confidence, since projecting a business outcome introduces uncertainty the forecast never carried. A positioning option built on a low-confidence forecast is flagged as such, never presented with false certainty.

**Position.** It takes Predict's forecast and frames Brand A's response as a small, named set of options rather than a single recommendation: Hold, Match, Close the Gap, and Diverge. Each option is stated against the predicted outcome as a price gap and as a relative price index. The price gap is the plain currency difference, in the geography's own local currency, never blended into one converted total across countries. The relative price index is the same comparison expressed as a ratio times 100. Above 100 means Brand A sits at a premium, and below 100 a discount. Which options appear depends on the kind of decision the question is asked for, a brand pricing decision or a retailer or promotional one. A retailer or promotional decision drops Diverge, since Diverge moves the brand's price position, which such a decision does not own. The set is never collapsed to one answer. The choice belongs to the executive, and the system's job is to frame it, not make it.

**Simulate.** It takes each Position option and projects what that option would do to the business: share, volume, category growth, revenue, and margin. The outcomes are shown side by side, so the trade-off between options is visible before a decision is made, not discovered afterward.

**Drill-down.** Drill-down is not a capability of its own. It is a lens available within every capability: a narrower geography, or a different metric, without leaving the analysis or re-asking the question. Within the range the underlying competitor data supports, a drilled figure is guaranteed consistent with the broader figure it was drilled from. Past that range, a drilled figure becomes a labeled allocation rather than a sourced forecast. It carries no decomposition of its own, since an allocated figure has no causal story to tell. That boundary reflects which competitor data is currently licensed and ingested, not a permanent limit.

Throughout every stage, the narrative layer explains numbers that already exist rather than generating new ones. That is what keeps an answer defensible in front of a CFO or a retailer. These capabilities are what "the answer" means throughout this product, together with the guarantee that no later stage is ever shown as more certain than the stage it was built on ([`specs/application/product/trust-and-explainability/guarantees.md § Guarantees This Answer Engine Makes`](/specs/application/product/trust-and-explainability/guarantees.md#guarantees-this-answer-engine-makes)). [`§ Diagrams § The Answer`](#the-answer) renders the capabilities and how they compose. [`§ Diagrams § From Evidence to Answer`](#from-evidence-to-answer) renders how a forecast is built from its evidence, and [`§ Diagrams § When an Answer Falls Short`](#when-an-answer-falls-short) renders what an answer shows when a stage cannot complete. Full detail: [`specs/application/product/answer-engine/predict.md`](/specs/application/product/answer-engine/predict.md), [`specs/application/product/answer-engine/position.md`](/specs/application/product/answer-engine/position.md), [`specs/application/product/answer-engine/simulate.md`](/specs/application/product/answer-engine/simulate.md), [`specs/application/product/answer-engine/drill-down.md`](/specs/application/product/answer-engine/drill-down.md), [`specs/application/product/answer-engine/decision-context.md`](/specs/application/product/answer-engine/decision-context.md).

## Trust & Explainability

A forecast here is never a magic number. It is built from a baseline plus a correction from each driver behind it. The baseline is the competitor's own price trend and promotional calendar carried forward, adjusted for anything the competitor has already announced. Each correction is sized by the evidence and by that driver's versioned weight. The forecast is exactly that sum, and the driver chart shows each part. Most of the evidence is in place before anyone asks. Documents are read as they arrive, and their facts are recorded and tagged with how credible that type of source is. Forecasts are computed on a schedule for every competitor and geography a business unit tracks, at standard horizons. A question outside that set has its forecast built when asked, the same way. When a forecast is built, the price history and the documents are checked against each other. Evidence that points where the baseline does not go, by enough to count as a price move, is then caught rather than averaged away.

The forecast's figures open to their why, without leaving the analysis. The baseline opens to the price history, forecasting models and announcements it was built from. Each driver opens to the document it came from, to the model that produced it where the driver is estimated rather than reported, or to both. A figure estimated below the geography the data reports opens to the figure it was allocated from and the weighting used. Every confidence figure opens to the reasons it sits where it does:

- For a forecast, and the options built on it, the reasons are how credible the weakest source is, how current the data is, and whether the evidence agrees. They name both sides of any disagreement big enough to count as a price move.
- For a simulated outcome, the reasons are how confident and how recently validated its models are, and whether the figure was held down to the forecast's own confidence.

Each reason opens to the evidence behind it. Opening each figure to its reasons and evidence is where tracing every number to a named source stops being an assertion and becomes something a Query user can check. It is also where an executive sees not just the number but why to believe it, or why not yet. [`§ Diagrams § From Evidence to Answer`](#from-evidence-to-answer) pictures this.

An answer a Query user can act on has to survive being questioned afterward: by the executive themselves, by a CFO, by a retailer across the table. These guarantees make that possible:

- The same question reproduces the same substance, every figure and score, as long as nothing has changed in between: neither the data, nor the application, model, or configuration versions behind it, nor the kind of decision it is asked for. The narrative's wording may differ.
- Every number traces back to a named, versioned model or dataset rather than being asserted on faith.
- Qualitative context, such as a regulatory change or a competitor's own stated plan, is weighed into the forecast rather than bolted on afterward as commentary.
- Every number shows how it was built and why to believe it.

Trust & Explainability is a different concern from whether the models are drifting over time, which is [`§ Accuracy Governance`](#accuracy-governance). It is also a different concern from who accessed the system or how it executed a request, which is [`§ Logging & Traceability`](#logging--traceability). Trust & Explainability is specifically about whether the answer in front of a Query user right now can be trusted.

Fallbacks hold those guarantees up at the edges. A question whose own terms cannot be resolved, or that leaves unclear which business unit or kind of decision it is about, returns a clarifying question rather than a guess. Nothing is computed for it. A forecast whose evidence falls below the confidence threshold is labeled as such rather than stated fluently. A stage that cannot complete after the answer is under way says so plainly and shows whatever earlier stages did complete. Where nothing completed, it says that instead. In none of these cases is a stale or guessed figure substituted. [`§ Diagrams § When an Answer Falls Short`](#when-an-answer-falls-short) pictures this. Full detail: [`specs/application/product/trust-and-explainability/guarantees.md`](/specs/application/product/trust-and-explainability/guarantees.md), [`specs/application/product/trust-and-explainability/degraded-answer-behavior.md`](/specs/application/product/trust-and-explainability/degraded-answer-behavior.md), [`specs/application/product/answer-engine/predict.md`](/specs/application/product/answer-engine/predict.md), [`specs/application/product/answer-engine/simulate.md`](/specs/application/product/answer-engine/simulate.md).

## Accuracy Governance

Separately from any single answer's own defensibility, every forecast is eventually checked against what actually happened once its horizon passes. The check does not grade a decision an executive already made. It tells whether the underlying models are drifting as markets shift. This is one mechanism visible at different scopes. A Platform admin sees, across every business unit an installation hosts, every driver signal used and the forecasts those signals fed. The Platform admin also sees whether each forecast turned out Right, Right direction, or Wrong, and by how far. That is the pattern Acme AI tunes archetype rules, model versions, and weighting rubrics against. A Control plane admin sees the same view scoped to their own business unit. The Control plane admin can escalate a pattern that looks like the platform itself rather than their own business unit's reality, and can raise a specific prediction with the Query user who asked it. A verdict is judged against what the forecast committed to when it was made, so a later settings change never rewrites it. Full detail: [`specs/application/product/accuracy-governance.md`](/specs/application/product/accuracy-governance.md).

## Tenant Administration

A self-service control plane lets a client manage the day-to-day realities of running PriceHorizon without needing Acme AI paged for routine changes. With it, a client can:

- add a business unit;
- retire a competitor;
- record a rebrand without losing its pricing history;
- connect a new data source Acme AI has already built support for;
- register the business unit's own wording for a term the product already governs, so local jargon resolves the way the standard term does;
- set the business unit's own thresholds for when a price counts as moving and when two options are close enough to show as one;
- rename how its options are labeled;
- resolve the handful of cases the system itself flags as uncertain or incomplete (a product match, a document extraction), since the client's own analysts know their catalog and market better than anyone outside the business unit.

A threshold change reaches the very next answer. The exception is a forecast computed on a schedule, which picks up a new stable-price threshold only when it is next computed. A Control plane admin can ask for the business unit's scheduled forecasts to be computed again rather than waiting for the next run.

The same self-service surface is where a Control plane admin sees, at any time, who has done what within their own business unit:

- Acme AI's own access through PriceHorizon's own systems;
- every configuration change made to the business unit, and who made it;
- every change to who has access to it;
- every change to who holds the Platform admin role;
- every change to which kinds of model call reach a frontier model provider;
- their own Query users' questions, and what they were told.

There, too, a Control plane admin can temporarily raise how much debugging detail PriceHorizon's application logs capture for their own business unit, when they are experiencing an issue and want it resolved faster. The audit record can be searched by who acted, what kind of action, and when. It can be exported as exactly the filtered set, with the narrative wording and figures themselves left behind, so a compliance reviewer can be handed it without needing access of their own.

What stays with Acme AI is the forecasting mechanism itself and the governed vocabulary, which change only through an application or model release. The bounds on every threshold stay with Acme AI too. So does how long the audit log is kept, which a Control plane admin can see but not change. Full detail: [`specs/application/product/tenant-administration/reference-data-management.md`](/specs/application/product/tenant-administration/reference-data-management.md), [`specs/application/product/tenant-administration/business-unit-settings.md`](/specs/application/product/tenant-administration/business-unit-settings.md), [`specs/application/product/tenant-administration/data-source-connections.md`](/specs/application/product/tenant-administration/data-source-connections.md), [`specs/application/product/tenant-administration/review-queues.md`](/specs/application/product/tenant-administration/review-queues.md), [`specs/application/product/tenant-administration/audit-log-visibility.md`](/specs/application/product/tenant-administration/audit-log-visibility.md), [`specs/application/product/tenant-administration/application-log-control.md`](/specs/application/product/tenant-administration/application-log-control.md).

## Identity & Access

The customer's own people sign in through their own identity provider, over OIDC or SAML, so there is no separate PriceHorizon login to learn or run. The identity provider asserts which business units each of them may query and which role they hold. A claim grants nothing until an Identity admin maps it. How Acme AI's own staff reach an installation is set out in [`§ Platform & Compliance Operations`](#platform--compliance-operations).

PriceHorizon keeps using it and administering it on architecturally separate paths, rather than relying on a permissions setting alone. A security-conscious buyer should be able to know not just who can ask a pricing question, but who can change what a competitor's code means or edit a threshold. The buyer should also be able to know whether those two populations are ever the same path by accident, even for a person holding both the Query user and Control plane admin roles. They are not. The path that answers questions never holds the credentials to change configuration, so a problem in the far more widely used query path has no way to reach the far more sensitive administrative one. Every role has to hold to this principle, and so does every technical service boundary built to enforce it. It is not a fact specific to any one of them. [`§ Diagrams § Using and Administering`](#using-and-administering) pictures this. Full detail on how using and administering are kept apart, how access federates to the customer's own identity provider, and how an Identity admin grants it: [`specs/application/product/identity-and-access/using-and-administering-kept-apart.md`](/specs/application/product/identity-and-access/using-and-administering-kept-apart.md), [`specs/application/product/identity-and-access/identity-federation.md`](/specs/application/product/identity-and-access/identity-federation.md), [`specs/application/product/identity-and-access/identity-administration.md`](/specs/application/product/identity-and-access/identity-administration.md).

## Platform & Compliance Operations

PriceHorizon deploys as a versioned, self-hosted installation inside each customer's own environment. The primary protection for competitively sensitive data is that the data never leaves the customer's own infrastructure, save what the client chooses to let a frontier model provider see. The customer's own identity provider sits inside that same environment. Every installation runs entirely within the customer's security boundary, air-gapped where the customer requires. An installation needs no connection outside that boundary unless the client lets some kinds of model call reach a frontier model provider. The client's own infrastructure team makes that choice, never Acme AI. A client raises a support case through Acme AI's own support portal, which PriceHorizon never connects to.

Acme AI's own staff hold the Platform admin role, and with it the access needed to support, monitor, and upgrade an installation. That access is itself governed and recorded rather than a blank check. It is reached through an account the client provisions in its own identity provider or, only where that cannot be reached, through local break-glass credentials. The client can disable it entirely from their own side at any time, without Acme AI's cooperation. Every credential the installation holds lives in an isolated vault, never in the same database as ordinary configuration or reference data.

An upgrade is a discrete, versioned, customer-visible event, never a silent change underneath the customer. The client elects each upgrade; Acme AI never moves an installation to a version they have not. The application and its models upgrade independently of each other. An elected upgrade is either Acme AI-managed, where Acme AI's own staff execute it, or self-managed, where the client's own infrastructure team applies the release. The client can see at any time which versions are currently running. Onboarding is treated as done only once it is verified as working, with real driver signals and forecasts flowing for real questions. Connected integrations alone do not make it done. Full detail: [`specs/application/product/platform-and-compliance-operations/deployment-topology.md`](/specs/application/product/platform-and-compliance-operations/deployment-topology.md), [`specs/application/product/platform-and-compliance-operations/versioned-upgrades.md`](/specs/application/product/platform-and-compliance-operations/versioned-upgrades.md), [`specs/application/product/platform-and-compliance-operations/onboarding-verification.md`](/specs/application/product/platform-and-compliance-operations/onboarding-verification.md).

## Logging & Traceability

PriceHorizon keeps different kinds of record about itself, each answering a different question for a different audience. The kinds are never folded into one.

The audit log records who did something and when, such as a Query user asking a question, an admin changing a setting, or Acme AI accessing an installation. It is a compliance record, kept for at least a year by default. A Control plane admin sees their own business unit's activity, and installation-wide events such as an upgrade or a change to who holds the Platform admin role. An Identity admin sees every change to who is granted access, and every question refused for lack of any business unit access. Acme AI sees its own installation's activity. The client sees its part through the self-service surface [`§ Tenant Administration`](#tenant-administration) describes.

The application log records how the software executed a request internally: which steps ran, how long each took, what failed. It is a debugging record for Acme AI's engineers, with no product screen, kept for weeks rather than years. It never carries the content of a forecast, a document, or a credential. It is forwarded to the client's own observability system or, where the client runs none, to an observability viewer shipped alongside PriceHorizon. It is never sent to anything Acme AI hosts, and never combined with another customer's. Acme AI's engineers see it in the client's system only through access the client grants, outside PriceHorizon and its audit log. In the viewer, they see it through their own governed access, which the audit log records.

An answer's own lineage records what one number is made of: which forecast, evidence, model and version produced it. A Query user sees the lineage inside the answer itself, by opening any figure to its why as [`§ Trust & Explainability`](#trust--explainability) describes, never in a log.

Conflating any two of these records, such as treating an access record as though it explained a number, is the mistake this separation exists to prevent. Full detail: [`specs/application/product/logging-and-traceability.md`](/specs/application/product/logging-and-traceability.md).

## Diagrams

### The Answer

```mermaid
---
config:
  layout: dagre
---
flowchart TD
    Q(["An executive question"]) --> P["Predict<br/>direction and magnitude<br/>of the competitor's likely move"]
    P -->|"forecast, confidence, rationale"| POS["Position<br/>Hold · Match · Close the Gap · Diverge<br/>which apply depends on the decision<br/>never collapsed to one answer"]
    POS -->|"never shown more certain<br/>than the forecast"| SIM["Simulate<br/>share, volume, category growth,<br/>revenue, margin"]
    SIM --> CHOICE(["Trade-offs side by side,<br/>the executive chooses"])

    DRILL["Drill-down<br/>narrower geography, or a different metric,<br/>without leaving the analysis"]
    P -.- DRILL
    POS -.- DRILL
    SIM -.- DRILL

    classDef done fill:#e8f2e8,stroke:#4a7,color:#222
    class CHOICE done
```

**Caption:** The capabilities in their fixed order, what each contributes, and Drill-down cutting across all of them.

**Sources:**
- [`specs/application/product/answer-engine/drill-down.md § Drill-down: cross-cutting, available at every stage`](/specs/application/product/answer-engine/drill-down.md#drill-down-cross-cutting-available-at-every-stage)
- [`specs/application/product/answer-engine/position.md § Position: where Brand A should sit`](/specs/application/product/answer-engine/position.md#position-where-brand-a-should-sit)
- [`specs/application/product/answer-engine/position.md § Position: where Brand A should sit § Options by Kind of Decision`](/specs/application/product/answer-engine/position.md#options-by-kind-of-decision)
- [`specs/application/product/answer-engine/position.md § Position: where Brand A should sit § The Strategies`](/specs/application/product/answer-engine/position.md#the-strategies)
- [`specs/application/product/answer-engine/predict.md § Predict: what will the competitor do`](/specs/application/product/answer-engine/predict.md#predict-what-will-the-competitor-do)
- [`specs/application/product/answer-engine/simulate.md § Simulate: what follows for the business`](/specs/application/product/answer-engine/simulate.md#simulate-what-follows-for-the-business)
- [`specs/application/product/trust-and-explainability/guarantees.md § Guarantees This Answer Engine Makes`](/specs/application/product/trust-and-explainability/guarantees.md#guarantees-this-answer-engine-makes)
- [`§ Answer Engine`](#answer-engine)

### From Evidence to Answer

```mermaid
---
config:
  layout: dagre
---
flowchart TD
    HIST["The competitor's own price history<br/>and announced changes"]
    DOCS["Documents, read as they arrive<br/>facts recorded, tagged for credibility"]
    HIST --> BUILD
    DOCS --> BUILD
    BUILD["The forecast: baseline plus each driver's correction,<br/>price history and documents checked against each other"]
    BUILD -->|"for a tracked competitor and geography,<br/>at a standard horizon"| BUILT["computed on a schedule"]
    BUILD -->|"for anything else"| LIVE["built when asked,<br/>the same way"]
    BUILT --> ANS
    LIVE --> ANS
    Q(["An executive question"]) --> ANS
    ANS["The answer<br/>scorecard of the forecast and its confidence,<br/>impact and KPIs, map, driver chart,<br/>options and their outcomes"]
    ANS --> WHY(["The baseline, every driver, and every confidence figure<br/>open to the reasons and evidence behind them"])

    classDef done fill:#e8f2e8,stroke:#4a7,color:#222
    class WHY done
```

**Caption:** How a forecast is built from its evidence, and what a Query user can open once the answer arrives.

**Sources:**
- [`specs/application/product/answer-engine/position.md § Position: where Brand A should sit`](/specs/application/product/answer-engine/position.md#position-where-brand-a-should-sit)
- [`specs/application/product/answer-engine/predict.md § Predict: what will the competitor do`](/specs/application/product/answer-engine/predict.md#predict-what-will-the-competitor-do)
- [`specs/application/product/answer-engine/simulate.md § Simulate: what follows for the business`](/specs/application/product/answer-engine/simulate.md#simulate-what-follows-for-the-business)
- [`specs/application/product/trust-and-explainability/guarantees.md § Guarantees This Answer Engine Makes`](/specs/application/product/trust-and-explainability/guarantees.md#guarantees-this-answer-engine-makes)
- [`§ Answer Engine`](#answer-engine)

### Using and Administering

```mermaid
---
config:
  layout: dagre
---
flowchart TD
    PEOPLE(["The customer's own people"]) --> IDP["The customer's own<br/>identity provider"]
    ACME(["Acme AI's own staff"]) -->|"an account<br/>the client provisions"| IDP
    subgraph USING["Using"]
        ANS["Query user"]
    end
    subgraph ADMIN["Administering"]
        ADM["Control plane admin<br/>and Identity admin:<br/>configuration,<br/>reference data,<br/>and who is granted access"]
        PLAT["Platform admin<br/>support, monitoring,<br/>and upgrades,<br/>accuracy across<br/>business units"]
    end
    IDP --> USING
    IDP --> ADM
    IDP --> PLAT
```

**Caption:** Who uses PriceHorizon and who administers it. The customer's people sign in through the customer's own identity provider, and so, ordinarily, do Acme AI's staff, through an account the client provisions. From there, using and administering run on separate paths. The path that answers questions never holds the credentials to change configuration, so a problem in the far more widely used path cannot reach the more sensitive one. Acme AI's own staff administer as Platform admins, on access that is governed, recorded, and something the client can disable.

**Sources:**
- [`specs/application/product/accuracy-governance.md § Tracking Forecast Accuracy`](/specs/application/product/accuracy-governance.md#tracking-forecast-accuracy)
- [`specs/application/product/identity-and-access/identity-administration.md § Identity Administration`](/specs/application/product/identity-and-access/identity-administration.md#identity-administration)
- [`specs/application/product/identity-and-access/identity-federation.md § Identity Federation`](/specs/application/product/identity-and-access/identity-federation.md#identity-federation)
- [`specs/application/product/identity-and-access/using-and-administering-kept-apart.md § Using and Administering Kept Apart`](/specs/application/product/identity-and-access/using-and-administering-kept-apart.md#using-and-administering-kept-apart)
- [`specs/application/product/platform-and-compliance-operations/deployment-topology.md § Deployment Topology`](/specs/application/product/platform-and-compliance-operations/deployment-topology.md#deployment-topology)
- [`specs/application/product/roles.md § Roles`](/specs/application/product/roles.md#roles)

### When an Answer Falls Short

```mermaid
---
config:
  layout: dagre
---
flowchart TD
    Q(["An executive question"]) --> R{"Is the question clear?"}
    R -->|"no"| CL(["A clarifying question,<br/>nothing computed"])
    R -->|"yes"| P["Predict"]
    P -->|"cannot complete"| NF(["No forecast,<br/>and the answer says so"])
    P -->|"completes"| POS["Position"]
    POS -->|"cannot complete"| NP(["The forecast, labeled as<br/>missing Position and Simulate"])
    POS -->|"completes"| SIM["Simulate"]
    SIM -->|"cannot complete"| NS(["The forecast and options,<br/>labeled as missing Simulate"])
    SIM -->|"completes"| FULL(["The full answer"])

    classDef stop fill:#f4f4f4,stroke:#777,color:#222
    classDef done fill:#e8f2e8,stroke:#4a7,color:#222
    class CL,NF,NP,NS stop
    class FULL done
```

**Caption:** What an answer shows when it cannot be completed in full. A question whose terms do not resolve, or that leaves unclear which business unit or kind of decision it is about, gets a clarifying question. A stage that cannot complete leaves whatever earlier stages produced, labeled with what is missing, never a stale or guessed figure in its place.

**Sources:**
- [`specs/application/product/trust-and-explainability/degraded-answer-behavior.md § Degraded Answer Behavior`](/specs/application/product/trust-and-explainability/degraded-answer-behavior.md#degraded-answer-behavior)
- [`specs/application/product/trust-and-explainability/guarantees.md § Guarantees This Answer Engine Makes`](/specs/application/product/trust-and-explainability/guarantees.md#guarantees-this-answer-engine-makes)
- [`§ Answer Engine`](#answer-engine)
