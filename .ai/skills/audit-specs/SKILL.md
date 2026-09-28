---
name: audit-specs
description: Audit the project against the rules that govern it by reading it. Use when a directory's summary may have fallen behind its files, when a capability's scenarios may not cover what it promises, when a rule may be stated twice or in the wrong file, when something may cite a section for a rule that section does not state, when a number or a positional reference may be restating a list, when a diagram may no longer match what it renders, or after any change large enough that something restating it has gone stale. Reading audits, with a script that clears the mechanically decidable failures first.
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

Every audit is governed by the rules below.

**Read the files in full —** not headings, not a previous read, not recall, per `specs/methodology/scope.md § Progressive Disclosure`. The one time a directory summary was built from headings and memory, it missed the largest gap in the directory.

**Compare against the open source, not against the summary —** re-reading a summary confirms it reads well, which it always does. The defect is only visible with the source beside it.

Where an audit compares one passage against what it restates, the ways a compression goes wrong are listed in the `design-specs` skill, in its section on compression distortion. Use that taxonomy rather than restating it. It applies to Directory summary currency, to Diagram currency, and to Whether the home holds the fact wherever a citer states in its own words what it attributes. The other audits compare no two versions of one passage, and it does not reach them.

## The audits

| Audit | Enforces |
|---|---|
| Directory summary currency | `specs/methodology/sourcing-and-citation.md § Keeping Companions in Step`, `specs/methodology/spec-placement.md § Where a File Goes` |
| Companion currency | `specs/methodology/sourcing-and-citation.md § Keeping Companions in Step` |
| Scenario coverage | `specs/methodology/acceptance-scenarios.md § Acceptance Scenarios`, `specs/methodology/acceptance-scenarios.md § Deciding What to Write` |
| Where a rule lives | `specs/methodology/sourcing-and-citation.md § One Home Per Fact`, `specs/AGENTS.md § Authoring Skills` |
| Whether the home holds the fact | `specs/methodology/sourcing-and-citation.md § One Home Per Fact`, `specs/methodology/sourcing-and-citation.md § Writing a Citation` |
| Ordinals and counts | `specs/AGENTS.md § Ordinals and Counts` |
| Literal text and emphasis | `specs/methodology/modeling-constructs.md § Emphasis`, `specs/methodology/modeling-constructs.md § Literal Text` |
| Diagram currency | `specs/methodology/modeling-constructs.md § Diagrams` |

### Directory summary currency

Does a directory's own summary still describe what it contains. Separate units, because the summaries cover different ground: an `index.md` covers a directory's direct contents, and an `architecture.md` covers everything beneath the directory that owns it. Read the tree once, then check the blueprint against all of it and each `index.md` row against its own file.

For the blueprint, both directions: a claim it makes that its detail files no longer support, and, the one usually missed, a fact those files establish that a reader of the blueprint alone would never learn. The test for that omission is not "is it stated somewhere else" but "would a reader of this file alone form a false impression, or find a later section unfollowable."

### Companion currency

Does a product fact and its technical mechanism still name each other and still describe one system. Take each product file's `technical-specs` frontmatter as the map and read both sides. Then sweep the other way: every product section a technical file cites should appear in that product file's own list, since a missing frontmatter entry is the likelier failure and the frontmatter map cannot see it.

Sweep the same pairing once more, for the converse: an entry naming a technical file that cites nothing in that product file back. This one is a judgment rather than an arithmetic check, which is why it is easy to skip. `specs/methodology/spec-placement.md § Naming the Technical Files Behind a Capability` requires the entry and the citation to stay in place together where a technical file was written to fulfill a capability, and separately scopes the list to what is needed to understand how that capability is built — a wider set. So an entry with no citation back is one of these things, and reading decides which: a file supplying context a capability depends on without implementing a promise of its own, which is correct and stays, or a missing citation on the technical side, which is the finding. What settles it is whether that technical file makes any promise this product file states. If it does and says so nowhere, the citation is missing; if it holds a schema or a boundary the capability rests on and claims none of its capability, the entry is a reading aid and correct.

The failure is not overlap, which is intended and explained at `specs/methodology/spec-placement.md § Product or Technical`. It is a side that has stopped doing its own job: a product spec specifying mechanism, or a technical spec promising something it does not implement.

### Scenario coverage

First, does each capability section have a `Test Scenarios` block at all. A section with none is the finding, and no coverage check reaches it.

Then, for those that have one: does it cover every promise and guardrail that section's own prose states, and does any scenario assert a case the prose does not.

### Where a rule lives

