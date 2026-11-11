---
name: audit-specs
description: Audit the project against the rules that govern it by reading it. Use when a directory's summary may have fallen behind its files, when a capability's scenarios may not cover what it promises, when a rule may be stated twice or in the wrong file, when a citation may name a section that does not state the rule, when a number or a position may restate a list, when text may point at other text by direction, when a term may stray from the glossary, when a diagram may no longer match what it renders, when prose may hold what a construct should, when a file may sit in the wrong place, when drafting residue or prose needing a second read may remain, when an instruction may assume a particular agent, when a skill or a working file's entry may have lost its form, when a rule may have no check, or after any change large enough that something restating it has gone stale. Reading audits, with a script that clears the mechanically decidable failures first.
---

# Auditing the specifications

The methodology and `specs/AGENTS.md` govern the files in Spec of Record's scope, as `specs/methodology/scope.md § What Spec of Record Governs` sets. This skill reads no code. Checking that those rules held splits into separate jobs.

A script decides whether a citation resolves, whether a front matter list is sorted and whether a fenced block is well-formed. Everything that has gone wrong here was a statement that resolved perfectly and was wrong anyway. A blueprint omitting the security control its own directory calls primary passes every mechanical check ever written.

The audits are the substance. The script is a pre-pass.

    python .ai/skills/audit-specs/scripts/audit-specs.py --check-scope                 # from the repo root
    python .ai/skills/audit-specs/scripts/audit-specs.py --check-scope --root <path>   # an explicit root
    python .ai/skills/audit-specs/scripts/audit-specs.py --list-candidates             # places for the reading audits that use them
    python .ai/skills/audit-specs/scripts/audit-specs.py --list-candidates --detail    # every Clear Prose candidate, not only their count for each file
    python .ai/skills/audit-specs/scripts/audit-specs.py --check-layout .ai/follow-ups.md  # the checks of a block of fields and of a blank line, for the Working-file form audit

Run the script first, because it is fast and because its findings would otherwise be noise in a reading pass.

## These audits assume an agent

Each audit requires a judgment the files do not encode, often across a whole directory held in mind at once. A script cannot judge whether a summary is still true. A person can, but a person does it by sampling, with attention that degrades across a long directory. Reading a whole unit in one pass and holding it together is what makes a method this exhaustive worth writing down rather than aspiring to.

## Workflow

A run follows this Workflow's steps, and each audit follows the ones it needs.

**Start from the entry point.** Read `specs/AGENTS.md`, then `specs/methodology/glossary.md`, and a directory's `index.md` before working in the directory, as `specs/methodology/scope.md § Progressive Disclosure` and `specs/methodology/scope.md § The Shape of the Scope` have it.

**Fork on the kind of specification.** Every file audited is of a kind of change, the working files aside, which are of no kind (`specs/methodology/working-files/main.md § The Working Files`) and are written `none` (`specs/methodology/design-workflow.md § A Design's Reviews`). Each audit's Kind column names the kinds of file the audit reads. `.ai/skills/audit-specs/references/canon-specs.md` holds the audits written for the canon, and `.ai/skills/audit-specs/references/app-specs.md` those written for the application specs. A run given `--kind` names one or more of the kinds `specs/methodology/working-files/main.md § A Design Document § The Kinds of Change` defines. A run picks its audits, and the files each audit reads of its unit, as `specs/methodology/design-workflow.md § A Design's Reviews` has it. `--kind` is the skill's argument, never the script's, and the script's pre-pass runs whole whatever the kinds. A run names no design, as `specs/AGENTS.md § Design, Refactor, Refine § An Audit` has an audit.

**Read the files in full.** Read the files themselves: not their headings, not a previous read, not recall, as `specs/methodology/scope.md § Progressive Disclosure` has it. The one time a directory summary was built from headings and memory, the summary missed the largest gap in the directory.

**Compare against the open source, not against the summary.** Re-reading a summary confirms that the summary reads well, and a summary always does. The defect is visible only with the source beside it.

Where an audit compares one passage against what the passage restates, the `design-specs` skill lists the ways a compression goes wrong, in its section on compression distortion. Use that taxonomy rather than restating it. The taxonomy applies to Directory summary currency and to Diagram currency. It also applies to Whether the home holds the fact, wherever a citer states in its own words what it attributes. The other audits compare no two versions of one passage, and the taxonomy does not reach them.

## The audits

**Reference Key:** Audit \
**Required:** Kind, Enforces

| Audit | Kind | Enforces |
|---|---|---|
| Directory summary currency | `canon-specs`, `application-specs` | `specs/methodology/sourcing-and-citation.md § Keeping Specs in Sync § Materialized Views`, `specs/methodology/spec-placement.md § Index, Architecture, Detail`, `specs/methodology/spec-placement.md § What an Overview Describes`, `specs/methodology/scope.md § The Shape of the Scope` |
| Counterpart currency | `application-specs` | `specs/methodology/sourcing-and-citation.md § Keeping Specs in Sync § Product and Technical Counterparts`, `specs/methodology/spec-placement.md § Product or Technical`, `specs/methodology/spec-placement.md § Naming the Technical Files Behind a Capability` |
| Scenario coverage | `application-specs` | `specs/methodology/acceptance-scenarios.md § Acceptance Scenarios`, `specs/methodology/acceptance-scenarios.md § Deciding What to Write`, `specs/methodology/acceptance-scenarios.md § Keeping a Scenario and Its Prose in Sync` |
| Where a rule lives | `canon-specs`, `application-specs`, `other` | `specs/methodology/sourcing-and-citation.md § One Home Per Fact`, `specs/methodology/sourcing-and-citation.md § A Definition and Its Instances`, `specs/methodology/sourcing-and-citation.md § Keeping Specs in Sync § Materialized Views`, `specs/methodology/sourcing-and-citation.md § Which Citations Are Allowed`, `specs/methodology/sourcing-and-citation.md § External Reference`, `specs/methodology/external-references.md § External References`, `specs/methodology/scope.md § What Spec of Record Governs`, `specs/methodology/scope.md § The Methodology Governs Itself` |
| Whether the home holds the fact | `canon-specs`, `application-specs` | `specs/methodology/sourcing-and-citation.md § One Home Per Fact`, `specs/methodology/sourcing-and-citation.md § Writing a Citation` |
| Ordinals and counts | `canon-specs`, `application-specs`, `documentation` | `specs/methodology/spec-style.md § Ordinals and Counts`, `specs/methodology/sourcing-and-citation.md § Writing a Citation § Referring to Other Text` |
| Markup | `canon-specs`, `application-specs`, `documentation`, `other` | `specs/methodology/modeling-constructs.md § Fields`, `specs/methodology/spec-style.md § Markdown`, `specs/methodology/spec-style.md § Blank Lines`, `specs/methodology/spec-style.md § Bold Lead-ins`, `specs/methodology/spec-style.md § Emphasis`, `specs/methodology/spec-style.md § Literal Text`, `specs/methodology/sourcing-and-citation.md § Titling a Heading` |
| Glossary terms | `canon-specs`, `application-specs`, `documentation` | `specs/methodology/glossary.md § Glossary`, `specs/methodology/glossary.md § Writing an Entry`, `specs/methodology/glossary.md § Using an Abbreviation` |
| Construct choice and form | `canon-specs`, `application-specs` | `specs/methodology/modeling-constructs.md § Purpose`, `specs/methodology/modeling-constructs.md § Defining Constructs`, `specs/methodology/modeling-constructs.md § Constructs`, `specs/methodology/modeling-constructs.md § Time`, `specs/methodology/modeling-constructs.md § When to Use Which`, `specs/methodology/expressions.md § Expressions`, `specs/methodology/expressions.md § Expressions § FEEL`, `specs/methodology/acceptance-scenarios.md § Why a Scenario Is Not a Modeling Construct`, `specs/methodology/checks.md § Check`, `specs/methodology/checks.md § Script Check`, `specs/methodology/checks.md § Semantic Check` |
| Placement | `canon-specs`, `application-specs` | `specs/methodology/spec-placement.md § Where a File Goes`, `specs/methodology/scope.md § Progressive Disclosure`, `specs/methodology/spec-placement.md § Naming a Capability Domain`, `specs/methodology/spec-placement.md § The Technical Stack`, `specs/methodology/spec-placement.md § Environments`, `specs/methodology/spec-placement.md § Open Question` |
| Finished style | `canon-specs`, `application-specs`, `documentation`, `other` | `specs/methodology/spec-style.md § What a Finished Spec Reads Like`, `specs/methodology/spec-style.md § Trade-offs Are Not Journey Language`, `specs/methodology/spec-style.md § Clear Prose`, `specs/methodology/sourcing-and-citation.md § Writing a Citation` |
| Agent agnostic | `canon-specs`, `other` | `specs/methodology/scope.md § Agent Agnostic` |
| Skill form | `canon-specs` | `specs/methodology/skills.md § Authoring a Skill`, `specs/methodology/sourcing-and-citation.md § Writing a Citation § Citing From Code`, `specs/methodology/scope.md § Rules and Skills`, `specs/methodology/skills.md § Registered Skills`, `specs/methodology/working-files/main.md § The Working Files`, `specs/methodology/checks.md § Check`, `specs/methodology/checks.md § The Areas of Checking` |
| Working-file form | `none` | `specs/methodology/working-files/main.md § The Working Files`, `specs/methodology/working-files/main.md § A Follow-up`, `specs/methodology/modeling-constructs.md § Fields`, `specs/methodology/spec-style.md § Markdown`, `specs/methodology/spec-style.md § Blank Lines` |
| Diagram currency | `canon-specs`, `application-specs` | `specs/methodology/modeling-constructs.md § Diagrams`, `specs/methodology/sourcing-and-citation.md § Keeping Specs in Sync § Materialized Views` |
| Principles held | `canon-specs`, `application-specs` | `specs/AGENTS.md § Constitutional Principles` |

Each audit reads its unit against every rule that the sections in its Enforces column state, or against the part of a section that the audit's text names (`specs/methodology/scope.md § Rules and Skills`). What an audit's own text adds is how to read, what is easy to miss, and how a finding is fixed (`specs/methodology/skills.md § Authoring a Skill`).

### Directory summary currency

The summaries are separate units, because they cover different ground. An `index.md` covers a directory's direct contents. An `architecture.md` covers everything beneath the directory that owns it, and what the directory's overview describes beyond the directory, code aside. Read the tree once. Then check the blueprint against all of the tree, and each `index.md` row against its own file. Of `specs/methodology/sourcing-and-citation.md § Keeping Specs in Sync § Materialized Views`, this audit reads the paragraph on a directory's `architecture.md`.

The finding usually missed in a blueprint is an omission: a fact its detail files establish that a reader of the blueprint alone would never learn. The test for it is not "is it stated somewhere else" but "would a reader of this file alone form a false impression, or find a later section unfollowable."

### Where a rule lives

Make one pass per unit, over every normative statement in the unit. Read each statement against the unit and against the files that state the rules, `specs/AGENTS.md` and `specs/methodology/`. A rule in the wrong file and a rule in two files need the same sweep, so they are one audit. Of `specs/methodology/sourcing-and-citation.md § Keeping Specs in Sync § Materialized Views`, this audit reads the statement that a view is never a second home.

Inventory first, then compare. Collect every normative statement in the unit, and in the files that state the rules, before judging any of them. Whether a rule already has a home cannot be answered about the first file until the last file has been read. A pass that judges as it goes degrades into sampling.

Inventory within a file and within a section too, not only across files. A duplicate inside one section is the one this audit reliably misses, because the two copies are read as one passage in one sitting, and a passage does not feel like it disagrees with itself. The shape to watch for is a rule stated once in a table and again in the prose around it. The table row is the enumeration, and the paragraph restates the rule while adding something real. The restatement is invisible because it arrives as continuation rather than repetition. Counting sites is what catches it: a rule found in two files is often in three.

One signal is worth naming, because it looks like the opposite of a defect: a passage that cites another file's rule and then adds more than `specs/methodology/sourcing-and-citation.md § One Home Per Fact` lets a citing place add. The extension reads as deference because the citation is there. The citation's absence reads as nothing at all: a passage that builds on another file's rule, or directs work under it, with nothing naming the rule's home. Of that section, the bare citation owing its application or its reason is Whether the home holds the fact's to find. This audit reads the rest.

**Several rules in one sentence.** Read each sentence stating a rule at a rule's home for one holding more than one rule (`specs/methodology/sourcing-and-citation.md § One Home Per Fact § One Rule to a Sentence`). Report such a sentence with each rule it holds, named by the question it answers.

**An outside standard is a fact whose home is its record.** A registered standard's version or link, stated anywhere but the standard's record in `specs/methodology/external-references.md § External References`, is a second home. A section whose rule adopts or maps onto a registered standard without citing the standard's record is a passage with nothing naming the home (`specs/methodology/sourcing-and-citation.md § External Reference`). Read the register too. Look for a standard the canon relies on and does not register, or registers though `specs/methodology/sourcing-and-citation.md § External Reference` would not. Look also for a record whose URL does not reach the version or revision it names, where the agent can fetch the URL. Look for a form the canon invents where a registered or a published standard fits, as `specs/methodology/sourcing-and-citation.md § External Reference § Which Form a Need Takes` would have it take the standard's; a departure from a standard the canon adopts or maps onto with no row of its mapping; a record whose Access its URL contradicts; and a paid standard whose meaning the canon relies on without stating it in its own words.

Product and technical are never compared with each other, for the reason `specs/methodology/spec-placement.md § Product or Technical` gives.

**An `architecture.md` restates its own directory by design, and those restatements are not findings.** This is a false-positive trap the audit sets, and an expensive one. An overview restates constantly and by instruction (`specs/methodology/spec-placement.md § Index, Architecture, Detail`). Neither an overview nor a diagram is a second home (`specs/methodology/sourcing-and-citation.md § Keeping Specs in Sync § Materialized Views`). An auditor who has not read those sections finds the overview restating half the directory, and reports it as the most drifted file present, confidently and at length. Some restatements stay findings, and are easy to miss while discounting everything else the overview restates: an `architecture.md` duplicating *itself*, or restating what lives outside both its own tree and what `specs/methodology/spec-placement.md § What an Overview Describes` names for it.

Where a duplicate is real, choose the home by `specs/methodology/sourcing-and-citation.md § One Home Per Fact`'s test, placing a rule several places use as that section says. Replace the other copies with citations. Where `specs/methodology/sourcing-and-citation.md § Which Citations Are Allowed` forbids that citation, as it does for an application spec restating a methodology rule, the restatement is cut back to the spec's own content instead.

### Whether the home holds the fact

What nothing else checks is that a cited home still states the fact attributed to it, as `specs/methodology/sourcing-and-citation.md § Writing a Citation` requires. A citer says "X is governed there". The audit asks whether *X* is there. Of that section, `specs/methodology/sourcing-and-citation.md § Writing a Citation § Referring to Other Text` is Ordinals and counts' to read, and the paragraph on where a citation sits is Finished style's. This audit reads the rest.

This is the audit that catches the most and is the easiest to leave out, because every symptom of it looks fine. The heading resolves, so the script clears it. The citer reads as correct, because it says what it means. The target reads as correct, because a section is not obviously missing a sentence. The defect exists only in the gap between two files that are each clean on their own. The citation's validity is what hides it.

Sweep by target, not by citer. Take a section that is cited from several places, and gather every citation into it at once. Before opening the section, write down what each citer attributes to it. Then read the target and check each attribution off. Sweeping citer by citer is what fails. One file attributing something absent looks like that file's own imprecision, and it takes the second citer to reveal that the target is what is thin.

**A bare citation that needed more.** With every citer of a section gathered, read each citer as an agent reading only that place would. Read it against the sentences of `specs/methodology/sourcing-and-citation.md § One Home Per Fact` on when a citing place states a rule's application and its reason, and on when a bare citation is enough. Those sentences are the one part of that section this audit reads. A citation that only routes or lists, such as a routing row, a Sources bullet or a `technical-specs` entry, applies no rule, and bare is enough there. An audit's Enforces cell is the citation the audit runs from, not one of these. A bare citation reads as correct because nothing in it is wrong. That is why it is missed.

Each shape this audit names is a finding, fixed on the side that is wrong rather than by weakening the citation:
- **The target never states the rule.** A capability file cites a guarantees section as holding a ceiling on what it may display. That section's prose never mentions the ceiling, and only the section's scenarios imply it. The prose is what is missing.
- **The target states it differently, and the citer is right.** A second file cites the same section while stating the rule in its correct, narrower form. When a citer is more accurate than the home it cites, the home is what is stale. The citer's wording is then the best available evidence of what the rule should say. Once the home holds the rule, the citer's restatement gives way to its citation.
- **A stage's own fact has no home anywhere.** The mechanism is specified on the technical side, the scenario asserts it, every file assumes it, and no product section states it. This finding surfaces here rather than under Scenario coverage, because what reveals it is a citation looking for a fact rather than a scenario looking for prose.

A target that never states the rule and a target that states it differently are the ordinary cases. Both were found in this repo on this audit's first run. Note what they share: a heavily-cited section accumulates attributions faster than it is re-read, so the most-cited section in a directory is where to start, not where to stop.

Same-layer citations count. Counterpart currency covers product against technical. This audit covers every direction a citation is allowed to point, and product-to-product is where both real cases were found.

**Where the files hold uncommitted changes, the target set is not a judgment call.** Every section whose meaning those changes altered, read in the diff against the last commit, is a mandatory target, because a citation written against the old meaning is still a valid citation, and nothing else will surface it. On a tree with no uncommitted change, targets are chosen by how heavily cited they are. On a tree holding one, this audit starts from the sections that changed and sweeps outward from each.

**Sweep twice, by citation and by wording, because they find different things.** A citation sweep finds citers. It does not find a passage that restates the fact without citing it. Such passages are common in the places that are supposed to track a change: a diagram, an `architecture.md`'s prose, a table row rendering a rule stated elsewhere. For the wording pass, take the fact's own distinctive phrasing and grep for it across the tree.

The evidence for needing both is one pass in this repo where a change widened a guarantee's condition. The citation sweep checked every citer of the amended section, and every attribution held: a clean result, correctly reported. Further copies of the superseded wording survived anyway, and neither of them cited anything. One was in a paragraph restating the guarantee. The other was in a diagram node whose own source table said it was "kept in sync with these tables whenever they change." Both were found by grepping the old phrasing. A sweep that had run only by citation would have closed the audit and left both.

### Ordinals and counts

Run the script with `--list-candidates`. Then read the files in scope in full, using the candidates as a guide to where numbers and directions are likely rather than as the boundary of the search. Judge every number against `specs/methodology/spec-style.md § Ordinals and Counts` as written. A violation gets a proposed rewrite, and a decline names that section's reason for keeping the number. Judge every reference to other text against `specs/methodology/sourcing-and-citation.md § Writing a Citation § Referring to Other Text`, the one part of `specs/methodology/sourcing-and-citation.md § Writing a Citation` this audit reads. A direction is fixed as that section says, and a candidate that the section's table of wordings excepts is declined with its reason. A violation the patterns missed is reported like any other, and its phrasing is a candidate for a new pattern.

### Markup

The script decides where bold and italic may appear, a field's form and key, a block of fields' line endings and its lists' indentation, where a blank line falls, a run of backticks, and a heading's form. The script cannot judge whether a backtick span holds literal text, whether an italic span holds real stress, and whether a bold lead-in's words are in sentence case, its names aside, as `specs/methodology/spec-style.md § Literal Text`, `specs/methodology/spec-style.md § Emphasis` and `specs/methodology/spec-style.md § Bold Lead-ins` have them. Run the script with `--list-candidates`. It lists each backtick span holding a capital letter and no punctuation that matches no heading, field key, or text a fenced example in the tree holds. It also lists each italic span of more than a few words. Then read the files in scope in full, using the candidates as a guide rather than as the boundary. Among bold lead-ins and headings, the case to look for is a lead-in a citation needs.

### Glossary terms

A use in a file's own ordinary sense, such as an application spec's product record or data field, is outside this audit unless the use could be misread as the methodology's. Run the script with `--list-candidates`. It lists each line outside the glossary where a glossary term, or one of the term's other names, seems to be defined. Then read the files in scope in full against `specs/methodology/glossary.md`, using the candidates as a guide rather than as the boundary. A second definition is cut, leaving what its file says about the term. A term used in the methodology's sense but differently is reworded, or, where the sense recurs, the glossary is corrected. Read too for an abbreviation that the methodology or the application coins and uses without recording it as `specs/methodology/glossary.md § Using an Abbreviation` has it. The script cannot recognize such an abbreviation.

### Construct choice and form

What reading passage by passage misses: prose that reads complete but that a construct would show has a gap. The script decides each declared construct's structure (`§ What the script checks`). It lists as candidates each Decision Table whose cells do not settle that every case matches a row, each Decision Table a cell of which tests against a fact or in another of FEEL's forms, and each Decision Table condition whose values are words only its table names. It lists each exclusive choice a guard of which compares a fact with another or is in another of FEEL's forms, and each table shaped as a construct's with no declaration. It lists each Algorithm step that is no comparison, computation, run or loop and holds `otherwise` or `if`, and each Algorithm or DAG whose Runs When holds words besides its citations. It also lists each loop written `in any order` or `in an order the system leaves open`, and each construct extending another by its Extends field, read with the construct it extends as one. This audit reads those candidates, and every rule of the sections it enforces that the script does not decide, among them:
- whether prose sends the cases of one rule by two or more facts, or by one fact to more than two outcomes, read by meaning since no fixed words mark routing, and so takes the construct `specs/methodology/modeling-constructs.md § When to Use Which` chooses, by its questions asked in order of the case's shape, having first gathered the rule's passages across sections and files, as that section reads a rule whole;
- whether a check of a request that `specs/methodology/modeling-constructs.md § When to Use Which` counts a construct is written as `specs/methodology/modeling-constructs.md § Constructs § Decision Table § A Request Turned Away` has it, never a Constraint, and whether a Constraint such a table keeps is Enforced By its rows;
- whether a configured instance's section says an instance is checked as the written construct is when it is saved, and whether a value a rule reads is taken as its input rather than as structure held as data, as `specs/methodology/modeling-constructs.md § When to Use Which § A Configured Instance` has them; and whether an extending construct's tables hold only what its base lacks and the two read as one are what its construct's section checks for, as `specs/methodology/modeling-constructs.md § Constructs § Declared Construct` has an Extends;
- whether a part hands its work to another construct where `specs/methodology/modeling-constructs.md § When to Use Which § Combining Constructs` writes it;
- where a State Machine's state cannot stay once its work is done, whether every case takes a transition out of it, the guards of an exclusive choice from it covering every case; and what a guard's fact means, and what a state's work is;
- whether a trigger is of the kind `specs/methodology/modeling-constructs.md § Constructs § State Machine § What It Means` gives its case, and an action whose outcome routes the entity a state's work, not an effect;
- whether a terminal state's description states an outcome, not work, and a protocol machine's states hold no work, its transitions are taken on an actor's action and its reasons are only those the system distinguishes;
- where an exclusive choice's guard compares a fact with another, or is in another of FEEL's forms, or its transitions are taken on conditions one occurrence makes true together, whether two of its guards can hold at once, and, where its state cannot stay, whether together they cover every case; and, for a guard in another of FEEL's forms, whether each name it holds is a fact the choice tests, its machine's file declares or its Reads cites;
- whether a state whose work is another machine's run says `governed by` it, and whether a trigger leaving governed work is written where `specs/methodology/modeling-constructs.md § Constructs § State Machine § A Submachine State` places it;
- whether a Trigger Classes table lists each occurrence of its class and no other;
- where a construct reads time, whether it names its clock as a declared fact and reads a clock other than the wall clock by a condition on it, as the trigger kinds' table in `specs/methodology/modeling-constructs.md § Constructs § State Machine § What It Means` has it, reads a value in force by a call naming the instant its rule fixes, splits a period a change falls within by the instants it reads, has a backdated or withdrawn instant follow its fact, and keeps a date on its month's last day or on a business day by the canon's functions; and, for a job's run, what a missed or a late run does, as `specs/methodology/modeling-constructs.md § Time` has them;
- whether a trigger in words is written in the same words wherever it recurs, and a trigger in FEEL in the same expression, names only what happens with no qualifier a guard should hold, and whether a row lists triggers;
- whether a state of a machine citing another's class takes, in its own words, one of the members that class gives;
- whether a condition cell holds only what tests its condition, with no gloss an annotation should hold;
- whether a Reads item citing a construct names an outcome that construct decides;
- whether each expression means what its construct says, as FEEL evaluates it: `null` where a value may be absent or a type differs, three-valued `and`, `or` and `not`, a date, a time or a duration combined as FEEL combines them, and a list, a context or a function read as FEEL reads them, as `specs/methodology/expressions.md § Expressions § FEEL § Null and Three-Valued Logic`, `specs/methodology/expressions.md § Expressions § FEEL § Arithmetic and Time` and `specs/methodology/expressions.md § Expressions § FEEL § Lists, Contexts and Functions` have them;
- where a Decision Table's condition names its kinds as words only its table names, whether its values hold every kind of case, or the condition sorts by kinds yes-or-no questions define and is to be written as those questions, as `specs/methodology/modeling-constructs.md § Constructs § Decision Table` has such a condition written;
- where a Decision Table's cell tests against a fact, which rows a case reaches and whether every case matches one; where a column's fact is declared in another file, whether its cells test values of that fact's Type; and whether a computed header's kind agrees with its cells';
- whether a computed outcome needing a walk whose order changes it cites an Algorithm, and whether an outcome other conditions decide is a table of its own;
- whether a loop or a comparison is folded into another step's work;
- where a table takes the outcome of every row it matches, whether the outcomes two rows give one case can both be carried out;
- whether each part a Constraint's Enforced By cites keeps the rule where a write could break it, whether every write able to break the rule is covered, whether a section a rule is `after` or `before` states in its own text an operation, and whether a step a rule bounds an approximation by keeps the bound;
- whether a table is the construct `specs/methodology/modeling-constructs.md § When to Use Which § A Table's Construct` gives it by its author's answers. It is reported wherever it is not, and the builder's triage tells which a design wrote. A table no change wrote keeps its declaration until the user migrates it;
- whether the right construct models the rule, and whether a Decision Table's outcomes are values and nothing its evaluation does acts, what acts being the construct running it;
- whether a construct section's prose states a rule an outcome the spec states depends on and the files could check, where no check decides it: a column, a field or a form the construct has and the author did not use, or one it lacks, which a design adds, a new construct or a notation by updating `specs/methodology/modeling-constructs.md` first, as `specs/methodology/modeling-constructs.md § Defining Constructs` has it;
- whether a part's identifier is short and kept stable for the part's life;
- whether a Basic Table the script does not reach, in a list item, a quote or an indented block, is headed by field labels, whether a header word the script passes as a proper noun's own casing is one, and whether a Basic Table declares its natural key where its rows have one and the columns every row must fill, and whether a key a citation names is short and kept stable for its part's life, as `specs/methodology/modeling-constructs.md § Constructs § Basic Table` and `specs/methodology/modeling-constructs.md § Constructs § Keyed Construct` have them;
- whether each task's work in a DAG is the whole of it, whether a task whose work is `none` is said to be whose and when done, and whether what runs the DAG is run on it;
- whether an Algorithm's branch with nothing to do is written `continue`;
- whether an Algorithm's work in words computes no value a later step reads and decides nothing, a value being a computation's and a choice a comparison's;
- whether a loop written `in any order` gives the same whatever its order, and whether one written `in an order the system leaves open` has a Constraint enforced by `nothing:` recording that its result depends on it;
- whether every path to an Algorithm's `End` sets each fact its Output names that its Inputs do not, and whether a fact read from another file is used as its record types it;
- whether a Terminates cell's number shrinks with each pass toward an end the step reaches;
- whether an Algorithm reads each value the system derives by a call given the current value, never by a path that keeps what the value held before a step changed what it derives from;
- whether an Algorithm whose Runs When states an occurrence is run on it;
- whether a value is rounded only where a computation calls `decimal` or a rounding function, or as the Algorithm's arithmetic or a fact's decimal places round it, whether money computed by multiplying or dividing reaches a part through a fact holding decimal places, and whether a result an order changes states its order;
- whether an item copied from a list is read from the list again once a step changes the list, before it is changed, run or merged back, and whether each function a step calls is a fact its file declares or its Inputs cite, or one a step sets, of one of the kinds `specs/methodology/modeling-constructs.md § Constructs § Algorithm` names, never a computation another construct specifies;
- whether each construct's section heading names a thing, never an activity, a section titled for an activity giving its construct a subsection, and whether its description says what it models for a reader meeting it first, as `specs/methodology/modeling-constructs.md § Constructs § Declared Construct` has them;

