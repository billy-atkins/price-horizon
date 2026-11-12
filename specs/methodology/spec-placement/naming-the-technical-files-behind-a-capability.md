## Naming the Technical Files Behind a Capability

A product spec file may open with a YAML front matter block ([`specs/methodology/external-references.md § External References [Name: YAML]`](/specs/methodology/external-references.md#external-references)) naming which technical files build its capabilities. A product document laid out as a folder holds its front matter in its `main.md`, its file, naming the technical files behind the capabilities of each of the document's files ([`specs/methodology/spec-placement/where-a-file-goes.md § Where a File Goes`](/specs/methodology/spec-placement/where-a-file-goes.md#where-a-file-goes)):

```yaml
---
technical-specs:
  - specs/application/technical/example-data-model.md
  - specs/application/technical/example-service/example.md
---
```

The block holds a list of file paths from the project root, written exactly as they appear anywhere else. The list is sorted in plain character order, so the order is never a judgment call and never signals importance. `technical-specs` is kebab-case ([`specs/methodology/spec-placement/kebab-case-conversion.md § Kebab-Case Conversion`](/specs/methodology/spec-placement/kebab-case-conversion.md#kebab-case-conversion)), as every front matter key here is.

This is a label, not a citation. It names files, never headings, and is never wrapped in the backtick-and-`§` form a citation uses.

**Reference Key:** State \
**Required:** Meaning

| State | Meaning |
|---|---|
| Omitted | Either the file has no technical implementation and never will, or it does but no target has been identified yet. Nothing is asserted about the technical side either way. |
| Populated | One or more file paths named. The ordinary case, once a target is actually known. |

**Direction.** `technical-specs` appears only in a product spec, never in a technical one. It points one way, from product to technical. Product specs govern. Technical specs exist to make them true. There is no reciprocal list, because the technical prose cites the product section it implements ([`specs/methodology/spec-placement/product-or-technical.md § Product or Technical`](/specs/methodology/spec-placement/product-or-technical.md#product-or-technical)).

**How this differs from an `index.md`.** An `index.md` gives breadth within one directory. It is a separate navigational file, describing what every file in that directory contains. `technical-specs` gives depth across directories for one specific file. It lives inside the product file it describes, and names the bounded set of technical files needed to understand how that file's capabilities are built.

**Reading it.** Before working on a technical file, check whether a product file's `technical-specs` names it. If so, that product file's capabilities are what the technical file already fulfills, and what an edit has to keep true.

**Writing it.** A product spec is usually written before any technical content implementing it exists. State the capability in prose with no technical reference of any kind, and leave `technical-specs` omitted. Naming a file before real technical work exists to name would be a guess dressed as a fact. When technical content is later written to fulfill a capability, add that file to the product file's list, in its place in plain character order. The technical prose cites the product section, as [`specs/methodology/spec-placement/product-or-technical.md § Product or Technical`](/specs/methodology/spec-placement/product-or-technical.md#product-or-technical) has each side name the other. The list is the coarse pointer and that citation the precise proof. Both stay.
