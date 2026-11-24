#!/usr/bin/env python3
"""The tests of the search in .ai/skills/lib/search.py, run over the scenarios in tests/spec-of-record/scenarios/search/.

  search-tests.py            every suite but the one on scale
  search-tests.py --scale    the suite on scale too, which copies the project's files ten times over and takes minutes

The tests take the project from the checkout they are run in: the nearest folder at or above the working directory
holding the search's code, whichever checkout holds this file, so a run in a worktree tests that worktree's search over
that worktree's scenarios. Each suite builds an index of its own under .ai/tmp/search-spec-of-record-scope/tests/ of
that checkout, cleared as the suite starts. A project a suite makes for itself, and the copies the suite on scale
makes, stand in a folder outside the checkout, so no path a test writes grows with the place the checkout sits in. A
suite prints each check it makes, and the run exits 1 where any failed. The scenarios hold faults on purpose: a doubled
space in a citation, a heading path standing twice, a heading inside a fenced block.
"""
import contextlib
import gc
import io
import json
import os
import re
import shutil
import stat
import subprocess
import sys
import tempfile
import time
from pathlib import Path

sys.dont_write_bytecode = True
# The files of the script these tests are of, the search: its code, and each file of the canon it reads a form from as
# it runs. A path ending in a slash names each file beneath it. The design script reads the two names from this file's
# text, and runs these tests where a set of changed files holds one of the files they name.
SCRIPT_FILES = (".ai/skills/lib/search.py", ".ai/skills/lib/reading.py", ".ai/skills/lib/spec_text.py", ".ai/skills/lib/code_checks.py",
                ".ai/skills/lib/constructs.py", ".ai/skills/search-spec-of-record-scope/scripts/")
FORM_FILES = ("specs/methodology/glossary/glossary.md", "specs/methodology/skills/registered-skills.md")
LIB = Path(".ai") / "skills" / "lib"
RUN_IN = Path.cwd().resolve()
# the checkout the tests are run in, or, run from outside every checkout, the one holding this file
PROJECT = next((p for p in (RUN_IN, *RUN_IN.parents) if (p / LIB / "search.py").is_file()), Path(__file__).resolve().parents[3])
SCENARIOS = PROJECT / "tests" / "spec-of-record" / "scenarios" / "search"
sys.path.insert(0, str(PROJECT / LIB))
import reading  # noqa: E402
import search  # noqa: E402

SCRATCH = PROJECT / search.SCRATCH / "tests"
FAILED = []


def check(name, holds, detail=""):
    print(("  pass  " if holds else "  FAIL  ") + name + ("" if holds or not detail else "\n        " + str(detail)))
    if not holds:
        FAILED.append(name)


def fresh(name):
    folder = SCRATCH / name
    if folder.exists():
        shutil.rmtree(folder)
    return folder


def files_under(root):
    return sorted(p.relative_to(root).as_posix() for p in root.rglob("*") if p.is_file())


def lines_of(places):
    """-> {(path, first line)} of a result's places."""
    return {(place.path, place.first) for place in places}


def line_holding(root, path, words):
    for n, line in enumerate((root / path).read_text(encoding="utf-8").split("\n"), 1):
        if words in line:
            return n
    raise AssertionError(f"{path} holds no line with: {words}")


def reading_suite():
    print("the one reading: where a line stands, a fenced block as a unit, a heading's path and a citation's form")
    tick, tilde = "`" * 3, "~" * 3
    text = "\n".join([
        "# Title", "", "## First", "", tilde + "text", "## Not A Heading", tick, "still inside", tilde, "",          # 1-10
        "- an item", "", "  " + tick + "markdown", "  ## Drafted", "  " + tick, "",                                      # 11-16
        tick * 2 + "outer", tick + "inner", "held", tick, tick * 2, "",                                                # 17-22
        "> " + tick + "mermaid", "> flowchart LR", ">   a --> b", "> " + tick, "",                                    # 23-27
        "    indented code", "", "| a | b |", "|---|---|", "",                                                        # 28-32
        "## Twice", "", "one", "", "## Twice", "", "two `specs/a.md § A § B [Country: Canada; Tax Year: 2025]` and", # 33-39
        "`§ Table [States.State: open]` with " + tick + "x" + tick + " inline", "",                                    # 40-41
    ])
    read, found, heads = reading.lines(text), reading.blocks(text), reading.headings(text)
    stands = lambda n: read[n - 1].stands_in
    check("a line in a tilde fence is fenced, a heading and a backtick fence written inside it among them",
          [stands(n) for n in range(5, 10)] == [reading.FENCED] * 5 and stands(10) == reading.TEXT, [stands(n) for n in range(5, 11)])
    check("a fence indented in a list item is a fence, and its block is dedented by the fence's indentation",
          stands(13) == reading.FENCED and found[1].word == "markdown" and found[1].content == "## Drafted" and found[1].before == "  ", (found[1].info, found[1].content, found[1].before))
    check("a fence nested in a longer one is content of the longer and no block of its own",
          found[2].info == "outer" and found[2].content == tick + "inner\nheld\n" + tick and (found[2].opens, found[2].closes) == (17, 21), (found[2].opens, found[2].closes, found[2].content))
    check("a block quoted in a note is a block, its quote prefix what stands before its fence and taken off its lines",
          found[3].word == "mermaid" and found[3].before == "> " and found[3].content == "flowchart LR\n  a --> b" and found[3].closed, (found[3].before, found[3].content))
    check("the blocks are those four, each with the lines of its fences", [(b.opens, b.closes) for b in found] == [(5, 9), (13, 15), (17, 21), (23, 26)], [(b.opens, b.closes) for b in found])
    check("a line of an indented code block stands in one, and a table's line in a table",
          stands(28) == reading.INDENTED and stands(30) == reading.TABLE and stands(31) == reading.TABLE, (stands(28), stands(30)))
    check("a heading in a fenced block is no heading, and a code span of three backticks opening no line is no fence",
          [h.title for h in heads] == ["Title", "First", "Twice", "Twice"] and stands(40) == reading.TEXT, [h.title for h in heads])
    check("of two headings sharing a path the path names the first, and the second is marked",
          [h.repeated for h in heads] == [False, False, False, True] and reading.sections(text)[("Twice",)].line == 33, [(h.line, h.repeated) for h in heads])
    check("each line stands under the heading path above it", read[2].lineage == ("First",) and read[7].lineage == ("First",) and read[38].lineage == ("Twice",) and read[0].lineage == (), read[38].lineage)
    cites = reading.citations(text)
    check("a keyed part with two keys gives a pair to each, and a key written as a path gives its names",
          [c.part for c in cites] == [((("Country",), "Canada"), (("Tax Year",), "2025")), ((("States", "State"), "open"),)], [c.part for c in cites])
    check("a citation gives its file, its heading path and its line, a citation of the same file naming none",
          [(c.file, c.lineage, c.line) for c in cites] == [("specs/a.md", ("A", "B"), 39), ("", ("Table",), 40)], [(c.file, c.lineage, c.line) for c in cites])
    check("a whole file's citation gives no heading path, and text that is no citation gives none",
          reading.parse_citation("specs/a.md").lineage == () and reading.parse_citation("a word") is None and reading.parse_citation("README.md") is None)
    live = reading.live(text)
    check("the live text blanks each fenced line to its own length, so a place in it is the same place in the text",
          len(live) == len(text) and live.split("\n")[5] == " " * len("## Not A Heading") and live.split("\n")[2] == "## First")
    check("the reading answers for any text, one that is no file and holds one diagram among them",
          [b.content for b in reading.blocks(tick + "mermaid\nflowchart TD\n" + tick)] == ["flowchart TD"] and reading.blocks("flowchart TD\n  a --> b") == ())
    check("the reading needs nothing a search requires", not ({"search", "sqlite3", "spec_text"} & set(vars(reading))) and reading.__file__.endswith("reading.py"))


