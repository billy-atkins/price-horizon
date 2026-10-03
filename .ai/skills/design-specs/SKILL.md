---
name: design-specs
description: Propose or revise a specification, the canon or the application specs, as a design document under .ai/plans/design-specs/. Use when adding or changing a capability, a guarantee, a mechanism, a rule, a term or a skill, reconciling two documents that disagree, closing a gap an audit or review found, or taking a change through Design, Refactor, Refine, or running a Refactor and Refine cycle over specs that have landed, the canon's or the application's, the whole or a part. Its Workflow gives each rule it applies a point-of-use citation and forks at the kind of specification changed into a reference for that kind, and it covers the failures that recur in the work, duplicating a rule that already has a home, distorting a fact while compressing it, and proposing edits whose anchors do not exist.
---

# Designing specifications

Every fact in this repo is supposed to live in exactly one place, and everywhere else that needs it points there. Most defects introduced here are not wrong statements. They are true statements written in a second place.

That is the difficulty. A sentence you are about to write is almost always correct on its own terms. The question is never "is this true" but "is this already stated, and is this where it belongs."

This skill does not restate the repo's conventions, which would be the same defect it exists to prevent. It says where they are and what recurs when applying them.

## Workflow

Each step applying a rule carries its point-of-use citation (`specs/methodology/sourcing-and-citation.md § One Home Per Fact`). Finding the fact's existing home, synchronizing whatever restates what you changed, and verifying anchors and citations mechanically are where the defects this skill's sections record actually get caught.

### Start from the entry point

`specs/AGENTS.md`, then `specs/methodology/glossary.md`, and a directory's `index.md` before working in it, per `specs/methodology/scope.md § Progressive Disclosure` and `specs/methodology/scope.md § The Shape of the Scope`.

### Scope the change

Scope it per `specs/AGENTS.md § Design, Refactor, Refine`, and draft it as a design document in `.ai/plans/design-specs/`, copied from `.ai/skills/design-specs/references/design-document-template.md`, per `specs/methodology/working-files.md § A Design Document`, its Specs field settling the change's kind before any file is edited. Set its Status as that section's lifecycle moves it, here and at each step that moves it. Where the work wants a new branch, propose it, and create it only once the user approves it, per `specs/AGENTS.md § Design, Refactor, Refine`. A Refactor and Refine cycle (`specs/methodology/glossary.md`) also reads `.ai/skills/design-specs/references/refactor-and-refine-existing-specs.md` here, whose steps join this Workflow's from this one on.

### Hand a change of its own to the user to spawn or log

At any step of this Workflow, a change of its own that the work turns up, a migration of files a rule change leaves out of step among them, and code a change to the specs leaves out of step, as `specs/methodology/working-files.md § A Design Document` splits it, goes to the user, who decides how it is worked, per `specs/methodology/working-files.md § A Design Document`: spawned as a design, not-started until it is taken up and named in this design's Depends On if this design cannot finish without it, or logged as a follow-up, per `specs/methodology/working-files.md § A Follow-up`. Ask rather than choose: which suits depends on how the user means to work it.

### Revise what waited, once what it waited on finishes

When `--show-workstack`, per `§ Verifying a proposal`, lists a design to revise, move it back to in progress first if it is approved, since it is validated and approved again, moving back what depends on it as `§ Workflow § Refactor and refine, then the adversarial review, then apply and audit` has a design moved back, then take in what each finished design its Depends On names settled, or why it was dropped, per `specs/methodology/working-files.md § A Design Document`, rerunning `§ Workflow § Fork on the kind of specification` through `§ Workflow § Verify mechanically` for whatever that changes. Record the revision in its passes, remove each from Depends On, and delete each design `--show-workstack` then lists as may be deleted.

### Record each steer and apply it

Each steer the user gives the design, a decision about what the design is rather than about how the work proceeds, goes into its Steering Decisions when it is given, per `specs/methodology/working-files.md § A Steering Decision`, the user's words quoted rather than paraphrased: a paraphrase drifts toward what the builder meant, and a reviewer reading it as background then checks fidelity to a decision the user never made. Then revise the design to apply it, rerunning `§ Workflow § Fork on the kind of specification` through `§ Workflow § Verify mechanically` for whatever it changes, before the work goes on: the steering decisions are the history of how the design was shaped, and a design lagging them leaves its reviewers reading a decision the design does not yet carry out. A decision about other work goes where that work is held, per `specs/methodology/working-files.md § A Steering Decision`, never only into your own memory; where an approved or applying design holds the work, ask the user whether to reopen it for the decision, and where nothing holds the work, whether to record a design for it or log a follow-up.

