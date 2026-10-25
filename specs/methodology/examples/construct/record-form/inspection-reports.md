## Inspection Reports

An inspection report's record type, a field holding one record of another type, a field holding a list of records, a nested record ending with a list of plain items, and a record holding two lists in the order its type gives them, each type declared once in a section of its own, written whole as a file would hold it:

```markdown
## Inspector

The inspector who signed a report. Its records sit only where a report's Inspector field holds one.

**Construct:** `specs/methodology/modeling-constructs.md § Constructs § Record Form` \
**Plural Name:** Inspectors \
**Reference Key:** Badge

| Field | Unique | Required | Default Value | Values | Holds |
|---|---|---|---|---|---|
| Badge | yes | yes | | text | the badge number the inspector signs with |
| Name | no | yes | | text | the inspector's name as the register holds it |

## Defect

A defect an inspection found. Its records sit only where a report's Defects field holds them.

**Construct:** `specs/methodology/modeling-constructs.md § Constructs § Record Form` \
**Plural Name:** Defects \
**Reference Key:** Code

| Field | Unique | Required | Default Value | Values | Holds |
|---|---|---|---|---|---|
| Code | yes | yes | | text | the defect's code in the inspection standard |
| Severity | no | yes | | "minor", "major", "critical" | how serious the defect is |
| Photos | no | no | none | text | a list, the file name of each photo taken of it |

## Inspection Report

A report an inspector files after inspecting a site. Its records sit in this spec.

**Construct:** `specs/methodology/modeling-constructs.md § Constructs § Record Form` \
**Plural Name:** Inspection Reports \
**Reference Key:** Report

| Field | Unique | Required | Default Value | Values | Holds |
|---|---|---|---|---|---|
| Report | yes | yes | | text | the report's number |
| Site | no | yes | | text | the site inspected |
| Inspector | no | yes | | `§ Inspector` | the inspector who signed it, one record |
| Defects | no | no | none | a list of `§ Defect` | the defects found, each a record |
| Actions | no | no | none | text | a list, each action the site must take |

## Inspection Reports

**Records:**
  - **Report:** IR-1041 \
    **Site:** Northgate depot \
    **Inspector:**
      - **Badge:** 2231 \
        **Name:** Dana Okafor

  - **Report:** IR-1042 \
    **Site:** Riverside yard \
    **Inspector:**
      - **Badge:** 1187 \
        **Name:** Luis Ferreira

    **Defects:**
      - **Code:** D-14 \
        **Severity:** major \
        **Photos:**
          - riverside-d14-east.jpg
          - riverside-d14-west.jpg

      - **Code:** D-31 \
        **Severity:** minor

    **Actions:**
      - fence the east gate
      - file the repair order for D-14
```

The Inspector field holds one record, its Values the citation of the Inspector type's definition. The Defects field holds a list of records, its Values `a list of` and the citation of the Defect type's definition. Neither type's records sit in a record section of their own, and no Values cites one, so nothing bars either type from nesting, and each record nests as [`specs/methodology/modeling-constructs.md § Constructs § Record Form § Held by Value`](/specs/methodology/modeling-constructs.md#held-by-value) has a record held by value. Defect D-14 of report IR-1042 ends with its Photos list, a list of plain items, and the report holds Defects and Actions, two lists, in the order its type gives them, each list two spaces beyond its key. A blank line falls where [`specs/methodology/spec-style.md § Blank Lines`](/specs/methodology/spec-style.md#blank-lines) places one: between two records of one field, and before a field that follows a nested record or a list, since the field opens its block's next paragraph.
