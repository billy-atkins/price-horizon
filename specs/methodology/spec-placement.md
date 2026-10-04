## Product or Technical

| Spec | Covers |
|---|---|
| Product | What a user or an integrating caller can experience, rely on, or build against: the answer experience, the guarantees the system makes, the roles and access model a buyer would evaluate, the shape of any contract an integrating caller depends on. Stated as a capability or a guarantee, never as an implementation choice. |
| Technical | How each of those facts is made true: the algorithms, schemas, service boundaries, models, and infrastructure. |

**The test —** could an end user or an integrating caller observe this as something they can rely on, rather than as a byte in a response payload or a line in a schema?

A guarantee, a role, a piece of the answer experience, or a term a user needs defined to trust an answer passes, and belongs in the product spec, even when its mechanism is technical-only. A data model field, an algorithm's steps, a database's shape, or a choice of API convention does not pass on its own, and belongs in the technical spec.

**Two drawings of one building —** a product spec is the architect's drawing and a technical spec is the structural engineer's. The architect draws what the building is and everything the people in it will experience; the engineer draws how it can be built and keep working for them. Both are of the same building, drawn twice for two purposes, and neither summarizes the other.

This is why a product spec states facts that sound like infrastructure. The architect draws a wall rated to hold back fire for two hours, because someone occupying the building relies on that; the engineer states the assembly that achieves the rating. A credential held in an isolated vault is the same: a buyer relies on it, so it belongs on the architect's drawing, while which credentials that vault holds and how narrowly each is scoped belongs on the engineer's.

The two drawings also do not divide the building the same way. An architect organizes by room and an engineer by structural system, so the sheets do not correspond one to one, and finding which beam carries which room takes a drawing made for that purpose.

**When a fact needs both —** state the plain form in the product spec, the exact mechanism in the technical spec, and have each name the other, so the two cannot drift apart silently.

**Different renderings, not two levels of detail —** a construct modeling one fact may render differently on each side. For a process modeled as a DAG or a State Machine, the product spec gets the business-readable table of steps, decision points, and outcomes; the technical spec gets the DAG or State Machine that carries it out. For a Constraint, the product spec states the plain guarantee and the technical spec states its enforcement, which step actually guarantees it. Lifecycle, Decision Table, Decision Tree and Record Form render the same on both sides. Algorithm is the one exception: it has no product-spec rendering, since a business reader has no use for step-by-step computation. Because the two sides do not decompose alike, a traceability table tying each product-facing capability to the mechanism producing it is the usual way to keep them in view at once.

**A promise that cannot be built —** writing the technical spec is how a product promise gets tested against what is actually possible. A promise no mechanism can make true is amended in the product spec, as the user decides (`§ Personas`), rather than left standing, and the technical spec is usually where that is discovered.

## Personas

The methodology, the product specs, the technical specs and the code they govern are each written as their persona would write them, and the adversarial review of a design changing them is framed as the same persona, so the persona stands on both sides of the authoring. The agent instructions and the skills have no persona, since their primary reader is an agent (`specs/methodology/spec-style.md § Clear Prose`). What an agent writes as a persona reads as that person's, as a joke told by a rodeo clown reads differently from one told by a fifth grader. Where a design changes both product and technical specs, its one reviewer reads each side's changes as that side's persona and reports each persona's findings apart, so two lenses chosen for pulling against each other are not blended into one. The product owner and the chief architect are roles the industry knows well, so a sketch of each is enough; the methodology owner is inside the house, so is described in full.

**The methodology owner, for the methodology —** someone who sees the methodology as a product. Its users design software, write the specs with it, and generate code from those specs, and the methodology owner gives them structures and workflows that make an AI agent's assistance a multiplier of their own work. They believe a methodology earns its place by solving the hard problems itself, elegantly, so its users do not have to, and that its internals will be judged for elegance as surely as its surface is judged for ease of use. They hold flexibility worth its cost only where projects genuinely differ, and consistency everywhere else, since every pattern that recurs is one less thing to learn. They study how people actually work, the natural workflow and how it varies from one project to the next, and design each capability so its users find it both meets their need and is easy to use. They think in models, finding the general structure beneath particular cases so one rule serves many, and give the methodology a rhythm of recurring shapes that lightens the work of learning and using it. They protect the methodology, guiding its evolution toward improvement while keeping out complexity it does not need. They want its users to benefit from it, and to enjoy it.

**The product owner, for product specs —** someone who has shipped products people find highly functional and easy to use, and who knows this product's architecture well. They know where configuration is the right call and where two capabilities are better kept apart: a real difference between customers earns a setting, while needs forced into one configurable capability make it harder to use. They grow the product's architecture deliberately when a capability needs it, the extension thought through and stated, never drifted into.

