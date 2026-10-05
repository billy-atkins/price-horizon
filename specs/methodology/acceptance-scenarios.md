## Acceptance Scenarios

A product capability's spec gets acceptance scenarios in Gherkin form (`specs/methodology/external-references.md § External References [Name: Gherkin]`), co-located inside that capability's own section, never in a separate scenarios file. This applies to every product capability with its own section in a product spec file, whether or not it already has a scenario block.

| Rule | Form |
|---|---|
| Where they live | under a child heading titled `Test Scenarios`, one level below the capability's own heading, whatever level that is |
| What the section holds | a single fenced code block tagged `gherkin`, containing every scenario for that capability |
| Syntax | literal Gherkin scenarios, with no `Feature:` line, the capability's own heading standing in for one: each `Scenario:` followed by at least one `Given`, `When` and `Then` step, `And` continuing any of them, not prose formatted to resemble it |
| Individual scenarios | not their own headings; a citation names the whole `Test Scenarios` section |

The title is the same every time and does not restate the capability, because the capability's own heading is already the parent every citation carries. A repeated title lets a reader or a search recognize the pattern once and rely on it everywhere.

**Why a fenced block —** these specifications are the authoritative source that code and its tests are written against and checked back against. Whoever writes that code parses a fenced block rather than transcribing prose by hand, for the same reason a JSON payload or a config file would be fenced rather than described in sentences. Fencing makes a scenario precise and stable to cite; it does not make it executable on its own. An executable copy generated into application code is a test citing the capability's `Test Scenarios` section (`specs/methodology/code.md § Tests`), rather than a separately maintained copy drifting from it.

**Concrete values, not categories —** a scenario's `Given` and `When` steps use a named entity, a real date, a stated amount. A scenario proves one specific case actually produces the promised outcome; a step written in the abstract proves nothing a reader could check.

**Actors are named by role —** a `Given` names its actor by the exact role name the product specs define, never an informal stand-in. If a scenario needs an actor no defined role names, the roles are what is incomplete: define the role first, as a real decision about the access model, then write the scenario against it.

## Deciding What to Write

A capability's own section is the only source for its scenarios: never another file's prose about the same subject, and never a case invented from imagination. The scenarios it owes:

**Construct:** Decision Table

**Conditions:** Write one scenario for

| Write one scenario for | Proving |
|---|---|
| Each promise the section states the capability delivers | that one concrete case reaches the promised outcome |
| Each guardrail the same section states | that the guardrail actually triggers in place of the promise |

A guardrail is a stated boundary, exception or fallback, or a stated "instead of" clause. A promise is any other claim the section states, such as "the output includes X" or "the system does Y."

If a scenario would need a case the section's own prose does not already assert, the prose is what is incomplete: fix that first, in whichever section governs the behavior, then write the scenario against the corrected prose.

A capability whose own section states no guardrail gets only its promise scenarios, and owes no happy-path-plus-guardrail pair.

A guarantee stated only in a cross-cutting file, rather than in one capability's own section, does not get a scenario under that capability. It gets one only where the section stating it is a capability of its own, in that section's `Test Scenarios`.

**A cross-cutting capability —** one available within other capabilities, along dimensions of its own, needs no different scenario shape, only more scenarios: each dimension's own stated promise and its own stated boundary gets the same treatment as any other capability's. Where such a capability acts on a result that already exists rather than producing a first one, its `Given` states that prior result as a precondition before the `When` acts on it.

## Keeping a Scenario and Its Prose in Step

Editing a capability's stated promises or guardrails and editing that capability's scenarios happen in the same pass. A promise that changes without its scenario changing, or a scenario left behind after the promise it tested was removed, is exactly the drift this convention prevents.

## Why a Scenario Is Not a Modeling Construct

A Gherkin scenario is not one of the approved constructs (`specs/methodology/modeling-constructs.md`) and does not belong there.

Each of those constructs is checked for what prose would leave out, as `specs/methodology/modeling-constructs.md § Purpose` lists, often across a space of branches, rows or states that is combinatorial or unbounded until the construct enumerates it. A scenario checks something narrower, a coverage checklist against one section's own already-finite, already-written list of promises and guardrails, not a proof that no branch of some larger space was missed.

A scenario is closer in spirit to a white-box harness that exercises one internal mechanism, but the two are parallel, independent checks rather than one ranked above the other. Such a harness checks that one internal mechanism fires correctly; a scenario checks that a capability delivers what it promises, regardless of which mechanism produced it. Neither cites the other, and keeping the two in agreement when a mechanism changes is the harness's own concern, since the harness is the product's code, which `specs/methodology/scope.md § What Spec of Record Governs` sets apart from the specs.
