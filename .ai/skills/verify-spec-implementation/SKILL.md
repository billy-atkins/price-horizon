---
name: verify-spec-implementation
description: Check that code truthfully carries out the application specs governing it. Use after implement-specs has written code and made its self-review, as the audit in a design changing code's apply, or whenever the code may have drifted from its specs. Its script first checks every app-spec annotation in the application's code, and lists the spec sections no code cites and the files citing none; then a cold reading judges whether each unit does what it cites and whether unannotated code is wiring, and reads the technical overview's account of the code against the code. It reports what it finds and changes nothing.
---

# Verifying the code against its specs

This skill is to code what `audit-specs` is to the specs. It is the independent check that runs once the builder's self-review is done, never the builder reading its own work. This skill reads. It does not run the project's tests, which a project runs as its own pipeline sets. A run is the skill's full run over every code root, the same whether or not a design came before it, and it names no design, as `specs/AGENTS.md § Design, Refactor, Refine § An Audit` has an audit.

## Workflow

Each step applying a rule carries its point-of-use citation (`specs/methodology/sourcing-and-citation.md § One Home Per Fact`). The script is `scripts/verify-spec-implementation.py`, the only one this skill runs. Run it from the project root, as `python .ai/skills/verify-spec-implementation/scripts/verify-spec-implementation.py --check-annotations`. Its `--help` gives its actions.

### Start from the entry point

Read `specs/AGENTS.md` and the glossary before any step. Descend only as far as a step needs, per `specs/methodology/scope.md § Progressive Disclosure`.

### Find the application's code

Read the code roots the technical specs' `stack.md` names, per `specs/methodology/spec-placement.md § The Technical Stack`. The script reads them the same way. A project with no stack file, or with none naming a code root, has no code this skill can find. Present that to the user as a gap in the specs, and verify nothing.

### Run the script first

`scripts/verify-spec-implementation.py --check-annotations` reports each annotation in the code roots that does not follow `specs/methodology/code.md § Citing the Specs From Code`, or the form `specs/methodology/sourcing-and-citation.md § Writing a Citation § Citing From Code` gives it:
- a malformed line;
- a citation naming no section or file that exists;
- a citation of anything but a product or technical spec;
- a list out of order.

It also reports a code root the stack names that does not exist. `--list-candidates` lists the spec sections no annotation cites and the files in the code roots carrying none. These are places for the reading to look, and the list decides nothing.

### Stop at annotations out of sync

Where the script's findings show existing annotations out of sync with the specs, read them against `specs/methodology/code.md § Changing Code`. That section says when they stop the work and how the work resumes. Here the stop comes before any reading. Present the findings to the user for triage, and verify nothing further until the user's fix is applied. Then run the script again. A run reads every annotation alike. Where it runs in a design changing code's apply, the builder, reading the report against the design's changes, tells the annotations that design wrote from existing ones, and settles their findings as `§ Workflow § Report, and settle as an audit` says.

### Read the code against its specs

For each annotated unit, read the sections it cites. Judge whether the unit carries them out, or checks them as a test does, no more and no less, per `specs/methodology/code.md § Governed Code and Wiring Code` and `specs/methodology/code.md § Tests`. Judge too whether the unit's annotations sit where `specs/methodology/code.md § Citing the Specs From Code` sets: as narrow as the unit, and never in a documentation comment, as `specs/methodology/sourcing-and-citation.md § Writing a Citation § Citing From Code` has it. The script cannot judge where they sit.

For each file the script lists as citing no spec, judge whether it is wiring or governed code missing its annotations. A file in a format with no comments is never governed code, and is judged as `specs/methodology/code.md § Governed Code and Wiring Code` sets. For each section the script lists as cited by no code, judge whether it states something code must carry out, and so is not yet implemented, or something no code carries out, as an overview does. Read the code for American English, per `specs/methodology/code.md § Changing Code`, and report each breach you find, as `specs/AGENTS.md § Design, Refactor, Refine § An Audit` has an audit report a rule reaching only what a change writes.

### Read the technical overview against the code

The technical specs' `architecture.md` describes the code carrying out the application specs, per `specs/methodology/spec-placement.md § What an Overview Describes`. Read the overview's account of the code against the code. Report what it says that the code does not bear out, per `specs/methodology/sourcing-and-citation.md § Keeping Specs in Sync § Materialized Views`.

### Report, and settle as an audit

Write the report to `.ai/tmp/verify-spec-implementation/`, one file per run, clearing an earlier report of the same scope, per `specs/methodology/working-files.md § The Working Files`. Name each finding with its file, its line, what it fails, and the rule or spec it fails. Report what you noticed beyond the checks you ran as review observations (`specs/methodology/glossary.md`), apart from the findings and uncounted. A run in a design changing code's apply reports its findings as any run does. Its report is the builder's, who triages each finding against the design's changes, as `specs/AGENTS.md § Design, Refactor, Refine § An Audit` has an audit read, and settles it with the user by `specs/methodology/working-files.md § A Design Document § Changes After Approval`, applying `specs/AGENTS.md § Design, Refactor, Refine § Settling a Round § The Test` where that section applies it. A finding the design did not cause goes to the user by that section's first row, the test dropping none. The builder brings each review observation with its triage.

## The checks

Each check names the section it enforces (`specs/methodology/scope.md § Rules and Skills`).

**Reference Key:** Check \
**Required:** How, Enforces

| Check | How | Enforces |
|---|---|---|
| Annotations | `--check-annotations`, then reading | `specs/methodology/code.md § Citing the Specs From Code` |
| Governed code and wiring | reading, from `--list-candidates` | `specs/methodology/code.md § Governed Code and Wiring Code` |
| Tests | reading | `specs/methodology/code.md § Tests` |
| American English in code | reading the code in every code root | `specs/methodology/code.md § Changing Code` |
| The technical overview's account of the code | reading | `specs/methodology/sourcing-and-citation.md § Keeping Specs in Sync § Materialized Views` |
