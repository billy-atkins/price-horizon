## A Review's Brief

Every adversarial review and every post-apply review the standard process runs is started with this brief alone, the same in every round, so the design is the one thing that changes between rounds. The brief holds no part of a review's task. The review's section, [`specs/AGENTS.md § Design, Refactor, Refine § The Adversarial Review`](/specs/AGENTS.md#the-adversarial-review) or [`specs/AGENTS.md § Design, Refactor, Refine § The Post-Apply Review`](/specs/AGENTS.md#the-post-apply-review), holds the whole of it, the section its record in [`specs/AGENTS.md § Design, Refactor, Refine § Who Checks What and Why § Check Roles`](/specs/AGENTS.md#check-roles) cites as its Work. The builder fills the brief's blanks as it starts a round, and adds nothing about the design or the rounds before it. What a finding means and where it goes stay the builder's to settle. The brief sits in a fenced block, so no link is written into it and it stays this text:

```text
You are the {adversarial | post-apply} reviewer of a Spec of Record design. You are cold: you did not build or apply it, and you change nothing but your report.

Design: {design document}
Report: {report file}

1. Read specs/AGENTS.md, then specs/methodology/glossary/glossary.md, then the design document whole.
2. Do the {adversarial | post-apply} review as specs/AGENTS.md § Design, Refactor, Refine § {The Adversarial Review | The Post-Apply Review} sets it, as specs/AGENTS.md § Design, Refactor, Refine § Who Checks What and Why § Check Roles [Check: the {adversarial | post-apply} review] has it.
3. Write the report from specs/methodology/working-files/check-report/review-report-form-template.md, writing only the parts specs/methodology/working-files/main.md § A Check's Report § Who Writes Each Part gives the reviewer, and check them as that section has them checked before handing the report back.
```

An audit takes no brief. Whoever starts one, the user or the builder in a design's apply, starts it as [`specs/AGENTS.md § Design, Refactor, Refine § Who Checks What and Why § Check Roles [Check: an audit]`](/specs/AGENTS.md#check-roles) has it made.

## A Research Brief

All research a design hands off starts with this brief, each cold agent of a share given it with its own share, as [`specs/AGENTS.md § Design, Refactor, Refine § Measure Twice, Cut Once § Research`](/specs/AGENTS.md#research) has research shared. Like the review's brief, it holds no part of the research's task, which that section holds, and no part of its report's form, which the research report's form template holds. The builder fills its blanks from the design and adds nothing else. Its reading step is the review's brief's. The brief sits in a fenced block, so no link is written into it:

```text
You are a cold agent doing research for a Spec of Record design. You are cold: you did not build the design, and you change nothing but your report.

Design: {design document}
Report: {report file}
Entry: {the entry the research's check is logged as}
Cause: {the research's cause, as specs/AGENTS.md § Design, Refactor, Refine § Measure Twice, Cut Once § Research and specs/AGENTS.md § Design, Refactor, Refine § Measure Twice, Cut Once § The Zoom-Out name it, by the entry, report or key recording it}
Places to read: {each place the builder knows to read, one to a line}
Share: {each place of your share, one to a line; or none, where the research is not shared}
Searches: {each Search, its key, what it is for, the goals it serves and its pattern, one to a line}

1. Read specs/AGENTS.md, then specs/methodology/glossary/glossary.md, then the design document whole.
2. Do the research as specs/AGENTS.md § Design, Refactor, Refine § Measure Twice, Cut Once § Research sets it, as specs/AGENTS.md § Design, Refactor, Refine § Who Checks What and Why § Check Roles [Check: a judgment the builder hands off] has it.
3. Write the report from specs/methodology/working-files/check-report/research-report-form-template.md, writing only the parts specs/methodology/working-files/main.md § A Check's Report § Who Writes Each Part gives the cold agent, and check them as that section has them checked before handing the report back.
```
