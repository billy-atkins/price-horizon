## What Spec of Record Governs

Spec of Record governs the files of these kinds, each named the way the table gives:

| Kind | Holds | Named by |
|---|---|---|
| Agent instructions | the method's entry point, and a project's own instructions to an agent | `specs/AGENTS.md`, and `AGENTS.md` at the project's root |
| Specs | the specifications, the methodology among them | their place under `specs/`, `specs/AGENTS.md` aside |
| Skills | the procedures that apply the method's rules | `specs/methodology/skills.md` |
| Working files | what writing the specs leaves behind | `specs/methodology/working-files.md § The Working Files` |

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
└── skills/<skill-name>/       a registered skill: SKILL.md, its entry point, and scripts/
```

The tree names the methodology's files, since they are the rules every task depends on, and describes none of them; it stops at `product/` and `technical/`, whose files grow with the product; and it leaves the working files to `specs/methodology/working-files.md § The Working Files`, which names them. What a file covers is its directory's `index.md` (`specs/methodology/spec-placement.md § Where a File Goes`), so before working in a directory an agent reads its `index.md`.

## Progressive Disclosure

An agent loads what its current step needs, when the step needs it, descending only as far as the step requires: from `specs/AGENTS.md`'s routing table, which maps a task to the rule governing it, to this scope, to a directory's `index.md`, to a file, and to the section a citation names. What is loaded long before it is needed sits behind everything loaded since and competes with all of it; what is loaded at the step that needs it is at the front of the agent's attention and carries its full weight.

Progressive disclosure governs when to read, not how much. Whatever is loaded is read in full and never skimmed, and read fresh rather than recalled (`specs/AGENTS.md § Design, Refactor, Refine (DRR)`), and a task whose unit is a whole directory, an audit among them, loads the whole directory. The path it relies on is checked: every directory under `specs/` has an `index.md` naming each of its files, and `§ The Shape of the Scope` names what exists.

## The Methodology Governs Itself

The methodology is held to the rules it states: it has an `index.md`, and an `architecture.md` summarizing it, a rule that is a lookup is authored as a table, and its files meet the style rules they set. The rules on acceptance scenarios and on `technical-specs` frontmatter scope themselves to product specs, and so do not reach it: a methodology file has no product capability to prove and no technical counterpart to name.

## Rules and Skills

The methodology's files state rules. They do not sequence the work, record what goes wrong while following it, check whether a result conforms, or teach the craft a rule assumes; the skills `specs/methodology/skills.md` registers do, and a cold agent needs them to follow the method in practice. `specs/AGENTS.md` states rules too, and sequences the work through Design, Refactor, Refine. No skill is a rule's home: where a skill and a rule disagree, the rule governs and the skill is what needs correcting.
