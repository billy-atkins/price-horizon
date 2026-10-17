---
name: implement-specs
description: Design and write the code that carries the application specs out. Use when specs have been applied and the code must follow them, the first time or after they change; when governed code or the tests that check a spec are to be written, fixed or restructured; or when wiring must connect them. It designs the code from the specs as a design document, taken through Design, Refactor, Refine, then an adversarial review and a validation review for the user to approve or steer, then writes the governed code with its app-spec annotations, the wiring and the tests, and checks its own work before `verify-spec-implementation` reads it.
---

# Implementing the specs

The specs say what the code does. This skill writes the code that does it. It starts where `design-specs` ends, from applied specs. It designs the code and the tests that bring the specs to life, as `design-specs` designs a change to the specs. Once this skill's best effort is exhausted, `verify-spec-implementation` reads its work, as `audit-specs` reads a design's. The steps guard against a unit doing more or less than the spec it cites, a citation higher or lower than what the unit carries out, governed code changed with no spec behind the change, and wiring that carries out a rule no spec states.

## Workflow

Each step applying a rule carries its point-of-use citation (`specs/methodology/sourcing-and-citation.md § One Home Per Fact`). The script is `scripts/implement-specs.py`, the only one this skill runs. Its `--help` gives its actions and the manifest `--check-quoted-text` reads. Each action reads this skill's plans folder and the other plans folders beside it. A name in another folder is printed as that folder's name, a slash and the file name.

### Start from the entry point

Read `specs/AGENTS.md` and the glossary before any step. Descend only as far as a step needs, per `specs/methodology/scope.md § Progressive Disclosure`. Propose a new branch for the work, and create it only on the user's approval, per `specs/AGENTS.md § Design, Refactor, Refine`.

### Start from the specs

Design the code from the specs as they stand, or as a design named in the design's Depends On leaves them. Do so the first time, or after the specs change. Write code only from specs that stand applied. Move the design's Status to in-progress as you take it up. A change to what governed code must do that no spec yet states goes to the specs first, per `specs/methodology/code.md § Changing Code`. Code written ahead of its spec is code no spec governs.

### Write the design

Write the design as the persona `specs/methodology/spec-placement.md § Personas` gives the code. Copy `references/design-document-template.md` to a file of its own under `.ai/plans/implement-specs/`, per `specs/methodology/working-files.md § A Design Document § A Design Changing Code`. Scope the design to one product module, per `specs/methodology/spec-placement.md § A Product Module`. Fill it from that module's specs, reading what `specs/methodology/spec-placement.md § A Product Module` sets, fresh, in the order `specs/methodology/scope.md § Progressive Disclosure` sets. Follow a section's citations rather than loading whole files beyond the module. Stop at a gap `specs/methodology/spec-placement.md § A Product Module` names, or at a local environment the specs do not give, per `specs/methodology/spec-placement.md § Environments`. Present what stopped you to the user as a gap the specs must put right.

Agree on the design goals with the user, then present the design frame, as `specs/AGENTS.md § Design, Refactor, Refine` has both. Record the goals as `specs/methodology/working-files.md § Design Goal` has them. Only once the user agrees on the goals and agrees to or adjusts the frame, describe the following in The Design, finding the code that carries a spec out by searching for its annotations rather than reading the codebase:

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

Take the design through the Design, Refactor, Refine process, per `specs/AGENTS.md § Design, Refactor, Refine`. Get it working, refactor it until it stops moving, and refine it by reading each cited spec against the unit citing it: no unit carries out more than it cites, and no wiring carries out a rule a spec states.

Check the design mechanically with `scripts/implement-specs.py --check-design`, `--check-quoted-text` and `--check-cited-headings`. Run `--check-design` and `--check-cited-headings` with `--with-edits-of` naming each design whose form the design's record uses, as `specs/methodology/working-files.md § A Design Document` has a form the methodology is still adding. Run `--check-quoted-text` without it, since the copy it builds holds no code.

At `specs/methodology/design-workflow.md § The Order of a Design's Work § The Work of a Design [States.State: drafting]`, check the whole design yourself. At drafting too, before its first adversarial review, offer the user the reviewer's model and reasoning effort. Where the user's approval ends the review before any round, make that offer before its post-apply audit. The effort defaults to the one `specs/methodology/design-workflow.md § A Design's Reviews` gives code, as `specs/methodology/design-workflow.md § A Review's Effort` has it.

