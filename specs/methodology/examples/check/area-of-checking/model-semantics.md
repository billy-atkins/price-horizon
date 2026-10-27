## Model Semantics

A rule of a construct's soundness in the file of a methodology the example invents defining the construct, with the script check holding each instance to it standing under it, written whole as a file would hold it:

```markdown
## Shift Rota

A rota assigns each shift of a week to one crew. Its rows are the week's shifts, and no shift is assigned twice, so a crew reading the rota finds one answer for the shift it asks about.

### Script Checks

**Records:**
  - **Name:** shift-assigned-once \
    **Tests:** no two rows of a rota name the same shift, as the Shift Rota rule has it \
    **Reads:**
      - `canon-specs`
      - `application-specs`

    **Carried Out By:**
      - `.ai/skills/check-depot-files/` `--check-shift-rotas`
```

The unit of the invented skill's script carrying the check out:

```python
# @canon-spec specs/methodology/rotas.md § Shift Rota § Script Checks [Name: shift-assigned-once]
def rota_findings(root):
    """No two rows of a rota name the same shift."""
    found = []
    for path, rota in rotas(root):
        shifts = [row["Shift"] for row in rota.rows]
        found += [(path, rota.line, f"the shift {s} assigned twice") for s in sorted(set(shifts)) if shifts.count(s) > 1]
    return found
```

The rule guards that a construct's instance is unambiguous, so its check falls in model semantics, as [`specs/methodology/checks.md § The Areas of Checking`](/specs/methodology/checks.md#the-areas-of-checking) has the area. The check stands under the construct's definition, which is its link to what it checks. A rota may stand in the methodology's worked examples or in the application specs, so the check's Reads lists both kinds of file. The unit carrying it out cites its record.