### Fork on the kind of specification

Every change is of a kind, and this skill forks on it (`specs/AGENTS.md § Writing specs`). A change to the canon also reads `.ai/skills/design-specs/references/canon-specs.md`, a change to the application specs `.ai/skills/design-specs/references/app-specs.md`: each holds the steps only that kind owes, in the order this Workflow reaches them, each naming the step it joins. A `code` change is `.ai/skills/implement-specs/`'s, not this skill's. A `neither` change reads neither, except that one editing the project's root `AGENTS.md` reads the canon reference, whose step adding or changing a skill holds both `AGENTS.md` files to agent-agnostic instructions. A change needing both kinds is split, per `specs/methodology/working-files.md § A Design Document`: a canon change finds what it leaves in the application specs as `.ai/skills/design-specs/references/canon-specs.md § Workflow` has it, and an application change needing the canon hands that on as `.ai/skills/design-specs/references/app-specs.md § Workflow` has it.

### Take up each specification's persona

Write as the persona `specs/methodology/spec-placement.md § Personas` gives each specification the design changes, so its persona's judgment shapes the change from its first draft rather than arriving with a review.

### Find the fact's existing home

Grep before drafting, per `specs/methodology/sourcing-and-citation.md § One Home Per Fact`. If it has one, the work is a citation, plus what that section asks of a citing place, and `§ Workflow § Decide its altitude, and its file` through `§ Workflow § Record what the specs rely on but have not decided` do not apply.

### Decide its altitude, and its file

`specs/methodology/spec-placement.md § Index, Architecture, Detail` for index versus architecture versus detail, and `specs/methodology/spec-placement.md § Where a File Goes` for which file, and where its row sits in its directory's `index.md`, which is the order it is read in, its folder, or, for a root file, the domain the product `architecture.md` names it under, deciding the product module it belongs to (`specs/methodology/spec-placement.md § A Product Module`).

### Check whether a construct applies before writing prose

`specs/methodology/modeling-constructs.md § Purpose` decides whether a passage is a construct or prose, `specs/methodology/modeling-constructs.md § When to Use Which` which construct it is, and `specs/methodology/modeling-constructs.md § Constructs` the form it is written in.

### Draft with the source file open

Anything compressed from another file is compared against it clause by clause, not re-read in isolation. Before putting an edit in the design, read what surrounds the text it changes as well as that text, per `specs/AGENTS.md § Design, Refactor, Refine`.

### Write the text in the form the rules give it

A field, a bold lead-in, emphasis and literal text as `specs/methodology/modeling-constructs.md § Fields`, `specs/methodology/modeling-constructs.md § Bold Lead-ins`, `specs/methodology/modeling-constructs.md § Emphasis` and `specs/methodology/modeling-constructs.md § Literal Text` give them, an entry of a repeated kind as `specs/methodology/modeling-constructs.md § Constructs § Record Form` does, and a number only where `specs/AGENTS.md § Ordinals and Counts` keeps one.

### Record what the specs rely on but have not decided

Record it as an open question, per `specs/methodology/spec-placement.md § An Open Question`, rather than hedging it inside settled prose.

### Write the references

`specs/methodology/sourcing-and-citation.md § Writing a Citation` for citing a section, `specs/methodology/sourcing-and-citation.md § Writing a Citation § Referring to Other Text` for referring to any other text, `specs/methodology/sourcing-and-citation.md § Which Citations Are Allowed` for whether it may point where it does, and `specs/methodology/sourcing-and-citation.md § Titling a Heading` for any heading added or retitled.

### Synchronize whatever restates what you changed

`specs/methodology/sourcing-and-citation.md § Keeping Renderings in Step`. A section you changed that a diagram renders cites that diagram, wherever it sits, so the diagram to re-check is named in the text you just edited.

