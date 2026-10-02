# PriceHorizon, built with Spec of Record

**Spec of Record** is a spec-driven development method for the agentic software development lifecycle, in which the specification, not the code, is the durable source of truth: the specs say what a system does and why. A software engineer designs each change with an AI agent, and the agent authors it, with the engineer as the human in the loop at every decision. Every rule the method states has a check: a script where a script can decide, an independent AI reviewer where it takes judgment. Today the method governs specifications, its own included; generating code from them is its next phase.

**PriceHorizon** is the worked example: the full product and technical specification of an AI answer engine for competitive pricing, written and governed with Spec of Record. Both are the work of [Billy Atkins](https://www.linkedin.com/in/billy-atkins). PriceHorizon and Acme AI, the SaaS company behind it, are fictional; the method, and the rigor applied to it, are real.

## At a glance

- **The problem —** AI agents write specs and code faster than people can check them. Specs drift from what they describe, a rule stated twice changes in one place, and prose reads as complete while leaving cases out, and AI agents make those failures arrive faster and harder to spot, because an agent's prose reads as fluent and authoritative even where it is wrong. Most spec-driven methods treat a spec as a per-change prompt: used to generate code, then discarded or left in a pile of per-feature documents that records changes, not the system as it stands.
- **The approach —** keep the specs. They stay the record of what the system does and why, kept true through every change, so code can be built from them rather than the other way round.
- **What makes it hold —** one home per fact; structured, checkable forms where prose would hide gaps; a test scenario for every promise; and a check for every rule, because a rule without a check is only a suggestion.
- **How it is built —** through its own process. The methodology is written in the language it defines, changed through the design and review process it prescribes, and audited by the checks it sets.
- **See for yourself —** this repo holds about 50 product and technical specification files with over 130 acceptance scenarios, a methodology governing them and itself, and the skills that carry it out. Some of the method only shows in use, so the best test is to take a change through it with your own agent.

## How Spec of Record differs from other spec-driven development

**Specs that outlive the change —** in most spec-driven development, a spec is an instruction set: it is used to generate code, and once the code works the spec is discarded, or kept as one more per-feature document in a growing pile. Like a ticket history, that pile records the changes, not the system as it stands; to learn what the system does today, a reader replays every change and hopes none contradicted another. Spec of Record keeps one specification of the system as it is, and every new feature is designed against it. Extending a building means extending its engineering plans and checking the new work against what is already there; catching an issue before pouring concrete is far cheaper than finding it after the foundation has cured. The specs become the layer of record, and code an implementation detail beneath them, as the JVM is beneath Java.

**The why, kept with the what —** code holds what a system does, rarely why. The specs hold both, so the next engineer, or the next agent, starts from a record of the reasons rather than rediscovering them, and settled questions stay settled.

**One home per fact, cited everywhere else —** every rule and definition is stated once, and everything that relies on it cites that home, down to the section. A change lands in one place, and everything depending on it can be found. Two copies of a rule are not redundancy; they are a defect waiting for the first edit to one of them.

**Every rule has a check —** scripts check whatever the files alone decide, because they are deterministic and spend no tokens; independent AI agents perform the remaining checks, the judgment-based, semantic ones that only they can; and a rule that leaves no trace in the files, such as reading a file fresh before editing it, is a named step of the skill that applies it.

**Governed by its own process —** like a self-hosting compiler that compiles itself, Spec of Record is specified, changed and audited by its own method, and that use has shaped it: when its own rule changes kept leaving the specs written under them out of step, it gained a step that records that impact before any rule change is approved.

**Not tied to one AI vendor —** the instructions and skills are written for any agent to follow, or a person to read directly. Optional helpers wire them into a specific tool.

## How an engineer and AI agents work together

Every change beyond a small edit the engineer approves directly runs the same loop, and each step exists because skipping it once cost something. The engineer is the human in the loop: agents author, review and audit, but nothing is approved, applied, fixed or committed without the engineer's decision.

- **Design, Refactor, Refine —** the agent authors each change as a design document starting from the problem it solves, restructured until it stops moving, then refined for clarity and elegance: the fewest, simplest instructions that do the job.
- **The engineer designs, the agent authors —** the software engineer designs each change with the agent and decides what it is. Those decisions are recorded in the engineer's own words, so reviewers check the design against what was decided rather than reopening it.
- **Measure twice, cut once —** the authoring agent checks its whole work before any review, as a software engineer would rather find their own defect than have QA find it.
- **An adversarial reviewer —** a separate AI agent, with none of the authoring agent's context and so none of its builder bias, reviews the design for what is over-engineered and for what is under-engineered. The engineer chooses the reviewer's model and reasoning effort.
- **Validation and approval —** another fresh agent checks that the design's record matches what it does, and stamps it with a content hash; the engineer then approves it, approves it and has it applied, or keeps it in progress.
- **Apply, audit, commit —** the approved change is applied, then audited, by script and by a fresh agent, and committed as one change on the engineer's go-ahead. The engineer settles each finding: a tactical fix is made only once the engineer approves it, and a flaw sends the design back; three review rounds in a row with flaws stop the work for the engineer to reassess, so review cannot spiral unnoticed.

## Where it is going

Spec of Record can now specify, evolve and audit itself. Its next two phases take it to code.

**Next, generating code from the specs —** an annotation and two skills, designed in sequence, the annotation first:

- **`@app-spec` —** an annotation through which code names the specification sections it carries out, the missing link between spec and code in most spec-driven methods.
- **`implement-specs` —** generating code from the specifications.
- **`verify-spec-implementation` —** checking that code truthfully carries out its specifications.

**Then, reverse engineering specs from existing code —** so a team can bring a codebase it already has under the method:

- **`survey-specs` —** mapping an existing codebase into the areas that need specifications, and planning how each is inferred.
- **`infer-specs` —** reading one area's code and reverse engineering its specifications.

The thesis, that the specs can be the record a codebase is built from and checked against, will be tested on Apache Fineract, an open-source core banking platform, starting by reverse engineering its modules into specifications.

## PriceHorizon, the worked example

Revenue Growth Management teams live with a specific, recurring question: what will a competitor do on price, where should our own brand sit in response, and what happens to the business as a result. PriceHorizon is a proposed answer engine for exactly that question. A user types one plain-language sentence, for example, "in six months, where will Competitor Brand's price be in Texas, and what will happen," and the system returns a layered answer: a confidence-scored forecast, a plain-language explanation of what is driving it, a map of how the number breaks down by market, a decomposition of the underlying forces, a small set of positioning options rather than one imposed answer, and the simulated business outcome of each, with the ability to drill into any of it, down to a county or a single store, or across to a different metric.

Every answer is built to meet guarantees that make it trustworthy enough to act on. It is repeatable: the same question, asked again with nothing changed in between, returns the same forecast and figures. Every number traces to a named, versioned model or dataset. Qualitative information, such as regulatory changes and competitive intelligence, is weighed alongside the numbers, not appended as commentary afterward. And the answer shows how it was built: each forecast opens to the baseline and driver corrections it is the sum of, and each confidence figure to its reasons. Beneath all of them, where the evidence falls short the system says so, and where a term in the question cannot be resolved it asks rather than guessing.

PriceHorizon runs as a self-hosted installation inside each customer's own environment, co-located with their data. It needs no connection outside that environment, so an installation can run air-gapped, and nothing from one customer's installation is ever combined with another's.

It is a design project, not an implementation: there is no application code yet.

## What the specifications look like

- **Two layers that answer to each other —** `specs/application/product/` states what a user can rely on, and `specs/application/technical/` states how it is made true. Each names the other, so the two cannot drift apart silently, and the technical overview maps each layer of the answer to the mechanism that produces it.
- **Structure where prose would hide gaps —** where a rule or a process has to be checkably complete, it is written as one of an approved set of constructs, such as a decision table, a state machine or an algorithm, because prose can describe anything but cannot be checked for what it leaves out.
- **Unsettled decisions marked where they apply —** a decision the specs rely on but have not made is recorded as an open question in the file it affects, with the answer in use until it is settled and everything that depends on it, so it is never mistaken for settled prose.
- **A scenario for every promise —** each capability states, in Given, When, Then form, how each of its promises would be tested, so a promise that could never be checked shows up as one.
- **Diagrams that cite their sources —** and each source cites the diagram back, so a change to what a drawing shows points to the drawing that needs to follow it.

One fact, followed end to end: the product promises that every answer shows how it was built (`specs/application/product/trust-and-explainability/guarantees.md`), a scenario beside that promise states how it would be tested, `specs/application/technical/guarantees-mechanics.md` gathers the mechanisms that keep the promise, and the product overview's From Evidence to Answer diagram draws it, citing that promise as its source.

## How to read this repo

For the method, start with `specs/AGENTS.md`, its entry point, and `specs/methodology/architecture.md`, an overview of its rules. For PriceHorizon, start with the two overviews: `specs/application/product/architecture.md`, what a user experiences and can rely on, and `specs/application/technical/architecture.md`, how it is made true, each with diagrams. Every directory under `specs/` has an `index.md` listing what it holds, and `specs/index.md` maps them as a whole. The skills that carry the method out are under `.ai/skills/`, each recording the failures that motivated it. To try the method, have your agent read `specs/AGENTS.md`, which sends each change to the skill that carries it out. The design documents, review reports and list of work still to do are working files, kept out of version control on purpose: what they settle reaches a reader only through the specs.

## Set up AI skills for Claude Code

Optional, for Claude Code users. The skills live in `.ai/skills/` so any agent can read them. These scripts link that directory to `.claude/skills/` so Claude Code loads them natively. Each is safe to re-run, and the link is gitignored.

Windows, using a directory junction:
```
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\setup-claude-skills.ps1
```

Mac or Linux, using a symbolic link:
```
sh scripts/setup-claude-skills.sh
```

## License

The specifications, methodology and documentation are licensed under [CC BY 4.0](LICENSE). The scripts under `.ai/skills/*/scripts/` and `scripts/` are licensed under the [MIT License](LICENSE-CODE).

Attribution: "PriceHorizon by Billy Atkins, https://github.com/billy-atkins/price-horizon"

## Author

Designed by [Billy Atkins](https://www.linkedin.com/in/billy-atkins) and authored by AI agents, as an applied exercise in spec-driven system design.

I'm an engineering leader who has spent over twenty years building software, and the platforms and teams behind it, most recently leading platform engineering for a cloud core banking platform, where I also helped engineering teams adopt AI. Spec of Record is built from what that work taught me:

- **A declarative source of truth —** years of Terraform taught me to trust a declared state that the real thing is brought in line with, changed only through a reviewed plan before anything is applied. A specification in Spec of Record is that declared state, and a design document its reviewed plan.
- **Structured descriptions can build software —** I built frameworks that generated service layers, data access and administration screens from structured metadata. The method's modeling constructs carry that idea: metadata describing what should be built.
- **Validate the definition, not only the request —** I designed a highly configurable reporting engine that validated every report definition as defect free and faithful to what its author meant before any report ran against it. Spec of Record validates its specifications the same way, by script and by review, before anything is built from them.
- **Rigor sized to the stakes —** on a core banking platform processing hundreds of millions of transactions a day for hundreds of financial institutions, a defect has severe consequences. A flaw in a core specification is like a flaw in a mint's engraving plate, reproduced on every banknote it prints.
- **Tests from the specs, and audited AI skills —** I led a team generating Gherkin scenarios and Playwright tests with AI, and wrote AI skills that audit a shared skills library against its standards. In Spec of Record every product promise carries a Gherkin scenario, its specs and skills are audited the same way, and PriceHorizon's code-generation phase will generate Playwright tests from those scenarios.
- **Every builder has blind spots —** design reviews, code reviews and QA engineers with a breaker mindset caught what I could not see in my own work. The method gives every change an independent adversarial reviewer for the same reason.
- **Use your own tools —** at a SaaS company, we ran our own time-keeping product internally and learned more from that than from any client report. Spec of Record was built with itself first.
