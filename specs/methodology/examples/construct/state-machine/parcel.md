## Parcel Journey

A parcel's journey from draft to sent or voided, written whole as a file would hold it. A warehouse clerk packs the parcel and sends it. Sending is an exclusive choice on whether the parcel is on hold, and each move to sent runs an Algorithm as its effect. A held parcel is voided once its hold limit passes, and a purchase is voided by any occurrence of a class:

```markdown
## Parcel

The journey of a parcel from a basket's draft to the carrier, or to being voided with its purchase or once held past its hold limit.

**Construct:** `specs/methodology/modeling-constructs.md § Constructs § State Machine`

**Table Name:** States

| State | Description | Initial | Terminal |
|---|---|---|---|
| draft | a parcel of a basket, not yet packed | Yes | No |
| packed | packed, waiting for a warehouse clerk to send it | No | No |
| held | packed, kept back until a warehouse clerk releases it | No | No |
| sent | handed to the carrier | No | Yes |
| voided | voided with its purchase, or held past its hold limit | No | Yes |

**Table Name:** Transitions

| From | To | Trigger | Guard | Effect |
|---|---|---|---|---|
| draft | packed | a warehouse clerk packs it | none | none |
| draft | voided | the purchase is voided | none | none |
| packed | sent | a warehouse clerk sends it | not(on hold?) | `§ Send Stamp` |
| packed | held | a warehouse clerk sends it | on hold? | none |
| held | sent | a warehouse clerk releases it | none | `§ Send Stamp` |
| packed | voided | the purchase is voided | none | none |
| held | voided | the purchase is voided | none | none |
| held | voided | after hold limit | none | none |

**Table Name:** Trigger Classes

| Member | Class |
|---|---|
| the buyer cancels | the purchase is voided |
| the payment is refunded | the purchase is voided |

## Send Stamp

The moment a parcel leaves for the carrier, recorded as it is sent.

**Construct:** `specs/methodology/modeling-constructs.md § Constructs § Algorithm`

**Inputs:** none

**Output:**

- sent at

**Runs When:** `§ Parcel`

| Step | Action |
|---|---|
| 1 | Set sent at to now() |
| 2 | End |

## Facts

**Records:**

- **Name:** on hold?
  **Type:** boolean
  **Means:** whether the buyer's address failed its check, so the parcel waits for a warehouse clerk

- **Name:** sent at
  **Type:** date and time
  **May Be Absent:** Yes
  **Means:** when the parcel was handed to the carrier

- **Name:** hold limit
  **Type:** days and time duration
  **Means:** how long a parcel may stay held before it is voided
```

When a warehouse clerk sends a packed parcel, the two transitions from packed are an exclusive choice. Their guards are a question and its negation over a fact the file declares. They never both hold. Both moves to sent run Send Stamp as their effect, and Send Stamp's Runs When cites the machine. A voided purchase ends a parcel whether it is a draft, packed or held, with a row for each From. A buyer canceling and a payment refunded each void the purchase, so the trigger is their class, its members its Trigger Classes table's rows. A held parcel's hold limit is counted from its entering held, and the parcel is voided once it passes.
