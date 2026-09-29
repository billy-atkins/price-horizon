---
name: audit-specs
description: Audit the project against the rules that govern it by reading it. Use when a directory's summary may have fallen behind its files, when a capability's scenarios may not cover what it promises, when a rule may be stated twice or in the wrong file, when something may cite a section for a rule that section does not state, when a number or a positional reference may be restating a list, when a term may be defined outside the glossary or used against its sense there, when a diagram may no longer match what it renders, when a spec may describe in prose what a construct should hold, when a file may sit in the wrong place, when drafting residue may remain, when an instruction may assume a particular agent, when a skill may not meet the authoring rules, when a working file's entry may have lost its form, when a rule may have no check, or after any change large enough that something restating it has gone stale. Reading audits, with a script that clears the mechanically decidable failures first.
---

# Auditing the specifications

The methodology and `specs/AGENTS.md` govern every file in Spec of Record's scope, per `specs/methodology/scope.md § What Spec of Record Governs`. Checking that they held splits into separate jobs.

A script decides whether a citation resolves, a frontmatter list is sorted, a fenced block is well-formed. Everything that has actually gone wrong here was a statement that resolved perfectly and was wrong anyway: a blueprint omitting the security control its own directory calls primary passes every mechanical check ever written.

The audits are the substance. The script is a pre-pass.

    python .ai/skills/audit-specs/scripts/audit-specs.py           # from the repo root
    python .ai/skills/audit-specs/scripts/audit-specs.py <path>    # explicit root
    python .ai/skills/audit-specs/scripts/audit-specs.py --candidates    # also list places for the reading audits that use them

Run it first, because it is fast and because its findings would otherwise be noise in a reading pass.

## These audits assume an agent

Each one requires a judgment the files do not encode, often across a whole directory held in mind at once. A script cannot judge whether a summary is still true. A person can, but does it by sampling, with attention that degrades across a long directory. Reading a whole unit in one pass and holding it together is what makes a method this exhaustive worth writing down rather than aspiring to.

## The method

Every audit follows the steps below.

**Start from the entry point —** `specs/AGENTS.md`, then `specs/methodology/glossary.md`, and a directory's `index.md` before working in it, per `specs/methodology/scope.md § Progressive Disclosure`.

**Read the files in full —** not headings, not a previous read, not recall, per `specs/methodology/scope.md § Progressive Disclosure`. The one time a directory summary was built from headings and memory, it missed the largest gap in the directory.

**Compare against the open source, not against the summary —** re-reading a summary confirms it reads well, which it always does. The defect is only visible with the source beside it.

Where an audit compares one passage against what it restates, the ways a compression goes wrong are listed in the `design-specs` skill, in its section on compression distortion. Use that taxonomy rather than restating it. It applies to Directory summary currency, to Diagram currency, and to Whether the home holds the fact wherever a citer states in its own words what it attributes. The other audits compare no two versions of one passage, and it does not reach them.

## The audits

