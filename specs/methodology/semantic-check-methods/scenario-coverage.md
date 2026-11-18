## Scenario Coverage

This check reads a product file's test scenarios against the prose they test.

**The sections with no block first.** The reader first finds each capability section that has no `Test Scenarios` block at all. Reading the blocks cannot find a section that has none.

**Each block against its prose, both ways.** The reader then reads each block against its section's prose. The reader looks for a promise or a guardrail with no scenario. The reader also looks for a scenario that asserts something the prose does not say. [`specs/methodology/acceptance-scenarios.md § Deciding What to Write`](/specs/methodology/acceptance-scenarios.md#deciding-what-to-write) has that as a gap in the prose.
