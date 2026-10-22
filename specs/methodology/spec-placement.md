## Product or Technical

**Reference Key:** Spec

**Required:** Covers

| Spec | Covers |
|---|---|
| Product | What a user or an integrating caller can experience, rely on, or build against: what a user sees and does, the guarantees the system makes, the roles and access model a buyer would evaluate, the shape of any contract an integrating caller depends on. Stated as a capability or a guarantee, never as an implementation choice. |
| Technical | How each of those facts is made true: the algorithms, schemas, service boundaries, models, and infrastructure. |

**The test.** Could an end user or an integrating caller observe this as something they can rely on, rather than as a byte in a response payload or a line in a schema?

A guarantee, a role, a piece of what a user sees and does, and a term a user needs defined to trust what the product shows them all pass. Each belongs in the product spec, even when its mechanism is technical-only. A data model field, an algorithm's steps, a database's shape and a choice of API convention do not pass on their own. They belong in the technical spec.

**Two drawings of one building.** A product spec is the architect's drawing and a technical spec is the structural engineer's. The architect draws what the building is and everything the people in it will experience. The engineer draws how it can be built and keep working for them. Both drawings are of the same building, drawn twice for two purposes. Neither summarizes the other.

This is why a product spec states facts that sound like infrastructure. The architect draws a wall rated to hold back fire for two hours, because someone occupying the building relies on that. The engineer states the assembly that achieves the rating. A customer's data encrypted at rest is the same case. A buyer relies on it, so it belongs on the architect's drawing. Which keys encrypt it, and how often they rotate, belongs on the engineer's.

The two drawings also divide the building differently. An architect organizes by room and an engineer by structural system, so the sheets do not correspond one to one. Finding which beam carries which room takes a drawing made for that purpose. The specs are the same. Product and technical specs do not decompose alike, so the usual way to keep them in view at once is a traceability table tying each product-facing capability to the mechanism producing it.

**When a fact needs both.** State the plain form in the product spec and the exact mechanism in the technical spec. Have each name the other, so the two cannot drift apart silently.

**Different renderings, not two levels of detail.** A construct modeling one fact may render differently on each side:

**Construct:** `specs/methodology/modeling-constructs.md § Constructs § Decision Table`

**Conditions:** Construct

| Construct | Product spec | Technical spec |
|---|---|---|
| "DAG", "State Machine for a process" | a business-readable table of its steps, decision points and outcomes | the DAG or State Machine that carries it out |
| Constraint | the plain guarantee | its enforcement, what its Enforced By names |
| "State Machine for an entity's or a system's status", "Decision Table" | the construct itself | the same construct |
| Record Form of entries written repeatedly | the construct itself | the same construct |
| "Record Form of a closed set", "Basic Table of a closed set" | the closed set: its type and its records, or its Basic Table | the data storing it, its database design and any enum naming its members, citing the set |
| Algorithm | no rendering, since a business reader has no use for step-by-step computation | the Algorithm |

