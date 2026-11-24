---
name: search-spec-of-record-scope
description: Search the files of Spec of Record's scope and the code for where something is. Use when you need every place citing a section, a keyed part or a file, before retitling or moving it; every cited section with the places citing it; the exact lines a citation names; every use of a term, a phrase or an identifier in whatever form it takes; the units of code that define, call, construct, extend or implement a name, or carry an annotation; the places saying the same thing as a passage in other words, when checking whether a fact already has a home or a rule is stated twice; or every place a flaw in formatting or structure stands. It answers over the durable files as they stand, as a commit held them, or over working files you name. Use it before writing a regular expression of your own, which matches a mention as readily as a citation and finds no passage worded differently.
---

# Searching Spec of Record's scope

A change to a fact reaches every place citing it, and `specs/methodology/sourcing-and-citation/one-home-per-fact.md § One Home Per Fact` has a fact live in one home with every other place citing that home. So most of what a change reaches is found by asking who cites a place. This skill answers that question, and the others its kinds of search give, from an index of the files, by its script. It decides nothing: every answer is a list of places to read.

Two rules send an agent here. A heading whose title changes has every citation naming it updated in the same edit (`specs/methodology/sourcing-and-citation/titling-a-heading.md § Titling a Heading`), and the search lists the places citing it. A change's zoom-out reaches every passage citing what it changes, and every passage still stating what it replaced (`specs/AGENTS.md § Design, Refactor, Refine § Measure Twice, Cut Once § The Zoom-Out`). The search lists the citing passages, and ranks candidates for the passages still stating what was replaced.

The search's code is `.ai/skills/lib/search.py`, shared code, so another skill's script calls it directly. This skill's script runs it for an agent. The search knows nothing of who asked. It leaves out no place for the section or the table the place stands in. Each place says where it stands, and a caller leaves out what it does not want. A search by meaning ranks only part of what a file holds, and sets some places apart when asked by a citation. `§ Workflow` and `§ What a search by meaning does not find` state both.

## Workflow

**Choose the kind of search.** The kinds of search, each an action of the script:

**Reference Key:** Kind \
**Required:** Action, Gives, Its Places Are

| Kind | Action | Gives | Its Places Are |
|---|---|---|---|
| citers | `--show-citers` | every place citing a section, a keyed part or a file | every place |
| cited sections | `--show-cited-sections` | each section, keyed part and file cited, with every place citing it | every place |
| lines | `--show-lines` | the lines a citation names | every place |
| terms | `--show-term-uses` | every use of a word, a phrase or an identifier | every place |
| code structure | `--show-code-structure` | every unit of code holding a structure, for a name | every place the syntax shows |
| meaning | `--show-similar-passages` | the places saying the same as a passage, or as a cited section, in other words | the part of a ranking asked for, its first twenty places where none is |
| pattern | `--show-pattern-matches` | every place a regular expression matches | every place |

Use `--show-pattern-matches` for a flaw in formatting or structure alone, such as a doubled space or a citation broken across lines. A regular expression matches every mention of its words and cannot tell a citation of a section from a mention of its title, so a term, a citer and a structure each have a search of their own.

A search by terms finds a phrase where its words stand together in their order, each in whatever form it takes. It does not find them where other words stand between: asked for `run again`, it gives "is run again" and "runs again", and not "runs each Search again". Ask for the fewest words that must stand together, or ask a search by meaning.

**Choose the files to answer over.** A search answers over one target, named with `--target`, and its result holds places of that target alone:

**Reference Key:** Target \
**Required:** Covers

| Target | Covers |
|---|---|
| `current-durable-files` | the durable files (`specs/methodology/glossary/glossary.md`) as they stand, a file not yet committed among them; the target of a search naming none |
| `committed-durable-files` | the durable files as a commit of the project's version control held them: the last commit, or the one `--commit` names |
| `working-files` | the working files (`specs/methodology/working-files/main.md § The Working Files`) under the paths `--paths` names |

The search takes the durable files by the kinds of file Spec of Record's scope names (`specs/methodology/scope/what-spec-of-record-governs.md § What Spec of Record Governs`). It takes the code among them as each code root the stack names, less the paths the stack excludes (`specs/methodology/spec-placement/technical-stack.md § The Technical Stack`). A search of the committed files takes the scope's kinds and the stack's code roots as the commit held them.

A search of the working files answers over the paths it is given and is refused where it is given none. It takes a path only where the working files sit, as `specs/methodology/working-files/main.md § The Working Files` names those places, and it never reads its own scratch space. So a caller bound in what it may read, as a reviewer is (`specs/AGENTS.md § Design, Refactor, Refine § Who Checks What and Why § What a Review Reads`), names the working files it may read and is given no place outside them.

