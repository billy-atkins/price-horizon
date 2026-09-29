## Registered Skills

A skill is part of Spec of Record when it is registered here, and only then; a skill under `.ai/skills/` that is not registered is outside the method. A skill is registered when its subject is the method's rules or a craft they govern, not because it is useful while specs are written, and registering one is a deliberate decision, made here first, as extending the set of constructs is (`specs/methodology/modeling-constructs.md § Purpose`). What a skill does is its `SKILL.md`, which this table never describes; the table names only the homes of the rules it serves.

| Skill | The rules it serves |
|---|---|
| `audit-specs` | `specs/AGENTS.md`, `specs/methodology/` |
| `author-mermaid-diagram` | `specs/methodology/modeling-constructs.md § Diagrams` |
| `design-specs` | `specs/AGENTS.md`, `specs/methodology/` |

## Authoring a Skill

A skill captures a procedure this repo has already worked out, so the next agent does not rediscover it by repeating the mistakes that produced it. Each one lives in its own directory under `.ai/skills/`, and one that is part of the method is registered by the test `§ Registered Skills` states.

**Name it verb-target, in kebab-case —** `author-mermaid-diagram`, not `mermaid` or `diagrams`. The verb states the action, the target states what it acts on, and someone scanning the directory can tell whether a skill applies without opening it. That directory name is the skill's name everywhere else it appears.

**`SKILL.md` is the entry point —** it opens with YAML front matter carrying `name`, matching the directory, and `description`. Write the description to answer "when would someone reach for this", not "what is this about": a description that only names the subject leaves a reader guessing at the trigger, which is the one thing it exists to remove.

**A skill's steps sit under a `## Workflow` heading —** in its `SKILL.md`, and in each reference adding steps, in the order they run, each step a `###` heading or a bold lead-in. The check on an operating rule finds the step carrying it out there, by the citation the step carries (`specs/methodology/scope.md § Rules and Skills`).

**A skill gives each rule governing its work a point-of-use citation —** rather than restating it, per `specs/methodology/sourcing-and-citation.md § One Home Per Fact`, or leaving it out, which would send a cold agent to re-derive it. What it adds is what that section asks of a citing place. Those rules live in `specs/AGENTS.md` and `specs/methodology/`, never in another skill: what two skills share belongs above both, and a skill cites into `.ai/skills/` only its own files. `specs/application/` is different: it is where the work is done, not a body of rules, so a skill works on it rather than citing it for how to work.

**Tooling goes in a `scripts/` child directory —** the entry-point script carries exactly the skill's own name: `.ai/skills/author-mermaid-diagram/scripts/author-mermaid-diagram.py`. Helpers sit beside it under their own names. Most skills will only ever have one script, and the convention costs nothing there; it earns itself in the rarer case of several, where a name matching the skill's own tells an agent listing the directory, or a person browsing it, which file is the way in without either having to read one. Apply it from the start rather than when another script appears, since by then the original is already named something else.

**Instructions only some paths need go in a `references/` child directory —** a file of its own for each path, read at the step that forks to it, so a path that does not need them never loads them. Where a skill forks on the kind of specification, its references are `references/app-specs.md` and `references/canon-specs.md`.

**A skill's scratch space is its own directory among the working files —** in the form `specs/methodology/working-files.md § The Working Files` gives it.

**Scripts are Python 3 —** standard library only wherever that is achievable. A script needing an install step is a script that will not run at the moment it is needed. Where a capability genuinely requires something external, degrade rather than fail: prefer a local tool when present, a documented remote or manual path when not, and report which one actually ran so a reader knows what they are trusting.

Record what actually went wrong. A skill earns its length by naming the failures that motivated it, the trap that only shows up at the wrong moment, the fix that is not obvious from the symptom. Anything derivable from reading the underlying tool's own documentation does not need to be here.
