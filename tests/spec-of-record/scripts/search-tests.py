#!/usr/bin/env python3
"""The tests of the search in .ai/skills/lib/search.py, run over the scenarios in tests/spec-of-record/scenarios/search/.

  search-tests.py            every suite but the one on scale
  search-tests.py --scale    the suite on scale too, which copies the project's files ten times over and takes minutes

Each suite builds an index of its own under .ai/tmp/search-spec-of-record-scope/tests/, cleared as the suite starts. A
suite prints each check it makes, and the run exits 1 where any failed. The scenarios hold faults on purpose: a doubled
space in a citation, a heading path standing twice, a heading inside a fenced block.
"""
import json
import shutil
import sys
import time
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve()
PROJECT = HERE.parents[3]
SCENARIOS = HERE.parents[1] / "scenarios" / "search"
sys.path.insert(0, str(PROJECT / ".ai" / "skills" / "lib"))
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
    out = set()
    for place in places:
        cite, _, where = place.rpartition("` ")
        path = cite.strip("`").split(" § ")[0]
        out.add((path, int(where.split(" ")[1].split("-")[0])))
    return out


def line_holding(root, path, words):
    for n, line in enumerate((root / path).read_text(encoding="utf-8").split("\n"), 1):
        if words in line:
            return n
    raise AssertionError(f"{path} holds no line with: {words}")


def corpus_suite():
    print("the corpus: reading, citers, lines, terms, code, pattern and the result's file")
    root = SCENARIOS / "corpus"
    s = search.Search(root, cover=files_under(root), scratch=fresh("corpus"), quiet=True)
    forms = "specs/forms.md"

    heads = [r[0] for r in s.db.execute("select h.lineage from files f join headings h on h.sha=f.sha where f.path=? and h.lineage != '' order by h.line", (forms,))]
    check("a heading in a tilde fence, an indented fence or a nested fence is no heading of its file",
          heads == ["Citations", "Fences", "After The Fences", "Twice", "Twice", "Terms"], heads)

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
    check("a citation in a fenced block is marked, in a tilde fence, in a backtick fence and as an annotation", sum("stands in a fenced block" in n and ": cites " not in n for n in r.notes) == 3, notes)
    bare = line_holding(root, forms, "Do the work as specs/target.md")
    check("a citation written bare in a fenced block is read to the heading it names",
          any(n.startswith(f"`specs/forms.md § Fences` line {bare}: cites a section within it, stands in a fenced block, as `specs/target.md § Target § Child`") for n in r.notes), notes)
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
    check("a keyed citation gives its table's row", r.places == ["`specs/target.md § Table [States.State: closed]` line 27"], r.places)
    r = s.lines("specs/forms.md § Twice")
    check("of two headings sharing a path the first is the one a citation names, and the result says so",
          r.places == [f"`specs/forms.md § Twice` lines {line_holding(root, forms, '## Twice')}-{line_holding(root, forms, 'The first section') + 1}"] and "stands 2 times" in r.notes[0], (r.places, r.notes))
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