**Choose the target a design's work asks of.** As `specs/methodology/working-files/main.md § A Check's Report § Search` sets it, a search made in a design's work asks of `current-durable-files` for the files the design works from, and of `committed-durable-files` for the state before a design's work and for every search of the durable files made while that design's uncommitted changes are kept, naming no commit. Name a commit with `--commit` only to ask of that one commit, as a reviewer reading the baseline of a Refactor and Refine cycle does. A search of `committed-durable-files` naming none asks of the last commit, whichever that is when it is asked. No check holds a recorder to the target it asks.

**Run the script from the project's root.** Give the citation, the term, the passage or the expression in quotes:

```text
python <skill-dir>/scripts/search-spec-of-record-scope.py --show-citers "specs/methodology/code.md § Citing the Specs From Code"
python <skill-dir>/scripts/search-spec-of-record-scope.py --show-cited-sections --paths specs/methodology/skills
python <skill-dir>/scripts/search-spec-of-record-scope.py --show-lines "specs/AGENTS.md § Writing specs"
python <skill-dir>/scripts/search-spec-of-record-scope.py --show-term-uses "design frame"
python <skill-dir>/scripts/search-spec-of-record-scope.py --show-code-structure calls parse_citation
python <skill-dir>/scripts/search-spec-of-record-scope.py --show-similar-passages "A fact lives in one home, and every other place cites it."
python <skill-dir>/scripts/search-spec-of-record-scope.py --show-similar-passages "A fact lives in one home, and every other place cites it." --limit 40 --start 21
python <skill-dir>/scripts/search-spec-of-record-scope.py --show-pattern-matches "§  +"
python <skill-dir>/scripts/search-spec-of-record-scope.py --show-term-uses "design frame" --paths specs/methodology .ai/skills
python <skill-dir>/scripts/search-spec-of-record-scope.py --show-term-uses "design frame" --target committed-durable-files
python <skill-dir>/scripts/search-spec-of-record-scope.py --show-term-uses "design frame" --target working-files --paths .ai/plans/design-specs
python <skill-dir>/scripts/search-spec-of-record-scope.py --show-snapshot-code --target committed-durable-files
```

`--paths` takes files and folders, and the search then answers over those alone. A citation is given as `specs/methodology/sourcing-and-citation/writing-a-citation.md § Writing a Citation` writes one for a place in another file, without its backticks, and loose white space in it is squeezed. A structure is one of `defines`, `calls`, `constructs`, `extends`, `implements`, `references` and `annotated-with`.

**Read the result's file, then read the places.** The script prints the file's name, the count of its places and whether they are every place or a part of a ranking. It prints the places too where they are few. The file holds all of them, in the form `§ Search Result` states. A place is a place to read and never a finding.

**Read which state of the files a result answered for.** Every result holds a snapshot code (`specs/methodology/glossary/glossary.md`) in its Snapshot: one code for the state of the files of its target, built from what each file holds. It stands for the whole target whatever paths the search was narrowed to, and for the paths named where the target is the working files. It is built one way whatever the target, so the files a commit held and the files as they stand take one code where each file holds the same. Two results holding one code answered for the same files. `--show-snapshot-code` gives the present code of a target, read fresh from its files, with `--target`, `--commit` and `--paths` as a search takes them: it equals a result's code while no file of the target holds anything new, and differs once one does. A file whose time of change alone moved leaves the code as it was. What a changed code means is its caller's to decide. A code does not show everything. A file whose content changed while its size and its time of change did not is not read again, so the code repeats what the index holds, as every answer does. The code of a search of the working files stands for the paths it names alone, never for the durable files that search reads its places against. A result of the committed files holds a Commit only where its asker named one with `--commit`. Where its asker named none, it holds the commit it read as its Last Commit, so a record copied from a result names a commit only where one was asked for.

**Read where a question named nothing.** The search tells its caller where a question names nothing to ask of, each case apart: a citation that names no place among the files it reads, a term or a passage that reduces to no word, and a path it is narrowed to under which no file of its target stands. Its answer stands as it otherwise would, no place given for what names nothing. The result's Notes say which case and of what, the script prints a line for each, and a script calling the search reads them from the result it is given.

**Read where each place stands.** Each place is written in the form `§ A Place` states: a citation with its lines, and what its lines stand in. A caller that wants no place of a given section, none beneath it, or none in a table, tells them by this and leaves them out itself.

**Read more of a ranking where you need it.** A search by meaning ranks each sentence as well as each passage, and gives the passage a sentence stands in. It gives a part of a ranking and never every place: a place it leaves out may still say the same thing. `--limit` says how many places it gives and `--start` the place of the ranking it gives them from, twenty from the start of the ranking where neither is given. Parts asked one after another make up the one ranking, no place twice and none missed, while the files stand as they do. A caller that will leave places out asks for more, and a caller that has read a part asks for the part after it.

**Know what a search by meaning does when asked by a citation.** Given a section's citation in place of a passage, it gives others and not the one it was given. The ranking holds neither that section nor a place whose section cites it. The places citing it are listed apart in the Notes, whole and the same with every part, since each may rely on the section and not restate it. Given a passage, the search sets no place apart.

**Read what the result says of its places.** Its Notes say more of a place than its citation does:
- a place that only relates to what was asked: a place citing a section within it, a section above it, a part of it or its file;
- a `technical-specs` entry, which is a label and no citation (`specs/methodology/spec-placement/naming-the-technical-files-behind-a-capability.md § Naming the Technical Files Behind a Capability`);
- an annotation, with the unit of code it stands over;
- a heading path that stands more than once in its file, with how many times and at which lines;
- each file of code no structure was searched in.

Headings sharing a parent may not share a title (`specs/methodology/sourcing-and-citation/titling-a-heading.md § Titling a Heading`). Where a file breaks that rule, the search still reads what each heading of the shared path holds. A citation of the path names what those headings hold together, and a place under any of them is cited by the path with its own lines. Read each section the note names.

**Record a search where another rule sets its form.** A search made for a design's check or its research is recorded as `specs/methodology/working-files/main.md § A Check's Report § Search` has it. That rule governs the record, and this skill's result is no part of a report.