| Audit | Enforces |
|---|---|
| Directory summary currency | `specs/methodology/sourcing-and-citation.md § Keeping Renderings in Step`, `specs/methodology/spec-placement.md § Index, Architecture, Detail`, `specs/methodology/scope.md § The Shape of the Scope` |
| Counterpart currency | `specs/methodology/sourcing-and-citation.md § Keeping Renderings in Step`, `specs/methodology/spec-placement.md § Product or Technical`, `specs/methodology/spec-placement.md § Naming the Technical Files Behind a Capability` |
| Scenario coverage | `specs/methodology/acceptance-scenarios.md § Acceptance Scenarios`, `specs/methodology/acceptance-scenarios.md § Deciding What to Write`, `specs/methodology/acceptance-scenarios.md § Keeping a Scenario and Its Prose in Step` |
| Where a rule lives | `specs/methodology/sourcing-and-citation.md § One Home Per Fact`, `specs/methodology/sourcing-and-citation.md § Keeping Renderings in Step`, `specs/methodology/sourcing-and-citation.md § Which Citations Are Allowed`, `specs/methodology/scope.md § What Spec of Record Governs`, `specs/methodology/scope.md § The Methodology Governs Itself` |
| Whether the home holds the fact | `specs/methodology/sourcing-and-citation.md § One Home Per Fact`, `specs/methodology/sourcing-and-citation.md § Writing a Citation` |
| Ordinals and counts | `specs/AGENTS.md § Ordinals and Counts` |
| Markup | `specs/methodology/modeling-constructs.md § Fields`, `specs/methodology/modeling-constructs.md § Bold Lead-ins`, `specs/methodology/modeling-constructs.md § Emphasis`, `specs/methodology/modeling-constructs.md § Literal Text`, `specs/methodology/sourcing-and-citation.md § Titling a Heading` |
| Glossary terms | `specs/methodology/glossary.md § Glossary`, `specs/methodology/glossary.md § Writing an Entry` |
| Construct choice and form | `specs/methodology/modeling-constructs.md § Purpose`, `specs/methodology/modeling-constructs.md § Constructs`, `specs/methodology/modeling-constructs.md § When to Use Which`, `specs/methodology/acceptance-scenarios.md § Why a Scenario Is Not a Modeling Construct` |
| Placement | `specs/methodology/spec-placement.md § Where a File Goes`, `specs/methodology/spec-placement.md § Naming a Capability Domain`, `specs/methodology/spec-placement.md § An Open Question` |
| Finished style | `specs/methodology/spec-style.md § What a Finished Spec Reads Like`, `specs/methodology/spec-style.md § Trade-offs Are Not Journey Language` |
| Agent agnostic | `specs/AGENTS.md § Agent Agnostic` |
| Skill form | `specs/AGENTS.md § Authoring Skills`, `specs/methodology/scope.md § Rules and Skills`, `specs/methodology/skills.md § Registered Skills` |
| Working-file form | `specs/methodology/working-files.md § The Working Files`, `specs/methodology/working-files.md § A Design Entry`, `specs/methodology/working-files.md § A Follow-up`, `specs/AGENTS.md § Design, Refactor, Refine (DRR)` |
| Diagram currency | `specs/methodology/modeling-constructs.md § Diagrams`, `specs/methodology/sourcing-and-citation.md § Keeping Renderings in Step` |

Each audit reads its unit against every rule the sections in its Enforces column state, or the part of one its text names (`specs/methodology/scope.md § Rules and Skills`); what an audit's own text adds is how to read, what is easy to miss, and how a finding is fixed (`specs/AGENTS.md § Authoring Skills`).

### Directory summary currency

The summaries are separate units, because they cover different ground: an `index.md` covers a directory's direct contents, and an `architecture.md` covers everything beneath the directory that owns it. Read the tree once, then check the blueprint against all of it and each `index.md` row against its own file. Of `specs/methodology/sourcing-and-citation.md § Keeping Renderings in Step`, this audit reads its paragraph on a directory's `architecture.md`.

The finding usually missed in a blueprint is an omission: a fact its detail files establish that a reader of the blueprint alone would never learn. The test for it is not "is it stated somewhere else" but "would a reader of this file alone form a false impression, or find a later section unfollowable."

### Counterpart currency

Take each product file's `technical-specs` frontmatter as the map and read both sides. Then sweep the other way, checking that each product section a technical file cites has its file's list naming that technical file, since a missing frontmatter entry is the likelier failure and the frontmatter map cannot see it. Of `specs/methodology/sourcing-and-citation.md § Keeping Renderings in Step`, this audit reads its paragraph on a product spec and its technical counterpart.

Sweep the same pairing once more, for the converse: an entry naming a technical file that cites nothing in that product file back. It is a judgment rather than an arithmetic check, which is why it is easy to skip, and reading decides which of two things it is: a file supplying context a capability depends on without implementing a promise of its own, which the list's own scope allows (`specs/methodology/spec-placement.md § Naming the Technical Files Behind a Capability`), or a missing citation on the technical side, which is the finding. What settles it is whether that technical file makes any promise this product file states.

Overlap between the two sides is intended, as `specs/methodology/spec-placement.md § Product or Technical` explains, and is not the finding; a side that has stopped doing its own job is.

### Scenario coverage