def corpus_suite():
    print("the corpus: reading, citers, lines, terms, code, pattern and the result's file")
    root = SCENARIOS / "corpus"
    s = search.Search(root, cover=files_under(root), scratch=fresh("corpus"), quiet=True)
    forms = "specs/forms.md"

    heads = [r[0] for r in s.db.execute("select h.lineage from files f join headings h on h.sha=f.sha where f.path=? and h.lineage != '' order by h.line", (forms,))]
    check("a heading in a tilde fence, an indented fence or a nested fence is no heading of its file",
          heads == ["Citations", "Fences", "After The Fences", "Twice", "Twice", "Terms", "Where A Place Stands", "Where A Place Stands § A Heading Holding Quillwort"], heads)

    r = s.citers("specs/target.md § Target")
    got = lines_of(r.places)
    want = {(forms, line_holding(root, forms, w)) for w in ("A plain citation", "a doubled space", "broken across lines", "carrying its link")}
    want.add((forms, line_holding(root, forms, "## Not A Heading In Tildes") + 1))
    want.add((forms, line_holding(root, forms, "The span: `specs/target.md § Target`")))
    want |= {(forms, line_holding(root, forms, "# @canon-spec specs/target.md § Target")), ("code/sample.py", 11), ("code/sample.ts", 7), ("code/settings.yaml", 1)}
    check("every place citing a section is listed: plain, loose white space, broken across lines, linked, fenced, and each annotation", got == want, sorted(got ^ want))
    check("a mention outside a code span and a same-file citation inside a fenced markdown block are no citers",
          (forms, line_holding(root, forms, "A mention that is no citation")) not in got and (forms, line_holding(root, forms, "A same-file citation of the block")) not in got)
    notes = "\n".join(r.notes)
    check("a citing place in a fenced block says so, in a tilde fence, in a backtick fence and as an annotation, and no other does",
          sorted(p.first for p in r.places if p.stands == "fenced block") == sorted([line_holding(root, forms, w) for w in ("The span: `specs/target.md § Target`", "# @canon-spec specs/target.md § Target")]
                                                                               + [line_holding(root, forms, "## Not A Heading In Tildes") + 1])
          and all(p.endswith(", in a fenced block") == (p.stands == "fenced block") for p in r.places), r.places)
    bare = line_holding(root, forms, "Do the work as specs/target.md")
    check("a citation written bare in a fenced block is read to the heading it names",
          any(n.startswith(f"`specs/forms.md § Fences` line {bare}, in a fenced block: cites a section within it, as `specs/target.md § Target § Child`") for n in r.notes), notes)
    part = s.citers("specs/target.md § Target [Name: first-record]")
    check("a keyed part's citers are listed, with the places citing the section holding it told apart",
          lines_of(part.places) == {(forms, line_holding(root, forms, "A citation of a part of it"))} and sum(": cites the section holding it" in n for n in part.notes) >= 5, (part.places, part.notes))
    check("an annotation is given with the unit it stands over", "an annotation over the unit `Ledger`" in notes, notes)
    check("a place citing a section within it, a part of it or its file is told apart",
          "cites a section within it" in notes and "cites a part of it, `[Name: first-record]`" in notes and "cites its file" in notes, notes)
    check("the same search gives the same list and the same file's name", s.citers("specs/target.md § Target").name == r.name)
    check("a citation asked for with loose white space is the same citation", lines_of(s.citers("specs/target.md  §   Target").places) == got)

    r = s.citers("specs/target.md")
    check("a technical-specs entry is listed with its file's citers, marked as a label",
          ("product/promise.md", 3) in lines_of(r.places) and "a `technical-specs` label, not a citation" in "\n".join(r.notes), r.notes)

    r = s.lines("specs/target.md § Target")
    check("a citation gives the lines of its section's own text", r.places == ["`specs/target.md § Target` lines 5-15"], r.places)
    check("and of its subtree and its file's text before its first section",
          any("lines 5-19: its whole subtree" in n for n in r.notes) and any("lines 1-4: its file's text" in n for n in r.notes), r.notes)
    r = s.lines("specs/target.md § Target § Child")
    check("a child's citation gives its parent whole and each ancestor's own text",
          r.places == ["`specs/target.md § Target § Child` lines 16-19"] and any("lines 5-19: its parent whole" in n for n in r.notes)
          and any("lines 5-15: an ancestor's text" in n for n in r.notes), (r.places, r.notes))
    r = s.lines("specs/target.md § Target [Name: second-record]")
    check("a keyed citation gives its record's lines", r.places == ["`specs/target.md § Target [Name: second-record]` lines 13-14"], r.places)
    r = s.lines("specs/target.md § Table [States.State: closed]")
    check("a keyed citation gives its table's row, and says it stands in a table", r.places == ["`specs/target.md § Table [States.State: closed]` line 27, in a table"], r.places)
    # two headings sharing a path: the index holds what both hold, a citation of the path names it all together, and
    # every result giving a place under either says the path stands more than once and where, so its reader reads each
    twice = [n for n, line in enumerate((root / forms).read_text(encoding="utf-8").split("\n"), 1) if line == "## Twice"]
    first, second = line_holding(root, forms, "The first section"), line_holding(root, forms, "The second section")
    said = f"the path `Twice` stands more than once in the file, 2 times, at lines {twice[0]}, {twice[1]}"
    r = s.lines("specs/forms.md § Twice")
    check("a citation of a path two headings share gives the lines of both, and the result says how many times the path stands and where",
          r.places == [f"`specs/forms.md § Twice` lines {twice[0]}-{twice[1] - 1}", f"`specs/forms.md § Twice` lines {twice[1]}-{line_holding(root, forms, '## Terms') - 1}"]
          and any(said in n for n in r.notes), (r.places, r.notes))
    for kind, find in (("a term's use", s.terms), ("a pattern's match", s.pattern)):
        for which, words, line in (("first", "first section of this path", first), ("second", "second section of this path", second)):
            r = find(words)
            check(f"{kind} under the {which} of two headings sharing a path is cited by the path with its own line, and the result notes the path",
                  [str(p) for p in r.places] == [f"`specs/forms.md § Twice` line {line}"] and any(said in n for n in r.notes), (r.places, r.notes))
    wick, ferry = line_holding(root, forms, "trims the lamp wick"), line_holding(root, forms, "ferry across the estuary")
    r = s.citers("specs/forms.md § Terms")
    check("a citation under each of the two is found, each cited by the path with its own line",
          {f"`specs/forms.md § Twice` line {wick}", f"`specs/forms.md § Twice` line {ferry}"} <= set(r.places) and any(said in n for n in r.notes), (r.places, r.notes))
    for which, name in (("first", "lamp-first"), ("second", "lamp-second")):
        at = line_holding(root, forms, f"**Name:** {name}")
        r = s.lines(f"specs/forms.md § Twice [Name: {name}]")
        check(f"a keyed part under the {which} of them is given by its citation", r.places == [f"`specs/forms.md § Twice [Name: {name}]` lines {at}-{at + 1}"], (r.places, r.notes))
        r = s.terms(name)
        check("and a term's use within it is cited by that keyed part", [str(p) for p in r.places] == [f"`specs/forms.md § Twice [Name: {name}]` line {at}"], r.places)
    r = s.lines("specs/target.md § Missing")
    check("a citation that does not resolve is reported with why", not r.places and "holds no section `Missing`" in r.notes[0], r.notes)

    r = s.terms("append entry")
    got = lines_of(r.places)
    want = {(forms, line_holding(root, forms, w)) for w in ("function append_entry", "flag --append-entry", "class AppendEntry", "appending entries", "the clerk will append")}
    want |= {("code/sample.py", 19), ("code/sample.py", 27), ("code/sample.ts", 12), ("code/sample.ts", 18), ("code/sample.cs", 12), ("code/sample.cs", 15)}
    check("a term is found in every form it takes, in a spec and in code, and where its words only stand apart it is not", got == want, sorted(got ^ want))
    r = s.terms("ledger entry")
    got = lines_of(r.places)
    check("a term is found under each other name the glossary gives it, and the result names the forms searched",
          (forms, line_holding(root, forms, "The LE is posted once")) in got and ("specs/target.md", 7) in got and "`LE`" in r.run_as and "`journal line`" in r.run_as, (sorted(got), r.run_as))

    r = s.pattern("§  +")
    check("a pattern lists every place it matches, and only those", lines_of(r.places) == {(forms, line_holding(root, forms, "a doubled space"))}, r.places)
    r = s.pattern(r"§\nTarget")
    r = s.pattern(r"\]\(/specs/target\.md#target\)")
    check("a pattern reads a file's text as written, a citation's link among it", lines_of(r.places) == {(forms, line_holding(root, forms, "carrying its link"))}, r.places)
    r = s.pattern(r"§\nTarget")
    check("a pattern matches across lines, over a file's whole text", lines_of(r.places) == {(forms, line_holding(root, forms, "broken across lines"))}, r.places)

    def units(structure, name):
        r = s.code_structure(structure, name)
        return {n.split(": the unit ")[0].replace("` line ", ":").strip("`") + " " + n.split(": the unit ")[1].strip("`") for n in r.notes if ": the unit `" in n}

    check("a unit calling a name is listed in each language", units("calls", "append_entry") == {"code/sample.py:19 Ledger.post"}
          and units("calls", "appendEntry") == {"code/sample.ts:12 Ledger.post"} and units("calls", "AppendEntry") == {"code/sample.cs:12 Ledger.Post"},
          (units("calls", "append_entry"), units("calls", "appendEntry"), units("calls", "AppendEntry")))
    check("a unit constructing a name is listed in each language",
          units("constructs", "Receipt") == {"code/sample.py:18 Ledger.post", "code/sample.ts:11 Ledger.post", "code/sample.cs:11 Ledger.Post"}, units("constructs", "Receipt"))
    check("a name in a comment or a string is never matched",
          not any(units(st, n) for st in ("calls", "constructs", "references") for n in ("Fake", "calls_in_a_string", "calls_in_a_comment", "callsInAString", "callsInAComment", "CallsInAString", "CallsInAComment")))
    check("a unit extending a name is listed in each language",
          units("extends", "Base") == {"code/sample.py:13 Ledger", "code/sample.ts:8 Ledger", "code/sample.cs:6 Ledger"}, units("extends", "Base"))
    check("a unit implementing a name is listed", units("implements", "Auditable") == {"code/sample.ts:8 Ledger"} and units("implements", "IAuditable") == {"code/sample.cs:6 Ledger"},
          (units("implements", "Auditable"), units("implements", "IAuditable")))
    check("a unit defining a name is listed", units("defines", "Ledger") == {"code/sample.py:13 Ledger", "code/sample.ts:8 Ledger", "code/sample.cs:6 Ledger"}, units("defines", "Ledger"))
    r = s.code_structure("annotated-with", "specs/target.md § Target § Child")
    notes = "\n".join(r.notes)
    check("a unit carrying an annotation is listed with the annotation", "`code/sample.py` line 12: the unit `Ledger`" in notes and "`code/sample.cs` line 5: the unit `Ledger`" in notes, notes)
    check("a language with no units is named as that, and so is one the search has no parser for",
          "`code/settings.yaml`: YAML has no units" in notes and "`code/schema.sql`: the search has no parser for a .sql file" in notes, notes)

    r = s.citers("specs/target.md § Table")
    after = line_holding(root, forms, "A citation after every fenced block")
    check("a citation after a fenced block is placed at its own line and under its own section, and is not marked as fenced",
          f"`specs/forms.md § After The Fences` line {after}" in r.places and not any(n.startswith(f"`specs/forms.md § After The Fences` line {after}:") for n in r.notes), (r.places, r.notes))
    check("an annotation in a language with no parser is still a citer", ("code/schema.sql", 1) in lines_of(r.places) and ("code/sample.py", 3) in lines_of(r.places), r.places)
    check("a result's file holds its own name, says its places are places to read and whether they are every place",
          r.path.read_text(encoding="utf-8").count(r.name) == 1 and "places to read, never findings" in r.path.read_text(encoding="utf-8") and "**Completeness:** complete" in r.path.read_text(encoding="utf-8"))
    long = s.terms("append entry " + "and a very long question holding a section sign § brackets [ ] and slashes / \\ " * 6)
    check("a result's name is one every system holds", len(long.name) <= search.MAX_NAME and set(long.name) <= set("abcdefghijklmnopqrstuvwxyz0123456789-."), long.name)
    r = s.citers("specs/target.md § Target", ["code"])
    check("a search narrowed to a folder lists no place outside it", {p for p, _ in lines_of(r.places)} == {"code/sample.py", "code/sample.ts", "code/settings.yaml"}, r.places)
    check("a result as the search wrote it passes the check of its form", search.Result.check(r.path) == [], search.Result.check(r.path))
    r.path.write_text(r.path.read_text(encoding="utf-8") + "      - `code/sample.py` line 1\n", encoding="utf-8", newline="\n")
    check("a result whose content was changed no longer gives the hash in its name", any("its content was changed" in p for p in search.Result.check(r.path)), search.Result.check(r.path))
    r = s.meaning("specs/target.md § Target")
    check("a place whose section cites the passage's own section is listed apart from the ranking",
          not any(p.startswith("`specs/forms.md § Citations`") for p in r.places) and any(n.startswith("`specs/forms.md § Citations`") for n in r.notes), (r.places, r.notes))
    r = s.meaning("Every posting is recorded a single time and never twice.")
    check("a search by meaning ranks a place saying the same in other words, and says its places are the first of a ranking",
          r.completeness == "ranked" and any(p.startswith("`product/promise.md § What Is Promised`") for p in r.places[:3]), r.places[:5])
    ferry, wick = line_holding(root, "specs/forms.md", "ferry across the estuary"), line_holding(root, "specs/forms.md", "trims the lamp wick")
    r = s.meaning("A boat crossing the river mouth takes at most forty people while the high spring tide runs.")
    check("a search by meaning gives a passage under the second of two headings sharing a path, cited by the path with its own lines, and notes the path",
          f"`specs/forms.md § Twice` line {ferry}" in r.places[:5] and any("the path `Twice` stands more than once in the file, 2 times" in n for n in r.notes), (r.places[:5], r.notes))
    r = s.meaning("Each evening before dark the lighthouse keeper cuts back the wick of the lamp.")
    check("and a passage under the first of them", f"`specs/forms.md § Twice` line {wick}" in r.places[:5], r.places[:5])
    r = s.meaning("specs/forms.md § Twice", limit=200)
    check("asked by the path's citation, a search by meaning takes what both sections hold as what it was given, and gives back a passage of neither",
          bool(r.places) and not any(p.startswith("`specs/forms.md § Twice`") for p in r.places), (r.places[:5], r.notes))


