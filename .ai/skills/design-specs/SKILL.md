---
name: design-specs
description: Propose or revise content in this repo's specifications. Use when adding a rule, reconciling two documents that disagree, closing a gap found in an audit or review, or taking a change through DRR. Routes to the conventions that govern the work, and covers the failures that recur in it, duplicating a rule that already has a home, distorting a fact while compressing it, and proposing edits whose anchors do not exist.
---

# Designing specifications

Every fact in this repo is supposed to live in exactly one place, and everywhere else that needs it points there. Most defects introduced here are not wrong statements. They are true statements written in a second place.

That is the difficulty. A sentence you are about to write is almost always correct on its own terms. The question is never "is this true" but "is this already stated, and is this where it belongs."

This skill does not restate the repo's conventions, which would be the same defect it exists to prevent. It says where they are and what recurs when applying them.

## Where the governing rules live

| Doing this | The rule is here |
|---|---|
| Deciding product spec versus technical spec | `specs/methodology/spec-placement.md § Product or Technical` |
| Deciding index, architecture, or detail file | `specs/methodology/spec-placement.md § Index, Architecture, Detail` |
| Placing a new product capability, or naming a domain | `specs/methodology/spec-placement.md § Naming a Capability Domain` |
| Deciding whether a rule may be restated | `specs/methodology/sourcing-and-citation.md § One Home Per Fact` |
| Writing a citation, or naming a section | `specs/methodology/sourcing-and-citation.md § Writing a Citation` |
| Deciding whether a citation may be written here | `specs/methodology/sourcing-and-citation.md § Which Citations Are Allowed` |
| Writing a number, a count, or a reference to an item's position | `AGENTS.md § Ordinals and Counts` |
| Adding or retitling a heading | `specs/methodology/sourcing-and-citation.md § Titling a Heading` |
| Writing or updating acceptance scenarios | `specs/methodology/acceptance-scenarios.md § Acceptance Scenarios` |
| Linking a product file to its technical files | `specs/methodology/spec-placement.md § Naming the Technical Files Behind a Capability` |
| Removing drafting residue and hedged framing | `specs/methodology/spec-style.md § What a Finished Spec Reads Like` |
| Taking work through Design, Refactor, Refine | `AGENTS.md § Design, Refactor, Refine (DRR)` |
| Recording a proposed change, or work to take up later | `specs/methodology/working-files.md § A Design Entry`, `specs/methodology/working-files.md § A Follow-up` |
| Describing a rule, a process, or an entity's behavior | `specs/methodology/modeling-constructs.md` |
| Recording a decision the specs rely on but have not made | `specs/methodology/spec-placement.md § An Open Question` |
| Writing a field, a bold lead-in, or an entry of a repeated kind | `specs/methodology/modeling-constructs.md § Fields`, `specs/methodology/modeling-constructs.md § Bold Lead-ins`, `specs/methodology/modeling-constructs.md § Constructs § Record Form` |
| Keeping a companion spec or an `architecture.md` in step | `specs/methodology/sourcing-and-citation.md § Keeping Companions in Step` |
| Adding, changing, or re-checking a diagram | `specs/methodology/modeling-constructs.md § Diagrams` for where it goes, its form, what it may show and how it and its sources cite each other, then `.ai/skills/author-mermaid-diagram/` |

## Workflow

The rule for each step is named at the step, because that is where it is needed. Finding the fact's existing home, synchronizing whatever restates what you changed, and verifying anchors and citations mechanically are where the defects below actually get caught.

**Scope the change**, per `AGENTS.md § Design, Refactor, Refine (DRR)`, and draft it as a design entry, per `specs/methodology/working-files.md § A Design Entry`.

**Find the fact's existing home.** Grep before drafting, per `specs/methodology/sourcing-and-citation.md § One Home Per Fact`. If it has one, the work is a citation plus whatever delta is specific to the new location, and most of the steps below do not apply.

