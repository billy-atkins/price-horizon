## What Spec of Record Governs

Spec of Record governs files by kind, each kind with what it holds and how its files are named:

| Kind | Holds | Named by |
|---|---|---|
| Agent instructions | the method's entry point, and a project's own instructions to an agent | `specs/AGENTS.md`, and `AGENTS.md` at the project's root |
| Specs | the specifications, the methodology among them | their place under `specs/`, `specs/AGENTS.md` aside |
| Skills | the procedures that apply the method's rules | `specs/methodology/skills.md` |
| Working files | the working files | `specs/methodology/working-files.md § The Working Files` |

Whatever is not named so is outside the scope, and the method's rules do not reach it. The method's rules, the methodology's and `specs/AGENTS.md`'s, reach every file in scope, except where a rule scopes itself, in its own text rather than through an exemption granted elsewhere, to something a file is not. A project's own root `AGENTS.md` holds that project's instructions, whose reach is the project's to set.

## The Shape of the Scope

```
AGENTS.md                      the project's own instructions, pointing to specs/AGENTS.md
specs/
├── AGENTS.md                  the entry point to Spec of Record
├── index.md                   in every directory under specs/: what it holds
├── methodology/               the rules for writing specs
│   ├── index.md
│   ├── architecture.md
│   ├── acceptance-scenarios.md
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
└── skills/<skill-name>/       a registered skill: SKILL.md, its entry point, references/ and scripts/
```

The tree names the methodology's files, since they are the rules every task depends on, and describes none of them; it stops at `product/` and `technical/`, whose files grow with the product; and it leaves the working files to `specs/methodology/working-files.md § The Working Files`, which names them. What a file covers is its directory's `index.md` (`specs/methodology/spec-placement.md § Where a File Goes`), so before working in a directory an agent reads its `index.md`.

## Progressive Disclosure

An agent loads what its current step needs, when the step needs it, descending only as far as the step requires: from `specs/AGENTS.md`'s playbook, which sends a change to the procedure that governs it, to that procedure's step and the reference it forks to, to a directory's `index.md`, to a file, and to the section a citation names. What is loaded long before it is needed sits behind everything loaded since and competes with all of it; what is loaded at the step that needs it is at the front of the agent's attention and carries its full weight.

The glossary is the one methodology file loaded ahead of need, read with `specs/AGENTS.md` before any step, since an agent cannot know a word is one of its terms without having read it.

Progressive disclosure governs when to read, not how much. Whatever is loaded is read in full and never skimmed, and read fresh rather than recalled (`specs/AGENTS.md § Design, Refactor, Refine (DRR)`), and a task whose unit is a whole directory, an audit among them, loads the whole directory.

## The Methodology Governs Itself

The methodology is held to the rules it states: it has an `index.md`, and an `architecture.md` summarizing it, a rule that is a lookup is authored as a table, and its files meet the style rules they set. The rules on acceptance scenarios and on `technical-specs` frontmatter scope themselves to product specs, and so do not reach it: a methodology file has no product capability to prove and no technical counterpart to name.

## Agent Agnostic

The instructions in Spec of Record's scope, both `AGENTS.md` files and each registered skill, stay agnostic of which agent reads them: no vendor-specific instruction filename, no tool-specific directory, no assumption about which model, CLI, or editor is running. The test for anything new: would it still make sense to an agent from a different vendor, or a person reading it directly. Anything written for one tool is the one exception, and only because it carries no content: an opt-in helper outside the method's scope, named for the tool it serves, may wire that tool up to the agnostic content, and an agent setting itself up may write what it needs to carry out a choice the method leaves to it (`specs/methodology/skills.md § Setting Up an Agent`). Whatever either writes is kept out of version control and outside the scope, and nothing depends on its having been written: a skill stays readable directly, and what was written only saves a step, or applies a choice, for someone using that tool.

## Rules and Skills

The methodology's files state rules. They do not sequence the work, record what goes wrong while following it, check whether a result conforms, or teach the craft a rule assumes; the skills `specs/methodology/skills.md` registers do, and a cold agent needs them to follow the method in practice. `specs/AGENTS.md` states rules too, and sequences the work through Design, Refactor, Refine. No skill is a rule's home: where a skill and a rule disagree, the rule governs and the skill is what needs correcting.

A rule without a check is a suggestion, so every rule of Spec of Record is enforced. A specification rule is checked against the files it governs by one of the audit skill's reading audits, its script first deciding whatever the files alone settle and never a judgment, since a check that cannot decide gives a confident false clear; a script listing places for a reading audit to look decides nothing. An operating rule is checked where it leaves a trace in the files the audits read, the scope's tree, the skills registry, a skill's form, a follow-up; a plan's form, a trace outside them, is checked by the skill writing the plan, its script and its steps; where a rule leaves no trace, as reading fresh, it is carried out as a named step of `specs/AGENTS.md` or a registered skill, and a skipped step is found by what it leaves wrong in the files. For every section of `specs/AGENTS.md` and of the methodology's files, the methodology's `architecture.md` and `index.md` aside since neither holds a rule of its own, `.ai/skills/audit-specs/` names the reading audit enforcing it, or names it an operating rule, whose check is a step under a registered skill's `## Workflow` applying it and giving it a point-of-use citation. A rule added or changed takes its check with it, in the same change. An audit reading only part of a section it names says which part, and the audits naming one section read all of it between them, each part once; where a step names a section too, the step carries what leaves no trace in the files and the audits read the rest.
