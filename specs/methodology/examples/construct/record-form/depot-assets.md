## Depot Assets

An abstract Asset type and two types extending it, a Vehicle adding fields of its own and a Pallet Rack adding none, each type's records in a record section of their own and none titled with the abstract type's Plural Name, written whole as a file would hold it:

```markdown
## Asset

Something the depot owns and tracks by its asset tag. Every asset is a vehicle or a pallet rack, so the type holds no records of its own, and each asset's record sits in the section of its kind.

**Construct:** `specs/methodology/modeling-constructs.md § Constructs § Record Form` \
**Plural Name:** Assets \
**Modifier:** Abstract \
**Reference Key:** Asset Tag

| Field | Unique | Required | Default Value | Values | Holds |
|---|---|---|---|---|---|
| Asset Tag | yes | yes | | text | the tag the asset register knows the asset by |
| Location | no | yes | | text | the bay or yard where the asset stands |

## Vehicle

A vehicle the depot runs. Its records sit in this spec's Vehicles section.

**Construct:** `specs/methodology/modeling-constructs.md § Constructs § Record Form` \
**Extends:** `§ Asset` \
**Plural Name:** Vehicles

| Field | Unique | Required | Default Value | Values | Holds |
|---|---|---|---|---|---|
| Registration | yes | yes | | text | the plate it is registered under |
| Payload | no | no | unknown | text | the most it may carry, in kilograms |

## Pallet Rack

A pallet rack standing in the depot. Its records sit in this spec's Pallet Racks section.

**Construct:** `specs/methodology/modeling-constructs.md § Constructs § Record Form` \
**Extends:** `§ Asset` \
**Plural Name:** Pallet Racks

## Vehicles

**Records:**
  - **Asset Tag:** A-0101 \
    **Location:** yard 2 \
    **Registration:** KX21 PLM \
    **Payload:** 3500

  - **Asset Tag:** A-0102 \
    **Location:** yard 2 \
    **Registration:** KX22 RTA

## Pallet Racks

**Records:**
  - **Asset Tag:** A-0450 \
    **Location:** bay 7

  - **Asset Tag:** A-0451 \
    **Location:** bay 8
```

The Asset type's Modifier is `Abstract`, so it is a base, as [`specs/methodology/modeling-constructs.md § Constructs § Record Form`](/specs/methodology/modeling-constructs.md#record-form) has an abstract type. It declares the Asset Tag and Location fields and the Reference Key, and each type extending it holds those fields first and takes that key. A vehicle's record gives the Asset Tag and Location before the Registration and Payload its own type adds. The Pallet Rack type declares no table of record fields, so its records hold the Asset type's fields alone. Assets names the records of both kinds together, and no section titled `Assets` holds records, since an asset is always a vehicle or a pallet rack. No field cites the Asset type, because no record is an Asset of its own. A field holding a vehicle cites the Vehicle type's definition.