First find each capability section with no `Test Scenarios` block at all, since reading a block cannot reach a section that has none. Then read each block against its own section's prose, both ways: a promise or a guardrail with no scenario, and a scenario asserting what the prose does not (`specs/methodology/acceptance-scenarios.md § Deciding What to Write`).

### Where a rule lives

One pass per unit, over every normative statement in it, read against the unit and the files that state the rules, `specs/AGENTS.md` and `specs/methodology/`. A rule in the wrong file and a rule in two files need the same sweep, so they are one audit. Of `specs/methodology/sourcing-and-citation.md § Keeping Renderings in Step`, this audit reads its statement that a rendering is not a second home.

Inventory first, then compare. Collect every normative statement in the unit, and in the files that state the rules, before judging any of them — whether a rule already has a home cannot be answered about the first file until the last one has been read, and a pass that judges as it goes degrades into sampling.

Inventory within a file and within a section too, not only across files. A duplicate inside one section is the one this audit reliably misses, because the two copies are read as one passage in one sitting and a passage does not feel like it disagrees with itself. The shape to watch for is a rule stated once in a table and again in the prose around it: the table row is the enumeration, the paragraph restates it while adding something real, and the restatement is invisible because it arrives as continuation rather than repetition. Counting sites is what catches it — a rule found in two files is often in three.

One signal is worth naming, because it looks like the opposite of a defect: a passage that cites another file's rule and then adds more than `specs/methodology/sourcing-and-citation.md § One Home Per Fact` lets a citing place add. The extension reads as deference precisely because the citation is there. Of that section, the bare citation owing its application or its reason is Whether the home holds the fact's to find; this audit reads the rest.

Product and technical are never compared with each other, for the reason `specs/methodology/spec-placement.md § Product or Technical` gives.

**An `architecture.md` restates its own directory by design, and those restatements are not findings —** a false-positive trap the audit sets, and an expensive one. An overview restates constantly and by instruction (`specs/methodology/spec-placement.md § Index, Architecture, Detail`), and neither it nor a diagram is a second home (`specs/methodology/sourcing-and-citation.md § Keeping Renderings in Step`); an auditor who has not read those sections finds the overview restating half the directory and reports it as the most drifted file present, confidently and at length. What stays a finding, and is easy to miss while discounting everything else it restates, is an `architecture.md` duplicating *itself*, or restating what lives outside its own directory.

Where a duplicate is real, choose the home by `specs/methodology/sourcing-and-citation.md § One Home Per Fact`'s test, a rule several files use placed as that section says, and replace the others with citations. Where `specs/methodology/sourcing-and-citation.md § Which Citations Are Allowed` forbids that citation, as for an application spec restating a methodology rule, the restatement is cut back to the spec's own content instead.

### Whether the home holds the fact

What nothing else checks is that a cited home still states the fact attributed to it, as `specs/methodology/sourcing-and-citation.md § Writing a Citation` requires. A citer says "X is governed there"; the audit asks whether *X* is actually there.

This is the audit that catches the most and is the easiest to leave out, because every symptom of it looks fine. The heading resolves, so the script clears it. The citer reads as correct, because it says what it means. The target reads as correct, because a section is not obviously missing a sentence. The defect exists only in the gap between two files that are each individually clean, and the citation being valid is precisely what hides it.

Sweep by target, not by citer. Take a section that is cited from several places, gather every citation into it at once, and write down what each citer attributes to it before opening it. Then read the target and check each attribution off. Doing it citer-by-citer is what fails: one file attributing something absent looks like that file's own imprecision, and it takes the second citer to reveal that the target is what is thin.

**A bare citation that needed more —** with every citer of a section gathered, read each as an agent reading only that place would, against the sentence of `specs/methodology/sourcing-and-citation.md § One Home Per Fact` on when a citing place states a rule's application and its reason, the one part of that section this audit reads. A citation that only routes or lists, a routing row, a Sources bullet, an Enforces cell or a `technical-specs` entry, applies no rule, and bare is enough there. A bare citation reads as correct because nothing in it is wrong, which is why it is missed.

Each shape below is a finding, fixed on the side that is wrong rather than by weakening the citation:

- **The target never states the rule —** a capability file cites a guarantees section as holding a ceiling on what it may display; that section's prose never mentions the ceiling, only its scenarios imply it. The prose is what is missing.
- **The target states it differently, and the citer is right —** a second file cites the same section while stating the rule in its correct, narrower form. When a citer is more accurate than the home it cites, the home is what is stale, and the citer's wording is the best available evidence of what the rule should say; once the home holds it, the citer's restatement gives way to its citation.
- **A stage's own fact has no home anywhere —** the mechanism is specified on the technical side, the scenario asserts it, every file assumes it, and no product section states it. This surfaces here rather than under Scenario coverage, because what reveals it is a citation looking for a fact rather than a scenario looking for prose.

A target that never states the rule and a target that states it differently are the ordinary cases and both were found in this repo on the first run of it. Note what they share: a heavily-cited section accumulates attributions faster than it is re-read, so the most-cited section in a directory is where to start, not where to stop.

Same-layer citations count. Counterpart currency covers product against technical; this audit covers every direction a citation is allowed to point, and product-to-product is where both real cases were found.

**After a change lands, the target set is not a judgment call —** every section whose meaning the change altered is a mandatory target, because a citation written against the old meaning is still a valid citation and nothing else will surface it. Choosing targets by how heavily cited they are is the rule for an audit run on a tree nobody just edited; run after a change, this audit starts from the sections that changed and sweeps outward from each.

**Sweep twice, by citation and by wording, because they find different things —** a citation sweep finds citers. It does not find a passage that restates the fact without citing it, and those are common in exactly the places that are supposed to track a change: a diagram, an `architecture.md`'s prose, a table row rendering a rule stated elsewhere. Take the fact's own distinctive phrasing and grep for it across the tree: that is the wording pass.

The evidence for needing both is one pass in this repo where a change widened a guarantee's condition. The citation sweep checked every citer of the amended section and every attribution held — a clean result, correctly reported. Further copies of the superseded wording survived anyway, neither of them citing anything: one in a paragraph restating the guarantee, one in a diagram node whose own source table said it was "kept in sync with these tables whenever they change." Both were found by grepping the old phrasing. A sweep that had run only by citation would have closed the audit and left both.

### Ordinals and counts

Run the script with `--candidates`, then read the files in scope in full, using the candidates as a guide to where numbers are likely rather than as the boundary of the search. Judge every number against `specs/AGENTS.md § Ordinals and Counts` as written: a violation gets a proposed rewrite, and a decline names that section's reason for keeping the number. A violation the patterns missed is reported like any other, and its phrasing is a candidate for a new pattern.

### Markup

The script decides where bold and italic may appear, a field's key, and a heading's form; whether a backtick span holds literal text and an italic span real stress, per `specs/methodology/modeling-constructs.md § Literal Text` and `specs/methodology/modeling-constructs.md § Emphasis`, is the judgment it cannot make. Run it with `--candidates`, which lists each backtick span holding a capital letter and no punctuation that matches no heading, field key, or text a fenced example in the tree holds, and each italic span of more than a few words, then read the files in scope in full, using the candidates as a guide rather than as the boundary. Among bold lead-ins and headings, the case to look for is a lead-in a citation needs.

### Glossary terms

A use in a file's own ordinary sense, an application spec's product record or data field among them, is outside this audit unless it could be misread as the method's. Run the script with `--candidates`, which lists each line outside the glossary where a glossary term or one of its other names seems to be defined, then read the files in scope in full against `specs/methodology/glossary.md`, using the candidates as a guide rather than as the boundary. A second definition is cut, leaving what its file says about the term, and a term used in the method's sense but differently is reworded or, where the sense recurs, the glossary is corrected.

### Construct choice and form

What reading passage by passage misses: prose that reads complete but that a construct would show has a gap, and a construct's own cross-references, a jump to a step or a transition to a state, which only reading its tables together catches. A Record Form of a type the script does not know is read here alone.

### Placement

What is easy to miss: a file named by a bare filename another directory shares, and an open question recorded in a file that cannot cite everything it impacts.