A diagram is the easiest rendering to leave stale and the hardest to notice, because a wrong one is invisible in source and obvious only once rendered. Authoring or re-checking one follows `specs/methodology/modeling-constructs.md § Diagrams` through `.ai/skills/author-mermaid-diagram/`, which covers the altitude check that keeps a label inside what its host file actually states, and the render step that catches what reading the source will not.

### Strip drafting residue

`specs/methodology/spec-style.md § What a Finished Spec Reads Like`, and `specs/methodology/spec-style.md § Trade-offs Are Not Journey Language` for a comparison kept.

### Verify mechanically

`.ai/skills/design-specs/scripts/design-specs.py`, per `§ Verifying a proposal`: `--check-quoted-text` for every quoted anchor, `--check-cited-headings` for every cited heading, and `--check-design` for the design document's form, its Target against its Specs, and its place in the workstack. A proposal whose quoted text or cited heading does not exist cannot be applied, however sound its reasoning. Anything the script cannot decide goes to a cold subagent, per `§ Recall picks the direction; the file supplies the words`.

### Refactor and refine, then the adversarial review, then apply and audit

Per `specs/AGENTS.md § Design, Refactor, Refine`, rerunning `§ Workflow § Fork on the kind of specification` through `§ Workflow § Verify mechanically` for whatever each pass changes. Before the adversarial review, before the validation review, and before the post-apply audit, each after your last edit, check the whole of the work yourself, per `specs/AGENTS.md § Design, Refactor, Refine`: the design against its problem and against the rules this Workflow's steps apply, its record against what the validation review reads (`specs/methodology/working-files.md § A Design Document`), and, before the post-apply audit, the applied files against the design's edits. Before the adversarial review, and again before the post-apply audit, offer the user the reviewer's model and reasoning effort as two choices, per `specs/AGENTS.md § Design, Refactor, Refine`, each lettered with its default first: effort (a) medium, (b) light or (c) high; model (a) the one you run on or (b) another you can start a reviewer on, named in the answer. Offer only what you can apply, saying which you cannot: a reasoning effort you set as you start a reviewer, or through the reviewer definition you were set up with for it; where you could apply a reasoning effort once set up, offer to set yourself up first, per `specs/methodology/skills.md § Setting Up an Agent`. Run the review as chosen, or as you allow, and name both in its pass. Give the reviewer the complete design document, its Steering Decisions among it, and in the brief name the failure patterns this skill's sections record; frame an adversarial review's reviewer as the persona of each specification the design changes, as `specs/methodology/spec-placement.md § Personas` has it. Record in each review's pass the flaws the user settled among its findings, per `specs/methodology/working-files.md § A Design Document`, and where its phase has reached the run of rounds with flaws `specs/AGENTS.md § Design, Refactor, Refine` sets, revise no further: take the design to the user to reassess. Once its findings are taken in and each design its Depends On names is approved or applying, since a design is validated and approved only then, per `specs/methodology/working-files.md § A Design Document`, and before the user is asked to approve, read the design's validation with `--show-validation`, per `§ Verifying a proposal`: a design still validated goes to the user as it is, and one stale or never stamped goes first to a cold agent running the validation review `specs/methodology/working-files.md § A Design Document` sets, briefed with the complete design document, its report going to `.ai/tmp/design-specs/`; it stamps the design with `--stamp-validation`, in the form `specs/methodology/working-files.md § A Stamp` gives. Ask for approval as a choice of approved, approved and apply, or not approved, so the answer is a word and the user can approve a design and pause, leaving nothing pending: approved moves its Status to approved; approved and apply moves it to approved and begins the apply, and is offered only once its Depends On names none, since a design is applied only then; not approved keeps it in progress, whatever the user says with it being a steer where it decides what the design is, per `specs/methodology/working-files.md § A Steering Decision`. Begin the apply only once its Depends On names none, nothing else is uncommitted and no other design is applying in the checkout, and move its Status to applying. Settle each finding of the post-apply audit with the user as `specs/methodology/working-files.md § A Design Document` has changes after approval: make each tactical fix the user approves as a direct edit, recording it in the audit's pass; hand on application work; record a finding the user sets aside, with the reason; and for a flaw, or a fix the user does not approve, move the design back to in progress and revert its changes to the files, through version control where the project has it. Whenever a design moves back to in progress, run `--check-workstack`, per `§ Verifying a proposal`, and move back each approved design it reports depending on one not approved, per `specs/methodology/working-files.md § A Design Document`, running it again until it reports none. Once each finding is settled, commit the design's changes on their own, one commit for the design, on the user's go-ahead, and move its Status to complete. An applying design the user abandons has the edits it wrote reverted first, per `specs/methodology/working-files.md § A Design Document`. The audit is `.ai/skills/audit-specs/`, forking on the same kind, whose script catches a citation left pointing at a heading that moved, and whose audits catch a summary that no longer describes what it summarizes.

