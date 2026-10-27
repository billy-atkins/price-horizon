## Implementation Conformance

A rule of code carrying out the specs in a methodology the example invents, with the script check reading the code for it standing under it, written whole as a file would hold it:

```markdown
## Annotated Units

Each unit of the governed code carrying out a spec names the section it carries out, on the unit's first line, so a reader of the code finds the promise it keeps.

### Script Checks

**Records:**
  - **Name:** unit-names-its-spec \
    **Tests:** each annotation in the governed code names a section that exists and stands where its unit starts, as the Annotated Units rule has it \
    **Reads:**
      - `application-specs`
      - `code`

    **Carried Out By:**
      - `.ai/skills/verify-depot-code/` `--check-unit-annotations`
```

The unit of the invented skill's script carrying the check out:

```python
# @canon-spec specs/methodology/depot-code.md § Annotated Units § Script Checks [Name: unit-names-its-spec]
def annotation_findings(root, sections):
    """Each annotation in the governed code names a section that exists and stands where its unit starts."""
    return [(a.path, a.line, f"an annotation naming {a.target}, which no spec holds, or standing away from its unit's start")
            for a in annotations(root) if a.target not in sections or not a.at_unit_start]
```

The rule guards that code carries out what the specs state, so its check falls in implementation conformance, as [`specs/methodology/checks.md § The Areas of Checking`](/specs/methodology/checks.md#the-areas-of-checking) has the area. The area's link is the annotation, held where the unit it marks starts: the governed code's annotations the check reads, and the one on the script's unit carrying the check out. The check stands under the rule the annotation keeps. It reads the governed code and the application specs its annotations name, so its Reads holds both kinds, and its Carried Out By names the invented skill checking the code.
