## The Working Files

Writing the specs leaves working files beside them. They serve the engineer writing the specs, never a reader of them, so none is committed. Which specs may name one is set in `specs/methodology/sourcing-and-citation.md § Which Citations Are Allowed`. What a working file settles reaches a reader only through the spec it changes.

| File | Holds |
|---|---|
| `.ai/designs.md` | changes proposed and under review, each as a design entry (`§ A Design Entry`) |
| `.ai/follow-ups.md` | work on the specs that should be done and is not yet, each as a follow-up (`§ A Follow-up`) |
| `.ai/tmp/` | the skills' own output, review and audit reports among it (`AGENTS.md § Authoring Skills`) |

`.ai/designs.md` and `.ai/follow-ups.md` each open with a short header naming what the file holds and citing this file, and the file's entries follow that header.

An open question about what is specified is not a working file's to hold. It belongs in the spec whose area it applies to, product or technical, where a reader relying on that area sees it.

## A Design Entry

A design entry describes one change taken through `AGENTS.md § Design, Refactor, Refine (DRR)`. Entries are separated by a horizontal rule, each headed by a level-two heading naming the change, and each holds these parts, in this order:

| Part | Form | Holds |
|---|---|---|
| Status | a `**Status:**` line | where the entry is in its lifecycle below, and each review it has been through, naming the review's report |
| Source | a `**Source:**` line | what asked for the change: the user's own words, or the finding that raised it |
| Target | a `**Target:**` line | every file the change edits |
| The problem | a `### The problem` section | what is wrong, stated on its own, before any fix |
| Scope | a `### Scope` section | how the sweep for affected content was done and what it found, what it left out included |
| The design | a `### The design` section | each edit, quoting exactly the text it replaces or follows, so it can be verified and applied as written |
| The builder's passes | a `### The builder's passes` section | what each pass and each review changed |
| Deliberately left alone | a `### Deliberately left alone` section | each change considered and declined, with the reason, and each piece of work deferred, named by its follow-up |

Work the change defers becomes a follow-up when it is deferred, not when the entry is pruned.

A Lifecycle. States:

| state | description | terminal |
|---|---|---|
| proposed | drafted, and under the builder's passes or a review | No |
| applied | its edits are written to the files it targets | No |
| pruned | removed from the file; what an applied entry decided lives on in the specs it changed | Yes |

Transitions:

| From | To | Trigger or condition |
|---|---|---|
| proposed | applied | the user gives the go-ahead, and the edits are written |
| proposed | pruned | the user withdraws the change |
| applied | pruned | the post-apply audit is settled |

## A Follow-up

A follow-up records work on the specs that should be done and is not yet, with enough context for someone arriving cold to take it up. It is kept until the work is done, however many changes pass in between, so nothing that should be worked is lost. Each sits under a priority heading: `## High`, the work to take up next; `## Medium`, which waits until High is settled; or `## Low`, worth doing once nothing more pressing is open. Each holds these parts, in this order:

| Part | Form | Holds |
|---|---|---|
| Name | a `###` heading, a kebab-case slug | the name the follow-up is referred to by |
| Status | a `**Status:**` line | where the follow-up is in its lifecycle below |
| Category | a `**Category:**` line | what kind of gap it is, such as under-developed, stale wording, a missing citation, or an open scope decision |
| Location | a `**Location:**` line | the file, section or files it concerns |
| Body | prose | the work, the context needed to take it up, and, where known, what found it |

A Lifecycle. States:

| state | description | terminal |
|---|---|---|
| not-started | recorded, and not yet taken up | No |
| in-progress | taken up, usually as a design entry | No |
| done | resolved, and removed from the file | Yes |

Transitions:

| From | To | Trigger or condition |
|---|---|---|
| not-started | in-progress | the work is taken up |
| in-progress | not-started | the design entry taking it up is withdrawn |
| in-progress | done | the change that resolves it lands, or the user decides nothing needs to change |
| not-started | done | a change made for another reason resolves it, or the user decides nothing needs to change |
