---
name: design-specs
description: Propose or revise a specification, the canon or the application specs, as a design document under .ai/plans/design-specs/. Use when adding or changing a capability, a guarantee, a mechanism, a rule, a term or a skill, reconciling two documents that disagree, closing a gap an audit or review found, or taking a change through Design, Refactor, Refine, or running a Refactor and Refine cycle over specs that have landed, the canon's or the application's, the whole or a part. Its Workflow gives each rule it applies a point-of-use citation and forks at the kind of specification changed into a reference for that kind, and it covers the failures that recur in the work, duplicating a rule that already has a home, distorting a fact while compressing it, and proposing edits whose anchors do not exist.
---

# Designing specifications

Every fact in this repo is meant to live in exactly one place. Everywhere else that needs the fact points there. Most defects introduced here are not wrong statements. They are true statements written in a second place.

That is the difficulty. A sentence you are about to write is almost always correct on its own terms. The question is never "is this true" but "is this already stated, and is this where it belongs."

This skill does not restate the repo's conventions, since restating them would be the same defect the skill exists to prevent. It says where the conventions are, and what recurs when applying them.

## Workflow

Each step applying a rule carries its point-of-use citation (`specs/methodology/sourcing-and-citation.md § One Home Per Fact`). The defects this skill's sections record get caught at the steps that find the fact's existing home, synchronize whatever restates what you changed, and verify anchors and citations mechanically.

### Start from the entry point

Read `specs/AGENTS.md`, then `specs/methodology/glossary.md`, and a directory's `index.md` before working in it, per `specs/methodology/scope.md § Progressive Disclosure` and `specs/methodology/scope.md § The Shape of the Scope`.

### Frame the change

Frame the change per `specs/AGENTS.md § Design, Refactor, Refine`. Record it in a design document in `.ai/plans/design-specs/`, copied from `.ai/skills/design-specs/references/design-document-form-template.md`, per `specs/methodology/working-files.md § A Design Document`. The design document's Kind field settles the change's kind before any file is edited. The kind also sizes the design's reviews, as `specs/methodology/design-workflow.md § A Design's Reviews` has them.

Agree on the design goals with the user first, then present the design frame, as `specs/AGENTS.md § Design, Refactor, Refine` has them come first. Record the goals as `specs/methodology/working-files.md § Design Goal` has them. Draft The Design only once the user agrees on the goals and agrees to or adjusts the frame. Record each answer as a steer.

Before the frame goes to the user, the frame tests each rule the change would otherwise state in a construct section's prose, by the test `specs/methodology/modeling-constructs.md § Defining Constructs` sets, and says which way each rule went. A close call, where either answer is arguable, goes to the user as a choice with the builder's recommendation, the canon's default where the canon gives one. The answer is recorded as a steer. A design bringing specs to the canon's forms may meet prose there that fails the test. The design writes that prose into a pass of the design that owns that construct's forms. Where no such design exists, it hands the prose to the user as `§ Workflow § Hand a change of its own to the user to spawn or log` has it.

A design taken up with its goals or its frame not yet stated has them stated, and agreed to or adjusted, before its drafting goes on. Set the design's Status as `specs/methodology/working-files.md § A Design Document § The States It Moves Through` moves it, here and at each step that moves it. Where the work wants a new branch, propose it. Create the branch only once the user approves it, per `specs/AGENTS.md § Design, Refactor, Refine`. A Refactor and Refine cycle (`specs/methodology/glossary.md`) also reads `.ai/skills/design-specs/references/refactor-and-refine-existing-specs.md` here. That reference's steps join this Workflow's from this step on.

### Hand a change of its own to the user to spawn or log

At any step of this Workflow, each of these goes to the user, who decides how it is worked (`specs/methodology/working-files.md § A Design Document`):

- a change of its own that the work turns up, such as a migration of files that a rule change leaves out of sync;
- code that a change to the specs leaves out of sync, as `specs/methodology/working-files.md § A Design Document` splits it.

Each is either spawned as a design or logged as a follow-up, as `specs/methodology/working-files.md § A Design Document` has it. A spawned design is not-started until it is taken up, and it is named in this design's Depends On if this design cannot finish without it (`specs/methodology/working-files.md § A Design Document`). A follow-up takes the form `specs/methodology/working-files.md § A Follow-up` gives. Ask rather than choose, because which suits depends on how the user means to work it. Show the user the design's or the follow-up's text, new or amended, and write it only once the user approves it.

### Revise what waited, once what it waited on finishes

When `--show-workstack` lists a design to revise (`§ Verifying a proposal`), first, if it is approved, move the design back to in progress, and move back what depends on it, as `§ Workflow § Refactor and refine, then the adversarial review, then apply and audit` has a design moved back. Its work then goes on as `specs/methodology/design-workflow.md § The Order of a Design's Work § The Work of a Design` routes it. Then take in what each finished design named in its Depends On settled, or why that design was dropped, per `specs/methodology/working-files.md § A Design Document`. Rerun `§ Workflow § Fork on the kind of specification` through `§ Workflow § Verify mechanically` for whatever that changes. Record the revision in the design's passes, and remove each finished design from Depends On. Then run `--show-workstack` again, and delete each design it lists as may be deleted.

