## Check

A check a skill makes is a test of the files, of the code or of a design against a rule. It is a script check or a semantic check ([`specs/methodology/glossary.md`](/specs/methodology/glossary.md)), as [`specs/methodology/scope.md § Rules and Skills`](/specs/methodology/scope.md#rules-and-skills) has a script decide what the files alone settle and never a judgment. A candidate list decides nothing, so it is no check of its own: it belongs to the semantic check it guides. A reading audit of `.ai/skills/audit-specs/` makes the semantic checks of the rules it enforces, over its unit.

Each check a skill makes is a record of one of this type's two concrete types, by how it is made: a [`§ Script Check`](#script-check) or a [`§ Semantic Check`](#semantic-check). The record type holds the checks a skill makes, and no other. An operating rule's check is the step applying it, as [`specs/methodology/scope.md § Rules and Skills`](/specs/methodology/scope.md#rules-and-skills) has it. The user's check is the workflow's steps in which the user reviews the work and approves it or says what should change. Neither is a script check or a semantic check, so neither takes a record.

**Where a check stands.** A check's records stand in a record section of its type under the section stating the rule it enforces, placed as [`specs/methodology/sourcing-and-citation.md § One Home Per Fact`](/specs/methodology/sourcing-and-citation.md#one-home-per-fact) places any fact. Its Tests says which of the section's rules it holds to, so a reader of the rule finds its checks there. What the checks standing under a section enforce between them is [`specs/methodology/scope.md § Rules and Skills`](/specs/methodology/scope.md#rules-and-skills)'s to say. A check holding several rules is split first, as [`specs/methodology/sourcing-and-citation.md § One Home Per Fact § One Rule to a Sentence`](/specs/methodology/sourcing-and-citation.md#one-rule-to-a-sentence) has a sentence split. A check left reading several places enforces the rule they share, and stands under that rule's own section. The skills' tables of checks hold the checks' entries until each is moved into a record.

**What a record leaves out.** No field of a check states when it runs, how it is made or what it enforces. Its type says how it is made, and the section it stands under says what it enforces. Carried Out By names what carries the check out over a skill's own units, never where a design's work runs it. Where it runs is stated where it runs: the states of the design workflow, the skills' steps and the rows of [`specs/AGENTS.md § Design, Refactor, Refine § Who Checks What and Why`](/specs/AGENTS.md#who-checks-what-and-why) that run it cite its record. Until a check's entry in a skill's table moves into a record, a state, a step or a row running it names that entry. [`specs/AGENTS.md § Design, Refactor, Refine § Who Checks What and Why`](/specs/AGENTS.md#who-checks-what-and-why) decides from its type the scope a check runs over a design's work.

Check is an abstract record type ([`specs/methodology/modeling-constructs.md § Constructs § Record Form`](/specs/methodology/modeling-constructs.md#record-form)), whose fields every check's record gives first:

**Construct:** `specs/methodology/modeling-constructs.md § Constructs § Record Form` \
**Plural Name:** Checks \
**Modifier:** Abstract \
**Reference Key:** Name

| Field | Unique | Required | Default Value | Values | Holds |
|---|---|---|---|---|---|
| Name | yes | yes | | text | the check's name, by which a citation names its record |
| Tests | no | yes | | text | what holds where the check passes, in a sentence, saying which of its section's rules it holds to |
| Reads | no | yes | | text | a list, the kinds of file the check reads, each item a kind of change [`specs/methodology/working-files.md § A Design Document § The Kinds of Change`](/specs/methodology/working-files.md#the-kinds-of-change) names, or `none`, for the working files, a design document among them, which are of no kind ([`specs/methodology/working-files.md § The Working Files`](/specs/methodology/working-files.md#the-working-files)) |
| Carried Out By | no | yes | | text | a list, an item to each skill carrying the check out over its own units: the skill's directory, then its script's flag, or the step or the reading of the skill doing so; never a design script's `--check-work`, which [`specs/AGENTS.md § Design, Refactor, Refine § Who Checks What and Why`](/specs/AGENTS.md#who-checks-what-and-why) runs over the work |

## Script Check

Script Check is the record type of a script check ([`specs/methodology/glossary.md`](/specs/methodology/glossary.md)). Its records stand as [`§ Check`](#check) places a check's records, and give the fields that type declares, adding none.

**Construct:** `specs/methodology/modeling-constructs.md § Constructs § Record Form` \
**Extends:** `§ Check` \
**Plural Name:** Script Checks

## Semantic Check

Semantic Check is the record type of a semantic check ([`specs/methodology/glossary.md`](/specs/methodology/glossary.md)). Its records stand as [`§ Check`](#check) places a check's records, and give the fields that type declares, then its own:

**Construct:** `specs/methodology/modeling-constructs.md § Constructs § Record Form` \
**Extends:** `§ Check` \
**Plural Name:** Semantic Checks

| Field | Unique | Required | Default Value | Values | Holds |
|---|---|---|---|---|---|
| Unit | no | yes | | text | what the check reads at a time |
| Candidates | no | no | none | text | a list, an item to each script listing places for the check's reading: the skill's directory, then its script's flag |

## The Areas of Checking

Each check falls in an area of checking ([`specs/methodology/glossary.md`](/specs/methodology/glossary.md)), named by what it guards. A software engineer knows each by its analog. Linked By gives where each area's link to what it checks is held, so no check's record restates it. A check of a form stands under the form's declaration, a check of a construct under the construct's definition, and a check of a rule it reads for or keeps under that rule. A workflow integrity check is linked by the state or the transition it guards, the state or the step running it citing its record. An implementation conformance check is linked by the annotation, held where the unit it marks starts.

**Reference Key:** Area \
**Required:** Guards, Analog, Linked By

| Area | Guards | Analog | Linked By |
|---|---|---|---|
| Document form | the shape of a file's text: its Markdown, headings, blank lines, fields and citations | inbound payload checks, of a schema and of what is required | the form's declaration |
| Model semantics | that each construct's instance, a table and a record section among them, is sound, complete, unambiguous and well typed | business rules | the construct's definition |
| Content meaning | that what the specs say is true, placed once, current and readable | a data-quality audit | the rules the check reads for |
| Workflow integrity | that a design moves through its work validly | a state machine's guards | the state or the transition it guards |
| Implementation conformance | that code, or a skill's script, carries out what the canon or the specs state | contract tests | the annotation, `@app-spec` from a code unit to the application spec it carries out and `@canon-spec` from a skill's script unit to the canon's check it carries out, held where the unit starts |
| System integrity | that the method holds together and keeps its bounds, every rule checked and nothing kept that should not be | security checks and configuration drift | the rule it keeps: coverage, the skills registry, what version control holds |
| Reviews | the work as a whole, by judgment | QA sign-off, and engineers reviewing a pull request | their brief, running the areas' checks over a scope and owning none |

The Reviews row names no area of checking. The reviews are judgment gates: they run the areas' checks over a scope, and own none.

**A check's area.** A check's area is the area of the rule it holds to. Its place names that rule's section, as an open question's place gives its subject ([`specs/methodology/spec-placement.md § Open Question`](/specs/methodology/spec-placement.md#open-question)). A rule's area is what the rule guards, so one section may hold checks of several areas. No area takes a type of its own. An operating rule carried out by a step stands apart: it is a step, and no check.

**Worked examples.** A rule of each area in its section, with its checks standing under it, written whole as a file would hold it, is in `specs/methodology/examples/check/area-of-checking/`.
