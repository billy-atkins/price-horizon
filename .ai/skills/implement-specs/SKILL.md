---
name: implement-specs
description: Design and write the code that carries the application specs out. Use when specs have been applied and the code must follow them, the first time or after they change; when governed code or the tests that check a spec are to be written, fixed or restructured; or when wiring must connect them. It plans the code from the specs as a design document whose steps state outcomes, taken through Design, Refactor, Refine, a validation review and an adversarial review for the user to approve or steer, then at the apply writes the governed code with its app-spec annotations, the wiring and the tests, makes its self-review, and takes it through a post-apply review, the user's review and `verify-spec-implementation`'s audit.
---

# Implementing the specs

The specs say what the code does. This skill writes the code that does it. It starts where `design-specs` ends, from applied specs. It designs the code and the tests that bring the specs to life, as `design-specs` designs a change to the specs. Once this skill's best effort is exhausted, `verify-spec-implementation`'s full run audits the code, as `audit-specs`' run audits the specs. The steps guard against a unit doing more or less than the spec it cites, a citation higher or lower than what the unit carries out, governed code changed with no spec behind the change, and wiring that carries out a rule no spec states.

## Workflow

Each step applying a rule carries its point-of-use citation (`specs/methodology/sourcing-and-citation.md § One Home Per Fact`). The script is `scripts/implement-specs.py`, the only one this skill runs. Its `--help` gives its actions. Its workstack actions read this skill's plans folder and the other plans folders beside it, and its validation review draws only on the design and the canon's declarations of its form. A name in another folder is printed as that folder's name, a slash and the file name.

Each step runs in the phase its work belongs to. A step deciding what the code does runs on the design's plan steps, before validation. A step writing the code, or checking what was written, runs at the apply (`specs/methodology/design-workflow.md § The Order of a Design's Work § The Apply`).

### Start from the entry point

Read `specs/AGENTS.md` and the glossary before any step. Descend only as far as a step needs, per `specs/methodology/scope.md § Progressive Disclosure`. Propose a new branch for the work, and create it only on the user's approval, per `specs/AGENTS.md § Design, Refactor, Refine`.

### Start from the specs

Design the code from the specs as they stand, or as a design named in the design's Depends On leaves them. Do so the first time, or after the specs change. Write code only from specs that stand applied. Move the design's Status to in-progress as you take it up. A change to what governed code must do that no spec yet states goes to the specs first, per `specs/methodology/code.md § Changing Code`. Code written ahead of its spec is code no spec governs.

### Write the design

Write the design as the persona `specs/methodology/spec-placement.md § Personas` gives the code. Copy `references/design-document-form-template.md` to a file of its own under `.ai/plans/implement-specs/`, per `specs/methodology/working-files.md § A Design Document § A Design Changing Code`. Scope the design to one product module, per `specs/methodology/spec-placement.md § A Product Module`. Fill it from that module's specs, reading what `specs/methodology/spec-placement.md § A Product Module` sets, fresh, in the order `specs/methodology/scope.md § Progressive Disclosure` sets. Follow a section's citations rather than loading whole files beyond the module. Stop at a gap `specs/methodology/spec-placement.md § A Product Module` names, or at a local environment the specs do not give, per `specs/methodology/spec-placement.md § Environments`. Present what stopped you to the user as a gap the specs must put right.

Agree on the design goals with the user, then present the design frame, as `specs/AGENTS.md § Design, Refactor, Refine` has both. Record the goals as `specs/methodology/working-files.md § Design Goal` has them. Only once the user agrees on the goals and agrees to or adjusts the frame, state the design's steps, each a record of the type `specs/methodology/working-files.md § Design Plan Step` declares, its Objectives the state the code holds once it is applied, never the code that brings it about. Find the code that carries a spec out by searching for its annotations rather than reading the codebase. The steps reach:

- each unit of governed code and its app-spec annotations, the narrowest citations that together state what the unit carries out, per `specs/methodology/code.md § Citing the Specs From Code`;
- the wiring that connects the units, per `specs/methodology/code.md § Governed Code and Wiring Code`;
- the tests that check the specs, per `specs/methodology/code.md § Tests`.

### Stop at annotations out of sync

Whenever you meet existing annotations, while writing the design or the code, read them against `specs/methodology/code.md § Changing Code`. That section says when they stop the work and how the work resumes. Present each annotation that stops the work to the user with its file, its line and what it fails: the rule in `specs/methodology/code.md` or the spec it no longer matches. Name the fix-it design the user decides in this design's Depends On, per `specs/methodology/working-files.md § A Design Document`, so the workstack holds the wait. Resume as revising what waited has it, against the code and the specs as they then stand.

### Sort each steer, and each gap you find

The specs are the starting point, so you draft the design of the code and the tests from them on your own. The user approves the design or steers it, as the human in the loop for the code as for the specs. Record each steer, per `specs/methodology/working-files.md § Steering Decision`, and sort it first. A steer deciding how the code carries out the specs belongs to this design. A steer changing what a spec states, whether a promise, a rule or a mechanism, is a decision about the specs. Spawn it as a design changing the specs, with the steer as that design's Source where the steer asks for the work, per `specs/methodology/working-files.md § Steering Decision`. Name the spawned design in this design's Depends On, so this design is blocked until the spawned one finishes, per `specs/methodology/working-files.md § A Design Document`. Ask the user when a steer could be either. A gap you find yourself, a spec the code needs that none states, goes to the user to spawn the same way. Any other change of its own the work turns up goes to the user to spawn or log, per `specs/methodology/working-files.md § A Design Document`.

### Revise what waited, once the specs it waited on change

When `scripts/implement-specs.py --show-workstack` lists this design to revise, move it back to in progress if it is approved. Its work then goes on as `specs/methodology/design-workflow.md § The Order of a Design's Work § The Work of a Design` routes it. Move back each approved design that `--check-workstack` then reports as depending on this one. Take in what each finished design named in this design's Depends On settled, or why it was dropped, against the specs as they now stand. Then remove that design from Depends On, per `specs/methodology/working-files.md § A Design Document`. The code is designed against the specs it will carry out, not the specs it was first drafted from.