## What the search requires

Every search first checks everything the search requires, whichever kind was asked for, and stops where any is missing, as `specs/methodology/skills/authoring-a-skill.md § Authoring a Skill` has a script stop where no other path gives the same answer. It then names each thing missing, why the search needs it and the command installing it. `--check-requirements` lists them at any time.

A search by meaning compares passages by what they say. A small language model, run on this machine, turns each passage and each sentence into a vector, a list of numbers, and passages saying the same thing get vectors that lie close together. So the search needs that model's files, a Python package to run the model, and one to find the vectors nearest a passage's. It also needs a parser for each language of code it reads as code. `--install-model` downloads the model's files to where `§ Where its output goes` has them sit, so they are set up once on the machine and every checkout of the project finds them. It is the one action that reaches the network. No search sends text off the machine or downloads anything.

A search of the committed files requires one thing more, the project's version control, and no other search asks it anything. What becomes of a search of the committed files is decided before it writes anything:

**Construct:** `specs/methodology/modeling-constructs.md § Constructs § Decision Table` \
**Hit Policy:** First \
**Conditions:** Under version control the search reads?, Its tool installed?, The tool answers with a failure?

| Under version control the search reads? | Its tool installed? | The tool answers with a failure? | The search |
|---|---|---|---|
| false | - | - | stops, saying the project is under no version control it reads |
| - | false | - | stops, saying the tool is not installed |
| - | - | true | stops, giving what it asked and the tool's own words |
| - | - | - | answers |

A search of the durable files as they stand, or of the working files, answers the same whatever these conditions hold.

## Where its output goes

A search answers over the checkout it is run in: the nearest folder at or above the working directory that holds this skill, whichever checkout holds the script being run. So the same files give the same answer in any checkout, a worktree kept beneath another checkout's working files among them.

The index and the results sit in `.ai/tmp/search-spec-of-record-scope/`, this skill's scratch space, in that checkout, as `specs/methodology/working-files/main.md § The Working Files` gives a skill one. The first use in a checkout builds the whole index, which takes minutes, and says how long it took. Each later run reads only the files that changed. The index keeps each target's files apart, and holds one commit's files at a time. Deleting the index loses nothing but the time to build it.

The model's files sit in `.ai/tmp/search-spec-of-record-scope/model/` of the project's main checkout, the one holding the repository that every other checkout of the project shares. A worktree finds the main checkout from its own files, wherever it sits, and a project under no version control is its own main checkout. So the model is the same one for every checkout of the project.

Results go to `results/` in the scratch space of the checkout the search is run in. A result's name holds as many of the words asked as fit. Its file's whole path stays within 259 characters, the longest path every system opens, so a checkout standing deep among folders shortens a name and never makes a result too long to open. Each part of a ranking is a result of its own. A run that finds a file changed clears every result in that folder before it answers, since each answered for files that no longer stand so. A caller that wants to keep a result moves its file to a folder of its own before the files change, and the file's name still says what its content must be.

