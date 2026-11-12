## A Product Module

For a domain that decomposes into sub-parts, a product module is a folder directly under `specs/application/product/`. For a domain that is one cohesive mechanism, it is a single document in that directory's root, one file, or a folder named for it where it holds more than one file unit ([`specs/methodology/spec-placement/where-a-file-goes.md § Where a File Goes`](/specs/methodology/spec-placement/where-a-file-goes.md#where-a-file-goes)). A module also holds each root file named in its domain's account in the product specs' `architecture.md`.

A change to a module's code reads:
- the module's product specs;
- the technical files they name in their `technical-specs` front matter ([`specs/methodology/spec-placement/naming-the-technical-files-behind-a-capability.md § Naming the Technical Files Behind a Capability`](/specs/methodology/spec-placement/naming-the-technical-files-behind-a-capability.md#naming-the-technical-files-behind-a-capability)): a file only this module names is read whole, and a file several modules name is read at the sections this module's code needs.

Every module also reads what no module owns:
- the product specs' own `index.md` and `architecture.md`, and any vision or overview of the product;
- each root file the product specs' `architecture.md` names as held by no domain;
- the technical specs' `architecture.md`;
- the technical specs' stack, `stack.md` ([`specs/methodology/spec-placement/technical-stack.md § The Technical Stack`](/specs/methodology/spec-placement/technical-stack.md#the-technical-stack));
- the technical specs' environments, `environments.md` ([`specs/methodology/spec-placement/environments.md § Environments`](/specs/methodology/spec-placement/environments.md#environments)).

Any other product file or folder that the product specs' `architecture.md` does not name is a gap in the specs. So is technical content that no module's front matter reaches. Each such gap is put right in the specs before code is written for it.