def places_suite():
    print("places: each a citation of the narrowest thing holding its lines, saying what they stand in")
    root = SCENARIOS / "corpus"
    s = search.Search(root, cover=files_under(root), scratch=fresh("places"), quiet=True)
    forms, section = "specs/forms.md", "`specs/forms.md § Where A Place Stands"
    r = s.terms("quillwort")
    by = {p.first: p for p in r.places}

    def at(words):
        return by.get(line_holding(root, forms, words))

    def n(words):
        return line_holding(root, forms, words)

    check("a place in running text is a citation of its section with its line, and says nothing of where it stands",
          at("Running text holding") == f"{section}` line {n('Running text holding')}", at("Running text holding"))
    check("a place in a row of a table declaring its key cites the row's keyed part, and says it stands in a table",
          at("a tabled quillwort") == f"{section} [Form: plain]` line {n('a tabled quillwort')}, in a table", at("a tabled quillwort"))
    check("a place in a row of a table declaring no key cites the section, and says it stands in a table",
          at("an unkeyed quillwort") == f"{section}` line {n('an unkeyed quillwort')}, in a table", at("an unkeyed quillwort"))
    check("a place in a record cites the record's keyed part", at("a recorded quillwort") == f"{section} [Name: a-record]` line {n('a recorded quillwort')}", at("a recorded quillwort"))
    check("a place in a record whose key an earlier record shares cites the section, since the key's citation names the earlier one",
          at("a second quillwort") == f"{section}` line {n('a second quillwort')}", at("a second quillwort"))
    check("a place in a record whose key holds a code span cites the section, since a citation is written in a code span and cannot hold one",
          at("no citation can write") == f"{section}` line {n('no citation can write')}", at("no citation can write"))
    check("a place in a fenced block says so", at("A fenced line holding") == f"{section}` line {n('A fenced line holding')}, in a fenced block", at("A fenced line holding"))
    check("a place in an indented code block stands in none of a table, a heading and a fenced block",
          at("An indented code block's line") == f"{section}` line {n('An indented code block')}", at("An indented code block's line"))
    check("a place in a heading cites the section the heading opens, and says it stands in a heading",
          at("### A Heading Holding Quillwort") == f"{section} § A Heading Holding Quillwort` line {n('### A Heading Holding')}, in a heading", at("### A Heading Holding Quillwort"))
    check("the search for the word gave those nine places and the last line's, each in the form a result states for a place",
          len(r.places) == 10 and all(search.PLACE.match(p) for p in r.places) and search.Result.check(r.path) == [], (len(r.places), search.Result.check(r.path)))

    first, last = n("| Form | Holds |"), n("| cited |")
    p = s._place(forms, first, last)
    check("a place whose lines hold several keyed parts cites their section with all its lines, and says they stand in a table",
          p == f"{section}` lines {first}-{last}, in a table" and p.key is None, p)
    r = s.pattern(r"a code span\n\n```text\nA fenced line")
    check("a place whose lines stand in more than one of them says nothing of where it stands", [str(x) for x in r.places] == [f"{section}` lines {n('no citation can write')}-{n('A fenced line holding')}"], r.places)
    r = s.pattern(r"line holding quillwort\.\n\n### A Heading")
    check("a place whose lines run from a section into a section beneath it cites the section holding both",
          [(x.lineage, x.first, x.last) for x in r.places] == [("Where A Place Stands", n("An indented code block"), n("### A Heading Holding"))], r.places)
    r = s.pattern(r"each journal line\.\n\n## Where A Place")
    check("a place whose lines run across two sections of a file cites the file",
          [str(x) for x in r.places] == [f"`specs/forms.md` lines {n('The LE is posted once')}-{n('## Where A Place Stands')}"], r.places)
    r = s.citers("specs/target.md § Table")
    cited = next((x for x in r.places if x.first == n("| cited |")), None)
    check("a citing place in a table's row cites the row and says it stands in a table", cited == f"{section} [Form: cited]` line {n('| cited |')}, in a table", r.places)
    code = [x for x in s.terms("append entry").places if x.path.startswith("code/")]
    check("a place in code cites its file with its line", bool(code) and all(x == f"`{x.path}` line {x.first}" for x in code), code)

    # every keyed part a place can cite is one its own citation gives back, over the canon's files kept with the known copies
    root = SCENARIOS / "known-copies" / "files"
    s = search.Search(root, cover=files_under(root), scratch=fresh("places-parts"), quiet=True)
    parts = s.db.execute("select f.path, p.lineage, p.key, p.line_start, p.line_end from files f join parts p on p.sha=f.sha order by f.path, p.line_start").fetchall()
    wrong = []
    for path, lineage, key, start, end in parts[::7]:
        got = s.lines(f"{path} § {lineage} [{key}]").places
        if [(x.first, x.last) for x in got] != [(start, end)]:
            wrong.append((path, lineage, key, start, end, got))
    check(f"a citation of a keyed part gives back the part's own lines, for one in seven of the {len(parts)} parts the canon's files hold", len(parts) > 100 and not wrong, wrong[:3])
    rows = s.db.execute("select f.path, p.lineage, p.key, p.line_start from files f join parts p on p.sha=f.sha where p.line_end > p.line_start order by f.path, p.line_start").fetchall()
    inside = [(path, key, s._place(path, start + 1)) for path, lineage, key, start in rows[::5]]
    check("a line inside a record cites that record or one within it", bool(inside) and all(x.key is not None for _, _, x in inside), [i for i in inside if i[2].key is None][:3])


def cited_sections_suite():
    print("cited sections: each place cited, with every place citing it")
    root = SCENARIOS / "corpus"
    s = search.Search(root, cover=files_under(root), scratch=fresh("cited-sections"), quiet=True)
    r = s.cited_sections()
    groups, order = {}, []
    for place in r.places:
        citing, _, cited = place.partition(" cites ")
        cited = cited.strip("`")
        order += [cited] if cited not in order else []
        groups.setdefault(cited, set()).add(citing)
    check("the listing is every place, each a citing place saying what it cites, and passes the check of a result's form",
          r.kind == "cited sections" and r.completeness == "complete" and search.Result.check(r.path) == [] and all(" cites `" in p for p in r.places), search.Result.check(r.path))
    check("a section, a section within it, a keyed part and a file are each listed as cited",
          {"specs/target.md § Target", "specs/target.md § Target § Child", "specs/target.md § Target [Name: first-record]", "specs/target.md", "specs/target.md § Table"} <= set(groups), sorted(groups))
    check("the places are ordered by what is cited, so the places citing one stand together", order == sorted(order), order)
    differ = {}
    for cited, citing in groups.items():
        alone = {str(p) for p in s.citers(cited).places}
        if alone != citing:
            differ[cited] = sorted(alone ^ citing)
    check(f"what it gives for each of the {len(groups)} places cited agrees with the places citing that one, asked alone", not differ, differ)
    check("a citation written bare in a fenced block is listed under the heading it names",
          any(p.startswith(f"`specs/forms.md § Fences` line {line_holding(root, 'specs/forms.md', 'Do the work as specs/target.md')}, in a fenced block cites") for p in r.places if p.endswith("`specs/target.md § Target § Child`")), r.places)
    narrowed = s.cited_sections(["code"])
    check("narrowed to a folder, it lists the citing places in that folder alone", bool(narrowed.places) and all(p.startswith("`code/") for p in narrowed.places), narrowed.places)
    check("a result saying what a place cites is in its form only as a listing of cited sections",
          any("no listing of cited sections" in p for p in _changed(r.path, "**Kind:** cited sections", "**Kind:** citers")), _changed(r.path, "**Kind:** cited sections", "**Kind:** citers"))


def _changed(path, was, now):
    """-> the problems the check of a result's form reports of a copy of a result with one thing changed."""
    copy = path.with_name("changed-" + path.name)
    copy.write_text(path.read_text(encoding="utf-8").replace(was, now), encoding="utf-8", newline="\n")
    try:
        return search.Result.check(copy)
    finally:
        copy.unlink()


def git(root, *args):
    done = subprocess.run(["git", "-c", "user.name=search-tests", "-c", "user.email=search-tests@example.invalid", "-c", "core.autocrlf=false", "-c", "commit.gpgsign=false"] + list(args),
                          cwd=root, capture_output=True, text=True)
    if done.returncode:
        raise AssertionError(f"git {' '.join(args)}: {done.stderr}")
    return done.stdout.strip()


def put(root, rel, text):
    f = root / rel
    f.parent.mkdir(parents=True, exist_ok=True)
    f.write_text(text, encoding="utf-8", newline="\n")


STACK_FILE = "specs/application/technical/stack.md"


def stack(code_root):
    return f"# Stack\n\n## The Stack\n\n| Language | Code Roots | Excluded |\n|---|---|---|\n| Python | `{code_root}` | |\n"


def a_project(root):
    """Write a small project: a spec, a stack naming `code` as its code root, code in two folders, and working files."""
    put(root, "specs/target.md", "# Target File\n\n## Target\n\nThe heron stands in the reeds.\n")
    put(root, STACK_FILE, stack("code"))
    put(root, "code/sample.py", "def heron():\n    return 'a heron in code'\n")
    put(root, "src/other.py", "def egret():\n    return 'an egret and a heron in other code'\n")
    put(root, ".ai/plans/design-specs/a-design.md", "# Design Document\n\n## The Problem\n\nThe heron is cited as `specs/target.md § Target` from this design.\n")
    put(root, ".ai/plans/other-plan.md", "# Another Plan\n\n## Notes\n\nA heron in another plan, citing `specs/target.md § Target` too.\n")
    put(root, ".ai/follow-ups.md", "# Follow-ups\n\n## One\n\nA heron in the follow-ups.\n")


def outside(name):
    """-> a new folder outside this checkout, so nothing above it is this project's repository."""
    return Path(tempfile.mkdtemp(prefix="search-tests-" + name + "-")).resolve()


def clear(folder):
    """Remove a folder made outside the checkout, git's own read-only files among it."""
    def writable(function, path, _):
        try:
            os.chmod(path, stat.S_IWRITE)
            function(path)
        except OSError:
            pass  # a file the system still holds open is left to the system's own clearing of its temporary folder
    gc.collect()
    shutil.rmtree(folder, onerror=writable)


def paths_of(result):
    return sorted({p.path for p in result.places})


def script(root, *args):
    """-> (the exit code, what was printed) of the search's script run over a project with the arguments given."""
    out = io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(out):
        code = search.main(["search-spec-of-record-scope.py"] + list(args), root=root)
    return code, out.getvalue()


