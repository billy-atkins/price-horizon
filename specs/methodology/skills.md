## Registered Skills

A skill is part of Spec of Record when it is registered here, and only then; a skill under `.ai/skills/` that is not registered is outside the method. A skill is registered when its subject is the method's rules or a craft they govern, not because it is useful while specs are written. Registering one is a deliberate decision, made here first, as extending the set of constructs is (`specs/methodology/modeling-constructs.md § Purpose`). What a skill does is stated in its `SKILL.md`, which this table never describes; the table names only the homes of the rules it serves.

| Skill | The rules it serves |
|---|---|
| `audit-specs` | `specs/AGENTS.md`, `specs/methodology/` |
| `author-mermaid-diagram` | `specs/methodology/modeling-constructs.md § Diagrams` |
| `configure-spec-of-record` | `§ Setting Up an Agent` |
| `design-specs` | `specs/AGENTS.md`, `specs/methodology/` |
| `implement-specs` | `specs/methodology/code.md`, `specs/methodology/spec-placement.md § Personas`, `specs/methodology/spec-placement.md § A Product Module`, `specs/methodology/spec-placement.md § Environments`, `specs/methodology/working-files.md § A Design Document` |
| `verify-spec-implementation` | `specs/methodology/code.md`, `specs/methodology/spec-placement.md § The Technical Stack` |

## Authoring a Skill

A skill captures a procedure this repo has already worked out, so the next agent does not rediscover it by repeating the mistakes that produced it. Each one lives in its own directory under `.ai/skills/`, and one that is part of the method is registered by the test `§ Registered Skills` states.

**Name it verb-target, in kebab-case —** `author-mermaid-diagram`, not `mermaid` or `diagrams`. The verb states the action, the target states what it acts on, and someone scanning the directory can tell whether a skill applies without opening it. That directory name is the skill's name everywhere else it appears.

**`SKILL.md` is the entry point —** it opens with YAML front matter carrying `name`, matching the directory, and `description`. Write the description to answer "when would someone reach for this", not "what is this about": a description that only names the subject leaves a reader guessing at the trigger, which is the one thing it exists to remove.

**A skill's steps sit under a `## Workflow` heading —** in its `SKILL.md`, and in each reference adding steps, in the order they run, each step a `###` heading or a bold lead-in. The check on an operating rule finds the step carrying it out there, by the citation the step carries (`specs/methodology/scope.md § Rules and Skills`).

**A skill gives each rule governing its work a point-of-use citation —** rather than restating it, per `specs/methodology/sourcing-and-citation.md § One Home Per Fact`, or leaving it out, which would send a cold agent to re-derive it. Beside the citation, it adds only what that section asks of a citing place. Those rules live in `specs/AGENTS.md` and `specs/methodology/`, never in another skill: what two skills share belongs above both, and a skill cites into `.ai/skills/` only its own files. `specs/application/` is different: it is where the work is done, not a body of rules, so a skill works on it rather than citing it for how to work.

**A skill is written clearly, for a cold agent —** per `specs/methodology/spec-style.md § Clear Prose`.

**Tooling goes in a `scripts/` child directory —** the entry-point script carries exactly the skill's own name: `.ai/skills/author-mermaid-diagram/scripts/author-mermaid-diagram.py`. Helpers sit beside it under their own names. Most skills will only ever have one script, and the convention costs nothing there; it earns itself in the rarer case of several, where a name matching the skill's own tells an agent listing the directory, or a person browsing it, which file is the way in without either having to read one. Apply it from the start rather than when another script appears, since by then the original is already named something else. An agent runs only a skill's entry script, so whatever a skill does is reached through the skill.

**Code two skills share goes in `.ai/skills/lib/` —** a module of its own, named for what it does in Python's module form, `design_documents.py`, imported by the skills' entry scripts and run by no agent directly. Two skills needing the same check share one copy of it rather than two that drift apart.

**Instructions only some paths need go in a `references/` child directory —** a file of its own for each path, read at the step that forks to it, so a path that does not need them never loads them. Where a skill forks on the kind of specification, its references for the kinds are `references/app-specs.md` and `references/canon-specs.md`.

**A template a step fills goes in `references/` too —** a file of its own, named for the form it holds with `-template` ending the name before its extension, `design-document-template.md`, so a reader listing `references/` tells a template from instructions without opening it. It is read at the step that fills it, so the form is copied rather than recalled. It holds the form's parts in order, each with a placeholder, a token in braces:

- for a value, the token says what kind of value replaces it, `{a few words}`, and the braces are replaced along with the token;
- for a section kept only in some cases, the token says when the section is kept, and is removed with its braces once the section is kept.

It leaves the rule setting the form to its home.

**A skill's scratch space, and its plans, are directories of its own among the working files —** in the form `specs/methodology/working-files.md § The Working Files` gives them.

**A script's actions are flags named verb-target —** as a skill is named, `--check-design-form`, `--show-workstack`, so an agent reads what a run does from the flag alone. The target says what the action acts on, and the verb what kind of action it is:

- a check reports what is wrong;
- a show describes a state;
- a verb changing a file, such as stamp, says that it does.

A flag setting how an action runs, rather than choosing one, is named for what it holds, `--output-directory`. Flags combine in one run, so a capability added is a flag added. A run naming no action prints the script's usage and exits 2. A flag's words are whole words, and a flag is never taken abbreviated, since an abbreviation can mean more than one thing; so every run's command line says what it does.

**Scripts are Python 3 —** importing only the standard library and the code the skills share, wherever that is achievable. A script needing an install step is a script that will not run at the moment it is needed. Where a capability genuinely requires something external, degrade rather than fail: prefer a local tool when present, a documented remote or manual path when not, and report which one actually ran so a reader knows what they are trusting.

**Record what actually went wrong —** a skill earns its length by naming the failures that motivated it, the trap that only shows up at the wrong moment, the fix that is not obvious from the symptom. Anything derivable from reading the underlying tool's own documentation does not need to be here.

## Setting Up an Agent

What only the agent in use can carry out, it sets up for itself, through `.ai/skills/configure-spec-of-record/`, writing what it needs as `specs/methodology/scope.md § Agent Agnostic` allows anything written for one tool.

**A review's reasoning effort —** an agent that applies a review's level (`specs/AGENTS.md § Design, Refactor, Refine`) as it starts a reviewer writes nothing for it. An agent that applies a level only through a definition of its own writes one reviewer definition for each level, named `review-light`, `review-medium` and `review-high`. Each is set to the agent's nearest level and gives no instructions of its own, since the brief the review is started with carries them. The agent keeps them out of version control through the checkout's own exclude file, `.git/info/exclude`, so its set-up changes no committed file.
