## Authoring a Skill

A skill captures a procedure this project has already worked out, so the next agent does not rediscover it by repeating the mistakes that produced it. Each skill lives in its own directory under `.ai/skills/`. A skill that is part of the methodology is registered by the test [`specs/methodology/skills/registered-skills.md § Registered Skills`](/specs/methodology/skills/registered-skills.md#registered-skills) states.

**Name it verb-target, in kebab-case.** `author-mermaid-diagram`, not `mermaid` or `diagrams`. The verb states the action, and the target states what it acts on. Its characters are written as [`specs/methodology/spec-placement/kebab-case-conversion.md § Kebab-Case Conversion`](/specs/methodology/spec-placement/kebab-case-conversion.md#kebab-case-conversion) has kebab-case written. Someone scanning the directory can then tell whether a skill applies without opening it. That directory name is the skill's name everywhere else it appears.

**`SKILL.md` is the entry point.** A skill takes the Agent Skills format ([`specs/methodology/external-references.md § External References [Name: Agent Skills]`](/specs/methodology/external-references.md#external-references)). Its `SKILL.md` opens with YAML front matter carrying `name` and `description`. The `name` matches the directory and is at most 64 characters. The `description` is at most 1,024 characters. Write the description to answer "when would someone reach for this", not "what is this about". A description that only names the subject leaves a reader guessing at the trigger, and removing that guess is the one thing a description exists to do.

**A skill's steps sit under a `## Workflow` heading.** They sit there in the skill's `SKILL.md`, and in each reference adding steps, in the order they run. Each step is a `###` heading or a bold lead-in. The check on a section stating operating rules finds there the step carrying its rules out, by the citation the step carries ([`specs/methodology/scope/rules-and-skills.md § Rules and Skills`](/specs/methodology/scope/rules-and-skills.md#rules-and-skills)). A step carrying a check out names it as [`specs/methodology/checks.md § Check`](/specs/methodology/checks.md#check) has a check named where it runs.

**A skill gives each rule governing its work that it does not keep a point-of-use citation.** The skill does not restate the rule, per [`specs/methodology/sourcing-and-citation/one-home-per-fact.md § One Home Per Fact`](/specs/methodology/sourcing-and-citation/one-home-per-fact.md#one-home-per-fact). Nor does it leave the rule out, which would send a cold agent to re-derive it. Beside the citation, the skill adds only what the cited section asks of a citing place. Such a rule lives in [`specs/AGENTS.md`](/specs/AGENTS.md) or `specs/methodology/`, as [`specs/methodology/scope/rules-and-skills.md § Rules and Skills`](/specs/methodology/scope/rules-and-skills.md#rules-and-skills) has a rule live, and never in another skill. What two skills share belongs above both, and a skill cites into `.ai/skills/` only its own files. `specs/application/` is different. It is where the work is done, not a body of rules, so a skill works on it rather than citing it for how to work.

**A rule a skill keeps names its check.** A skill keeps only an operating rule no other skill needs, as [`specs/methodology/scope/rules-and-skills.md § Rules and Skills`](/specs/methodology/scope/rules-and-skills.md#rules-and-skills) has a rule live. The skill checks each rule it keeps, and the rule names that check beside it. The check is a script check, named by its script's flag, where the work, an agent's among it, has a pattern or a schema a script can verify. It is a semantic check, named by the Workflow step making it, where the rule takes judgment. The check takes no Check record, as [`specs/methodology/checks.md § Check`](/specs/methodology/checks.md#check) has it, so the script carrying it out cites nothing back.

**A skill is written clearly, for a cold agent.** Per [`specs/methodology/spec-style/clear-prose.md § Clear Prose`](/specs/methodology/spec-style/clear-prose.md#clear-prose).

**Tooling goes in a `scripts/` child directory.** The entry-point script carries exactly the skill's own name: `.ai/skills/author-mermaid-diagram/scripts/author-mermaid-diagram.py`. Helpers sit beside it under their own names. Most skills will only ever have one script, and the convention costs nothing there. It earns itself in the rarer case of several. There, a name matching the skill's own tells an agent listing the directory, or a person browsing it, which file is the way in, without either having to read one. Apply the convention from the start rather than when another script appears, since by then the original is already named something else. An agent runs only a skill's entry script, so whatever a skill does is reached through the skill.

**Code two skills share goes in `.ai/skills/lib/`.** The code is a module of its own, named for what it does in Python's module form ([`specs/methodology/external-references.md § External References [Name: Python]`](/specs/methodology/external-references.md#external-references)), as `design_documents.py`. The skills' entry scripts import it, and no agent runs it directly. Two skills needing the same check share one copy of it rather than two that drift apart.

**A script takes where a line stands from the one reading.** One module of the shared code, `.ai/skills/lib/reading.py`, works out where a line of a file stands and what form a citation takes. Where a line stands is the headings it is under, and whether it is in running text, a heading, a table or a fenced block. A script that needs any of this takes it from that module, and keeps no reader of its own. Two readers of the same file drift apart, and two checks then answer differently of one file. The module reads a file as [`specs/methodology/spec-style/markdown.md § Markdown`](/specs/methodology/spec-style/markdown.md#markdown) has it read, and a citation as [`specs/methodology/sourcing-and-citation/writing-a-citation.md § Writing a Citation`](/specs/methodology/sourcing-and-citation/writing-a-citation.md#writing-a-citation) writes one. What a check judges of a file stays the check's own.

**Instructions only some paths need go in a `references/` child directory.** Each path has a file of its own, read at the step that forks to it, so a path that does not need the instructions never loads them. Where a skill forks on the kind of specification, its references for the kinds are `references/app-specs.md` and `references/canon-specs.md`.

**A form template a step fills goes in `references/` too.** It takes the form [`specs/methodology/scope/form-templates.md § Form Templates`](/specs/methodology/scope/form-templates.md#form-templates) gives every form template.

**A skill's scratch space, and its plans, are directories of its own among the working files.** They take the form [`specs/methodology/working-files/main.md § The Working Files`](/specs/methodology/working-files/main.md#the-working-files) gives them.

**A script's actions are flags named verb-target.** A flag is named as a skill is: `--check-design-form`, `--show-workstack`. An agent then reads what a run does from the flag alone. The target says what the action acts on, and the verb what kind of action it is:
- a check reports what is wrong;
- a show describes a state;
- a verb changing a file, such as stamp, says that it does.

A flag setting how an action runs, rather than choosing one, is named for what it holds, as `--output-directory`. Flags combine in one run, so a capability added is a flag added. A run naming no action prints the script's usage and exits 2. A flag's words are whole words. A flag is never taken abbreviated, since an abbreviation can mean more than one thing. So every run's command line says what it does.

**A skill's account of its script.** What a skill's text says its script does stays true of the script: each flag it names, and each row saying what the script checks or lists. A change to the script changes that account in the same change.

**Scripts are Python.** Wherever that is achievable, a script imports only the standard library, the skill's own helpers beside its entry script, and the code the skills share. A script needing an install step will not run at the moment it is needed, so a script requires something external only where its capability needs it. Such a script checks for everything it requires before it reads or writes. Where something is missing and another path gives the same answer, a local tool when present and a documented remote or manual path when not, the script takes that path. It reports which one ran, so a reader knows what they are trusting. Where no other path gives the same answer, the script stops and tells the user what is missing and why the script needs it, with how to install it where the script knows. A script never carries on by a path giving a lesser answer, since its reader would take that answer as whole.

**A script's copy of the canon's values, or the canon read in place.** A script checks against values the canon states. It either keeps its own copy of them or reads them from the canon as it runs. It keeps a copy where a value gone missing would be a defect. The copy guards the methodology. An accidental change to the canon shows as a difference between the two. A deliberate change has to update the copy in the same change, which brings its effect on the script into that change's scope. `.ai/skills/lib/spec_checks.py` keeps such a copy of the kinds of file in scope, and reports any difference from [`specs/methodology/scope/what-spec-of-record-governs.md § What Spec of Record Governs`](/specs/methodology/scope/what-spec-of-record-governs.md#what-spec-of-record-governs) for the user to review. A value whose change is an editorial decision, as a word in a list a style check reads, is read in place. A copy there would only make each deliberate edit ask twice. A record type is read in place too, from its declaration ([`specs/methodology/modeling-constructs.md § Constructs § Record Form`](/specs/methodology/modeling-constructs.md#record-form)). A construct's Reference Key is read in place from the field its definition declares ([`specs/methodology/modeling-constructs.md § Constructs § Keyed Construct`](/specs/methodology/modeling-constructs.md#keyed-construct)). The check reads each declaration itself, so a declaration gone missing fails the check outright. Each copy carries a canon-spec annotation ([`specs/methodology/glossary/glossary.md`](/specs/methodology/glossary/glossary.md)) above it, written as [`specs/methodology/sourcing-and-citation/writing-a-citation.md § Writing a Citation § Citing From Code`](/specs/methodology/sourcing-and-citation/writing-a-citation.md#citing-from-code) writes one, citing the area its values come from. A cold agent then finds what the code stands for, and the audit confirms the area is still there.

**Forms read from the canon beside the script, the project's data from its root.** A script reads each form it reads from the canon standing beside its own code. That is the project's canon, or a copy's canon where the script runs from a copy of the project's files. It reads what it checks, searches or appends to from the root it is given. A few tables of the canon are not forms but the project's data, the subject a script reads of the project it is run over. A check reads such a table from that project alone, and reports it missing where the project holds none, never reading the table beside the script's own code in its place. Every other text of the canon a script reads is a form. The tables that are the project's data:

**Reference Key:** Table \
**Required:** Held In

| Table | Held In |
|---|---|
| the table of working files | [`specs/methodology/working-files/main.md`](/specs/methodology/working-files/main.md) |
| the registry of skills | [`specs/methodology/skills/registered-skills.md`](/specs/methodology/skills/registered-skills.md) |
| the other names the glossary gives a term | [`specs/methodology/glossary/glossary.md`](/specs/methodology/glossary/glossary.md) |
| the ledger of rules and the checks enforcing them | [`specs/methodology/scope/rules-and-skills.md`](/specs/methodology/scope/rules-and-skills.md) |
| the table of the audit's checks | [`.ai/skills/audit-specs/SKILL.md`](/.ai/skills/audit-specs/SKILL.md) |
| the table of the code's checks | [`.ai/skills/verify-spec-implementation/SKILL.md`](/.ai/skills/verify-spec-implementation/SKILL.md) |
| the register of external standards | [`specs/methodology/external-references.md`](/specs/methodology/external-references.md) |
| the tables of words the prose checks read | [`specs/methodology/spec-style/clear-prose.md`](/specs/methodology/spec-style/clear-prose.md) and [`specs/methodology/spec-style/what-a-finished-spec-reads-like.md`](/specs/methodology/spec-style/what-a-finished-spec-reads-like.md) |

**A unit carrying out a check cites its record.** A unit of a skill's script, or of the code the skills share, that carries out a check carries a canon-spec annotation citing the check's record, as narrow as the unit. The annotation sits as an app-spec annotation sits on the code carrying out its spec ([`specs/methodology/code.md § Citing the Specs From Code`](/specs/methodology/code.md#citing-the-specs-from-code)), so a cold agent finds which check the unit carries out. Until a check's entry in a skill's table moves into a record, a unit carrying the entry out, whole or in part, carries a canon-spec annotation citing each section of the entry that its part enforces, so a test of the unit finds it by the same citation. A unit carrying out no check, as one handing on the findings of others, cites none.

**Record what actually went wrong.** A skill earns its length by naming the failures that motivated it: the trap that only shows up at the wrong moment, and the fix that is not obvious from the symptom. Anything a reader can derive from the underlying tool's own documentation does not need to be in the skill.

### Kept Tests

A script's kept tests ([`specs/methodology/glossary/glossary.md`](/specs/methodology/glossary/glossary.md)) hold what the script does, so a change that breaks it is found by a run and not by the next design to use it. A script is its code together with each file of the canon it reads a form from as it runs, so a change to a form alone changes the script.

**The kept tests stand under `tests/spec-of-record/`.** The registered runner's settings, `pytest.ini`, and what every test is handed, `conftest.py`, stand in the folder itself and nowhere else. The tests' code stands under `scripts/`. The fixture files stand under `fixtures/`. A fixture file is of its own kind, and each other file of the folder is a file of the skills, as [`specs/methodology/scope/what-spec-of-record-governs.md § What Spec of Record Governs`](/specs/methodology/scope/what-spec-of-record-governs.md#what-spec-of-record-governs) has them. No file kept under the folder carries the name of an agent instructions file, `AGENTS.md` ([`specs/methodology/external-references.md § External References [Name: AGENTS.md]`](/specs/methodology/external-references.md#external-references)), so nothing looking for such a file by its name finds one there.

**The kept tests are run by pytest.** pytest ([`specs/methodology/external-references.md § External References [Name: pytest]`](/specs/methodology/external-references.md#external-references)) finds, selects and runs each test, and writes the run's report. A test is written for pytest and uses pytest's own means for each thing pytest gives: finding and naming a test, handing a test what it needs, marking it, and running code before and after it. No set of tests holds a runner of its own.

**A set of kept tests is a folder named for its script.** It stands at `tests/spec-of-record/scripts/<script>/`, as `search/` is the search's. A test is a function named `test_` and what it holds, in a file of the set named `test_` and what its tests are of. The set's `conftest.py` says which files are its script's, by names written out at its top level:

**Reference Key:** Name \
**Required:** Holds

| Name | Holds |
|---|---|
| `SCRIPT_FILES` | a tuple of paths, the files holding the script's code |
| `FORM_FILES` | a tuple of paths, each file of the canon the script reads a form from as it runs, each named by its own path and none by a folder's |
| `ACTIONS_IN` | a path, the file of the script's code stating its actions |

A path of `SCRIPT_FILES` ending in a slash names each file beneath it. A kept comparison stands in a script's set as `comparison.py`, which the runner takes for no test. The design script holds one, which shows the designs a change reads differently, as [`specs/methodology/working-files/main.md § A Check's Report § Kinds of Builder Check [Check Kind: differential test]`](/specs/methodology/working-files/main.md#kinds-of-builder-check) has it judged.

**A script holding kept tests states its actions in one form.** The file its set names in `ACTIONS_IN` holds a tuple named `FLAGS` at its top level, with a row to each action, each row opening with the action's flag. So a check reads a script's actions from its file alone, running nothing.

**A test says what it holds.** It says so by pytest's markers, which `pytest.ini` declares, and by a canon-spec annotation:

**Reference Key:** Marker \
**Required:** Says

| Marker | Says |
|---|---|
| `action` | each action of its script the test holds, by the flag the script states the action under, whether the test calls the unit carrying the action out or runs the entry script with the flag |
| `passes` | that the test holds what it names where that passes; given names, that it holds those alone so |
| `reports` | that the test holds what it names where that reports; given names, that it holds those alone so |
| `reads` | the fixtures the test takes: a fixture file's name, then the key of each fixture taken from it |

A test holding a Script Check carries a canon-spec annotation ([`specs/methodology/glossary/glossary.md`](/specs/methodology/glossary/glossary.md)) citing the check's record, and a test holding a check a skill's table enforces carries one citing the section the table enforces, each in the comment lines directly above the test, written as [`specs/methodology/sourcing-and-citation/writing-a-citation.md § Writing a Citation § Citing From Code`](/specs/methodology/sourcing-and-citation/writing-a-citation.md#citing-from-code) writes one. What a test names is its actions and the checks it cites. A test's annotation says the test holds the check. It never counts as a unit carrying the check out.

**A test takes what it needs from what the runner hands it.** `conftest.py` hands a test each of these, by pytest's way of handing a test what it asks for by name:

**Reference Key:** Handed \
**Required:** Holds

| Handed | Holds |
|---|---|
| `work` | the test's own folder within the run's folder, empty as the test starts and removed as it ends |
| `fixtures` | the snippet of each fixture the test's `reads` marker names, by its key, and of no other fixture |
| `project_files` | the folder holding the files the tests are run from: the project root, or the folder of a copy of the project's files |
| `run_folder` | the run's folder |

A test builds everything it needs within `work`, or holds it in memory, and writes nowhere else. A project of fixtures it runs the script over is one or the other: written within `work`, or held in memory as the scope a unit taking one is handed, which writes nothing. What several tests of one file share, a file's own pytest fixture builds once within the run's folder.

The runner hands a test nothing that stands in for an assertion.

#### A Kept Test's Shape

**A test holds one behavior of one unit.** It imports the unit from the code the skills share or from its script's own code, calls it with a small input, and asserts what it returns or what it writes by pytest's own `assert`. The cases of one behavior, each a fixture or a value, are handed to one test by pytest's parameters, each case a test of its own in the run's report. So a failing test names the behavior that broke, and a test reads in a few lines.

**A few tests hold an entry script's wiring.** A test runs an entry script as a process of its own only to hold that the script takes an action's flag, reaches the unit carrying it out, prints what it gives and exits as it says, one test to each such part. What the unit does is held by the tests calling it, each marked with the action the unit carries out, so an action is held where it passes and where it reports by the tests of its unit.

**A test works with its fixtures alone.** No test writes to, copies or takes as its subject a file of the canon or a real working file. What a test searches, ranks, audits or validates is fixtures. So is what the script reads of the project it is run over as its data, each table [`§ Authoring a Skill`](#authoring-a-skill) lists as the project's data among it. A test gives such a table by a fixture placed at the table's path. That fixture is no file of the canon: its rows are of a subject that is not the canon's, and none is a row of the canon's own table. A script reads its forms from the canon beside its own code, so a test has the script read them from the canon as it stands, whether it calls a unit or runs an entry script over a project of fixtures. No project a test builds holds a file of the canon or a copy of the skills' code. Each variant of a case is a fixture of its own, and no test alters a fixture's text to make one. A fault a check was once found with is held by a faulty fixture, the input the fault mishandled, which a test has the check report.

**No test runs the kept tests.** A unit of a run, choosing what to run, sizing the run or reading its report, is held by calling it, never by starting a run. A test of an action that runs a set of tests has it run a set written as fixtures.

#### Fixture

A fixture ([`specs/methodology/glossary/glossary.md`](/specs/methodology/glossary/glossary.md)) stands in a fixture file as an entry of this type, a record type ([`specs/methodology/modeling-constructs.md § Constructs § Record Form`](/specs/methodology/modeling-constructs.md#record-form)):

**Construct:** `specs/methodology/modeling-constructs.md § Constructs § Record Form` \
**Plural Name:** Fixtures \
**Reference Key:** Fixture

| Field | Unique | Required | Default Value | Values | Holds |
|---|---|---|---|---|---|
| Fixture | yes | yes | | text | its key, by which a kept test takes it |
| Holds | no | yes | | text | what the snippet holds, as plain fact, calling it neither right nor wrong and naming no test |
| Snippet | no | yes | | text | what the tests read, Markdown or code or data of another language, in a fenced block naming its language, and only what the tests reading it need |

**The fixture files stand in one folder.** They stand under `tests/spec-of-record/fixtures/` and nowhere else. Each file there is a Markdown file of fixtures or the folder's index. A file of fixtures holds a `**Records:**` list of fixtures and no other text. A fixture's key is lower-case words joined by hyphens, and no two fixtures of one file share a key. Its Snippet's fenced block stands in from the fixture's fields as a record's block does, and a test is handed the block's text with that indent taken off.

**A fixture is governed by the tests it serves.** A scenario governs the test that carries it out the same way ([`specs/methodology/acceptance-scenarios.md`](/specs/methodology/acceptance-scenarios.md)). Its Holds says what the snippet holds and calls it neither right nor wrong. The test says how it uses the fixture and what it expects of it, so one fixture may serve one test as text a check passes and another as text a check reports. A snippet states nothing: no reader holds it to be true, and it may break a rule of the canon for a spec on purpose. A fixture holds only what the tests reading it need. No fixture is written into a test's code, and a variant a test needs is a fixture of its own ([`§ Authoring a Skill § Kept Tests § A Kept Test's Shape`](#a-kept-tests-shape)).

**A test reads an existing fixture where one already fits.** An agent writing a test looks for a fixture that fits before it writes one: it reads the folder's index, then the Holds of the fixtures in the file the index points it to, or it searches the fixture files (`.ai/skills/search-spec-of-record-scope/`). No fixture is changed to fit a second test. Where none fits as it stands, the test takes a new one.

**The folder's index lists each fixture file.** `tests/spec-of-record/fixtures/index.md` takes the form [`specs/methodology/spec-placement/index-architecture-detail.md § Index, Architecture, Detail`](/specs/methodology/spec-placement/index-architecture-detail.md#index-architecture-detail) gives an index: a title, and a table naming each file of the folder with its description. The form is stated here since that section's rule on a directory's index reaches the specs alone. A file's description says what its fixtures hold, fully enough for an agent to tell whether the file may hold a fixture it needs. It names no test, since which tests read a fixture is the tests' to say.

#### A Run

**A run is made by the design script or by hand.** The design script's `--check-kept-tests` runs the kept tests, as [`§ Authoring a Skill § Kept Tests § When the Kept Tests Are Run`](#when-the-kept-tests-are-run) has it. By hand, from the folder holding the files to be tested, which is the project root unless they stand in a copy of the project's files:

```
python -B -m pytest tests/spec-of-record
```

A run by hand takes pytest's own ways of choosing tests, a file, a test or a word of a test's name. It also takes `--action` with a flag, for the tests naming that action, `--script-check` with a check's Name, for the tests citing that check.

**A run leaves the machine to the person using it.** A run puts itself below the priority of a person's own work as it starts, and each process a test starts takes that priority from it, so the system serves what the person is using first. The design script's run keeps the processes of tests it runs at once under half the machine's memory and half its processors, read from the machine as the run starts. It counts each process at the most a process holding the search's model takes, not at what a process takes as it starts, since the model is loaded later. It hands each process it starts the number of threads the search's model may work on, that process's share of the half, and the search builds its model on that number. A search run by hand, handed none, works on half the machine's processors. So a run made while a person works slows itself and not the person.

**A run runs every test.** No test is marked to be left out of a run, and no run of the design script leaves one out for the time it takes. A person choosing fewer names them, by pytest's own ways. So a test a change breaks is found by the run that follows the change, whichever test it is.

**A run writes only within its one folder among the working files.** [`specs/methodology/working-files/main.md § The Working Files`](/specs/methodology/working-files/main.md#the-working-files) names the folder. What a test builds, the runner's temporary folders and the run's report all stand there. A run compiles no module to a file, the tests' or the scripts', and keeps no cache of the runner's. No test and no setting of the runner names a place to write outside the folder.

**One clean-up runs before and after.** It runs by the runner's own hooks: over a test's folder before the test starts and after it ends, and over the run's folder before the run starts and after it ends. Both are needed, since a test may fail and a run may be cut off. What either left is cleared as the next starts. After a run the folder holds the run's report alone.

**A run a test starts keeps to a folder of its own.** It writes within a folder inside the folder of the run that started it, and its clean-up clears that folder alone. So a test may make a run that passes, one that fails and one cut off, and read what each left.

**A run's report is `report.xml` in the run's folder.** It holds to the schema of the JUnit XML report ([`specs/methodology/external-references.md § External References [Name: JUnit XML]`](/specs/methodology/external-references.md#external-references)). Each result the design script gives of a run is read from the report, never from the words a run prints: the tests run, each test that failed with what it reported, and each test's time. A run leaving no report, or one out of the schema, is a run of tests that could not be run.

#### When the Kept Tests Are Run

**A script's kept tests are run whenever a change holds one of its files.** The design script's `--check-kept-tests` runs them. For this, a script's files are its code, each file of the canon it reads a form from, its set of kept tests with the runner's settings and `conftest.py`, and each fixture file its tests read a fixture from. Given a set of changed files, the action runs the kept tests of each script whose files they hold and no others, each file of tests as a process of its own, and each kept comparison whose script's files they hold. It gives what the report holds of the run and says where the report stands. It fails where a test fails or cannot be run, and never for what a comparison lists. The design script runs the tests itself, so no builder records a run in place of one.

**Checks are made with each run.** With a script's kept tests the action checks what those tests hold: each action the script states, each Script Check it carries out and each check of a skill's table it carries out is held by a test where it passes and by one where it reports, and no test names an action, a Script Check or a section its script does not hold ([`§ Authoring a Skill § Script Checks [Name: each-script-check-and-action-held-by-a-test]`](#script-checks)). An action that checks reports where it finds what it checks for. An action that shows reports where it refuses what it is given, or shows the other of the states it tells apart, as a search shows that it gives no place. So what is held does not come to be unheld. Of a script holding no kept tests a run reports nothing, and such a script joins as it gains its first kept test. A changed script that no set of kept tests names holds none, and the action says so. The design script's `--show-test-coverage` shows the same for every script of the skills when asked, a script holding no kept tests among them, and fails nothing.

**The tests' folder is checked as a whole.** A change holding any file under `tests/spec-of-record/` runs the checks of the folder, whether or not it runs a test, and so does each run of the kept tests the design script makes. Each is a Script Check: that no file there carries the name of an agent instructions file ([`§ Authoring a Skill § Script Checks [Name: no-instructions-name-kept-under-the-tests]`](#script-checks)), that the fixtures' index lists its folder ([`§ Authoring a Skill § Script Checks [Name: fixtures-index-lists-its-folder]`](#script-checks)), that each fixture file holds fixtures in their form ([`§ Authoring a Skill § Script Checks [Name: fixture-file-holds-fixtures-in-their-form]`](#script-checks)), that each fixture is read by a kept test ([`§ Authoring a Skill § Script Checks [Name: each-fixture-read-by-a-kept-test]`](#script-checks)), and that no comment or docstring of the kept tests' code names the canon outside a spec annotation ([`specs/methodology/sourcing-and-citation/writing-a-citation.md § Writing a Citation § Citing From Code § Script Checks [Name: canon-named-only-in-an-annotation]`](/specs/methodology/sourcing-and-citation/writing-a-citation.md#script-checks)).

**In a design and outside one.** In a design, `--stamp-settled-report` runs the action over the design's changes as it validates the report of a self-review over applied work, and stamps no such report where a test fails or cannot be run or a check made with the run reports, and appending the report's entry runs none, as [`§ Authoring a Skill § Script Checks [Name: kept-tests-pass-at-the-self-review]`](#script-checks) has it. Outside a design, a direct edit of one of a script's files runs it before the user approves the edit, as [`specs/AGENTS.md § Design, Refactor, Refine § Direct Edits`](/specs/AGENTS.md#direct-edits) has a direct edit made. A change to a script changes its kept tests with it: a new action, a new Script Check or a new check of a skill's table takes a test where it passes and one where it reports in the same change.

### Script Checks

**Records:**
  - **Name:** script-check-carried-out \
    **Tests:** each Script Check record standing in the specs, a record in a fenced block aside, is cited by a canon-spec annotation in the scripts of a skill its Carried Out By names, or in the code the skills share, as a unit carrying out a check cites its record \
    **Reads:**
      - `canon-specs`

    **Carried Out By:**
      - `.ai/skills/audit-specs/` `--check-scope`

  - **Name:** kept-tests-pass-at-the-self-review \
    **Tests:** as the report of a self-review over applied work is validated, a pass's among them, the kept tests pass of each script any of whose files the design's changes hold, a script's files being those [`§ Authoring a Skill § Kept Tests § When the Kept Tests Are Run`](#when-the-kept-tests-are-run) names, each check made with a run of the kept tests reports nothing, the checks of the tests' folder among them where those changes hold a file under the tests, and the comparison has run where those changes hold a file of the design script, each run by the design script itself and its result written into the report's Script Output, as [`§ Authoring a Skill`](#authoring-a-skill) has a script's kept tests run whenever a design's changes hold one of its files: `--stamp-settled-report` stamps no such report where a test fails or cannot be run or such a check reports, and appending the report's entry runs none \
    **Reads:**
      - `canon-specs`
      - `fixture-files`
      - `other`
      - `working-files`

    **Carried Out By:**
      - `.ai/skills/design-specs/` `--stamp-settled-report`
      - `.ai/skills/implement-specs/` `--stamp-settled-report`

  - **Name:** each-script-check-and-action-held-by-a-test \
    **Tests:** each unit carrying out a check, read by the citation its canon-spec annotation holds, a Script Check's record or the section a skill's table enforces, is held where it passes and where it reports by kept tests citing the same place, in each set whose script carries the check out: each set whose script files hold the entry script of a skill the record's Carried Out By names, or of the skill whose table enforces the section, and no set whose script does not carry it out; each action a script holding kept tests states is held the same two ways by tests marked with it, a test calling the unit carrying the action out among them; a script holding kept tests states its actions in the form [`§ Authoring a Skill`](#authoring-a-skill) gives, and no kept test names a Script Check, a section or an action its script does not hold, a test's citing never counting as a unit's that carries the check out \
    **Reads:**
      - `canon-specs`

    **Carried Out By:**
      - `.ai/skills/design-specs/` `--check-kept-tests`
      - `.ai/skills/implement-specs/` `--check-kept-tests`

  - **Name:** no-instructions-name-kept-under-the-tests \
    **Tests:** no file kept under the kept tests' folder carries the name of an agent instructions file, `AGENTS.md`, as [`specs/methodology/external-references.md § External References [Name: AGENTS.md]`](/specs/methodology/external-references.md#external-references) gives it \
    **Reads:**
      - `canon-specs`
      - `fixture-files`

    **Carried Out By:**
      - `.ai/skills/design-specs/` `--check-kept-tests`
      - `.ai/skills/implement-specs/` `--check-kept-tests`

  - **Name:** fixtures-index-lists-its-folder \
    **Tests:** the index of the kept tests' fixture files lists each file standing in the fixtures' folder, and each file it lists stands there \
    **Reads:**
      - `fixture-files`

    **Carried Out By:**
      - `.ai/skills/design-specs/` `--check-kept-tests`
      - `.ai/skills/implement-specs/` `--check-kept-tests`

  - **Name:** fixture-file-holds-fixtures-in-their-form \
    **Tests:** each file standing in the kept tests' fixtures folder is the folder's index or a Markdown file holding fixtures and no other text, and each fixture holds its key, what it holds and its snippet in a fenced block naming its language, as the Fixture record type has a fixture \
    **Reads:**
      - `fixture-files`

    **Carried Out By:**
      - `.ai/skills/design-specs/` `--check-kept-tests`
      - `.ai/skills/implement-specs/` `--check-kept-tests`

  - **Name:** each-fixture-read-by-a-kept-test \
    **Tests:** each fixture of a script's kept tests is read by a kept test of that script, as the registered runner gives which test takes which fixture \
    **Reads:**
      - `canon-specs`
      - `fixture-files`

    **Carried Out By:**
      - `.ai/skills/design-specs/` `--check-kept-tests`
      - `.ai/skills/implement-specs/` `--check-kept-tests`

  - **Name:** kept-test-results-read-from-the-report \
    **Tests:** each result the design script gives of a run of the kept tests is read from the run's report, which holds to the registered schema of the report, and a run leaving no report, or one out of that schema, is reported as a kept file that cannot be run \
    **Reads:**
      - `canon-specs`
      - `working-files`

    **Carried Out By:**
      - `.ai/skills/design-specs/` `--check-kept-tests`
      - `.ai/skills/implement-specs/` `--check-kept-tests`