def targets_suite():
    print("targets: the durable files as they stand, as a commit held them, and the working files given")
    root, scratch = outside("targets"), fresh("targets")
    try:
        a_project(root)
        git(root, "init", "-q")
        git(root, "add", "specs", "code")
        git(root, "commit", "-q", "-m", "first")
        first = git(root, "rev-parse", "HEAD")
        put(root, "specs/target.md", "# Target File\n\n## Target\n\nThe heron stands in the reeds.\n\nThe ibis came with the second commit.\n")
        git(root, "add", "specs")
        git(root, "commit", "-q", "-m", "second")
        second = git(root, "rev-parse", "HEAD")
        # since the last commit: the spec gains a line, and the stack names another code root
        put(root, "specs/target.md", "# Target File\n\n## Target\n\nThe heron stands in the reeds.\n\nThe ibis came with the second commit.\n\nThe egret is not yet committed.\n")
        put(root, STACK_FILE, stack("src"))

        def searched(**given):
            return search.Search(root, scratch=scratch, quiet=True, **given)

        s = searched()
        r = s.terms("heron")
        check("a search naming no target answers over the durable files as they stand, the code among them by the stack as it stands, and says so",
              paths_of(r) == ["specs/target.md", "src/other.py"] and r.target == search.CURRENT and r.commit is None and "**Target:** current-durable-files" in r.path.read_text(encoding="utf-8")
              and "**Commit:**" not in r.path.read_text(encoding="utf-8"), (paths_of(r), r.target))
        check("and finds a line not yet committed", paths_of(s.terms("egret")) == ["specs/target.md", "src/other.py"], paths_of(s.terms("egret")))
        s.db.close()

        s = searched(target=search.COMMITTED)
        r = s.terms("heron")
        check("a search of the committed target answers for the files as the last commit held them, the code among them by the code roots the stack named then",
              paths_of(r) == ["code/sample.py", "specs/target.md"], paths_of(r))
        check("and gives no line written since, whatever the files hold now", not s.terms("egret").places and paths_of(s.terms("ibis")) == ["specs/target.md"], s.terms("egret").places)
        held = r.path.read_text(encoding="utf-8")
        check("its result names the target and, its asker having named no commit, the last commit it read under a name of its own, and passes the check of a result's form",
              r.target == search.COMMITTED and r.commit is None and r.last_commit == second and f"**Last Commit:** {second}" in held and "**Commit:**" not in held and search.Result.check(r.path) == [],
              (r.commit, r.last_commit, search.Result.check(r.path)))
        check("a result of the committed files holding neither a Commit nor a Last Commit is not in its form",
              any("holds neither" in p for p in _changed(r.path, f"    **Last Commit:** {second} \\\n", "")), _changed(r.path, f"    **Last Commit:** {second} \\\n", ""))
        check("and one holding both is not in its form",
              any("holds both" in p for p in _changed(r.path, f"    **Last Commit:** {second} \\\n", f"    **Commit:** {second} \\\n    **Last Commit:** {second} \\\n")))
        lines = s.lines("specs/target.md § Target")
        check("the lines a citation names are the commit's", [(p.first, p.last) for p in lines.places] == [(3, 8)], lines.places)
        s.db.close()

        s = searched(target=search.COMMITTED, commit=second)
        check("a search naming the last commit by its name holds it as the Commit its asker named", s.terms("heron").commit == second and s.terms("heron").last_commit is None, (s.terms("heron").commit, s.terms("heron").last_commit))
        s.db.close()

        s = searched(target=search.COMMITTED, commit=first)
        named = s.terms("heron")
        held = named.path.read_text(encoding="utf-8")
        check("a search naming another commit answers for that one, and its result names it",
              not s.terms("ibis").places and paths_of(named) == ["code/sample.py", "specs/target.md"] and named.commit == first, (s.terms("ibis").places, s.commit))
        check("a result holds a Commit only where its asker named one, and then no Last Commit, so a record copied from it pins a search only where one was asked for",
              named.last_commit is None and f"**Commit:** {first}" in held and "**Last Commit:**" not in held and search.Result.check(named.path) == [], (named.last_commit, search.Result.check(named.path)))
        check("a result of the durable files as they stand that names a commit is not in its form",
              any("its Target is not the committed files" in p for p in _changed(named.path, "    **Target:** committed-durable-files \\\n", "    **Target:** current-durable-files \\\n")))
        s.db.close()

        for given, why in (({}, "is given none"), ({"paths": ["specs"]}, "is no working file")):
            try:
                searched(target=search.WORKING, **given)
                refused = ""
            except ValueError as e:
                refused = str(e)
            check(f"a search of the working files that {'is given no path' if not given else 'is given a path that is no working file'} is refused", why in refused, refused)
        s = searched(target=search.WORKING, paths=[".ai/plans/design-specs"])
        r = s.terms("heron")
        check("a search of the working files answers over the paths it is given alone, and its result names the target and the paths",
              paths_of(r) == [".ai/plans/design-specs/a-design.md"] and r.target == search.WORKING and r.narrowed == [".ai/plans/design-specs"] and search.Result.check(r.path) == [],
              (paths_of(r), r.narrowed, search.Result.check(r.path)))
        r = s.citers("specs/target.md § Target")
        check("it lists the working files' places citing a durable file's section, read against that file, and no place among the durable files",
              paths_of(r) == [".ai/plans/design-specs/a-design.md"] and not any("does not resolve" in n for n in r.notes), (r.places, r.notes))
        r = s.cited_sections()
        check("its listing of cited sections holds citing places of the working files alone, the durable section they cite named and no place",
              [str(p) for p in r.places] == ["`.ai/plans/design-specs/a-design.md § The Problem` line 5 cites `specs/target.md § Target`"], r.places)
        check("a result of the working files holding no path it was given is not in its form",
              any("holds no Narrowed To" in p for p in _changed(r.path, "    **Narrowed To:**\n      - `.ai/plans/design-specs`\n\n", "")), _changed(r.path, "    **Narrowed To:**\n      - `.ai/plans/design-specs`\n\n", ""))
        s.db.close()
        s = searched(target=search.WORKING, paths=[".ai/plans", ".ai/follow-ups.md"])
        check("given more paths it answers over more, a file and a folder among them",
              paths_of(s.terms("heron")) == [".ai/follow-ups.md", ".ai/plans/design-specs/a-design.md", ".ai/plans/other-plan.md"] and s.read_count == 2, (paths_of(s.terms("heron")), s.read_count))
        s.db.close()
        s = searched(target=search.WORKING, paths=[".ai/plans/design-specs"])
        check("given fewer again, it reads no file again and gives no place of a path it was not given", s.read_count == 0 and paths_of(s.terms("heron")) == [".ai/plans/design-specs/a-design.md"], (s.read_count, paths_of(s.terms("heron"))))
        s.db.close()

        # one index held all three: each target's search still gives its own files alone
        s = searched()
        check("after the other targets' searches, a search of the durable files as they stand gives no working file and no file only the commit held",
              paths_of(s.terms("heron")) == ["specs/target.md", "src/other.py"] and s.read_count == 0, (paths_of(s.terms("heron")), s.read_count))
        s.db.close()
        s = searched(target=search.COMMITTED)
        check("and a search of the committed target gives the commit's files alone, reading again only the one file the last commit holds otherwise than the commit searched before it",
              paths_of(s.terms("heron")) == ["code/sample.py", "specs/target.md"] and paths_of(s.terms("ibis")) == ["specs/target.md"] and s.read_count == 1, (paths_of(s.terms("heron")), s.read_count))
        s.db.close()

        ran, refused = script(root, "--show-term-uses", "ibis", "--target", search.COMMITTED, "--commit", first)[0], script(root, "--show-term-uses", "heron", "--target", search.WORKING)[0]
        check("the script takes the target and the commit, and refuses a search of the working files given no path", ran == 0 and refused == 2, (ran, refused))

        # a project standing in a folder of a larger repository is under git
        put(root, "inner/specs/target.md", "# Inner\n\n## Target\n\nThe bittern is committed in a folder of the repository.\n")
        git(root, "add", "inner")
        git(root, "commit", "-q", "-m", "third")
        put(root, "inner/specs/target.md", "# Inner\n\n## Target\n\nThe bittern is committed in a folder of the repository.\n\nThe crane is not.\n")
        s = search.Search(root / "inner", scratch=fresh("targets-inner"), quiet=True, target=search.COMMITTED)
        check("a project standing in a folder of a larger repository is read as under git, its committed files given by their paths from the project's root",
              search.version_control(root / "inner") == search.GIT and paths_of(s.terms("bittern")) == ["specs/target.md"] and not s.terms("crane").places, (paths_of(s.terms("bittern")), s.terms("crane").places))
        s.db.close()
    finally:
        clear(root)


