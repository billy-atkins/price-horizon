Which spec a fact belongs in, which altitude, which file, and how a product capability names the technical files that build it.

## Product or Technical

| Spec | Covers |
|---|---|
| Product | What a user or an integrating caller can experience, rely on, or build against: the answer experience, the guarantees the system makes, the roles and access model a buyer would evaluate, the shape of any contract an integrating caller depends on. Stated as a capability or a guarantee, never as an implementation choice. |
| Technical | How each of those facts is made true: the algorithms, schemas, service boundaries, models, and infrastructure. |

**The test.** Could an end user or an integrating caller observe this as something they can rely on, rather than as a byte in a response payload or a line in a schema?

A guarantee, a role, a piece of the answer experience, or a term a user needs defined to trust an answer passes, and belongs in the product spec, even when its mechanism is technical-only. A data model field, an algorithm's steps, a database's shape, or a choice of API convention does not pass on its own, and belongs in the technical spec.

**Two drawings of one building.** A product spec is the architect's drawing and a technical spec is the structural engineer's. The architect draws what the building is and everything the people in it will experience; the engineer draws how it can be built and keep working for them. Both are of the same building, drawn twice for two purposes, and neither summarizes the other.

This is why a product spec states facts that sound like infrastructure. The architect draws a wall rated to hold back fire for two hours, because someone occupying the building relies on that; the engineer states the assembly that achieves the rating. A credential held in an isolated vault is the same: a buyer relies on it, so it belongs on the architect's drawing, while which credentials that vault holds and how narrowly each is scoped belongs on the engineer's.

The two drawings also do not divide the building the same way. An architect organizes by room and an engineer by structural system, so the sheets do not correspond one to one, and finding which beam carries which room takes a drawing made for that purpose.

**When a fact needs both.** State the plain form in the product spec, the exact mechanism in the technical spec, and have each name the other, so the two cannot drift apart silently.

**Different renderings, not two levels of detail.** A construct modeling one fact renders differently on each side. For a process modeled as a DAG or a State Machine, the product spec gets the business-readable table of steps, decision points, and outcomes; the technical spec gets the DAG or State Machine that carries it out. For a Constraint, the product spec states the plain guarantee and the technical spec states its enforcement, which step actually guarantees it. Algorithm is the one exception: it has no product-spec rendering, since a business reader has no use for step-by-step computation. Because the two sides do not decompose alike, a traceability table tying each product-facing capability to the mechanism producing it is the usual way to keep them in view at once.

**A promise that cannot be built.** Writing the technical spec is how a product promise gets tested against what is actually possible. A promise no mechanism can make true is amended in the product spec rather than left standing, and the technical spec is usually where that is discovered.

## Index, Architecture, Detail

Every directory under `specs/` organizes its files by altitude. New content belongs at the altitude matching what it actually is.

| Altitude | File | Holds |
|---|---|---|
| Navigation | `index.md` | a file-name-to-description table and front matter, no content of its own |
| Overview | `architecture.md` | a self-contained description of the whole directory's shape, naming every major piece and how they relate, in its own words |
| Detail | everything else | one file per functional area, holding the actual mechanism, schema, or experience, at whatever depth the subject needs |

**The test for new content.** Does it explain how pieces fit together, in prose rich enough to stand on its own? That is overview. Does it specify what one piece does or shows, precisely enough to need citation-grade traceability? That is detail.

**What an `architecture.md` is, and is not.** It is written so it can be read, understood, and shared in isolation, the way an architecture document stands apart from the system it describes rather than being a portal into it. A closing mention of where fuller detail lives is fine; that mention is not how the overview gets its meaning.

Opposite failure modes, and the same fix for each. An overview that accumulates full detail has stopped being an overview. An overview that thins into a table of citations cannot be understood without opening the files it points at. In either case: write the overview so it stands alone, move genuine step-by-step or field-level detail into its own file, and repath every citation that pointed at the old location in the same pass.

A directory's own mapping table, where it has one, is the exception that proves the rule: a deliberately citation-heavy traceability artifact is legitimate *beside* an overview that stands on its own, not *instead* of one.

**Where a diagram goes**, at any altitude, is set by `specs/methodology/modeling-constructs.md § Diagrams`.

## Where a File Goes

**Every directory gets an `index.md`,** listing only its own direct contents. A parent's `index.md` names a subdirectory as a single row pointing at it, never expanding that subdirectory's files inline. This applies recursively, at every level.

**Check the directory's `index.md` before adding a file.** Prefer extending an existing spec over creating a new one that duplicates its content.

**When a subject earns its own file, and when a directory earns a subfolder —** a subject area here means a product capability domain on the product side and a service on the technical side; the test is the same for both.

| Situation | Placement |
|---|---|
| A subject area decomposes into multiple sub-parts, each substantial enough to carry its own promise and its own scenarios independently of the others | its own subfolder, one file per sub-part |
| A sub-topic still needs the others' context to make sense | a heading inside one file |
| A subject area stays one cohesive mechanism, however many internal facets it has | a loose file at the directory's root |
| A subject area is cross-cutting, used by more than one other and owned by none | a loose file at the directory's root |

A section growing long, or gaining a second heading, is not a reason to split it. Being referenced as a single findable unit from everywhere that needs it matters more than how many headings a file holds, and a directory scatters exactly what needs to stay whole.