At the design's reviewing state, run a cold agent's adversarial review over it, per `specs/AGENTS.md § Design, Refactor, Refine`. Brief the review with the complete design, its Design Goals as the yardstick, the specs it implements, and the decisions earlier rounds' findings fell on. Ask the review only what its row of `specs/AGENTS.md § Design, Refactor, Refine § Who Checks What` gives it. Frame it as the persona `specs/methodology/spec-placement.md § Personas` gives the code. Settle each round of the adversarial review per `specs/AGENTS.md § Design, Refactor, Refine § Settling a Round`. Record each review's pass as `specs/methodology/working-files.md § A Design Document` has it.

Once the design reaches `specs/methodology/design-workflow.md § The Order of a Design's Work § The Work of a Design [States.State: validating]`, run the validation review, `scripts/implement-specs.py --stamp-validation`. Add `--with-edits-of` as `specs/methodology/working-files.md § A Design Document` has a form the methodology is still adding. Fix each problem the validation review reports, and run it again until it stamps the design. Where the design quotes the existing code it changes, match what the design does against `scripts/implement-specs.py --show-edits`.

Where the user approves the design's text anywhere in its work, record the approval in a pass, saying whether the user gave it with apply. Let the state in hand finish its own work. A round still running or being settled is left with its findings as they are. Then go on to validating, as the same state machine routes it. Once stamped, the design is approved. It is applied where the approval said so, once `specs/methodology/working-files.md § A Design Document § The States It Moves Through` lets it move into applying. Once the approval has ended the review, the user may ask for another round at awaiting approval.

### Ask for approval

Ask for approval as a choice of approved, approved and apply, or not approved. Where the user's approval had ended the review, also offer another round. Each choice moves the design as `specs/methodology/working-files.md § A Design Document § The States It Moves Through` has a design move. Offer approved and apply only once that section would let the design move into applying.

### Write the code

Once `specs/methodology/working-files.md § A Design Document § The States It Moves Through` lets the design's Status move to applying, move it. Then write what the design holds:

- the governed code, with its annotations above each unit, per `specs/methodology/code.md § Citing the Specs From Code`;
- the wiring, carrying no annotations;
- the tests.

Write them in American English, per `specs/methodology/code.md § Changing Code`. As you write, run the targeted form of the local environment's test tasks on the tests citing the specs the code carries out, per `specs/methodology/spec-placement.md § Environments`. Change governed code only as the design says, per `specs/methodology/code.md § Changing Code`. A change the design does not hold sends the design back, and the code written is reverted, as `specs/methodology/design-workflow.md § The Order of a Design's Work § The Apply [States.State: sent back]` has it. A change no spec states goes back to the specs.

### Check your own work, then verify-spec-implementation's

Before anyone else reads the code, check it against the design, per `specs/AGENTS.md § Design, Refactor, Refine`. Check that:

- every unit is written;
- every annotation names a heading that exists, is sorted, and is as narrow as the unit;
- the wiring carries no spec's rule;
- what you wrote is in American English;
- every build, lint and test task of the local environment passes, after the targeted tests citing the specs the code carries out, which you ran as you worked, per `specs/methodology/spec-placement.md § Environments`.

`specs/methodology/spec-placement.md § Environments` also says what to present where the specs give no such tasks. Record the check in the design's passes.

`.ai/skills/verify-spec-implementation/` is the design's post-apply audit, at `specs/methodology/design-workflow.md § The Order of a Design's Work § The Apply [States.State: auditing]`. It is asked only what its row of `specs/AGENTS.md § Design, Refactor, Refine § Who Checks What` gives it. Settle each finding with the user by `specs/methodology/working-files.md § A Design Document § Changes After Approval`. Revert the code you wrote where that section's table sends the design back. Commit the code on the user's go-ahead, at `specs/methodology/design-workflow.md § The Order of a Design's Work § The Apply [States.State: awaiting the commit]`, as one commit for the design. Then move the design's Status to complete.