One pass per unit, asking these questions of every normative statement: is this file the most specific home for this rule, or does a narrower file already own its subject; and does this rule already have a home elsewhere, in the unit or in the rule homes, `specs/AGENTS.md` and `specs/methodology/`. One question catches a rule in the wrong file, the other catches it in two. Both need the same sweep, so they are one audit. A pass over `.ai/skills/` asks only whether a skill restates a rule from the rule homes, per `specs/AGENTS.md § Authoring Skills`. Naming a construct is not restating a rule; reaching into the methodology for its own claims is, per `specs/methodology/sourcing-and-citation.md § Which Citations Are Allowed`.

Inventory first, then compare. Collect every normative statement in the unit, and in the rule homes, before judging any of them — whether a rule already has a home cannot be answered about the first file until the last one has been read, and a pass that judges as it goes degrades into sampling.

Inventory within a file and within a section too, not only across files. A duplicate inside one section is the one this audit reliably misses, because the two copies are read as one passage in one sitting and a passage does not feel like it disagrees with itself. The shape to watch for is a rule stated once in a table and again in the prose around it: the table row is the enumeration, the paragraph restates it while adding something real, and the restatement is invisible because it arrives as continuation rather than repetition. Counting sites is what catches it — a rule found in two files is often in three.

One signal is worth naming, because it looks like the opposite of a defect: a passage that cites another file's rule and then extends it. A citation followed by application is correct. A citation followed by further rules about the cited subject is a second home with a citation attached, reading as deference precisely because the citation is there.

Product and technical are never compared with each other, for the reason `specs/methodology/spec-placement.md § Product or Technical` gives.

**An `architecture.md` restates its own directory by design, and those restatements are not findings —** this is a false-positive trap the audit sets, and it is expensive: an overview names every major piece in its own words rather than leaning on citations to carry its meaning, per `specs/methodology/spec-placement.md § Index, Architecture, Detail`, so it restates constantly and by instruction. `specs/methodology/sourcing-and-citation.md § Keeping Companions in Step` is what resolves it — a rendering is not a second home. A diagram, wherever it sits, is a rendering too. An auditor who has not read that sentence finds the overview restating half the directory and reports it as the most drifted file present, confidently and at length. What is still a finding is an `architecture.md` duplicating *itself*, or restating anything from outside its own directory, which no rule licenses, and which is easy to miss while discounting everything else it restates.

Where a duplicate is real, choose the home by `specs/methodology/sourcing-and-citation.md § One Home Per Fact`'s test and replace the others with citations. Where `specs/methodology/sourcing-and-citation.md § Which Citations Are Allowed` forbids that citation, as for an application spec restating a methodology rule, the restatement is cut back to the spec's own content instead. Where several files use a rule and none owns it, hoist to the narrowest location covering every use and no further. Hoisting too high is not illegal, but it overstates how far the rule reaches. Name which usages forced the height; a home no usage forces is too high.

### Whether the home holds the fact

One home per fact means everywhere else cites that home instead of restating it. What nothing checks is the other half of that bargain: that the home still states the fact being attributed to it. A citer says "X is governed there"; the audit asks whether *X* is actually there.

This is the audit that catches the most and is the easiest to leave out, because every symptom of it looks fine. The heading resolves, so the script clears it. The citer reads as correct, because it says what it means. The target reads as correct, because a section is not obviously missing a sentence. The defect exists only in the gap between two files that are each individually clean, and the citation being valid is precisely what hides it.

Sweep by target, not by citer. Take a section that is cited from several places, gather every citation into it at once, and write down what each citer attributes to it before opening it. Then read the target and check each attribution off. Doing it citer-by-citer is what fails: one file attributing something absent looks like that file's own imprecision, and it takes the second citer to reveal that the target is what is thin.

Each shape below is a finding, fixed on the side that is wrong rather than by weakening the citation:

- **The target never states the rule —** a capability file cites a guarantees section as holding a ceiling on what it may display; that section's prose never mentions the ceiling, only its scenarios imply it. The prose is what is missing.
- **The target states it differently, and the citer is right —** a second file cites the same section while stating the rule in its correct, narrower form. When a citer is more accurate than the home it cites, the home is what is stale, and the citer's wording is the best available evidence of what the rule should say.
- **A stage's own fact has no home anywhere —** the mechanism is specified on the technical side, the scenario asserts it, every file assumes it, and no product section states it. This surfaces here rather than under Scenario coverage, because what reveals it is a citation looking for a fact rather than a scenario looking for prose.

A target that never states the rule and a target that states it differently are the ordinary cases and both were found in this repo on the first run of it. Note what they share: a heavily-cited section accumulates attributions faster than it is re-read, so the most-cited section in a directory is where to start, not where to stop.