### Record each steer and apply it

Record each steer the user gives the design, a decision about what the design is rather than about how the work proceeds, in the design's Steering Decisions when it is given, per `specs/methodology/working-files.md § Steering Decision`. Quote the user's words rather than paraphrasing them, because a paraphrase drifts toward what the builder meant. A reviewer reading the paraphrase as background then checks fidelity to a decision the user never made. Set the steer's Type as `specs/methodology/working-files.md § Steering Decision` has it.

Confirm a steer changing the goals or the frame with the user first, stating what it would change, as `specs/AGENTS.md § Design, Refactor, Refine` has it. Record any other steer as given. Then revise the design to apply the steer before the work goes on, rerunning `§ Workflow § Fork on the kind of specification` through `§ Workflow § Verify mechanically` for whatever the steer changes. The steering decisions are the history of how the design was shaped. A design lagging them leaves its reviewers reading a decision the design does not yet carry out.

A decision about other work goes where that work is held, per `specs/methodology/working-files.md § Steering Decision`, never only into your own memory. Where an approved or applying design holds the work, ask the user whether to reopen that design for the decision. Where nothing holds the work, ask whether to record a design for it or log a follow-up.

### Fork on the kind of specification

Every change is of a kind, and this skill forks on the kind (`specs/AGENTS.md § Writing specs`). A change to the canon also reads `.ai/skills/design-specs/references/canon-specs.md`. A change to the application specs also reads `.ai/skills/design-specs/references/app-specs.md`. Each reference holds the steps only that kind owes, in the order this Workflow reaches them, and each of those steps names the step it joins.

A `code` change is `.ai/skills/implement-specs/`'s, not this skill's. A `documentation` change reads neither reference, and an `other` change reads neither, except a change editing the project's root `AGENTS.md`. That change reads the canon reference, whose step adding or changing a skill holds both `AGENTS.md` files to agent-agnostic instructions.

A change needing both kinds is split, per `specs/methodology/working-files.md § A Design Document`. A canon change finds what it leaves in the application specs as `.ai/skills/design-specs/references/canon-specs.md § Workflow` has it. An application change needing the canon hands that need on as `.ai/skills/design-specs/references/app-specs.md § Workflow` has it.

### Take up the persona of what the design changes

Write as the persona `specs/methodology/spec-placement.md § Personas` gives each specification, or the documentation, that the design changes, so the persona's judgment shapes the change from its first draft rather than arriving with a review.

### Find the fact's existing home

Grep before drafting, per `specs/methodology/sourcing-and-citation.md § One Home Per Fact`. If the fact has a home, the work is a citation, plus what that section asks of a citing place. In that case, `§ Workflow § Decide its altitude, and its file` through `§ Workflow § Record what the specs rely on but have not decided` do not apply.

### Decide its altitude, and its file