The search keeps each answer it computes of a kind whose answer rests on the files of its Target alone, with its index. It keeps it under what was asked, the Kind, the Query, the Target, with the Commit, and the paths it was narrowed to, under the snapshot code of the files it answered over, and under a code of its own reading, built from what the search's own script and each module of the shared code it imports hold, with the form of its index and the name of its model. Asked the same again while each of those stands, it gives the answer it kept and computes nothing anew. Where any differs it computes anew. It keeps no answer of a search by meaning, which ranks over every content its index holds, so each part of a ranking is computed as it is asked, and none of a search of the code structure `constructs`, which reads the classes every content its index holds defines. An answer of a search of the working files is kept also under the snapshot code of the durable files as they stand. What the search keeps is its own: it is no result's file, a caller cannot move it, and nothing reads it but the search.

## A Place

What a search gives for each place, the same form in every kind of search: a citation, written as `specs/methodology/sourcing-and-citation/writing-a-citation.md § Writing a Citation` writes one, then its lines, as `line 12` or `lines 12-14`, then what its lines stand in.

### What a place cites

A place cites the narrowest thing that holds every line it gives:

**Construct:** `specs/methodology/modeling-constructs.md § Constructs § Decision Table` \
**Hit Policy:** First \
**Conditions:** Every line in one keyed part?, Every line in one section?

| Every line in one keyed part? | Every line in one section? | The place cites |
|---|---|---|
| true | - | that keyed part |
| - | true | the deepest section holding its lines |
| - | - | its file |

### What a place says its lines stand in

A place says what its lines stand in only where every line of it that is not blank stands in the same thing:

**Construct:** `specs/methodology/modeling-constructs.md § Constructs § Decision Table` \
**Conditions:** Its lines stand in \
**Input Values:**
  - Its lines stand in: "a table", "a heading", "a fenced block", "running text", "more than one of these"

| Its lines stand in | The place says |
|---|---|
| "a table" | `in a table` |
| "a heading" | `in a heading` |
| "a fenced block" | `in a fenced block` |
| "running text" | nothing |
| "more than one of these" | nothing |

## Search Result

What a search gave, written by the script as one file, the same form whoever asked. A result's file holds one record of this type, in its `**Records:**`:

**Construct:** `specs/methodology/modeling-constructs.md § Constructs § Record Form` \
**Plural Name:** Search Results \
**Reference Key:** Result

| Field | Unique | Required | Default Value | Values | Holds |
|---|---|---|---|---|---|
| Result | yes | yes | | text | the file's name, built from the kind of search, what was asked and the file's content |
| Kind | no | yes | | "citers", "cited sections", "lines", "terms", "code structure", "meaning", "pattern" | the kind of search |
| Query | no | yes | | text | what was asked |
| Target | no | yes | | "current-durable-files", "committed-durable-files", "working-files" | the files the search answered over |
| Commit | no | where its asker named one | | text | the commit its asker named to the search, by its full name, which a search of "committed-durable-files" alone can name |
| Last Commit | no | where the Target is "committed-durable-files" and its asker named no commit | | text | the last commit, whose files the search answered over, by its full name |
| Narrowed To | no | no | the whole | text | a list, the paths the search was narrowed to, which a search of the working files always holds |
| Snapshot | no | yes | | text | the snapshot code (`specs/methodology/glossary/glossary.md`) of the files of the Target as the search answered: one code for the whole Target whatever the search was narrowed to, and for the paths named where the Target is "working-files"; written as sixteen hexadecimal digits |
| Run As | no | yes | | text | what the script ran for the Query, `as asked` where it added nothing |
| Completeness | no | yes | | "complete", "ranked" | whether the Places are every place of the Kind or a part of a ranking |
| Ranking Part | no | where the Completeness is "ranked" | | text | the part of the ranking the Places are, by the numbers its places hold in the ranking, as `1 to 20`; `none` where the ranking holds no place there |
| Places | no | yes | | text | a list, the places to read, each in the form `§ A Place` states; in a result of the Kind "cited sections" each is a citing place followed by `cites` and the citation it cites, the list ordered by what is cited; `none` where it found nothing |
| Notes | no | no | none | text | a list, an item to each place the script says more of |

A result's name ends with a hash of its content, so a file whose content was changed no longer gives the hash in its name. The script's `--check-result` checks a result's file against this form, each place against the form of a place, and its name against its content.