**Decide which spec it belongs to.** `specs/methodology/spec-placement.md § Product or Technical`.

**Decide its altitude, and its file.** `specs/methodology/spec-placement.md § Index, Architecture, Detail` for index versus architecture versus detail. For a product capability, `specs/methodology/spec-placement.md § Naming a Capability Domain` first, then `specs/methodology/spec-placement.md § Where a File Goes`'s test for subfolder versus root file.

**Check whether a construct applies before writing prose.** `specs/methodology/modeling-constructs.md § Purpose` decides whether a passage is a construct or prose, and `specs/methodology/modeling-constructs.md § When to Use Which` which construct it is.

**Draft with the source file open.** Anything compressed from another file is compared against it clause by clause, not re-read in isolation.

**Write the references.** `specs/methodology/sourcing-and-citation.md § Writing a Citation` for citing a section, `specs/methodology/sourcing-and-citation.md § Which Citations Are Allowed` for whether it may point where it does, `specs/methodology/sourcing-and-citation.md § Titling a Heading` for any heading added or retitled, `specs/methodology/spec-placement.md § Naming the Technical Files Behind a Capability` when a technical file now fulfills a product file's capability.

**Update the scenarios in the same pass.** `specs/methodology/acceptance-scenarios.md § Keeping a Scenario and Its Prose in Step`.

**Synchronize whatever restates what you changed.** `specs/methodology/sourcing-and-citation.md § Keeping Companions in Step`. A section you changed that a diagram renders cites that diagram, wherever it sits, so the diagram to re-check is named in the text you just edited.

A diagram is the easiest rendering to leave stale and the hardest to notice, because a wrong one is invisible in source and obvious only once rendered. Authoring or re-checking one goes through `.ai/skills/author-mermaid-diagram/`, which covers the altitude check that keeps a label inside what its host file actually states, and the render step that catches what reading the source will not.

**Strip drafting residue.** `specs/methodology/spec-style.md § What a Finished Spec Reads Like`.

**Verify every anchor and every citation mechanically.** `.ai/skills/design-specs/scripts/design-specs.py`, both modes, below. A proposal whose quoted text or cited heading does not exist cannot be applied, however sound its reasoning. Anything the script cannot decide goes to a cold subagent, per `§ Recall picks the direction; the file supplies the words`.

**Refactor and refine, then the adversarial DRR, then apply and audit**, per `AGENTS.md § Design, Refactor, Refine (DRR)`, rerunning the steps above for whatever each pass changes. In the brief, name the failure patterns this skill's sections record. The audit is `.ai/skills/audit-specs/`, whose script catches a citation left pointing at a heading that moved, and whose audits catch a summary that no longer describes what it summarizes.

## Search for the fact before drafting the sentence

Not after. Not during review. Before, because once a well-formed paragraph exists the instinct is to place it rather than delete it, and a second home for a fact is nearly invisible afterward: both copies read correctly, and they diverge later when one is edited.

The search is cheap and mechanical. Take the fact's distinctive nouns and grep for each. Take the rule's governing verb and grep for that. If a search returns a document already covering the subject, read it before writing anything, even when you are confident it says something different.

What to do when you find one is not a judgment call: `specs/methodology/sourcing-and-citation.md § One Home Per Fact` says cite the home and write only the delta specific to the new location, never re-derive or re-explain the rule. Deciding a home for the first time is the same section, and it turns on whose subject the rule is, not which file happened to need it first.

**Your own recent work is not exempt.** A document you edited earlier in the session is searched and read like any other, per `§ Recall picks the direction; the file supplies the words`.

## Compression distortion

`specs/methodology/spec-placement.md § Index, Architecture, Detail` requires `architecture.md` to describe its whole directory in its own words while not accumulating full detail, which means compressing its detail files. Every clause compressing a paragraph into a phrase is an opportunity to assert something the source does not.

