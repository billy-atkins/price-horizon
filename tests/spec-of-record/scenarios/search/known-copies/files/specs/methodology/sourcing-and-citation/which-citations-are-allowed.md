## Which Citations Are Allowed

The specifications are layered by what governs what:

```
specs/AGENTS.md
  └ specs/methodology/
      └ specs/application/
          └ product/
              └ technical/
```

The rules of [`specs/AGENTS.md`](/specs/AGENTS.md) and of the methodology reach the files in Spec of Record's scope, as [`specs/methodology/scope/what-spec-of-record-governs.md § What Spec of Record Governs`](/specs/methodology/scope/what-spec-of-record-governs.md#what-spec-of-record-governs) sets. A product spec states what a user can rely on, and a technical spec states how it is made true ([`specs/methodology/spec-placement/product-or-technical.md § Product or Technical`](/specs/methodology/spec-placement/product-or-technical.md#product-or-technical)).

A citation pointing down a layer sends the reader somewhere for a specific purpose. A citation pointing up a layer gives background that benefits the local text.

What a citation may name depends on where it is written. Each row its source matches grants what that row lists:

**Construct:** `specs/methodology/modeling-constructs.md § Constructs § Decision Table` \
**Order:** any \
**Hit Policy:** Collect \
**Conditions:** From

| From | May cite |
|---|---|
| A product spec | another product spec |
| A technical spec | another technical spec, a product spec |
| A methodology spec | another methodology spec; [`specs/AGENTS.md`](/specs/AGENTS.md); the main file of `specs/`; [`specs/architecture.md`](/specs/architecture.md); the skills' directory, a registered skill or a file of one, and the code the skills share, naming what applies its rules |
| [`specs/AGENTS.md`](/specs/AGENTS.md) | any spec; a registered skill or a file of one |
| The main file of `specs/` | [`specs/AGENTS.md`](/specs/AGENTS.md); any spec; a registered skill or a file of one |
| [`specs/architecture.md`](/specs/architecture.md) | [`specs/AGENTS.md`](/specs/AGENTS.md); any spec; a registered skill or a file of one |
| "A product spec", "A technical spec", "A methodology spec" | the project's root `AGENTS.md` as a whole file, never a section of it |
| A `**Construct:**` field, in any spec | the section defining the construct its instance is of, wherever it sits |
| Code the application specs govern | a product spec, a technical spec, or a section of one, never a record, naming what it carries out or checks with an app-spec annotation ([`specs/methodology/sourcing-and-citation/writing-a-citation.md § Writing a Citation § Citing From Code`](/specs/methodology/sourcing-and-citation/writing-a-citation.md#citing-from-code)) |
| A registered skill's script, or the code the skills share | [`specs/AGENTS.md`](/specs/AGENTS.md) or a methodology spec, or a section of one, naming where a copy it holds takes its values from, or a check's record, naming the check a unit carries out, or the section a check enforces while its entry stands in a skill's table, with a canon-spec annotation ([`specs/methodology/sourcing-and-citation/writing-a-citation.md § Writing a Citation § Citing From Code`](/specs/methodology/sourcing-and-citation/writing-a-citation.md#citing-from-code)) |

Code is governed by the specs rather than being a layer of them. The table is the whole permission for citations from these specs, from code, from the skills' scripts, and from [`specs/AGENTS.md`](/specs/AGENTS.md), the main file of `specs/` and [`specs/architecture.md`](/specs/architecture.md). Files outside that set, the project's own root `AGENTS.md` among them, cite these specs under their own rules. The root `AGENTS.md` holds the project's instructions rather than the methodology's. No spec other than the working-files document, its [`specs/methodology/working-files/main.md`](/specs/methodology/working-files/main.md) and every other file under its folder, names a working file ([`specs/methodology/working-files/main.md § The Working Files`](/specs/methodology/working-files/main.md#the-working-files)). No working file is committed, so its name would point a reader at nothing. [`specs/AGENTS.md`](/specs/AGENTS.md) is agent instructions rather than a spec, and it names the working files its procedures act on.

A product spec citing a technical spec would make a promise depend on its own implementation. The `technical-specs` front matter key serves that direction instead ([`specs/methodology/spec-placement/naming-the-technical-files-behind-a-capability.md § Naming the Technical Files Behind a Capability`](/specs/methodology/spec-placement/naming-the-technical-files-behind-a-capability.md#naming-the-technical-files-behind-a-capability)). The key is file-level and coarse by design, so it cannot carry a dependency at heading precision. A methodology spec citing an application spec would make a rule depend on the document it governs.

An application spec cites no methodology spec, and none of [`specs/AGENTS.md`](/specs/AGENTS.md), the main file of `specs/` and [`specs/architecture.md`](/specs/architecture.md). The reason is subject, not direction, since such a citation would point up. An application spec's subject is the product, and how a spec is authored is no part of it. So a reader of the product has no use for the authoring rule behind a sentence. An application spec may still name a construct, because a construct is what its own content is authored as. Its Construct field cites the construct's definition, since the definition is what the instance is held to ([`specs/methodology/modeling-constructs.md § Defining Constructs § References and Names`](/specs/methodology/modeling-constructs.md#references-and-names)). That field is the one citation of the methodology an application spec makes. An application spec does not reach into the methodology, [`specs/AGENTS.md`](/specs/AGENTS.md), the main file of `specs/` or [`specs/architecture.md`](/specs/architecture.md) for their own claims. [`specs/AGENTS.md`](/specs/AGENTS.md) holds the methodology's own rules, the main file of `specs/` what the canon has every specification share, and [`specs/architecture.md`](/specs/architecture.md) describes how the methodology lays the specifications out.