This audit also reads whether a record type is an entry written repeatedly or a closed set a spec defines, and never a schema of data the product stores, as `specs/methodology/modeling-constructs.md § Constructs § Record Form` has it. The script knows every type the specs declare.

Of `specs/methodology/checks.md § Check`, `specs/methodology/checks.md § Script Check` and `specs/methodology/checks.md § Semantic Check`, this audit reads each record type's declaration, what the sections say of the two concrete types, and what `specs/methodology/checks.md § Check` says a record's fields leave out. Skill form reads the rest of `specs/methodology/checks.md § Check`: what a check is, a candidate list, the checks taking no record, where a check stands, the skills' tables of checks and naming a check where it runs.

### Placement

What is easy to miss: one particular file named by a bare filename another directory shares, or a kind of file named by a path, an open question recorded in a file that cannot cite everything it impacts, and a spec of a system that exists stating what its author intended rather than what is built, the suspected defect no open question.

### Finished style

Of `specs/methodology/sourcing-and-citation.md § Writing a Citation`, this audit reads only the paragraph on where a citation sits. Run the script with `--list-candidates`. It lists each line holding a phrase the Example column of `specs/methodology/spec-style.md § What a Finished Spec Reads Like`'s table quotes, each long sentence of chained clauses, and each path into the application specs in the methodology, `specs/AGENTS.md` or `specs/architecture.md`. It also counts, for each file, the places `specs/methodology/spec-style.md § Clear Prose` has a reader test in a sentence of prose:
- a term of its tables of words;
- a contraction;
- a curly quotation mark;
- a comma that may splice two statements;
- a contrast;
- a trailing clause;
- a reason ending a long sentence;
- a chain of "its";
- "never" with "always";
- a paragraph whose sentences average long or hold no short one;
- a paragraph holding more than one semicolon.

In the skills too, the script counts each sentence carrying more than one citation. It also counts each citation inside its clause: one that neither closes its clause, nor stands in parentheses, nor opens its sentence, nor follows "as". `--detail` lists each one. The script lists nothing in a table or a heading, so read those whole. Use the list as a guide rather than as the boundary. A listed word is a finding only where it adds nothing to its sentence. An emphasis word whose deletion leaves the meaning as it was is one such word. A listed construction is a finding where it breaks the rule naming it, such as a chain of "its" that leaves its noun unclear, or a semicolon that does not lean. Read too for what no script lists: an actor left unnamed where a sentence describes what a system or a person does, a term varied for variety, a pattern of machine-written prose, and an analogy removed by a rewrite or wedged into a rule's clause. Read for American English too, which no script lists: a spelling Merriam-Webster does not give first, and a usage American English replaces (`specs/methodology/spec-style.md § Clear Prose`). Neither is a finding in a quotation, a title or a name from outside the specs. A trade-off that passes its section's test is declined with the reason. For `specs/methodology/spec-style.md § Clear Prose`, read each passage in the unit once, as its primary reader. A passage that takes a second read is a finding, and its fix rewords it without changing what it states. An example in the canon drawn from the application specs is a finding, read for by meaning, with the listed paths as where to start. The skills are Skill form's to read for it, through `specs/methodology/skills.md § Authoring a Skill`.

### Working-file form

Of `specs/methodology/working-files/main.md § The Working Files`, the paragraphs on a skill's scratch space and on its plans are Skill form's to read. This audit reads the rest. It reads `specs/methodology/modeling-constructs.md § Fields` and `specs/methodology/spec-style.md § Blank Lines` only as they reach `.ai/follow-ups.md`, as `specs/methodology/scope.md § Rules and Skills` has an audit name the part of a section it reads. `--check-scope` reads no working file, so this audit runs the checks `specs/methodology/modeling-constructs.md § Fields` gives a block of fields and the check `specs/methodology/spec-style.md § Blank Lines` gives a blank line over that file itself, by `--check-layout .ai/follow-ups.md`. It reads no plan, as `specs/methodology/working-files/main.md § A Design Document` has it. What is easy to miss: a follow-up leaning on a skill's output under `.ai/tmp/`, which the skill clears once the output is stale.

### Diagram currency

Run this audit only once the script's diagram check passes. If the check fails, the work is fixing the citations, and there is nothing yet to compare. Then render the diagram through `.ai/skills/author-mermaid-diagram/`, and read every section the diagram's Sources list names. Read the picture against those sections, each label against the diagram's host file, and the list against where each thing the diagram draws lives. A source the uncommitted changes edited, read in their diff against the last commit, is where to look first. Of `specs/methodology/sourcing-and-citation.md § Keeping Specs in Sync § Materialized Views`, this audit reads the paragraph on a diagram. A picture saying something its sources do not takes the report row for a summary that disagrees with what it summarizes. A source missing from the list, or a listed section that is only a summary of the home or broader than `specs/methodology/modeling-constructs.md § Diagrams` asks, takes the row for a required thing that is absent or sits on the wrong side.

### Principles held

This audit makes each semantic check whose Carried Out By names it, among those standing under `specs/AGENTS.md § Constitutional Principles` and under each principle. An audit names no design, so it cannot read what a change replaced, and it reads the files as they stand. What is easy to miss:
- a unit amended rather than written, a clause or a case wedged beside text left as it was, each sentence of which reads true on its own;
- a rule below the principles relaxing one by an exception for its own case, naming no principle.

## The report

A run states the unit it covered and gives a verdict on it: current, current with named fixes, or drifted. A run in a design's apply reports its findings as any run does, and the builder triages them against the design's changes, as `specs/AGENTS.md § Design, Refactor, Refine § An Audit` has an audit read. Each finding is a row, in the shape this section gives for its kind of defect.

**Construct:** `specs/methodology/modeling-constructs.md § Constructs § Decision Table` \
**Conditions:** Defect

| Defect | Row |
|---|---|
| A summary disagrees with what it summarizes | the file, the claim, the source, and which compression distortion it is |
| A required thing is absent, or sits on the wrong side | the location, the rule it breaks, and what is missing or misplaced |
| A rule has two homes | both statements, the home chosen, and, where it was hoisted, the usages that forced its height |
| Any other rule broken | the location, the rule it breaks, and what is wrong |