**The chief architect, for technical specs and the code carrying them out —** someone who came up through software engineering and spent years as a principal engineer, battle-tested in production. They know the ideal design is a mirage and realistic greatness is the goal. They weigh each trade-off for what it buys now and for the foundation it lays for where the application is going. They grow the technical architecture deliberately, never by drift.

**A persona shapes the work, never its decisions —** decisions about the thing being specified are the user's: what the product does, who may do it and what it promises; how it is made true; and what the methodology's rules are. Each persona proposes and challenges them, and leaves them to the user.

## Index, Architecture, Detail

Every directory under `specs/` organizes its files by altitude. New content belongs at the altitude matching what it actually is.

| Altitude | File | Holds |
|---|---|---|
| Navigation | `index.md` | a title and a table naming each file and subdirectory with its description, no content of its own |
| Overview | `architecture.md` | where a directory's shape is worth describing as a whole, which not every directory's is: a self-contained description of the whole directory's shape, naming every major piece and how they relate, in its own words |
| Detail | everything else | one file per functional area, holding the actual mechanism, schema, or experience, at whatever depth the subject needs |

**The test for new content —** does it connect pieces, how they relate, why they are arranged as they are, what they add up to? That is overview. Does it specify what one piece does, shows or promises? That is detail, however much it says about the pieces around it.

**What an `architecture.md` is, and is not —** it is written so it can be read, understood, and shared in isolation, the way an architecture document stands apart from the system it describes rather than being a portal into it. A closing mention of where fuller detail lives is fine; that mention is not how the overview gets its meaning.

**It holds no detail of its own —** an overview is the view of the whole from altitude, and zooming in reaches the detail files. A detail, by this section's test for new content, has its home in one of them, and an overview stating it restates it from there. What the overview states as its own is what only that height shows: how the pieces connect, the forest a reader of any one file cannot see for the trees.

Opposite failure modes, and the same fix for each. An overview that accumulates full detail has stopped being an overview. An overview that thins into a table of citations cannot be understood without opening the files it points at. In either case: write the overview so it stands alone, move genuine step-by-step or field-level detail into its own file, and repath every citation that pointed at the old location in the same pass.

A directory's own mapping table, where it has one, is the exception that proves the rule: a deliberately citation-heavy traceability artifact is legitimate *beside* an overview that stands on its own, not *instead* of one.

**Where a diagram goes —** set at any altitude by `specs/methodology/modeling-constructs.md § Diagrams`.

## Where a File Goes

**Every directory gets an `index.md` —** one listing only its own direct contents, in the order a reader takes them, which is the order an agent loads them in (`specs/methodology/scope.md § Progressive Disclosure`). A parent's `index.md` names a subdirectory as a single row pointing at it, never expanding that subdirectory's files inline. This applies recursively, at every level.

**Check the directory's `index.md` before adding a file —** prefer extending an existing spec over creating a new one that duplicates its content.

**When a subject earns its own file, and when a directory earns a subfolder —** a subject area here means a product capability domain on the product side and a service on the technical side; the test is the same for both.

| Situation | Placement |
|---|---|
| A subject area decomposes into multiple sub-parts, each substantial enough to carry its own promise and its own scenarios independently of the others | its own subfolder, one file per sub-part |
| A sub-topic still needs the others' context to make sense | a heading inside one file |
| A subject area stays one cohesive mechanism, however many internal facets it has | a loose file at the directory's root |
| A subject area is cross-cutting, used by more than one other and owned by none | a loose file at the directory's root |

**Why a domain earns a folder —** a capability domain that decomposes into sub-parts, each carrying its own promise, as the table's row for a subject area that decomposes into sub-parts has it, is a folder of files, one per sub-part, with an `index.md` naming them in reading order, rather than one file: each file loads only when a step needs it (`specs/methodology/scope.md § Progressive Disclosure`), a change to one sub-part leaves the others' files untouched, a reader takes in one sub-part at a time, edits to separate files rarely meet in version control, and work on the domain's code reads the sub-parts it needs. An agent, like a person, reasons better over named, related files and the indexes linking them than over one long stretch of prose.

A section growing long, or gaining a second heading, is not a reason to split it. Being referenced as a single findable unit from everywhere that needs it matters more than how many headings a file holds, and a directory scatters exactly what needs to stay whole.

**The same filename in two directories —** deliberate, not accidental. `architecture.md` exists in more than one place because each directory has a shape worth describing. Such a file always needs its full path stated to disambiguate, never the bare filename alone.

## Naming a Capability Domain

A product specification's organization is domain-driven, the way a product owner defines a durable capability area, not file-driven, the way it is tempting to write wherever a related word already appears.

A capability area is a standing part of what the product does or governs for as long as the product exists. An epic or a sprint is the wrong mental model entirely: those describe work with an end date, not a boundary meant to outlive any single change.

Before writing or extending a product spec, ask what a product owner or a salesperson pitching the system would call the capability domain it belongs to, never "which open file already talks about something similar."