### Design, Refactor, Refine, then the reviews

Take the steps through the Design, Refactor, Refine process, per `specs/AGENTS.md § Design, Refactor, Refine`, and again for each step a change moves. Get them working, refactor them until they stop moving, and refine them by reading each cited spec against the unit a step states: no unit carries out more than it cites, and no wiring carries out a rule a spec states (`specs/methodology/code.md § Governed Code and Wiring Code`).

Then, at the end of `specs/methodology/design-workflow.md § The Order of a Design's Work § The Work of a Design [States.State: drafting]` and of changing, before the design goes to validating, make your self-review for the adversarial review that follows, as your row of `specs/AGENTS.md § Design, Refactor, Refine § Who Checks What` sets. Run `--check-cited-headings` for each spec the design cites, and `--check-target-kind` for its Target, as part of it. So the work runs Design, Refactor, Refine, your self-review, the validation, then the adversarial review.

At drafting too, before its first adversarial review, offer the user the reviewer's model and reasoning effort. Where the user's approval ends the review before any round, make that offer before its post-apply review. The post-apply review and the audit start on the same choice. The effort defaults to the one `specs/methodology/design-workflow.md § A Design's Reviews` gives code, as `specs/methodology/design-workflow.md § A Review's Effort` has it.

At `specs/methodology/design-workflow.md § The Order of a Design's Work § The Work of a Design [States.State: validating]`, run `scripts/implement-specs.py --check-workstack` first, and put right what it reports. Then run the validation review: `--check-design` before an adversarial round, and `--stamp-validation` on the way to the user's approval, which stamps the design once it passes. Fix each problem the script reports, and run it again.

At the design's reviewing state, start a cold agent with the brief `specs/methodology/design-workflow.md § A Review's Brief` holds, naming the adversarial review, its blanks filled and nothing added, the report a file under `.ai/tmp/implement-specs/`, as `specs/methodology/working-files.md § The Working Files` gives a skill's output. Settle each round of the adversarial review per `specs/AGENTS.md § Design, Refactor, Refine § Settling a Round`. Before each fix, zoom out as `specs/AGENTS.md § Design, Refactor, Refine`'s Measure twice, cut once has it, and write the fix whole across every place stating the fact it changes. At changing, prove the change by your self-review, never by rereading the fix alone. Record each review's pass as `specs/methodology/working-files.md § A Design Document` has it.

Where the user approves the plan anywhere in its work, record the approval in a pass, saying whether the user gave it with apply. Let the state in hand finish its own work. A round still running or being settled is left with its findings as they are. Then go on to validating, as the same state machine routes it. Once stamped, the design is approved. It is applied where the approval said so, once `specs/methodology/working-files.md § A Design Document § The States It Moves Through` lets it move into applying. Once the approval has ended the review, the user may ask for another round at awaiting approval.

### Ask for approval

Ask for approval as a choice of approved, approved and apply, or not approved. Where the user's approval had ended the review, also offer another round. Each choice moves the design as `specs/methodology/working-files.md § A Design Document § The States It Moves Through` has a design move. Offer approved and apply only once that section would let the design move into applying.

### Write the code

Once `specs/methodology/working-files.md § A Design Document § The States It Moves Through` lets the design's Status move to applying, move it. At `specs/methodology/design-workflow.md § The Order of a Design's Work § The Apply [States.State: writing]`, write what the steps state, within the Target and with no change asking its own approval, since the user's approval of the plan authorizes it (`specs/methodology/working-files.md § A Design Document`). Write from the files as they stand, the code a send-back kept among them, keeping what the steps reach and removing what they do not, as `specs/methodology/working-files.md § A Design Document § The States It Moves Through § A Send-back` has it. Write:

