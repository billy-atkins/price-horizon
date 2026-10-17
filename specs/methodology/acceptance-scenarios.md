## Acceptance Scenarios

A product capability's spec gets acceptance scenarios in Gherkin form ([`specs/methodology/external-references.md § External References [Name: Gherkin]`](/specs/methodology/external-references.md#external-references)). The scenarios sit inside that capability's own section, never in a separate scenarios file. This applies to every product capability with its own section in a product spec file, whether or not it already has a scenario block.

**Reference Key:** Rule

**Required:** Form

| Rule | Form |
|---|---|
| Where they live | under a child heading titled `Test Scenarios`, one level below the capability's own heading, whatever level that is |
| What the section holds | a single fenced code block tagged `gherkin`, containing every scenario for that capability |
| Syntax | literal Gherkin scenarios, not prose formatted to resemble them, with no `Feature:` line, the capability's own heading standing in for one. Each `Scenario:` is followed by at least one `Given`, `When` and `Then` step, and `And` continues any of them |
| Individual scenarios | given no heading of their own. A citation names the whole `Test Scenarios` section |

The title is the same every time and does not restate the capability, because the capability's heading is already the parent every citation carries. A repeated title lets a reader or a search recognize the pattern once and rely on it everywhere.

**Why a fenced block.** The specs are the authoritative source that code and its tests are written against and checked back against. Whoever writes that code parses a fenced block rather than transcribing prose by hand. A JSON payload or a config file would be fenced rather than described in sentences, for the same reason. Fencing makes a scenario precise and stable to cite. It does not make the scenario executable on its own. An executable copy generated into application code is a test that cites the capability's `Test Scenarios` section ([`specs/methodology/code.md § Tests`](/specs/methodology/code.md#tests)), not a separately maintained copy that drifts from it.

**Concrete values, not categories.** A scenario's `Given` and `When` steps use a named entity, a real date, a stated amount. A scenario proves that one specific case produces the promised outcome. A step written in the abstract proves nothing a reader could check.

**Actors are named by role.** A `Given` names its actor by the exact role name the product specs define, never an informal stand-in. If a scenario needs an actor that no defined role names, the roles are what is incomplete. Define the role first, as a real decision about the access model, then write the scenario against it.

## Deciding What to Write

A capability's own section is the only source for its scenarios. Another file's prose about the same subject is never a source, and neither is an invented case.

### Scenarios a Capability Owes

The scenarios a capability's own section owes:

**Construct:** `specs/methodology/modeling-constructs.md § Constructs § Decision Table`

**Conditions:** Write one scenario for

| Write one scenario for | Proving |
|---|---|
| Each promise the section states the capability delivers | that one concrete case reaches the promised outcome |
| Each guardrail the same section states | that the guardrail actually triggers in place of the promise |

A guardrail is a stated boundary, exception or fallback, or a stated "instead of" clause. A promise is any other claim the section states, such as "the output includes X" or "the system does Y."

If a scenario would need a case that the section's prose does not already assert, the prose is what is incomplete. Fix the prose first, in whichever section governs the behavior, then write the scenario against the corrected prose.

A capability whose own section states no guardrail gets only its promise scenarios. It owes no happy-path-plus-guardrail pair.

A guarantee stated only in a cross-cutting file, rather than in one capability's own section, gets no scenario under that capability. It gets one only where the section stating it is a capability of its own, and then in that section's `Test Scenarios`.

**A cross-cutting capability.** A capability available within other capabilities, along dimensions of its own, needs no different scenario shape. It needs only more scenarios: each dimension's stated promise and stated boundary get the same treatment as any other capability's. Where such a capability acts on a result that already exists, rather than producing a first one, its `Given` states that prior result as a precondition before the `When` acts on it.

## Keeping a Scenario and Its Prose in Sync

An author edits a capability's stated promises or guardrails and that capability's scenarios in the same pass. A promise that changes while its scenario does not, or a scenario left behind after the promise it tested was removed, is the drift this convention prevents.

## Why a Scenario Is Not a Modeling Construct

A Gherkin scenario is not one of the approved constructs ([`specs/methodology/modeling-constructs.md`](/specs/methodology/modeling-constructs.md)) and does not belong there.

Each of those constructs is checked for what prose would leave out, as each construct's definition lists ([`specs/methodology/modeling-constructs.md § Constructs`](/specs/methodology/modeling-constructs.md#constructs)). The check often runs across a space of branches, rows or states that is combinatorial or unbounded until the construct enumerates it. A scenario checks something narrower. It is a coverage checklist against one section's list of promises and guardrails, a list already finite and already written. It is not a proof that no branch of some larger space was missed.

A scenario is closer in spirit to a white-box harness that exercises one internal mechanism. But the two are parallel, independent checks, and neither ranks above the other. Such a harness checks that one internal mechanism fires correctly. A scenario checks that a capability delivers what it promises, whichever mechanism produced it. Neither cites the other. Keeping the two in agreement when a mechanism changes is the harness's concern, because the harness is the product's code, which [`specs/methodology/scope.md § What Spec of Record Governs`](/specs/methodology/scope.md#what-spec-of-record-governs) sets apart from the specs.
