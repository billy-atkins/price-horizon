## The Shape of the Specifications

The specifications are layered by what governs what, each layer describing a different kind of thing.

```
specs/
├── AGENTS.md             the entry point to Spec of Record
├── index.md
├── methodology/          the rules for writing specs, and for the code the specs govern
│   ├── index.md
│   └── architecture.md
└── application/          the product being specified
    ├── index.md
    ├── product/
    └── technical/
```

At the top of `specs/` sits `specs/AGENTS.md`, Spec of Record's entry point. It holds:

- the kinds a change can be, and the skills every change and every check is sent to, each forking on whether the canon or the application specs are touched, and the skills designing, writing and checking code;
- where to find a rule mid-step;
- the rules reaching every author: how work is designed, reviewed and approved.

The project's own `AGENTS.md`, at its root, holds that project's own instructions to an agent, and points to `specs/AGENTS.md`.

`specs/methodology/scope.md § The Shape of the Scope` draws the whole scope, down to each methodology file, and each directory's own `index.md` lists what it holds, so this tree names only the layers and the files that establish them.

**`specs/methodology/` —** the rules for writing a specification here, and for the code the specs govern:

- what the method governs, how an agent reads it, how the methodology governs itself, how each rule is enforced, how its instructions stay agnostic of the agent reading them, and the terms it gives meanings of its own;
- which skills belong to the method, how a skill is authored, and how the agent in use is set up;
- which spec a fact belongs in, at which altitude and in which file, and the persona each spec, and the code they govern, is written as;
- how a capability domain is named, how a product file names the technical files behind it, what a product module is and what a change to its code reads, and where an open question is recorded;
- what the technical stack and the environments hold;
- where a fact has its one home, which citations are allowed, how a section is titled and cited, and which renderings of a fact are kept in step;
- when a structured construct is required instead of prose, how markup is written, and how a diagram is drawn and sourced;
- when a capability owes acceptance scenarios;
- what a finished spec reads like and the trade-off that belongs in one, the clear prose it is written in, where an example is drawn from and how a number is used;
- the working files, and the kinds of file a design is bounded to;
- the rules that reach the code the application specs govern.

**`specs/application/` —** the specification of the product itself, split by what a reader can rely on versus how it is made true. `product/` covers what a user or an integrating caller can experience, rely on, or build against, stated as a capability or a guarantee rather than as an implementation choice. `technical/` covers how each of those facts is actually made true: the algorithms, schemas, service boundaries, models, and infrastructure.

## The Methodology Governs Itself

The methodology is held to the rules it states, and a rule reaches a methodology file unless the rule itself scopes it away, as the rules on acceptance scenarios and `technical-specs` frontmatter do, and `code.md`'s, which reach only code (`specs/methodology/scope.md § The Methodology Governs Itself`).

## How the Rules Relate

The detail files that govern what a spec says, and the one governing code, are not independent. Each answers a question another leaves open, and they apply to different subsets of what is written here. `specs/methodology/index.md` lists what each contains; this section says how they fit together.

**The scope frames all of them —** every rule here applies within it:

- `scope.md` states which files these rules reach and the shape of that scope, and how an agent loads what a step needs. It also states how the methodology governs itself, how rules and skills relate, how every rule is enforced, and how the method's instructions stay agnostic of the agent reading them.
- `skills.md` states which skills belong to the method, how a skill is authored, and how the agent in use is set up to carry out what the method leaves to it.
- `glossary.md` states the terms the method gives meanings of its own, how an entry is written, and where an abbreviation may be used.

**Placement comes first and constrains everything after it —** `spec-placement.md` settles which spec a fact belongs in, at which altitude, in which file. Nothing downstream can be decided before that: a citation cannot be written until there is a file to cite, and a capability cannot owe scenarios until it is known to be a product capability. `spec-placement.md` also sets how a capability domain is named, how a product file names the technical files that build it, what a change to a product module's code reads, and what the technical stack and the environments hold.

**A persona for the methodology, the application specs and their code —** `spec-placement.md` also gives the persona the methodology, the product specs, the technical specs and the code they govern are each written as, and the adversarial review of a design changing them framed as.

**Sourcing and citation depends on placement and feeds back into it —** `sourcing-and-citation.md` governs where a fact lives, how everywhere else points at it, by a citation to a stable heading and never by direction, and what happens afterward when the fact changes. Its layering rules are stated in terms of the directories placement defines. The dependency runs both ways in one respect: deciding a fact's one home is a placement decision made under a sourcing rule, which is why the two are the pair most often consulted together.

A fact stated once is often rendered in more than one place: a counterpart spec on the other side of the product and technical split, a directory's own `architecture.md`, a diagram wherever it sits. None of those renderings keeps itself current, so each is a place to revisit when the fact it restates changes, an obligation that outlasts the writing of the file.