A report carries the warnings the script listed for its unit, under a heading of their own. Each warning is a rule the specs record as kept by nothing. A warning is listed, and is never a finding. A report also carries what was examined and declined: the candidate that had the shape of a defect and turned out not to be one, with the reason it failed the test. This record is neither padding nor optional. The expensive half of an audit is arriving at the judgment that something suspicious is correct. A report that keeps only the findings throws that half away, so the next run pays for it again and may reach the opposite answer. Declining a candidate in writing is also what makes an over-eager audit reviewable: a reader can check a rejection as easily as a finding.

A report carries its review observations (`specs/methodology/glossary.md`) apart from its findings, under a heading of their own and uncounted: what the auditor noticed beyond the audits it ran. A run in a design's apply has the builder bring each to the user with its triage, as `specs/AGENTS.md § Design, Refactor, Refine § Who Decides` has it.

Each run writes one file to `.ai/tmp/audit-specs/`, named for the unit and the date. A run clears any earlier report for the same unit. That earlier report is stale output, which a skill cleans as `specs/methodology/working-files/main.md § The Working Files` has it.

A finding in a working file's form is put right as `specs/methodology/working-files/main.md § The Working Files` has the file changed. In a design's apply, its builder settles each other finding as `specs/AGENTS.md § Design, Refactor, Refine § An Audit` has an audit's findings settled. Outside a design's apply, any other finding becomes a design document (`specs/methodology/working-files/main.md § A Design Document`) rather than an edit. The design goes through the Design, Refactor, Refine process (`specs/AGENTS.md § Design, Refactor, Refine`). `specs/AGENTS.md § Design, Refactor, Refine § Direct Edits` says when a small finding may be applied directly instead.

## Running one

`specs/AGENTS.md § Design, Refactor, Refine § An Audit` covers who reads an audit's findings, how their quoted evidence is confirmed and how they are triaged. Who runs an audit and what the audit reads are as `specs/AGENTS.md § Design, Refactor, Refine § Who Checks What and Why § Check Roles [Check: an audit]` has them: a cold agent given this skill's name and, in a design's apply, the kinds `specs/methodology/design-workflow.md § A Design's Reviews` sets, with no brief (`specs/methodology/design-workflow.md § A Review's Brief`). All of it applies. Here, an audit run by the content's own author costs a confident sweep that misses the section the author forgot existed.

## Scoping a run

### Audit Unit

The unit each audit reads at a time:

**Construct:** `specs/methodology/modeling-constructs.md § Constructs § Decision Table` \
**Conditions:** Audit

| Audit | Unit |
|---|---|
| Directory summary currency | the tree rooted at a directory owning an `architecture.md`, and what its overview describes beyond its directory, code aside, plus each `index.md` beneath it |
| Counterpart currency | per product file, and each technical file no product file's `technical-specs` names |
| Scenario coverage | per product file |
| Where a rule lives | per unit: `AGENTS.md`, `specs/AGENTS.md`, `specs/main.md`, `specs/architecture.md`, `specs/methodology/`, `specs/application/product/`, `specs/application/technical/` |
| Whether the home holds the fact | per cited section, taking every citation into it in one pass |
| Ordinals and counts | everything in the script's scope |
| Markup | everything in the script's scope |
| Glossary terms | everything in the script's scope, the glossary among it |
| Construct choice and form | every spec, `specs/AGENTS.md`, and each skill's files, every form template aside, a skill's or the core canon's |
| Placement | per directory, its `index.md` and every file in it, with the product `architecture.md` for the product side |
| Finished style | the specs and the documentation, and, for `specs/methodology/spec-style.md § Clear Prose`, both `AGENTS.md` files, and, for where a citation sits, every skill |
| Agent agnostic | both `AGENTS.md` files, each registered skill, the project's `.gitignore`, and the helpers the root `AGENTS.md` names |
| Skill form | `specs/methodology/skills.md`, each registered skill, the code the skills share, each unregistered skill `--list-candidates` lists, the states of `specs/methodology/design-workflow.md § The Order of a Design's Work`, the Check Role records of `specs/AGENTS.md § Design, Refactor, Refine § Who Checks What and Why § Check Roles`, and each section a record section of `Script Checks` or `Semantic Checks` stands under |
| Working-file form | `.ai/follow-ups.md` |
| Diagram currency | per diagram, with every section its Sources list names |
| Principles held | every spec, `specs/AGENTS.md` and each skill's files, each check it makes reading them by the Unit its record gives |

`specs/architecture.md` roots the tree over the whole of `specs/`, so a directory summary run over it reaches `specs/index.md` and `specs/application/index.md`. `specs/index.md` sits above every other architecture-rooted tree, and `specs/application/index.md` above the application's.

## What the script checks

Each row describes, in the script's own terms, what the script checks for the section the row names. That section governs the check (`specs/methodology/scope.md § Rules and Skills`). A check that lists a warning reports what the specs record as a gap of the system: a Constraint that nothing keeps. The script prints its warnings after its findings, apart from them. A warning never sets the script's exit status, so a run listing warnings alone passes.

**Reference Key:** Check \
**Required:** Section