The ways it goes wrong, in rough order of frequency:

- **A dropped qualifier that was load-bearing.** The source says a capability works "though never carrying X"; the summary says it works. The exception was the protection, and the overview now promises something broader than the system does.
- **A default promoted to a universal.** The source says a path is "the default" among several; the summary says it is how the thing works.
- **A count asserted where the source enumerates.** The source names two behaviors and points at a third elsewhere; the summary says "two ways," which reads as closed and is not.
- **A referent stranded by the cut.** The summary keeps "than that window allows" after deleting the clause naming the window.

Re-reading your own summary will not catch these; it will read fine. Open the source beside the clause and compare directly, asking what the source said that this does not, and whether the omission changes what a reader concludes.

## Adding a statement changes which rules apply to it

Conventions here are often conditional. `specs/methodology/acceptance-scenarios.md § Deciding What to Write` exempts a guarantee stated *only* in a cross-cutting file from needing a scenario under each capability relying on it. Add that guarantee to a capability's own section and the condition stops holding: it is now a guardrail stated in that section, and a scenario is owed.

Before adding a sentence, check which conventions currently apply because of where the fact is *not* stated. Citing the existing statement rather than restating it usually keeps the condition intact and owes nothing further, which is also what `specs/methodology/sourcing-and-citation.md § One Home Per Fact` asks for anyway.

## Never propose structure before proving the existing structure fails

New sections, new files, new domains, new notation. Each is expensive, hard to remove later, and the most satisfying thing to write.

Before proposing any, name the existing home that would have to receive the content, and say why it cannot. If you cannot name one, you have not looked hard enough. A proposal that starts from new structure and reasons toward it will always find the reasoning. The tests are already written: `specs/methodology/spec-placement.md § Where a File Goes` for whether a domain earns a subfolder or stays a root file, `specs/methodology/spec-placement.md § Naming a Capability Domain` for whether a domain exists at all, and `specs/methodology/sourcing-and-citation.md § Titling a Heading` for whether a bold lead-in should become a heading.

The strongest disconfirming question is whether the thing is ordinary. A capability every comparable system has, that a reader assumes without being told, rarely deserves its own home; what deserves stating is the part that is *not* ordinary. A generic affordance plus one unusual property is usually one sentence about the unusual property, not a file about the affordance.

## Recall picks the direction; the file supplies the words

Recall is the right instrument for deciding where to go. Which file probably holds this, what shape the change takes, which rule governs, whether the fact likely already has a home — being wrong there costs one lookup, and the lookup corrects it.

It is never the source for anything written down. A quotation, a heading path, a count, a claim that a file does or does not say something: each of those is read from the file at the moment of writing it, not recalled from having read it.

The reason is `AGENTS.md § Design, Refactor, Refine (DRR)`'s for reading fresh before any work.

The tell, when this has gone wrong, is that the *direction* was right and the *text* was not: the correct file, named with a heading it does not have. That pattern is the signature, and it means a proposal can be wholly sound in substance and entirely unapplicable.

**One instrument for each half.**

*What is mechanically decidable goes to the script*: `.ai/skills/design-specs/scripts/design-specs.py` verifies quoted text with `anchors` and cited heading paths with `citations`, per `§ Verifying anchors and citations`. They are separate modes because a proposal makes both kinds of claim, and a checker covering only quotations lets every wrong heading through — which is exactly how several of them once reached a reviewer in a single revision, in a proposal whose every quotation passed.

*What needs judgment goes to a cold subagent.* Whether a section actually states the rule being attributed to it, whether a count holds, whether "nothing in the repo says X" is true: no script decides these, and re-reading your own work does not either, for the reason `AGENTS.md § Design, Refactor, Refine (DRR)` gives. The cold subagent runs the adversarial DRR before a change lands and the post-apply audit after it.

## Names carry claims

