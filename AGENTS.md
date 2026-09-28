# PriceHorizon — Agent Instructions

## What this project is

PriceHorizon is a proposed technical approach to a Revenue Growth Management (RGM) problem: how an AI capability could answer plain-language business questions (for example, a competitor pricing forecast) with a repeatable, evidence-grounded, layered answer, designed as a standalone product for a fictional client, Acme AI. This repo is the working spec and supporting design research for that approach, written by Billy Atkins as an applied exercise in spec-driven system design.

## Product naming and positioning
- Product name: **PriceHorizon**. A single, standalone RGM offering, not a module extending or positioned against any other product.
- PriceHorizon owns its own vocabulary end to end, its own natural language interface, its own trust and confidence model, its own harmonized data foundation. Nothing in the specs should describe it as consuming, extending, or surfacing through another platform's infrastructure.

## Writing specs

`specs/methodology/` holds the rules for writing a specification in this repo, which apply to every spec, its own files included. The rules in this file apply to the whole project, specs among it. Read the governing rule before drafting, not after; `specs/methodology/index.md` lists which file covers what.

| Doing this | The rule is here |
|---|---|
| Deciding product spec versus technical spec | `specs/methodology/spec-placement.md § Product or Technical` |
| Deciding index, architecture, or detail file | `specs/methodology/spec-placement.md § Index, Architecture, Detail` |
| Placing a new file, or deciding whether a domain earns a subfolder | `specs/methodology/spec-placement.md § Where a File Goes` |
| Naming a new product capability domain | `specs/methodology/spec-placement.md § Naming a Capability Domain` |
| Linking a product file to the technical files that build it | `specs/methodology/spec-placement.md § Naming the Technical Files Behind a Capability` |
| Deciding whether a rule may be restated | `specs/methodology/sourcing-and-citation.md § One Home Per Fact` |
| Writing a citation, or deciding whether one may be written | `specs/methodology/sourcing-and-citation.md § Writing a Citation`, `specs/methodology/sourcing-and-citation.md § Which Citations Are Allowed` |
| Adding or retitling a heading | `specs/methodology/sourcing-and-citation.md § Titling a Heading` |
| Describing a rule, a process, or an entity's behavior | `specs/methodology/modeling-constructs.md` |
| Recording a decision the specs rely on but have not made | `specs/methodology/spec-placement.md § An Open Question` |
| Writing a field, a bold lead-in, or an entry of a repeated kind | `specs/methodology/modeling-constructs.md § Fields`, `specs/methodology/modeling-constructs.md § Bold Lead-ins`, `specs/methodology/modeling-constructs.md § Constructs § Record Form` |
| Writing or updating acceptance scenarios | `specs/methodology/acceptance-scenarios.md § Acceptance Scenarios` |
| Removing drafting residue and hedged framing | `specs/methodology/spec-style.md § What a Finished Spec Reads Like` |
| Recording a proposed change, or work to take up later | `specs/methodology/working-files.md § A Design Entry`, `specs/methodology/working-files.md § A Follow-up` |

`.ai/skills/design-specs/` sequences this work and names the governing rule at each step; `.ai/skills/audit-specs/` checks the result, by reading and by script.

## Repo conventions

- This is a proposal and research repo, not a codebase. Do not scaffold application code here unless explicitly asked to build a prototype.
- These instructions, and everything under `.ai/`, stay agnostic of which agent reads them: `AGENTS.md` rather than a vendor-specific instruction filename, no tool-specific directory, no assumption about which model, CLI, or editor is running. The test for anything new: would it still make sense to an agent from a different vendor, or a person reading it directly. Tooling is the one exception, and only because it carries no content: an opt-in helper under `scripts/`, named for the tool it serves, may wire that tool up to the agnostic content, the way `scripts/setup-claude-skills.ps1` and `scripts/setup-claude-skills.sh` link `.ai/skills/` into the directory Claude Code loads skills from. Whatever a helper generates is gitignored, and `README.md` says how to run it. Nothing here depends on a helper having run: a skill stays readable directly, and a helper only saves a step for someone using that tool.
- Before doing by hand a kind of work a skill under `.ai/skills/` covers, read its `SKILL.md`: `.ai/skills/design-specs/` covers proposing or revising spec content, `.ai/skills/audit-specs/` checks the project against the rules that govern it, and `.ai/skills/author-mermaid-diagram/` covers authoring, rendering, and checking a Mermaid diagram. What a skill is, and how one is authored or changed, is `§ Authoring Skills`.

## Ordinals and Counts

Avoid numbers that add nothing a reader cannot already see but create friction when the set changes. A number restating a list's order or its size goes stale silently the moment an item is added or moved, and so does everything that refers to it. Say what things are, what they mean, or where they are; whoever needs a count can count them when they do the work.

- Nothing is numbered: not a heading, a bold lead-in, or a list item.
- Nothing refers to an item by its position, by number or by word ("step 5", "the second", "the latter"). Refer to it by its name.
- Nothing says how many things a list or the repo holds. Name them, describe them, or point to them.

Numbers that carry value stay. Algorithm and Decision Tree tables keep their numbered steps, and references to those steps, because that numbering is an industry standard a cold agent reads without further instruction, as a software engineer would (`specs/methodology/modeling-constructs.md`). A Gherkin scenario states its own test case in full, and its numbers are that case's data. A value is not a count: a two-week window, a floor of two options, exactly one home. Neither is naming a pair, "both", "either" or "the two", nor where something sits on the page, "the table above" or "below".