Same-layer citations count. Companion currency covers product against technical; this audit covers every direction a citation is allowed to point, and product-to-product is where both real cases were found.

**After a change lands, the target set is not a judgment call —** every section whose meaning the change altered is a mandatory target, because a citation written against the old meaning is still a valid citation and nothing else will surface it. Choosing targets by how heavily cited they are is the rule for an audit run on a tree nobody just edited; run after a change, this audit starts from the sections that changed and sweeps outward from each.

**Sweep twice, by citation and by wording, because they find different things —** a citation sweep finds citers. It does not find a passage that restates the fact without citing it, and those are common in exactly the places that are supposed to track a change: a diagram, an `architecture.md`'s prose, a table row rendering a rule stated elsewhere. Take the fact's own distinctive phrasing and grep for it across the tree as a second pass.

The evidence for needing both is one pass in this repo where a change widened a guarantee's condition. The citation sweep checked every citer of the amended section and every attribution held — a clean result, correctly reported. Further copies of the superseded wording survived anyway, neither of them citing anything: one in a paragraph restating the guarantee, one in a diagram node whose own source table said it was "kept in sync with these tables whenever they change." Both were found by grepping the old phrasing. A sweep that had run only by citation would have closed the audit and left both.

### Ordinals and counts

Does any number break `specs/AGENTS.md § Ordinals and Counts`. Run the script with `--candidates`, then read the files in scope in full, using the candidates as a guide to where numbers are likely rather than as the boundary of the search. Judge every number against the rule as written: a violation gets a proposed rewrite, and a decline names the rule's reason for keeping the number. A violation the patterns missed is reported like any other, and its phrasing is a candidate for a new pattern.

### Literal text and emphasis

Does every backtick span hold text written exactly so elsewhere, and does every italic span stress a word or a short phrase whose stress changes what its sentence means. The script checks only where bold and italic may appear; this is the judgment it cannot make. Run it with `--candidates`, which lists each backtick span holding a capital letter and no punctuation that matches no heading, field key, or text a fenced example in the tree holds, and each italic span of more than a few words, then read the files in scope in full, using the candidates as a guide rather than as the boundary. A name in backticks is written plain; an italic span stressing nothing loses its italic, and one carrying a point that needs more is given the structure `specs/methodology/modeling-constructs.md § Emphasis` names.

### Diagram currency

Run only once the script's diagram check passes; if it fails, the work is fixing the citations, and there is nothing yet to compare. Then render the diagram through `.ai/skills/author-mermaid-diagram/`, read every section its Sources list names, and check that the picture says nothing its sources do not, that every label is one its host file names, and that the list names the home of everything drawn, each as specific as the rule asks and none a summary. A source the current change edited is where to look first. A picture saying something its sources do not takes the report row for a summary that disagrees with what it summarizes; a source missing from the list, or a listed section that is only a summary of the home or broader than the rule asks, takes the row for a required thing that is absent or sits on the wrong side.

## The report

A run states the unit it covered and a verdict on it: current, current with named fixes, or drifted. Findings are rows in one of the shapes below, depending on what kind of defect it is.

| Defect | Row |
|---|---|
| A summary disagrees with what it summarizes | the file, the claim, the source, and which compression distortion it is |
| A required thing is absent, or sits on the wrong side | the location, the rule it breaks, and what is missing or misplaced |
| A rule has two homes | both statements, the home chosen, and, where it was hoisted, the usages that forced its height |

A report also carries what was examined and declined: the candidate that had the shape of a defect and turned out not to be one, with the reason it failed the test. This is not padding and not optional. An audit's expensive half is arriving at the judgment that something suspicious is correct, and a report that keeps only the findings throws that half away, so the next run pays for it again and may reach the opposite answer. Declining a candidate in writing is also what makes an over-eager audit reviewable: a reader can check a rejection as easily as a finding.

Output goes to `.ai/tmp/audit-specs/`, one file per run named for the unit and the date. A run clears any earlier report for the same unit, the stale output `specs/AGENTS.md § Authoring Skills` has a skill clean.

A finding becomes a design entry (`specs/methodology/working-files.md § A Design Entry`) rather than an edit, and that entry goes through `specs/AGENTS.md § Design, Refactor, Refine (DRR)` before anything lands. A finding small enough to qualify may instead be applied directly, per that section.

## Running one

`specs/AGENTS.md § Design, Refactor, Refine (DRR)` covers briefing a reader, verifying findings before acting on them, and not auditing your own work. All of it applies.

What is worth adding is what auditing your own work costs here: a confident sweep that misses the section its author forgot existed, for the reason that section gives. Where you wrote the content, delegate the audit.