| Check | Section |
|---|---|
| Every `file § A § B` resolves to that heading path in that file | `specs/methodology/sourcing-and-citation.md § Writing a Citation` |
| Every citation in `README.md`, the files under `docs/` and every spec but `specs/AGENTS.md` is a link reaching what it resolves to, a Construct, an Extends or an Implements value, a fenced block and front matter aside; and no skill or `AGENTS.md` file carries one | `specs/methodology/sourcing-and-citation.md § Writing a Citation § A Citation's Link` |
| A citation never points down a layer except from `specs/AGENTS.md`, `specs/main.md` or `specs/architecture.md`, never crosses between application and methodology or from an application spec to either, whether it names a section or a whole file, but a Construct field citing its construct's definition from any layer, and no spec cites a section of the project's root `AGENTS.md` | `specs/methodology/sourcing-and-citation.md § Which Citations Are Allowed` |
| No citation targets an `index.md` | `specs/methodology/sourcing-and-citation.md § Writing a Citation` |
| A cross-file citation carries a project-root path | `specs/methodology/sourcing-and-citation.md § Writing a Citation` |
| A section citation into `.ai/skills/` comes only from a file of the same skill | `specs/methodology/skills.md § Authoring a Skill`, `specs/methodology/sourcing-and-citation.md § Which Citations Are Allowed` |
| Every section token sits inside a backtick span | `specs/methodology/sourcing-and-citation.md § Writing a Citation` |
| A heading carries no ordinal, no section token, and is unique among its siblings | `specs/methodology/sourcing-and-citation.md § Titling a Heading` |
| A `Test Scenarios` section sits one level below its capability, and a file holding one holds a `gherkin` fence | `specs/methodology/acceptance-scenarios.md § Acceptance Scenarios` |
| Every `gherkin` block parses: each `Scenario:` followed by at least one `Given`, `When`, and `Then` | `specs/methodology/acceptance-scenarios.md § Acceptance Scenarios` |
| Every `technical-specs` list is sorted in plain character order, appears only in a product file, and every path in it resolves under the technical directory | `specs/methodology/spec-placement.md § Naming the Technical Files Behind a Capability` |
| `specs/methodology/glossary.md` holds no citation and one table, headed Term, Abbreviation and Definition, whose Term cells are bare terms, unique and sorted, each with its abbreviation, if any, bare in its own column and a definition naming none; each definition ends with its other full names in the fixed form, and no abbreviation or other name is shared by two terms or equals a term | `specs/methodology/glossary.md § Writing an Entry` |
| No specification, `AGENTS.md` file or skill, its scripts among it, uses an inside-the-house abbreviation, one in the glossary's Abbreviation column or recorded in the application specs as `(abbreviated X)`, anywhere but where it is recorded, a diagram's node ids aside, and none is recorded twice | `specs/methodology/glossary.md § Using an Abbreviation` |
| Every section of `specs/AGENTS.md`, of `specs/main.md` and of each file under `specs/methodology/` its index tables name but its `architecture.md`, its `index.md` files, its worked examples and a form template, one whose name ends `-form-template`, is named, itself or through a section it sits under, in the Enforces column of `§ The audits` or the Sections of a record of `§ Operating rules carried out by a step § Skipped Steps`, or, for a section of `specs/methodology/code.md`, in the Enforces column of the `verify-spec-implementation` skill's table of checks, or is named by a record section of `Script Checks` or `Semantic Checks` standing directly under it, which names no section under that one, no record section of checks being itself reported, and each section a Skipped Step's Sections names is cited, itself or through a section it sits under, by a step under a registered skill's `## Workflow`, `§ Operating rules carried out by a step § Skipped Steps` holding at least one record | `specs/methodology/scope.md § Rules and Skills` |
| No spec embeds an image | `specs/methodology/modeling-constructs.md § Diagrams` |
| Each working file `specs/methodology/working-files/main.md § The Working Files` names is ignored by a line of the project's `.gitignore` naming it or a directory holding it, and no negating line un-ignores it | `specs/methodology/working-files/main.md § The Working Files` |
| No reviewer definition an agent writes to set itself up, `review-light`, `review-medium` or `review-high`, whatever its extension or held as a folder, is tracked, read from `git ls-files` where the project is a git repository | `specs/methodology/scope.md § Agent Agnostic`, `specs/methodology/skills.md § Setting Up an Agent` |
| Every directory under `specs/` has an `index.md`, naming each file and subdirectory it holds, each row naming one that exists, this check alone reading the filesystem rather than the index tables | `specs/methodology/spec-placement.md § Where a File Goes` |
| The script's scope is read from `specs/methodology/skills.md` and the files `specs/methodology/scope.md § What Spec of Record Governs` names; a missing or empty registry is a finding, never an empty scope | `specs/methodology/scope.md § What Spec of Record Governs` |
| The tree in the fenced block of `specs/methodology/scope.md § The Shape of the Scope`, read inside its fence, names exactly the files in `specs/methodology/`, and every path it names exists | `specs/methodology/scope.md § The Shape of the Scope` |
| The kinds in `specs/methodology/scope.md § What Spec of Record Governs` are the ones the script reads, and each home the table names exists | `specs/methodology/scope.md § What Spec of Record Governs` |
| Every row of the registry in `specs/methodology/skills.md` names a skill in backticks with a directory under `.ai/skills/` | `specs/methodology/skills.md § Registered Skills` |
| Every registered skill's `SKILL.md` opens with YAML front matter whose `name` is its directory's name, in kebab-case, at most 64 characters, and whose `description` is present, at most 1,024 characters; a `scripts/` directory beside it, where it has one, holds an entry-point script named for the skill | `specs/methodology/skills.md § Authoring a Skill` |
| Every registered skill's `SKILL.md` has a `## Workflow` section | `specs/methodology/skills.md § Authoring a Skill` |
| Every diagram in `specs/` sits directly under a heading of its own whose section holds, in this order and nothing else, the diagram, then its `**Caption:**` and `**Sources:**` fields as one block of fields, the Caption citing no section and no file, the Sources a list of one citation per item, sorted, each resolving to a section or a record other than the diagram's own; and every listed section carries a citation of that diagram's heading in its own text, or, for a record section or a record, in that record section's `**Diagrams:**` field | `specs/methodology/modeling-constructs.md § Diagrams` |
| Every fenced `mermaid` block under `specs/` declares `flowchart` | `specs/methodology/modeling-constructs.md § Diagrams` |
| No bold lead-in or list item carries a number | `specs/methodology/spec-style.md § Ordinals and Counts` |
| No file under `specs/` other than a file of the working-files document's folder, `specs/methodology/working-files/`, and `specs/AGENTS.md` names a working file | `specs/methodology/sourcing-and-citation.md § Which Citations Are Allowed` |
| Every bold span opens a line, after any list marker, quote marker and indentation, and closes on a colon inside the bold, a field, its bold key followed by a space and any list marker before it a hyphen, or a period or a question mark inside the bold, a bold lead-in; bold italic and underscore bold are reported wherever they appear; and an em dash or an en dash outside code, which no sentence uses as punctuation | `specs/methodology/modeling-constructs.md § Fields`, `specs/methodology/spec-style.md § Bold Lead-ins`, `specs/methodology/spec-style.md § Emphasis`, `specs/methodology/spec-style.md § Clear Prose` |
| No line opens with italic, after any list marker, quote marker and indentation; underscore italic goes unchecked, since it cannot be told apart from an identifier such as retention_purge written outside backticks | `specs/methodology/spec-style.md § Emphasis` |
| Every record citation resolves to a record section, names each field of its type's Reference Key, in the key's order, and no other, separated by `; `, and matches exactly one record; brackets on a section that is not a record section name a part of the construct the section declares, one key its construct's definition declares as its Reference Key, a table's name and its key joined by a dot where the construct has more than one keyed table and a key written alone read so in the application specs only, and a value a part of it holds, or a row of the one Basic Table the citation's path or its key's columns reach, by the path its Table Name and its key make where it declares a name, each column its Reference Key names, in its order, and no other, separated by `; `, matching exactly one row, and are malformed on a section declaring neither; and a value a citation names holds no `§`, `;` or `]` | `specs/methodology/sourcing-and-citation.md § Writing a Citation` |
| No heading title contains `[` | `specs/methodology/sourcing-and-citation.md § Titling a Heading` |
| In each file under `specs/` and each skill's file but a form template, a skill's or the core canon's, one whose name ends `-form-template`, a section holding a `**Records:**` field is titled with the Plural Name of a type the specs declare, its fields read from its declaration, a type extending another holding its base's fields first; a record section holds an optional `**Diagrams:**` field, then any section fields its type declares, each it requires present, in its order, none at its default and each value one its Values allow, then a `**Records:**` field of at least one record, one list item each, and nothing else, the section's fields one block of fields; each record, a nested one against the type its field cites, gives its type's fields in their order as one block of fields in its item, every field its type requires and none at its default value, each value one its type's Values allow where they list them; a construct nested beneath a field, at any depth, stands only beneath a field whose Holds cites `specs/methodology/modeling-constructs.md § Fields § A Nested Construct`, and each field of any other block nested beneath a field's text is read as a field of its record; a field holding records holds each as an item of its list, each item a record opening with a field its type gives, a field holding one record holding one item; no two records of one collection, a record section's own items or the records one field holds, share their identifying values, nor a value of a field marked Unique; a value of a field whose Values cite a closed set is one of the set's members, a second record section of a closed set a fact's or a field's Values cite is reported, and a field whose Values cite the definition of a type whose record section a Values cites is reported; the records a fenced `markdown` block holds are read as a file of its own, against the types the block declares and the canon's; an `Open Questions` section is its file's last top-level section, and each of its records' Impacts carries at least one section citation | `specs/methodology/modeling-constructs.md § Constructs § Record Form`, `specs/methodology/modeling-constructs.md § Fields § A Nested Construct`, `specs/methodology/spec-style.md § Markdown`, `specs/methodology/spec-placement.md § Open Question`, `specs/methodology/sourcing-and-citation.md § External Reference`, `specs/methodology/modeling-constructs.md § Defining Constructs § Declaring a Construct § Fact` |
| Every canon-spec annotation in a registered skill's scripts, and the code the skills share, is a comment line of its own holding the tag, a space and a citation of `specs/AGENTS.md` or a methodology file, or a section of one, that exists, a part it cites being a check's record, matching one record, and each run of them on consecutive lines is sorted in plain character order | `specs/methodology/sourcing-and-citation.md § Writing a Citation § Citing From Code`, `specs/methodology/skills.md § Authoring a Skill` |
| Each form template in the core canon, a file under `specs/` whose name ends `-form-template`, cites a section in its first placeholder; each heading it lays out outside a fence is the heading of a part that section's table of parts gives, in the table's order; and each field it lays out with a placeholder citing a record type's section is a field that type declares, in the type's order | `specs/methodology/scope.md § Form Templates` |
| The script's copy of each construct's table of the fields it declares matches that table where it is defined, row by row: each field's name and order, whether it is required, its default value and its values, each Values cell a quoted list, a citation or `text`; a record type has none, read from its declaration; and its copy of the columns of a table of fields and of each tabular construct's tables matches the `Column | Holds` tables defining them, each column headed in backticks, in order, its optional columns and a Name column where it may open one among them | `specs/methodology/modeling-constructs.md § Constructs § Construct`, `specs/methodology/modeling-constructs.md § Constructs § Tabular Construct`, `specs/methodology/modeling-constructs.md § Constructs § Decision Table`, `specs/methodology/modeling-constructs.md § Constructs § Algorithm` |
| In `specs/application/technical/environments.md`, every environment's section opens with one `**Kind:**` field, on a line of its own, whose value is local, integration, shared or production, no other Kind field appears, exactly one environment is local, and every tools table is headed Tool, Version and Purpose with at least one install column after them, and every tasks table Task, Command and Does, with Runs On after them where a task needs it | `specs/methodology/spec-placement.md § Environments` |
| Each Basic Table outside a fenced block, a list item, a quote and an indented block is headed by field labels, but a header in backticks and a word in a proper noun's own casing; its fields opening it, `**Table Name:**`, `**Reference Key:**` and `**Required:**`, in that order, one block of fields before it, its Table Name, and a Table Name opening any construct's table, a field label unique among its section's tables, a construct's keyed tables taking part in the clash, its Reference Key and its Required naming columns its header holds, none named by both, no cell under either blank and its key's values unique, alone or together; of tables in one section keyed by the same declared columns, all but one declaring a distinct Table Name; a cited key value holding no `§`, `;` or `]`; and a Reference Key a definition sets names, where its instances write more than one keyed table, each table's name as its definition gives it and that table's key, joined by a dot | `specs/methodology/modeling-constructs.md § Constructs § Basic Table`, `specs/methodology/modeling-constructs.md § Constructs § Keyed Construct` |
| A table whose first header is a registered standard's Name and which holds a Treatment column is a mapping onto that standard in its one form, opened by its fields: its Table Name the standard's Name and `Elements`, its Reference Key that Name, its Required `Section, Treatment`, its columns that Name, Section, Treatment, Departs For and Why, each Treatment opening `the same`, `differs:` or `not written`, and a Departs For of one or two of `the standard's gap`, `the canon's form` and `no need yet`, in that order, and a Why on each row that differs or is not written and on no other; the script's copy of those kinds matches the mapping's Departs For row; and a sentence of a methodology file, its overview and its index aside, naming a departure from a registered standard, in any wording, departing, differing or deviating from it, unlike it or contrary to it, cites a row of that standard's mapping, a sentence opening that standard's mapping aside | `specs/methodology/sourcing-and-citation.md § External Reference § A Mapping onto a Standard` |
| In each file under `specs/` and each skill's file but a form template, a skill's or the core canon's, every line opening with a bold phrase ending in a colon inside the bold carries a key a form declares, where that form places it, a record type the specs declare declaring its fields' keys and the fields of a construct nested beneath a record's field placed as that construct's | `specs/methodology/modeling-constructs.md § Fields`, `specs/methodology/modeling-constructs.md § Fields § A Nested Construct`, `specs/methodology/modeling-constructs.md § Constructs § Record Form` |
| A Record Form, a record type's declaration, gives a Plural Name, then its tables: a table of any section fields it declares, headed Field, Required, Default Value, Values and Holds, then its table of record fields, headed Field, Unique, Required, Default Value, Values and Holds, that table left out only by a type extending another; each field named once, by it or its base, its Unique yes or no, and a Reference Key, its own or its base's, naming fields the type gives and requires, a type extending another declaring none and a key of one field marking that field Unique, its Default Value empty where it is required and given where it is not, and each Values cell a quoted list, a citation or `text`, a citation of a record type's definition, alone or after `a list of`, holding that type's records, one or a list; a type holding itself through fields whose Required is yes, each citing a record type's definition, its own or other types' in turn, is reported; an abstract type, its Modifier `Abstract`, is extended by some type, no field cites its definition, and no record section is titled with its Plural Name; it declares no Order or Held In; its section is titled with the type's name, bare, opening with no article and never its Plural Name; and its Plural Name is no other type's where its records may sit, a canon type's in each file under `specs/` and each skill's file but a form template, an application spec's type's in the application specs, and those of a type a fenced `markdown` block declares in that block alone, the block's declarations' own findings unreported | `specs/methodology/modeling-constructs.md § Constructs § Record Form`, `specs/methodology/spec-style.md § Markdown`, `specs/methodology/modeling-constructs.md § Constructs § Construct` |
| A Facts record's Values written as one citation names the record section of a type identifying its records by one field, or a Basic Table keyed by one column, its values the identifying values of those records or rows, and sits on a fact whose Type is `string`, judged once the record's Type is one FEEL names | `specs/methodology/modeling-constructs.md § Defining Constructs § Declaring a Construct § Fact`, `specs/methodology/modeling-constructs.md § Constructs § Record Form` |
| Each directory of the worked examples a section of `specs/AGENTS.md`, of `specs/main.md` or of the methodology's files names exists, and each topic of `specs/methodology/examples/`, a subject's subdirectory, is named by such a section | `specs/methodology/scope.md § Progressive Disclosure` |
| Outside a fenced code block, and outside an indented one where `specs/methodology/spec-style.md § Blank Lines` reads a line as one, no run of two or more backticks opens or closes a code span but a citation's, carrying a key value that holds a backtick | `specs/methodology/spec-style.md § Literal Text` |
| Every block of fields, those a fenced `markdown` block holds and those nested beneath a field among them, as `specs/methodology/spec-style.md § Markdown` and `specs/methodology/modeling-constructs.md § Fields § A Nested Construct` have them read, has each line that a line opening a field's key directly follows end with one space and a backslash, no other line of the block end with one, and each list a field holds stand with its items two spaces beyond its key, a list at its key's indentation reported | `specs/methodology/modeling-constructs.md § Fields`, `specs/methodology/modeling-constructs.md § Fields § A Nested Construct`, `specs/methodology/spec-style.md § Markdown` |
| Every blank line stands where the Decision Table of `specs/methodology/spec-style.md § Blank Lines` gives true and nowhere it gives false, each line read as the element it opens or continues, a fenced `markdown` block read as `specs/methodology/spec-style.md § Markdown` has it and any other code block as one element, a field nested beneath the field above where its key stands two spaces beyond that field's key, the table read from `specs/methodology/spec-style.md § Blank Lines`, each of its conditions taken by its name, the element names the module holds compared with the table's Input Values and each condition it names that the module does not work out reported | `specs/methodology/spec-style.md § Blank Lines` |
| Every construct's section opens with prose before its `**Construct:**` field, its description; every `**Construct:**` field, at the margin or opening a construct nested beneath a field as `specs/methodology/modeling-constructs.md § Fields § A Nested Construct` has one stand, its block read dedented, cites a construct's definition, locally qualified, a bare name read so in the application specs alone until they are migrated, opens the construct's block of fields: the fields that construct sets, in that block, a list-valued one its items beneath its key, in their order, a field the construct sets standing beneath a `**Table Name:**` reported, an Algorithm's Inputs and Output, either taking `none` on its key's line, and a Decision Table's Conditions among them, and no field written at its default value, a Hit Policy as Unique, or Reads, Computed, Annotations, Input Values or Default Output as none, or a Protocol as No, and each value one its field's Values allow where they list them; no such field outside a construct's block, but a Reference Key in a construct's definition, or a Table Name, a Reference Key or a Required opening a Basic Table, before it in that order; then its tables headed as its form gives, a column a construct renamed read in its old spelling, a State Machine's `description` as `Description`, say, in the application specs alone until their tables are migrated, and reported in it anywhere else, every row as many cells as its header, no cell empty but where its form allows, no cell holding `none` or `-` where its form does not give it, a Name column opening only a table it may open, every row named and no two alike, and each part's identifier, a state's, a task's or a Name, holding no `§`, `;` or `]`; a Held In, a list, gives an item for each table its construct's form gives, each a fact's name, a colon and the citation of a Facts record declaring it whose Type is a list of a context whose entries are named as that table's columns; an Extends cites a construct of the same kind, and a construct declaring one is checked for its fields and its tables' form alone; and no section holds two constructs of its own | `specs/methodology/modeling-constructs.md § Defining Constructs § Declaring a Construct`, `specs/methodology/modeling-constructs.md § Defining Constructs § References and Names`, `specs/methodology/modeling-constructs.md § Constructs § Declared Construct`, `specs/methodology/modeling-constructs.md § Constructs § Ordered Construct`, `specs/methodology/modeling-constructs.md § Constructs § Configured Construct`, `specs/methodology/modeling-constructs.md § Constructs § Keyed Construct`, `specs/methodology/modeling-constructs.md § Constructs § Tabular Construct`, `specs/methodology/modeling-constructs.md § Constructs § Decision Table`, `specs/methodology/modeling-constructs.md § Constructs § Algorithm` |
| A State Machine's States and Transitions tables open with their Table Names, States and Transitions; its Transitions table is headed From, To and Trigger, then a Guard, an Effect or both in that order, no such column every cell of which is none, each Effect cell the citation of an Algorithm or a Decision Table, or `none`; a Recorded In field is a fact's name, a colon and the citation of a Facts record whose Values, a quoted list or the citation of a closed set, hold each state's name, a state drawn from a closed set opening its description with the citation of its member, its record or its row; a word a guard tests a fact for, by `=`, `!=` or `in` a list or tests, one of the fact's Values, the fact its machine's own file declares or the one its Reads cites; each Reads item a fact's name, a colon and a citation; a protocol machine has no Effect column, no transition with no trigger or taken on time or a condition, and no governed state; a Trigger Classes table, found in the machine's section after its Transitions table and before a subsection by its Table Name or its header, and reported where no machine's section holds it so, opens with its Table Name, is headed Member and Class, each row a member and its class each written, writes each member once, a member citing a machine cites one whose Trigger Classes table holds its class and stands for the members that table gives it, a member written in FEEL checked as a trigger is, each class a trigger a transition names, and no state takes a class and one of its members; a state's description saying `governed by` names a State Machine and no part of one, and a description citing another machine's whole section says it; a state is governed by one machine at most, no machine governs itself, a governed state is not terminal, and it is left, of its transitions with no trigger, as its machine's exits have it: by one with no guard where its machine has one terminal state, by one for each guarded `exit = "{that state}"` where it has more, by the join alone where it stands in a join's From, and by none where its machine never ends | `specs/methodology/modeling-constructs.md § Constructs § State Machine`, `specs/methodology/modeling-constructs.md § Constructs § State Machine § A Submachine State` |
| A State Machine's states are named uniquely, free of a comma and the word `and`, each initial and terminal Yes or No, one initial and each reached from it, a state that is not terminal having a way out and a terminal one none; each From and To names a state, a From one state or a join's several; its forks and joins pair, and an exclusive choice's guards, each a FEEL boolean expression parsed by `expressions.py`, a fact it tests as a boolean named as a question, every fact it tests holding no word FEEL keeps, read where each is a conjunction of tests of facts as a Decision Table's rows, each fact tested once, every name a test holds one a guard of the choice tests, its machine's file declares or its Reads cites, or `exit`, a fact compared with another of its kind, and each fact one kind of value across them, never both hold, and each can hold, a choice with a guard in any other of FEEL's forms listed for the reading audit | `specs/methodology/modeling-constructs.md § Constructs § State Machine` |
| A trigger opening with `after`, `at` or `when` and a space is a FEEL expression parsed by `expressions.py`, judged with the facts in scope, its file's own and those its machine's Reads cites, every problem it gives reported, and one calling FEEL's `today()` or `now()` reported, `after` and `at` reading the wall clock; `after`'s giving a duration, `at`'s a date or a date and time and `when`'s a yes or no; two triggers in FEEL are compared by their tokens; a Trigger Classes member written in FEEL is checked as a trigger is | `specs/methodology/modeling-constructs.md § Constructs § State Machine`, `specs/methodology/modeling-constructs.md § Constructs § State Machine § What It Means`, `specs/methodology/modeling-constructs.md § Time` |
| A Decision Table is judged by the groups of its section's Checks in their order, each only once the table breaks none before it, and which rows a case matches only once every condition column tells one case from another; it names its conditions in a Conditions field and any hit policy as DMN names one, and its Conditions and Annotations name columns it holds, conditions first, then one or more outcomes, then annotations, each annotation's header a field label; each cell is FEEL's unary tests or a word written plain, which is no number, never `true`, `false`, `null` or `-`, holds no `?`, and opens as no other form does, `@` and a brace among them, nor with `null`, `true` or `false` and a comma, no value tested after `=`, a question's outcome `true`, `false` or `null`, a condition column and its Input Values test one kind of value, `null` aside, and no outcome cell outside a Computed column is written as a test or a list, `=` among them; a condition's header is a fact's name or a computation; a cell, a computed header or a computed outcome names only a condition's fact, a fact its file's Facts section declares or a Reads item, a cell ending at a fact of its column's kind, each Reads item a fact's name or a question, a colon and a citation, its name the one a Facts record it cites gives, a Computed field names outcome columns, and each computed header and computed outcome parses as FEEL, by `expressions.py`, its kinds agreeing; a column whose fact its file's Facts section declares tests values of its Type, `null` only where it may be absent, and takes no Input Values item, a record breaking the Fact's checks giving its column no Type and no values; a Facts record is judged against its Type only once its Type is one FEEL names, and its name is a fact's name opening with no word FEEL keeps, a boolean fact's a question, its Values are FEEL's unary tests naming no fact, or, on a string fact, the citation of a closed set's record section or its keyed Basic Table, never empty or written plain, its Type a type FEEL names, and its Decimal Places, on a number or a function giving one, a whole number or a fact its file declares, and its Derivation, on a function alone, a FEEL function, and its Initial Value a FEEL expression of its Type, judged with its file's facts in scope; each Input Values item is a condition's header, a colon, and FEEL's unary tests naming no fact, never empty or written plain, an item in a form the checks do not read leaving its column's coverage to the reading audit, `null` among them where it is given, a question taking none, its values being true and false; no cell lies outside its column's values, and, where every condition gives them, no Default Output stands in and the hit policy takes one row's outcome, every case matches a row, an absent value matched as DMN matches it; in a table of two or more rows, no condition column holds one and the same cell in every row, `-` in each reported, and one test in each where the table takes one row's outcome and gives no Default Output, a configured instance's columns aside; a table any of whose cells tests against a fact, or tests in a form other than those the section lists, is listed for the reading audit, which rows a case reaches and whether every case is matched being read; a First table gives no Default Output; every row gives some case its outcome, none having every case it matches taken by a row ahead of it under First or Priority; under Unique no case matches two rows, under Any two rows a case matches give one outcome, under Priority and Output order its Output Values are given, each item an outcome column's header, a colon and a quoted list, and hold every outcome, and under no other policy are they given; a Default Output is one value for one outcome column, and an item for each of several, its header, a colon and its value; and an aggregating Collect has one outcome column, of numbers but for a count | `specs/methodology/modeling-constructs.md § Constructs § Decision Table`, `specs/methodology/modeling-constructs.md § Defining Constructs § Declaring a Construct § Fact` |
| Every FEEL expression, every cell's and value list's unary tests and every guard of an exclusive choice parse by FEEL's whole grammar, in `expressions.py`, given the names in scope where its construct has them, a guard in another of FEEL's forms judged for its form alone and its names read: a name opening with a word FEEL keeps, a name no fact, binding or function names, a value of one known kind combined with another, a path into a value holding no part of that name, a call of a function neither FEEL builds in nor the canon's functions hold, or giving it a number of arguments none of its signatures takes, or giving a parameter of the canon's held to values a quoted value outside them, a minus before what is neither a number nor a duration, a filter whose test is neither a yes or no nor a place, and an `@` value in no form a date, a time or a duration has, each reported; and the script's copies of FEEL's built-in functions and of the words it keeps match their homes, the functions' table row by row, each one's name, what it takes and what it gives, in order, and which take a list's items as arguments, and the list of the words FEEL keeps word for word; and the script's copy of the canon's functions matches their table row by row, each one's name, what it takes, what it gives and the values a parameter is held to, in order, each body a FEEL expression giving what its row gives with its parameters in scope and calling no function at or after its own row, its groups' tables read in order | `specs/methodology/expressions.md § Expressions § FEEL § Its Values`, `specs/methodology/expressions.md § Expressions § FEEL § Names`, `specs/methodology/expressions.md § Expressions § FEEL § Its Expressions`, `specs/methodology/expressions.md § Expressions § FEEL § Unary Tests`, `specs/methodology/expressions.md § Expressions § FEEL § Arithmetic and Time`, `specs/methodology/expressions.md § Expressions § FEEL § Its Functions`, `specs/methodology/expressions.md § Expressions § FEEL § The Canon's Functions` |
| A DAG, its names, dependencies, cycles, guards, timeouts and tolerated cells checked in its file and the rest across files, has a Runs When field, its citations naming each DAG whose task's work cites it and each State Machine whose state's description does, and no other; its tasks are named uniquely, free of a comma and the word `and` and not ending in `ended`; each Reads item is a fact's name, a colon and a citation; each work is `none`, `none, leaving` facts the file declares or the DAG's Reads cites, or a citation resolving to an Algorithm, a Decision Table or a DAG whole, no part of one, a Decision Table's outcome columns facts of either, and no DAG holds itself through the tasks it cites; each dependency names a task it holds, its ` ended` aside, and no task depends on itself, directly or through others; `ended` is waited for only of a task that can end other than done, able to fail, its work an Algorithm or a DAG or its timeout not `none`, to be skipped, its guard not `none`, or to be unreached, a task it waits for to be done able to fail or be unreached, and `Yes` tolerated only of one that can fail; each guard is a FEEL boolean, each timeout a FEEL duration literal or a declared fact of a duration type and each tolerated `Yes` or `No`, the first two judged with its file's facts and those its Reads cites in scope and every problem the expression check gives reported, and a Guard or a Timeout column has some cell that is not `none` and a Tolerated column some cell that is `Yes`; no two tasks free at once give one fact, an Algorithm's Output, a Decision Table's outcomes, a nested DAG's tasks' gives or what a `none` leaves, or read, by work or guard, a nested DAG reading what its tasks read less what they give, one the other gives, no task reads a fact a task after it gives without reading it, and a fact read that some task before the reader gives, none of them surely, a sure giver unguarded, not reached through a dependency `ended` and, within a nested DAG, neither tolerated nor waiting to be done, directly or through others, for a task that is, an Output the work's Inputs also name given surely by any task, a nested DAG's tasks' works' among them, is declared May Be Absent, its record read in the DAG's file, through its Reads, or in the file of the work reading it; an Algorithm a task's work cites has the DAG among the runners its Runs When must name | `specs/methodology/modeling-constructs.md § Constructs § DAG` |
| An Algorithm, checked whole once across files, its Precision a whole number above zero and below 34 and its Rounding Mode one of the modes `specs/methodology/expressions.md` names or a fact it knows whose Values hold only modes, one read by name alone listed for reading, declares Inputs, each item a fact's name or a name, a colon and a citation, Output, each item a fact's name set by a computation, given by a run or gathered by a loop, or one its Inputs also name, and Runs When, its citations naming each construct running it and no other, an Algorithm whose run cites it, a State Machine whose Effect cell or state's description cites it, a DAG whose task's work cites it or a Decision Table whose computed outcome cites it, a citation of a step or a row running nothing; its steps run from 1 in order, each a computation, a run, a loop over a list, a comparison or work, no work citing an Algorithm or a Decision Table whole; each jump is written `Go to step` in those letters and names by its number a step the table holds, a step opening `If` is written in a comparison's form with one `; otherwise, ` and a branch going forward, its condition a FEEL boolean expression, no branch a loop, a step that is no comparison holds no `; otherwise,` and never goes back, each branch holds one jump at most, each jump and each `End` ends its branch, an `End` with no words after it, and its last step, and each branch of it, ends or jumps; a computation is `Set` a fact, or a part reached by names joined by `.` and through no list, `to` a FEEL expression of the kind the fact or part holds, a comparison whose only work is setting one fact reported; a run is `Run`, the citation of an Algorithm or a Decision Table and nothing else, ` with {input} as {expression}` for each fact it names, each one the construct takes, an Algorithm its Inputs and a Decision Table its conditions' facts, the facts of value its computed headers and outcomes name, a function they call being its own, and its Reads, each of the kind its record types, and `, giving` what it gives, each an Output or an outcome of the construct, `as` a fact where it writes to another name, every fact it takes given or known; a loop over a list is written in its form, its list a list, judged with the loops holding it in scope, its order `by` a FEEL expression and `ascending` or `descending`, `in any order`, `in an order the system leaves open` or `at once`, a pass `at once` setting by a computation, a run or a loop only its item and what it gathers, its body the steps after it, never the table's last, within any body holding it, entered from its loop alone and left at `End` alone; and a step going back, or a run recurring through the Algorithms and Decision Tables it runs, has a Terminates cell, a FEEL expression giving a number or the citation of a Constraint some construct enforces, and no other step has one, the column written only where some step needs it, every expression judged by `expressions.py` with the step's facts in scope | `specs/methodology/modeling-constructs.md § Constructs § Algorithm` |
| A Constraint, checked once across files, has in each row a rule in a form FEEL has, giving a yes or no, judged with its file's facts and those its Reads cites in scope, each Reads item a fact's name, a colon and a citation, and, after or before an Algorithm, or a transition whose Effect runs one, that Algorithm's Inputs and, after it, its Output, before a DAG what the work of its first tasks takes and after it what the work of its tasks takes and gives, an Algorithm's, a Decision Table's, a nested DAG's or what a `none` leaves, naming no fact nothing declares, combining no values of two kinds and reaching no part a fact does not hold; an Applies To that is `always`, or `after` or `before` a citation resolving to an Algorithm or a DAG whole, to a transition named in a State Machine's Transitions table, or to a section that declares no construct and holds no records; and an Enforced By that is citations joined by `and`, which the citation checks resolve, or `nothing:` and words, the latter listed as a warning, never a finding, an Enforced By opening `nothing` in any other spelling reported | `specs/methodology/modeling-constructs.md § Constructs § Constraint` |
| An Algorithm's steps and an Enforced By's opening value are read with the contents of their code spans set aside, as literal text, so a jump, a separator, an `End` or `nothing:` quoted there is never read as the text's own; a citation is read as written | `specs/methodology/spec-style.md § Literal Text` |
| A Name column opens a table exactly where a part of it is cited, by Name, from outside its construct's section | `specs/methodology/modeling-constructs.md § Constructs § Keyed Construct § Part Identifier` |
| Each definition under `specs/methodology/modeling-constructs.md § Constructs` gives the Modifier, Extends and Implements the script's copy of it holds, its Modifier `Abstract` or `Interface`, its Extends citing one definition whose section comes before its own, multiple only for an interface extending interfaces, and given by every definition but Construct and an interface, and its Implements citing interfaces whose sections come before its own; no definition gives a field or a column a definition it extends gives, sets or bounds a member of no interface it implements, its bases' and the interfaces they extend among them, or sets a member a definition it extends sets; every Construct, Extends and Implements field cites its definition; every member Specified By Definition, the Locator among them, set by each concrete definition implementing its interface, and none Specified By Instance set by a definition; every interface's section after Construct's; no Modifier, Implements or member Specified By Definition stands outside a definition's section, but for the Modifier a record type's declaration gives; and no Construct field names an abstract definition or an interface | `specs/methodology/modeling-constructs.md § Defining Constructs`, `specs/methodology/modeling-constructs.md § Defining Constructs § Inheritance`, `specs/methodology/modeling-constructs.md § Defining Constructs § Modifiers`, `specs/methodology/modeling-constructs.md § Defining Constructs § Interfaces and Members`, `specs/methodology/modeling-constructs.md § Defining Constructs § References and Names`, `specs/methodology/modeling-constructs.md § Constructs § Keyed Construct` |

**Scope.** The script's scope is the files that `specs/methodology/scope.md § What Spec of Record Governs` names, the working files aside. Those files are the root `AGENTS.md`, the documentation, every file under `specs/`, found by one walk of the index tables from `specs/index.md` down, and each skill that `specs/methodology/skills.md` registers: its `SKILL.md`, its references and its scripts, with the code the skills' scripts share under `.ai/skills/lib/`. The documentation is `README.md` and the files under `docs/`. Code is aside too, since the skill does not read it. The working files are aside because they legitimately carry citations to things since moved or removed, and the script's pre-pass reads none of them. The Working-file form audit reads `.ai/follow-ups.md` instead, and runs the checks `specs/methodology/modeling-constructs.md § Fields` gives a block of fields and the check `specs/methodology/spec-style.md § Blank Lines` gives a blank line over it in its own run alone. `.ai/skills/design-specs/` and `.ai/skills/implement-specs/` check the plans they write. No check of this script reads the skills' output under `.ai/tmp/`, because that output is reports rather than rules. The reports a design's log names are read instead by the `--log-entry`, `--check-handed-back` and `--check-settled-report` of `.ai/skills/design-specs/` and `.ai/skills/implement-specs/`, as `specs/methodology/working-files/main.md § A Check's Report § What the Design Script Checks` has them checked. The check keeping the working files out of version control reads the project's `.gitignore`. `--list-candidates` lists places for the Ordinals and counts audit, the Markup audit, the Glossary terms audit, the Construct choice and form audit, the Finished style audit and the Agent agnostic audit to read. For the Skill form audit, it lists an unregistered skill whose `SKILL.md` cites the methodology's rules, and a registered skill's script importing a module that is neither in the standard library, nor one of the skill's own helpers, nor the code the skills share. It also lists a skill's long sentence of chained clauses, and a path into the application specs in a skill. An audit whose unit names the script's scope for a full run uses this scope. The candidates print apart from the findings, since a list of places to read decides nothing (`specs/methodology/scope.md § Rules and Skills`).