`specs/methodology/spec-placement.md § Index, Architecture, Detail` decides index versus architecture versus detail. `specs/methodology/spec-placement.md § Where a File Goes` decides which file, and where the file's row sits in its directory's `index.md`, which is the order it is read in. That section also decides the file's folder or, for a root file, the domain the product `architecture.md` names it under, which decides the product module the file belongs to (`specs/methodology/spec-placement.md § A Product Module`).

### Check whether a construct applies before writing prose

`specs/methodology/modeling-constructs.md § When to Use Which` decides whether a passage is a construct or prose, by the count it sets, and which construct it is. The decision covers routing too, however the routing reads. `specs/methodology/modeling-constructs.md § When to Use Which § A Table's Construct` decides which of a Decision Table, records and a Basic Table a table is. `specs/methodology/modeling-constructs.md § When to Use Which § A Configured Instance` decides the same where a construct's rows, states or steps are the system's data. `specs/methodology/modeling-constructs.md § When to Use Which § Combining Constructs` decides how one construct hands its work to another. `specs/methodology/modeling-constructs.md § Constructs` gives the form the construct is written in.

### Draft with the source file open

Compare anything compressed from another file against that file clause by clause, rather than re-reading it in isolation. Before putting an edit in the design, zoom out and write the rule's reach whole, as `specs/AGENTS.md § Design, Refactor, Refine`'s Measure twice, cut once has it.

### Write the text in the form the rules give it

Write a field, a bold lead-in, emphasis and literal text as `specs/methodology/modeling-constructs.md § Fields`, `specs/methodology/spec-style.md § Bold Lead-ins`, `specs/methodology/spec-style.md § Emphasis` and `specs/methodology/spec-style.md § Literal Text` give them. Write an entry of a repeated kind, or a closed set's members, as `specs/methodology/modeling-constructs.md § When to Use Which § A Table's Construct` chooses: a record type's records or a Basic Table's rows. Write a number only where `specs/methodology/spec-style.md § Ordinals and Counts` keeps one.

### Record what the specs rely on but have not decided

Record it as an open question, per `specs/methodology/spec-placement.md § Open Question`, rather than hedging it inside settled prose.

### Write the references

Cite a section as `specs/methodology/sourcing-and-citation.md § Writing a Citation` gives. Refer to any other text as `specs/methodology/sourcing-and-citation.md § Writing a Citation § Referring to Other Text` gives. `specs/methodology/sourcing-and-citation.md § Which Citations Are Allowed` decides whether a citation may point where it does. `specs/methodology/sourcing-and-citation.md § Titling a Heading` governs any heading added or retitled.

### Synchronize whatever restates what you changed

Follow `specs/methodology/sourcing-and-citation.md § Keeping Specs in Sync`. A section you changed that a diagram renders cites that diagram, wherever the diagram sits, so the diagram to re-check is named in the text you just edited.

A diagram is the easiest view to leave stale and the hardest to notice, because a wrong one is invisible in source and obvious only once rendered. Author or re-check a diagram as `specs/methodology/modeling-constructs.md § Diagrams` has it, through `.ai/skills/author-mermaid-diagram/`. That skill covers the altitude check that keeps a label inside what its host file states. It also covers the render step that catches what reading the source will not.

### Strip drafting residue, and write clearly

Follow `specs/methodology/spec-style.md § What a Finished Spec Reads Like`, `specs/methodology/spec-style.md § Trade-offs Are Not Journey Language` for a comparison kept, and `specs/methodology/spec-style.md § Clear Prose` for prose its primary reader understands on the first read.

### Verify mechanically

Run `.ai/skills/design-specs/scripts/design-specs.py`, per `§ Verifying a proposal`: `--check-quoted-text` for every quoted anchor, `--check-cited-headings` for every cited heading, and `--check-design` for the design document's form, its Target against its Kind, each quoted edit applying, each citation resolving, and the design's place in the workstack.

Run `--check-design` and `--check-cited-headings` with `--with-edits-of` naming each design whose form this design's record uses, as `specs/methodology/working-files.md § A Design Document` has a form the methodology is still adding. `--check-quoted-text` takes `--with-edits-of` only for another design, never this one, because a copy holding this design's edits no longer holds this design's anchors.

A proposal whose quoted text or cited heading does not exist cannot be applied, however sound its reasoning. Anything the script cannot decide goes to a cold agent, as a judgment the builder hands off, per `specs/AGENTS.md § Design, Refactor, Refine § Who Checks What` and `§ Recall picks the direction; the file supplies the words`.

### Refactor and refine, then the adversarial review, then apply and audit

Work the design in the order `specs/methodology/design-workflow.md § The Order of a Design's Work` gives, per `specs/AGENTS.md § Design, Refactor, Refine`. Rerun `§ Workflow § Fork on the kind of specification` through `§ Workflow § Verify mechanically` for whatever each pass changes. What this skill adds at the states of its two machines, each named where it acts:

