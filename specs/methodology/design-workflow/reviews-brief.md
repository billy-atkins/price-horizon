## A Review's Brief

Every adversarial review and every post-apply review the standard process runs is started with this brief alone, the same in every round, so the design is the one thing that changes between rounds. The brief holds no part of a review's task. The review's section, [`specs/AGENTS.md § Design, Refactor, Refine § The Adversarial Review`](/specs/AGENTS.md#the-adversarial-review) or [`specs/AGENTS.md § Design, Refactor, Refine § The Post-Apply Review`](/specs/AGENTS.md#the-post-apply-review), holds the whole of it, the section its record in [`specs/AGENTS.md § Design, Refactor, Refine § Who Checks What and Why § Check Roles`](/specs/AGENTS.md#check-roles) cites as its Work. The builder fills the brief's blanks as it starts a round, and adds nothing about the design or the rounds before it. What a finding means and where it goes stay the builder's to settle. The brief sits in a fenced block, so no link is written into it and it stays this text:

```text
You are the {adversarial | post-apply} reviewer of a Spec of Record design. You are cold: you did not build or apply it, and you change nothing but your report.

Design: {design document}
Report: {report file}

1. Read specs/AGENTS.md, then specs/methodology/glossary/glossary.md, then {the design document whole | the design document as specs/AGENTS.md § Design, Refactor, Refine § The Post-Apply Review has it read}.
2. Do the {adversarial | post-apply} review as specs/AGENTS.md § Design, Refactor, Refine § {The Adversarial Review | The Post-Apply Review} sets it, as specs/AGENTS.md § Design, Refactor, Refine § Who Checks What and Why § Check Roles [Check: the {adversarial | post-apply} review] has it.
3. Write the report from specs/methodology/working-files/check-report/review-report-form-template.md, writing only the parts specs/methodology/working-files/main.md § A Check's Report § Who Writes Each Part gives the reviewer, and check them as that section has them checked before handing the report back.
```

An audit takes no brief. Whoever starts one, the user or the builder in a design's apply, starts it as [`specs/AGENTS.md § Design, Refactor, Refine § Who Checks What and Why § Check Roles [Check: an audit]`](/specs/AGENTS.md#check-roles) has it made.

## A Research Brief

All research a design hands off starts with this brief, each cold agent of a share given it with its own share, as [`specs/AGENTS.md § Design, Refactor, Refine § Measure Twice, Cut Once § Research`](/specs/AGENTS.md#research) has research shared. Like the review's brief, it holds no part of the research's task, which that section holds, and no part of its report's form, which the research report's form template holds. The builder fills its blanks from the design and adds nothing else. Beside its blanks it names what each kind of search is for and when each target is asked, each as the home it names has it, so the cold agent reads the Searches it is given. Its reading step is the adversarial reviewer's in the review's brief, the design document read whole. The brief sits in a fenced block, so no link is written into it:

```text
You are a cold agent doing research for a Spec of Record design. You are cold: you did not build the design, and you change nothing but your report.

Design: {design document}
Report: {report file}
Entry: {the entry the research's check is logged as}
Cause: {the research's cause, as specs/AGENTS.md § Design, Refactor, Refine § Measure Twice, Cut Once § Research and specs/AGENTS.md § Design, Refactor, Refine § Measure Twice, Cut Once § The Zoom-Out name it, by the entry, report or key recording it}
Places to read: {each place the builder knows to read within your share, one to a line}
Share: {each place of your share, one to a line; or none, where the research is not shared}
Searches: {each Search, its key, what it is for, the goals it serves, its kind, its target, what it asks and, where the research is shared, the paths of your share it is narrowed to, one to a line}

A kind of search, and what each is for, as .ai/skills/search-spec-of-record-scope/ gives them: citers, for every place citing a section, a part or a file; cited sections, for each cited section with the places citing it; lines, for the lines a citation names; terms, for a word, a phrase or an identifier in whatever form it takes, a phrase's words found together and apart within a sentence, asked by default or for exact as specs/methodology/working-files/main.md § A Check's Report § Search § Who Asks for Exact has its kind of search ask; code structure, for the code holding a structure; meaning, for a rule or a fact that may be said in other words, asked as a statement a rule might say and never as a question, as specs/AGENTS.md § Design, Refactor, Refine § Measure Twice, Cut Once § Research has it asked; pattern, only for a flaw in formatting or structure.

A target, and when each is asked, as specs/methodology/working-files/main.md § A Check's Report § Search sets it: current-operative-files, the operative files as they stand, for research, except while a design's uncommitted changes are kept; committed-operative-files, the operative files as the last commit held them, for research made while such changes are kept and for a question of the state before a design's work; current-fixture-files and committed-fixture-files, the fixture files of the kept tests the same two ways, only where a Search asks for the fixture files; working-files, for the working files named.

1. Read specs/AGENTS.md, then specs/methodology/glossary/glossary.md, then the design document whole.
2. Do the research as specs/AGENTS.md § Design, Refactor, Refine § Measure Twice, Cut Once § Research sets it, as specs/AGENTS.md § Design, Refactor, Refine § Who Checks What and Why § Check Roles [Check: a judgment the builder hands off] has it.
3. Write the report from specs/methodology/working-files/check-report/research-report-form-template.md, writing only the parts specs/methodology/working-files/main.md § A Check's Report § Who Writes Each Part gives the cold agent, and check them as that section has them checked before handing the report back.
```
