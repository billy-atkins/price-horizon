# PriceHorizon, built with Spec of Record

Spec of Record is a spec-driven development methodology for building software with AI agents. The specifications are the durable source of truth. They say what a system does and why, and they stay current through every change. A software engineer designs each change with an AI agent, and the agent writes it. The engineer makes every decision about what the change is, and approves all of the work the AI agents do: the designs, the plans and the implemented work. Code is built from the specifications and checked against them.

This repository holds two sets of specifications. The methodology specifications state the rules of Spec of Record. PriceHorizon, the worked example, is an AI answer engine for competitive pricing, written and governed with Spec of Record: its product specifications state what a user can rely on, and its technical specifications state how the system makes that true. PriceHorizon and Acme AI, the SaaS company behind it, are fictional. The methodology, and the rigor applied to it, are real. Spec of Record and PriceHorizon are both the work of [Billy Atkins](#author).

## At a glance

- Applications drift from their documentation, because nothing links the two explicitly. Most spec-driven methodologies write a single-use specification for each change, so the drift begins with the next change.
- Spec of Record keeps one set of specifications of the system as it stands, and designs every change against it.
- The specifications record why the system behaves as it does, as well as what it does.
- Each fact has one home, and everything relying on it cites that home.
- Structured forms, called constructs, take the place of prose wherever prose would hide a gap.
- Every rule has a check, by a script where a script can decide and by an independent AI reviewer where it takes judgment.
- The methodology evolves through the rules and constructs it defines and the AI skills that apply them, as a self-hosting compiler compiles itself.
- PriceHorizon has no code yet. Generating it from the specifications is the methodology's next phase of evolution.

## Why it matters

Documentation drifts because nothing ties it to the system it describes. Most spec-driven methodologies do not stop that drift. They treat a specification as the prompt for one change: it generates the code, and then it is discarded or filed with the other per-feature documents. The drift begins on the next change. Like a ticket history, the pile of documents records each change. To learn what the system does today, a reader replays every change and hopes none contradicted another.

AI agents raise the stakes. An agent's prose reads as fluent and authoritative even where it is wrong, and it can read as complete while it leaves cases out. An agent that edits one copy of a rule stated in two places leaves the other copy stale, and nothing notices.

Spec of Record works differently. Its specifications describe the system as it stands, and each change is designed against them. Extending a building works the same way. The engineers extend the building's plans and check the new work against what is already there. An issue caught before the concrete is poured costs far less than one found after the foundation has cured. The specifications become the layer of record, and code becomes an implementation detail beneath them, as the JVM is beneath a Java program.

In Spec of Record, why a system behaves as it does is as important as what it does. The code tells an engineer or an agent what. The why often lives only in old Jira tickets, or in the mind of an engineer who has worked on the application for years. Without it, an application is hard to evolve. A change can lose or break important behavior when nobody knows why it is there. Spec of Record makes the why a core part of the methodology. The product and technical specifications state the why beside the what, where the reason arises naturally. Structured Design Decisions, coming to the methodology, will record the choices whose reasons the specifications do not otherwise hold.

## How the methodology holds together

In software design, DRY, short for "Don't Repeat Yourself", keeps each piece of knowledge in one place. Andrew Hunt and David Thomas, in "The Pragmatic Programmer", define it as every piece of knowledge having a single, unambiguous, authoritative representation within a system. A change is then made once, no copy can drift from another, and a reader always finds the authoritative version. Spec of Record applies DRY to specifications. Every rule and definition is stated once, in its home. Everything relying on it cites that home down to the section, with a point-of-use citation placed where the rule is applied. A change then lands in one place, and every place depending on it can be found through its citations. Diagrams and overviews restate their sources the way a materialized view restates its tables. They are kept in sync whenever a source changes, and they are never the source of what they restate.

Where prose would hide a gap, the specifications use constructs. A rule decided by one fact, with at most two outcomes, stays prose. Anything more takes one of an approved set of constructs, drawn from standards an engineer or an agent already knows: the DecisionTable of DMN, the Decision Model and Notation standard, and UML's StateMachine, Activity and Constraint. Every expression is written in FEEL, DMN's expression language. Prose can describe anything, and nothing can check it for what it leaves out. The audit script parses FEEL's whole grammar, so a rule that tests a value nothing defines, or compares a date with a price, is caught before anyone reads it.

Every rule has a check. A script checks whatever programming logic alone can decide, since a script is deterministic and spends no tokens. An independent AI agent makes the checks that require judgment. A rule that leaves no trace in the files, such as reading a file fresh before editing it, is a named step of the skill that applies it.

Product capabilities state, as Gherkin scenarios in Given, When, Then form, how their promises would be tested. A promise that could never be checked then shows up as one. A decision the specifications rely on but have not made is recorded as an open question in the file it affects. The question carries a provisional answer the work moves forward on, so it never blocks the work and is never mistaken for a settled decision.

Spec of Record evolves the way a self-hosting compiler is built, by compiling its own source. Its rules are written in the constructs it defines. Every change to them is designed, reviewed and audited with the same AI skills and tooling that design and author application specifications. So although PriceHorizon has no code yet, the methodology is in real use. Its own rules and PriceHorizon's specifications are both written and governed through it.

## How an engineer and AI agents work together

Every change runs the same workflow, except a small edit the engineer approves making directly. Each step exists because skipping it once cost something. The engineer is the human in the loop. Agents author, review and audit, and nothing is approved, applied or committed without the engineer's decision.

Every change starts with its design goals: what the change must achieve, agreed on in discussion between the engineer and the agent. The agent then proposes the design frame, which sets the scope, the approach and the outcomes the draft will be judged by. The engineer agrees to the frame or adjusts it. The goals and the frame are the engineer's to decide, so a later decision that changes either is confirmed with the engineer before the work goes on. Each decision is recorded in the engineer's own words, so a reviewer checks the design against what was decided instead of reopening it.

The agent writes the design as a design document, a plan that holds the change from its problem to its edits, and works it through the Design, Refactor, Refine process. It first drafts a solution that works. It then restructures the draft until the structure stops moving, and finally refines the solution for clarity and ease of use. Before each edit, the agent reads outward to see how far the rule it touches reaches. Before any review, it checks its whole work and traces every path through each state machine or other flow its edits change, just as a software engineer would rather find a defect in their own work than have QA find it.

A separate AI agent then reviews the design adversarially. It starts cold, with none of the authoring agent's context, so it shares none of the authoring agent's bias. A reviewer on a different model can also see past blind spots the two would share. The reviewer looks for what is over-engineered and what is under-engineered, judged against the goals agreed on, and marks each finding a design flaw, an implementation flaw or a nit. A design flaw is a fault in the design goals or frame, and it goes to the engineer with the agent's recommended change to them. An implementation flaw is a fault in the edits that carry the goals and frame out, and a nit is a minor finding, such as one of wording or order. The authoring agent settles those itself, grouping each round's findings by the decision they touch and fixing them at their causes. Where findings keep landing on one mechanism, the agent rewrites it whole instead of patching it again.

A round that finds a flaw is followed by another, which checks the fixes. The review converges at the first round that finds only nits the authoring agent judges harmless, or nothing. A nit that would harm what is built counts as an implementation flaw.

The workflow's rigor scales with the change. Each design names its kind: a change to the methodology, the application specifications, code, documentation or other files. Its kind sets the reasoning effort its reviews take by default, the most for the methodology, whose flaws reach every specification written under it, and the least for documentation, whose flaws reach no further. The engineer chooses the model the reviews run on and can change the effort.

Review cannot spiral unnoticed. A run of three rounds with a design flaw, or of five with an implementation flaw, stops the work, and the engineer and the agent step back to reassess.

Once the review has converged, a script validates the design document. It checks the document's form and its records, that each edit still applies to its file, and that everything the document cites exists. It never judges whether the design is right, which the review has done. The script stamps the record with a content hash, and the engineer approves the design, approves it and has it applied, or keeps it in progress. The engineer can also approve the design's text before the review converges, which ends the review. A later change to the text brings the design back to the engineer to approve again.

The approved change is applied, then audited by script and by another fresh agent, over the files the design's kind sets. The engineer decides how each audit finding is settled. A small fix is made as a direct edit once the engineer approves it. A finding that exposes a design flaw, or an implementation flaw no direct edit fixes, sends the design back with its changes reverted. Once its audit is settled, the change is committed on its own, on the engineer's go-ahead. A run of three audits that send it back stops the work, and the engineer and the agent step back to reassess.

## PriceHorizon, the worked example

Revenue Growth Management teams face a recurring question: what will a competitor do on price, where should our own brand sit in response, and what will happen to the business as a result? PriceHorizon is a proposed answer engine for that question. A user types one plain-language sentence, such as "in six months, where will Competitor Brand's price be in Texas, and what will happen?" The system returns a layered answer. The answer opens with a confidence-scored forecast and a plain-language explanation of what drives it. It maps how the number breaks down by market, and decomposes the forces beneath it. It offers a small set of positioning options instead of one imposed answer, each with its simulated business outcome. A user can drill into any part of it, down to a county or a single store, or across to a different metric.

Every answer is built to meet guarantees that make it trustworthy enough to act on. It is repeatable: the same question, asked again with nothing changed in between, returns the same forecast and figures. Every number traces to a named, versioned model or dataset. Qualitative information, such as regulatory changes and competitive intelligence, is weighed alongside the numbers instead of appended afterward as commentary. The answer also shows how it was built. Each forecast opens to the baseline and the driver corrections it is the sum of, and each confidence figure to its reasons. Where the evidence falls short, the system says so, and it asks about a term in the question it cannot resolve instead of guessing.

PriceHorizon runs as a self-hosted installation inside each customer's own environment, alongside their data. It needs no connection outside that environment unless the customer lets some kinds of model call reach a frontier model provider, and it runs air-gapped where the customer requires. Nothing from one customer's installation is ever combined with another's.

Its product specifications reach across the product, from the answer engine to identity and access, tenant administration, and platform and compliance operations. Its technical specifications reach the data model, the services, the model registry, the stack and the environments.

## Finding your way around

The methodology specifications, the specifications' entry point and overview, and the skills the methodology registers to apply its rules, with the code those skills share, together form the canon: the part of the repository that states and applies the methodology's rules. The application specifications, PriceHorizon's product and technical specifications, are written under the canon, and the canon is written under its own rules, as a self-hosting compiler compiles itself.

```
AGENTS.md                   the project's instructions for any AI agent
README.md                   this file
specs/
  AGENTS.md                 the entry point, where every change starts
  architecture.md           the overview of the specifications as a whole
  index.md                  the map of the specifications
  methodology/              the rules of Spec of Record
    glossary.md             the terms the methodology gives a meaning of its own
    architecture.md         the overview of the rules
  application/
    product/                PriceHorizon: what a user can rely on
      architecture.md       the product overview, with diagrams
    technical/              PriceHorizon: how it is made true
      architecture.md       the technical overview, with diagrams
.ai/skills/                 the skills that carry the methodology out
docs/                       user documentation, still to come
```

Every directory under `specs/` holds an `index.md` listing what it holds. An overview, an `architecture.md`, describes how the files of its directory fit together, and the glossary defines each term the methodology gives a meaning of its own. The `AGENTS.md` files are the agent instructions, what an AI agent reads before it works here.

Each part is written for its reader. The product specifications are written for a product owner, and the technical specifications for a software engineer. The methodology specifications are written for a practitioner: a software engineer designing a project's specifications. The agent instructions and the skills are written for an AI agent arriving with no context but what it reads, and any agent can follow them.

The skills under `.ai/skills/` carry the methodology out. Each is a set of instructions any AI agent can follow, with scripts wherever programming logic alone can decide, and each records the failures that motivated it:

- `design-specs` takes a change to any set of specifications, the methodology's or an application's, through the Design, Refactor, Refine process as a design document, and runs Refactor and Refine cycles over specifications that have already landed.
- `audit-specs` checks the specifications, the agent instructions, the skills and this README against every rule that governs them. Its script clears what programming logic can decide, and a reading audit judges the rest, from an overview that has fallen behind its files to a rule stated twice.
- `implement-specs` designs the code for one product module from its specifications, takes that design through the same reviews as a change to the specifications, and then writes the code, its tests and the wiring between them.
- `verify-spec-implementation` checks that code carries out the specifications it cites. Its script checks the annotations and lists the sections no code cites, and an independent agent judges the rest. It reports what it finds and changes nothing.
- `author-mermaid-diagram` writes and revises the diagrams, keeps each in sync with its sources, and renders each before it ships.
- `configure-spec-of-record` sets up the agent in use for what Spec of Record leaves to it, such as running a review at the reasoning effort the engineer chose.

The product and technical specifications answer to each other. The product layer is the building architect's drawing: everything a person using the building experiences. The technical layer is the structural engineer's: how the building is built and stands safely, inventing no feature the architect did not draw. Each layer names the other, so the two cannot drift apart silently. Diagrams cite their sources, and each source cites the diagram back, so a change to a fact a diagram shows points to the diagram that must follow it.

One fact shows how the pieces fit. The product promises that every answer shows how it was built ([`specs/application/product/trust-and-explainability/guarantees.md`](/specs/application/product/trust-and-explainability/guarantees.md)). A Gherkin scenario beside that promise states how it would be tested. [`specs/application/technical/guarantees-mechanics.md`](/specs/application/technical/guarantees-mechanics.md) gathers the mechanisms that keep the promise. The product overview's From Evidence to Answer diagram draws it, citing that promise as its source.

For the methodology, start with [`specs/AGENTS.md`](/specs/AGENTS.md), then [`specs/methodology/glossary.md`](/specs/methodology/glossary.md) and the overviews. For PriceHorizon, start with its product and technical overviews. The design documents, the review reports and the list of work still to do are working files, kept out of version control on purpose. What they settle reaches a reader only through the specifications.

## Try it

Some of the methodology only shows in use, so the best test is to take a change through it with your own AI agent. The skills' scripts run on Python 3, and a Claude Code user can link the skills beforehand, as [Set up AI skills for Claude Code](#set-up-ai-skills-for-claude-code) describes. Have the agent run `configure-spec-of-record` first, so it is set up for what Spec of Record leaves to the agent in use. Then have it read [`specs/AGENTS.md`](/specs/AGENTS.md), which sends each change to the skill that carries it out, and ask it for a change to one PriceHorizon capability, such as a new guarantee an answer makes. The agent starts by agreeing on the change's design goals with you.

## Where it is going

Spec of Record now governs the code built from its specifications. Its first tools for code are available now: `@app-spec`, an annotation through which code names the sections of the specifications it carries out or checks, and the skills `implement-specs` and `verify-spec-implementation`. The annotation is the link between specifications and code that most spec-driven methodologies lack.

PriceHorizon's code comes next. It will be generated from its specifications once they are rewritten in the constructs as the methodology now defines them, on the stack and environments its technical specifications set. Its Playwright tests will be generated from its Gherkin scenarios. The methodology will also gain structured Design Decisions, and a way to draft an open question's provisional answer and bring it to the engineer.

After that comes reverse engineering specifications from existing code, so a team can bring a codebase it already has under the methodology. `survey-specs` will map an existing codebase into the areas that need specifications and plan how each is inferred. `infer-specs` will read one area's code and reverse engineer its specifications. The thesis is that specifications can be the record a codebase is built from and checked against. It will be tested on [Apache Fineract](https://github.com/apache/fineract/), an open-source core banking platform, starting by reverse engineering its modules into specifications.

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

The specifications, methodology and documentation are licensed under [CC BY 4.0](LICENSE). The scripts under `.ai/skills/*/scripts/`, `.ai/skills/lib/` and `scripts/` are licensed under the [MIT License](LICENSE-CODE).

Attribution: "PriceHorizon by Billy Atkins, https://github.com/billy-atkins/price-horizon"

## Author

Designed by [Billy Atkins](https://www.linkedin.com/in/billy-atkins) and authored by AI agents, as an applied exercise in spec-driven system design.

I am an engineering leader who has spent over twenty years building software, and the platforms and teams behind it. Most recently I led platform engineering for a cloud core banking platform, where I also helped engineering teams adopt AI. I have engineered framework capabilities that other engineers used to build applications and systems. Spec of Record continues that theme for designing and building applications and systems through the agentic software development life cycle, the agentic SDLC. It is built from what that work taught me.

### Teaching through analogies

I teach through analogies. In my personal and professional life, I bring an audience to a new concept through something they already know, and what is familiar always depends on who is listening. Spec-driven development is not yet an established industry practice, so its ideas need that framing. That is why Spec of Record holds analogies. A building architect draws what people experience, and a structural engineer draws how the building stands. That pair shaped the split between product and technical specifications. Minified code, shorter than its source and unreadable, shows why prose cut too far fails its reader. The Rube Goldberg machine and the Potemkin village name two of the failures the adversarial review looks for: a mechanism far more elaborate than its task, and a front with nothing behind it.

### Lessons from systems I built

Years of Terraform experience taught me the value of a declared definition. A Terraform configuration, written in its own domain-specific language, first describes the infrastructure an engineer wants. Terraform generates a plan, the engineer approves it, and Terraform applies it. The configuration then describes the infrastructure as it now stands. Every change takes the same path: amend the configuration, generate the plan, approve and apply it, and the infrastructure and its configuration are in sync again. Spec of Record works the same way. The engineer designs the change to the specifications, an agent generates an implementation plan, the engineer approves it, and the plan is applied, so the code is in sync with the specifications again. Terraform keeps a state file as its memory of what it built from each part of the configuration. In Spec of Record, the `@app-spec` annotations do that job. They link the code to the specifications that govern it, so an agent never has to infer which specifications govern which code.

I also built frameworks that generated service layers, data access and administration screens from structured metadata. The methodology's constructs carry that idea: metadata describing what should be built. I designed a highly configurable reporting engine that validated that every report definition was free of defects and faithful to what its author meant, before any report ran against it. Spec of Record validates its specifications the same way, by script and by agent review, before anything is built from them.

Spec of Record is not my first spec-driven approach. It is built with the lessons I learned from my previous spec-driven development efforts. In one of them, I discovered the need to nudge an agent at the moment a rule applies. People and agents alike apply an instruction best when it is in front of them as they work. A playbook does this: each step links to the detailed procedure it carries out. That is why Spec of Record places point-of-use citations in its natural workflows, each step citing the single home of the rule that applies there.

### Rigor, review and testing

On a core banking platform processing hundreds of millions of transactions a day for hundreds of financial institutions, a defect has severe consequences. A flaw in the methodology specifications is like a flaw in a mint's engraving plate, reproduced on every banknote it prints: every set of specifications written under them carries it. Rigor still has a point of diminishing returns. Lint on a moving blanket that protects furniture in transit harms nothing, while lint on a sterile cloth holding surgical instruments can harm a patient. A design document is the blanket, discarded once its change lands, so a nit left in it costs nothing. The applied specifications are the sterile cloth, so every finding in them is settled.

Every builder has blind spots, me included. Design reviews, code reviews and QA engineers with a breaker mindset caught what I could not see in my own work, so the methodology gives every design an independent adversarial reviewer. In earlier work, I wrote AI skills that audit a shared skills library against its standards. That experience shaped how Spec of Record audits its own specifications and skills.

Testing from the user's perspective came from a gap I found in a previous application. We had many internal tests for parts of our workflows, and none for the workflows our users followed. I led a team that generated Gherkin scenarios and Playwright tests with AI, from the application code, the user documentation and the OpenAPI definitions, and that let us test the application as its users experience it. The user's perspective is one of the most important tests, since the system exists largely for its users' benefit. A restaurant can test every ingredient of a complex dish and find each one good, and the dish can still disappoint the patron who orders it. Testing each ingredient matters, since a bad one can spoil the dish or harm the diner. Testing the finished dish matters too. That is why Spec of Record asks for a Gherkin scenario for every product promise, and why PriceHorizon's code will come with Playwright tests generated from those scenarios.

### How I work

I build each design in passes. I first get it logically working. I then refactor it for structural improvements until it settles, and finally refine it for elegance and ease of use. That became the Design, Refactor, Refine process. In racing, smooth is fast: sloppy work turns out slow, and methodical, correct work turns out fast. That became Measure twice, cut once, in which the authoring agent checks its own work before any reviewer sees it. As an enterprise architect, I learned that no solution can be evaluated until the people building it agree on its goals. So every design in Spec of Record starts from goals the engineer and the agent agree on.

I enjoy solving complex problems with elegant solutions. Spec of Record is one of those problems, and elegance, complexity minimized and never hidden, is the aim of every change to it. I also work as Eric Ries's Lean Startup describes: build, measure, learn, with feedback from real use. At a SaaS company, we ran our own time-keeping product internally and learned more from that than from any client report. Spec of Record was built with itself first. Generating PriceHorizon's code, and then the Fineract test, are the next turns of that loop.