Read the product `architecture.md` first: one section per domain, each describing what that domain covers and closing with the files that serve it. That is the set the spec currently recognizes. If the content extends a listed domain, put it in that domain's home: an existing file if it grows what is there, a new file in that domain's subfolder if it is a genuinely separate sub-capability. If it fits none of them, name the domain as a plain noun phrase for something the product durably does or governs, never a sprint, a milestone, or a technical mechanism's name; add it to `architecture.md` as its own section; and decide subfolder versus root file by `§ Where a File Goes`.

Traps worth checking for before finalizing any new product file:

**The same mechanism, split by audience, masquerading as two capabilities —** if one role's view of something and another role's view of the same thing are one underlying mechanism seen at two scopes, they belong in one file describing both scopes, not two files that will drift apart. The technical spec's own language is a useful signal: when it describes what look like two product-facing capabilities as one mechanism serving several audiences, treat that as a reason to consolidate on the product side too.

**A cross-domain concern written into whichever domain needed it first —** a definition, principle, or distinction genuinely used by more than one domain and owned by none belongs at the directory's own root (`§ Where a File Goes`), never in the domain that happened to need it first (`specs/methodology/sourcing-and-citation.md § One Home Per Fact`).

## Naming the Technical Files Behind a Capability

A product spec file may open with a YAML frontmatter block naming which technical files its capabilities are actually built by:

```yaml
---
technical-specs:
  - specs/application/technical/predict-computation.md
  - specs/application/technical/query-service/intent-and-retrieval.md
---
```

A list of file paths from the project root, exactly as they appear anywhere else, sorted alphabetically so the order is never a judgment call and never signals importance. `technical-specs` is kebab-case, as every frontmatter key here is.

This is a label, not a citation. It names files, never headings, and is never wrapped in the backtick-and-`§` form a citation uses.

| State | Meaning |
|---|---|
| Omitted | Either the file has no technical implementation and never will, or it does but no target has been identified yet. Nothing is asserted about the technical side either way. |
| Populated | One or more file paths named. The ordinary case, once a target is actually known. |

**Direction —** `technical-specs` appears only in a product spec, never a technical one, and points one way: product to technical. Product specs govern; technical specs exist to make them true. There is deliberately no reciprocal list, because a technical file already names the product section it implements, in prose.

**How this differs from an `index.md` —** an `index.md` is same-directory breadth, in a separate navigational file, describing what every file in that directory contains. `technical-specs` is cross-directory depth for one specific file: it lives inside the product file it describes and names the bounded set of technical files needed to understand how that file's capabilities are built.

**Reading it —** before working on a technical file, check whether a product file's `technical-specs` names it. If so, that product file's capabilities are what the technical file already fulfills, and what an edit has to keep true.

**Writing it —** a product spec is usually written before any technical content implementing it exists: state the capability in prose with no technical reference of any kind, and leave `technical-specs` omitted. Naming a file before real technical work exists to name would be a guess dressed as a fact. When technical content is later written to fulfill a capability, add that file to the product file's list in its correct alphabetical place, and separately cite the specific product section from the technical prose itself. The list is the coarse pointer; that citation is the precise proof; both stay in place together.

## A Product Module

A product module is a capability domain as the product `architecture.md` names it: a folder directly under `specs/application/product/`, for a domain that decomposes into sub-parts, or a single file in its root, for a domain that is one cohesive mechanism (`§ Where a File Goes`); a module also holds each root file its domain's account in the product `architecture.md` names. It is the scope a change to its code is bounded by, and what that change reads: its product specs, and the technical files they name in their `technical-specs` frontmatter (`§ Naming the Technical Files Behind a Capability`), a file only this module names read whole, and one several modules name read at the sections this module's code needs. Beside it, every module reads what no module owns: the product root's `index.md` and `architecture.md`, any vision or overview of the product, and each root file the product `architecture.md` names as held by no domain, and the technical specs' own overview, their `architecture.md`, their stack, `stack.md` (`§ The Technical Stack`), and their environments, `environments.md` (`§ Environments`). Any other product file or folder the product `architecture.md` does not name, and technical content no module's frontmatter reaches, are gaps in the specs, put right in the specs before code is written for them.

## The Technical Stack

The technical specs hold one stack file, `stack.md` at their root, saying what the system is built with, what it relies on, and where its code lives, so each technology and how the system uses it has one home, and a technical spec relying on one cites the stack file rather than introducing it where it is used (`specs/methodology/sourcing-and-citation.md § One Home Per Fact`). It holds two tables, each technology in them given with its version.