**The same filename in two directories** is deliberate, not accidental. `architecture.md` exists in more than one place because each directory has a shape worth describing. Such a file always needs its full path stated to disambiguate, never the bare filename alone.

## Naming a Capability Domain

A product specification's organization is domain-driven, the way a product owner defines a durable capability area, not file-driven, the way it is tempting to write wherever a related word already appears.

A capability area is a standing part of what the product does or governs for as long as the product exists. An epic or a sprint is the wrong mental model entirely: those describe work with an end date, not a boundary meant to outlive any single change.

Before writing or extending a product spec, ask what a product owner or a salesperson pitching the system would call the capability domain it belongs to, never "which open file already talks about something similar."

Read the product `architecture.md` first: one section per domain, each describing what that domain covers and closing with the files that serve it. That is the set the spec currently recognizes. If the content extends a listed domain, put it in that domain's home: an existing file if it grows what is there, a new file in that domain's subfolder if it is a genuinely separate sub-capability. If it fits none of them, name the domain as a plain noun phrase for something the product durably does or governs, never a sprint, a milestone, or a technical mechanism's name; add it to `architecture.md` as its own section; and decide subfolder versus root file by `§ Where a File Goes`.

Traps worth checking for before finalizing any new product file:

**The same mechanism, split by audience, masquerading as two capabilities.** If one role's view of something and another role's view of the same thing are one underlying mechanism seen at two scopes, they belong in one file describing both scopes, not two files that will drift apart. The technical spec's own language is a useful signal: when it describes what look like two product-facing capabilities as one mechanism serving several audiences, treat that as a reason to consolidate on the product side too.

**A cross-domain concern written into whichever domain needed it first.** A definition, principle, or distinction genuinely used by more than one domain and owned by none belongs at the directory's own root (`§ Where a File Goes`), or as a named principle in `architecture.md`, never in the domain that happened to need it first (`specs/methodology/sourcing-and-citation.md § One Home Per Fact`).

## Naming the Technical Files Behind a Capability

A product spec file may open with a YAML frontmatter block naming which technical files its capabilities are actually built by:

```yaml
---
technical-specs:
  - specs/application/technical/predict-computation.md
  - specs/application/technical/query-service/intent-and-retrieval.md
---
```

A list of file paths from the project root, exactly as they appear anywhere else, sorted alphabetically so the order is never a judgment call and never signals importance. The field name is kebab-case, the standard this repo's frontmatter fields follow.

This is a label, not a citation. It names files, never headings, and is never wrapped in the backtick-and-`§` form a citation uses.

| State | Meaning |
|---|---|
| Omitted | Either the file has no technical implementation and never will, or it does but no target has been identified yet. Nothing is asserted about the technical side either way. |
| Populated | One or more file paths named. The ordinary case, once a target is actually known. |

**Direction.** This field appears only in a product spec, never a technical one, and points one way: product to technical. Product specs govern; technical specs exist to make them true. There is deliberately no reciprocal field, because a technical file already names the product section it implements, in prose.

**How this differs from an `index.md`.** An `index.md` is same-directory breadth, in a separate navigational file, describing what every file in that directory contains. `technical-specs` is cross-directory depth for one specific file: it lives inside the product file it describes and names the bounded set of technical files needed to understand how that file's capabilities are built.

**Reading it.** Before working on a technical file, check whether a product file's `technical-specs` names it. If so, that product file's capabilities are what the technical file already fulfills, and what an edit has to keep true.

**Writing it.** A product spec is usually written before any technical content implementing it exists: state the capability in prose with no technical reference of any kind, and leave the field omitted. Naming a file before real technical work exists to name would be a guess dressed as a fact. When technical content is later written to fulfill a capability, add that file to the product file's list in its correct alphabetical place, and separately cite the specific product section from the technical prose itself. The field is the coarse pointer; that citation is the precise proof; both stay in place together.

## An Open Question

A decision the specs rely on but have not made is recorded as an open question, in the spec whose area it applies to, methodology, product or technical, in the file whose scope covers everything the question impacts, which must also be able to cite every section its Impacts names (`specs/methodology/sourcing-and-citation.md § Which Citations Are Allowed`). Its records sit in a record section titled Open Questions, the file's last top-level section, so a reader finds every question a file holds in one place, after the settled content it qualifies. It is a Record Form (`specs/methodology/modeling-constructs.md § Constructs § Record Form`) whose type is named Open Questions:

| Field | Identifies | Holds |
|---|---|---|
| Name | yes | a short name for what is undecided |
| Open Question | no | what is undecided, asked as a question |
| Provisional Answer | no | what the specs rely on until it is settled, stated as settled prose would state it |
| Impacts | no | prose naming what relies on the provisional answer, each with a citation of the section holding it, and, where that section holds more, the step, row or data field that relies on it, named by what it says, or, for an Algorithm's or a Decision Tree's step, by its number |

A sentence relying on the provisional answer cites the record where it would otherwise read as settled and `specs/methodology/sourcing-and-citation.md § Which Citations Are Allowed` lets it, so a reader meets the question from the text that depends on it.

The provisional answer is stated in the record alone, and the text relying on it states only what does not depend on it. Settling one is a change like any other: the settled answer is written where each section its Impacts names, or that cites it, needs it, in place of that citation, and the record is removed, along with its record section once that holds no record.
