---
name: implement-specs
description: Design and write the code that carries the application specs out. Use when specs have been applied and the code must follow them, the first time or after they change; when governed code or the tests that check a spec are to be written, fixed or restructured; or when wiring must connect them. It designs the code from the specs as a design document, taken through Design, Refactor, Refine, then an adversarial review and a validation review for the user to approve or steer, then writes the governed code with its app-spec annotations, the wiring and the tests, and checks its own work before `verify-spec-implementation` reads it.
---

# Implementing the specs

The specs say what the code does; this skill writes the code that does it. It starts where `design-specs` ends, from applied specs, and designs the code and the tests that bring them to life, as `design-specs` designs a change to the specs; once its best effort is exhausted, `verify-spec-implementation` reads its work, as `audit-specs` reads a design's. Its steps guard against a unit doing more or less than the spec it cites, a citation higher or lower than what the unit carries out, governed code changed with no spec behind the change, and wiring that carries out a rule no spec states.

## Workflow

Each step applying a rule carries its point-of-use citation (`specs/methodology/sourcing-and-citation.md § One Home Per Fact`). The script is `scripts/implement-specs.py`, the only one this skill runs; `--help` gives its actions and the manifest `--check-quoted-text` reads, each reading this skill's plans folder and the others beside it, names in another printed as that folder's name, a slash and the file name.

### Start from the entry point

Read `specs/AGENTS.md` and the glossary before any step, and descend only as far as a step needs, per `specs/methodology/scope.md § Progressive Disclosure`. Propose a new branch for the work, and create it only on the user's approval, per `specs/AGENTS.md § Design, Refactor, Refine`.

### Start from the specs

Design the code from the specs as they stand, or as a design its Depends On names leaves them, the first time or after they change, and write code only from specs that stand applied; move the design's Status to in-progress as you take it up. A change to what governed code must do that no spec yet states goes to the specs first, per `specs/methodology/code.md § Changing Code`: code written ahead of its spec is code no spec governs.

### Write the design

Write it as the persona `specs/methodology/spec-placement.md § Personas` gives the code. Copy `references/design-document-template.md` to a file of its own under `.ai/plans/implement-specs/`, per `specs/methodology/working-files.md § A Design Document § A Design Changing Code`, scope it to one product module, per `specs/methodology/spec-placement.md § A Product Module`, and fill it from that module's specs, reading what that section sets, fresh, in the order `specs/methodology/scope.md § Progressive Disclosure` sets, following a section's citations rather than loading whole files beyond the module, and stopping at a gap that section names, or a local environment the specs do not give, per `specs/methodology/spec-placement.md § Environments`, presenting it to the user as one the specs must put right, and finding the code that carries a spec out by searching for its annotations rather than reading the codebase: each unit of governed code and its app-spec annotations, the narrowest citations that together state what the unit carries out, per `specs/methodology/code.md § Citing the Specs From Code`; the wiring that connects the units, per `specs/methodology/code.md § Governed Code and Wiring Code`; and the tests that check the specs, per `specs/methodology/code.md § Tests`.

### Stop at annotations out of step

Whenever you meet existing annotations, as the design is written or the code, read them against `specs/methodology/code.md § Changing Code`, which says when they stop the work and how it resumes. Present each one that stops it to the user with its file, its line and what it fails, the rule in `specs/methodology/code.md` or the spec it no longer matches; name the fix-it design the user decides in this design's Depends On, per `specs/methodology/working-files.md § A Design Document`, so the workstack holds the wait; and resume as revising what waited has it, against the code and the specs as they then stand.

### Sort each steer, and each gap you find

The specs are the starting point, so you draft the design of the code and the tests from them on your own; the user approves it or steers it, the human in the loop for the code as for the specs. Record each steer, per `specs/methodology/working-files.md § A Steering Decision`, and sort it first. One deciding how the code carries out the specs is this design's. One changing what a spec states, a promise, a rule, a mechanism, is a decision about the specs: spawn it as a design changing the specs, the steer its Source where it asks for the work, per `specs/methodology/working-files.md § A Steering Decision`, and name it in this design's Depends On, so this design is blocked until it finishes, per `specs/methodology/working-files.md § A Design Document`. Ask the user when a steer could be either. A gap you find yourself, a spec the code needs and none states, goes to the user to spawn the same way, and any other change of its own the work turns up goes to the user to spawn or log, per `specs/methodology/working-files.md § A Design Document`.

### Revise what waited, once the specs it waited on change

When `scripts/implement-specs.py --show-workstack` lists this design to revise, move it back to in progress if it is approved, moving back each approved design `--check-workstack` then reports depending on it, take in what each finished design its Depends On names settled, or why it was dropped, against the specs as they now stand, and remove it from Depends On, per `specs/methodology/working-files.md § A Design Document`: the code is designed against the specs it will carry out, not the specs it was first drafted from.

### Design, Refactor, Refine, then the reviews

Take the design through `specs/AGENTS.md § Design, Refactor, Refine`: get it working, refactor it until it stops moving, and refine it, reading each cited spec against the unit citing it, no unit carrying out more than it cites, and no wiring carrying out a rule a spec states. Check it mechanically with `scripts/implement-specs.py --check-design`, `--check-quoted-text` and `--check-cited-headings`, then check the whole design yourself, offer the user the reviewer's model and reasoning effort, and run a cold agent's adversarial review over it, per `specs/AGENTS.md § Design, Refactor, Refine`, briefed with the complete design and the specs it implements and framed as the persona `specs/methodology/spec-placement.md § Personas` gives the code. Once its findings are taken in, a cold agent runs the validation review `specs/methodology/working-files.md § A Design Document` sets, and stamps the design with `scripts/implement-specs.py --stamp-validation`.

### Ask for approval

Ask for approval as a choice of approved, approved and apply, or not approved, as `specs/methodology/working-files.md § A Design Document § The States It Moves Through` has a design move, approved and apply offered only once its Depends On names none.

### Write the code

On the go-ahead, with nothing else uncommitted and no other design applying in the checkout, move the design's Status to applying and write what it holds: the governed code with its annotations above each unit, per `specs/methodology/code.md § Citing the Specs From Code`; the wiring, carrying none; and the tests. As you write, run the targeted form of the local environment's test tasks on the tests citing the specs the code carries out, per `specs/methodology/spec-placement.md § Environments`. Change governed code only as the design says, per `specs/methodology/code.md § Changing Code`; a change the design does not hold goes back to the design, and one no spec states goes back to the specs.

### Check your own work, then verify-spec-implementation's

Before anyone else reads the code, check it against the design, per `specs/AGENTS.md § Design, Refactor, Refine`: every unit written, every annotation naming a heading that exists, sorted and as narrow as the unit, the wiring carrying no spec's rule, and, having run the targeted tests citing the specs it carries out as it worked, every build, lint and test task of the local environment passing, per `specs/methodology/spec-placement.md § Environments`, which says what to present where the specs give none. Record the check in the design's passes. Then `.ai/skills/verify-spec-implementation/` runs as its post-apply audit; settle each finding with the user by `specs/methodology/working-files.md § A Design Document § Changes After Approval`, reverting the code it wrote where a finding exposes a flaw in the design or the user does not approve a tactical fix to that code. Once each is settled, commit the code on the user's go-ahead, one commit for the design, and move its Status to complete.
