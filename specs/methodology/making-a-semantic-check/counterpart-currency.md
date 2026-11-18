## Counterpart Currency

This check reads a product file against the technical files that build its capabilities.

The reader makes a pass of each kind over each pairing:
- **From the product file's list.** The reader takes the product file's `technical-specs` front matter as the map and reads both sides. [`specs/methodology/spec-placement/naming-the-technical-files-behind-a-capability.md § Naming the Technical Files Behind a Capability`](/specs/methodology/spec-placement/naming-the-technical-files-behind-a-capability.md#naming-the-technical-files-behind-a-capability) says which file holds that front matter.
- **From the technical side.** The reader checks that each product section a technical file cites sits in a product file whose list names that technical file. A missing entry is the more likely failure, and the list cannot show it.
- **For an entry that cites nothing back.** The reader looks for an entry naming a technical file that cites nothing in that product file. [`specs/methodology/spec-placement/naming-the-technical-files-behind-a-capability.md § Naming the Technical Files Behind a Capability`](/specs/methodology/spec-placement/naming-the-technical-files-behind-a-capability.md#naming-the-technical-files-behind-a-capability) says which of two things such an entry is, and reading decides between them. This pass takes judgment, so it is easy to skip.

**What is no finding.** The two sides are meant to overlap, as [`specs/methodology/spec-placement/product-or-technical.md § Product or Technical`](/specs/methodology/spec-placement/product-or-technical.md#product-or-technical) explains. The finding is a side that has stopped doing its own job.