### Finished style

Run the script with `--candidates`, which lists each line holding a phrase the Example column of `specs/methodology/spec-style.md § What a Finished Spec Reads Like`'s table quotes, and use the list as a guide rather than as the boundary. A trade-off that passes its section's test is declined with the reason.

### Agent agnostic

Run the script with `--candidates`, which lists each line naming a vendor, a model or a tool-specific path. The root `AGENTS.md` naming its opt-in helpers, and with them the tools they serve, is what the section's exception allows, and the usual candidate to decline.

### Skill form

The script decides a registered skill's front matter and script names; the rest is read here, with each unregistered skill `--candidates` lists read against the registry's test and the import candidates guiding the standard-library rule. What is easy to miss: a skill restating a rule it should cite, a row of the operating table naming a step its skill no longer has, and a row of the script table no longer describing what the script checks.

### Working-file form

What is easy to miss: an applied design entry whose Status names no adversarial DRR, work an entry defers with no follow-up recording it, and a follow-up leaning on a skill's output under `.ai/tmp/`, which the skill clears once it is stale.

### Diagram currency

Run only once the script's diagram check passes; if it fails, the work is fixing the citations, and there is nothing yet to compare. Then render the diagram through `.ai/skills/author-mermaid-diagram/`, read every section its Sources list names, and read the picture against them, each label against the diagram's host file, and the list against where each thing it draws lives. A source the current change edited is where to look first. Of `specs/methodology/sourcing-and-citation.md § Keeping Renderings in Step`, this audit reads its paragraph on a diagram. A picture saying something its sources do not takes the report row for a summary that disagrees with what it summarizes; a source missing from the list, or a listed section that is only a summary of the home or broader than `specs/methodology/modeling-constructs.md § Diagrams` asks, takes the row for a required thing that is absent or sits on the wrong side.

## The report

A run states the unit it covered and a verdict on it: current, current with named fixes, or drifted. Findings are rows in one of the shapes below, depending on what kind of defect it is.

| Defect | Row |
|---|---|
| A summary disagrees with what it summarizes | the file, the claim, the source, and which compression distortion it is |
| A required thing is absent, or sits on the wrong side | the location, the rule it breaks, and what is missing or misplaced |
| A rule has two homes | both statements, the home chosen, and, where it was hoisted, the usages that forced its height |

A report also carries what was examined and declined: the candidate that had the shape of a defect and turned out not to be one, with the reason it failed the test. This is not padding and not optional. An audit's expensive half is arriving at the judgment that something suspicious is correct, and a report that keeps only the findings throws that half away, so the next run pays for it again and may reach the opposite answer. Declining a candidate in writing is also what makes an over-eager audit reviewable: a reader can check a rejection as easily as a finding.

Output goes to `.ai/tmp/audit-specs/`, one file per run named for the unit and the date. A run clears any earlier report for the same unit, the stale output `specs/AGENTS.md § Authoring Skills` has a skill clean.

A finding becomes a design entry (`specs/methodology/working-files.md § A Design Entry`) rather than an edit, taken through `specs/AGENTS.md § Design, Refactor, Refine (DRR)`, which also says when a small one may be applied directly instead.

## Running one

`specs/AGENTS.md § Design, Refactor, Refine (DRR)` covers briefing a reader, verifying findings before acting on them, and who runs an audit. All of it applies. What an audit run by the content's own author costs here is a confident sweep that misses the section its author forgot existed.

## Scoping a run

