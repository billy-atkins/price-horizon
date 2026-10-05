## What Spec of Record Governs

Spec of Record governs files by kind, each kind with what it holds and what names its files:

| Kind | Holds | Named by |
|---|---|---|
| Agent instructions | the method's entry point, and a project's own instructions to an agent, each an AGENTS.md file (`specs/methodology/external-references.md § External References [Name: AGENTS.md]`) | `specs/AGENTS.md`, and `AGENTS.md` at the project's root |
| Specs | the specifications, the methodology among them | their place under `specs/`, `specs/AGENTS.md` aside |
| Skills | the procedures that apply the method's rules, and the code their scripts share | `specs/methodology/skills.md` |
| Working files | the working files | `specs/methodology/working-files.md § The Working Files` |
| Code | the application's code, governed code and the wiring connecting it | the code roots the technical specs' stack names (`specs/methodology/spec-placement.md § The Technical Stack`) |

Whatever is not named so is outside the scope, and the method's rules do not reach it. The method's rules, the methodology's and `specs/AGENTS.md`'s, reach every file in scope but code. A rule reaches less only where it scopes itself, in its own text, to something a file is not; no exemption granted elsewhere narrows it. Code is reached by the rules in `specs/methodology/code.md`, and by the rules it cites for code, and by no other. A project's own root `AGENTS.md` holds that project's instructions, and the project sets what those instructions reach.

## The Shape of the Scope

```
AGENTS.md                      the project's own instructions, pointing to specs/AGENTS.md
specs/
├── AGENTS.md                  the entry point to Spec of Record
├── index.md                   in every directory under specs/: what it holds
├── methodology/               the rules for writing specs, and for the code the specs govern
│   ├── index.md
│   ├── architecture.md
│   ├── acceptance-scenarios.md
│   ├── code.md
│   ├── external-references.md
│   ├── glossary.md
│   ├── modeling-constructs.md
│   ├── scope.md
│   ├── skills.md
│   ├── sourcing-and-citation.md
│   ├── spec-placement.md
│   ├── spec-style.md
│   └── working-files.md
└── application/               the product being specified
    ├── index.md
    ├── product/               what a user can rely on
    └── technical/             how it is made true
.ai/
└── skills/
    ├── <skill-name>/          a registered skill: SKILL.md, its entry point, references/ and scripts/
    └── lib/                   the code the registered skills' scripts share
```

The tree:

- names the methodology's files, since they are the rules every task depends on, and describes none of them;
- stops at `product/` and `technical/`, whose files grow with the product;
- leaves the working files to `specs/methodology/working-files.md § The Working Files`, which names them;
- does not draw code, which sits wherever a project keeps it.

A directory's `index.md` says what each of its files covers (`specs/methodology/spec-placement.md § Where a File Goes`), so before working in a directory an agent reads its `index.md`.

## Progressive Disclosure

An agent loads what its current step needs, when the step needs it, descending only as far as the step requires:

- from `specs/AGENTS.md`, which sends a change to the procedure that governs it,
- to that procedure's step and the reference it forks to,
- to a directory's `index.md`,
- to a file,
- and to the section a citation names.

What is loaded long before it is needed sits behind everything loaded since and competes with all of it; what is loaded at the step that needs it is at the front of the agent's attention and carries its full weight.

The glossary is the one methodology file loaded ahead of need, read with `specs/AGENTS.md` before any step, since an agent cannot know a word is one of its terms without having read it.

An agent reads what it loads from a directory in the order the directory's `index.md` lists, a parent directory before the directories under it: the order its authors set (`specs/methodology/spec-placement.md § Where a File Goes`). Progressive disclosure governs when to read, not how much. Whatever is loaded is read in full, never skimmed, and read fresh rather than recalled (`specs/AGENTS.md § Design, Refactor, Refine`). A task whose unit is a whole directory, an audit among them, loads the whole directory.

## The Methodology Governs Itself

The methodology is held to the rules it states:

- it has an `index.md`, and an `architecture.md` summarizing it;
- a rule that is a lookup is authored as a Decision Table (`specs/methodology/modeling-constructs.md § Constructs § Decision Table`);
- its files meet the style rules they set.

The rules on acceptance scenarios and on `technical-specs` frontmatter scope themselves to product specs, and so do not reach it: a methodology file has no product capability to prove and no technical counterpart to name. The rules in `specs/methodology/code.md` reach only code, and so do not reach it either.

## Agent Agnostic

The instructions in Spec of Record's scope, both `AGENTS.md` files and each registered skill, stay agnostic of which agent reads them: no vendor-specific instruction filename, no tool-specific directory, no assumption about which model, CLI, or editor is running.

**The test —** would anything new still make sense to an agent from a different vendor, or to a person reading it directly?

**The one exception —** anything written for one tool, and only because it carries no content:

- an opt-in helper outside the method's scope, named for the tool it serves, may wire that tool up to the agnostic content;
- an agent setting itself up may write what it needs to carry out a choice the method leaves to it (`specs/methodology/skills.md § Setting Up an Agent`).

Whatever either writes is kept out of version control and outside the scope, and nothing depends on its having been written: a skill stays readable directly, and what was written only saves a step, or applies a choice, for someone using that tool.

## Rules and Skills

The methodology's files state rules. They do not sequence the work, record what goes wrong while following it, check whether a result conforms, or teach the craft a rule assumes; the skills `specs/methodology/skills.md` registers do, and a cold agent needs them to follow the method in practice. `specs/AGENTS.md` states rules too, and sequences the work through Design, Refactor, Refine. No skill is a rule's home: where a skill and a rule disagree, the rule governs and the skill is what needs correcting.

A rule without a check is a suggestion, so every rule of Spec of Record is enforced, and a rule added or changed takes its check with it, in the same change.

**A specification rule —** is checked against the files it governs by one of the audit skill's reading audits, or, for a rule of `specs/methodology/code.md`, by a check of `.ai/skills/verify-spec-implementation/` reading the code. Either skill's script first decides whatever the files alone settle, and never a judgment, since a check that cannot decide gives a confident false clear. A script listing places for a reading audit to look decides nothing.

**An operating rule —** is checked where it leaves a trace in the files the audits read: the scope's tree, the skills registry, a skill's form, a follow-up. A plan's form leaves its trace outside them, and is checked by the skill writing the plan, through its script and its steps. Where a rule leaves no trace, as reading fresh leaves none, it is carried out as a named step of `specs/AGENTS.md` or of a registered skill, and a skipped step is found by what it leaves wrong in the files.

**Which check enforces each section —** for every section of `specs/AGENTS.md` and of the methodology's files but its `architecture.md` and `index.md`, which hold no rule of their own, `.ai/skills/audit-specs/` names the reading audit enforcing it, or names it an operating rule, whose check is a step under a registered skill's `## Workflow` that applies it and gives it a point-of-use citation. For a section of `specs/methodology/code.md`, `.ai/skills/verify-spec-implementation/` names the check enforcing it instead, or `.ai/skills/audit-specs/` names it an operating rule.

**A section read in parts —** an audit reading only part of a section it names says which part, and the audits naming one section read all of it between them, each part once. Where a step names a section too, the step carries what leaves no trace in the files, and the audits read the rest.
