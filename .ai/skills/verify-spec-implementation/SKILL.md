---
name: verify-spec-implementation
description: Check that code truthfully carries out the application specs governing it. Use after implement-specs has written code and checked its own work, as a design changing code's post-apply audit, or whenever the code may have drifted from its specs. Its script first checks every app-spec annotation in the application's code, and lists the spec sections no code cites and the files citing none; then a cold reading judges whether each unit does what it cites and whether unannotated code is wiring. It reports what it finds and changes nothing.
---

# Verifying the code against its specs

This skill is to code what `audit-specs` is to the specs: the independent check that runs once the builder's own check is done, never the builder reading its own work. It reads; it does not run the project's tests, which a project runs as its own pipeline sets.

## Workflow

Each step applying a rule carries its point-of-use citation (`specs/methodology/sourcing-and-citation.md § One Home Per Fact`). The script is `scripts/verify-spec-implementation.py`, the only one this skill runs, from the project root, as `python .ai/skills/verify-spec-implementation/scripts/verify-spec-implementation.py --check-annotations`; `--help` gives its actions.

### Start from the entry point

Read `specs/AGENTS.md` and the glossary before any step, and descend only as far as a step needs, per `specs/methodology/scope.md § Progressive Disclosure`.

### Find the application's code

Read the code roots the technical specs' `stack.md` names, per `specs/methodology/spec-placement.md § The Technical Stack`; the script reads them the same way. A project with no stack file, or none naming a code root, has no code this skill can find: present that to the user as a gap in the specs, and verify nothing.

### Run the script first

`scripts/verify-spec-implementation.py --check-annotations` reports each annotation in the code roots that does not follow `specs/methodology/code.md § Citing the Specs From Code`: a malformed line, a citation naming no section or file that exists, one citing anything but a product or technical spec, and a list out of order; and a code root the stack names that does not exist. `--list-candidates` lists the spec sections no annotation cites and the files in the code roots carrying none, places for the reading to look, deciding nothing.

### Stop at annotations out of step

Where the script's findings show existing annotations out of step with the specs, read them against `specs/methodology/code.md § Changing Code`, which says when they stop the work and how it resumes. Here the stop comes before any reading: present the findings to the user for triage, and verify nothing further until the user's fix is applied, then run the script again. Run as a design changing code's post-apply audit, the annotations that design wrote are its work under audit, never existing ones: their findings are this audit's, settled as `§ Workflow § Report, and settle as an audit` says.

### Read the code against its specs

For each annotated unit, read the sections it cites, and judge whether the unit carries them out, or checks them as a test does, no more and no less, per `specs/methodology/code.md § Governed Code and Wiring Code` and `specs/methodology/code.md § Tests`, and whether its annotations sit where `specs/methodology/code.md § Citing the Specs From Code` sets, as narrow as the unit and never in a documentation comment, which the script cannot judge. For each file the script lists as citing no spec, judge whether it is wiring or governed code missing its annotations; a file in a format with no comments is never governed code, and is judged as `specs/methodology/code.md § Governed Code and Wiring Code` sets. For each section it lists as cited by no code, judge whether it states something code must carry out, and so is not yet implemented, or something no code carries out, as an overview does.

### Report, and settle as an audit

Write the report to `.ai/tmp/verify-spec-implementation/`, one file per run, clearing an earlier report of the same scope, per `specs/methodology/working-files.md § The Working Files`. Name each finding with its file, its line, what it fails and the rule or spec it fails. Run as a design changing code's post-apply audit, its findings are settled with the user as `specs/methodology/working-files.md § A Design Document` has changes after approval.

## The checks

Each check names the rule it enforces (`specs/methodology/scope.md § Rules and Skills`).

| Check | How | Enforces |
|---|---|---|
| Annotations | `--check-annotations`, then reading | `specs/methodology/code.md § Citing the Specs From Code` |
| Governed code and wiring | reading, from `--list-candidates` | `specs/methodology/code.md § Governed Code and Wiring Code` |
| Tests | reading | `specs/methodology/code.md § Tests` |