## Scoping a run

| Audit | Unit |
|---|---|
| Directory summary currency | the tree rooted at a directory owning an `architecture.md`, plus each `index.md` beneath it |
| Companion currency | per product file |
| Scenario coverage | per product file |
| Where a rule lives | per unit: `AGENTS.md`, `specs/AGENTS.md`, `specs/methodology/`, `specs/application/product/`, `specs/application/technical/`, `.ai/skills/` |
| Whether the home holds the fact | per cited section, taking every citation into it in one pass |
| Ordinals and counts | the files a change touched, or everything in the script's scope for a full run |
| Literal text and emphasis | the files a change touched, or everything in the script's scope for a full run |
| Diagram currency | per diagram, with every section its Sources list names |

`specs/index.md` and `specs/application/index.md` sit above every architecture-rooted tree, so a directory summary run names them explicitly or nothing covers them.

`specs/methodology/` is audited by the rules it states, minus those that do not reach it at all, per `specs/methodology/scope.md § The Methodology Governs Itself`: it owes no acceptance scenarios and carries no `technical-specs` frontmatter. Scenario coverage also reaches no technical file.

## What the script checks

| Check | Rule |
|---|---|
| Every `file § A § B` resolves to that heading path in that file | `specs/methodology/sourcing-and-citation.md § Writing a Citation` |
| A citation never points down a layer except from `specs/AGENTS.md`, never crosses between application and methodology or from an application spec to `specs/AGENTS.md`, whether it names a section or a whole file, and no spec cites a section of the project's root `AGENTS.md` | `specs/methodology/sourcing-and-citation.md § Which Citations Are Allowed` |
| No citation targets an `index.md` | `specs/methodology/sourcing-and-citation.md § Writing a Citation` |
| A cross-file citation carries a project-root path | `specs/methodology/sourcing-and-citation.md § Writing a Citation` |
| Every section token sits inside a backtick span | `specs/methodology/sourcing-and-citation.md § Writing a Citation` |
| A heading carries no ordinal, no section token, and is unique among its siblings | `specs/methodology/sourcing-and-citation.md § Titling a Heading` |
| A `Test Scenarios` section sits one level below its capability and holds a `gherkin` fence | `specs/methodology/acceptance-scenarios.md § Acceptance Scenarios` |
| Every `gherkin` block parses: each `Scenario:` followed by at least one `Given`, `When`, and `Then` | `specs/methodology/acceptance-scenarios.md § Acceptance Scenarios` |
| Every `technical-specs` list is alphabetically sorted, appears only in a product file, and every path in it resolves under the technical directory | `specs/methodology/spec-placement.md § Naming the Technical Files Behind a Capability` |
| Every directory under `specs/` has an `index.md`, naming each file and subdirectory it holds, each row naming one that exists | `specs/methodology/spec-placement.md § Where a File Goes` |
| The script's scope is read from `specs/methodology/skills.md` and the files `specs/methodology/scope.md § What Spec of Record Governs` names; a missing or empty registry is a finding, never an empty scope | `specs/methodology/scope.md § What Spec of Record Governs` |
| The tree in `specs/methodology/scope.md § The Shape of the Scope` names exactly the files in `specs/methodology/`, and every path it names exists | `specs/methodology/scope.md § The Shape of the Scope` |
| The kinds in `specs/methodology/scope.md § What Spec of Record Governs` are the ones the script reads, and each home the table names exists | `specs/methodology/scope.md § What Spec of Record Governs` |
| Every row of the registry in `specs/methodology/skills.md` names a skill in backticks with a directory under `.ai/skills/` | `specs/methodology/skills.md § Registered Skills` |
| Every registered skill's `SKILL.md` opens with YAML front matter whose `name` is its directory's name, in kebab-case, and whose `description` is present; a `scripts/` directory beside it, where it has one, holds an entry-point script named for the skill | `specs/AGENTS.md § Authoring Skills` |
| Every diagram in `specs/` sits directly under a heading of its own whose section holds, in this order and nothing else, the diagram, a single `**Caption:**` paragraph citing no section and no file, and a `**Sources:**` line followed by one citation per bullet, sorted, each resolving to a section or a record other than the diagram's own; and every listed section carries a citation of that diagram's heading in its own text, or, for a record section or a record, in that record section's `**Diagrams:**` field | `specs/methodology/modeling-constructs.md § Diagrams` |
| Every fenced `mermaid` block declares `flowchart` | `specs/methodology/modeling-constructs.md § Diagrams` |
| No bold lead-in or list item carries a number | `specs/AGENTS.md § Ordinals and Counts` |
| No file under `specs/` other than `specs/methodology/working-files.md` names a working file | `specs/methodology/sourcing-and-citation.md § Which Citations Are Allowed` |
| Every bold span opens a line, after any list marker, quote marker and indentation, and closes on a colon inside the bold, a field, or a space and an em dash inside the bold, a bold lead-in; bold italic and underscore bold are reported wherever they appear | `specs/methodology/modeling-constructs.md § Bold Lead-ins`, `specs/methodology/modeling-constructs.md § Emphasis` |
| No line opens with italic, after any list marker, quote marker and indentation; underscore italic goes unchecked, since it cannot be told apart from an identifier such as retention_purge written outside backticks | `specs/methodology/modeling-constructs.md § Emphasis` |
| Every record citation resolves to a record section, names each of its type's identifying fields in the type's order and no other, separated by `; `, and matches exactly one record; brackets on a section that is not a record section are a malformed record citation; and an identifying value holds no `;` | `specs/methodology/sourcing-and-citation.md § Writing a Citation` |
| No heading title contains `[` | `specs/methodology/sourcing-and-citation.md § Titling a Heading` |
| Under `specs/`, an `Open Questions` section is its file's last top-level section and holds an optional `**Diagrams:**` field, then a `**Records:**` field of at least one record, one list item each, and nothing else; a blank line precedes each field; each record is its `**Name:**`, `**Open Question:**`, `**Provisional Answer:**` and `**Impacts:**` fields in that order, the later ones indented two spaces, its Impacts carrying at least one section citation, and no two records share a Name | `specs/methodology/modeling-constructs.md § Constructs § Record Form`, `specs/methodology/spec-placement.md § An Open Question` |
| Under `specs/`, every line opening with a bold phrase ending in a colon inside the bold carries a key a form declares, where that form places it | `specs/methodology/modeling-constructs.md § Fields` |