- **Checking your own work.** Check your own work at drafting, validating and writing, as its row of `specs/AGENTS.md § Design, Refactor, Refine § Who Checks What` sets. Read the design against its problem, too, and against the rules this Workflow's steps apply. At validating, also match what the design does to `--show-edits`, per `§ Verifying a proposal`.
- **Offering a review's model and effort.** At drafting, offer the user a review's model and effort once for a design, before its first adversarial review. Where the user's approval ends the review before any round, offer them before its post-apply audit instead. The post-apply audit at writing starts on the same choice, as `specs/AGENTS.md § Design, Refactor, Refine` has the choice kept. Offer two choices, each lettered with its default first. For effort: (a) the level the design's Kind gives (`specs/methodology/design-workflow.md § A Design's Reviews`) or (b) another, named in the answer. For model: (a) the one you run on or (b) another you can start a reviewer on, named in the answer. Offer only a level you can apply, as `specs/methodology/design-workflow.md § A Review's Effort` has it, and say which levels you cannot apply. Name the model and the effort in the review's pass.
- **Briefing the adversarial review.** At reviewing, brief the adversarial review with the complete design document, its Design Goals and its Steering Decisions among it. Give the review the design's goals as the yardstick, the failure patterns this skill's sections record, and the decisions earlier rounds' findings fell on. Ask the review only what its row of `specs/AGENTS.md § Design, Refactor, Refine § Who Checks What` gives it. Frame it as the persona of each specification, or the documentation, that the design changes, as `specs/methodology/spec-placement.md § Personas` has it.
- **Settling a round.** At settling, settle the round per `specs/AGENTS.md § Design, Refactor, Refine § Settling a Round`. Record each review's pass as `specs/methodology/working-files.md § A Design Document` has it.
- **The validation review.** At validating, run `--stamp-validation`, adding `--with-edits-of` as `specs/methodology/working-files.md § A Design Document` has a form the methodology is still adding. The script checks the design document's validity by the record's checks that section sets. Once the design passes, the script stamps it, in the form `specs/methodology/working-files.md § A Stamp` gives. Fix each problem the script reports and run it again. None of those problems is a question for the user. A design still validated, read with `--show-validation`, goes on as `specs/methodology/design-workflow.md § The Order of a Design's Work § The Work of a Design` routes it.
- **An approval that ends the review.** Where the user approves the design's text anywhere in its work, record the approval in a pass, saying whether it was given with apply. Let the state in hand finish its own work, leaving a round still running or being settled with its findings as they are. Where the approval was given in reassessing, apply the round's settled change first, so the user approves the text again. Then go on to validating, as `specs/methodology/design-workflow.md § The Order of a Design's Work § The Work of a Design` routes it. Once stamped, the design is approved. It is applied where the approval said so, once `specs/methodology/working-files.md § A Design Document § The States It Moves Through` lets it move into applying.
- **Asking for approval.** At awaiting approval, ask for approval as a choice of approved, approved and apply, or not approved, so the answer is a word and the user can approve a design and pause. Where the user's approval had ended the review, another round is a choice too. Approved moves the design's Status to approved. Approved and apply moves it to approved and begins the apply. Offer approved and apply only once `specs/methodology/working-files.md § A Design Document § The States It Moves Through` would let the design move into applying. Not approved keeps the design in progress. Whatever the user says with that answer is a steer where it decides what the design is, per `specs/methodology/working-files.md § Steering Decision`.
- **Applying.** At the states of `specs/methodology/design-workflow.md § The Order of a Design's Work § The Apply`, move the design's Status to applying only once `specs/methodology/working-files.md § A Design Document § The States It Moves Through` lets it. Once the design's edits are in, run `--refresh-links`, per `specs/methodology/sourcing-and-citation.md § Writing a Citation § A Citation's Link`. Settle each finding of the post-apply audit with the user by the Decision Table in `specs/methodology/working-files.md § A Design Document § Changes After Approval`, taking its rows in their order. Revert the changes of a design sent back to in progress, through version control where the project has it. Commit the design's changes on their own, one commit for the design, on the user's go-ahead, and move its Status to complete. An applying design the user abandons has the edits it wrote reverted first, per `specs/methodology/working-files.md § A Design Document`. The audit is `.ai/skills/audit-specs/`, forking on the same kind and asked only what its row of `specs/AGENTS.md § Design, Refactor, Refine § Who Checks What` gives it. Its script catches a citation left pointing at a heading that moved. Its audits catch a summary that no longer describes what it summarizes.
- **Moving a design back.** Whenever a design moves back to in progress, run `--check-workstack`, per `§ Verifying a proposal`. Move back each approved design it reports depending on one not approved, per `specs/methodology/working-files.md § A Design Document`. Run it again until it reports none.