**A promise that cannot be built.** Writing the technical spec tests a product promise against what is possible. A promise no mechanism can make true is amended in the product spec, as the user decides ([`§ Personas`](#personas)), rather than left standing.

## Personas

The methodology, [`specs/architecture.md`](/specs/architecture.md), the documentation, the product specs, the technical specs and the code the application specs govern are each written as their persona would write them. What an agent writes as a persona reads as that person's. A joke told by a rodeo clown reads differently from one told by a fifth grader. The adversarial review and the post-apply review of a design changing any of them are each framed as the same persona, so the persona stands on both sides of the authoring. Where a design changes both product and technical specs, each review's one reviewer reads each side's changes as that side's persona. The reviewer reports each persona's findings apart, so two lenses chosen for pulling against each other are not blended into one.

The agent instructions and the skills have no persona, since their primary reader is an agent ([`specs/methodology/spec-style.md § Clear Prose`](/specs/methodology/spec-style.md#clear-prose)). The product owner and the software engineer are roles the industry knows well, so a sketch of each is enough. The methodology owner is inside the house, and so is described in full.

**The methodology owner, for the methodology, [`specs/architecture.md`](/specs/architecture.md) and the documentation.** Someone who sees the methodology as a product. Its users design software, write the specs with it, and generate code from those specs. The methodology owner gives them structures and workflows that make an AI agent's assistance a multiplier of their own work. They believe a methodology earns its place by solving the hard problems itself, elegantly, so its users do not have to. They believe too that its internals will be judged for elegance as surely as its surface is judged for ease of use. They hold flexibility worth its cost only where projects genuinely differ, and consistency everywhere else, since every pattern that recurs is one less thing to learn. They study how people actually work: the natural workflow, and how it varies from one project to the next. They design each capability so its users find it both meets their need and is easy to use. They think in models. They find the general structure beneath particular cases, so one rule serves many, and they give the methodology a rhythm of recurring shapes that lightens the work of learning and using it. They protect the methodology, guiding its evolution toward improvement while keeping out complexity it does not need. They want its users to benefit from it, and to enjoy it.

**The product owner, for product specs.** Someone who has shipped products people find highly functional and easy to use, and who knows this product's architecture well. They know where configuration is the right call, and where two capabilities are better kept apart. A real difference between customers earns a setting. Needs forced into one configurable capability make it harder to use. They grow the product's architecture deliberately when a capability needs it: the extension is thought through and stated, never drifted into.

**The software engineer, for technical specs and the code carrying them out.** Someone who spent years as a principal engineer, battle-tested in production. They know the ideal design is a mirage and realistic greatness is the goal. They weigh each trade-off for what it buys now and for the foundation it lays for where the application is going. They grow the technical architecture deliberately, never by drift.

**A persona shapes the work, never its decisions.** Decisions about the thing being specified are the user's:

- what the product does, who may do it and what it promises;
- how it is made true;
- what the methodology's rules are.

Each persona proposes and challenges them, and leaves them to the user.

## Index, Architecture, Detail

Every directory under `specs/` organizes its files by altitude. New content belongs at the altitude that matches what it is.

**Reference Key:** Altitude

**Required:** File, Holds

| Altitude | File | Holds |
|---|---|---|
| Navigation | `index.md` | a title and a table naming each file and subdirectory with its description, no content of its own |
| Overview | `architecture.md` | a self-contained description of the directory's shape, every directory beneath it included, and of what [`§ What an Overview Describes`](#what-an-overview-describes) names beyond it, in its own words, naming every major piece and how they relate; only where that shape is worth describing as a whole, which not every directory's is |
| Detail | everything else | one file per functional area, holding the actual mechanism, schema, or experience, at whatever depth the subject needs |

**The test for new content.** Does it connect pieces, how they relate, why they are arranged as they are, what they add up to? That is overview. Does it specify what one piece does, shows or promises? That is detail, however much it says about the pieces around it.

**What an `architecture.md` is, and is not.** It is written so it can be read, understood, and shared in isolation. An architecture document stands apart from the system it describes in the same way, rather than being a portal into it. A closing mention of where fuller detail lives is fine, but the overview does not get its meaning from that mention.

**It holds no detail of its own.** An overview is the view of the whole from altitude. Zooming in reaches the detail files. By this section's test for new content, a detail has its home in one of those files, and an overview stating the detail restates it from there. What the overview states as its own is what only that height shows: how the pieces connect, the forest a reader of any one file cannot see for the trees.

An overview fails in opposite ways, and each has the same fix. One that accumulates full detail has stopped being an overview. One that thins into a table of citations cannot be understood without opening the files it points at. In either case, write the overview so it stands alone. Move genuine step-by-step or field-level detail into a file of its own, and repath every citation that pointed at the old location in the same pass.

A directory's own mapping table, where it has one, is the one exception: a deliberately citation-heavy traceability artifact is legitimate *beside* an overview that stands on its own, not *instead* of one.

**Where a diagram goes.** Set at any altitude by [`specs/methodology/modeling-constructs.md § Diagrams`](/specs/methodology/modeling-constructs.md#diagrams).

## What an Overview Describes

An overview describes its directory, every directory beneath it, and what this table names for its directory ([`§ Index, Architecture, Detail`](#index-architecture-detail)). It is kept in sync with all it describes ([`specs/methodology/sourcing-and-citation.md § Keeping Specs in Sync § Materialized Views`](/specs/methodology/sourcing-and-citation.md#materialized-views)):

**Construct:** `specs/methodology/modeling-constructs.md § Constructs § Decision Table`

**Conditions:** Directory

**Default Output:** nothing beyond its directory

| Directory | Describes beyond it |
|---|---|
| `specs/methodology/` | the skills registered as Spec of Record's, and the code their scripts share ([`specs/methodology/skills.md § Registered Skills`](/specs/methodology/skills.md#registered-skills), [`specs/methodology/skills.md § Authoring a Skill`](/specs/methodology/skills.md#authoring-a-skill)) |
| `specs/application/technical/` | the code carrying out the application specs, within the code roots its technical stack names ([`§ The Technical Stack`](#the-technical-stack), [`specs/methodology/code.md`](/specs/methodology/code.md)) |

## Where a File Goes

**Every directory gets an `index.md`.** The `index.md` lists only the directory's direct contents, in the order a reader takes them. That is the order an agent loads them in ([`specs/methodology/scope.md § Progressive Disclosure`](/specs/methodology/scope.md#progressive-disclosure)). A parent's `index.md` names a subdirectory as a single row pointing at it, and never expands that subdirectory's files inline.

**Check the directory's `index.md` before adding a file.** Prefer extending an existing spec over creating a new one that duplicates its content.

**When a subject earns its own file, and when a directory earns a subfolder.** A subject area here means a product capability domain on the product side and a service on the technical side. The test is the same for both:

**Construct:** `specs/methodology/modeling-constructs.md § Constructs § Decision Table`

**Conditions:** Does the subject area decompose into sub-parts each substantial enough to carry its own promise and its own scenarios independently of the others?

| Does the subject area decompose into sub-parts each substantial enough to carry its own promise and its own scenarios independently of the others? | Placement |
|---|---|
| true | its own subfolder, one file per such sub-part |
| false | a loose file at the directory's root |

A subject area that does not decompose so stays one cohesive mechanism, however many internal facets it has.

A sub-topic that still needs another sub-topic's context to make sense is a heading inside the file of the one whose context it needs. A cross-cutting subject area, one used by more than one other and owned by none, sits at the directory's root, never inside another's subfolder. The table decides whether it is a subfolder of its own or a loose file.

**Why a domain earns a folder.** A folder of files, one per sub-part, serves better than one file:

- each file loads only when a step needs it ([`specs/methodology/scope.md § Progressive Disclosure`](/specs/methodology/scope.md#progressive-disclosure));
- a change to one sub-part leaves the others' files untouched, and edits to separate files rarely meet in version control;
- a reader takes in one sub-part at a time, and work on the domain's code reads the sub-parts it needs.

An agent, like a person, reasons better over named, related files and the indexes linking them than over one long stretch of prose.

A section growing long, or gaining headings, is no reason to split it. Being cited as one findable unit from everywhere that needs it matters more than how many headings its file holds. A directory scatters what needs to stay whole.

**The same filename in more than one directory.** It is deliberate, as with `architecture.md` and `index.md`. Where one particular file is meant, it is named by its full path, never by the bare filename alone. A kind of file is named as [`specs/methodology/sourcing-and-citation.md § Writing a Citation`](/specs/methodology/sourcing-and-citation.md#writing-a-citation) has it.

## Naming a Capability Domain

The product specs are organized by capability domain ([`specs/methodology/glossary.md`](/specs/methodology/glossary.md)), rather than by file.

Before writing or extending a product spec, ask what a product owner, or a salesperson pitching the system, would call the capability domain it belongs to. Never ask which open file already talks about something similar.

### Home of New Product Content

The capability domain new product content belongs to decides which file it goes in. Read the product specs' `architecture.md` first. It gives each domain a section of its own, which describes what the domain covers and closes with the files that serve it. Its sections are therefore the domains the specs recognize. Then find the content's home:

**Construct:** `specs/methodology/modeling-constructs.md § Constructs § Decision Table`

**Conditions:** Extends a listed domain?, Grows what one of its files holds?

| Extends a listed domain? | Grows what one of its files holds? | Its home |
|---|---|---|
| true | true | that file |
| true | false | a new file in the domain's subfolder, the content a genuinely separate sub-capability |
| false | - | a new domain, named as a plain noun phrase for something the product durably does or governs, never a sprint, a milestone, or a technical mechanism's name, added to the product specs' `architecture.md` as its own section, subfolder or root file decided by [`§ Where a File Goes`](#where-a-file-goes) |

### Traps Before a New Product File

Check for these traps before finalizing any new product file:

**The same mechanism, split by audience, masquerading as two capabilities.** One role's view of a thing and another role's view of the same thing may be one underlying mechanism seen at two scopes. They then belong in one file describing both scopes, not in two files that will drift apart. The technical spec's language is a useful signal. When it describes what look like two product-facing capabilities as one mechanism serving several audiences, treat that as a reason to consolidate on the product side too.

**A cross-domain concern written into whichever domain needed it first.** A definition, principle, or distinction used by more than one domain and owned by none belongs at the directory's root ([`§ Where a File Goes`](#where-a-file-goes)), never in the domain that happened to need it first ([`specs/methodology/sourcing-and-citation.md § One Home Per Fact`](/specs/methodology/sourcing-and-citation.md#one-home-per-fact)).

## Naming the Technical Files Behind a Capability

A product spec file may open with a YAML front matter block ([`specs/methodology/external-references.md § External References [Name: YAML]`](/specs/methodology/external-references.md#external-references)) naming which technical files build its capabilities:

```yaml
---
technical-specs:
  - specs/application/technical/example-data-model.md
  - specs/application/technical/example-service/example.md
---
```

The block holds a list of file paths from the project root, written exactly as they appear anywhere else. The list is sorted in plain character order, so the order is never a judgment call and never signals importance. `technical-specs` is kebab-case, as every front matter key here is.

This is a label, not a citation. It names files, never headings, and is never wrapped in the backtick-and-`§` form a citation uses.

**Reference Key:** State

**Required:** Meaning

| State | Meaning |
|---|---|
| Omitted | Either the file has no technical implementation and never will, or it does but no target has been identified yet. Nothing is asserted about the technical side either way. |
| Populated | One or more file paths named. The ordinary case, once a target is actually known. |

**Direction.** `technical-specs` appears only in a product spec, never in a technical one. It points one way, from product to technical. Product specs govern. Technical specs exist to make them true. There is no reciprocal list, because the technical prose cites the product section it implements ([`§ Product or Technical`](#product-or-technical)).

**How this differs from an `index.md`.** An `index.md` gives breadth within one directory. It is a separate navigational file, describing what every file in that directory contains. `technical-specs` gives depth across directories for one specific file. It lives inside the product file it describes, and names the bounded set of technical files needed to understand how that file's capabilities are built.

**Reading it.** Before working on a technical file, check whether a product file's `technical-specs` names it. If so, that product file's capabilities are what the technical file already fulfills, and what an edit has to keep true.

**Writing it.** A product spec is usually written before any technical content implementing it exists. State the capability in prose with no technical reference of any kind, and leave `technical-specs` omitted. Naming a file before real technical work exists to name would be a guess dressed as a fact. When technical content is later written to fulfill a capability, add that file to the product file's list, in its place in plain character order. The technical prose cites the product section, as [`§ Product or Technical`](#product-or-technical) has each side name the other. The list is the coarse pointer and that citation the precise proof. Both stay.

## A Product Module

For a domain that decomposes into sub-parts, a product module is a folder directly under `specs/application/product/`. For a domain that is one cohesive mechanism, it is a single file in that directory's root ([`§ Where a File Goes`](#where-a-file-goes)). A module also holds each root file named in its domain's account in the product specs' `architecture.md`.

A change to a module's code reads:

- the module's product specs;
- the technical files they name in their `technical-specs` front matter ([`§ Naming the Technical Files Behind a Capability`](#naming-the-technical-files-behind-a-capability)): a file only this module names is read whole, and a file several modules name is read at the sections this module's code needs.

Every module also reads what no module owns:

- the product specs' own `index.md` and `architecture.md`, and any vision or overview of the product;
- each root file the product specs' `architecture.md` names as held by no domain;
- the technical specs' `architecture.md`;
- the technical specs' stack, `stack.md` ([`§ The Technical Stack`](#the-technical-stack));
- the technical specs' environments, `environments.md` ([`§ Environments`](#environments)).

Any other product file or folder that the product specs' `architecture.md` does not name is a gap in the specs. So is technical content that no module's front matter reaches. Each such gap is put right in the specs before code is written for it.

## The Technical Stack

The technical specs hold one stack file, `stack.md` at their root. It says what the system is built with, what it relies on, and where its code lives. So each technology, and how the system uses it, has one home. A technical spec relying on a technology cites the stack file rather than introducing the technology where it is used ([`specs/methodology/sourcing-and-citation.md § One Home Per Fact`](/specs/methodology/sourcing-and-citation.md#one-home-per-fact)). The stack file holds a table of the system's parts and a table of what they rely on, and gives each technology in them with its version.

**The parts.** The table of the parts has one row for each part of the system: a user interface and a backend, say, or a single service. Its columns, in order:

| Column | Holds |
|---|---|
| Part | the part |
| Language | the language it is written in |
| Framework | the framework it builds on |
| Build Tool | the tools that build it, any tool generating files among them |
| Test Framework | the framework its tests are written in, the executable copies of the acceptance scenarios among them ([`specs/methodology/code.md § Tests`](/specs/methodology/code.md#tests)); a browser automation framework such as Playwright or Selenium for a user interface, say |
| Code Roots | the directories holding its code, its tests' directories among them |
| Excluded | the paths under its code roots that are not the application's own, code vendored from elsewhere or generated by a tool |

Each path is written from the project root, in backticks. A code root is never the project root itself, and never sits under another code root. So the specs and the working files stay outside the application's code, and no file is the code of two parts. The code roots, less what is excluded, name the application's code ([`specs/methodology/scope.md § What Spec of Record Governs`](/specs/methodology/scope.md#what-spec-of-record-governs)), so a check on code knows where to look, and a file outside them is no concern of [`specs/methodology/code.md`](/specs/methodology/code.md)'s rules.

**What the parts rely on.** The table of what the parts rely on is headed Technology, Kind and Purpose. It has one row for each technology the parts use in every environment, beyond the parts' own code, and each row says what the system uses the technology for:

- each database, with the purpose it serves, the core application's data or reporting, say;
- each cache, such as Redis or Memcached;
- each queue or stream;
- any other service of that kind.

A technology only some environments use is stated in those environments instead ([`§ Environments`](#environments)).

## Environments

The technical specs hold one environments file, `environments.md`, at their root beside the stack file. It has a section for each environment the system is built, tested or run in, titled with the name the project gives that environment. An environment states only what differs from the stack ([`§ The Technical Stack`](#the-technical-stack)). So the stack stays the home of each technology every environment uses, and of each version, and no environment restates them. An environment holds no secret value, credential or host name. At most, it names the vault or configuration they come from.

Each environment's section opens with a required `**Kind:**` field ([`specs/methodology/modeling-constructs.md § Fields`](/specs/methodology/modeling-constructs.md#fields)), whose value is one of a closed set, so what this section asks of an environment follows from its role, never from its name:

**Construct:** `specs/methodology/modeling-constructs.md § Constructs § Decision Table`

**Conditions:** Kind

**Annotations:** Holds

| Kind | What it owes | Holds |
|---|---|---|
| local | it names each operating system its developers may use, and the project supports only those; it has tools, a build task, a lint task, and a test task for every kind of test the project has, its acceptance tests among them | developers' own machines or a development container, where code is written |
| integration | it runs every build, lint and test task of the local environment, naming the operating systems it runs them on; a local operating system it does not run them on is supported as stated, not as shown | continuous integration |
| shared | nothing beyond every environment's own sections | a deployed environment people or tests use, development, quality assurance, staging or a hotfix environment, say |
| production | where a product spec specifies the production environment, a customer's own installation, say, it cites that spec and adds only what the stack and that spec leave open | the environment serving real users |

Exactly one environment is local.

After its Kind, each environment's section gives, as bold lead-ins in this order:

- what it is for and who uses it;
- where it runs;
- what differs from the stack: each technology the environment uses in place of, or beside, one the stack names, with its purpose;
- what data it holds.

Then, where it has any, comes a table of the tools it needs. The table is headed Tool, Version and Purpose, and has one column for each operating system the environment names, saying how the tool is installed there. A tool's Version is given only where the stack does not name the tool. A tool the stack names takes the stack's version.

Then, where it has any, comes a table of its tasks. The table is headed Task, Command and Does, and Runs On where any task needs it. Each command is run from the project root. A task runs on every operating system the environment names, unless its Runs On names the ones it runs on. A task whose command differs between operating systems takes a row for each. A command may take an argument, written in angle brackets, and Does says how to fill it. Each test task has a targeted form, which takes an argument selecting the tests to run.

As it works, the agent writing code runs the targeted form of a test task on the tests citing the specs its work carries out ([`specs/methodology/code.md § Tests`](/specs/methodology/code.md#tests)). Before its work is checked, the agent runs every build, lint and test task of the local environment, so a task that no longer works is found as soon as code is written. A project whose specs give no local environment, or whose local environment lacks any of these tasks, has code an agent cannot check. That is a gap in the specs, and the agent presents it rather than writing code around it.

## Open Question

An open question is recorded in the specs whose area it applies to: methodology, product or technical. Within those specs, it is recorded in the file whose scope covers everything the question impacts. That file must be able to cite every section the question's Impacts names ([`specs/methodology/sourcing-and-citation.md § Which Citations Are Allowed`](/specs/methodology/sourcing-and-citation.md#which-citations-are-allowed)). Open Question is a record type ([`specs/methodology/modeling-constructs.md § Constructs § Record Form`](/specs/methodology/modeling-constructs.md#record-form)), and a file's open questions sit in its record section of this type. That record section is the file's last top-level section, so a reader finds them all in one place, after the settled content they qualify:

**Construct:** `specs/methodology/modeling-constructs.md § Constructs § Record Form`

**Plural Name:** Open Questions

**Reference Key:** Name

| Field | Unique | Required | Default Value | Values | Holds |
|---|---|---|---|---|---|
| Name | yes | yes | | text | a short name for what is undecided |
| Open Question | no | yes | | text | what is undecided, asked as a question |
| Provisional Answer | no | yes | | text | what the specs rely on until it is settled, stated as settled prose would state it |
| Impacts | no | yes | | text | prose naming each thing that relies on the provisional answer, with a citation of the section holding it, or, where that section holds more, of the part of a construct that relies on it ([`specs/methodology/modeling-constructs.md § Constructs § Keyed Construct`](/specs/methodology/modeling-constructs.md#keyed-construct)); a data field that relies on it is named by what it says beside its section's citation |

A sentence that relies on the provisional answer, and would otherwise read as settled, cites the record wherever [`specs/methodology/sourcing-and-citation.md § Which Citations Are Allowed`](/specs/methodology/sourcing-and-citation.md#which-citations-are-allowed) allows that citation, so a reader meets the question from the text that depends on it. A spec of a system that exists states the system as it is built. Where its author suspects a defect, what the system should do is an open question, and its Provisional Answer is the behavior as built. So the spec states as built nothing the system does not do.

The provisional answer is stated in the record alone. The text relying on it states only what does not depend on it. Settling an open question is a change like any other. The settled answer is written, wherever it is needed, into each section the record's Impacts names and each section citing the record. There it replaces any citation of the record. Then the record is removed, and its record section too once that section holds no record.
