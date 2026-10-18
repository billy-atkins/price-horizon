## Work Order Statuses

A work order's statuses, a closed set a product spec defines, a fact taking its values from them, and a workflow drawing on the set, written whole as a file would hold it:

```markdown
## Work Order Status

A status a work order can hold, the set the product owner settles before, and apart from, the workflows that move a work order between them, each with the code integrations exchange for it. Its records sit in this spec.

**Construct:** `specs/methodology/modeling-constructs.md § Constructs § Record Form`

**Plural Name:** Work Order Statuses

**Reference Key:** Name

| Field | Unique | Required | Default Value | Values | Holds |
|---|---|---|---|---|---|
| Name | yes | yes | | text | the status as users read it |
| Description | no | yes | | text | what it means for a work order to hold it |
| Is Active | no | no | Yes | "Yes", "No" | whether a work order may still be given it |
| Code | yes | yes | | text | the identifier integrations exchange for it, never changed once published |

## Work Order Statuses

**Records:**

- **Name:** Open
  **Description:** raised, not yet given to a technician
  **Code:** WO-OPEN

- **Name:** Assigned
  **Description:** given to a technician to carry out
  **Code:** WO-ASGN

- **Name:** On Hold
  **Description:** paused awaiting parts, retired, no workflow giving it any longer
  **Is Active:** No
  **Code:** WO-HOLD

- **Name:** Completed
  **Description:** carried out and signed off
  **Code:** WO-DONE

- **Name:** Canceled
  **Description:** withdrawn before it was carried out
  **Code:** WO-CANC

## Facts

**Records:**

- **Name:** work order status
  **Type:** string
  **Values:** `§ Work Order Statuses`
  **Means:** the status a work order holds

## Work Order

The workflow of a work order raised through the portal.

**Construct:** `specs/methodology/modeling-constructs.md § Constructs § State Machine`

**Recorded In:** work order status: `§ Facts [Name: work order status]`

**Table Name:** States

| State | Description | Initial | Terminal |
|---|---|---|---|
| Open | `§ Work Order Statuses [Name: Open]`, waiting in the portal's queue for a dispatcher | Yes | No |
| Assigned | `§ Work Order Statuses [Name: Assigned]`, its technician notified by the portal | No | No |
| Completed | `§ Work Order Statuses [Name: Completed]` | No | Yes |
| Canceled | `§ Work Order Statuses [Name: Canceled]` | No | Yes |

**Table Name:** Transitions

| From | To | Trigger |
|---|---|---|
| Open | Assigned | a dispatcher assigns it |
| Open | Canceled | the requester cancels it |
| Assigned | Completed | the technician signs it off |
| Assigned | Canceled | the requester cancels it |
```

The statuses are records, not a Basic Table's rows, since Is Active takes a default and is held to its Values, and Code is unique on its own ([`specs/methodology/modeling-constructs.md § When to Use Which § A Table's Construct`](/specs/methodology/modeling-constructs.md#a-tables-construct)). The defining section, titled with the type's name, declares the type. Its Plural Name titles the record section, and its Reference Key, Name, is what a citation of a status names. Code is unique on its own and never cited. On Hold writes Is Active, where it differs from its default. The fact's Values cite the record section, so the fact's values are the statuses' Names. The State Machine recorded in the fact uses all but the retired On Hold. Each state's description opens with its status's record, then says what goes on in that state in this workflow.
