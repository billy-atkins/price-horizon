## Governed Code and Wiring Code

Governed code does what a product or technical spec states, or, as a test, checks that it is done (`§ Tests`), and names that spec with app-spec annotations (`§ Citing the Specs From Code`). Wiring code, the routing, configuration, dependency registration and glue that no spec states, carries no annotation.

A file in a format with no comments is never governed code:

- a contract a spec states, an API contract designed first, say, is itself a spec, and lives with the technical specs;
- one a tool generates is among the paths the stack excludes, its tool named in the stack (`specs/methodology/spec-placement.md § The Technical Stack`);
- any other is wiring.

Wiring exists because the specs stop where more detail would no longer improve the code: the agent writing the code writes the wiring they leave to it, so that the whole delivers what they state.

## Citing the Specs From Code

Governed code names each spec it carries out or checks with app-spec annotations, each a spec annotation holding the tag `@app-spec`, in the form `specs/methodology/sourcing-and-citation.md § Writing a Citation § Citing From Code` gives:

```
// @app-spec specs/application/product/example-domain/example.md § Example Capability
// @app-spec specs/application/technical/example-data-model.md
// @app-spec specs/application/technical/example-service/example.md § Parent § Child
```

**What it cites —** a product spec or a technical spec, or a section of one, as `specs/methodology/sourcing-and-citation.md § Which Citations Are Allowed` permits code.

**Cited no higher than needed —** the annotations are the narrowest citations that together state all of what the unit carries out or checks: for each part, the deepest section holding it, or a whole file where the unit carries out the whole file, as a data repository class carrying out every entity of a data model file cites that file. A citation above what is needed claims the unit carries out more than it does; one below it leaves part of what governs the unit uncited.

**Where it sits —** above everything belonging to the smallest unit whose behavior carries out or checks the cited spec, or its part of it, the unit's documentation comment, decorators, attributes and annotations included. That unit is a function, a method, a class, or a module. A module's annotations open its file, after whatever the language or its tools require first, a shebang, a license header or a package clause among them. Where a language reads the comment directly above a unit as its documentation, as Go does, a blank line separates the annotations from the unit's own comment.

## Changing Code

What governed code does changes only as its specs do, so the specs stay the record of what it does. Governed code, its annotation lines alone aside, is never edited outside a design changing code, which the user approves (`specs/methodology/working-files.md § A Design Document § A Design Changing Code`). Each of these reaches the code through such a design:

- a change to what the code must do that no spec yet states, which starts in the specs, as a design document the user approves (`specs/methodology/working-files.md § A Design Document`);
- carrying applied specs into code for the first time;
- fixing code that does not do what its specs state;
- restructuring governed code.

**Annotation lines alone —** an edit to them, as a retitled heading asks of every annotation naming it (`specs/methodology/sourcing-and-citation.md § Writing a Citation § Citing From Code`), changes nothing the code does, and rides with the design that retitles the heading, its Target naming the files it touches. A change to the annotation's form is rolled out by a design changing code of its own, as a design leaving code out of step hands it on (`specs/methodology/working-files.md § A Design Document`).

**Wiring code —** changes as any other file does: as a direct edit when the change is small and the user approves it (`specs/AGENTS.md § Design, Refactor, Refine`), or within a design changing code.

**Annotations out of step stop the work —** existing annotations that do not follow `§ Citing the Specs From Code`, or that cite what the specs no longer hold, stop any work on code that meets them, as schema on read stops at an entity that no longer fits. The work stops for triage, and the user decides which side is wrong:

- the code, whose annotations are then brought in step by a design changing code of its own;
- or the specs, where a heading was retitled in error or a change was lost, as in a merge conflict, which a design changing the specs puts right.

The work resumes once that design is applied and finished.

## Tests

A test checks a spec rather than carrying it out, and is governed code all the same. It cites what it checks, as `§ Citing the Specs From Code` gives:

- a test generated from a capability's acceptance scenarios cites that capability's `Test Scenarios` section (`specs/methodology/acceptance-scenarios.md § Acceptance Scenarios`);
- a test checking a mechanism cites the technical section stating it.

A test's fixtures and the set-up that runs it, which check nothing a spec states, are wiring.
