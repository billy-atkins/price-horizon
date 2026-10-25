## Governed Code and Wiring Code

Governed code does what a product or technical spec states, or, as a test, checks that it is done ([`§ Tests`](#tests)). It names that spec with app-spec annotations ([`§ Citing the Specs From Code`](#citing-the-specs-from-code)). Wiring code is the routing, configuration, dependency registration and glue that no spec states. It carries no annotation.

A file in a format with no comments is never governed code:
- a contract a spec states, such as an API contract designed first, is itself a spec and lives with the technical specs;
- a file a tool generates is among the paths the stack excludes, and the stack names its tool ([`specs/methodology/spec-placement.md § The Technical Stack`](/specs/methodology/spec-placement.md#the-technical-stack));
- any other is wiring.

Wiring exists because the specs stop where more detail would no longer improve the code. The agent writing the code writes the wiring the specs leave to it, so that the whole delivers what the specs state.

## Citing the Specs From Code

Governed code names each spec it carries out or checks with app-spec annotations. Each is a spec annotation holding the tag `@app-spec`, in the form [`specs/methodology/sourcing-and-citation.md § Writing a Citation § Citing From Code`](/specs/methodology/sourcing-and-citation.md#citing-from-code) gives:

```
// @app-spec specs/application/product/example-domain/example.md § Example Capability
// @app-spec specs/application/technical/example-data-model.md
// @app-spec specs/application/technical/example-service/example.md § Parent § Child
```

**What it cites.** A product spec or a technical spec, or a section of one, as [`specs/methodology/sourcing-and-citation.md § Which Citations Are Allowed`](/specs/methodology/sourcing-and-citation.md#which-citations-are-allowed) permits code.

**Cited no higher than needed.** The annotations are the narrowest citations that together state all of what the unit carries out or checks. For each part, that is the deepest section holding it. Where the unit carries out a whole file, it is the whole file, as a data repository class carrying out every entity of a data model file cites that file. A citation above what is needed claims the unit carries out more than it does. One below it leaves part of what governs the unit uncited.

**Where it sits.** The annotations sit above everything belonging to the smallest unit whose behavior carries out or checks the cited spec, or its part of it. That includes the unit's documentation comment, decorators, attributes and annotations. The unit is a function, a method, a class, or a module. A module's annotations open its file, after whatever the language or its tools require first, such as a shebang, a license header or a package clause. Where a language reads the comment directly above a unit as its documentation, as Go does, a blank line separates the annotations from the unit's own comment.

## Changing Code

What governed code does changes only as its specs change, so the specs stay the record of what the code does. Apart from its annotation lines alone, governed code is never edited outside a design changing code, which the user approves ([`specs/methodology/working-files.md § A Design Document § A Design Changing Code`](/specs/methodology/working-files.md#a-design-changing-code)). Each of these reaches the code through such a design:
- a change to what the code must do that no spec yet states, which starts in the specs as a design document the user approves ([`specs/methodology/working-files.md § A Design Document`](/specs/methodology/working-files.md#a-design-document));
- carrying applied specs into code for the first time;
- fixing code that does not do what its specs state;
- restructuring governed code.

Making cloud infrastructure changes in the console guarantees drift. That is why every change goes through Terraform's natural process of write, plan and apply, which keeps the Terraform configuration and the infrastructure in sync.

**Annotation lines alone.** An edit to annotation lines alone changes nothing the code does. A retitled heading asks such an edit of every annotation naming it ([`specs/methodology/sourcing-and-citation.md § Writing a Citation § Citing From Code`](/specs/methodology/sourcing-and-citation.md#citing-from-code)). The edit rides with the design that retitles the heading, whose Target names the files the edit touches. A change to the annotation's form is rolled out by a design changing code of its own, as a design leaving code out of sync hands that work on ([`specs/methodology/working-files.md § A Design Document`](/specs/methodology/working-files.md#a-design-document)).

**Wiring code.** Wiring code changes as any other file does: as a direct edit when the change is a small tactical fix ([`specs/methodology/glossary.md`](/specs/methodology/glossary.md)) the user approves ([`specs/AGENTS.md § Design, Refactor, Refine § Direct Edits`](/specs/AGENTS.md#direct-edits)), or within a design changing code.

**American English in code.** What a change writes in code is in American English, as [`specs/methodology/spec-style.md § Clear Prose`](/specs/methodology/spec-style.md#clear-prose) has it. That covers its comments, a name it gives, and a message it writes for a developer or an operator, such as a log line or an error. A message a user of the product reads is in American English too, unless the product specs set another language for it. Text the change does not write stays as it stands, so code brought under the specs keeps its spelling until a change writes it. A name the code already holds keeps its spelling even where a change touches it, as Clear Prose keeps a name from outside the specs. A name a change adds beside a family of names spelled one way follows the family, as `colour_secondary` does beside `colour_primary`. Spelling alone is never a reason to change governed code or wiring unless the user requests or approves it, as Clear Prose has a name respelled.

**Annotations out of sync stop the work.** Existing annotations that do not follow [`§ Citing the Specs From Code`](#citing-the-specs-from-code), or that cite what the specs no longer hold, stop any work on code that meets them. Schema on read stops the same way at an entity that no longer fits. The work stops for triage, and the user decides which side is wrong:
- the code, whose annotations are then brought into sync by a design changing code of its own;
- or the specs, where a heading was retitled in error or a change was lost, as in a merge conflict, and a design changing the specs puts that right.

The work resumes once that design is applied and finished.

## Tests

A test checks a spec rather than carrying it out. It is governed code all the same. It cites what it checks, as [`§ Citing the Specs From Code`](#citing-the-specs-from-code) gives:
- a test generated from a capability's acceptance scenarios cites that capability's `Test Scenarios` section ([`specs/methodology/acceptance-scenarios.md § Acceptance Scenarios`](/specs/methodology/acceptance-scenarios.md#acceptance-scenarios));
- a test checking a mechanism cites the technical section stating it.

A test's fixtures and the setup that runs it check nothing a spec states, so they are wiring.