## Operating rules carried out by a step

Each operating rule that leaves no trace in the files the audits read is carried out by the steps applying it, and each of those steps gives it a point-of-use citation (`specs/methodology/scope.md § Rules and Skills`). Each failure a skipped step leaves is a Skipped Step record (`specs/methodology/scope.md § Rules and Skills § Skipped Step`).

### Skipped Steps

**Records:**
  - **Failure:** a fact placed, cited or formed against its rule \
    **Sections:**
      - `specs/AGENTS.md § Writing specs`

    **Rule:** `specs/AGENTS.md § Writing specs` \
    **Leaves:** the fact, placed, cited or formed against its rule \
    **Caught By:**
      - `§ The audits`

  - **Failure:** a direct edit made without the user's approval \
    **Sections:**
      - `specs/AGENTS.md § Design, Refactor, Refine`

    **Rule:** `specs/AGENTS.md § Design, Refactor, Refine § Direct Edits` \
    **Leaves:** nothing in the files \
    **Caught By:**
      - the user

  - **Failure:** a new branch made without the user's approval \
    **Sections:**
      - `specs/AGENTS.md § Design, Refactor, Refine`

    **Rule:** `specs/AGENTS.md § Design, Refactor, Refine § A New Branch` \
    **Leaves:** nothing in the files \
    **Caught By:**
      - the user

  - **Failure:** a review's entry naming no model and effort \
    **Sections:**
      - `specs/AGENTS.md § Design, Refactor, Refine`

    **Rule:** `specs/AGENTS.md § Design, Refactor, Refine § Each Review's Model and Effort` \
    **Leaves:** a log entry naming no model and reasoning effort, refused as it is appended \
    **Caught By:**
      - `.ai/skills/design-specs/` `--log-entry`
      - `.ai/skills/implement-specs/` `--log-entry`
      - `specs/AGENTS.md § Design, Refactor, Refine § Who Checks What and Why § Check Roles [Check: the validation review]`

  - **Failure:** a review's model and effort not offered \
    **Sections:**
      - `specs/AGENTS.md § Design, Refactor, Refine`

    **Rule:** `specs/AGENTS.md § Design, Refactor, Refine § Each Review's Model and Effort` \
    **Leaves:** nothing in the files \
    **Caught By:**
      - the user

  - **Failure:** a design revised past a run the user did not have go on \
    **Sections:**
      - `specs/AGENTS.md § Design, Refactor, Refine`

    **Rule:** `specs/AGENTS.md § Design, Refactor, Refine § Converging, or Not § The Runs` \
    **Leaves:** the design's log, whose entries show the rounds of the run \
    **Caught By:**
      - the user

  - **Failure:** a step stated without its reach researched \
    **Sections:**
      - `specs/AGENTS.md § Design, Refactor, Refine`

    **Rule:** `specs/AGENTS.md § Design, Refactor, Refine § Measure Twice, Cut Once § Research` \
    **Leaves:** the step patched \
    **Caught By:**
      - `specs/AGENTS.md § Design, Refactor, Refine § Who Checks What and Why § Check Roles [Check: the adversarial review]`
      - `specs/AGENTS.md § Design, Refactor, Refine § Who Checks What and Why § Check Roles [Check: the post-apply review]`

  - **Failure:** a passage written without zooming out \
    **Sections:**
      - `specs/AGENTS.md § Design, Refactor, Refine`

    **Rule:** `specs/AGENTS.md § Design, Refactor, Refine § Measure Twice, Cut Once § The Zoom-Out` \
    **Leaves:** the passage patched \
    **Caught By:**
      - `specs/AGENTS.md § Design, Refactor, Refine § Who Checks What and Why § Check Roles [Check: the adversarial review]`
      - `specs/AGENTS.md § Design, Refactor, Refine § Who Checks What and Why § Check Roles [Check: the post-apply review]`

  - **Failure:** a moved step not taken through Design, Refactor, Refine \
    **Sections:**
      - `specs/AGENTS.md § Design, Refactor, Refine`

    **Rule:** `specs/AGENTS.md § Design, Refactor, Refine § Measure Twice, Cut Once § The Order of a Design's Parts` \
    **Leaves:** nothing the script reads \
    **Caught By:**
      - `specs/AGENTS.md § Design, Refactor, Refine § Who Checks What and Why § Check Roles [Check: the adversarial review]`

  - **Failure:** a finding left unmarked \
    **Sections:**
      - `specs/AGENTS.md § Design, Refactor, Refine`

    **Rule:** `specs/AGENTS.md § Design, Refactor, Refine § Weighing a Review's Findings` \
    **Leaves:** a finding in the round's report holding no mark \
    **Caught By:**
      - `specs/AGENTS.md § Design, Refactor, Refine § Settling a Round`

  - **Failure:** a kept finding without its rationale or possible fix \
    **Sections:**
      - `specs/AGENTS.md § Design, Refactor, Refine`

    **Rule:** `specs/AGENTS.md § Design, Refactor, Refine § Weighing a Review's Findings` \
    **Leaves:** a kept finding in the round's report holding no rationale or no possible fix, a possible fix in neither of its forms, or a dropped finding holding no reason \
    **Caught By:**
      - `specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: report-in-its-form]`

  - **Failure:** a finding judged wrong raised again with no new argument \
    **Sections:**
      - `specs/AGENTS.md § Design, Refactor, Refine`

    **Rule:** `specs/AGENTS.md § Design, Refactor, Refine § Weighing a Review's Findings` \
    **Leaves:** the finding in the round's report \
    **Caught By:**
      - `specs/AGENTS.md § Design, Refactor, Refine § Settling a Round`

  - **Failure:** findings weighed, or the earlier reports read, before all are collected \
    **Sections:**
      - `specs/AGENTS.md § Design, Refactor, Refine`

    **Rule:** `specs/AGENTS.md § Design, Refactor, Refine § Weighing a Review's Findings` \
    **Leaves:** the report's Reading, showing what the review read \
    **Caught By:**
      - the user

  - **Failure:** an audit's finding left untriaged \
    **Sections:**
      - `specs/AGENTS.md § Design, Refactor, Refine`

    **Rule:** `specs/AGENTS.md § Design, Refactor, Refine § An Audit` \
    **Leaves:** nothing the script reads \
    **Caught By:**
      - the user

  - **Failure:** a self-review short of its reading and questions \
    **Sections:**
      - `specs/AGENTS.md § Design, Refactor, Refine`

    **Rule:** `specs/AGENTS.md § Design, Refactor, Refine § Measure Twice, Cut Once § The Self-Review` \
    **Leaves:** nothing the script reads, a review then finding what the self-review would have caught \
    **Caught By:**
      - the user

  - **Failure:** a round's change proven by rereading it alone \
    **Sections:**
      - `specs/AGENTS.md § Design, Refactor, Refine`

    **Rule:** `specs/AGENTS.md § Design, Refactor, Refine § Settling a Round § The Round at Its Causes § Change and Prove` \
    **Leaves:** nothing the script reads \
    **Caught By:**
      - the user

  - **Failure:** something the user says at the apply acted on untold apart \
    **Sections:**
      - `specs/AGENTS.md § Design, Refactor, Refine`

    **Rule:** `specs/AGENTS.md § Design, Refactor, Refine § Measure Twice, Cut Once § What the User Says at the Apply` \
    **Leaves:** nothing the script reads \
    **Caught By:**
      - the user

  - **Failure:** a script changed with no differential test \
    **Sections:**
      - `specs/AGENTS.md § Design, Refactor, Refine`

    **Rule:** `specs/methodology/working-files/main.md § A Check's Report § Kinds of Builder Check` \
    **Leaves:** a self-review's report recording no differential test of the script \
    **Caught By:**
      - `specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: builder-checks-required]`

  - **Failure:** a self-review over applied work of a `canon-specs` or `application-specs` design with no construct choice recorded \
    **Sections:**
      - `specs/AGENTS.md § Design, Refactor, Refine`

    **Rule:** `specs/methodology/working-files/main.md § A Check's Report § Kinds of Builder Check` \
    **Leaves:** a self-review's report over applied work recording no `construct choice` Builder Check \
    **Caught By:**
      - `specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: builder-checks-required]`

  - **Failure:** a draft on goals or a frame the user has not agreed \
    **Sections:**
      - `specs/AGENTS.md § Design, Refactor, Refine`

    **Rule:** `specs/AGENTS.md § Design, Refactor, Refine § The Goals and the Frame` \
    **Leaves:** nothing the script reads \
    **Caught By:**
      - the user

  - **Failure:** a settlement stating no cause or no miss \
    **Sections:**
      - `specs/AGENTS.md § Design, Refactor, Refine`

    **Rule:** `specs/AGENTS.md § Design, Refactor, Refine § Settling a Round § The Round at Its Causes § Propose` \
    **Leaves:** a round's Settlement holding no Cause, or a flaw's Cause holding no Miss \
    **Caught By:**
      - `specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: report-in-its-form]`

  - **Failure:** a round settled finding by finding \
    **Sections:**
      - `specs/AGENTS.md § Design, Refactor, Refine`

    **Rule:** `specs/AGENTS.md § Design, Refactor, Refine § Settling a Round § The Round at Its Causes` \
    **Leaves:** the round's Settlement, showing each finding settled where it sits \
    **Caught By:**
      - `specs/AGENTS.md § Design, Refactor, Refine § Who Checks What and Why § Check Roles [Check: the adversarial review]`
      - `specs/AGENTS.md § Design, Refactor, Refine § Who Checks What and Why § Check Roles [Check: the post-apply review]`
      - the user

  - **Failure:** a round settled by more than the least change \
    **Sections:**
      - `specs/AGENTS.md § Design, Refactor, Refine`

    **Rule:** `specs/AGENTS.md § Design, Refactor, Refine § Settling a Round § The Round at Its Causes § Propose` \
    **Leaves:** the round's Settlement, showing a change past the least of the revisions at its causes \
    **Caught By:**
      - `specs/AGENTS.md § Design, Refactor, Refine § Who Checks What and Why § Check Roles [Check: the adversarial review]`
      - `specs/AGENTS.md § Design, Refactor, Refine § Who Checks What and Why § Check Roles [Check: the post-apply review]`
      - the user

  - **Failure:** a change settling short given no reason \
    **Sections:**
      - `specs/AGENTS.md § Design, Refactor, Refine`

    **Rule:** `specs/AGENTS.md § Design, Refactor, Refine § Settling a Round § Order and Lineage` \
    **Leaves:** a Settlement holding no Departure Reason where its change settles less than the finding's possible fix reaches, which no field the script compares shows, a departure in verdict, in where a finding lies or in lineage being the script's `departures-reasoned` \
    **Caught By:**
      - `specs/AGENTS.md § Design, Refactor, Refine § Who Checks What and Why § Check Roles [Check: the adversarial review]`
      - `specs/AGENTS.md § Design, Refactor, Refine § Who Checks What and Why § Check Roles [Check: the post-apply review]`
      - the user

  - **Failure:** a change proposed before the misses are asked \
    **Sections:**
      - `specs/AGENTS.md § Design, Refactor, Refine`

    **Rule:** `specs/AGENTS.md § Design, Refactor, Refine § Settling a Round § The Round at Its Causes § Group` \
    **Leaves:** nothing a record dates, a report holding what was read and never when \
    **Caught By:**
      - `specs/AGENTS.md § Design, Refactor, Refine § Who Checks What and Why § Check Roles [Check: the adversarial review]`
      - `specs/AGENTS.md § Design, Refactor, Refine § Who Checks What and Why § Check Roles [Check: the post-apply review]`
      - the user

  - **Failure:** a user's answer to a call left unrecorded \
    **Sections:**
      - `specs/AGENTS.md § Design, Refactor, Refine`

    **Rule:** `specs/AGENTS.md § Design, Refactor, Refine § Who Decides` \
    **Leaves:** nothing the script reads \
    **Caught By:**
      - the user

  - **Failure:** an applied Decision Table or State Machine left untraced \
    **Sections:**
      - `specs/AGENTS.md § Design, Refactor, Refine`

    **Rule:** `specs/AGENTS.md § Design, Refactor, Refine § Measure Twice, Cut Once § Tracing a Mechanism` \
    **Leaves:** a self-review's report over applied work holding no Trace of a table or a machine a section the diff changed holds, or a Trace leaving a path out \
    **Caught By:**
      - `specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: traces-name-their-paths]`

  - **Failure:** another mechanism left untraced \
    **Sections:**
      - `specs/AGENTS.md § Design, Refactor, Refine`

    **Rule:** `specs/AGENTS.md § Design, Refactor, Refine § Measure Twice, Cut Once § Tracing a Mechanism` \
    **Leaves:** a self-review's report showing the traces it records \
    **Caught By:**
      - `specs/AGENTS.md § Design, Refactor, Refine § Who Checks What and Why § Check Roles [Check: the adversarial review]`
      - `specs/AGENTS.md § Design, Refactor, Refine § Who Checks What and Why § Check Roles [Check: the post-apply review]`
      - the user

  - **Failure:** an approval ending the review logged as no plan-approval entry \
    **Sections:**
      - `specs/AGENTS.md § Design, Refactor, Refine`

    **Rule:** `specs/AGENTS.md § Design, Refactor, Refine § The Adversarial Review § The Plan's Approval` \
    **Leaves:** a log holding no `plan-approval` entry \
    **Caught By:**
      - the user

  - **Failure:** a set of steers closed with no steer entry \
    **Sections:**
      - `specs/methodology/working-files/main.md § Steering Decision § When a Steer Is Recorded`

    **Rule:** `specs/methodology/working-files/main.md § Steering Decision § When a Steer Is Recorded` \
    **Leaves:** a Steering Decision no `steer` entry names once its set has closed \
    **Caught By:**
      - the user

  - **Failure:** a steer acted on before its set closes \
    **Sections:**
      - `specs/AGENTS.md § Design, Refactor, Refine`

    **Rule:** `specs/AGENTS.md § Design, Refactor, Refine § Who Decides § A Set of Steers` \
    **Leaves:** a design rebuilt, or a round ended, from a steer whose set's `steer` entry stands later, or a set closed with a question of the builder's still open, which the log shows only as the order of the work \
    **Caught By:**
      - the user

  - **Failure:** work running at a set's close stopped or continued without the user's call \
    **Sections:**
      - `specs/AGENTS.md § Design, Refactor, Refine`

    **Rule:** `specs/AGENTS.md § Design, Refactor, Refine § Who Decides § A Set of Steers` \
    **Leaves:** a set's entry whose Running Work names no call on work then running, or a check cut short that no Cuts Short names \
    **Caught By:**
      - the user

  - **Failure:** a design revised past a completed run with no reassessment entry \
    **Sections:**
      - `specs/AGENTS.md § Design, Refactor, Refine`

    **Rule:** `specs/AGENTS.md § Design, Refactor, Refine § Converging, or Not § The Runs` \
    **Leaves:** a log holding no `reassessment` entry after the run's last round \
    **Caught By:**
      - the user

  - **Failure:** a nit judged harmless that harms the work \
    **Sections:**
      - `specs/AGENTS.md § Design, Refactor, Refine`

    **Rule:** `specs/AGENTS.md § Design, Refactor, Refine § Converging, or Not § A Nit` \
    **Leaves:** nothing the script reads \
    **Caught By:**
      - the user
      - `specs/AGENTS.md § Design, Refactor, Refine § Who Checks What and Why § Check Roles [Check: the post-apply review]`

  - **Failure:** goals or a frame letting findings in left unrevised \
    **Sections:**
      - `specs/AGENTS.md § Design, Refactor, Refine`

    **Rule:** `specs/AGENTS.md § Design, Refactor, Refine § Settling a Round § The Round at Its Causes § Propose` \
    **Leaves:** nothing in the files \
    **Caught By:**
      - the user

  - **Failure:** a Frame Outcome naming no goal \
    **Sections:**
      - `specs/AGENTS.md § Design, Refactor, Refine`

    **Rule:** `specs/methodology/working-files/main.md § A Design Document § Frame Outcome` \
    **Leaves:** a Frame Outcome whose Goals names no goal \
    **Caught By:**
      - `specs/AGENTS.md § Design, Refactor, Refine § Who Checks What and Why § Check Roles [Check: the validation review]`

  - **Failure:** an Approach resting on a goal it does not cite \
    **Sections:**
      - `specs/AGENTS.md § Design, Refactor, Refine`

    **Rule:** `specs/methodology/working-files/main.md § A Design Document` \
    **Leaves:** an Approach citing no goal \
    **Caught By:**
      - `specs/AGENTS.md § Design, Refactor, Refine § Who Checks What and Why § Check Roles [Check: the adversarial review]`

  - **Failure:** a review reading another working file \
    **Sections:**
      - `specs/AGENTS.md § Design, Refactor, Refine`

    **Rule:** `specs/AGENTS.md § Design, Refactor, Refine § Who Checks What and Why § What a Review Reads` \
    **Leaves:** nothing in the files, but where the read surfaces in a finding or a citation in the review's report \
    **Caught By:**
      - `specs/AGENTS.md § Design, Refactor, Refine § Settling a Round`

  - **Failure:** a marked finding anchored in nothing, or in what the design does not hold \
    **Sections:**
      - `specs/AGENTS.md § Design, Refactor, Refine`

    **Rule:** `specs/methodology/working-files/main.md § A Check's Report § Finding` \
    **Leaves:** a marked finding naming no goal, Frame Outcome or step Objective and citing no rule it breaks, or naming one the design does not hold \
    **Caught By:**
      - `specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: findings-anchored-in-the-design]`

  - **Failure:** a reviewer's kept finding dropped on the builder's own call \
    **Sections:**
      - `specs/AGENTS.md § Design, Refactor, Refine`

    **Rule:** `specs/AGENTS.md § Design, Refactor, Refine § Settling a Round § The Test` \
    **Leaves:** a dropped Settlement departing from its writer's kept verdict, holding a Departure Reason and no User Decision, which no field the script compares tells from a drop the user made \
    **Caught By:**
      - `specs/AGENTS.md § Design, Refactor, Refine § Who Checks What and Why § Check Roles [Check: the adversarial review]`
      - the user

  - **Failure:** a Settlement missing its indicators \
    **Sections:**
      - `specs/AGENTS.md § Design, Refactor, Refine`

    **Rule:** `specs/AGENTS.md § Design, Refactor, Refine § Settling a Round § The Test` \
    **Leaves:** a Settlement holding no Required By, or not the Justifying Goals or Justifying Rules it names, or, where its finding is kept, no Fix Authority \
    **Caught By:**
      - `specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: report-in-its-form]`
      - `specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: settlements-justified]`

  - **Failure:** a tertiary fix made without the user's call \
    **Sections:**
      - `specs/AGENTS.md § Design, Refactor, Refine`

    **Rule:** `specs/AGENTS.md § Design, Refactor, Refine § Settling a Round § Order and Lineage` \
    **Leaves:** a tertiary Settlement, or one whose change reaches a tertiary place, holding a Fix Authority other than the user's or no User Decision \
    **Caught By:**
      - `specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: settlements-justified]`
      - `specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: orders-follow-their-lineage]`

  - **Failure:** an order left unassigned or made shallower \
    **Sections:**
      - `specs/AGENTS.md § Design, Refactor, Refine`

    **Rule:** `specs/AGENTS.md § Design, Refactor, Refine § Settling a Round § Order and Lineage` \
    **Leaves:** a Settlement or a Changed Place holding no Order, or one shallower than its lineage gives \
    **Caught By:**
      - `specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: report-in-its-form]`
      - `specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: orders-follow-their-lineage]`

  - **Failure:** a departure given no reason \
    **Sections:**
      - `specs/AGENTS.md § Design, Refactor, Refine`

    **Rule:** `specs/AGENTS.md § Design, Refactor, Refine § Settling a Round § Order and Lineage` \
    **Leaves:** a Settlement departing from a finding it settles, in verdict, in where it lies or in lineage, holding no Departure Reason \
    **Caught By:**
      - `specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: departures-reasoned]`

  - **Failure:** a finding settled or dropped against the test \
    **Sections:**
      - `specs/AGENTS.md § Design, Refactor, Refine`

    **Rule:** `specs/AGENTS.md § Design, Refactor, Refine § Settling a Round § The Test` \
    **Leaves:** the round's Settlement, showing each finding it settles and drops \
    **Caught By:**
      - `specs/AGENTS.md § Design, Refactor, Refine § Who Checks What and Why § Check Roles [Check: the adversarial review]`
      - the user

  - **Failure:** a review observation counted \
    **Sections:**
      - `specs/AGENTS.md § Design, Refactor, Refine`

    **Rule:** `specs/AGENTS.md § Design, Refactor, Refine § Who Checks What and Why § What a Review Reads` \
    **Leaves:** nothing the script reads \
    **Caught By:**
      - the user

  - **Failure:** a review observation not brought \
    **Sections:**
      - `specs/AGENTS.md § Design, Refactor, Refine`

    **Rule:** `specs/AGENTS.md § Design, Refactor, Refine § Who Decides` \
    **Leaves:** nothing the script reads \
    **Caught By:**
      - the user

  - **Failure:** a user's edit at the apply not confirmed, logged or checked \
    **Sections:**
      - `specs/AGENTS.md § Design, Refactor, Refine`

    **Rule:** `specs/methodology/working-files/main.md § Steering Decision § Telling a Steer Apart § Steer, Direction, Feedback, Other Work or the User's Edit` \
    **Leaves:** a file changed outside the Target that no entry names, or a self-review's report leaving a user's edit unchecked \
    **Caught By:**
      - `.ai/skills/design-specs/` `--check-changed-files`
      - `.ai/skills/implement-specs/` `--check-changed-files`
      - `specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: builder-checks-required]`
      - the user

  - **Failure:** a design's changes read from outside their home \
    **Sections:**
      - `specs/AGENTS.md § Design, Refactor, Refine`

    **Rule:** `specs/methodology/working-files/main.md § A Design Document § Applying and Committing` \
    **Leaves:** a rule reading a design's changes otherwise \
    **Caught By:**
      - `specs/AGENTS.md § Design, Refactor, Refine § Who Checks What and Why § Check Roles [Check: the post-apply review]`
      - `specs/AGENTS.md § Design, Refactor, Refine § Who Checks What and Why § Check Roles [Check: an audit]`

  - **Failure:** something the user approves shown without its summary \
    **Sections:**
      - `specs/AGENTS.md § Design, Refactor, Refine`

    **Rule:** `specs/AGENTS.md § Design, Refactor, Refine § What the User Is Shown` \
    **Leaves:** nothing in the files \
    **Caught By:**
      - the user

  - **Failure:** the reach and wording checks left unrun \
    **Sections:**
      - `specs/AGENTS.md § Design, Refactor, Refine`

    **Rule:** `specs/AGENTS.md § Design, Refactor, Refine § Measure Twice, Cut Once § The Self-Review` \
    **Leaves:** nothing the script reads, the retired wording or the file outside the Target left behind \
    **Caught By:**
      - `specs/AGENTS.md § Design, Refactor, Refine § Who Checks What and Why § Check Roles [Check: the post-apply review]`

  - **Failure:** the work's checks left unrun over the work \
    **Sections:**
      - `specs/AGENTS.md § Design, Refactor, Refine`

    **Rule:** `specs/AGENTS.md § Design, Refactor, Refine § Who Checks What and Why § The Scope a Check Runs Over` \
    **Leaves:** nothing the script reads, the breach the work caused left in the files \
    **Caught By:**
      - `specs/AGENTS.md § Design, Refactor, Refine § Who Checks What and Why § Check Roles [Check: the post-apply review]`
      - `specs/AGENTS.md § Design, Refactor, Refine § Who Checks What and Why § Check Roles [Check: an audit]`

  - **Failure:** the construct checks left unrun at the self-review \
    **Sections:**
      - `specs/AGENTS.md § Design, Refactor, Refine`

    **Rule:** `specs/AGENTS.md § Design, Refactor, Refine § Measure Twice, Cut Once § The Self-Review` \
    **Leaves:** a construct's gap or overlap in the applied text carried to the post-apply review \
    **Caught By:**
      - `specs/AGENTS.md § Design, Refactor, Refine § Who Checks What and Why § Check Roles [Check: the post-apply review]`
      - `§ The audits [Audit: Construct choice and form]`

  - **Failure:** What Sets the Work not read again on resuming \
    **Sections:**
      - `specs/AGENTS.md § Design, Refactor, Refine`

    **Rule:** `specs/AGENTS.md § Design, Refactor, Refine § Reading Fresh` \
    **Leaves:** nothing in the files \
    **Caught By:**
      - the user

  - **Failure:** findings grouped before the earlier reports are read \
    **Sections:**
      - `specs/AGENTS.md § Design, Refactor, Refine`

    **Rule:** `specs/AGENTS.md § Design, Refactor, Refine § Settling a Round § The Round at Its Causes § Group` \
    **Leaves:** nothing in the files \
    **Caught By:**
      - the user

  - **Failure:** settling reads missing a finding's evidence \
    **Sections:**
      - `specs/AGENTS.md § Design, Refactor, Refine`

    **Rule:** `specs/AGENTS.md § Design, Refactor, Refine § Settling a Round § The Round at Its Causes § Group` \
    **Leaves:** a round's Settling Reads, with the Read Assessments the log's handed-off judgments hold, leaving out a place a marked finding's Evidence names \
    **Caught By:**
      - `specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: settling-reads-cover-the-evidence]`

  - **Failure:** a self-review's reads missing a miss's place \
    **Sections:**
      - `specs/AGENTS.md § Design, Refactor, Refine`

    **Rule:** `specs/AGENTS.md § Design, Refactor, Refine § Measure Twice, Cut Once § The Self-Review` \
    **Leaves:** a self-review's Reads leaving out a place a Miss of the phase names \
    **Caught By:**
      - `specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: reads-cover-the-misses]`

  - **Failure:** a settlement naming no earlier report \
    **Sections:**
      - `specs/AGENTS.md § Design, Refactor, Refine`

    **Rule:** `specs/AGENTS.md § Design, Refactor, Refine § Reading the Earlier Reports` \
    **Leaves:** a round's Settlement leaving out an earlier report of its phase \
    **Caught By:**
      - `specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: earlier-reports-listed]`

  - **Failure:** a tactical fix short of its Search's matches \
    **Sections:**
      - `specs/AGENTS.md § Design, Refactor, Refine`

    **Rule:** `specs/AGENTS.md § Design, Refactor, Refine § Settling a Round § The Round at Its Causes § Propose` \
    **Leaves:** a tactical fix made at fewer than every place its Search matched \
    **Caught By:**
      - `specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: tactical-fixes-cover-their-searches]`
      - `specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: searches-cover-their-matches]`

  - **Failure:** a tactical fix made with no Search \
    **Sections:**
      - `specs/AGENTS.md § Design, Refactor, Refine`

    **Rule:** `specs/methodology/working-files/main.md § A Check's Report § Proposed Change` \
    **Leaves:** a Cause's Proposed Change of the Kind tactical fix naming no Search \
    **Caught By:**
      - `specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: report-in-its-form]`

  - **Failure:** a Trace or a continuing Cause stating no outcome \
    **Sections:**
      - `specs/AGENTS.md § Design, Refactor, Refine`

    **Rule:** `specs/AGENTS.md § Design, Refactor, Refine § The Goals and the Frame § Whether the Goals and the Frame Name a Mechanism` \
    **Leaves:** a Trace of a self-review before the adversarial review, asked of a mechanism the steps change with no rows, or a Cause continuing an earlier one, stating no outcome of the table \
    **Caught By:**
      - `specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: report-in-its-form]`

  - **Failure:** the goals and frame test left unasked, unrecorded or not borne out \
    **Sections:**
      - `specs/AGENTS.md § Design, Refactor, Refine`

    **Rule:** `specs/AGENTS.md § Design, Refactor, Refine § The Goals and the Frame § Whether the Goals and the Frame Name a Mechanism` \
    **Leaves:** the self-review's report before an adversarial round with no Trace of a mechanism the test reaches, the round's report settling a decision drawing findings again with no Cause continuing an earlier one, or either holding an outcome the goals and the frame do not bear out \
    **Caught By:**
      - `specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: traces-name-their-paths]`
      - `specs/AGENTS.md § Design, Refactor, Refine § Who Checks What and Why § Check Roles [Check: the adversarial review]`
      - the user

  - **Failure:** a researched place left unassessed \
    **Sections:**
      - `specs/AGENTS.md § Design, Refactor, Refine`

    **Rule:** `specs/AGENTS.md § Design, Refactor, Refine § Measure Twice, Cut Once § Research` \
    **Leaves:** a report of research leaving a place a Search matched outside the design document, or a place the builder named, within no Read Assessment's Area \
    **Caught By:**
      - `specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: reads-assessed]`

  - **Failure:** a sweep unrecorded \
    **Sections:**
      - `specs/AGENTS.md § Design, Refactor, Refine`

    **Rule:** `specs/methodology/working-files/main.md § A Design Document` \
    **Leaves:** a Scope recording no method for its sweep \
    **Caught By:**
      - `specs/AGENTS.md § Design, Refactor, Refine § Who Checks What and Why § Check Roles [Check: the adversarial review]`

  - **Failure:** a sweep short of the change's rules and terms \
    **Sections:**
      - `specs/AGENTS.md § Design, Refactor, Refine`

    **Rule:** `specs/AGENTS.md § Design, Refactor, Refine § The Goals and the Frame` \
    **Leaves:** Assessed Areas missing a passage stating part of a rule the change states or a use of a term it defines or redefines \
    **Caught By:**
      - `specs/AGENTS.md § Design, Refactor, Refine § Who Checks What and Why § Check Roles [Check: the adversarial review]`

  - **Failure:** a working file changed by a design's step \
    **Sections:**
      - `specs/methodology/working-files/main.md § The Working Files`

    **Rule:** `specs/methodology/working-files/main.md § The Working Files` \
    **Leaves:** the design's Target naming the working file \
    **Caught By:**
      - `.ai/skills/design-specs/` `--check-target-kind`
      - `.ai/skills/implement-specs/` `--check-target-kind`

  - **Failure:** a design or its records out of their form \
    **Sections:**
      - `specs/methodology/working-files/main.md § A Design Document`
      - `specs/methodology/working-files/main.md § Design Goal`
      - `specs/methodology/working-files/main.md § Design Plan Step`
      - `specs/methodology/working-files/main.md § Design Log Entry`
      - `specs/methodology/working-files/main.md § Retired Phrase`
      - `specs/methodology/working-files/main.md § Steering Decision`
      - `specs/methodology/working-files/main.md § A Stamp`

    **Rule:** `specs/methodology/working-files/main.md § A Design Document` \
    **Leaves:** a design document out of its form \
    **Caught By:**
      - `specs/AGENTS.md § Design, Refactor, Refine § Who Checks What and Why § Check Roles [Check: the validation review]`

  - **Failure:** a design's records out of their record types \
    **Sections:**
      - `specs/methodology/working-files/main.md § Design Goal`
      - `specs/methodology/working-files/main.md § Design Plan Step`
      - `specs/methodology/working-files/main.md § Design Log Entry`
      - `specs/methodology/working-files/main.md § Retired Phrase`
      - `specs/methodology/working-files/main.md § Steering Decision`

    **Rule:** `specs/methodology/modeling-constructs.md § Constructs § Record Form` \
    **Leaves:** a step, a step Objective, a goal, a Frame Outcome, an Assessed Area, a steer, a log entry or a retired phrase out of its record type \
    **Caught By:**
      - `specs/AGENTS.md § Design, Refactor, Refine § Who Checks What and Why § Check Roles [Check: the validation review]`
      - `.ai/skills/design-specs/` `--log-entry`
      - `.ai/skills/implement-specs/` `--log-entry`

  - **Failure:** a logged entry edited, moved or inserted after its event \
    **Sections:**
      - `specs/methodology/working-files/main.md § Design Log Entry`

    **Rule:** `specs/methodology/working-files/main.md § Design Log Entry` \
    **Leaves:** the log, an entry's record of its event changed or standing where its event did not happen \
    **Caught By:**
      - `specs/methodology/working-files/main.md § Design Log Entry § Script Checks [Name: entry-at-the-version-read]`
      - the user

  - **Failure:** a check cut short left unsettled \
    **Sections:**
      - `specs/methodology/working-files/main.md § Design Log Entry § When an Entry Is Appended`

    **Rule:** `specs/methodology/working-files/main.md § Design Log Entry § When an Entry Is Appended` \
    **Leaves:** a Cuts Short naming an entry the log never holds, or a report holding a finding no Settlement settles \
    **Caught By:**
      - `specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: findings-settled-once]`
      - the user

  - **Failure:** a design's own working files left out of the form its apply lands \
    **Sections:**
      - `specs/methodology/working-files/main.md § The Working Files`

    **Rule:** `specs/methodology/working-files/main.md § The Working Files` \
    **Leaves:** the design's working files in a form no longer in force, which its later checks refuse \
    **Caught By:**
      - `specs/AGENTS.md § Design, Refactor, Refine § Who Checks What and Why § Check Roles [Check: the validation review]`
      - `.ai/skills/design-specs/` `--log-entry`
      - `.ai/skills/implement-specs/` `--log-entry`

  - **Failure:** log entries out of their count or their order \
    **Sections:**
      - `specs/methodology/working-files/main.md § Design Log Entry`

    **Rule:** `specs/methodology/working-files/main.md § Design Log Entry` \
    **Leaves:** log entries out of their count or their order \
    **Caught By:**
      - `specs/AGENTS.md § Design, Refactor, Refine § Who Checks What and Why § Check Roles [Check: the validation review]`
      - `.ai/skills/design-specs/` `--log-entry`
      - `.ai/skills/implement-specs/` `--log-entry`

  - **Failure:** a design's dependencies out of sync with the workstack \
    **Sections:**
      - `specs/methodology/working-files/main.md § A Design Document § The Record's Checks`

    **Rule:** `specs/methodology/working-files/main.md § A Design Document § What Blocks What` \
    **Leaves:** a design whose Depends On Designs the workstack does not bear out \
    **Caught By:**
      - `.ai/skills/design-specs/` `--check-workstack`
      - `.ai/skills/implement-specs/` `--check-workstack`

  - **Failure:** a design's Status out of sync with the workstack \
    **Sections:**
      - `specs/methodology/working-files/main.md § A Design Document § The Record's Checks`

    **Rule:** `specs/methodology/working-files/main.md § A Design Document § Blocked and to Revise` \
    **Leaves:** a design whose Status the workstack does not bear out \
    **Caught By:**
      - `.ai/skills/design-specs/` `--check-workstack`
      - `.ai/skills/implement-specs/` `--check-workstack`

  - **Failure:** a design's citation of another file unresolved \
    **Sections:**
      - `specs/methodology/working-files/main.md § A Design Document § The Record's Checks`

    **Rule:** `specs/methodology/sourcing-and-citation.md § Writing a Citation` \
    **Leaves:** a citation of another file that does not resolve \
    **Caught By:**
      - `specs/AGENTS.md § Design, Refactor, Refine § Who Checks What and Why § Check Roles [Check: the adversarial review]`

  - **Failure:** a Target out of its Kind \
    **Sections:**
      - `specs/methodology/working-files/main.md § A Design Document § The Record's Checks`

    **Rule:** `specs/methodology/working-files/main.md § A Design Document § The Kinds of Change` \
    **Leaves:** a Target naming a file the design's Kind does not let it change \
    **Caught By:**
      - `specs/AGENTS.md § Design, Refactor, Refine § Who Checks What and Why § Check Roles [Check: the adversarial review]`

  - **Failure:** a construct or a table in an Objective \
    **Sections:**
      - `specs/methodology/working-files/main.md § Design Plan Step § Step Objective`

    **Rule:** `specs/methodology/working-files/main.md § Design Plan Step § Step Objective` \
    **Leaves:** a step Objective holding a construct or a table \
    **Caught By:**
      - `specs/AGENTS.md § Design, Refactor, Refine § Who Checks What and Why § Check Roles [Check: the validation review]`

  - **Failure:** an Objective stating no outcome \
    **Sections:**
      - `specs/methodology/working-files/main.md § Design Plan Step § Step Objective`

    **Rule:** `specs/methodology/working-files/main.md § Design Plan Step § Step Objective` \
    **Leaves:** an Objective stating a means: how its step is implemented, a construct, a place in a file, a name the apply writes, or wording that is not the user's \
    **Caught By:**
      - `specs/methodology/working-files/main.md § Design Plan Step § Step Objective § Semantic Checks [Name: objective-states-an-outcome]`
      - `specs/AGENTS.md § Design, Refactor, Refine § Who Checks What and Why § Check Roles [Check: the builder's self-review]`
      - `specs/AGENTS.md § Design, Refactor, Refine § Who Checks What and Why § Check Roles [Check: the adversarial review]`

  - **Failure:** prose around a step's change left inconsistent \
    **Sections:**
      - `specs/methodology/working-files/main.md § A Design Document § The Standing Objective`

    **Rule:** `specs/methodology/working-files/main.md § A Design Document § The Standing Objective` \
    **Leaves:** prose within the Target left inconsistent with the steps \
    **Caught By:**
      - `specs/AGENTS.md § Design, Refactor, Refine § Who Checks What and Why § Check Roles [Check: the post-apply review]`

  - **Failure:** a change none of the design's changes \
    **Sections:**
      - `specs/methodology/working-files/main.md § A Design Document § Applying and Committing`

    **Rule:** `specs/methodology/working-files/main.md § A Design Document § Applying and Committing` \
    **Leaves:** a change that is none of the design's changes \
    **Caught By:**
      - `specs/AGENTS.md § Design, Refactor, Refine § Who Checks What and Why § Check Roles [Check: the post-apply review]`
      - `.ai/skills/design-specs/` `--check-changed-files`
      - `.ai/skills/implement-specs/` `--check-changed-files`

  - **Failure:** a tactical fix sent back \
    **Sections:**
      - `specs/methodology/working-files/main.md § A Design Document § Changes After Approval`

    **Rule:** `specs/methodology/working-files/main.md § A Design Document § Changes After Approval` \
    **Leaves:** nothing the script reads \
    **Caught By:**
      - the user

  - **Failure:** a steer recorded out of its form \
    **Sections:**
      - `specs/methodology/working-files/main.md § Steering Decision`

    **Rule:** `specs/methodology/working-files/main.md § Steering Decision` \
    **Leaves:** a Decision not giving the essence of what its steer decided \
    **Caught By:**
      - `specs/AGENTS.md § Design, Refactor, Refine § Who Checks What and Why § Check Roles [Check: the adversarial review]`
      - the user

  - **Failure:** a revising steer not naming the steer it revises \
    **Sections:**
      - `specs/methodology/working-files/main.md § Steering Decision § When a Steer Is Recorded`

    **Rule:** `specs/methodology/working-files/main.md § Steering Decision § When a Steer Is Recorded` \
    **Leaves:** a revising steer's Decision not naming the steer it revises \
    **Caught By:**
      - `specs/AGENTS.md § Design, Refactor, Refine § Who Checks What and Why § Check Roles [Check: the adversarial review]`
      - the user

  - **Failure:** a steer quoting only part of the user's words \
    **Sections:**
      - `specs/methodology/working-files/main.md § Steering Decision § Telling a Steer Apart`

    **Rule:** `specs/methodology/working-files/main.md § Steering Decision § Telling a Steer Apart § Steer, Direction, Feedback, Other Work or the User's Edit` \
    **Leaves:** a Steer quoting only part of the user's words that decided \
    **Caught By:**
      - `specs/AGENTS.md § Design, Refactor, Refine § Who Checks What and Why § Check Roles [Check: the builder's self-review]`
      - the user

  - **Failure:** a steer of a Type other than its own \
    **Sections:**
      - `specs/methodology/working-files/main.md § Steering Decision § A Steer's Type`

    **Rule:** `specs/methodology/working-files/main.md § Steering Decision § A Steer's Type` \
    **Leaves:** a steer of a Type other than its own \
    **Caught By:**
      - `specs/AGENTS.md § Design, Refactor, Refine § Who Checks What and Why § Check Roles [Check: the adversarial review]`
      - the user

  - **Failure:** a set of steers changing the goals or the frame applied unconfirmed \
    **Sections:**
      - `specs/AGENTS.md § Design, Refactor, Refine`
      - `specs/methodology/working-files/main.md § Steering Decision § When a Steer Is Recorded`

    **Rule:** `specs/AGENTS.md § Design, Refactor, Refine § The Goals and the Frame` \
    **Leaves:** nothing in the files \
    **Caught By:**
      - the user

  - **Failure:** an unanswered question read as agreed \
    **Sections:**
      - `specs/methodology/working-files/main.md § Steering Decision § When a Steer Is Recorded`

    **Rule:** `specs/methodology/working-files/main.md § Steering Decision § When a Steer Is Recorded` \
    **Leaves:** nothing in the files \
    **Caught By:**
      - the user

  - **Failure:** an earlier steering decision rewritten \
    **Sections:**
      - `specs/methodology/working-files/main.md § Steering Decision § When a Steer Is Recorded`

    **Rule:** `specs/methodology/working-files/main.md § Steering Decision § When a Steer Is Recorded` \
    **Leaves:** nothing in the files \
    **Caught By:**
      - the user

  - **Failure:** a design lagging a steer \
    **Sections:**
      - `specs/methodology/working-files/main.md § Steering Decision § When a Steer Is Recorded`

    **Rule:** `specs/methodology/working-files/main.md § Steering Decision § When a Steer Is Recorded` \
    **Leaves:** a design not yet carrying out a steer it records \
    **Caught By:**
      - `specs/AGENTS.md § Design, Refactor, Refine § Who Checks What and Why § Check Roles [Check: the adversarial review]`
      - the user

  - **Failure:** a frame out of sync with its steers or its steps \
    **Sections:**
      - `specs/AGENTS.md § Design, Refactor, Refine § Measure Twice, Cut Once § The Order of a Design's Parts`

    **Rule:** `specs/AGENTS.md § Design, Refactor, Refine § Measure Twice, Cut Once § The Order of a Design's Parts` \
    **Leaves:** a frame out of sync with its steers or its steps, a Frame Outcome untrue of them among it \
    **Caught By:**
      - `specs/AGENTS.md § Design, Refactor, Refine § Who Checks What and Why § Check Roles [Check: the adversarial review]`
      - `specs/AGENTS.md § Design, Refactor, Refine § Who Checks What and Why § Check Roles [Check: the builder's self-review]`

  - **Failure:** a design's part holding less than its form asks \
    **Sections:**
      - `specs/methodology/working-files/main.md § A Design Document`

    **Rule:** `specs/methodology/working-files/main.md § A Design Document` \
    **Leaves:** an Out of Scope naming another working file, a dependency named with no statement of what the design relies on from it, or a canon design's Impact on the Application Specs holding no item and not saying how its research was done \
    **Caught By:**
      - `specs/AGENTS.md § Design, Refactor, Refine § Who Checks What and Why § Check Roles [Check: the adversarial review]`
      - `specs/AGENTS.md § Design, Refactor, Refine § Who Checks What and Why § Check Roles [Check: the builder's self-review]`

  - **Failure:** a hand-off that nothing holds \
    **Sections:**
      - `specs/methodology/working-files/main.md § A Design Document`

    **Rule:** `specs/methodology/working-files/main.md § A Design Document § Spawning a Change of Its Own` \
    **Leaves:** an item of Out of Scope or of Impact on the Application Specs handing on work no design or follow-up holds \
    **Caught By:**
      - `specs/AGENTS.md § Design, Refactor, Refine § Who Checks What and Why § Check Roles [Check: the builder's self-review]`
      - the user

  - **Failure:** a reliance no longer matching its dependency \
    **Sections:**
      - `specs/methodology/working-files/main.md § A Design Document § Blocked and to Revise`

    **Rule:** `specs/methodology/working-files/main.md § A Design Document § Blocked and to Revise` \
    **Leaves:** a statement of what a design relies on that its finished dependency does not settle \
    **Caught By:**
      - `specs/AGENTS.md § Design, Refactor, Refine § Who Checks What and Why § Check Roles [Check: the adversarial review]`
      - the user

  - **Failure:** a decision of the user's left out of the steers \
    **Sections:**
      - `specs/methodology/working-files/main.md § Steering Decision § When a Steer Is Recorded`

    **Rule:** `specs/methodology/working-files/main.md § Steering Decision § When a Steer Is Recorded` \
    **Leaves:** a design's steers missing a decision the user gave \
    **Caught By:**
      - `specs/AGENTS.md § Design, Refactor, Refine § Who Checks What and Why § Check Roles [Check: the builder's self-review]`
      - the user

  - **Failure:** a report not recording its settlement \
    **Sections:**
      - `specs/methodology/working-files/main.md § A Check's Report`

    **Rule:** `specs/methodology/working-files/main.md § A Check's Report` \
    **Leaves:** a check's report not recording how its findings were settled \
    **Caught By:**
      - `specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: findings-settled-once]`

  - **Failure:** an audit's triage not recording what the design caused \
    **Sections:**
      - `specs/methodology/working-files/main.md § A Check's Report § Verdicts`

    **Rule:** `specs/AGENTS.md § Design, Refactor, Refine § An Audit` \
    **Leaves:** the builder's triage of an audit not recording each finding as caused by the design or not \
    **Caught By:**
      - `specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: findings-settled-once]`

  - **Failure:** a report handed back unchecked \
    **Sections:**
      - `specs/methodology/working-files/main.md § A Check's Report § Who Writes Each Part`

    **Rule:** `specs/AGENTS.md § Design, Refactor, Refine § The Adversarial Review` \
    **Leaves:** a report out of its form as settling starts \
    **Caught By:**
      - `.ai/skills/design-specs/` `--take-up-report`
      - `.ai/skills/implement-specs/` `--take-up-report`

  - **Failure:** a reviewer's part of a report changed by the builder \
    **Sections:**
      - `specs/methodology/working-files/main.md § A Check's Report § Who Writes Each Part`

    **Rule:** `specs/methodology/working-files/main.md § A Check's Report § Who Writes Each Part` \
    **Leaves:** a part its cold agent wrote no longer matching the fingerprint its Hand-back holds \
    **Caught By:**
      - `specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: cold-parts-kept]`

  - **Failure:** a cause or a miss the files do not bear out \
    **Sections:**
      - `specs/methodology/working-files/main.md § A Check's Report § What the Design Script Checks`

    **Rule:** `specs/AGENTS.md § Design, Refactor, Refine § Settling a Round § The Round at Its Causes § Group` \
    **Leaves:** a Cause's decision or a Miss the files do not bear out \
    **Caught By:**
      - `specs/AGENTS.md § Design, Refactor, Refine § Who Checks What and Why § Check Roles [Check: the adversarial review]`
      - `specs/AGENTS.md § Design, Refactor, Refine § Who Checks What and Why § Check Roles [Check: the post-apply review]`
      - the user

  - **Failure:** a verdict the files do not bear out \
    **Sections:**
      - `specs/methodology/working-files/main.md § A Check's Report § What the Design Script Checks`

    **Rule:** `specs/AGENTS.md § Design, Refactor, Refine § Settling a Round § The Test` \
    **Leaves:** a Finding's Verdict the files do not bear out \
    **Caught By:**
      - `specs/AGENTS.md § Design, Refactor, Refine § Who Checks What and Why § Check Roles [Check: the adversarial review]`
      - `specs/AGENTS.md § Design, Refactor, Refine § Who Checks What and Why § Check Roles [Check: the post-apply review]`
      - the user

  - **Failure:** a Builder Check's Result the files do not bear out \
    **Sections:**
      - `specs/methodology/working-files/main.md § A Check's Report § What the Design Script Checks`

    **Rule:** `specs/methodology/working-files/main.md § A Check's Report § Kinds of Builder Check` \
    **Leaves:** a Builder Check's Result the files do not bear out \
    **Caught By:**
      - `specs/AGENTS.md § Design, Refactor, Refine § Who Checks What and Why § Check Roles [Check: the adversarial review]`
      - `specs/AGENTS.md § Design, Refactor, Refine § Who Checks What and Why § Check Roles [Check: the post-apply review]`
      - the user

  - **Failure:** a log entry out of its type \
    **Sections:**
      - `specs/methodology/working-files/main.md § Design Log Entry`

    **Rule:** `specs/methodology/working-files/main.md § Design Log Entry` \
    **Leaves:** a log entry out of its type, refused as it is appended \
    **Caught By:**
      - `.ai/skills/design-specs/` `--log-entry`
      - `.ai/skills/implement-specs/` `--log-entry`
      - `specs/AGENTS.md § Design, Refactor, Refine § Who Checks What and Why § Check Roles [Check: the validation review]`

  - **Failure:** a design applied over uncommitted changes \
    **Sections:**
      - `specs/methodology/working-files/main.md § A Design Document § Uncommitted Changes`

    **Rule:** `specs/methodology/working-files/main.md § A Design Document § Uncommitted Changes` \
    **Leaves:** nothing the script reads \
    **Caught By:**
      - the user

  - **Failure:** a design's changes committed with another's \
    **Sections:**
      - `specs/methodology/working-files/main.md § A Design Document § Applying and Committing`

    **Rule:** `specs/methodology/working-files/main.md § A Design Document § Applying and Committing` \
    **Leaves:** nothing the script reads \
    **Caught By:**
      - the user

  - **Failure:** a design's changes committed unbidden \
    **Sections:**
      - `specs/methodology/working-files/main.md § A Design Document § Applying and Committing`

    **Rule:** `specs/methodology/design-workflow.md § The Order of a Design's Work § The Apply` \
    **Leaves:** nothing the script reads \
    **Caught By:**
      - the user

  - **Failure:** a commit message not naming each edit \
    **Sections:**
      - `specs/methodology/working-files/main.md § A Design Document § Applying and Committing`

    **Rule:** `specs/methodology/working-files/main.md § A Design Document § Applying and Committing` \
    **Leaves:** a commit message leaving out a direct edit or an edit of the user's \
    **Caught By:**
      - the user

  - **Failure:** a send-back setting aside its kept changes \
    **Sections:**
      - `specs/methodology/working-files/main.md § A Design Document § The States It Moves Through § A Send-back`

    **Rule:** `specs/methodology/working-files/main.md § A Design Document § The States It Moves Through § A Send-back` \
    **Leaves:** nothing the script reads \
    **Caught By:**
      - the user

  - **Failure:** a sent-back design's kept changes read as the last commit \
    **Sections:**
      - `specs/methodology/working-files/main.md § A Design Document § The States It Moves Through § A Send-back`

    **Rule:** `specs/methodology/working-files/main.md § A Design Document § The States It Moves Through § A Send-back` \
    **Leaves:** changes that are none of the design's \
    **Caught By:**
      - `specs/AGENTS.md § Design, Refactor, Refine § Who Checks What and Why § Check Roles [Check: the post-apply review]`

  - **Failure:** a design worked out of its machines' order \
    **Sections:**
      - `specs/methodology/design-workflow.md § The Order of a Design's Work`

    **Rule:** `specs/methodology/design-workflow.md § The Order of a Design's Work` \
    **Leaves:** nothing the files decide \
    **Caught By:**
      - the user

  - **Failure:** a review started with more than the standard brief, a brief of a skill's own among it, or an audit with any brief \
    **Sections:**
      - `specs/AGENTS.md § Design, Refactor, Refine`
      - `specs/methodology/design-workflow.md § A Review's Brief`

    **Rule:** `specs/methodology/design-workflow.md § A Review's Brief` \
    **Leaves:** nothing the script reads \
    **Caught By:**
      - the user

  - **Failure:** research started with more than the research brief, a brief of a skill's own among it \
    **Sections:**
      - `specs/methodology/design-workflow.md § A Research Brief`

    **Rule:** `specs/methodology/design-workflow.md § A Research Brief` \
    **Leaves:** nothing the script reads \
    **Caught By:**
      - the user

  - **Failure:** a review not sized by its Kind \
    **Sections:**
      - `specs/methodology/design-workflow.md § A Design's Reviews`

    **Rule:** `specs/methodology/design-workflow.md § A Design's Reviews` \
    **Leaves:** the design's log, whose entries name each review's effort \
    **Caught By:**
      - the user

  - **Failure:** a review not run at its effort \
    **Sections:**
      - `specs/methodology/design-workflow.md § A Review's Effort`

    **Rule:** `specs/methodology/design-workflow.md § A Review's Effort` \
    **Leaves:** the design's log, whose entries name each review's model and effort \
    **Caught By:**
      - the user

  - **Failure:** an audit in an apply other than its Target's kinds pick \
    **Sections:**
      - `specs/methodology/design-workflow.md § A Design's Reviews`

    **Rule:** `specs/methodology/design-workflow.md § A Design's Reviews` \
    **Leaves:** nothing the script reads \
    **Caught By:**
      - the user

  - **Failure:** a reviewer definition left in version control \
    **Sections:**
      - `specs/methodology/skills.md § Setting Up an Agent`

    **Rule:** `specs/methodology/skills.md § Setting Up an Agent` \
    **Leaves:** a reviewer definition in version control \
    **Caught By:**
      - `§ What the script checks`

  - **Failure:** a citation naming a heading that does not exist \
    **Sections:**
      - `specs/methodology/scope.md § Progressive Disclosure`
      - `specs/methodology/scope.md § The Shape of the Scope`

    **Rule:** `specs/methodology/sourcing-and-citation.md § Writing a Citation` \
    **Leaves:** the citation \
    **Caught By:**
      - `§ What the script checks`

  - **Failure:** a fact given a second home \
    **Sections:**
      - `specs/methodology/scope.md § Progressive Disclosure`
      - `specs/methodology/scope.md § The Shape of the Scope`
      - `specs/methodology/sourcing-and-citation.md § One Home Per Fact`

    **Rule:** `specs/methodology/sourcing-and-citation.md § One Home Per Fact` \
    **Leaves:** the fact stated twice \
    **Caught By:**
      - `§ The audits [Audit: Where a rule lives]`

  - **Failure:** a term used against its sense \
    **Sections:**
      - `specs/methodology/scope.md § Progressive Disclosure`
      - `specs/methodology/scope.md § The Shape of the Scope`

    **Rule:** `specs/methodology/glossary.md § Glossary` \
    **Leaves:** the term's use \
    **Caught By:**
      - `§ The audits [Audit: Glossary terms]`

  - **Failure:** a sentence holding several rules \
    **Sections:**
      - `specs/methodology/sourcing-and-citation.md § One Home Per Fact`

    **Rule:** `specs/methodology/sourcing-and-citation.md § One Home Per Fact § One Rule to a Sentence` \
    **Leaves:** the sentence \
    **Caught By:**
      - `§ The audits [Audit: Where a rule lives]`

  - **Failure:** a citation bare where it owed more \
    **Sections:**
      - `specs/methodology/sourcing-and-citation.md § One Home Per Fact`

    **Rule:** `specs/methodology/sourcing-and-citation.md § One Home Per Fact` \
    **Leaves:** a citation bare where it owed its application or its reason \
    **Caught By:**
      - `§ The audits [Audit: Whether the home holds the fact]`

  - **Failure:** a view or a counterpart left out of sync \
    **Sections:**
      - `specs/methodology/sourcing-and-citation.md § Keeping Specs in Sync`

    **Rule:** `specs/methodology/sourcing-and-citation.md § Keeping Specs in Sync` \
    **Leaves:** the view or the counterpart, out of sync with what the change reached \
    **Caught By:**
      - `§ The audits [Audit: Directory summary currency]`
      - `§ The audits [Audit: Diagram currency]`
      - `§ The audits [Audit: Counterpart currency]`

  - **Failure:** the technical overview's account of the code left out of sync \
    **Sections:**
      - `specs/methodology/sourcing-and-citation.md § Keeping Specs in Sync`

    **Rule:** `specs/methodology/sourcing-and-citation.md § Keeping Specs in Sync § Materialized Views` \
    **Leaves:** the technical overview's account, untrue of the code \
    **Caught By:**
      - `.ai/skills/verify-spec-implementation/`

  - **Failure:** a file or a domain placed against its test \
    **Sections:**
      - `specs/methodology/spec-placement.md § Where a File Goes`
      - `specs/methodology/spec-placement.md § Naming a Capability Domain`

    **Rule:** `specs/methodology/spec-placement.md § Where a File Goes` \
    **Leaves:** the file or the domain where its test does not place it \
    **Caught By:**
      - `§ The audits [Audit: Placement]`

  - **Failure:** a section stating rules that no check names \
    **Sections:**
      - `specs/methodology/scope.md § Rules and Skills`

    **Rule:** `specs/methodology/scope.md § Rules and Skills` \
    **Leaves:** a section stating rules that neither `§ The audits` nor any Skipped Step's Sections names, nor, for `specs/methodology/code.md`, the check on code's, nor a record section of checks standing directly under it \
    **Caught By:**
      - `§ What the script checks`

  - **Failure:** a section stating operating rules no step cites \
    **Sections:**
      - `specs/methodology/scope.md § Rules and Skills`

    **Rule:** `specs/methodology/scope.md § Rules and Skills` \
    **Leaves:** a section stating operating rules that no Workflow step cites \
    **Caught By:**
      - `§ What the script checks`

  - **Failure:** a work not read as its persona's \
    **Sections:**
      - `specs/methodology/spec-placement.md § Personas`

    **Rule:** `specs/methodology/spec-placement.md § Personas` \
    **Leaves:** a spec, the documentation, or a design changing code, that does not read as its persona's \
    **Caught By:**
      - `specs/AGENTS.md § Design, Refactor, Refine § Who Checks What and Why § Check Roles [Check: the adversarial review]`

  - **Failure:** a review not framed as its persona \
    **Sections:**
      - `specs/methodology/spec-placement.md § Personas`

    **Rule:** `specs/methodology/spec-placement.md § Personas` \
    **Leaves:** nothing in the files \
    **Caught By:**
      - the user

  - **Failure:** a technical change breaking its product file's promise \
    **Sections:**
      - `specs/methodology/spec-placement.md § Naming the Technical Files Behind a Capability`

    **Rule:** `specs/methodology/spec-placement.md § Naming the Technical Files Behind a Capability` \
    **Leaves:** the technical file, breaking a promise its product file makes \
    **Caught By:**
      - `§ The audits [Audit: Counterpart currency]`

  - **Failure:** a code design reaching beyond one module \
    **Sections:**
      - `specs/methodology/spec-placement.md § A Product Module`

    **Rule:** `specs/methodology/working-files/main.md § A Design Document § A Design Changing Code § One Product Module` \
    **Leaves:** a design changing code whose Target reaches beyond one module \
    **Caught By:**
      - `specs/AGENTS.md § Design, Refactor, Refine § Who Checks What and Why § Check Roles [Check: the adversarial review]`

  - **Failure:** a gap the module rule names \
    **Sections:**
      - `specs/methodology/spec-placement.md § A Product Module`

    **Rule:** `specs/methodology/spec-placement.md § A Product Module` \
    **Leaves:** a design written past the gap \
    **Caught By:**
      - `specs/AGENTS.md § Design, Refactor, Refine § Who Checks What and Why § Check Roles [Check: the adversarial review]`
      - the user

  - **Failure:** code handed on with a local task unrun \
    **Sections:**
      - `specs/methodology/spec-placement.md § Environments`

    **Rule:** `specs/methodology/spec-placement.md § Environments` \
    **Leaves:** a self-review's report recording no run of the task \
    **Caught By:**
      - `specs/methodology/spec-placement.md § Environments`
      - `specs/AGENTS.md § Design, Refactor, Refine § Who Checks What and Why § Check Roles [Check: the post-apply review]`

  - **Failure:** governed code doing what no spec states \
    **Sections:**
      - `specs/methodology/code.md § Changing Code`

    **Rule:** `specs/methodology/code.md § Changing Code` \
    **Leaves:** the code \
    **Caught By:**
      - `.ai/skills/verify-spec-implementation/`

  - **Failure:** code a change writes against American English \
    **Sections:**
      - `specs/methodology/code.md § Changing Code`

    **Rule:** `specs/methodology/code.md § Changing Code` \
    **Leaves:** the code's spelling \
    **Caught By:**
      - `.ai/skills/verify-spec-implementation/`

  - **Failure:** a change to code made outside a design \
    **Sections:**
      - `specs/methodology/code.md § Changing Code`

    **Rule:** `specs/methodology/code.md § Changing Code` \
    **Leaves:** nothing in the files \
    **Caught By:**
      - the user

