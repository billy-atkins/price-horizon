## What Spec of Record Governs

Spec of Record governs files by kind. For each kind, the table gives what it holds and what names its files:

**Reference Key:** Kind \
**Required:** Holds, Named By

| Kind | Holds | Named By |
|---|---|---|
| Agent instructions | the methodology's entry point, and a project's own instructions to an agent, each an AGENTS.md file ([`specs/methodology/external-references.md § External References [Name: AGENTS.md]`](/specs/methodology/external-references.md#external-references)) | [`specs/AGENTS.md`](/specs/AGENTS.md), and `AGENTS.md` at the project's root |
| Specs | the specifications, the methodology among them | their place under `specs/`, [`specs/AGENTS.md`](/specs/AGENTS.md) aside |
| Skills | the procedures that apply the methodology's rules, and the code their scripts share | [`specs/methodology/skills/registered-skills.md § Registered Skills`](/specs/methodology/skills/registered-skills.md#registered-skills) |
| Documentation | the project's README and its guides | `README.md` at the project's root, and the files under `docs/` |
| Working files | the working files | [`specs/methodology/working-files/main.md § The Working Files`](/specs/methodology/working-files/main.md#the-working-files) |
| Code | the application's code, governed code and the wiring connecting it | the code roots the technical specs' stack names ([`specs/methodology/spec-placement/technical-stack.md § The Technical Stack`](/specs/methodology/spec-placement/technical-stack.md#the-technical-stack)) |

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
│   ├── checks.md
│   ├── code.md
│   ├── design-workflow/
│   ├── examples/
│   ├── expressions.md
│   ├── external-references.md
│   ├── glossary/
│   ├── modeling-constructs.md
│   ├── scope/
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
