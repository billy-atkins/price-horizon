## Form Templates

A form template holds a form's parts for the step that fills it, so the form is copied rather than recalled. A skill's form templates and the core canon's take one form:
- A form template is a file of its own, named for the form it holds, with `-form-template` ending the name before its extension: `design-document-form-template.md`. A reader listing its folder then tells a form template from instructions or specs without opening it.
- Its first placeholder cites the section stating the form it holds. It holds the form's parts in the order that section gives, each with a placeholder.
- A placeholder is a token in braces, citing the rule or the record type that defines its part. For a value, the token says what kind of value replaces it, `{a few words}`, and the braces are replaced along with the token. For a section kept only in some cases, the token says when the section is kept, and is removed with its braces once the section is kept.
- It is read at the step that fills it, and it leaves each rule setting the form to that rule's home.

A skill keeps its form templates among its references ([`specs/methodology/skills/authoring-a-skill.md § Authoring a Skill`](/specs/methodology/skills/authoring-a-skill.md#authoring-a-skill)). A form template in the core canon is a file unit of its own ([`specs/methodology/spec-placement/where-a-file-goes.md § Where a File Goes`](/specs/methodology/spec-placement/where-a-file-goes.md#where-a-file-goes)).

### Script Checks

**Records:**
  - **Name:** form-template-in-its-form \
    **Tests:** each form template in the core canon cites a section in its first placeholder, each heading it lays out is the heading of a part that section's table of parts gives, in the table's order, and each field it lays out with a placeholder citing a record type's section is a field that type declares, in the type's order \
    **Reads:**
      - `canon-specs`

    **Carried Out By:**
      - `.ai/skills/audit-specs/` `--check-scope`