## Search for the fact before drafting the sentence

Not after. Not during review. Before, because once a well-formed paragraph exists the instinct is to place it rather than delete it, and a second home for a fact is nearly invisible afterward: both copies read correctly, and they diverge later when one is edited.

The search is cheap and mechanical. Take the fact's distinctive nouns and grep for each. Take the rule's governing verb and grep for that. If a search returns a document already covering the subject, read it before writing anything, even when you are confident it says something different.

`specs/methodology/sourcing-and-citation.md § One Home Per Fact` says what to do when you find one: cite the home, and add what it asks of a citing place. Deciding a home for the first time is the same section, and it turns on whose subject the rule is, not which file happened to need it first.

**Your own recent work is not exempt —** a document you edited earlier in the session is searched and read like any other, per `§ Recall picks the direction; the file supplies the words`.

## Compression distortion

`specs/methodology/spec-placement.md § Index, Architecture, Detail` requires `architecture.md` to describe its whole directory in its own words while not accumulating full detail, which means compressing its detail files. Every clause compressing a paragraph into a phrase is an opportunity to assert something the source does not.

The ways it goes wrong, in rough order of frequency:

- **A dropped qualifier that was load-bearing —** the source says a capability works "though never carrying X"; the summary says it works. The exception was the protection, and the overview now promises something broader than the system does.
- **A default promoted to a universal —** the source says a path is "the default" among several; the summary says it is how the thing works.
- **A count asserted where the source enumerates —** the source names two behaviors and points at a third elsewhere; the summary says "two ways," which reads as closed and is not.
- **A referent stranded by the cut —** the summary keeps "than that window allows" after deleting the clause naming the window.

Re-reading your own summary will not catch these; it will read fine. Open the source beside the clause and compare directly, asking what the source said that this does not, and whether the omission changes what a reader concludes.

## Never propose structure before proving the existing structure fails

New sections, new files, new domains, new notation. Each is expensive, hard to remove later, and the most satisfying thing to write, which is how a Rube Goldberg machine gets built where the aim is elegance (`specs/methodology/glossary.md`).

Before proposing any, name the existing home that would have to receive the content, and say why it cannot. If you cannot name one, you have not looked hard enough. A proposal that starts from new structure and reasons toward it will always find the reasoning. The tests are already written: `specs/methodology/spec-placement.md § Where a File Goes` for whether a domain earns a subfolder or stays a root file, `specs/methodology/spec-placement.md § Naming a Capability Domain` for whether a domain exists at all, and `specs/methodology/sourcing-and-citation.md § Titling a Heading` for whether a bold lead-in should become a heading.

The strongest disconfirming question is whether the thing is ordinary. A capability every comparable system has, that a reader assumes without being told, rarely deserves its own home; what deserves stating is the part that is *not* ordinary. A generic affordance plus one unusual property is usually one sentence about the unusual property, not a file about the affordance.

## Recall picks the direction; the file supplies the words

Recall is the right instrument for deciding where to go. Which file probably holds this, what shape the change takes, which rule governs, whether the fact likely already has a home — being wrong there costs one lookup, and the lookup corrects it.

It is never the source for anything written down. A quotation, a heading path, a count, a claim that a file does or does not say something: each of those is read from the file at the moment of writing it, not recalled from having read it.

The reason is `specs/AGENTS.md § Design, Refactor, Refine`'s for reading fresh before any work.

The tell, when this has gone wrong, is that the *direction* was right and the *text* was not: the correct file, named with a heading it does not have. That pattern is the signature, and it means a proposal can be wholly sound in substance and entirely unapplicable.

**One instrument for each half —**

**What is mechanically decidable goes to the script —** `.ai/skills/design-specs/scripts/design-specs.py` verifies quoted text with `--check-quoted-text`, cited heading paths with `--check-cited-headings` and a design document with `--check-design`, per `§ Verifying a proposal`. They are separate checks because a proposal makes both kinds of claim, and a checker covering only quotations lets every wrong heading through — which is exactly how several of them once reached a reviewer in a single revision, in a proposal whose every quotation passed.