## What a search by meaning does not find

A search by meaning is held to a set of known pairs of passages, kept with Spec of Record's tests. Each pair is an original and a copy, and a test with one expectation, judged on the twenty places a search gives where it is asked for no part: the copy is in the result, or it is not. Where the search does not meet what a pair says, the pair stays as a test of what the search does, and its kind of case is a limit stated here. Read on for yourself wherever one of these limits may hide what you are looking for.

**Text that is no prose.** A search by meaning ranks the prose of each section: its paragraphs, its list items and the rows of its tables. It ranks no line of a fenced block, a diagram's and an example's among them, no heading and no front matter. It ranks no passage and no sentence shorter than forty characters. A rule restated in a diagram's node or in a heading's words is not found.

**A restatement in other words.** A place that restates a rule with almost none of its original's words may not be found. `specs/methodology/scope/progressive-disclosure.md` says "and one word names one concept wherever the canon writes it". `specs/methodology/spec-style/clear-prose.md` says "A term is defined where it first appears and used the same way after it." Asked with the sentence of `progressive-disclosure.md`, the search does not give the sentence of `clear-prose.md`.

**A rule stated in general where the original states one case of it.** A place stating a rule for every case may not be found from a place stating it of one case among other things. `specs/methodology/scope/what-spec-of-record-governs.md` says of one directory "it has an `index.md`, and an `architecture.md` summarizing it". `specs/methodology/spec-placement/where-a-file-goes.md` says "Every directory gets an `index.md`." Asked with the sentence of `what-spec-of-record-governs.md`, the search does not give the sentence of `where-a-file-goes.md`.

**A clause of a sentence that says several things.** The search ranks a sentence and nothing smaller. A rule that is one clause of a long sentence, restated as one clause of another, may not be found. `specs/methodology/sourcing-and-citation/writing-a-citation.md` lists, in one sentence, an annotation "on a unit carrying out a check, citing the check's record" among other cases. `specs/methodology/skills/authoring-a-skill.md` says a unit "carries a canon-spec annotation citing the check's record, as narrow as the unit". Asked with the clause of `writing-a-citation.md`, the search does not give the clause of `authoring-a-skill.md`.

**A question in place of the rule's own words.** The search ranks the places worded as what it was asked is. Asked a question, it gives places that speak of the question's subject, and may not give the rule that answers it, which shares few of the question's words. Asked "Which state of the files does a search answer for?", it does not give the rule of `specs/methodology/working-files/main.md` that a reading made while a send-back's changes are kept "reads the files at the last commit wherever it would otherwise read the files as they stand". Asked with that rule in other words, it gives it. Ask with a sentence the rule you look for might say.

**A place beside the original, on the same subject.** A place in the original's own section, or in a section beneath it, that says something else of the same subject is given among the places a ranking opens with. In `specs/methodology/sourcing-and-citation/which-citations-are-allowed.md`, a search for "The table is the whole permission" gives "An application spec does not reach into the methodology", which stands in the same section. A caller that wants no such place leaves it out by its citation.

**A place that points at a rule without stating it.** A place naming what a rule decides, in the rule's own words, is given though it states nothing of what the rule decides. `specs/methodology/sourcing-and-citation/titling-a-heading.md` says "a paragraph that is, or needs to be, a citation's target is authored as a child heading instead". `specs/methodology/sourcing-and-citation/writing-a-citation.md` only "says when such content becomes a heading", and the search gives it.

## What went wrong before this skill

**A regular expression found mentions, not citers.** A pattern built from a section's title matched every sentence using those words. Telling the citations apart meant reading each match.

**A pattern's syntax changed its meaning.** A search for the canon's literal `Bloat?` made its `t` optional and matched other words. A term given to `--show-term-uses` is never read as an expression.

**A term was missed in another form.** A search for `append entry` found neither `append_entry` nor `AppendEntry`, and a search for a term missed its plural and the abbreviation the glossary gives it.

**A rule stated twice was found only by luck.** A trial over eleven files found a copy only where the reader happened to hold both passages or thought of a word they share. `--show-similar-passages` ranks passages by what they say.

**The scripts read a file in ways that disagree.** One reader of a fenced block missed a tilde fence and a fence nested in a longer one, another read an indented code block as a fence, and readers of a heading path standing more than once chose different headings. The search reads a file by the one reading every script takes, as `specs/methodology/skills/authoring-a-skill.md § Authoring a Skill` has it.

**A search that carried on without what it needed looked whole.** An answer from a lesser method holds fewer places and nothing saying so. The search stops instead.
