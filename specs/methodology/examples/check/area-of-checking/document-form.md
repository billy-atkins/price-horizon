## Document Form

A rule of a field's form in a style file of a methodology the example invents, with the script check holding the files to it standing under it, written whole as a file would hold it:

```markdown
## Due Dates

A work order's Due Date field holds a calendar date written year, month and day, `2026-11-02`, never a weekday or a date relative to another, so every reader and every script reads the same day from it.

### Script Checks

**Records:**
  - **Name:** due-date-written-whole \
    **Tests:** every Due Date field holds a date written year, month and day, as the Due Dates rule has it \
    **Reads:**
      - `application-specs`

    **Carried Out By:**
      - `.ai/skills/check-depot-files/` `--check-due-dates`
```

The unit of the invented skill's script carrying the check out:

```python
# @canon-spec specs/methodology/work-orders.md § Due Dates § Script Checks [Name: due-date-written-whole]
def due_date_findings(root):
    """Every Due Date field holds a date written year, month and day."""
    return [(path, line, "a Due Date not written year, month and day")
            for path, line, value in due_date_fields(root) if not WHOLE_DATE.fullmatch(value)]
```

The rule guards the shape of a field's text, so its check falls in document form, as [`specs/methodology/checks.md § The Areas of Checking`](/specs/methodology/checks.md#the-areas-of-checking) has the area. The check is linked to the rule by where it stands: its record section sits directly under the section declaring the form, so a reader of the rule finds its check there. A script decides the date's form from the files alone, so the check is a Script Check, giving the fields every check gives and no other. The unit carrying it out cites its record by the path of the invented file holding the rule, so a reader of the script finds which check the unit carries out, as [`specs/methodology/skills.md § Authoring a Skill`](/specs/methodology/skills.md#authoring-a-skill) has a unit carrying out a check cite its record.
