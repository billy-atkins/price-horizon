## Glossary

The terms Spec of Record gives a meaning of its own, each defined here once and nowhere else: a file using a term states its rules about it, never a second definition. This file also states what earns a term its entry, how an entry is written, and where an abbreviation may be used.

| Term | Abbreviation | Definition |
|---|---|---|
| Adversarial review |  | A Design, Refactor, Refine run by a cold agent over a builder's design. |
| Altitude |  | The level of a file, or of its content, within its directory, from the navigation that names what the directory holds down to the detail that states it. |
| App-spec annotation |  | A spec annotation in governed code, naming a spec, or a section of one, that the code carries out or, as a test, checks. |
| Builder |  | The person or agent who does a piece of work and takes it through Design, Refactor, Refine. |
| Canon |  | The part of the Spec of Record scope that states and applies the method's rules: the entry point to the specifications, the methodology, and the skills the methodology registers, each skill the specification of a procedure, with the code their scripts share. Not a product's specifications, and not a canonical form or version. |
| Canon-spec annotation |  | A spec annotation in a registered skill's script, or the code the skills share, naming the area of the method's own specifications that a copy the script holds takes its values from. |
| Capability domain |  | A standing part of what a product does or governs for as long as the product exists, defined by its product owner: a boundary meant to outlive any single change. Not an epic or a sprint, which describe work with an end date. |
| Citation |  | A pointer from one place in the Spec of Record scope to another, written in a fixed form a reader and a script can both follow. Not a bibliographic reference. |
| Cold agent |  | An agent arriving with no context but what it reads, and so with no attachment to the decisions of whoever did the work before it. |
| Construct |  | A structured form, one of a bounded set the method approves, in which a rule, a process, an entity's behavior or a repeated entry is written rather than in free prose. Not the programming sense. |
| Design document |  | A plan describing one change to the specifications or to code taken through Design, Refactor, Refine, from the problem it solves to the edits that make it. Not a design the product's architecture describes. |
| Design, Refactor, Refine | DRR | A process by which work is brought to elegance: a draft that solves the problem, then structural change until the structure settles, then its wording. |
| Elegance |  | A quality of a solution, the opposite of a Rube Goldberg machine, in which its objective is satisfied by the fewest rules, as a minimal proof reaches its theorem in the fewest steps. So a skilled reader sees in it simple, recurring patterns, a rhythm and a beauty, where an unskilled reader sees only complexity. The complexity is reduced, never hidden: everything the objective truly requires is still there, in its simplest form. |
| Field |  | A key-value pair written into a spec's or a working file's text. Not a table's column, a data field a data model defines, or a key in a file's frontmatter. |
| Governed code |  | Code that carries out a spec, or a test that checks one. Not code a governance process approves. |
| Home |  | The one place where a fact or a rule is stated. |
| Inside the house |  | A term, abbreviation or example coined or introduced by Spec of Record or the application specs: known to those working within them, and taught by the specs to every agent and engineer who arrives, as a household's own words make sense only to those living in it. Not one known outside them. |
| Key |  | The name of a field. Not a database key, and not a key in a file's frontmatter. |
| Layer |  | A level in the order of what governs what among the specifications, each governed by those above it. Not a layer the product's specifications describe. |
| Methodology owner |  | The persona the methodology is written as, and a design changing it reviewed as. |
| Open question |  | A decision the specs rely on but have not made, recorded with the answer in use until it is settled. Not a question merely unanswered in conversation. |
| Operating rule |  | A rule about operating Spec of Record: how work on the specifications and the code they govern is done, reviewed, recorded and tooled, rather than what they hold. Not a rule about how the product operates. |
| Outside the house |  | A term, abbreviation or example common to many across the industry or the domain, a norm agents know from their training and engineers from experience. |
| Persona |  | A character a specification, or the code it governs, is written as, described by how they see the work, what they care about and how they go about it, never by steps to follow, so an agent taking one up brings what it knows of such a person. Not a user persona of product design, an archetype of the people a product serves. |
| Plan |  | A working file in which a skill describes a change before making it. Not a schedule, a project plan, or a plan the product's specifications describe. |
| Point-of-use citation |  | A citation placed where the rule, definition or principle it names is applied, in the step or passage doing the work. |
| Potemkin village |  | A front built to look complete with nothing behind it, as the painted village facades of the legend: a guarantee, rule or enforcement mechanism relied on as real that is stated but not specified or not checked. |
| Product module |  | A capability domain as the product architecture names it, a folder or a single file, bounding the scope of a change to the code that carries it out. Not a Python module, and not a module of the code. |
| Progressive disclosure |  | A way of reading in which what a step needs is loaded at the step that needs it, rather than everything at once. |
| Reasoning effort |  | A setting of the model an agent runs on: how far it reasons before it answers. Not how far a review reaches, nor how many reviewers run it. |
| Record |  | An entry of a record type, written in the Record Form. Not the product's stored data. |
| Record section |  | A section holding the records of one record type. |
| Refactor and Refine cycle | RR cycle | The Refactor and Refine of Design, Refactor, Refine, run over specifications that have landed, their state at a baseline commit standing as the design: a change to their structure and wording that leaves what they state. Not the Refactor and Refine within a design still in flight. |
| Rube Goldberg machine |  | A mechanism far more elaborate than the task it performs, as the cartoonist's contraptions chain many steps to do something simple: a mechanism, role or safeguard whose complexity no stated need justifies, where a light switch would do. |
| Spec annotation |  | A citation written in code as a plain comment line of its own, a tag and then the citation, naming a spec, or a section of one, that the code relies on. Not a language's own annotation construct, such as a Java annotation or a C# attribute. |
| Spec of Record |  | A methodology for the agentic SDLC, governed and spec-as-source, in which the specifications are the durable source a system is built from, and a human designs and steers while an AI agent assists. |
| Spec of Record scope |  | The set of files Spec of Record governs, and nothing else. |
| Specification rule |  | A rule governing what the specifications and the code they govern hold, and how they are written. Not a rule a specification states about the product. |
| Stamp |  | A field's value recording when a check passed and a hash of the content it passed on. Not a version number or a signature. |
| Steering decision |  | A record of a decision the user made about what a design is: what it solves, decides, includes or leaves out, quoting the user's words, and kept in the design it decides. Not the request that opened the design, nor the user's direction about how the work proceeds, nor a tactical adjustment. |
| Validation review |  | A review by a cold agent of whether a plan holds to the rules for its form and its record, run before the user approves it. Not an adversarial review, which reviews the design itself. |
| Wiring code |  | Code that connects governed code into a working application, service or system, carrying out no spec of its own. |
| Working file |  | A file that the work on the specs or their code leaves behind, serving whoever does that work. |
| Workstack |  | The tree of design documents their Spawned By draws from one design that was not spawned, together with the blocking their Depends On records. Not a call stack or a task queue. |