| Audit | Unit |
|---|---|
| Directory summary currency | the tree rooted at a directory owning an `architecture.md`, plus each `index.md` beneath it |
| Counterpart currency | per product file, and each technical file no product file's `technical-specs` names |
| Scenario coverage | per product file |
| Where a rule lives | per unit: `AGENTS.md`, `specs/AGENTS.md`, `specs/methodology/`, `specs/application/product/`, `specs/application/technical/` |
| Whether the home holds the fact | per cited section, taking every citation into it in one pass |
| Ordinals and counts | the files a change touched, or everything in the script's scope for a full run |
| Markup | the files a change touched, or everything in the script's scope for a full run |
| Glossary terms | the glossary and the files a change touched, or everything in the script's scope for a full run |
| Construct choice and form | the specs a change touched, or every spec for a full run |
| Placement | per directory, its `index.md` and every file in it, with the product `architecture.md` for the product side |
| Finished style | the specs a change touched, or every spec for a full run |
| Agent agnostic | both `AGENTS.md` files, each registered skill, the project's `.gitignore`, and the helpers the root `AGENTS.md` names |
| Skill form | `specs/methodology/skills.md`, each registered skill, and each unregistered one `--candidates` lists |
| Working-file form | `.ai/designs.md` and `.ai/follow-ups.md` |
| Diagram currency | per diagram, with every section its Sources list names |

`specs/index.md` and `specs/application/index.md` sit above every architecture-rooted tree, so a directory summary run names them explicitly or nothing covers them.

## What the script checks

Each row describes, in the script's own terms, what it checks for the rule it names, and that rule governs it (`specs/methodology/scope.md § Rules and Skills`).