**Scope —** the files `specs/methodology/scope.md § What Spec of Record Governs` names, the working files aside: the root `AGENTS.md`, every file under `specs/`, and each skill `specs/methodology/skills.md` registers, its `SKILL.md` and its scripts. The working files legitimately carry citations to things since moved or pruned: `.ai/designs.md` and `.ai/follow-ups.md` are reached once their forms are record forms, and the skills' output under `.ai/tmp/` stays outside the checks, being reports rather than rules. `--candidates` lists places for the Ordinals and counts audit and the Literal text and emphasis audit to read, and, for a reader to judge, an unregistered skill whose `SKILL.md` cites the method's rules and a registered skill's script importing from outside the standard library. The audits above set their own scope, except Ordinals and counts, which uses this one.

## What is deliberately not audited

**Nothing the script cannot decide moves into the script —** now or later. Listing candidates for a reading audit is not deciding: `--candidates` reports places to read, never a finding or a clear, and its output is kept apart from the findings for that reason. One claiming to judge whether a compression stayed faithful would produce a confident false clear over the findings that cost the most. What is possible later is more mechanical checks and more audits, never the conversion of one into the other.

**Script checks were built and removed —** because a check that cannot decide is worse than no check. "Every product capability section has a `Test Scenarios` child" — "is this a capability" is a judgment the files do not encode, and most of its findings were overview or definitional headings. "Every `Given` names a role the role table defines" — the rule is real, but absence does not decide a violation: a scenario about system state has no actor, and one may name its role in the `Then`. Scenario coverage now covers both by reading.

**Drafting residue gets no audit of its own —** the `design-specs` skill applies `specs/methodology/spec-style.md` at authoring time.

**File placement and altitude get no audit —** whether a file sits at the right altitude, whether a domain earned its subfolder, whether an overview has accumulated detail that belongs in a detail file: all real, all governed by `specs/methodology/spec-placement.md § Index, Architecture, Detail` and `specs/methodology/spec-placement.md § Where a File Goes`, and none of it checked here. Directory summary currency reaches the case where an overview has thinned into pointers, because that shows up as a fact its reader cannot learn. It does not reach the opposite case, an overview that has accumulated full detail. That gap is known and accepted rather than overlooked.

**Migration fidelity gets no audit —** though comparing a migration's source statements against their rewritten destinations is exactly this kind of work. Migrations are rare enough that a written method would be exercised about once, and one exercise is not enough to generalize a method from. Brief it directly when a migration happens.

## Traps worth knowing

**A level-1 heading is the file's title, not a section —** a lineage starts below it, which is why a citation naming a top-level section resolves in a file whose first line is a title. Building lineages from level 1 down makes every same-file citation in the repo fail at once; that was the script's earliest defect, and it looked like a wall of broken citations rather than one bad assumption.

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