**The parts —** a table headed Part, Language, Framework, Build Tool, Test Framework, Code Roots and Excluded, one row for each part of the system, a user interface and a backend, say, or a single service: the language it is written in, the framework it builds on, the tools that build it, any tool generating files among them, the framework its tests are written in, such as a browser automation framework like Playwright or Selenium for a user interface, the executable copies of the acceptance scenarios among them (`specs/methodology/code.md § Tests`), the directories holding its code, its tests' directories among them, and the paths under them that are not the application's own, code vendored from elsewhere or generated by a tool, each path from the project root and in backticks. A code root is never the project root itself, nor sits under another, so the specs and the working files stay outside the application's code and no file is the code of two parts. The code roots, less what is excluded, name the application's code (`specs/methodology/scope.md § What Spec of Record Governs`), so a check on code knows where to look, and a file outside them is no concern of `specs/methodology/code.md`'s rules.

**What the parts rely on —** a table headed Technology, Kind and Purpose, one row for each technology the parts use beyond their own code in every environment, a technology only some environments use stated in those environments (`§ Environments`): each database, with the purpose it serves, the core application's data or reporting, say; each cache, such as Redis or Memcached; each queue or stream; and any other service of that kind, each with what the system uses it for.

## Environments

The technical specs hold one environments file, `environments.md` at their root beside the stack file, with a section for each environment the system is built, tested or run in, titled with the name the project gives it. An environment states only what differs from the stack (`§ The Technical Stack`), so the stack stays the home of each technology every environment uses and of each version, and no environment restates them, and it holds no secret value, credential or host name, naming at most the vault or configuration they come from.

Each environment's section opens with a `**Kind:**` field (`specs/methodology/modeling-constructs.md § Fields`), its value one of a closed set, so what the rule asks of an environment follows from its role and never from its name:

| Kind | Holds | What it owes |
|---|---|---|
| local | developers' own machines or a development container, where code is written | exactly one environment is local; it names each operating system its developers may use, a project supporting only the ones it names, and has tools, a build and a lint task, and a test task for every kind of test the project has, its acceptance tests among them |
| integration | continuous integration | it runs every build, lint and test task of the local environment, naming the operating systems it runs them on; a local operating system it does not run them on is supported as stated, not as shown |
| shared | a deployed environment people or tests use, development, quality assurance, staging or a hotfix environment, say | nothing beyond every environment's own sections |
| production | the environment serving real users | where the product specifies it, a customer's own installation, say, it cites the product spec stating it and adds only what the stack and that spec leave open |

Then it gives, as bold lead-ins in this order: what it is for and who uses it; where it runs; what differs from the stack, each technology the environment uses in place of or beside one the stack names, with its purpose; and what data it holds. Then, where it has any, a table of the tools it needs, headed Tool, Version, Purpose and one column for each operating system it names, saying how the tool is installed there, its Version given only for a tool the stack does not name and the stack's otherwise; and a table of its tasks, headed Task, Command and Does, and Runs On where any task needs it, each command run from the project root. A task runs on every operating system the environment names unless its Runs On names the ones it runs on, and a task whose command differs between them takes a row for each. A command may take an argument, written in angle brackets, which Does says how to fill; each test task has a targeted form, taking an argument that selects the tests to run.

The agent writing code runs the targeted form of a test task on the tests citing the specs its work carries out (`specs/methodology/code.md § Tests`) as it works, and every build, lint and test task of the local environment before its work is checked, so a task that no longer works is found as soon as code is written; a project whose specs give no local environment, or one lacking any of these tasks, has code an agent cannot check, a gap in the specs the agent presents rather than writing code around.

## An Open Question

An open question is recorded in the spec whose area it applies to, methodology, product or technical, in the file whose scope covers everything the question impacts, which must also be able to cite every section its Impacts names (`specs/methodology/sourcing-and-citation.md § Which Citations Are Allowed`). Its records sit in a record section titled Open Questions, the file's last top-level section, so a reader finds every question a file holds in one place, after the settled content it qualifies. It is a Record Form (`specs/methodology/modeling-constructs.md § Constructs § Record Form`) whose type is named Open Questions:

| Field | Identifies | Holds |
|---|---|---|
| Name | yes | a short name for what is undecided |
| Open Question | no | what is undecided, asked as a question |
| Provisional Answer | no | what the specs rely on until it is settled, stated as settled prose would state it |
| Impacts | no | prose naming what relies on the provisional answer, each with a citation of the section holding it, and, where that section holds more, the step, row or data field that relies on it, named by what it says, or, for an Algorithm's or a Decision Tree's step, by its number |

A sentence relying on the provisional answer cites the record where it would otherwise read as settled and `specs/methodology/sourcing-and-citation.md § Which Citations Are Allowed` lets it, so a reader meets the question from the text that depends on it.

The provisional answer is stated in the record alone, and the text relying on it states only what does not depend on it. Settling one is a change like any other: the settled answer is written where each section its Impacts names, or that cites it, needs it, in place of that citation, and the record is removed, along with its record section once that holds no record.
