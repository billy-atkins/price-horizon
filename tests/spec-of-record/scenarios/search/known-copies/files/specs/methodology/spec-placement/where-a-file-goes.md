## Where a File Goes

**Every directory gets an `index.md`.** The `index.md` lists only the directory's direct contents, in the order a reader takes them, its `main.md`, where it holds one, first among its specs. That is the order an agent browsing the directory loads them in ([`specs/methodology/scope/progressive-disclosure.md § Progressive Disclosure`](/specs/methodology/scope/progressive-disclosure.md#progressive-disclosure)). A parent's `index.md` names a subdirectory as a single row pointing at it, and never expands that subdirectory's files inline.

**A directory's `main.md` is made when its content first needs it.** A directory holds one as [`specs/methodology/spec-placement/index-architecture-detail.md § Index, Architecture, Detail`](/specs/methodology/spec-placement/index-architecture-detail.md#index-architecture-detail) gives the Main altitude, never ahead of that content. Nothing in it is read ahead of need: a file relying on content in it cites that content, as it cites anything else it relies on. At `specs/`, the entry point, [`specs/AGENTS.md`](/specs/AGENTS.md), is agent instructions and no spec, and stands apart from the main file there, which holds what the core canon's specs share, never an agent instruction or a constitutional principle, which the entry point holds, and nothing an application spec relies on, since no application spec may cite it ([`specs/methodology/sourcing-and-citation/which-citations-are-allowed.md § Which Citations Are Allowed`](/specs/methodology/sourcing-and-citation/which-citations-are-allowed.md#which-citations-are-allowed)). Wherever the canon names its own files, it names that main file, which stands only where `specs/` has such content, as any directory's does.

**Check the directory's `index.md` before adding a file.** Prefer extending an existing spec over creating a new one that duplicates its content.

**When a subject earns its own file, and when a directory earns a subfolder.** A subject area here means a product capability domain on the product side, a service on the technical side, and the methodology. The test is the same for each:

**Construct:** `specs/methodology/modeling-constructs.md § Constructs § Decision Table` \
**Conditions:** Does the subject area decompose into sub-parts each a document of its own that is read and changed independently of the others?

| Does the subject area decompose into sub-parts each a document of its own that is read and changed independently of the others? | Placement |
|---|---|
| true | its own subfolder, each sub-part a document in it, laid out by the file-unit test |
| false | a loose document at the directory's root: one file, or a folder named for it where it holds more than one file unit |

On the product side, such a sub-part carries its own promise and its own scenarios. In the methodology, it states its own rules. The line falls at the document: the methodology is one subject area, `specs/methodology/`, whose documents are its sub-parts, so a methodology document holding more than one file unit is a document laid out as a folder, never a subfolder of documents. A subject area that does not decompose so stays one document, however many internal facets it has.

A cross-cutting subject area, one used by more than one other and owned by none, sits at the directory's root, never inside another's subfolder. The table decides whether it is a subfolder of its own or a loose document.

**Why a subject area earns a folder.** A folder of documents, one per sub-part, serves better than one document:
- each file loads only when a step needs it ([`specs/methodology/scope/progressive-disclosure.md § Progressive Disclosure`](/specs/methodology/scope/progressive-disclosure.md#progressive-disclosure));
- a change to one sub-part leaves the others' files untouched, and edits to separate files rarely meet in version control;
- a reader takes in one sub-part at a time, and work on the subject area reads the sub-parts it needs.

An agent, like a person, reasons better over named, related files and the indexes linking them than over one long stretch of prose.

**A file unit takes a file of its own.** This rule lays out the specs alone, the core canon's and the application's. The agent instructions and the skills stand as they are ([`specs/methodology/scope/what-spec-of-record-governs.md § What Spec of Record Governs`](/specs/methodology/scope/what-spec-of-record-governs.md#what-spec-of-record-governs)). A file unit ([`specs/methodology/glossary/glossary.md`](/specs/methodology/glossary/glossary.md)) takes a file named for it, whatever its size. Size decides nothing either way.

**When content takes a file of its own.** Content needed together with other content for understanding in most circumstances stays in one file with it, however long the file grows. Content with a reading use case of its own, a step an agent comes to it alone for, takes a file of its own, citing what it relies on. So an agent's context holds what the work at hand needs, and is rich where the work needs it. Where the test is in doubt, the content stays together. Content that is no file unit of its own is a heading in the file of the content whose context it reads with. A citation naming content gives it no reading use case of its own, since a step citing a part reads it with what holds it. Content needed together, as aids to judgment and never a closed set:
- a family of sections defining one thing;
- content a human reads beside the text it serves, as a diagram is read beside its text;
- each part of a keyed construct's instance, a record or a row its key cites, read with that instance, the instance keeping its set or list of parts whole in one file;
- content another rule keeps inside the section it serves, as a capability's test scenarios are read with the capability they test ([`specs/methodology/acceptance-scenarios.md § Acceptance Scenarios`](/specs/methodology/acceptance-scenarios.md#acceptance-scenarios)).

So an overview stays one file with its diagrams, a keyed instance stays one with its parts, and a capability laid out as a file unit carries its test scenarios into its own file.

**A file unit cites what it relies on.** A file unit depending on another cites that unit's own file, fully qualified, where it is used, never through an `index.md`. A file unit moved out of the text that held it states, or cites fully qualified, whatever it took from that text by its position: a term, a scope, or what a reference points at. A file unit standing on its own cites no parent.

**A file unit is cited where it is needed.** As a file unit leaves the text that held it, each step, index row or rule needing it cites it: a citation of it standing is repathed, and a place that reached it only by reading its host whole gains a citation of it. So no file unit is left reached by nothing.

**A document of several file units is a folder.** A document holding more than one file unit is a folder named for the document. It holds each file unit's file, its `index.md`, and its `main.md` where [`specs/methodology/spec-placement/index-architecture-detail.md § Index, Architecture, Detail`](/specs/methodology/spec-placement/index-architecture-detail.md#index-architecture-detail) gives it one. A file unit with file units of its own is a folder in turn. A document is cited through its files, its `main.md` where it holds one or a file unit's own file, never as a folder. The worked examples keep their own tree, by subject and topic ([`specs/methodology/scope/progressive-disclosure.md § Progressive Disclosure`](/specs/methodology/scope/progressive-disclosure.md#progressive-disclosure)).

**A name is the term for what it holds.** A file or folder under `specs/` is named for its subject area's term for what it holds, never a description of it. Its name is that term in kebab-case ([`specs/methodology/spec-placement/kebab-case-conversion.md § Kebab-Case Conversion`](/specs/methodology/spec-placement/kebab-case-conversion.md#kebab-case-conversion)), a leading article dropped first, so `Trust & Explainability` names `trust-and-explainability/`. A document laid out as a folder keeps the name its file had. The names `index.md`, `main.md` and `architecture.md` are their altitudes' ([`specs/methodology/spec-placement/index-architecture-detail.md § Index, Architecture, Detail`](/specs/methodology/spec-placement/index-architecture-detail.md#index-architecture-detail)), never a term's, and a kind of file the canon names by a rule of its own keeps that rule.

**The same filename in more than one directory.** It is deliberate, as with `architecture.md`, `index.md` and `main.md`. Where one particular file is meant, it is named by its full path, never by the bare filename alone. A kind of file is named as [`specs/methodology/sourcing-and-citation/writing-a-citation.md § Writing a Citation`](/specs/methodology/sourcing-and-citation/writing-a-citation.md#writing-a-citation) has it.