## Search for the fact before drafting the sentence

Not after. Not during review. Search before, because once a well-formed paragraph exists, the instinct is to place it rather than delete it. A second home for a fact is nearly invisible afterward. Both copies read correctly, and they diverge later when one is edited.

The search is cheap and mechanical. Take the fact's distinctive nouns and grep for each. Take the rule's governing verb and grep for that. If a search returns a document already covering the subject, read it before writing anything, even when you are confident it says something different.

`specs/methodology/sourcing-and-citation.md § One Home Per Fact` says what to do when you find one: cite the home, and add what it asks of a citing place. Deciding a home for the first time follows the same section. The decision turns on whose subject the rule is, not on which file happened to need it first.

**Your own recent work is not exempt.** A document you edited earlier in the session is searched and read like any other, per `§ Recall picks the direction; the file supplies the words`.

## Compression distortion

`specs/methodology/spec-placement.md § Index, Architecture, Detail` requires `architecture.md` to describe its directory, every directory beneath it, and what `specs/methodology/spec-placement.md § What an Overview Describes` names beyond it, in its own words and without accumulating full detail. Meeting that requirement means compressing its detail files. Every clause compressing a paragraph into a phrase is an opportunity to assert something the source does not.

The ways it goes wrong, in rough order of frequency:

- **A dropped qualifier that was load-bearing.** The source says a capability works "though never carrying X". The summary says it works. The exception was the protection, and the overview now promises something broader than the system does.
- **A default promoted to a universal.** The source says a path is "the default" among several. The summary says it is how the thing works.
- **A count asserted where the source enumerates.** The source names two behaviors and points at a third elsewhere. The summary says "two ways," which reads as closed and is not.
- **A referent stranded by the cut.** The summary keeps "than that window allows" after deleting the clause naming the window.

Re-reading your own summary will not catch these, because it will read fine. Open the source beside the clause and compare the two directly. Ask what the source said that the clause does not, and whether the omission changes what a reader concludes.

## Never propose structure before proving the existing structure fails

New sections, new files, new domains, new notation. Each is expensive, hard to remove later, and the most satisfying thing to write. That is how a Rube Goldberg machine gets built where the aim is elegance (`specs/methodology/glossary.md`).

Before proposing any, name the existing home that would have to receive the content, and say why it cannot. If you cannot name one, you have not looked hard enough. A proposal that starts from new structure and reasons toward it will always find the reasoning. The tests are already written: `specs/methodology/spec-placement.md § Where a File Goes` for whether a domain earns a subfolder or stays a root file, `specs/methodology/spec-placement.md § Naming a Capability Domain` for whether a domain exists at all, and `specs/methodology/sourcing-and-citation.md § Titling a Heading` for whether a bold lead-in should become a heading.