def git_cases_suite():
    print("git absent or failing: the committed target stops and says which, and the other targets answer the same")
    under_git, unreadable, under_none = outside("git"), outside("unreadable"), outside("none")
    path = os.environ.get("PATH", "")
    empty = outside("no-git-on-path")
    try:
        for root in (under_git, unreadable, under_none):
            a_project(root)
        git(under_git, "init", "-q")
        git(under_git, "add", "specs", "code")
        git(under_git, "commit", "-q", "-m", "first")
        put(unreadable, ".git/HEAD", "no repository git can read\n")
        check("the three projects are told apart from their files: under git, under git, and under no version control the search reads",
              [search.version_control(r) for r in (under_git, unreadable, under_none)] == [search.GIT, search.GIT, search.NONE_READ], [search.version_control(r) for r in (under_git, unreadable, under_none)])

        def answers(root, name, **given):
            scratch = fresh("git-cases-" + name)
            try:
                s = search.Search(root, scratch=scratch, quiet=True, **given)
            except search.CannotSearch as e:
                return str(e), scratch.exists()
            places = [str(p) for p in s.terms("heron").places] + [str(p) for p in s.citers("specs/target.md § Target").places]
            s.db.close()
            return places, True

        working = {"target": search.WORKING, "paths": [".ai/plans"]}
        want = {"current": answers(under_git, "want-current")[0], "working": answers(under_git, "want-working", **working)[0]}
        check("with git at hand, each target answers over the project under git", len(want["current"]) == 3 and len(want["working"]) == 4 and isinstance(answers(under_git, "want-committed", target=search.COMMITTED)[0], list), want)

        said, wrote = answers(unreadable, "unreadable-committed", target=search.COMMITTED)
        check("over a repository git cannot read, a search of the committed target stops, giving what it asked and git's own words, and writes nothing",
              isinstance(said, str) and "git answered with a failure" in said and "`git rev-parse --verify HEAD^{commit}`" in said and "git answered: fatal:" in said and not wrote, said)
        check("and a search of either other target answers as it does over the project under git",
              answers(unreadable, "unreadable-current")[0] == want["current"] and answers(unreadable, "unreadable-working", **working)[0] == want["working"])

        said, wrote = answers(under_none, "none-committed", target=search.COMMITTED)
        check("over a folder under no version control, a search of the committed target stops, saying the project is under no version control the search reads, and writes nothing",
              isinstance(said, str) and "under no version control the search reads" in said and not wrote, said)
        check("and a search of either other target answers as it does over the project under git",
              answers(under_none, "none-current")[0] == want["current"] and answers(under_none, "none-working", **working)[0] == want["working"])

        os.environ["PATH"] = str(empty)
        try:
            hidden = shutil.which("git") is None
            said, wrote = answers(under_git, "hidden-committed", target=search.COMMITTED)
            current, worked = answers(under_git, "hidden-current")[0], answers(under_git, "hidden-working", **working)[0]
            none_said = answers(under_none, "hidden-none-committed", target=search.COMMITTED)[0]
        finally:
            os.environ["PATH"] = path
        check("with git kept from it, a search of the committed target over a project under git stops, saying git is not installed, and writes nothing",
              hidden and isinstance(said, str) and "the project is under git and git is not installed" in said and not wrote, said)
        check("and it never reads that project as under no version control, which it says of a folder under none even then",
              "no version control" not in said and isinstance(none_said, str) and "under no version control the search reads" in none_said, (said, none_said))
        check("and a search of either other target answers as it does with git at hand", current == want["current"] and worked == want["working"], (current, worked))
        # git names the commit and lists its files, and fails reading what they hold: one file's object is spoiled
        blob = git(under_git, "rev-parse", "HEAD:specs/target.md").strip()
        held = under_git / ".git" / "objects" / blob[:2] / blob[2:]
        os.chmod(held, 0o666)
        held.write_bytes(b"no object git can read")
        said, wrote = answers(under_git, "spoiled-committed", target=search.COMMITTED)
        check("where git gives no content for a file the commit lists, a search of the committed target stops, giving what it asked and what git answered, and writes nothing",
              isinstance(said, str) and "git gave no content for a file the commit lists" in said and "`git cat-file --batch`" in said and "a file it calls missing" in said and not wrote, said)
        ran, printed = script(under_git, "--show-term-uses", "heron", "--target", search.COMMITTED)
        check("and the script stops with those words and no traceback", ran == 1 and "`git cat-file --batch`" in printed and "Traceback" not in printed, (ran, printed))
        check("and a search of either other target answers as it does over the project under git",
              answers(under_git, "spoiled-current")[0] == want["current"] and answers(under_git, "spoiled-working", **working)[0] == want["working"])

        ran, printed = script(under_none, "--show-term-uses", "heron", "--target", search.COMMITTED)
        check("the script stops with the same words and no usage", ran == 1 and "under no version control the search reads" in printed and "usage:" not in printed, (ran, printed))
    finally:
        os.environ["PATH"] = path
        for folder in (under_git, unreadable, under_none, empty):
            clear(folder)


def moved_in_time(path):
    """Move a file's time of change and leave what it holds."""
    held = path.stat()
    os.utime(path, ns=(held.st_atime_ns + 5_000_000_000, held.st_mtime_ns + 5_000_000_000))


def snapshot_suite():
    print("the snapshot code: the state of a target's files, on every result and on request")
    root, scratch = outside("snapshot"), fresh("snapshot")
    try:
        a_project(root)
        git(root, "init", "-q")
        git(root, "add", "specs", "code")
        git(root, "commit", "-q", "-m", "first")

        def searched(**given):
            return search.Search(root, scratch=scratch, quiet=True, **given)

        s = searched()
        r, narrow, cite = s.terms("heron"), s.terms("heron", ["specs"]), s.citers("specs/target.md § Target")
        code = r.snapshot
        check("every result carries a snapshot code, sixteen hexadecimal digits, which its file holds, and passes the check of a result's form",
              bool(search.SNAPSHOT.fullmatch(code or "")) and f"**Snapshot:** {code} \\" in r.path.read_text(encoding="utf-8") and search.Result.check(r.path) == [], (code, search.Result.check(r.path)))
        check("one code stands for the whole target, whatever a search was narrowed to and whatever its kind", narrow.snapshot == code == cite.snapshot and narrow.narrowed == ["specs"], (code, narrow.snapshot, cite.snapshot))
        check("a result whose Snapshot is not in a code's form fails the check of its form",
              any("not a snapshot code" in p for p in _changed(r.path, f"**Snapshot:** {code}", "**Snapshot:** the-files-as-i-found-them")), _changed(r.path, f"**Snapshot:** {code}", "**Snapshot:** the-files-as-i-found-them"))
        check("and one holding none fails it", any("holds no Snapshot" in p for p in _changed(r.path, f"    **Snapshot:** {code} \\\n", "")))
        s.db.close()
        check("the search gives the present code on request, equal to a result's while no file of the target holds anything new", search.snapshot(root, scratch=scratch) == code, search.snapshot(root, scratch=scratch))
        ran, printed = script(root, "--show-snapshot-code")
        check("the script gives it too, from an index of its own, the code built from the files and never from an index", ran == 0 and code in printed.split("\n"), (ran, printed))
        s = searched(target=search.COMMITTED)
        check("the code is built one way whatever the target: the files the last commit held take the code the files as they stand take, each file holding the same",
              s.terms("heron").snapshot == code and search.snapshot(root, target=search.COMMITTED, scratch=scratch) == code, s.terms("heron").snapshot)
        s.db.close()

        moved_in_time(root / "specs" / "target.md")
        s = searched()
        check("a file whose time of change alone moved is read again and leaves the code as it was", s.read_count == 1 and s.terms("heron").snapshot == code, (s.read_count, s.terms("heron").snapshot))
        s.db.close()

        put(root, "specs/target.md", "# Target File\n\n## Target\n\nThe heron stands in the reeds.\n\nThe egret is not yet committed.\n")
        s = searched()
        after = s.terms("heron").snapshot
        check("once a file of the target holds something new the code differs, on a result and on request", after != code and search.snapshot(root, scratch=scratch) == after, (code, after))
        s.db.close()
        check("and the code of the committed files stands as it did, no commit having changed", search.snapshot(root, target=search.COMMITTED, scratch=scratch) == code)
        put(root, "specs/target.md", "# Target File\n\n## Target\n\nThe heron stands in the reeds.\n")
        check("a file brought back to what it held brings the code back", search.snapshot(root, scratch=scratch) == code)

        s = searched(target=search.WORKING, paths=[".ai/plans/design-specs"])
        one = s.terms("heron").snapshot
        s.db.close()
        check("a result of the working files holds the code of the paths it names, which the search gives on request for those paths",
              bool(search.SNAPSHOT.fullmatch(one)) and one != code and search.snapshot(root, target=search.WORKING, paths=[".ai/plans/design-specs"], scratch=scratch) == one, one)
        check("and other paths take another code", search.snapshot(root, target=search.WORKING, paths=[".ai/plans"], scratch=scratch) != one)
        put(root, ".ai/plans/other-plan.md", "# Another Plan\n\n## Notes\n\nA heron in another plan, changed.\n")
        put(root, "specs/target.md", "# Target File\n\n## Target\n\nThe heron stands in the reeds, changed.\n")
        check("a working file changed outside the paths named, and a durable file changed, leave that code as it was: it stands for the paths named alone",
              search.snapshot(root, target=search.WORKING, paths=[".ai/plans/design-specs"], scratch=scratch) == one)
        put(root, ".ai/plans/design-specs/a-design.md", "# Design Document\n\n## The Problem\n\nThe heron, changed.\n")
        check("and a working file changed under them changes it", search.snapshot(root, target=search.WORKING, paths=[".ai/plans/design-specs"], scratch=scratch) != one)
    finally:
        clear(root)


def same_answer(one, other):
    """-> whether two results hold the same answer: the same record but its name, each place the same place."""
    places = lambda r: [(str(p), getattr(p, "path", None), getattr(p, "first", None), getattr(p, "last", None), getattr(p, "lineage", None), getattr(p, "key", None), getattr(p, "stands", None)) for p in r.places]
    return one.body() == other.body() and places(one) == places(other) and one.notes == other.notes and one.names_nothing == other.names_nothing


