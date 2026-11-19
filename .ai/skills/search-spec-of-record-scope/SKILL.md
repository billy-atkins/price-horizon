---
name: search-spec-of-record-scope
description: Search the files of Spec of Record's scope and the code for where something is. Use when you need every place citing a section, a keyed part or a file, before retitling or moving it; the exact lines a citation names; every use of a term, a phrase or an identifier in whatever form it takes; the units of code that define, call, construct, extend or implement a name, or carry an annotation; the places saying the same thing as a passage in other words, when checking whether a fact already has a home or a rule is stated twice; or every place a fault of form stands. Use it before writing a regular expression of your own, which matches a mention as readily as a citation and finds no passage worded differently.
---

# Searching Spec of Record's scope

A change to a fact reaches every place citing it, and `specs/methodology/sourcing-and-citation/one-home-per-fact.md § One Home Per Fact` has a fact live in one home with every other place citing that home. So most of what a change reaches is found by asking who cites a place. This skill answers that question, and the others its kinds of search give, from an index of the files, by its script. It decides nothing: every answer is a list of places to read.

Two rules send an agent here. A heading retitled or moved takes every citation of it along (`specs/methodology/sourcing-and-citation/titling-a-heading.md § Titling a Heading`), and the places citing it are the search's to list. A change's zoom-out reaches every passage citing what it changes, and every passage still stating what it replaced (`specs/AGENTS.md § Design, Refactor, Refine § Measure Twice, Cut Once § The Zoom-Out`). The search lists the first, and ranks candidates for the second.

The search covers the files in Spec of Record's scope, the working files aside. The scope names those files by kind (`specs/methodology/scope/what-spec-of-record-governs.md § What Spec of Record Governs`). The code among them is each code root the stack names, less the paths it excludes (`specs/methodology/spec-placement/technical-stack.md § The Technical Stack`). The search reads no version control, so a file not yet committed is searched like any other.

The search's code is `.ai/skills/lib/search.py`, shared code, so another skill's script calls it directly. This skill's script runs it for an agent.

## Workflow

**Choose the kind of search.** The kinds of search, each an action of the script:

**Reference Key:** Kind \
**Required:** Action, Gives, Its Places Are

| Kind | Action | Gives | Its Places Are |
|---|---|---|---|
| citers | `--show-citers` | every place citing a section, a keyed part or a file | every place |
| lines | `--show-lines` | the lines a citation names | every place |
| terms | `--show-term-uses` | every use of a word, a phrase or an identifier | every place |
| code structure | `--show-code-structure` | every unit of code holding a structure, for a name | every place the syntax shows |
| meaning | `--show-similar-passages` | the places saying the same as a passage, or as a cited section, in other words | the first of a ranking |
| pattern | `--show-pattern-matches` | every place a regular expression matches | every place |

Use `--show-pattern-matches` for a fault of form alone, such as a doubled space or a citation broken across lines. A regular expression matches every mention of its words and cannot tell a citation of a section from a mention of its title, so a term, a citer and a structure each have a search of their own.

**Run the script from the project's root.** Give the citation, the term, the passage or the expression in quotes:

```text
python <skill-dir>/scripts/search-spec-of-record-scope.py --show-citers "specs/methodology/code.md § Citing the Specs From Code"
python <skill-dir>/scripts/search-spec-of-record-scope.py --show-lines "specs/AGENTS.md § Writing specs"
python <skill-dir>/scripts/search-spec-of-record-scope.py --show-term-uses "design frame"
python <skill-dir>/scripts/search-spec-of-record-scope.py --show-code-structure calls parse_citation
python <skill-dir>/scripts/search-spec-of-record-scope.py --show-similar-passages "A fact lives in one home, and every other place cites it."
python <skill-dir>/scripts/search-spec-of-record-scope.py --show-pattern-matches "§  +"
python <skill-dir>/scripts/search-spec-of-record-scope.py --show-term-uses "design frame" --paths specs/methodology .ai/skills
```

`--paths` takes files and folders, and the search then answers over those alone. A citation is given as `specs/methodology/sourcing-and-citation/writing-a-citation.md § Writing a Citation` writes one for a place in another file, without its backticks, and loose white space in it is squeezed. A structure is one of `defines`, `calls`, `constructs`, `extends`, `implements`, `references` and `annotated-with`.

**Read the result's file, then read the places.** The script prints the file's name, the count of its places and whether they are every place or the first of a ranking. It prints the places too where they are few. The file holds all of them, in the form `§ Search Result` states. A place is a place to read and never a finding. A ranked result is never every place: a place it leaves out may still say the same thing.