The strongest disconfirming question is whether the thing is ordinary. A capability every comparable system has, one a reader assumes without being told, rarely deserves its own home. What deserves stating is the part that is *not* ordinary. A generic affordance plus one unusual property is usually one sentence about the unusual property, not a file about the affordance.

A column, a field or a form added to a construct's own tables is decided by the test `specs/methodology/modeling-constructs.md § Defining Constructs` sets, not by this rule alone. The section's prose is the existing structure, and that prose fails where the test says it does.

## Recall picks the direction; the file supplies the words

Recall is the right instrument for deciding where to go: which file probably holds this, what shape the change takes, which rule governs, whether the fact likely already has a home. Being wrong there costs one lookup, and the lookup corrects it.

Recall is never the source for anything written down. A quotation, a heading path, a count, a claim that a file does or does not say something: each of those is read from the file at the moment of writing it, not recalled from having read it.

The reason is the one `specs/AGENTS.md § Design, Refactor, Refine` gives for reading fresh before any work.

When this has gone wrong, the tell is that the *direction* was right and the *text* was not: the correct file, named with a heading it does not have. That pattern is the signature. It means a proposal can be wholly sound in substance and entirely unapplicable.

**One instrument for each half.**

**What is mechanically decidable goes to the script.** `.ai/skills/design-specs/scripts/design-specs.py` verifies quoted text with `--check-quoted-text`, cited heading paths with `--check-cited-headings` and a design document with `--check-design`, per `§ Verifying a proposal`. They are separate checks because a proposal makes both kinds of claim. A checker covering only quotations lets every wrong heading through. That is how several wrong headings once reached a reviewer in a single revision, in a proposal whose every quotation passed.

**What needs judgment goes to a cold agent.** Whether a section states the rule attributed to it, whether a count holds, whether "nothing in the repo says X" is true: no script decides these. Re-reading your own work does not decide them either, for the reason `specs/AGENTS.md § Design, Refactor, Refine` gives. While drafting, that cold agent's check is a judgment the builder hands off. Over the whole design, the check is the adversarial review and then the post-apply audit, each as its row of `specs/AGENTS.md § Design, Refactor, Refine § Who Checks What` sets.

## Names carry claims

A term smuggles in whatever its ordinary meaning implies. A word suggesting rhythm implies recurrence. A word suggesting configuration implies something holds a setting. A word suggesting choice implies an actor who chooses.

When naming anything, state the claims the word makes beyond your definition and confirm each is true. When reviewing an existing name, ask what a reader would assume from the word alone, then check whether the document supports it. Renaming is cheap before citations exist and expensive after. `specs/methodology/sourcing-and-citation.md § Titling a Heading` requires every citation to move in the same edit.

Sometimes the answer is no name at all. If a distinction has two values that work as adjectives on something already named, the axis may not need a noun. Inventing one creates a thing readers expect to be able to set.

A term Spec of Record itself would give a meaning of its own is a change to the canon, made as `.ai/skills/design-specs/references/canon-specs.md` says.

## Numbers stated in passing

A figure quoted to support an argument gets believed and reused, including by you. A count from a quick search usually counts something adjacent to the claim: occurrences of a character rather than of the construct containing it, lines rather than matches, files rather than instances.

Verify a number before stating it, or state none. An argument needing a specific count to work is an argument needing the count to be right.

## Decline explicitly

A proposal silently omitting something looks identical to one that never considered it, and the next reader raises it again.

When you consider a change and reject it, say so and why, in the proposal. When work is real but out of scope, hand it to the user to spawn as a design, or to log as a follow-up when it is deferred, per `specs/methodology/working-files.md § A Design Document`. A follow-up takes the form `specs/methodology/working-files.md § A Follow-up` gives. A statement that something was deliberately left alone is worth as much to the next reader as the changes.

## Verifying a proposal