def kept_suite():
    print("the answers the search keeps: given again while nothing changed, computed anew once anything did")
    root, scratch = outside("kept"), fresh("kept")
    try:
        a_project(root)
        put(root, "specs/target.md", "# Target File\n\n## Target\n\nThe heron stands in the reeds.\n\n## Citing\n\nThe reeds are cited as `specs/target.md § Target`.\n")
        put(root, "code/sample.py", "class Heron:\n    pass\n\n\ndef heron():\n    return Heron()\n")
        git(root, "init", "-q")
        git(root, "add", "specs", "code")
        git(root, "commit", "-q", "-m", "first")

        def searched(**given):
            return search.Search(root, scratch=scratch, quiet=True, **given)

        asks = {
            "citers": lambda s: s.citers("specs/target.md § Target"),
            "cited sections": lambda s: s.cited_sections(),
            "lines": lambda s: s.lines("specs/target.md § Target"),
            "terms": lambda s: s.terms("heron"),
            "code structure": lambda s: s.code_structure("defines", "heron"),
            "pattern": lambda s: s.pattern("heron +stands"),
        }
        s = searched()
        first = {kind: ask(s) for kind, ask in asks.items()}
        check("an answer computed is no answer the search kept, and each is computed once", not any(r.kept for r in first.values()) and s.computed == len(asks), s.computed)
        again = {kind: ask(s) for kind, ask in asks.items()}
        check("asked the same again while the files stand, the search gives the answer it kept of each kind resting on its target's files alone, and computes nothing anew",
              all(r.kept for r in again.values()) and s.computed == len(asks), ([k for k, r in again.items() if not r.kept], s.computed))
        check("and the answer it kept is the answer it computed, written as a result of the same name",
              all(same_answer(first[k], again[k]) and first[k].name == again[k].name and again[k].path.is_file() for k in asks), [k for k in asks if not same_answer(first[k], again[k])])
        s.db.close()
        s = searched()
        later = {kind: ask(s) for kind, ask in asks.items()}
        check("a later run gives the kept answers too, computing nothing", all(r.kept for r in later.values()) and s.computed == 0, s.computed)
        other = search.Search(root, scratch=fresh("kept-fresh"), quiet=True)
        computed = {kind: ask(other) for kind, ask in asks.items()}
        other.db.close()
        check("an answer the search gives from what it kept is the answer a fresh computing gives, from an index built anew",
              not any(r.kept for r in computed.values()) and all(same_answer(later[k], computed[k]) for k in asks), [k for k in asks if not same_answer(later[k], computed[k])])
        for stale in (scratch / "results").glob("*.md"):
            stale.unlink()
        check("what the search keeps is no result's file: with every result's file gone it still gives the answer it kept, and writes the result again",
              s.terms("heron").kept and s.terms("heron").path.is_file())

        before = s.computed
        check("a question differing in what was asked is computed anew", not s.terms("egret").kept and not s.terms("reeds").kept and s.computed == before + 2, s.computed)
        check("and one differing in the paths it is narrowed to, which is then kept as a question of its own",
              not s.terms("heron", ["specs"]).kept and s.terms("heron", ["specs"]).kept and paths_of(s.terms("heron", ["specs"])) == ["specs/target.md"] and s.terms("heron").kept)
        check("and one differing in its kind", not s.pattern("heron").kept and s.pattern("heron").kept)
        s.db.close()
        s = searched(target=search.COMMITTED)
        check("and one differing in its target, an answer kept for the files as they stand being none for the committed files", not s.terms("heron").kept and s.terms("heron").kept)
        last = s.commit
        s.db.close()
        s = searched(target=search.COMMITTED, commit=last)
        check("and one differing in the commit its asker named, though it names the last commit", not s.terms("heron").kept and s.terms("heron").commit == last)
        s.db.close()

        moved_in_time(root / "specs" / "target.md")
        s = searched()
        check("a file whose time of change alone moved leaves the kept answer standing", s.read_count == 1 and s.terms("heron").kept)
        s.db.close()
        put(root, "specs/target.md", "# Target File\n\n## Target\n\nThe heron stands in the reeds.\n\n## Citing\n\nThe reeds are cited as `specs/target.md § Target`.\n\nA second heron came.\n")
        s = searched()
        r = s.terms("heron")
        check("once a file of the target holds something new, every answer is computed anew and gives the new place",
              not r.kept and len([p for p in r.places if p.path == "specs/target.md"]) == 2 and not s.citers("specs/target.md § Target").kept, (r.kept, r.places))
        check("and is then kept under the code the files now take", s.terms("heron").kept)
        s.db.close()
        s = searched(target=search.COMMITTED)
        check("an answer kept for the committed files stands while no commit changed them, whatever the files as they stand came to hold", s.terms("heron").kept)
        s.db.close()

        s = searched()
        reading = search.own_reading()
        search._OWN_READING = "0" * 16   # the search's own code as another checkout holds it
        try:
            changed = s.terms("heron")
            check("once the search's own code has changed, a kept answer is not given: the answer is computed anew by the code that runs", not changed.kept)
        finally:
            search._OWN_READING = None
        check("the code of the search's own reading is built from its own script and the shared modules it imports",
              search.own_reading() == reading and bool(search.SNAPSHOT.fullmatch(reading)))
        check("and an answer that other code computed is not given by this code, which computes its own and keeps it", not s.terms("heron").kept and s.terms("heron").kept)

        m, n = s.meaning("The heron stands in the reeds."), s.meaning("The heron stands in the reeds.")
        c, d = s.code_structure("constructs", "Heron"), s.code_structure("constructs", "Heron")
        check("no answer is kept of a search by meaning or of a search for constructions, each computed whenever it is asked",
              not (m.kept or n.kept or c.kept or d.kept) and paths_of(c) == ["code/sample.py"], (m.kept, n.kept, c.kept, d.kept, c.places))
        s.db.close()
        put(root, ".ai/plans/other-plan.md", "# Another Plan\n\n## Notes\n\nThe heron stands in the reeds of another plan.\n\nclass Heron:\n")
        s = searched(target=search.WORKING, paths=[".ai/plans"])
        s.terms("heron")
        s.db.close()
        s = searched()
        before = s.computed
        m, c = s.meaning("The heron stands in the reeds."), s.code_structure("constructs", "Heron")
        check("asked again after another target's files changed, each is computed anew, while a search of a kind kept gives what it kept",
              not m.kept and not c.kept and s.computed == before + 2 and s.terms("heron").kept and s.computed == before + 2, (m.kept, c.kept, s.computed - before))
        s.db.close()

        s = searched(target=search.WORKING, paths=[".ai/plans/design-specs"])
        w = s.citers("specs/target.md § Target")
        check("an answer of a search of the working files is kept", not w.kept and len(w.places) == 1 and s.citers("specs/target.md § Target").kept, w.places)
        s.db.close()
        put(root, "specs/target.md", "# Target File\n\n## Retitled\n\nThe heron stands in the reeds.\n")
        s = searched(target=search.WORKING, paths=[".ai/plans/design-specs"])
        w = s.citers("specs/target.md § Target")
        check("and also under the code of the durable files as they stand, which it reads what its places cite against: a durable file changed, it is computed anew, no working file having changed",
              s.read_count == 1 and not w.kept and any("does not resolve" in n for n in w.notes), (s.read_count, w.kept, w.notes))
        s.db.close()
    finally:
        search._OWN_READING = None
        clear(root)


def names_nothing_suite():
    print("a question naming nothing to ask of: told to the caller, each case apart")
    root = SCENARIOS / "corpus"
    s = search.Search(root, cover=files_under(root), scratch=fresh("names-nothing"), quiet=True)
    asked = s.citers("specs/target.md § Target")
    check("a question naming something tells its caller nothing of the kind", asked.names_nothing == [] and len(asked.places) > 0, asked.names_nothing)
    for kind, r in (("citers", s.citers("specs/target.md § No Such Section")), ("lines", s.lines("specs/target.md § No Such Section")), ("citers of a file", s.citers("specs/no-such-file.md § Target")),
                    ("meaning", s.meaning("specs/target.md § No Such Section"))):
        check(f"a citation that names no place among the files is told, and the answer stands as no place given ({kind})",
              r.names_nothing == [search.NO_PLACE] and r.places == [] and any("does not resolve" in n for n in r.notes), (r.names_nothing, r.places, r.notes))
    r = s.terms("--- !!! ---")
    check("a term reducing to no word is told", r.names_nothing == [search.NO_WORD] and r.places == [] and any("reduces to no word" in n for n in r.notes), (r.names_nothing, r.notes))
    r = s.meaning("--- !!! ---")
    check("a passage reducing to no word is told", r.names_nothing == [search.NO_WORD] and any("reduces to no word" in n for n in r.notes), (r.names_nothing, r.notes))
    r = s.terms("posting", ["specs/nowhere"])
    check("a path the search is narrowed to under which no file of its target stands is told, with the path",
          r.names_nothing == [search.NO_FILE] and r.places == [] and any("`specs/nowhere`" in n for n in r.notes), (r.names_nothing, r.notes))
    r = s.terms("posting", ["specs", "specs/nowhere"])
    check("it is told of the one path holding no file where another holds some, the answer standing for the other", r.names_nothing == [search.NO_FILE] and len(r.places) > 0, (r.names_nothing, r.places))
    r = s.pattern("posting", ["code/nowhere"])
    check("it is told of a pattern's narrowing too, a pattern holding no word being a question as any other", r.names_nothing == [search.NO_FILE] and s.pattern("§  +").names_nothing == [], r.names_nothing)
    r = s.terms("--- !!! ---", ["specs/nowhere"])
    check("each case is told apart from the others, a question holding two holding both", sorted(r.names_nothing) == sorted([search.NO_WORD, search.NO_FILE]) and len(set(search.NAMES_NOTHING)) == 3, r.names_nothing)
    again = s.terms("posting", ["specs/nowhere"])
    check("an answer the search kept tells it as the answer computed did", again.kept and again.names_nothing == [search.NO_FILE] and same_answer(again, s.terms("posting", ["specs/nowhere"])))
    s.db.close()
    root = outside("names-nothing")
    try:
        a_project(root)
        w = search.Search(root, scratch=fresh("names-nothing-working"), quiet=True, target=search.WORKING, paths=[".ai/plans/no-such-plans"])
        r = w.terms("heron")
        check("a search of the working files given a path holding no file is told so", r.names_nothing == [search.NO_FILE] and r.places == [], (r.names_nothing, r.places))
        w.db.close()
        ran, printed = script(root, "--show-citers", "specs/target.md § No Such Section")
        check("the script says it of a question it ran, in words of its own for each case", ran == 0 and "the question names nothing to ask of: " + search.NO_PLACE in printed, printed)
        ran, printed = script(root, "--show-term-uses", "heron", "--paths", "specs/nowhere")
        check("and of a path holding no file", ran == 0 and "the question names nothing to ask of: " + search.NO_FILE in printed, printed)
    finally:
        clear(root)


def research_failures_suite():
    print("the three failures of a design's research, each a test of what the search does")
    root = SCENARIOS / "research-failures"
    s = search.Search(root, cover=files_under(root), scratch=fresh("research-failures"), quiet=True)
    against = line_holding(root, "specs/reading.md", "read against")
    r = s.terms("read again")
    check("a search for the words `read again` finds them, and gives no place saying only `read against`",
          lines_of(r.places) == {("specs/reading.md", line_holding(root, "specs/reading.md", "checked is read again"))} and ("specs/reading.md", against) not in lines_of(r.places), (lines_of(r.places), against))
    apart = line_holding(root, "specs/running.md", "runs each Search again")
    r = s.terms("run again")
    check("a search for `run again` finds the words standing together, in whatever form each takes",
          ("specs/running.md", line_holding(root, "specs/running.md", "is run again")) in lines_of(r.places), r.places)
    # a limit of the search, stated in its skill: a term is searched as a phrase, its words in their order with none between
    check("and does not find them where other words stand between, as in `runs each Search again`: a limit the skill states", ("specs/running.md", apart) not in lines_of(r.places), r.places)
    s.db.close()
    root = SCENARIOS / "known-copies" / "files"
    s = search.Search(root, cover=files_under(root), scratch=fresh("research-failures-meaning"), quiet=True)
    rule = line_holding(root, "specs/methodology/working-files/main.md", "reads the files at the last commit wherever it would otherwise read the files as they stand")
    r = s.meaning("Which state of the files does a search answer for?")
    found = any(p.path == "specs/methodology/working-files/main.md" and p.first <= rule <= p.last for p in r.places)
    # a limit of the search, stated in its skill: asked a question, it ranks the places worded as the question is, and
    # the rule answering it, which shares none of its words, stands outside the first twenty
    check("a search by meaning asked which state of the files a search answers for does not give, among its first twenty places, the rule on reading the last commit while a send-back's changes are kept: a limit the skill states",
          not found and r.ranking_part() == f"1 to {search.RANKED}", [str(p) for p in r.places[:5]])
    r = s.meaning("While changes are kept in a checkout, a reading for a design reads the files as the last commit held them, not as they stand.")
    check("asked with the rule in other words, it gives that rule among its first twenty places",
          any(p.path == "specs/methodology/working-files/main.md" and p.first <= rule <= p.last for p in r.places), [str(p) for p in r.places[:5]])
    s.db.close()


def rerun_suite():
    print("the index: what a run reads again")
    source, root = SCENARIOS / "corpus", fresh("rerun-files")
    shutil.copytree(source, root)
    scratch = fresh("rerun")
    first = search.Search(root, cover=files_under(root), scratch=scratch, quiet=True)
    check("the first use builds the whole index, reading every file", first.built and first.read_count == len(files_under(root)), first.read_count)
    name = first.citers("specs/target.md § Target").name
    other = first.terms("posting").name
    first.db.close()
    second = search.Search(root, cover=files_under(root), scratch=scratch, quiet=True)
    check("on unchanged files a run reads no file again", second.read_count == 0 and not second.built, second.read_count)
    check("and writes a result of the same name", second.citers("specs/target.md § Target").name == name)
    second.db.close()
    with open(root / "specs" / "target.md", "a", encoding="utf-8", newline="\n") as f:
        f.write("\nA line added, citing `specs/target.md § Target` from its own file.\n")
    third = search.Search(root, cover=files_under(root), scratch=scratch, quiet=True)
    check("after one file changes a run reads that file alone", third.read_count == 1, third.read_count)
    check("and clears every result written before the change, a result of a question not asked again among them",
          not (scratch / "results" / other).exists() and not list((scratch / "results").glob("*.md")), list((scratch / "results").glob("*.md")))
    changed = third.citers("specs/target.md § Target")
    check("and the result's name differs once its content does", changed.name != name and not (scratch / "results" / name).exists(), changed.name)
    third.db.close()