## Writing an Entry

**What earns an entry —** a meaning in Spec of Record that training knowledge alone would not give: a term coined by the method, overloaded with another meaning nearby, used across areas in a narrow sense, or adopted as shorthand for a principle.

**The term —** the bare term, without markup or any of its other names, listed once, the table sorted by term.

**The definition —** it opens with its genus, the broader kind the term belongs to, a term of this glossary wherever one fits, so a term builds on the terms it rests on rather than restating them. It then states what sets the term apart, and a use it must not be mistaken for opens with `Not`.

**Other names —** a term's one abbreviation goes in its Abbreviation column, left empty where it has none. A definition ends with the term's other full names, as `Also called X.`, several separated by commas. Each name belongs to that term alone, never to another term.

**Nothing cited —** the glossary cites nothing, so it reads as a dictionary: a definition stands on its own and on the terms beside it.

## Using an Abbreviation

An abbreviation outside the house may be used in any specification or instruction, its meaning already known to the agents and engineers reading it. One inside the house is used in none of them; they spell its term out instead, since an agent reads every word of a rule as the rule's, and may misread a short form only the house knows. The short form is for people talking to an agent, since the agent can ask them what one means.

**Where one is recorded —** each inside-the-house abbreviation is recorded once, beside its term's definition, which is how it is known to be one:

- the method's, in its glossary entry's Abbreviation column;
- the application's, where the application specs define its term, at that term's altitude, written `(abbreviated X)` directly after the term.