`.ai/skills/design-specs/scripts/design-specs.py` checks that text a proposal quotes from a file it does not contain is there, and that a heading the proposal cites is there. It checks that a design document, and the workstack the design documents draw, hold together. It also lists a design's edits, and shows what a Refactor and Refine cycle changed. These checks and this skill's steps hold a design document to its form, per `specs/methodology/working-files.md § A Design Document`. The script's checks are flags, per `specs/methodology/skills.md § Authoring a Skill`. The exit status is 0 when every check passes, 1 when one finds a problem, and 2 for a usage error, so a run can gate a proposal.

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
    python .ai/skills/design-specs/scripts/design-specs.py --check-design <design-document> --with-edits-of <design-document>
    python .ai/skills/design-specs/scripts/design-specs.py --show-edits <design-document>
    python .ai/skills/design-specs/scripts/design-specs.py --show-refactor-and-refine-of-existing-specs <baseline-commit>

`--check-design-form` checks a design document against `specs/methodology/working-files.md § A Design Document`, `specs/methodology/working-files.md § Design Goal` and `specs/methodology/working-files.md § Steering Decision`. It checks:

- its heading, its fields in order, a file named for its Name, a Status that is a state, and a Target of paths;
- its sections in order, a canon design's Impact on the Application Specs among them and no other design's;
- its Design Goals' records against the Design Goal type its declaration gives, each Name a slug used once, and each citation of a goal in its design frame naming one;
- its design frame's headings in order and, once it is approved, neither its goals nor a part of its frame reading `Not yet stated.`;
- each edit of The Design in a form its row gives, `This text:` then `becomes:`, or `A new file:`;
- each steering decision's fields, and its Type one of the values the field allows;
- a design approved or further carrying a stamp, current while it is approved;
- each adversarial review's and post-apply audit's pass naming the model and reasoning effort it ran on, its lead-in written exactly as that section sets it.

`--check-target-kind` reads the design's Kind field. It checks that every file the design's Target names is of that kind, or is a file of `documentation` or `other`, by the kinds `specs/methodology/working-files.md § A Design Document § The Kinds of Change` defines. `--check-target-kind` decides the canon and application paths alone. Whether a file is the application's code is set by the code roots the technical stack names, which `.ai/skills/verify-spec-implementation/` reads.

`--check-design` runs both. It reports each quoted edit that does not apply and each citation that does not resolve, as the record's checks The edits and References have them, while the design's Status is in-progress or approved. It reports where `specs/methodology/working-files.md § Steering Decision` does not declare the Steering Decision type, or `specs/methodology/working-files.md § Design Goal` the Design Goal type, since this tooling reads the records' fields from those declarations. It also reports what `--check-workstack` finds wrong with that design. Any problem any of these reports counts, whatever it is filed under.

`--show-workstack` reads every design document under `.ai/plans/design-specs/`, unless given another directory. It also reads every design document in the other skills' plans folders beside it, because a workstack spans designs, a design changing code among them, which `.ai/skills/implement-specs/` writes and revises. A design in another folder prints as that folder's name, a slash and its file name. `--stamp-validation` reads the same folders.

`--show-workstack` draws the tree from each design's Spawned By and Depends On. It marks each design blocked, with a finished design to take in, or, while it is in progress or approved, validated or validation stale. It lists the designs ready to work, the one the most open designs wait on first, the blocked ones apart, and the finished ones no design names in its Depends On, which may be deleted. `--check-workstack` reads the same designs. It reports a Status out of sync with what the design depends on, a Depends On naming no design, and a loop in Depends On or Spawned By.

`--show-refactor-and-refine-of-existing-specs` shows, through git, what a Refactor and Refine cycle changed in the specs and the skills since its baseline commit, per `.ai/skills/design-specs/references/refactor-and-refine-existing-specs.md`. It reads a heading without its level, and sets bare markup aside. It shows every line of six words or more now repeated more often than at the baseline, every line now held fewer times than at the baseline, and every line held more times, each with the files holding it. It decides nothing and exits 0, because whether a repeat is a second home or one made by design, and what each loss or gain traces to, is a reader's to judge. It runs from the repository's root, on a working tree with the cycle's changes applied.

`--show-validation` prints a design's stamped hash, its hash as it stands, and whether it is validated, stale or never stamped. The script compares the hashes, and they are never compared by hand.