def checkout_suite():
    print("the checkout: where the model is found, how long a result's path grows, and which checkout a search runs over")
    # a project of its own, outside this checkout, holding a copy of the search's code as this checkout holds it, under
    # version control, with a second checkout of it, a worktree kept among its own working files
    root = outside("checkout")
    try:
        shutil.copytree(PROJECT / LIB, root / LIB, ignore=shutil.ignore_patterns("__pycache__"))
        a_project(root)
        put(root, ".ai/skills/%s/SKILL.md" % search.SKILL, "# The Search's Skill\n\nA stand-in, so each checkout of the project holds the skill's folder.\n")
        git(root, "init", "-q")
        git(root, "add", "-A")
        git(root, "commit", "-q", "-m", "a project made for a test")
        second = root / ".ai" / "tmp" / "worktrees" / "second"
        git(root, "worktree", "add", "-q", "--detach", str(second), "HEAD")

        def model_of(checkout):
            """-> where the search whose code stands in a checkout looks for its model, asked of that code itself."""
            asked = subprocess.run([sys.executable, "-c", "import sys\nsys.dont_write_bytecode = True\nsys.path.insert(0, sys.argv[1])\nimport search\nprint(search.model_folder())",
                                    str(checkout / LIB)], capture_output=True, text=True, encoding="utf-8", cwd=checkout)
            return Path(asked.stdout.strip()).resolve() if asked.returncode == 0 and asked.stdout.strip() else asked.stderr[-300:]

        kept = (root / search.SCRATCH / "model").resolve()
        check("the search whose code stands in a project's main checkout looks for its model in that checkout's scratch space", model_of(root) == kept, model_of(root))
        check("the search whose code stands in a second checkout, a worktree, looks for its model where the main checkout keeps it", model_of(second) == kept, model_of(second))
        check("a checkout under no version control is its own main checkout, and a worktree's is the checkout holding the repository",
              search.main_checkout(root / "code") == root / "code" and search.main_checkout(second) == root and search.main_checkout(root) == root,
              (search.main_checkout(second), root))

        # a result written in a folder standing deep: its whole path stays one every system opens
        deep = root
        while len(str(deep)) < 200:
            deep = deep / "a-folder-standing-deep"
        asked = "the lighthouse keeper trims the lamp wick each evening before dark and the ferry crosses the estuary at the turn of the tide " * 3
        result = search.Result("terms", asked, [], "each form searched as a phrase", "complete", [])
        try:
            written = result.write(deep / "results")
            wrote = written.is_file()
        except OSError as failed:
            written, wrote = deep / "results" / (result.name or ""), "the result could not be written: %s" % failed
        check("a result written in a folder standing deep keeps its whole path within the longest every system opens, and is written",
              wrote is True and len(str(written.resolve())) <= search.MAX_PATH, (wrote, len(str(written)), search.MAX_PATH))
        check("and its name still tells it apart by its two hashes, with the words asked that fit",
              wrote is True and bool(re.fullmatch(r"terms-the-lighthouse[a-z0-9-]*-[0-9a-f]{6}-[0-9a-f]{8}\.md", written.name)), written.name)
        shallow = search.Result("terms", asked, [], "each form searched as a phrase", "complete", []).write(root / "results")
        check("in a folder standing shallow the same result's name holds the words asked up to the length a name may take, and ends in the same two hashes",
              search.MAX_NAME - 1 <= len(shallow.name) <= search.MAX_NAME and shallow.name[-18:] == written.name[-18:], (len(shallow.name), shallow.name[-18:], written.name[-18:]))

        # a search naming no project answers over the checkout it is run in, whichever checkout holds the script
        was = Path.cwd()
        out = io.StringIO()
        try:
            os.chdir(second)
            with contextlib.redirect_stdout(out), contextlib.redirect_stderr(out):
                code = search.main(["search-spec-of-record-scope.py", "--show-term-uses", "heron"])
        finally:
            os.chdir(was)
        check("a search naming no project, run in a second checkout, answers over that checkout's files and writes its result there",
              code == 0 and "`specs/target.md § Target` line 5" in out.getvalue() and len(list((second / search.SCRATCH / "results").glob("terms-heron-*.md"))) == 1
              and not (root / search.SCRATCH / "results").exists(),
              (code, out.getvalue()[-400:], [p.name for p in (second / search.SCRATCH / "results").glob("*")], (root / search.SCRATCH / "results").exists()))
    finally:
        gc.collect()
        clear(root)


def requirements_suite():
    print("what the search requires")
    held = search.REQUIREMENTS
    try:
        search.REQUIREMENTS = held + [search.Requirement("a package that is absent", "a test takes it away", "python -m pip install it", lambda root: False)]
        scratch = fresh("requirements")
        for kind in ("citers", "lines", "terms", "pattern", "meaning", "code_structure"):
            try:
                search.Search(SCENARIOS / "corpus", cover=[], scratch=scratch, quiet=True)
                stopped, text = False, ""
            except search.MissingRequirements as e:
                stopped, text = True, str(e)
            check(f"with a requirement absent a search by {kind.replace('_', ' ')} stops before it reads or writes",
                  stopped and not scratch.exists() and "a package that is absent: a test takes it away" in text and "to install it: python -m pip install it" in text, text)
    finally:
        search.REQUIREMENTS = held


def ranking_suite():
    print("a ranking: a sentence restated in a longer passage, and a ranking read in parts")
    # a corpus of its own: a rule, more than twenty short statements sharing its words, and one long passage on other
    # subjects holding one sentence that restates the rule
    root = SCENARIOS / "restated-sentence"
    rule = (root / "product/stocktake.md").read_text(encoding="utf-8").split("## The Rule")[1].split("##")[0].strip()

    def place_of_the_restating_passage(name):
        s = search.Search(root, cover=files_under(root), scratch=fresh(name), quiet=True)
        places = s.meaning(rule, limit=100).places
        s.db.close()
        return next((n for n, place in enumerate(places, 1) if place.path == "product/stock-notes.md"), None), places

    at, places = place_of_the_restating_passage("ranking-sentences")
    notes = line_holding(root, "product/stock-notes.md", "Whatever figure has gone into the book")
    check("a rule restated in one sentence of a longer passage stands among the first twenty places, the place given being the passage the sentence stands in",
          at is not None and at <= search.RANKED and places[at - 1].first <= notes <= places[at - 1].last, (at, places[:search.RANKED]))
    # the same search with no sentence ranked, the passages alone, shows the case is one the sentences decide
    held, search.sentences = search.sentences, lambda text: []
    try:
        alone, _ = place_of_the_restating_passage("ranking-passages-alone")
    finally:
        search.sentences = held
    check("ranked by its passage alone, with no sentence ranked, the same passage stands outside the first twenty", alone is None or alone > search.RANKED, alone)

    root = SCENARIOS / "known-copies" / "files"
    s = search.Search(root, cover=files_under(root), scratch=fresh("ranking-parts"), quiet=True)
    asked = "A fact lives in one home, and every other place that needs it cites that home."
    whole = s.meaning(asked, limit=200)
    check("a ranking read past its first places holds no place twice", len(whole.places) == 200 and len(set(whole.places)) == 200, len(whole.places))
    first = s.meaning(asked)
    check("a search asked for no part gives the first twenty places of its ranking, and its result says which part it holds",
          first.places == whole.places[:search.RANKED] and first.ranking_part() == "1 to 20" and "**Ranking Part:** 1 to 20" in first.path.read_text(encoding="utf-8"), first.ranking_part())
    for size in (20, 7, 64):
        parts = [s.meaning(asked, limit=size, start=at) for at in range(1, 201, size)]
        read = [place for part in parts for place in part.places][:200]
        check(f"parts of {size} places asked one after another make up the ranking, no place twice and none missed", read == whole.places,
              [(n, a, b) for n, (a, b) in enumerate(zip(read, whole.places), 1) if a != b][:3])
    third = s.meaning(asked, limit=20, start=41)
    check("a part further on says which places of the ranking it holds, and passes the check of a result's form",
          third.ranking_part() == "41 to 60" and search.Result.check(third.path) == [], (third.ranking_part(), search.Result.check(third.path)))
    check("a result of each part asked stands beside the others, none clearing another", first.path.exists() and third.path.exists() and first.path != third.path)
    held = third.path.read_text(encoding="utf-8")
    third.path.write_text(held.replace("**Ranking Part:** 41 to 60", "**Ranking Part:** 41 to 70"), encoding="utf-8", newline="\n")
    check("a result whose Ranking Part does not agree with the places it holds fails the check of its form", any("Ranking Part" in problem for problem in search.Result.check(third.path)), search.Result.check(third.path))
    past = s.meaning(asked, limit=20, start=100000)
    check("a part asked past the end of the ranking holds no place and says so", past.places == [] and past.ranking_part() == "none" and search.Result.check(past.path) == [], (past.places[:2], past.ranking_part()))
    try:
        s.meaning(asked, limit=0)
        refused = False
    except ValueError:
        refused = True
    check("a limit or a start that is no whole number from 1 is refused", refused)

    cited = "specs/methodology/sourcing-and-citation/one-home-per-fact.md § One Home Per Fact"
    citing = {(place.path, place.lineage) for place in s.citers(cited).places}
    whole = s.meaning(cited, limit=120)
    parts = [s.meaning(cited, limit=30, start=at) for at in (1, 31, 61, 91)]
    check("asked by a section's citation, parts asked one after another make up the ranking", [place for part in parts for place in part.places] == whole.places and len(whole.places) == 120,
          len(whole.places))
    own = [place for place in whole.places if (place.path, place.lineage) == ("specs/methodology/sourcing-and-citation/one-home-per-fact.md", "One Home Per Fact")]
    check("asked by a section's citation, no part of the ranking gives back that section", own == [], own)
    check("asked by a section's citation, no part of the ranking holds a place whose section cites it", [place for place in whole.places if (place.path, place.lineage) in citing] == [],
          [place for place in whole.places if (place.path, place.lineage) in citing][:3])
    apart = [note for note in whole.notes if isinstance(note, search.Place)]
    passages = {(path, first) for path, lineage in citing
                for (first,) in s.db.execute("select p.line_start from passages p join files f on f.sha=p.sha where f.path=? and p.lineage=?", (path, lineage))}
    check("the places whose section cites it are listed apart, whole: every passage of every citing section, and no other place",
          bool(apart) and all((place.path, place.lineage) in citing for place in apart) and {(place.path, place.first) for place in apart} >= passages and len(set(apart)) == len(apart),
          (len(apart), len(passages)))
    check("the places listed apart are the same with every part", all(part.notes == whole.notes for part in parts), [len(part.notes) for part in parts])
    by_passage = s.meaning(asked, limit=120)
    check("asked by a passage and not a citation, the search leaves nothing out and lists nothing apart",
          by_passage.notes == [] and any((place.path, place.lineage) == ("specs/methodology/sourcing-and-citation/one-home-per-fact.md", "One Home Per Fact") for place in by_passage.places),
          by_passage.notes[:2])
    s.db.close()

    # the script, over a project of its own, since it keeps its index and its results under the project it searches
    root = fresh("ranking-script-files")
    a_project(root)
    birds = ("heron", "egret", "ibis", "stork", "crane", "bittern", "spoonbill")
    put(root, "specs/birds.md", "# Birds\n\n" + "".join(f"## The {bird.title()}\n\nThe {bird} stands in the reeds at dusk and waits for the tide to turn.\n\n" for bird in birds))
    asked, cited = "A wading bird stands in the reeds at dusk and waits for the tide.", "specs/target.md § Target"
    code, out = script(root, "--show-similar-passages", asked, "--limit", "3", "--start", "2")
    check("the script gives the part of a ranking its --limit and --start ask for", code == 0 and out.count("\n  `") == 3 and "3 places, ranked" in out, out[:300])
    for wrong in (["--show-similar-passages", asked, "--limit", "0"], ["--show-similar-passages", asked, "--start", "two"], ["--show-citers", cited, "--limit", "5"]):
        code, out = script(root, *wrong)
        check(f"the script refuses {' '.join(wrong[-2:])} {'of a search that is no ranking' if wrong[0] == '--show-citers' else 'as no whole number from 1'}", code == 2 and out.startswith("usage:"), (code, out[:80]))


