# Spec of Record: Record types and their records, Worked Examples

**Reference Key:** File \
**Required:** Description

| File | Description |
|---|---|
| `depot-assets.md` | An abstract Asset type and two types extending it, a Vehicle adding fields of its own and a Pallet Rack adding none, each type's records in a record section of their own and none titled with the abstract type's Plural Name, written whole as a file would hold it |
| `employees.md` | An Employee type whose optional Direct Reports field holds a list of Employee records, the records of an Employees section nesting as a tree, each employee written once, beneath their manager, written whole as a file would hold it |
| `inspection-reports.md` | An inspection report's record type, a field holding one record of another type, a field holding a list of records, a nested record ending with a list of plain items, and a record holding two lists in the order its type gives them, each type declared once in a section of its own, written whole as a file would hold it |
| `work-order-statuses.md` | A work order's statuses, a closed set a product spec defines, a fact taking its values from them, and a workflow drawing on the set, written whole as a file would hold it |