`--stamp-validation` refuses a design whose Depends On names a design not approved or applying, among them a finished one to be taken in first. It refuses such a design because a design is validated only once each design it names is approved or applying, per `specs/methodology/working-files.md § A Design Document`. Otherwise `--stamp-validation` runs `--check-design`. When that finds nothing but the stamp's own absence, and neither the design's goals nor a part of its design frame reads `Not yet stated.`, it writes the stamp `specs/methodology/working-files.md § A Stamp` sets into the Validated field. It leaves a current stamp as it is, so the stamp's date stays that of the review that earned it. The builder runs it at validating, as `specs/methodology/working-files.md § A Design Document` has the validation review. Every check it stamps on is the script's own, so a stamp vouches for nothing a reader had to judge.

`--with-edits-of` runs the other actions asked for in a copy of the repository's root files, specs, skills and plans that holds a design's quoted edits, as `specs/methodology/working-files.md § A Design Document` has a form the methodology is still adding. An edit already applied is taken as applied. A stamp written in the copy is copied back.

How each of the record's checks (`specs/methodology/working-files.md § A Design Document`) is decided, `--stamp-validation` running `--check-design` before it stamps:

**Reference Key:** Check

**Required:** Decided By

| Check | Decided By |
|---|---|
| Form | `--check-design` for the heading, the fields in order and their values, the Kind among them, the sections, the frame's headings and, by the time it is validated, no goal and no part of its frame not yet stated |
| Records | `--check-design` for each record's fields, its Type's values, each goal's Name a slug and each Name used once |
| The edits | `--check-design` for each quoted edit applying to its file exactly once, or already applied; an edit to code a copy `--with-edits-of` builds does not hold checked by `--check-quoted-text` |
| References | `--check-design` for each citation resolving in the files as they stand or as the design's own edits leave them, each goal the frame cites one the design holds, and each design its Depends On names existing |

`--show-edits` lists every edit of a design document's The Design, in the forms `specs/methodology/working-files.md § A Design Document` gives. It lists each edit by its line and the file it edits, with the words it removes from the text it replaces and the words it adds, or every word of a new file. The listing is untruncated and sets quote markers and fences aside, so the builder and the adversarial review match what the design does to one listing. It decides nothing and exits 0, because whether a clause states an edit is a reader's to judge.

`--check-cited-headings` reads the proposal itself and resolves every cross-file citation span in it against the live file:

```
path/from/root.md § Parent § Child
```

It reports a missing file, a heading that does not exist, and a lineage that is wrong while the title is right. For a wrong lineage, it prints the real lineage beside it. That report is the most useful of these, because it names the fix.

It resolves a filename given in shorthand by path suffix, because a proposal is prose for a reviewer and refers back to a file whose full path it gave once. A suffix matching several files is reported rather than guessed. In a tree holding several `architecture.md` files, a bare one names nothing in particular. A proposal relying on surrounding prose to disambiguate is relying on the reader to do it too.

A same-file citation, one with no path, is skipped. A proposal is not the file it cites into, so a bare section token in it has no file to resolve against. So a proposal is clearer giving the full path in every citation, even where a spec would legitimately shorten it.

The manifest `--check-quoted-text` reads takes the form the script's `--help` gives. The `--help` is that form's home, because the script's actions are the code the skills share in `.ai/skills/lib/design_documents.py`. `.ai/skills/implement-specs/` runs that code through its own entry script too.

Each anchor reports `ok`, `missing`, or `ambiguous` with a match count. A missing anchor is retried with whitespace collapsed, and the report says so when whitespace is the only difference, which is the usual cause.

Ways a quoted anchor fails, each of which the script names:

- the string is quoted from recall and differs in a word;
- the string is real but lifted from a *different* file discussing the same subject;
- the string appears more than once, so the edit is ambiguous.

Run every check against every proposal before review, rather than at apply time. Run `--show-refactor-and-refine-of-existing-specs` on a working tree with the proposal's changes applied. The script cannot tell you a proposal is right. It tells you a proposal is applicable, which is a cheaper thing to be wrong about.
