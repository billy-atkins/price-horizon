# PriceHorizon

A portfolio project, not a real product or company. PriceHorizon does not exist, and neither does Acme AI. At this stage it is a design project, not an implementation: there is no application code. It is an exercise in spec-driven system design: a product and technical specification for an AI capability that answers a real class of hard business question, written the way a real engagement would need it written, then hardened over many rounds of review for consistency and precision, and against internal contradiction. The spec-driven development methodology behind it was created by the author, Billy Atkins, for this project.

## What PriceHorizon is

Revenue Growth Management teams live with a specific, recurring question: what will a competitor do on price, where should our own brand sit in response, and what happens to the business as a result. PriceHorizon is a proposed answer engine for exactly that question. A user types one plain-language sentence, for example, "in six months, where will Competitor Brand's price be in Texas, and what will happen," and the system returns a layered answer: a confidence-scored forecast, a plain-language explanation of what is driving it, a map of how the number breaks down by market, a decomposition of the underlying forces, a small set of positioning options rather than one imposed answer, and the simulated business outcome of each, with the ability to drill into any of it, down to a county or a single store, or across to a different metric.

Every answer is built to meet guarantees that make it trustworthy enough to act on. It is repeatable: the same question, asked again with nothing changed in between, returns the same forecast and figures. Every number traces to a named, versioned model or dataset. Qualitative information, such as regulatory changes and competitive intelligence, is weighed alongside the numbers, not appended as commentary afterward. And the answer shows how it was built: each forecast opens to the baseline and driver corrections it is the sum of, and each confidence figure to its reasons. Beneath all of them, where the evidence falls short the system says so, and where a term in the question cannot be resolved it asks rather than guessing.

PriceHorizon runs as a self-hosted installation inside each customer's own environment, co-located with their data. It needs no connection outside that environment, so an installation can run air-gapped, and nothing from one customer's installation is ever combined with another's.

## Spec-driven Development Methodology

The interesting part of this exercise was not just the pricing domain but also the methodology: the discipline of keeping a specification honest as it grows. Specifications drift: a product promise and the mechanism meant to deliver it stop agreeing, a rule stated in two places changes in one, and prose reads as complete while silently leaving cases out. When AI agents write and maintain the specs, those failures arrive faster and read more confidently. The methodology is built to prevent them:

- **Two layers that answer to each other.** `specs/application/product/` states what a user can rely on, and `specs/application/technical/` states how it is made true. Each names the other, so the two cannot drift apart silently, and the technical overview maps each layer of the answer to the mechanism that produces it.
- **One home per fact.** Everywhere else cites that home, down to the section, so a change lands in one place and everything that depends on it can be found.
- **Structure where prose would hide gaps.** Where a rule or a process has to be checkably complete, it is written as one of an approved set of constructs, such as a decision table, a state machine, or an algorithm, because prose can describe anything but cannot be checked for what it leaves out.
- **A scenario for every promise.** Each capability owes, in Given, When, Then form, a statement of how each of its promises would be tested, so a promise that could never be checked shows up as one.
- **Diagrams that cite their sources.** Each source cites the diagram back, so a change to what a drawing shows points to the drawing that needs to follow it.
- **A methodology held to its own rules.** `specs/methodology/` is held to the rules it states.

One fact, followed end to end: the product promises that every answer shows how it was built (`specs/application/product/trust-and-explainability/guarantees.md`), a scenario beside that promise states how it would be tested, `specs/application/technical/guarantees-mechanics.md` gathers the mechanisms that keep the promise, and the product overview's From Evidence to Answer diagram draws it, citing that promise as its source.

Changes are made through Design, Refactor, Refine, set out in `AGENTS.md`. A change is drafted as a design, starting from the problem it solves, and restructured until it stops moving, then its wording is polished. A separate AI agent, with none of the drafting agent's context, then reviews it adversarially, for what is over-engineered and for what is relied on but never specified. Only with the author's approval is it applied, and another fresh agent then audits the result: by script for what a script can decide, and by reading for everything else. The designs, the review reports, and the list of work still to do are working files, kept out of version control on purpose: they serve the engineer writing the specs, never a reader of them, and what they settle reaches a reader only through the specs.

None of this is tied to one AI vendor's tools. `AGENTS.md` and `.ai/skills/` are written for any agent to follow, or a person to read directly. Each skill is a procedure this repo has worked out, such as designing a spec change or auditing the project against its rules, and records the failures that motivated it.

## How to read this repo

For a high-level view of PriceHorizon, start with the two overviews: `specs/application/product/architecture.md`, what a user experiences and can rely on, and `specs/application/technical/architecture.md`, how it is made true, each with diagrams. For the methodology, start with `specs/methodology/architecture.md`. Every directory under `specs/` has an `index.md` listing what it holds, and `specs/index.md` maps the specifications as a whole.

## Setup AI Skills for Claude Code

Optional, for Claude Code users. The skills live in `.ai/skills/` so any agent can read them. These scripts link that directory to `.claude/skills/` so Claude Code loads them natively. Each is safe to re-run, and the link is gitignored.

Windows, using a directory junction:
```
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\setup-claude-skills.ps1
```

Mac or Linux, using a symbolic link:
```
sh scripts/setup-claude-skills.sh
```

## Author

Written by Billy Atkins as an applied exercise in spec-driven system design.
