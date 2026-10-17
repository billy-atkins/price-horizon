## The Shape of the Specifications

The specifications are layered, each layer describing a different kind of thing, the methodology above the application, its rules reaching the application's specs, and the product above the technical. What each overview describes beyond its directory is set in `specs/methodology/spec-placement.md § What an Overview Describes`.

```
specs/
├── AGENTS.md             the entry point to Spec of Record
├── index.md
├── architecture.md       this overview
├── methodology/          the rules for writing specs, and for the code the specs govern
│   ├── index.md
│   └── architecture.md
└── application/          the product being specified
    ├── index.md
    ├── product/
    └── technical/
```

At the top of `specs/` sits `specs/AGENTS.md`, Spec of Record's entry point. It holds:

- the kinds a change can be, and the skills every change and every check is sent to, each forking on whether the canon or the application specs are touched, and the skills designing, writing and checking code;
- where to find a rule mid-step;
- the rules reaching every author: how work is designed, reviewed and approved, who makes each check, how each round of an adversarial review is settled at the causes of its findings, and how what a change reaches is kept in sync with it.

`specs/methodology/scope.md § The Shape of the Scope` draws the whole scope, down to each methodology file, and each directory's own `index.md` lists what it holds, so this tree names only the layers and the files that establish them. The methodology has its own overview, `specs/methodology/architecture.md`, and the application one for each half, `specs/application/product/architecture.md` and `specs/application/technical/architecture.md`.

**`specs/methodology/` —** the rules for writing a specification here, and for the code the specs govern, described in its own overview, `specs/methodology/architecture.md`, with the skills carrying its rules out.

**`specs/application/` —** the specification of the product itself, split by what a reader can rely on versus how it is made true. `product/` covers what a user or an integrating caller can experience, rely on, or build against, stated as a capability or a guarantee rather than as an implementation choice. `technical/` covers how each of those facts is actually made true: the algorithms, schemas, service boundaries, models, and infrastructure. A product spec and its technical counterpart are two drawings of one subject, each from its own perspective, kept aligned (`specs/methodology/sourcing-and-citation.md § Keeping Specs in Sync § Product and Technical Counterparts`).