`.ai/skills/audit-specs/` enforces this rule.

## Authoring Skills

A skill captures a procedure this repo has already worked out, so the next agent does not rediscover it by repeating the mistakes that produced it. Each one lives in its own directory under `.ai/skills/`.

**Name it verb-target, in kebab-case.** `author-mermaid-diagram`, not `mermaid` or `diagrams`. The verb states the action, the target states what it acts on, and someone scanning the directory can tell whether a skill applies without opening it. That directory name is the skill's name everywhere else it appears.

**`SKILL.md` is the entry point**, opening with YAML front matter carrying `name`, matching the directory, and `description`. Write the description to answer *when would someone reach for this*, not *what is this about*: a description that only names the subject leaves a reader guessing at the trigger, which is the one thing it exists to remove.

**A skill cites the rules that govern its work, at the step where the work needs them**, rather than restating them, per `specs/methodology/sourcing-and-citation.md § One Home Per Fact`, or leaving them out, which would send a cold agent to re-derive them. What it adds is what those rules do not say. Those rules live in `AGENTS.md` and `specs/methodology/`. `specs/application/` is different: it is where the work is done, not a body of rules, so a skill works on it rather than citing it for how to work.

**Tooling goes in a `scripts/` child directory**, and the entry-point script carries exactly the skill's own name: `.ai/skills/author-mermaid-diagram/scripts/author-mermaid-diagram.py`. Helpers sit beside it under their own names. Most skills will only ever have one script, and the convention costs nothing there; it earns itself in the rarer case of several, where a name matching the skill's own tells an agent listing the directory, or a person browsing it, which file is the way in without either having to read one. Apply it from the start rather than when another script appears, since by then the original is already named something else.

**Scratch space is `.ai/tmp/<skill-name>/`**, created by the skill if it is not there. One directory per skill so that one skill's output is never mistaken for another's, and under `.ai/tmp/` so none of it is ever committed. A skill does not delete its own output when it finishes: the output is usually the whole point, and something downstream, an agent or a person, is about to read it. What a skill should clean is its own *stale* output, the file left behind from a previous run that no longer corresponds to anything, since a reader has no way to tell that from a current one.

**Scripts are Python 3**, standard library only wherever that is achievable. A script needing an install step is a script that will not run at the moment it is needed. Where a capability genuinely requires something external, degrade rather than fail: prefer a local tool when present, a documented remote or manual path when not, and report which one actually ran so a reader knows what they are trusting.

Record what actually went wrong. A skill earns its length by naming the failures that motivated it, the trap that only shows up at the wrong moment, the fix that is not obvious from the symptom. Anything derivable from reading the underlying tool's own documentation does not need to be here.

## Design, Refactor, Refine (DRR)

How anything here gets built or reworked, whether a spec, a rule, a skill, or code. Whoever does the work, the builder, takes it through the process below; a cold subagent, one with none of the builder's context and no attachment to their decisions, then runs its own adversarial DRR over the result. `.ai/skills/design-specs/` applies it to specs.

**Read fresh before any work.** Before working on a file, however small the change or recent the last read, read it again, direct edits included. Nothing tells an agent whether its memory of a file survived compaction, and content written an hour ago feels remembered when it is a reconstruction.

**Scope comes first.** Determine the actual scope of the change before drafting it. Too small a scope reaches a local optimum, right for the file in hand and wrong for the system around it; only the real scope admits the global one. Widen it until nothing outside it would change the answer, and sweep for it by meaning as well as by the draft's own words: a search built from the draft's terms finds only what the draft already knew about.

- **Design.** Start from the problem to solve, stated plainly, and get it logically working: a draft that solves it correctly, before it is good. The draft is described in a design entry in `.ai/designs.md` (`specs/methodology/working-files.md § A Design Entry`).
- **Refactor.** Macro improvements to its internal workings and its external surface: structural changes that make it better meet its actual needs, not wording. Repeat until it converges, when a round leaves the structure where it was.
- **Refine.** Once Refactor has converged, enhance its elegance and make it easy to use and to understand: wording, naming, phrasing, consistency. Polishing something still moving structurally is wasted effort.

**The adversarial DRR.** When the builder judges the work optimal, the cold subagent is given the same problem and the builder's design, each stated on its own. It is never the builder, since re-reading your own work re-reads what you meant. It does not derive its own solution: it takes the builder's design through Design, Refactor and Refine again, from the perspectives of what is over-engineered, a mechanism, role, or safeguard whose complexity no stated need justifies, and what is under-developed, something relied on as a guarantee or an enforcement mechanism that is asserted but not specified. It reports findings; it does not edit.

Brief it with more than the task: name the failure patterns earlier rounds found, say which decisions the user has settled so it checks fidelity to them rather than reopening them, ask for any sweep of the repo to be redone by its own method, and point it at whatever the design decides, since that is where defects concentrate.

The builder checks every finding against the files before acting on it, since a review can be confidently wrong. The user steers which findings are addressed and how. Accepted findings go back through the builder's process, and if they changed the structure, the revised design gets another adversarial DRR. Then, with the user's go-ahead, the builder applies the work and a cold subagent audits it, which for specs means `.ai/skills/audit-specs/`.

**Direct edits.** A small tactical edit, narrow in scope and low in risk, may skip this process and be applied directly, but only once the user has approved it. Anything larger or riskier goes through the process.
