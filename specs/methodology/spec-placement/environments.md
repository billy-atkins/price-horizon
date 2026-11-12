## Environments

The technical specs hold one environments document, `environments.md`, at their root beside the stack document, laid out as a folder named for it where it holds more than one file unit ([`specs/methodology/spec-placement/where-a-file-goes.md § Where a File Goes`](/specs/methodology/spec-placement/where-a-file-goes.md#where-a-file-goes)). It has a section for each environment the system is built, tested or run in, titled with the name the project gives that environment. An environment states only what differs from the stack ([`specs/methodology/spec-placement/technical-stack.md § The Technical Stack`](/specs/methodology/spec-placement/technical-stack.md#the-technical-stack)). So the stack stays the home of each technology every environment uses, and of each version, and no environment restates them. An environment holds no secret value, credential or host name. At most, it names the vault or configuration they come from.

Each environment's section opens with a required `**Kind:**` field ([`specs/methodology/modeling-constructs.md § Fields`](/specs/methodology/modeling-constructs.md#fields)), whose value is one of a closed set, so what this section asks of an environment follows from its role, never from its name:

**Construct:** `specs/methodology/modeling-constructs.md § Constructs § Decision Table` \
**Conditions:** Kind \
**Annotations:** Holds

| Kind | What it owes | Holds |
|---|---|---|
| local | it names each operating system its developers may use, and the project supports only those; it has tools, a build task, a lint task, and a test task for every kind of test the project has, its acceptance tests among them | developers' own machines or a development container, where code is written |
| integration | it runs every build, lint and test task of the local environment, naming the operating systems it runs them on; a local operating system it does not run them on is supported as stated, not as shown | continuous integration |
| shared | nothing beyond every environment's own sections | a deployed environment people or tests use, development, quality assurance, staging or a hotfix environment, say |
| production | where a product spec specifies the production environment, a customer's own installation, say, it cites that spec and adds only what the stack and that spec leave open | the environment serving real users |

Exactly one environment is local.

After its Kind, each environment's section gives, as bold lead-ins ([`specs/methodology/spec-style/markdown.md § Bold Lead-ins`](/specs/methodology/spec-style/markdown.md#bold-lead-ins)) in this order:
- what it is for and who uses it;
- where it runs;
- what differs from the stack: each technology the environment uses in place of, or beside, one the stack names, with its purpose;
- what data it holds.

Then, where it has any, comes a table of the tools it needs. The table is headed Tool, Version and Purpose, and has one column for each operating system the environment names, saying how the tool is installed there. A tool's Version is given only where the stack does not name the tool. A tool the stack names takes the stack's version.

Then, where it has any, comes a table of its tasks. The table is headed Task, Command and Does, and Runs On where any task needs it. Each command is run from the project root. A task runs on every operating system the environment names, unless its Runs On names the ones it runs on. A task whose command differs between operating systems takes a row for each. A command may take an argument, written in angle brackets, and Does says how to fill it. Each test task has a targeted form, which takes an argument selecting the tests to run.

As it works, the agent writing code runs the targeted form of a test task on the tests citing the specs its work carries out ([`specs/methodology/code.md § Tests`](/specs/methodology/code.md#tests)). Before its work is checked, the agent runs every build, lint and test task of the local environment, so a task that no longer works is found as soon as code is written. A project whose specs give no local environment, or whose local environment lacks any of these tasks, has code an agent cannot check. That is a gap in the specs, and the agent presents it rather than writing code around it.
