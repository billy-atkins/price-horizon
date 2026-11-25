## What Spec of Record Governs

Spec of Record governs files by kind. For each kind, the table gives what it holds and what names its files:

**Reference Key:** Kind \
**Required:** Holds, Named By

| Kind | Holds | Named By |
|---|---|---|
| Agent instructions | the methodology's entry point, and a project's own instructions to an agent, each an AGENTS.md file ([`specs/methodology/external-references.md § External References [Name: AGENTS.md]`](/specs/methodology/external-references.md#external-references)) | [`specs/AGENTS.md`](/specs/AGENTS.md), and `AGENTS.md` at the project's root |
| Specs | the specifications, the methodology among them | their place under `specs/`, [`specs/AGENTS.md`](/specs/AGENTS.md) aside |
| Skills | the procedures that apply the methodology's rules, the code their scripts share, and the files of their scripts' kept tests that are no fixture file, the tests' code and what runs and compares with it | [`specs/methodology/skills/registered-skills.md § Registered Skills`](/specs/methodology/skills/registered-skills.md#registered-skills), and, for the kept tests' files, their place under `tests/spec-of-record/`, the fixtures' folder aside |
| Fixture files | the files standing in the folder of the kept tests' fixtures, each a file of fixtures or the index of them ([`specs/methodology/skills/authoring-a-skill.md § Authoring a Skill`](/specs/methodology/skills/authoring-a-skill.md#authoring-a-skill)), which a reader reads only where it names the fixture files or one of them | their place under `tests/spec-of-record/fixtures/` |
| Documentation | the project's README and its guides | `README.md` at the project's root, and the files under `docs/` |
| Working files | the working files | [`specs/methodology/working-files/main.md § The Working Files`](/specs/methodology/working-files/main.md#the-working-files) |
| Code | the application's code, governed code and the wiring connecting it | the code roots the technical specs' stack names ([`specs/methodology/spec-placement/technical-stack.md § The Technical Stack`](/specs/methodology/spec-placement/technical-stack.md#the-technical-stack)) |

Whatever is not named so is outside the scope, and the methodology's rules do not reach it. Those rules, the rules of the methodology's files and of [`specs/AGENTS.md`](/specs/AGENTS.md), reach every file in scope but code and the fixture files. A rule reaches less only where its own text scopes it to something a file is not. No exemption granted elsewhere narrows a rule. Code is reached by the rules in [`specs/methodology/code.md`](/specs/methodology/code.md) and the rules that file cites for code, and by no other rule. A fixture file is reached by the rules [`specs/methodology/skills/authoring-a-skill.md § Authoring a Skill`](/specs/methodology/skills/authoring-a-skill.md#authoring-a-skill) states for the kept tests and their fixtures, and by no other rule. The constitutional principles bind code and the fixture files as they bind every file in scope ([`specs/AGENTS.md § Constitutional Principles`](/specs/AGENTS.md#constitutional-principles)). A project's root `AGENTS.md` holds that project's own instructions, and the project sets what those instructions reach.

**What reads a fixture file.** A file is a fixture file by standing under the fixtures' folder, whatever its name, its size or what it holds. Each reader of the scope's files says what it reads: a search by its target, a script by the kinds it asks the scripts' listing for, a check by its Reads ([`specs/methodology/checks.md § Check`](/specs/methodology/checks.md#check)), an audit by its Kind and its unit, and a design's work and its reviews by the design's Target and their reach. Where a reader names a kind of change, it names the operative files ([`specs/methodology/glossary/glossary.md`](/specs/methodology/glossary/glossary.md)) of that kind, and the fixture files are named by a value of their own. So a search asked for no target reads none, and neither does a check or an audit naming a kind of change and not the fixture files. What a design of a kind may change is another question, which [`specs/methodology/working-files/main.md § A Design Document § The Kinds of Change`](/specs/methodology/working-files/main.md#the-kinds-of-change) answers: a design changing the canon may change the kept tests' folder whole, its fixture files among it.

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
│   ├── checks.md
│   ├── code.md
│   ├── design-workflow/
│   ├── examples/
│   ├── expressions.md
│   ├── external-references.md
│   ├── glossary/
│   ├── modeling-constructs.md
│   ├── scope/
│   ├── semantic-check-methods/
│   ├── skills/
│   ├── sourcing-and-citation/
│   ├── spec-placement/
│   ├── spec-style/
│   └── working-files/
└── application/               the product being specified
    ├── index.md
    ├── product/               what a user can rely on
    └── technical/             how it is made true
.ai/
└── skills/
    ├── <skill-name>/          a registered skill: SKILL.md, its entry point, references/ and scripts/
    └── lib/                   the code the registered skills' scripts share
tests/
└── spec-of-record/            the kept tests of the skills' scripts, with the runner's settings
    ├── scripts/               the tests' code, and what runs and compares with it
    └── fixtures/              the fixture files the tests read, and their index
```

The tree:
- names the methodology's files and folders, since they hold the rules every task depends on, and describes none of them;
- draws each folder of the methodology by its name alone, whatever laid it out, leaving its files to the folder's own `index.md`;
- draws a directory's `main.md` and its overview only where one stands ([`specs/methodology/spec-placement/index-architecture-detail.md § Index, Architecture, Detail`](/specs/methodology/spec-placement/index-architecture-detail.md#index-architecture-detail));
- stops at `product/` and `technical/`, whose files grow with the product;
- leaves the working files to [`specs/methodology/working-files/main.md § The Working Files`](/specs/methodology/working-files/main.md#the-working-files), which names them;
- does not draw code, which sits wherever a project keeps it.

A directory's `index.md` says what each of the directory's files covers ([`specs/methodology/spec-placement/where-a-file-goes.md § Where a File Goes`](/specs/methodology/spec-placement/where-a-file-goes.md#where-a-file-goes)). So an agent reads a directory's `index.md` before working in that directory.

## The Methodology Governs Itself

The methodology is held to the rules it states:
- it has an `index.md`, and an `architecture.md` summarizing it;
- a rule that is a lookup is authored as a Decision Table ([`specs/methodology/modeling-constructs.md § Constructs § Decision Table`](/specs/methodology/modeling-constructs.md#decision-table));
- its files meet the style rules they set.

It is dogfooding, the way a company uses its own product as its clients would: using it firsthand uncovers where it should improve.

The rules on acceptance scenarios and on `technical-specs` front matter scope themselves to product specs, so they do not reach the methodology. A methodology file has no product capability to prove and no technical counterpart to name. The rules in [`specs/methodology/code.md`](/specs/methodology/code.md) reach only code, so they do not reach the methodology either.