| Check | Rule |
|---|---|
| Every `file § A § B` resolves to that heading path in that file | `specs/methodology/sourcing-and-citation.md § Writing a Citation` |
| A citation never points down a layer except from `specs/AGENTS.md`, never crosses between application and methodology or from an application spec to `specs/AGENTS.md`, whether it names a section or a whole file, and no spec cites a section of the project's root `AGENTS.md` | `specs/methodology/sourcing-and-citation.md § Which Citations Are Allowed` |
| No citation targets an `index.md` | `specs/methodology/sourcing-and-citation.md § Writing a Citation` |
| A cross-file citation carries a project-root path | `specs/methodology/sourcing-and-citation.md § Writing a Citation` |
| Every section token sits inside a backtick span | `specs/methodology/sourcing-and-citation.md § Writing a Citation` |
| A heading carries no ordinal, no section token, and is unique among its siblings | `specs/methodology/sourcing-and-citation.md § Titling a Heading` |
| A `Test Scenarios` section sits one level below its capability, and a file holding one holds a `gherkin` fence | `specs/methodology/acceptance-scenarios.md § Acceptance Scenarios` |
| Every `gherkin` block parses: each `Scenario:` followed by at least one `Given`, `When`, and `Then` | `specs/methodology/acceptance-scenarios.md § Acceptance Scenarios` |
| Every `technical-specs` list is alphabetically sorted, appears only in a product file, and every path in it resolves under the technical directory | `specs/methodology/spec-placement.md § Naming the Technical Files Behind a Capability` |
| `specs/methodology/glossary.md` holds no citation and one table, headed Term and Definition, whose Term cells are bare terms, unique and sorted, each with a definition; each definition ends with its other names in the fixed form, and no other name is shared by two terms or equals a term | `specs/methodology/glossary.md § Writing an Entry` |
| Every section of `specs/AGENTS.md` and of each file in `specs/methodology/` but its `architecture.md` and `index.md` is named, itself or through a section it sits under, in the Enforces column of `§ The audits` or the Operating rule column of `§ Operating rules carried out by a step` | `specs/methodology/scope.md § Rules and Skills` |
| No spec embeds an image | `specs/methodology/modeling-constructs.md § Diagrams` |
| Each working file `specs/methodology/working-files.md § The Working Files` names is ignored by a line of the project's `.gitignore` naming it or a directory holding it, and no negating line un-ignores it | `specs/methodology/working-files.md § The Working Files` |
| Every directory under `specs/` has an `index.md`, naming each file and subdirectory it holds, each row naming one that exists | `specs/methodology/spec-placement.md § Where a File Goes` |
| The script's scope is read from `specs/methodology/skills.md` and the files `specs/methodology/scope.md § What Spec of Record Governs` names; a missing or empty registry is a finding, never an empty scope | `specs/methodology/scope.md § What Spec of Record Governs` |
| The tree in `specs/methodology/scope.md § The Shape of the Scope` names exactly the files in `specs/methodology/`, and every path it names exists | `specs/methodology/scope.md § The Shape of the Scope` |
| The kinds in `specs/methodology/scope.md § What Spec of Record Governs` are the ones the script reads, and each home the table names exists | `specs/methodology/scope.md § What Spec of Record Governs` |
| Every row of the registry in `specs/methodology/skills.md` names a skill in backticks with a directory under `.ai/skills/` | `specs/methodology/skills.md § Registered Skills` |
| Every registered skill's `SKILL.md` opens with YAML front matter whose `name` is its directory's name, in kebab-case, and whose `description` is present; a `scripts/` directory beside it, where it has one, holds an entry-point script named for the skill | `specs/AGENTS.md § Authoring Skills` |
| Every diagram in `specs/` sits directly under a heading of its own whose section holds, in this order and nothing else, the diagram, a single `**Caption:**` paragraph citing no section and no file, and a `**Sources:**` line followed by one citation per bullet, sorted, each resolving to a section or a record other than the diagram's own; and every listed section carries a citation of that diagram's heading in its own text, or, for a record section or a record, in that record section's `**Diagrams:**` field | `specs/methodology/modeling-constructs.md § Diagrams` |
| Every fenced `mermaid` block under `specs/` declares `flowchart` | `specs/methodology/modeling-constructs.md § Diagrams` |
| No bold lead-in or list item carries a number | `specs/AGENTS.md § Ordinals and Counts` |
| No file under `specs/` other than `specs/methodology/working-files.md` and `specs/AGENTS.md` names a working file | `specs/methodology/sourcing-and-citation.md § Which Citations Are Allowed` |
| Every bold span opens a line, after any list marker, quote marker and indentation, and closes on a colon inside the bold, a field, or a space and an em dash inside the bold, a bold lead-in; bold italic and underscore bold are reported wherever they appear | `specs/methodology/modeling-constructs.md § Bold Lead-ins`, `specs/methodology/modeling-constructs.md § Emphasis` |
| No line opens with italic, after any list marker, quote marker and indentation; underscore italic goes unchecked, since it cannot be told apart from an identifier such as retention_purge written outside backticks | `specs/methodology/modeling-constructs.md § Emphasis` |
| Every record citation resolves to a record section, names each of its type's identifying fields in the type's order and no other, separated by `; `, and matches exactly one record; brackets on a section that is not a record section are a malformed record citation; and an identifying value holds no `;` | `specs/methodology/sourcing-and-citation.md § Writing a Citation` |
| No heading title contains `[` | `specs/methodology/sourcing-and-citation.md § Titling a Heading` |
| Under `specs/`, an `Open Questions` section is its file's last top-level section and holds an optional `**Diagrams:**` field, then a `**Records:**` field of at least one record, one list item each, and nothing else; a blank line precedes each field; each record is its `**Name:**`, `**Open Question:**`, `**Provisional Answer:**` and `**Impacts:**` fields in that order, the later ones indented two spaces, its Impacts carrying at least one section citation, and no two records share a Name | `specs/methodology/modeling-constructs.md § Constructs § Record Form`, `specs/methodology/spec-placement.md § An Open Question` |
| Under `specs/`, every line opening with a bold phrase ending in a colon inside the bold carries a key a form declares, where that form places it | `specs/methodology/modeling-constructs.md § Fields` |

**Scope —** the files `specs/methodology/scope.md § What Spec of Record Governs` names, the working files aside: the root `AGENTS.md`, every file under `specs/`, and each skill `specs/methodology/skills.md` registers, its `SKILL.md` and its scripts. The working files legitimately carry citations to things since moved or pruned, so the Working-file form audit reads them instead, and the skills' output under `.ai/tmp/` is read by no check, being reports rather than rules; the check keeping the working files out of version control reads the project's `.gitignore`. `--candidates` lists places for the Ordinals and counts audit, the Markup audit, the Glossary terms audit, the Finished style audit and the Agent agnostic audit to read, and, for the Skill form audit, an unregistered skill whose `SKILL.md` cites the method's rules and a registered skill's script importing from outside the standard library. An audit whose unit names the script's scope for a full run uses this one. The candidates print apart from the findings, since a list of places to read decides nothing (`specs/methodology/scope.md § Rules and Skills`).

