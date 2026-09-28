## The Shape of the Specifications

The specifications are layered by what governs what. Each layer is governed by the one above it and describes a different kind of thing.

```
specs/
├── AGENTS.md             the entry point to Spec of Record
├── index.md
├── methodology/          the rules for writing specs
│   ├── index.md
│   └── architecture.md
└── application/          the product being specified
    ├── index.md
    ├── product/
    └── technical/
```

At the top of `specs/` sits `specs/AGENTS.md`, Spec of Record's entry point: where to find each rule, and the rules that reach the method's whole scope, how work is designed and reviewed, how a skill is written, how a list is numbered or counted, and how the method's instructions stay agnostic of which agent reads them. The project's own `AGENTS.md`, at its root, holds what the project is, how its product is positioned, and its conventions, and points to `specs/AGENTS.md`.

`specs/methodology/scope.md § The Shape of the Scope` draws the whole scope, down to each methodology file, and each directory's own `index.md` lists what it holds, so this tree names the layers and the files that fix them.

**`specs/methodology/` —** the rules for writing a specification here: which spec a fact belongs in, which altitude, where a decision the specs rely on but have not made is recorded, how a section is titled and cited, when a structured construct is required instead of prose, when a capability owes acceptance scenarios, what a finished spec reads like, and the working files that writing specs leaves behind.

**`specs/application/` —** the specification of the product itself, split by what a reader can rely on versus how it is made true. `product/` covers what a user or an integrating caller can experience, rely on, or build against, stated as a capability or a guarantee rather than as an implementation choice. `technical/` covers how each of those facts is actually made true: the algorithms, schemas, service boundaries, models, and infrastructure.

## Spec-Driven for Itself

The methodology is held to the rules it states, and a rule reaches a methodology file unless the rule itself scopes it away, as the rules on acceptance scenarios and `technical-specs` frontmatter do (`specs/methodology/scope.md § The Methodology Governs Itself`).

## How the Rules Relate

The detail files that govern what a spec says are not independent. Each answers a question another leaves open, and they apply to different subsets of what is written here. `index.md` lists what each contains; what follows is how they fit together.

**The scope frames all of them —** `scope.md` states which files these rules reach, how the methodology governs itself, and how rules and skills relate, and `skills.md` which skills belong to the method; every rule here applies within that scope.

**Placement comes first and constrains everything after it —** `spec-placement.md` settles which spec a fact belongs in, at which altitude, in which file. Nothing downstream can be decided before that: a citation cannot be written until there is a file to cite, and a capability cannot owe scenarios until it is known to be a product capability.

**Sourcing and citation depends on placement and feeds back into it —** `sourcing-and-citation.md` governs where a fact lives, how everywhere else points at it, and what happens afterward when it changes, and its layering rules are stated in terms of the directories placement defines. The dependency runs both ways in one respect: deciding a fact's one home is a placement decision made under a sourcing rule, which is why the two are the pair most often consulted together.

What happens after a fact changes outlives the writing. A fact stated once is often rendered in more than one place — a companion spec on the other side of the product and technical split, a directory's own `architecture.md`, a diagram wherever it sits — and none of those renderings keeps itself current. Each is a place to revisit when the fact it restates changes, an obligation that outlasts the file being written.

**Modeling constructs cut across both —** whether a passage is prose or a table is independent of which spec it sits in or how it is cited. `modeling-constructs.md` applies wherever a rule, a process, an entity's behavior, or an entry recorded repeatedly is being described, at any altitude, in either half of `specs/application/` and in these files, and a record form reaches the working files too. Its `specs/methodology/modeling-constructs.md § Fields` and `specs/methodology/modeling-constructs.md § Bold Lead-ins` govern every bold phrase opening a line, wherever it sits, its `specs/methodology/modeling-constructs.md § Emphasis` and `specs/methodology/modeling-constructs.md § Literal Text` what italic and backticks mark, and its Record Form gives an open question, placed by `spec-placement.md`, its form. Its diagram rules are the exception to that independence, and are read with `sourcing-and-citation.md`, as a record's citation form is.

**Acceptance scenarios reach the narrowest scope —** `acceptance-scenarios.md` applies only to a product capability's own section, the narrowest reach of the files that govern what a spec says. It scopes itself to product specs in its own text, which is why no technical file owes any.

**Style applies last and to everything —** `spec-style.md` governs what any finished spec reads like, whatever it says and wherever it sits. It is the only detail file with no scope condition at all.

**Working files govern no spec —** `working-files.md` sets the form of the files the work leaves behind, a design entry carrying one change through review and a follow-up holding work not yet done; no spec but `working-files.md` names one (`specs/methodology/sourcing-and-citation.md § Which Citations Are Allowed`).

## How the Rules Are Applied

These files state the rules, and the skills `specs/methodology/skills.md` registers apply them: they sequence the work, record what goes wrong, check the result, and teach the craft a rule assumes. No skill is a rule's home, and where one disagrees with a rule the rule governs (`specs/methodology/scope.md § Rules and Skills`).

**`design-specs` sequences these rules and carries what they cannot —** it names the governing file at each step of a change rather than restating any of it, which is the only way it can stay correct as these rules are amended. What it adds is the part no rule can hold: the failures that recur while applying them, a fact written before checking whether it already had a home, a qualifier lost while compressing one file into another, an edit anchored to text that does not exist. Its script checks that a proposal's quoted text and cited headings exist in the files before the proposal is reviewed. A rule states what correct looks like; that skill records how people miss it.

**`audit-specs` checks whether these rules, and the `specs/AGENTS.md` rules its audits name, actually held —** its audits are performed by reading: whether a directory's summary still describes what it contains, whether a product fact and its technical mechanism still describe one system, whether a capability's scenarios cover what it promises, whether a diagram still agrees with the sources it lists, whether a rule is stated twice or in the wrong file, whether a section cited as a rule's home actually states the rule attributed to it, whether a number or a positional reference restates a list, and whether backticks hold only literal text and italic only real stress. Each names the rule it enforces, so a rule that changes takes its check with it and a finding points at the rule rather than only at a line. Underneath them a script decides what can be decided from the files alone, citation resolution and form, the layering directions, heading hygiene, scenario and diagram shape, a diagram's sources citing it back, frontmatter, index coverage, numbered lead-ins and list items, a working file named in a spec, a field's key and where it sits, an Open Questions section's shape and its records' fields, a record citation, where bold and italic appear, the scope's tree, the skills registry and each registered skill's form, and it runs first so a reading pass is never spent on a broken citation.

What the skill deliberately leaves unaudited, drafting residue or a file's altitude among it, it declines by name rather than by silence.

**`author-mermaid-diagram` serves the diagram rules —** `specs/methodology/modeling-constructs.md § Diagrams` licenses exactly one kind of rendering for a human reader and leaves where it goes to the reader's need, and bounds its form, what it may show, and how it and its sources cite each other; that skill is how one gets authored, rendered, and checked, and that section points at it directly. It differs from `design-specs` and `audit-specs` in its subject, not in how it is governed: drawing a good diagram is craft, so the skill cites these files only where they govern a diagram, while `design-specs` and `audit-specs` exist to serve these rules and cite them throughout.

A skill belongs to the method by being registered in `specs/methodology/skills.md`, which is also the boundary between the method's skills and any other skill under `.ai/skills/`.