**Read what the result says of its places.** Its Notes tell apart the places that only relate to what you asked: a place citing a section within it, a section above it, a part of it or its file. They mark a citation standing in a fenced block, a `technical-specs` entry, which is a label and no citation (`specs/methodology/spec-placement/naming-the-technical-files-behind-a-capability.md § Naming the Technical Files Behind a Capability`), and an annotation with the unit of code it stands over. They name each file of code no structure was searched in.

**Record a search where another rule sets its form.** A search made for a design's check or its research is recorded as `specs/methodology/working-files/main.md § A Check's Report § Search` has it. That rule governs the record, and this skill's result is no part of a report.

## What the search requires

Every search first checks everything the search requires, whichever kind was asked for, and stops where any is missing, as `specs/methodology/skills/authoring-a-skill.md § Authoring a Skill` has a script stop where no other path gives the same answer. It then names each thing missing, why the search needs it and the command installing it. `--check-requirements` lists them at any time.

A search by meaning compares passages by what they say. A small language model, run on this machine, turns each passage into a vector, a list of numbers, and two passages saying the same thing get vectors that lie close together. So the search needs that model's files, a Python package to run the model, and one to find the vectors nearest a passage's. It also needs a parser for each language of code it reads as code. `--install-model` downloads the model's files into this skill's scratch space. It is the one action that reaches the network. No search sends text off the machine or downloads anything.

## Where its output goes

The index, the model's files and the results sit in `.ai/tmp/search-spec-of-record-scope/`, this skill's scratch space, as `specs/methodology/working-files/main.md § The Working Files` gives a skill one. The first use builds the whole index and says how long it took. Each later run reads only the files that changed. Deleting the index loses nothing but the time to build it.

Results go to `results/` in that folder. A run that finds a file changed clears every result in that folder before it answers, since each answered for files that no longer stand so. The search knows nothing of who asked. A caller that wants to keep a result moves its file to a folder of its own before the files change, and the file's name still says what its content must be.

## Search Result

What a search gave, written by the script as one file, the same form whoever asked. A result's file holds one record of this type, in its `**Records:**`:

**Construct:** `specs/methodology/modeling-constructs.md § Constructs § Record Form` \
**Plural Name:** Search Results \
**Reference Key:** Result

| Field | Unique | Required | Default Value | Values | Holds |
|---|---|---|---|---|---|
| Result | yes | yes | | text | the file's name, built from the kind of search, what was asked and the file's content |
| Kind | no | yes | | "citers", "lines", "terms", "code structure", "meaning", "pattern" | the kind of search |
| Query | no | yes | | text | what was asked |
| Narrowed To | no | no | the whole | text | a list, the paths the search was narrowed to |
| Run As | no | yes | | text | what the script ran for the Query, `as asked` where it added nothing |
| Completeness | no | yes | | "complete", "ranked" | whether the Places are every place of the Kind or the first of a ranking |
| Places | no | yes | | text | a list, the places to read, each a citation of the section or the file holding it with its lines; `none` where it found nothing |
| Notes | no | no | none | text | a list, an item to each place the script says more of |

A result's name ends with a hash of its content, so a file whose content was changed no longer gives the hash in its name. The script's `--check-result` checks a result's file against this form and its name against its content.

## What went wrong before this skill

**A regular expression found mentions, not citers.** A pattern built from a section's title matched every sentence using those words. Telling the citations apart meant reading each match.

**A pattern's syntax changed its meaning.** A search for the canon's literal `Bloat?` made its `t` optional and matched other words. A term given to `--show-term-uses` is never read as an expression.

**A term was missed in another form.** A search for `append entry` found neither `append_entry` nor `AppendEntry`, and a search for a term missed its plural and the abbreviation the glossary gives it.

**A rule stated twice was found only by luck.** A trial over eleven files found a copy only where the reader happened to hold both passages or thought of a word they share. `--show-similar-passages` ranks passages by what they say.

**The scripts read a file in ways that disagree.** One reader of a fenced block missed a tilde fence and a fence nested in a longer one, and two readers of a heading path standing twice chose different headings. The search reads a file by one reading, as `specs/methodology/spec-style/markdown.md § Markdown` has it read. Of two headings sharing a path it takes the first, and its result says the path stands twice.

**A search that carried on without what it needed looked whole.** An answer from a lesser method holds fewer places and nothing saying so. The search stops instead.
