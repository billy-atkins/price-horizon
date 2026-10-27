## System Integrity

A rule keeping a methodology's bounds, in a methodology the example invents, with the script check holding the project to it standing under it, written whole as a file would hold it:

```markdown
## Scratch Files Stay Local

A skill's scratch files are never committed. Version control ignores the directory holding them, so no scratch file reaches a reader as if it stated something.

### Script Checks

**Records:**
  - **Name:** scratch-directory-ignored \
    **Tests:** a line of the ignore file names the scratch directory and no line un-ignores it, as the Scratch Files Stay Local rule has it \
    **Reads:**
      - `other`

    **Carried Out By:**
      - `.ai/skills/check-depot-files/` `--check-scratch-ignored`
```

The unit of the invented skill's script carrying the check out:

```python
# @canon-spec specs/methodology/depot-scope.md § Scratch Files Stay Local § Script Checks [Name: scratch-directory-ignored]
def scratch_findings(root):
    """A line of the ignore file names the scratch directory, and no line un-ignores it."""
    lines = ignore_lines(root)
    if SCRATCH not in lines or "!" + SCRATCH in lines:
        return [(".gitignore", 0, f"the scratch directory {SCRATCH} is not ignored")]
    return []
```

The rule guards what version control holds, so its check falls in system integrity, as [`specs/methodology/checks.md § The Areas of Checking`](/specs/methodology/checks.md#the-areas-of-checking) has the area. The check is linked by the rule it keeps, and stands under it. It reads the ignore file, of `other`, the scratch directory's path held by the script, so its Reads holds that kind alone. The unit carrying it out cites its record.