def known_copies_suite():
    print("the known copies: a search by meaning")
    root = SCENARIOS / "known-copies" / "files"
    pairs = json.loads((SCENARIOS / "known-copies" / "copies.json").read_text(encoding="utf-8"))
    s = search.Search(root, cover=files_under(root), scratch=fresh("known-copies"), quiet=True)

    def line_of(place):
        text = search.strip_links((root / place["file"]).read_text(encoding="utf-8"))
        want = search.squeeze(search.strip_links(place["quote"]))
        return next(n for n, line in enumerate(text.split("\n"), 1) if want in search.squeeze(line))

    # each pair says whether its second place says the same as its first or only something related, and what the
    # search is held to for it: found or a known gap, kept out or a known intrusion
    got = {held: [] for held in ("found", "a known gap", "kept out", "a known intrusion")}
    for pair in pairs:
        oline, cline = line_of(pair["original"]), line_of(pair["copy"])
        row = s.db.execute("select p.text from passages p join files f on f.sha=p.sha where f.path=? and p.line_start<=? and p.line_end>=? order by p.id limit 1",
                           (pair["original"]["file"], oline, oline)).fetchone()
        passage = row[0] if row else search.squeeze(search.strip_links(pair["original"]["quote"]))
        hit = False
        for place in s.meaning(passage).places:
            cite, _, where = place.rpartition("` ")
            span = where.split(" ")[1].split("-")
            if cite.strip("`").split(" § ")[0] == pair["copy"]["file"] and int(span[0]) <= cline <= int(span[-1]):
                hit = True
        got[pair["held to"]].append((hit, pair["record"] + ": " + pair["copy"]["quote"][:70]))

    def hits(held):
        return sum(hit for hit, _ in got[held])

    def named(held, want):
        return [name for hit, name in got[held] if hit == want]

    same = len(got["found"]) + len(got["a known gap"])
    in_first = hits("found") + hits("a known gap")
    print(f"        places saying the same: {in_first} of {same} stand in the first {search.RANKED} results for their own original passage")
    check("over the whole set of known copies, at least half stand in the first twenty results for their own original passage", in_first * 2 >= same)
    check(f"each of the {len(got['found'])} copies the search is held to finding is found", hits("found") == len(got["found"]), named("found", False))
    check(f"each of the {len(got['kept out'])} related places the search is held to keeping out of the first twenty is kept out", hits("kept out") == 0, named("kept out", True))
    print(f"        known gaps, places saying the same that are not yet found: {len(got['a known gap']) - hits('a known gap')} of {len(got['a known gap'])}")
    for name in named("a known gap", False):
        print("          " + name)
    print(f"        known intrusions, related places that still stand in the first twenty: {hits('a known intrusion')} of {len(got['a known intrusion'])}")
    for name in named("a known intrusion", True):
        print("          " + name)
    moved = named("a known gap", True) + named("a known intrusion", False)
    if moved:
        print("        now better than its label says, so the set's labels can be brought up to date:")
        for name in moved:
            print("          " + name)


def scale_suite():
    print("scale: a run after one changed file, on this project's files and on ten times as many")
    live = search.Search(PROJECT, quiet=True)
    listed = live.covered()
    live.db.close()
    times = {}
    for copies in (1, 10):
        root, scratch = fresh(f"scale-{copies}-files"), fresh(f"scale-{copies}")
        cover = []
        for c in range(copies):
            for rel in listed:
                target = root / f"c{c}" / rel
                target.parent.mkdir(parents=True, exist_ok=True)
                # each copy holds a line of its own, so its content is the index's own to hold, and ten copies give
                # ten times the lines, the citations and the passages
                target.write_bytes((PROJECT / rel).read_bytes() + f"\n\nThis sentence stands in copy {c} of {rel} alone, so no two copies hold the same content.\n".encode("utf-8"))
                cover.append(f"c{c}/{rel}")
        started = time.perf_counter()
        search.Search(root, cover=cover, scratch=scratch, quiet=True).db.close()
        print(f"        {len(cover)} files: the whole index built in {time.perf_counter() - started:.1f} seconds")
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
    check("on a corpus ten times the size, a run after one changed file takes no more than three times as long", times[10] <= 3 * times[1], times)


if __name__ == "__main__":
    for stream in (sys.stdout, sys.stderr):
        stream.reconfigure(encoding="utf-8")
    try:
        search.check_requirements(PROJECT)
    except search.MissingRequirements as e:
        print(e)
        sys.exit(1)
    suites = [corpus_suite, rerun_suite, requirements_suite, known_copies_suite] + ([scale_suite] if "--scale" in sys.argv else [])
    for suite in suites:
        suite()
    print(f"{len(FAILED)} failed" if FAILED else "every check passed")
    sys.exit(1 if FAILED else 0)