IN, OUT = "in the result", "not in the result"


def known_copies_suite():
    print("the known copies: a search by meaning, each pair one test")
    root = SCENARIOS / "known-copies" / "files"
    pairs = json.loads((SCENARIOS / "known-copies" / "copies.json").read_text(encoding="utf-8"))
    s = search.Search(root, cover=files_under(root), scratch=fresh("known-copies"), quiet=True)

    def line_of(place):
        text = search.strip_links((root / place["file"]).read_text(encoding="utf-8"))
        want = search.squeeze(search.strip_links(place["quote"]))
        return next(n for n, line in enumerate(text.split("\n"), 1) if want in search.squeeze(line))

    # Each pair is one test. It says whether its second place says the same as its first or only something related,
    # and, apart from that, what the search is expected to do with it: give the second place among the first twenty
    # places for the first's passage, the part a caller asking for none is given, or not. A positive test expects it
    # in the result and a negative test expects it absent, and each passes where the search does as expected.
    failed = {IN: [], OUT: []}
    count = {IN: 0, OUT: 0}
    for pair in pairs:
        oline, cline = line_of(pair["original"]), line_of(pair["copy"])
        row = s.db.execute("select p.text from passages p join files f on f.sha=p.sha where f.path=? and p.line_start<=? and p.line_end>=? order by p.id limit 1",
                           (pair["original"]["file"], oline, oline)).fetchone()
        passage = row[0] if row else search.squeeze(search.strip_links(pair["original"]["quote"]))
        result = s.meaning(passage)
        hit = any(place.path == pair["copy"]["file"] and place.first <= cline <= place.last for place in result.places)
        count[pair["expected"]] += 1
        if hit != (pair["expected"] == IN) or result.ranking_part() != f"1 to {search.RANKED}":
            failed[pair["expected"]].append(pair["record"] + ": " + pair["copy"]["quote"][:70])
    s.db.close()
    check("every pair holds one expectation, its copy in the result or not in the result", all(pair.get("expected") in (IN, OUT) and "held to" not in pair for pair in pairs))
    check(f"each of the {count[IN]} positive tests passes: the copy stands among the first twenty places", not failed[IN], failed[IN])
    check(f"each of the {count[OUT]} negative tests passes: the copy stands outside the first twenty places", not failed[OUT], failed[OUT])
    print(f"        {count[IN] - len(failed[IN])} positive tests passed, {count[OUT] - len(failed[OUT])} negative tests passed")

    # A pair whose expectation parts from what it says records a limit of the search: a place saying the same that the
    # search does not find, or a related place it gives. Only a pair the search failed before it ranked sentences may
    # record one, and each is marked. So no test that passed then is turned: a change that loses a copy the search
    # found, or lets in a related place it left out, fails that pair's test and is put right.
    def parts(pair):
        return (pair["says"] == "the same") != (pair["expected"] == IN)

    turned = [pair["record"] + ": " + pair["copy"]["quote"][:70] for pair in pairs if parts(pair) and not pair.get("once an expected failure")]
    check("a pair's expectation parts from what the pair says only where the search failed that pair before, so no passing test is turned", not turned, turned)
    marked = [pair["record"] for pair in pairs if pair.get("once an expected failure") and not parts(pair)]
    check("a pair the search now meets is marked as no limit, so it can never record one", not marked, marked)
    missed = [pair for pair in pairs if parts(pair) and pair["says"] == "the same"]
    given = [pair for pair in pairs if parts(pair) and pair["says"] != "the same"]
    print(f"        pairs recording a limit: {len(missed)} saying the same that the search does not find, {len(given)} saying something related that it gives")
    for pair in missed + given:
        print("          " + pair["record"] + ": " + pair["copy"]["quote"][:70])
    same = [pair for pair in pairs if pair["says"] == "the same"]
    check("over the whole set of known copies, at least half the places saying the same stand in the first twenty", sum(pair["expected"] == IN for pair in same) * 2 >= len(same))


def scale_suite():
    print("scale: a run after one changed file, on this project's files and on ten times as many")
    live = search.Search(PROJECT, quiet=True)
    listed = live.covered()
    live.db.close()
    times, memory = {}, {}
    for copies in (1, 10):
        # the copies stand outside the checkout, so a copy's path is no longer for the place the checkout sits in
        root, scratch = outside(f"scale-{copies}"), fresh(f"scale-{copies}")
        try:
            cover = []
            for c in range(copies):
                for rel in listed:
                    target = root / f"c{c}" / rel
                    target.parent.mkdir(parents=True, exist_ok=True)
                    # each copy holds a line of its own, so its content is the index's own to hold, and ten copies
                    # give ten times the lines, the citations and the passages
                    target.write_bytes((PROJECT / rel).read_bytes() + f"\n\nThis sentence stands in copy {c} of {rel} alone, so no two copies hold the same content.\n".encode("utf-8"))
                    cover.append(f"c{c}/{rel}")
            # the whole index is built by a process of its own, since the most memory a process held never falls
            # again and this one has run every suite before this
            listing = scratch.parent / f"scale-{copies}-cover.json"
            listing.write_text(json.dumps(cover), encoding="utf-8")
            built = subprocess.run([sys.executable, str(Path(__file__).resolve()), "--build", str(root), str(scratch), str(listing)], capture_output=True, text=True, encoding="utf-8")
            assert built.returncode == 0, built.stderr
            seconds, memory[copies] = (float(x) for x in built.stdout.split())
            print(f"        {len(cover)} files: the whole index built in {seconds:.1f} seconds, holding at most {memory[copies]:.2f} GB")
            runs = []
            for attempt in range(3):
                with open(root / "c0" / "README.md", "a", encoding="utf-8", newline="\n") as f:
                    f.write(f"\nA sentence added for run {attempt}, so this one file has changed.\n")
                started = time.perf_counter()
                s = search.Search(root, cover=cover, scratch=scratch, quiet=True)
                s.citers("c0/specs/AGENTS.md § Writing specs")
                runs.append(time.perf_counter() - started)
                assert s.read_count == 1, s.read_count
                s.db.close()
            times[copies] = min(runs)
            print(f"        {len(cover)} files: a run after one changed file took {times[copies]:.2f} seconds")
        finally:
            clear(root)
    check("on a corpus ten times the size, a run after one changed file takes no more than three times as long", times[10] <= 3 * times[1], times)
    check(f"building the whole index holds no more than {MEMORY_BOUND} GB of memory, on this project's files and on ten times as many",
          all(m <= MEMORY_BOUND for m in memory.values()), memory)


MEMORY_BOUND = 1.0  # GB: the model and its working memory, with room, whatever the count of files


def most_memory():
    """-> the most memory this process has held, in GB, as the system counts it."""
    if os.name == "nt":
        import ctypes
        from ctypes import wintypes

        class Counters(ctypes.Structure):
            _fields_ = [("cb", wintypes.DWORD), ("PageFaultCount", wintypes.DWORD)] + [(n, ctypes.c_size_t) for n in (
                "PeakWorkingSetSize", "WorkingSetSize", "QuotaPeakPagedPoolUsage", "QuotaPagedPoolUsage", "QuotaPeakNonPagedPoolUsage",
                "QuotaNonPagedPoolUsage", "PagefileUsage", "PeakPagefileUsage")]

        counters = Counters()
        counters.cb = ctypes.sizeof(counters)
        ctypes.windll.kernel32.GetCurrentProcess.restype = wintypes.HANDLE
        ctypes.windll.psapi.GetProcessMemoryInfo.argtypes = [wintypes.HANDLE, ctypes.POINTER(Counters), wintypes.DWORD]
        ctypes.windll.psapi.GetProcessMemoryInfo(ctypes.windll.kernel32.GetCurrentProcess(), ctypes.byref(counters), counters.cb)
        return counters.PeakWorkingSetSize / 2 ** 30
    import resource
    held = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    return held / (2 ** 30 if sys.platform == "darwin" else 2 ** 20)  # bytes on macOS, kilobytes elsewhere


def build(root, scratch, listing):
    """Build the whole index of the files a listing names, and print the seconds it took and the most memory held."""
    started = time.perf_counter()
    search.Search(Path(root), cover=json.loads(Path(listing).read_text(encoding="utf-8")), scratch=Path(scratch), quiet=True).db.close()
    print(f"{time.perf_counter() - started:.1f} {most_memory():.3f}")


if __name__ == "__main__":
    for stream in (sys.stdout, sys.stderr):
        stream.reconfigure(encoding="utf-8")
    try:
        search.check_requirements(PROJECT)
    except search.MissingRequirements as e:
        print(e)
        sys.exit(1)
    if sys.argv[1:2] == ["--build"]:
        build(*sys.argv[2:5])
        sys.exit(0)
    suites = [reading_suite, corpus_suite, places_suite, cited_sections_suite, targets_suite, git_cases_suite, snapshot_suite, kept_suite, names_nothing_suite, research_failures_suite,
              rerun_suite, checkout_suite, requirements_suite, ranking_suite, known_copies_suite] + ([scale_suite] if "--scale" in sys.argv else [])
    named = [a for a in sys.argv[1:] if not a.startswith("--")]
    if named:
        suites = [suite for suite in suites if suite.__name__ in named or suite.__name__[:-len("_suite")] in named]
    for suite in suites:
        suite()
    print(f"{len(FAILED)} failed" if FAILED else "every check passed")
    sys.exit(1 if FAILED else 0)