**What needs judgment goes to a cold subagent —** whether a section actually states the rule being attributed to it, whether a count holds, whether "nothing in the repo says X" is true: no script decides these, and re-reading your own work does not either, for the reason `specs/AGENTS.md § Design, Refactor, Refine` gives. The cold subagent runs the adversarial review before a change lands and the post-apply audit after it.

## Names carry claims

A term smuggles in whatever its ordinary meaning implies. A word suggesting rhythm implies recurrence. A word suggesting configuration implies something holds a setting. A word suggesting choice implies an actor who chooses.

When naming anything, state the claims the word makes beyond your definition and confirm each is true. When reviewing an existing name, ask what a reader would assume from the word alone, then check whether the document supports it. Renaming is cheap before citations exist and expensive after, and `specs/methodology/sourcing-and-citation.md § Titling a Heading` requires every citation to move in the same edit.

Sometimes the answer is no name at all. If a distinction has two values that work as adjectives on something already named, the axis may not need a noun; inventing one creates a thing readers expect to be able to set.

A term Spec of Record itself would give a meaning of its own is a change to the canon, made as `.ai/skills/design-specs/references/canon-specs.md` says.

## Numbers stated in passing

A figure quoted to support an argument gets believed and reused, including by you. A count from a quick search usually counts something adjacent to the claim: occurrences of a character rather than of the construct containing it, lines rather than matches, files rather than instances.

Verify a number before stating it, or state none. An argument needing a specific count to work is an argument needing the count to be right.

## Decline explicitly

A proposal silently omitting something looks identical to one that never considered it, and the next reader raises it again.

When you consider a change and reject it, say so and why, in the proposal. When work is real but out of scope, hand it to the user to spawn as a design or log as a follow-up when it is deferred, per `specs/methodology/working-files.md § A Design Document`, a follow-up in the form `specs/methodology/working-files.md § A Follow-up` gives. A statement that something was deliberately left alone is worth as much to the next reader as the changes.

## Verifying a proposal

`.ai/skills/design-specs/scripts/design-specs.py` checks that text a proposal quotes from a file it does not contain is there, that a heading it cites is there, and that a design document, and the workstack the design documents draw, hold together, and shows what a Refactor and Refine cycle changed. These checks and this skill's steps are what hold one to its form, per `specs/methodology/working-files.md § A Design Document`. Its checks are flags, per `specs/methodology/skills.md § Authoring a Skill`, and the exit status is 0 when every check passes, 1 when one finds a problem, and 2 for a usage error, so a run can gate a proposal.

    python .ai/skills/design-specs/scripts/design-specs.py --check-quoted-text <manifest>
    python .ai/skills/design-specs/scripts/design-specs.py --check-quoted-text -    # manifest on stdin
    python .ai/skills/design-specs/scripts/design-specs.py --check-cited-headings <proposal>
    python .ai/skills/design-specs/scripts/design-specs.py --check-design-form <design-document>
    python .ai/skills/design-specs/scripts/design-specs.py --check-target-kind <design-document>
    python .ai/skills/design-specs/scripts/design-specs.py --check-design <design-document>
    python .ai/skills/design-specs/scripts/design-specs.py --check-workstack [plans-dir]
    python .ai/skills/design-specs/scripts/design-specs.py --show-workstack [plans-dir]
    python .ai/skills/design-specs/scripts/design-specs.py --show-validation <design-document>
    python .ai/skills/design-specs/scripts/design-specs.py --stamp-validation <design-document>
    python .ai/skills/design-specs/scripts/design-specs.py --show-refactor-and-refine-of-existing-specs <baseline-commit>

