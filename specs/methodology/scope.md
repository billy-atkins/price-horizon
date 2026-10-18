## What Spec of Record Governs

Spec of Record governs files by kind. For each kind, the table gives what it holds and what names its files:

**Reference Key:** Kind

**Required:** Holds, Named By

| Kind | Holds | Named By |
|---|---|---|
| Agent instructions | the methodology's entry point, and a project's own instructions to an agent, each an AGENTS.md file ([`specs/methodology/external-references.md § External References [Name: AGENTS.md]`](/specs/methodology/external-references.md#external-references)) | [`specs/AGENTS.md`](/specs/AGENTS.md), and `AGENTS.md` at the project's root |
| Specs | the specifications, the methodology among them | their place under `specs/`, [`specs/AGENTS.md`](/specs/AGENTS.md) aside |
| Skills | the procedures that apply the methodology's rules, and the code their scripts share | [`specs/methodology/skills.md`](/specs/methodology/skills.md) |
| Documentation | the project's README and its guides | `README.md` at the project's root, and the files under `docs/` |
| Working files | the working files | [`specs/methodology/working-files.md § The Working Files`](/specs/methodology/working-files.md#the-working-files) |
| Code | the application's code, governed code and the wiring connecting it | the code roots the technical specs' stack names ([`specs/methodology/spec-placement.md § The Technical Stack`](/specs/methodology/spec-placement.md#the-technical-stack)) |

Whatever is not named so is outside the scope, and the methodology's rules do not reach it. Those rules, the rules of the methodology's files and of [`specs/AGENTS.md`](/specs/AGENTS.md), reach every file in scope but code. A rule reaches less only where its own text scopes it to something a file is not. No exemption granted elsewhere narrows a rule. Code is reached by the rules in [`specs/methodology/code.md`](/specs/methodology/code.md) and the rules that file cites for code, and by no other rule. A project's root `AGENTS.md` holds that project's own instructions, and the project sets what those instructions reach.

## The Shape of the Scope

```
AGENTS.md                      the project's own instructions, pointing to specs/AGENTS.md
README.md                      the project's documentation, read first
docs/                          its guides
specs/
├── AGENTS.md                  the entry point to Spec of Record
├── index.md                   in every directory under specs/: what it holds
├── architecture.md            the overview of the specifications as a whole
├── methodology/               the rules for writing specs, and for the code the specs govern
│   ├── index.md
│   ├── architecture.md
│   ├── acceptance-scenarios.md
│   ├── code.md
│   ├── design-workflow.md
│   ├── examples/
│   ├── expressions.md
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

- names the methodology's files, since they hold the rules every task depends on, and describes none of them;
- stops at `product/` and `technical/`, whose files grow with the product;
- leaves the working files to [`specs/methodology/working-files.md § The Working Files`](/specs/methodology/working-files.md#the-working-files), which names them;
- does not draw code, which sits wherever a project keeps it.

A directory's `index.md` says what each of the directory's files covers ([`specs/methodology/spec-placement.md § Where a File Goes`](/specs/methodology/spec-placement.md#where-a-file-goes)). So an agent reads a directory's `index.md` before working in that directory.

## Progressive Disclosure

An agent loads what its current step needs, when the step needs it, descending only as far as the step requires:

- from [`specs/AGENTS.md`](/specs/AGENTS.md), which sends a change to the procedure that governs it,
- to that procedure's step and the reference it forks to,
- to a directory's `index.md`,
- to a file,
- and to the section a citation names.

What is loaded long before it is needed sits behind everything loaded since, and competes with all of it. What is loaded at the step that needs it is at the front of the agent's attention, and carries its full weight.

Worked examples teach applying the canon's forms, as [`specs/methodology/spec-style.md § Clear Prose`](/specs/methodology/spec-style.md#clear-prose) has an example teach, and they are loaded the same way. They sit in `specs/methodology/examples/`, a tree whose path names what each example shows, as a Java package's name is its directory, so an agent that knows what it needs knows where it is. The path runs broad to narrow, a subject and then a topic within it, as `examples/construct/dag/` or `examples/time/calendar/`. The directories at one level are one kind of thing, a subject's topics the things its section of the canon defines, as the constructs and the Fact they declare are the construct subject's, each named in singular kebab-case as the canon names it, and one word names one concept wherever the canon writes it. An example sits under the topic it shows, whichever file states the topic's rule, and one showing two topics sits under the one it is chiefly about. The section stating a topic's rule names the topic's directory, whose `index.md` describes each example, and an agent loads an example only where its step needs one.

The glossary is the one methodology file loaded ahead of need. An agent reads it with [`specs/AGENTS.md`](/specs/AGENTS.md) before any step, since the agent cannot know a word is one of the glossary's terms without having read the glossary.

An agent reads what it loads from a directory in the order that the directory's `index.md` lists, a parent directory before the directories under it. That order is the one the directory's authors set ([`specs/methodology/spec-placement.md § Where a File Goes`](/specs/methodology/spec-placement.md#where-a-file-goes)). Progressive disclosure governs when to read, not how much. Whatever is loaded is read in full, never skimmed, and read fresh rather than recalled ([`specs/AGENTS.md § Design, Refactor, Refine`](/specs/AGENTS.md#design-refactor-refine)). A task whose unit is a whole directory, an audit among them, loads the whole directory.

## The Methodology Governs Itself

The methodology is held to the rules it states:

- it has an `index.md`, and an `architecture.md` summarizing it;
- a rule that is a lookup is authored as a Decision Table ([`specs/methodology/modeling-constructs.md § Constructs § Decision Table`](/specs/methodology/modeling-constructs.md#decision-table));
- its files meet the style rules they set.

It is dogfooding, the way a company uses its own product as its clients would: using it firsthand uncovers where it should improve.

The rules on acceptance scenarios and on `technical-specs` front matter scope themselves to product specs, so they do not reach the methodology. A methodology file has no product capability to prove and no technical counterpart to name. The rules in [`specs/methodology/code.md`](/specs/methodology/code.md) reach only code, so they do not reach the methodology either.

## Agent Agnostic

The instructions in Spec of Record's scope, both `AGENTS.md` files and each registered skill, stay agnostic of which agent reads them. They use no vendor-specific instruction filename and no tool-specific directory, and they assume nothing about which model, CLI, or editor is running.

**The test.** Would anything new still make sense to an agent from a different vendor, or to a person reading it directly?

**The one exception.** Anything written for one tool is allowed, and only because it carries no content:

- an opt-in helper outside the methodology's scope, named for the tool it serves, may wire that tool up to the agnostic content;
- an agent setting itself up may write what it needs to carry out a choice the methodology leaves to it ([`specs/methodology/skills.md § Setting Up an Agent`](/specs/methodology/skills.md#setting-up-an-agent)).

Whatever either writes is kept out of version control and outside the scope. Nothing depends on its having been written. A skill stays readable directly, and what was written only saves a step, or applies a choice, for someone using that tool.

## Rules and Skills

The methodology's files state rules. They do not sequence the work, record what goes wrong while following it, check whether a result conforms, or teach the craft a rule assumes. The skills that [`specs/methodology/skills.md`](/specs/methodology/skills.md) registers do those things, and a cold agent needs them to follow the methodology in practice. [`specs/AGENTS.md`](/specs/AGENTS.md) states rules too, and sequences the work through the Design, Refactor, Refine process. The methodology's files and [`specs/AGENTS.md`](/specs/AGENTS.md), with the specifications' overview, make up the core canon ([`specs/methodology/glossary.md`](/specs/methodology/glossary.md)). The skills, with the code they share, are the rest of the canon. No skill is a rule's home. Where a skill and a rule disagree, the rule governs, and the skill is what needs correcting.

A rule without a check is a suggestion, so every rule of Spec of Record is enforced. A rule added or changed takes its check with it, in the same change. [`specs/methodology/spec-style.md § Clear Prose`](/specs/methodology/spec-style.md#clear-prose), as it reaches the working files, stands without a check. The user holds the working files to it in reading them, since an audit of files that never last would cost more than it finds.

**A specification rule.** It is checked against the files it governs by one of the audit skill's reading audits. A rule of [`specs/methodology/code.md`](/specs/methodology/code.md) is checked instead by a check of `.ai/skills/verify-spec-implementation/` that reads the code. Either skill's script first decides whatever the files alone settle. The script never decides a judgment, since a check that cannot decide gives a confident false clear. A script that lists places for a reading audit to look decides nothing.

**An operating rule.** It is checked where it leaves a trace in the files the audits read: the scope's tree, the skills registry, a skill's form, a follow-up. A plan's form leaves its trace outside those files. The skill that writes the plan checks the plan's form, through the skill's script and steps. Where a rule leaves no trace, as reading fresh leaves none, the rule is carried out as a named step of [`specs/AGENTS.md`](/specs/AGENTS.md) or of a registered skill. A skipped step is found by what it leaves wrong in the files.

**Which check enforces each section.** `.ai/skills/audit-specs/` covers every section of [`specs/AGENTS.md`](/specs/AGENTS.md) and of the methodology's files, except the methodology's `architecture.md` and `index.md` and its worked examples under `examples/`, which hold no rule of their own. For each section, it names the reading audit that enforces the section, or names the section an operating rule. An operating rule's check is a step under a registered skill's `## Workflow` that applies the rule and gives it a point-of-use citation. For a section of [`specs/methodology/code.md`](/specs/methodology/code.md), `.ai/skills/verify-spec-implementation/` names the check that enforces it instead, or `.ai/skills/audit-specs/` names it an operating rule.

**A section read in parts.** An audit that reads only part of a section it names says which part. The audits that name one section read all of it between them, each part once. Where a step names the section too, the step carries what leaves no trace in the files, and the audits read the rest.
