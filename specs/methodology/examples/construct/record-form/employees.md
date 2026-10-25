## Employees

An Employee type whose optional Direct Reports field holds a list of Employee records, the records of an Employees section nesting as a tree, each employee written once, beneath their manager, written whole as a file would hold it:

```markdown
## Employee

An employee of the depot and, where they manage others, the employees reporting to them. The records of the depot's head sit in this spec, and every other employee's record sits beneath their manager's.

**Construct:** `specs/methodology/modeling-constructs.md § Constructs § Record Form` \
**Plural Name:** Employees \
**Reference Key:** Employee Number

| Field | Unique | Required | Default Value | Values | Holds |
|---|---|---|---|---|---|
| Employee Number | yes | yes | | text | the number payroll knows the employee by |
| Name | no | yes | | text | the employee's name as the register holds it |
| Role | no | yes | | text | the role they hold |
| Direct Reports | no | no | none | a list of `§ Employee` | the employees reporting to them, each a record |

## Employees

**Records:**
  - **Employee Number:** E-100 \
    **Name:** Priya Natarajan \
    **Role:** depot manager \
    **Direct Reports:**
      - **Employee Number:** E-210 \
        **Name:** Tomasz Nowak \
        **Role:** shift supervisor \
        **Direct Reports:**
          - **Employee Number:** E-311 \
            **Name:** Aisha Bello \
            **Role:** forklift operator

          - **Employee Number:** E-312 \
            **Name:** Marco Rossi \
            **Role:** loader

      - **Employee Number:** E-220 \
        **Name:** Hana Sato \
        **Role:** dispatcher
```

The Direct Reports field cites the Employee type's own definition after `a list of`, so the type holds itself, and its records nest as a tree, as [`specs/methodology/modeling-constructs.md § Constructs § Record Form § Held by Value`](/specs/methodology/modeling-constructs.md#held-by-value) has a type hold itself. The tree ends where a record leaves Direct Reports absent, as the forklift operator's, the loader's and the dispatcher's do, since the field is not required. Each employee is written once, held by value inside their manager's record and never shared with another record. The depot manager's record is the one item the Employees section's Records holds, so a citation names that record alone, by its Employee Number, and reaches a report's record through it.