`--check-design-form` checks a design document against `specs/methodology/working-files.md § A Design Document` and `specs/methodology/working-files.md § A Steering Decision`: its heading, its fields in order, a file named for its Name, a Status that is a state, a Target of paths, its sections in order, a canon design's Impact on the Application Specs among them and no other design's, each steering decision's fields, a design approved or further naming an adversarial review in its passes and carrying a stamp, current while it is approved, and each adversarial review's and post-apply audit's pass naming the model and reasoning effort it ran on, its lead-in written exactly as that section sets it. `--check-target-kind` reads its Specs field and checks every file its Target names is of that kind or of `neither`, by the kinds `specs/methodology/working-files.md § A Design Document` defines. `--check-target-kind` decides the canon and application paths alone: whether a file is the application's code is set by the code roots the technical stack names, which `.ai/skills/verify-spec-implementation/` reads. `--check-design` runs both, and reports what `--check-workstack` finds wrong with that design; any problem any of them reports counts, whatever it is filed under.

`--show-workstack` reads every design document under `.ai/plans/design-specs/`, unless given another directory, and every one in the other skills' plans folders beside it, since a workstack spans designs, a design changing code among them, which `.ai/skills/implement-specs/` writes and revises; a design in another folder prints as that folder's name, a slash and its file name, and `--stamp-validation` reads the same folders. It draws the tree from each design's Spawned By and Depends On, marking each design blocked, with a finished design to take in, or validated or validation stale while it is in progress or approved; lists the designs ready to work, the one the most open designs wait on first, the blocked ones apart, and the finished ones no design names in its Depends On, which may be deleted. `--check-workstack` reads the same designs and reports a Status out of step with what the design depends on, a Depends On naming no design, and a loop in Depends On or Spawned By.

`--show-refactor-and-refine-of-existing-specs` shows, through git, what a Refactor and Refine cycle changed in the specs and the skills since its baseline commit, per `.ai/skills/design-specs/references/refactor-and-refine-existing-specs.md`, a heading read without its level and bare markup set aside: every line of six words or more now repeated more often than at the baseline, every line now held fewer times than at the baseline, and every line held more times, each with the files holding it. It decides nothing and exits 0, since whether a repeat is a second home or one made by design, and what each loss or gain traces to, is a reader's to judge; it runs from the repository's root, on a working tree with the cycle's changes applied.

`--show-validation` prints a design's stamped hash, its hash as it stands, and whether it is validated, stale or never stamped, the hashes compared by the script and never by hand. `--stamp-validation` refuses a design whose Depends On names a design not approved or applying, a finished one to be taken in first, since one is validated only once each design it names is approved or applying, per `specs/methodology/working-files.md § A Design Document`, and otherwise runs `--check-design` and, when that finds nothing but the stamp's own absence, writes the stamp `specs/methodology/working-files.md § A Stamp` sets into the Validated field, leaving a current stamp as it is, so its date stays that of the review that earned it. The validation review runs it, once its reading checks pass, and the builder never does: a stamp the builder wrote would vouch for reading checks no one made.

`--check-cited-headings` reads the proposal itself and resolves every cross-file citation span in it against the live file:

```
path/from/root.md § Parent § Child
```

It reports a missing file, a heading that does not exist, and — the most useful of these, because it names the fix — a lineage that is wrong while the title is right, printing the real lineage beside it.

It resolves a filename given in shorthand by path suffix, since a proposal is prose for a reviewer and refers back to a file whose full path it gave once. A suffix matching several files is reported rather than guessed: in a tree holding several `architecture.md` files, a bare one names nothing in particular, and a proposal relying on surrounding prose to disambiguate is relying on the reader to do it too.

A same-file citation, one with no path, is skipped. A proposal is not the file it cites into, so a bare section token in it has no file to resolve against — which also means a proposal is clearer giving the full path in every citation, even where a spec would legitimately shorten it.

The manifest `--check-quoted-text` reads takes the form the script's `--help` gives, its home, since the script's actions are the code the skills share in `.ai/skills/lib/design_documents.py`, which `.ai/skills/implement-specs/` runs through its own entry script too.

Each anchor reports `ok`, `missing`, or `ambiguous` with a match count. A missing anchor is retried with whitespace collapsed and says so when that is the only difference, which is the usual cause.

Ways a quoted anchor fails, all of which the script names: the string is quoted from recall and differs in a word; the string is real but lifted from a *different* file discussing the same subject; the string appears more than once, so the edit is ambiguous.

Run every check against every proposal, before review rather than at apply time, `--show-refactor-and-refine-of-existing-specs` reading the proposal's changes applied in a working tree. The script cannot tell you a proposal is right; it tells you a proposal is applicable, which is a cheaper thing to be wrong about.