A term smuggles in whatever its ordinary meaning implies. A word suggesting rhythm implies recurrence. A word suggesting configuration implies something holds a setting. A word suggesting choice implies an actor who chooses.

When naming anything, state the claims the word makes beyond your definition and confirm each is true. When reviewing an existing name, ask what a reader would assume from the word alone, then check whether the document supports it. Renaming is cheap before citations exist and expensive after, and `specs/methodology/sourcing-and-citation.md § Titling a Heading` requires every citation to move in the same edit.

Sometimes the answer is no name at all. If a distinction has two values that work as adjectives on something already named, the axis may not need a noun; inventing one creates a thing readers expect to be able to set.

## Numbers stated in passing

A figure quoted to support an argument gets believed and reused, including by you. A count from a quick search usually counts something adjacent to the claim: occurrences of a character rather than of the construct containing it, lines rather than matches, files rather than instances.

Verify a number before stating it, or state none. An argument needing a specific count to work is an argument needing the count to be right.

## Decline explicitly

A proposal silently omitting something looks identical to one that never considered it, and the next reader raises it again.

When you consider a change and reject it, say so and why, in the proposal. When work is real but out of scope, record it as a follow-up when it is deferred, per `specs/methodology/working-files.md § A Design Entry`. A statement that something was deliberately left alone is worth as much to the next reader as the changes.

## Hand product decisions back

Some forks are craft and yours to settle: where content goes, how a rule is worded, whether to cite or restate.

Some are not. What the product does, who may do it, what it promises a user, are decisions about the thing being specified rather than about specifying it. Present the options and consequences, recommend one, and let the person decide. Settling these quietly inside a proposal is how a specification acquires facts nobody chose.

## Verifying anchors and citations

`.ai/skills/design-specs/scripts/design-specs.py` checks that text a proposal quotes from a file it does not contain is there, and that a heading it cites is there.

    python .ai/skills/design-specs/scripts/design-specs.py anchors <manifest>
    python .ai/skills/design-specs/scripts/design-specs.py anchors -    # manifest on stdin
    python .ai/skills/design-specs/scripts/design-specs.py citations <proposal.md>

`citations` reads the proposal itself and resolves every cross-file citation span in it against the live file:

```
path/from/root.md § Parent § Child
```

It reports a missing file, a heading that does not exist, and — the most useful of these, because it names the fix — a lineage that is wrong while the title is right, printing the real lineage beside it.

It resolves a filename given in shorthand by path suffix, since a proposal is prose for a reviewer and refers back to a file whose full path it gave once. A suffix matching several files is reported rather than guessed: in a tree holding several `architecture.md` files, a bare one names nothing in particular, and a proposal relying on surrounding prose to disambiguate is relying on the reader to do it too.

A same-file citation, one with no path, is skipped. A proposal is not the file it cites into, so a bare section token in it has no file to resolve against — which also means a proposal is clearer giving the full path in every citation, even where a spec would legitimately shorten it.

The manifest is plain text. A line beginning `--- ` names a file; everything up to the next `--- ` is one anchor, verbatim, newlines included. Lines beginning `#` before the first `--- ` are comments.

    --- specs/application/product/architecture.md
    an upgrade is a discrete, versioned, customer-visible event
    --- specs/application/product/platform-and-compliance-operations/versioned-upgrades.md
    Under an Acme AI-managed upgrade, a Platform admin executes it

Each anchor reports `ok`, `missing`, or `ambiguous` with a match count. A missing anchor is retried with whitespace collapsed and says so when that is the only difference, which is the usual cause. Exit status is non-zero if anything failed, so it can gate a proposal.

Ways a quoted anchor fails, all of which the script names: the string is quoted from recall and differs in a word; the string is real but lifted from a *different* file discussing the same subject; the string appears more than once, so the edit is ambiguous.

Run both modes against every proposal, before review rather than at apply time. The script cannot tell you a proposal is right; it tells you a proposal is applicable, which is a cheaper thing to be wrong about.
