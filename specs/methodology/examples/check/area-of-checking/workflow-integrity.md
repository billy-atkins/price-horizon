## Workflow Integrity

A rule of a design's move to approval in a methodology the example invents, with the script check reading the design standing under it, written whole as a file would hold it:

```markdown
## Ready for Approval

A design goes to approval only once each of its steps names the files it changes, so the approver sees the whole of what the design will touch before saying yes.

### Script Checks

**Records:**
  - **Name:** steps-name-their-files \
    **Tests:** each step of a design going to approval names the files it changes, as the Ready for Approval rule has it \
    **Reads:**
      - `none`

    **Carried Out By:**
      - `.ai/skills/plan-depot-changes/` `--check-plan-steps`
```

The unit of the invented skill's script carrying the check out:

```python
# @canon-spec specs/methodology/depot-changes.md § Ready for Approval § Script Checks [Name: steps-name-their-files]
def plan_step_findings(design):
    """Each step of the design names the files it changes."""
    return [(design.path, step.line, f"the step {step.name} names no file it changes") for step in design.steps if not step.files]
```

The rule guards that a design moves through its work validly, so its check falls in workflow integrity, as [`specs/methodology/checks.md § The Areas of Checking`](/specs/methodology/checks.md#the-areas-of-checking) has the area. A design is a working file, of no kind, so the check's Reads holds `none`, as [`specs/methodology/checks.md § Check`](/specs/methodology/checks.md#check) has a check reading the working files. The record states no state of the workflow: the invented methodology's state moving a design to approval runs the check and cites its record, so where the check runs is stated where it runs. The unit carrying it out cites its record.