## Operating rules carried out by a step

The steps carrying out the operating rules that leave no trace in the files (`specs/methodology/scope.md § Rules and Skills`):

| Operating rule | Carried out by | A skipped step leaves |
|---|---|---|
| `specs/AGENTS.md § Writing specs`, `specs/AGENTS.md § Authoring Skills` | `specs/AGENTS.md`, whose routing table sends each task to the rule governing it and whose Writing specs section names the skills that sequence and check the work; `design-specs`, whose Workflow names the governing rule at each step | a fact placed, cited or formed against its rule, which the audit reading that rule finds |
| `specs/AGENTS.md § Design, Refactor, Refine (DRR)` | `design-specs`' Workflow, which scopes a change and takes it through the adversarial DRR, and this skill's audit once the change is applied | an applied design entry whose Status names no adversarial DRR, which Working-file form finds while the entry stands, a trace that goes when the entry is pruned; a direct edit made without the user's approval leaves nothing in the files, and the user who approves is its check |
| `specs/methodology/scope.md § Progressive Disclosure`, `specs/methodology/scope.md § The Shape of the Scope` | the Start from the entry point step of `design-specs` and of this skill; this skill's method, reading the files in full; `design-specs`' section on recall and the file, and its step deciding a fact's altitude and file | a citation naming a heading that does not exist, which the script finds; a fact given a second home, which Where a rule lives finds; a term used against its sense, which Glossary terms finds |
| `specs/methodology/sourcing-and-citation.md § One Home Per Fact` | `design-specs`' step finding the fact's existing home, and its section on searching before drafting | a fact given a second home, which Where a rule lives finds; a citation bare where it owed its application or its reason, which Whether the home holds the fact finds |
| `specs/methodology/spec-placement.md § Where a File Goes`, `specs/methodology/spec-placement.md § Naming a Capability Domain` | `design-specs`' step deciding a fact's altitude and file | a file or a domain placed against its test, which Placement finds |
| `specs/methodology/scope.md § Rules and Skills` | `design-specs`' step giving a changed rule its check | a rule section no audit names, which the script finds |
| `specs/methodology/spec-placement.md § Naming the Technical Files Behind a Capability` | `design-specs`' step deciding which spec a fact belongs to, which reads the product files naming a technical file before it is edited | a technical change breaking a promise its product file makes, which Counterpart currency finds |

## What is deliberately not audited

**Script checks were built and removed —** for the reason `specs/methodology/scope.md § Rules and Skills` gives. "Every product capability section has a `Test Scenarios` child" — "is this a capability" is a judgment the files do not encode, and most of its findings were overview or definitional headings. "Every `Given` names a role the role table defines" — the rule is real, but absence does not decide a violation: a scenario about system state has no actor, and one may name its role in the `Then`. Scenario coverage now covers both by reading.

**Migration fidelity gets no audit —** though comparing a migration's source statements against their rewritten destinations is exactly this kind of work. Migrations are rare enough that a written method would be exercised about once, and one exercise is not enough to generalize a method from. Brief it directly when a migration happens.

## Traps worth knowing

**Lineages start below the file's title —** as `specs/methodology/sourcing-and-citation.md § Writing a Citation` states. Building them from level 1 down made every same-file citation in the repo fail at once, the script's earliest defect, and it looked like a wall of broken citations rather than one bad assumption.

**Not every backtick span containing a section token is a citation —** a rule that discusses the token, or shows a forbidden heading form as an example, is the token being mentioned rather than used. Only these shapes are treated as citations:

```
§ Title
path/to/file.md § Title
§ Title [Key: value]
path/to/file.md § Title [Key: value; Key: value]
```

Everything else is left alone, and every inline span is stripped before looking for a token outside one. This skill's own documentation tripped that check on its first run, which is the most direct evidence available that the distinction is needed.

**Fenced blocks are stripped before anything is parsed —** examples inside them are illustrations, not live content, and linting them produces findings nobody can act on.

**A mermaid block does not begin with `flowchart` —** every diagram in this repo opens with a `config` frontmatter block inside the fence, so a check reading the first line fails on correct content. Match anywhere before the first node.