## What is deliberately not audited

**Script checks were built and removed.** They were removed for the reason `specs/methodology/scope.md § Rules and Skills` gives. "Every product capability section has a `Test Scenarios` child": "is this a capability" is a judgment the files do not encode, and most of its findings were overview or definitional headings. "Every `Given` names a role the product specs define": the rule is real, but absence does not decide a violation. A scenario about system state has no actor, and a scenario may name its role in the `Then`. Scenario coverage now covers both by reading.

**Migration fidelity gets no audit.** Comparing a migration's source statements against their rewritten destinations is exactly this kind of work. Yet migrations are rare enough that a written method would be exercised about once, and one exercise is not enough to generalize a method from. Brief the comparison directly when a migration happens.

## Traps worth knowing

**Lineages start below the file's title.** `specs/methodology/sourcing-and-citation.md § Writing a Citation` states this. Building lineages from level 1 down was the script's earliest defect. It made every same-file citation in the repo fail at once, and it looked like a wall of broken citations rather than one bad assumption.

**Not every backtick span containing a section token is a citation.** A rule that discusses the token, or shows a forbidden heading form as an example, mentions the token rather than using it. The script treats only a span in one of the citation shapes as a citation:

```
§ Title
path/to/file.md § Title
§ Title [Key: value]
path/to/file.md § Title [Key: value; Key: value]
```

The script leaves every other span alone. Before it looks for a token outside a span, it strips every inline span. This skill's own documentation tripped that check on its first run. That is the most direct evidence available that the distinction is needed.

**A fenced block's content is set aside unless a check's row says it reads the block.** A citation shown inside a fenced block is an illustration, and the citation checks do not read it. A check reads inside a fence only where its row in `§ What the script checks` says so: the rows on a `gherkin` block, a `mermaid` block, the scope's tree and a `markdown` block, which is read as a file of its own, as `specs/methodology/spec-style.md § Markdown` has it.

**A mermaid block does not begin with `flowchart`.** Every diagram in this repo opens with a `config` front matter block inside the fence, so a check reading the first line fails on correct content. Match anywhere before the first node.