- the governed code, with its annotations above each unit, per `specs/methodology/code.md § Citing the Specs From Code`;
- the wiring, carrying no annotations;
- the tests.

Write them in American English, per `specs/methodology/code.md § Changing Code`. As you write, run the targeted form of the local environment's test tasks on the tests citing the specs the code carries out, per `specs/methodology/spec-placement.md § Environments`. Change governed code only through this design, per `specs/methodology/code.md § Changing Code`, and only as the steps reach, per `specs/methodology/working-files.md § A Design Document`. A change the steps do not hold is a finding that the plan cannot be delivered as its steps state it. Take it to the user, whose triage of it as lying in the plan sends the design back with the code written kept in place, as `specs/methodology/design-workflow.md § The Order of a Design's Work § The Apply [States.State: sent back]` has it, and nothing is reverted. A change no spec states goes back to the specs. At every state of the apply, before acting on anything the user says, tell it apart by `specs/methodology/working-files.md § Steering Decision § Telling a Steer Apart`, as `specs/AGENTS.md § Design, Refactor, Refine`'s Measure twice, cut once has it, and act by its route: feedback on the applied result is taken in while writing, never as a steer. Where the user's words ask for a route the canon does not have, say so and name the canon's route before acting.

### Check what you wrote, then the post-apply review, the audit and the commit

Before anyone else reads the code, make your self-review for the post-apply review that follows, as your row of `specs/AGENTS.md § Design, Refactor, Refine § Who Checks What` sets. As part of it, check that:

- every unit is written;
- every annotation names a heading that exists, is sorted, and is as narrow as the unit (`specs/methodology/code.md § Citing the Specs From Code`);
- the wiring carries no spec's rule (`specs/methodology/code.md § Governed Code and Wiring Code`);
- what you wrote is in American English (`specs/methodology/code.md § Changing Code`);
- every build, lint and test task of the local environment passes, after the targeted tests citing the specs the code carries out, which you ran as you worked, per `specs/methodology/spec-placement.md § Environments`.

`specs/methodology/spec-placement.md § Environments` also says what to present where the specs give no such tasks. Record the check in the design's passes.

At the end of writing, start a cold agent with the brief `specs/methodology/design-workflow.md § A Review's Brief` holds, naming the post-apply review, its blanks filled and nothing added, the report a file under `.ai/tmp/implement-specs/`, as `specs/methodology/working-files.md § The Working Files` gives a skill's output. Settle its round per `specs/AGENTS.md § Design, Refactor, Refine § Settling a Round`, fixing its nits in the code. Before each fix, zoom out as `specs/AGENTS.md § Design, Refactor, Refine`'s Measure twice, cut once has it, and write the fix whole across every place stating the fact it changes. Before the next round, or before the user's review where none follows, prove the change by your self-review, never by rereading the fix alone. A finding lying in the plan goes to the user, whose triage sends the design back. At `specs/methodology/design-workflow.md § The Order of a Design's Work § The Apply [States.State: user reviewing]`, show the user the applied code and the post-apply review's pass, and ask for a choice of approving the applied result, another round, or feedback, which goes back to writing.

At `specs/methodology/design-workflow.md § The Order of a Design's Work § The Apply [States.State: auditing]`, start a cold agent on each audit `specs/methodology/design-workflow.md § A Design's Reviews` picks from the kinds of the files the Target names: `.ai/skills/verify-spec-implementation/`, given its name alone, as the user starts one, and, where the Target names a file of another kind, `.ai/skills/audit-specs/`, given those kinds as its `--kind`. At settling the audit, read each finding against the diff of the files the apply altered, still uncommitted, against the last commit, and triage it as caused by the design or not, as `specs/AGENTS.md § Design, Refactor, Refine` has an audit read. Settle each finding with the user by `specs/methodology/working-files.md § A Design Document § Changes After Approval`. A design that section's table sends back keeps the code written in place, as `specs/methodology/working-files.md § A Design Document § The States It Moves Through § A Send-back` has it. Commit the code on the user's go-ahead, at `specs/methodology/design-workflow.md § The Order of a Design's Work § The Apply [States.State: awaiting the commit]`, as one commit for the design. Then move the design's Status to complete.
