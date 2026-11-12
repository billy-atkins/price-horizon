## Agent Agnostic

The instructions in Spec of Record's scope, both `AGENTS.md` files and each registered skill, stay agnostic of which agent reads them. They use no vendor-specific instruction filename and no tool-specific directory, and they assume nothing about which model, CLI, or editor is running.

**The test.** Would anything new still make sense to an agent from a different vendor, or to a person reading it directly?

**The one exception.** Anything written for one tool is allowed, and only because it carries no content:
- an opt-in helper outside the methodology's scope, named for the tool it serves, may wire that tool up to the agnostic content;
- an agent setting itself up may write what it needs to carry out a choice the methodology leaves to it ([`specs/methodology/skills/setting-up-an-agent.md § Setting Up an Agent`](/specs/methodology/skills/setting-up-an-agent.md#setting-up-an-agent)).

Whatever either writes is kept out of version control and outside the scope. Nothing depends on its having been written. A skill stays readable directly, and what was written only saves a step, or applies a choice, for someone using that tool.