**Modeling constructs cut across both —** whether a passage is prose or a table is independent of which spec it sits in or how it is cited. `modeling-constructs.md` applies wherever a rule, a process, an entity's behavior, or an entry recorded repeatedly is being described, at any altitude, in either half of `specs/application/` and in these files; its Record Form reaches the working files too. It also sets the form of markup, wherever it is written: `specs/methodology/modeling-constructs.md § Fields` and `specs/methodology/modeling-constructs.md § Bold Lead-ins` govern every bold phrase opening a line, and `specs/methodology/modeling-constructs.md § Emphasis` and `specs/methodology/modeling-constructs.md § Literal Text` what italic and backticks mark. Its Record Form gives an open question, placed by `spec-placement.md`, its form, and a design document's steering decisions theirs. Its diagram rules are the exception to that independence, and are read with `sourcing-and-citation.md`, as a record's citation form is.

**Acceptance scenarios reach the narrowest scope —** `acceptance-scenarios.md` applies only to a product capability's own section, the narrowest reach of the files that govern what a spec says. It scopes itself to product specs in its own text, which is why no technical file owes any.

**Code is reached by one file —** `code.md` holds the rules that reach the code the application specs govern: which code is governed and which is wiring, how governed code names the specs it carries out or checks, how it changes, and what a test is. Its annotation is a citation written as `sourcing-and-citation.md` gives, without the backticks. No other file's rules reach code, but those it cites (`specs/methodology/scope.md § What Spec of Record Governs`).

**Style applies last, and to every spec —** `spec-style.md` governs what any finished spec reads like, whatever it says and wherever it sits, and its clear prose and its rule on numbers reach the agent instructions and the skills too, each file written for its primary reader.

**Working files govern no spec —** `working-files.md` sets the form of the working files: a design document carrying one change through review, with the steers that settled it and the designs it waits on, and how a design changing code differs; a stamp recording when a check passed; and a follow-up holding work not yet done. No spec but `working-files.md` names one (`specs/methodology/sourcing-and-citation.md § Which Citations Are Allowed`).

## How the Rules Are Applied

These files state the rules, and the skills registered in `specs/methodology/skills.md` apply them: they sequence the work, record what goes wrong, check the result, and teach the craft a rule assumes. Registration is also the boundary between the method's skills and any other skill under `.ai/skills/`. No skill is a rule's home, and where one disagrees with a rule the rule governs (`specs/methodology/scope.md § Rules and Skills`).

**`design-specs` sequences these rules and carries what they cannot —** it gives each rule a change applies a point-of-use citation rather than restating it, the only way it can stay correct as these rules are amended, and forks on the kind of specification a change touches. What it adds is what no rule can hold: the failures that recur while applying them, such as a fact written before checking whether it already had a home. A rule states what correct looks like; that skill records how people miss it.

**`audit-specs` checks whether these rules, and `specs/AGENTS.md`'s, actually held —** a script first decides what the files alone can, and reading audits, one per family of rules, judge the rest. For every rule section it names the reading audit enforcing it, or names it an operating rule checked by the skill steps that apply and cite it; for a section of `code.md`, `verify-spec-implementation` names the check enforcing it instead, unless `audit-specs` names it an operating rule (`specs/methodology/scope.md § Rules and Skills`). So a rule that changes takes its check with it, and a finding points at the rule rather than only at a line.

What it deliberately leaves unaudited it declines by name rather than by silence.

**`author-mermaid-diagram` serves the diagram rules —** `specs/methodology/modeling-constructs.md § Diagrams` licenses exactly one kind of rendering for a human reader. It leaves where a diagram goes to the reader's need, and bounds its form, what it may show, and how it and its sources cite each other. That skill is how a diagram gets authored, rendered and checked, and that section points at it directly. It differs from `design-specs` and `audit-specs` in its subject, not in how it is governed: drawing a good diagram is craft, so the skill cites these files only where they govern a diagram, while `design-specs` and `audit-specs` exist to serve these rules and cite them throughout.

**`configure-spec-of-record` sets up the agent in use —** the method's instructions name no agent, so the agent in use sets itself up, through that skill, for what only it can carry out, applying a review's reasoning effort among it (`specs/methodology/skills.md § Setting Up an Agent`). It writes only what it needs, outside the scope.

**`implement-specs` carries the specs into code —** it applies `code.md`'s rules: how governed code names what it carries out or checks, how it changes, and what a test is. It designs the code and its tests from one product module's specs as a design document, written as the chief architect would, and takes it through the same reviews as a design changing the specs; the user approves it before any code is written. It then writes the code, runs the local environment's tasks, and checks its own work before `verify-spec-implementation` checks it.

**`verify-spec-implementation` checks the code against its specs —** it is to code what `audit-specs` is to the specs: a script checks the app-spec annotations and lists the spec sections no code cites, and a cold reading judges whether each unit carries out what it cites and whether code with no annotation is wiring. It only reads: the project's tests run where the project's own pipeline runs them.
