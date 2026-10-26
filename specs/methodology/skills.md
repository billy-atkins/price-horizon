## Registered Skills

A skill is part of Spec of Record when it is registered here, and only then. A skill under `.ai/skills/` that is not registered is outside the methodology. A skill is registered when its subject is the methodology's rules or a craft they govern, not because it is useful while specs are written. Registering one is a deliberate decision, made here first, as extending the set of constructs is ([`specs/methodology/modeling-constructs.md § Purpose`](/specs/methodology/modeling-constructs.md#purpose)). A skill's `SKILL.md` states what the skill does, and this table never describes it. The table names only the homes of the rules each skill serves.

**Reference Key:** Skill \
**Required:** The Rules It Serves

| Skill | The Rules It Serves |
|---|---|
| `audit-specs` | [`specs/AGENTS.md`](/specs/AGENTS.md), `specs/methodology/` |
| `author-mermaid-diagram` | [`specs/methodology/modeling-constructs.md § Diagrams`](/specs/methodology/modeling-constructs.md#diagrams) |
| `configure-spec-of-record` | [`§ Setting Up an Agent`](#setting-up-an-agent), [`specs/methodology/design-workflow.md § A Review's Effort`](/specs/methodology/design-workflow.md#a-reviews-effort) |
| `design-specs` | [`specs/AGENTS.md`](/specs/AGENTS.md), `specs/methodology/` |
| `implement-specs` | [`specs/methodology/code.md`](/specs/methodology/code.md), [`specs/methodology/spec-placement.md § Personas`](/specs/methodology/spec-placement.md#personas), [`specs/methodology/spec-placement.md § A Product Module`](/specs/methodology/spec-placement.md#a-product-module), [`specs/methodology/spec-placement.md § Environments`](/specs/methodology/spec-placement.md#environments), [`specs/methodology/working-files.md § A Design Document`](/specs/methodology/working-files.md#a-design-document), [`specs/methodology/design-workflow.md`](/specs/methodology/design-workflow.md) |
| `verify-spec-implementation` | [`specs/methodology/code.md`](/specs/methodology/code.md), [`specs/methodology/spec-placement.md § The Technical Stack`](/specs/methodology/spec-placement.md#the-technical-stack), [`specs/methodology/spec-placement.md § What an Overview Describes`](/specs/methodology/spec-placement.md#what-an-overview-describes), [`specs/methodology/sourcing-and-citation.md § Keeping Specs in Sync § Materialized Views`](/specs/methodology/sourcing-and-citation.md#materialized-views) |

## Authoring a Skill

A skill captures a procedure this repo has already worked out, so the next agent does not rediscover it by repeating the mistakes that produced it. Each skill lives in its own directory under `.ai/skills/`. A skill that is part of the methodology is registered by the test [`§ Registered Skills`](#registered-skills) states.

**Name it verb-target, in kebab-case.** `author-mermaid-diagram`, not `mermaid` or `diagrams`. The verb states the action, and the target states what it acts on. Someone scanning the directory can then tell whether a skill applies without opening it. That directory name is the skill's name everywhere else it appears.

**`SKILL.md` is the entry point.** A skill takes the Agent Skills format ([`specs/methodology/external-references.md § External References [Name: Agent Skills]`](/specs/methodology/external-references.md#external-references)). Its `SKILL.md` opens with YAML front matter carrying `name` and `description`. The `name` matches the directory and is at most 64 characters. The `description` is at most 1,024 characters. Write the description to answer "when would someone reach for this", not "what is this about". A description that only names the subject leaves a reader guessing at the trigger, and removing that guess is the one thing a description exists to do.

**A skill's steps sit under a `## Workflow` heading.** They sit there in the skill's `SKILL.md`, and in each reference adding steps, in the order they run. Each step is a `###` heading or a bold lead-in. The check on a section stating operating rules finds there the step carrying its rules out, by the citation the step carries ([`specs/methodology/scope.md § Rules and Skills`](/specs/methodology/scope.md#rules-and-skills)).

**A skill gives each rule governing its work a point-of-use citation.** The skill does not restate the rule, per [`specs/methodology/sourcing-and-citation.md § One Home Per Fact`](/specs/methodology/sourcing-and-citation.md#one-home-per-fact). Nor does it leave the rule out, which would send a cold agent to re-derive it. Beside the citation, the skill adds only what the cited section asks of a citing place. Those rules live in [`specs/AGENTS.md`](/specs/AGENTS.md) and `specs/methodology/`, never in another skill. What two skills share belongs above both, and a skill cites into `.ai/skills/` only its own files. `specs/application/` is different. It is where the work is done, not a body of rules, so a skill works on it rather than citing it for how to work.

**A skill is written clearly, for a cold agent.** Per [`specs/methodology/spec-style.md § Clear Prose`](/specs/methodology/spec-style.md#clear-prose).

**Tooling goes in a `scripts/` child directory.** The entry-point script carries exactly the skill's own name: `.ai/skills/author-mermaid-diagram/scripts/author-mermaid-diagram.py`. Helpers sit beside it under their own names. Most skills will only ever have one script, and the convention costs nothing there. It earns itself in the rarer case of several. There, a name matching the skill's own tells an agent listing the directory, or a person browsing it, which file is the way in, without either having to read one. Apply the convention from the start rather than when another script appears, since by then the original is already named something else. An agent runs only a skill's entry script, so whatever a skill does is reached through the skill.

**Code two skills share goes in `.ai/skills/lib/`.** The code is a module of its own, named for what it does in Python's module form, as `design_documents.py`. The skills' entry scripts import it, and no agent runs it directly. Two skills needing the same check share one copy of it rather than two that drift apart.

**Instructions only some paths need go in a `references/` child directory.** Each path has a file of its own, read at the step that forks to it, so a path that does not need the instructions never loads them. Where a skill forks on the kind of specification, its references for the kinds are `references/app-specs.md` and `references/canon-specs.md`.

**A form template a step fills goes in `references/` too.** The form template is a file of its own, named for the form it holds, with `-form-template` ending the name before its extension: `design-document-form-template.md`. A reader listing `references/` then tells a form template from instructions without opening it. The form template is read at the step that fills it, so the form is copied rather than recalled. It holds the form's parts in order, each with a placeholder, a token in braces:
- for a value, the token says what kind of value replaces it, `{a few words}`, and the braces are replaced along with the token;
- for a section kept only in some cases, the token says when the section is kept, and is removed with its braces once the section is kept.

The form template leaves the rule setting the form to that rule's home.

**A skill's scratch space, and its plans, are directories of its own among the working files.** They take the form [`specs/methodology/working-files.md § The Working Files`](/specs/methodology/working-files.md#the-working-files) gives them.

**A script's actions are flags named verb-target.** A flag is named as a skill is: `--check-design-form`, `--show-workstack`. An agent then reads what a run does from the flag alone. The target says what the action acts on, and the verb what kind of action it is:
- a check reports what is wrong;
- a show describes a state;
- a verb changing a file, such as stamp, says that it does.

A flag setting how an action runs, rather than choosing one, is named for what it holds, as `--output-directory`. Flags combine in one run, so a capability added is a flag added. A run naming no action prints the script's usage and exits 2. A flag's words are whole words. A flag is never taken abbreviated, since an abbreviation can mean more than one thing. So every run's command line says what it does.

**Scripts are Python 3.** Wherever that is achievable, a script imports only the standard library, the skill's own helpers beside its entry script, and the code the skills share. A script needing an install step is a script that will not run at the moment it is needed. Where a capability genuinely requires something external, degrade rather than fail. Prefer a local tool when present, and a documented remote or manual path when not. Report which one ran, so a reader knows what they are trusting.

**A script's copy of the canon's values, or the canon read in place.** A script checks against values the canon states. It either keeps its own copy of them or reads them from the canon as it runs. It keeps a copy where a value gone missing would be a defect. The copy guards the methodology. An accidental change to the canon shows as a difference between the two. A deliberate change has to update the copy in the same change, which brings its effect on the script into that change's scope. `.ai/skills/lib/spec_checks.py` keeps such a copy of the kinds of file in scope, and reports any difference from [`specs/methodology/scope.md § What Spec of Record Governs`](/specs/methodology/scope.md#what-spec-of-record-governs) for the user to review. A value whose change is an editorial decision, as a word in a list a style check reads, is read in place. A copy there would only make each deliberate edit ask twice. A record type is read in place too, from its declaration ([`specs/methodology/modeling-constructs.md § Constructs § Record Form`](/specs/methodology/modeling-constructs.md#record-form)). A construct's Reference Key is read in place from the field its definition declares ([`specs/methodology/modeling-constructs.md § Constructs § Keyed Construct`](/specs/methodology/modeling-constructs.md#keyed-construct)). The check reads each declaration itself, so a declaration gone missing fails the check outright. Each copy carries a canon-spec annotation ([`specs/methodology/glossary.md`](/specs/methodology/glossary.md)) above it, written as [`specs/methodology/sourcing-and-citation.md § Writing a Citation § Citing From Code`](/specs/methodology/sourcing-and-citation.md#citing-from-code) writes one. A cold agent then finds what the code stands for, and the audit confirms the area is still there.

**Record what actually went wrong.** A skill earns its length by naming the failures that motivated it: the trap that only shows up at the wrong moment, and the fix that is not obvious from the symptom. Anything a reader can derive from the underlying tool's own documentation does not need to be in the skill.

## Setting Up an Agent

The agent in use sets up for itself what only it can carry out, through `.ai/skills/configure-spec-of-record/`. It writes what it needs as [`specs/methodology/scope.md § Agent Agnostic`](/specs/methodology/scope.md#agent-agnostic) allows anything written for one tool.

**A review's reasoning effort.** Where an agent applies a review's level through a reviewer definition, as [`specs/methodology/design-workflow.md § A Review's Effort`](/specs/methodology/design-workflow.md#a-reviews-effort) has it, the agent writes one definition for each level, named `review-light`, `review-medium` and `review-high`. Each definition is set to the agent's nearest level. It gives no instructions of its own, since the brief starts a review whose task the canon holds ([`specs/methodology/design-workflow.md § A Review's Brief`](/specs/methodology/design-workflow.md#a-reviews-brief)), and an audit follows its own skill's instructions. The agent keeps the definitions out of version control through the checkout's own exclude file, `.git/info/exclude`, so its setup changes no committed file.
