"""Each kind of search over the corpus of forms: two specs, a product file, a glossary and code in five languages,
which hold faults on purpose, a doubled space in a citation, a heading path standing twice and headings inside fenced
blocks among them. The file's tests share one index of the corpus, built once in the file's folder."""
import pytest

pytestmark = [pytest.mark.reads("search-corpus-specs.md", "forms-spec", "target-spec", "promise-product-file", "ledger-glossary"),
              pytest.mark.reads("search-corpus-code.md", "ledger-python", "ledger-typescript", "ledger-csharp", "ledger-table-sql", "ledger-settings-yaml")]
FORMS = "specs/forms.md"
# an annotation line of a fixture, its tag written in two parts so this file's own line reads as no annotation
ANNOTATED = "# @canon" "-spec specs/target.md § Target"


@pytest.fixture
def corpus(shared, fixtures, tools):
    """-> (the corpus's root, a search over every file of it), written and indexed by the first test of the file."""
    def build():
        root = tools.a_corpus(shared.folder / "project", fixtures)
        return root, shared.opened(root, cover=tools.files_under(root), scratch=shared.folder / "index")
    return shared.once("corpus", build)


def test_a_heading_inside_a_fenced_block_is_no_heading_of_its_file(corpus, check):
    # the forms spec writes headings inside a tilde fence, a fence indented in a list item and a fence nested in a
    # longer one; its own headings are the eight named here, the path Twice standing twice
    root, s = corpus
    heads = [r[0] for r in s.db.execute("select h.lineage from files f join headings h on h.sha=f.sha where f.path=? and h.lineage != '' order by h.line", (FORMS,))]
    check("a heading in a tilde fence, an indented fence or a nested fence is no heading of its file",
          heads == ["Citations", "Fences", "After The Fences", "Twice", "Twice", "Terms", "Where A Place Stands", "Where A Place Stands § A Heading Holding Quillwort"], heads)


@pytest.mark.action("--show-citers")
@pytest.mark.passes
def test_citers_lists_every_place_citing_a_section_in_whatever_form(corpus, tools, search, check):
    # the forms spec cites the target spec's section Target plainly, with a doubled space, across two lines, with a
    # link, inside a tilde fence, inside a backtick fence and as a fenced annotation; the code annotates it in
    # Python, TypeScript and YAML; one mention of it stands outside any code span, which is no citation
    root, s = corpus
    at = lambda words: tools.line_holding(root, FORMS, words)
    r = s.citers("specs/target.md § Target")
    got = tools.lines_of(r.places)
    want = {(FORMS, at(w)) for w in ("A plain citation", "a doubled space", "broken across lines", "carrying its link")}
    want.add((FORMS, at("## Not A Heading In Tildes") + 1))
    want.add((FORMS, at("The span: `specs/target.md § Target`")))
    want |= {(FORMS, at(ANNOTATED)), ("code/sample.py", 11), ("code/sample.ts", 7), ("code/settings.yaml", 1)}
    check("every place citing a section is listed: plain, loose white space, broken across lines, linked, fenced, and each annotation", got == want, sorted(got ^ want))
    check("a mention outside a code span and a same-file citation inside a fenced markdown block are no citers",
          (FORMS, at("A mention that is no citation")) not in got and (FORMS, at("A same-file citation of the block")) not in got)
    notes = "\n".join(r.notes)
    check("a citing place in a fenced block says so, in a tilde fence, in a backtick fence and as an annotation, and no other does",
          sorted(p.first for p in r.places if p.stands == "fenced block") == sorted([at(w) for w in ("The span: `specs/target.md § Target`", ANNOTATED)]
                                                                               + [at("## Not A Heading In Tildes") + 1])
          and all(p.endswith(", in a fenced block") == (p.stands == "fenced block") for p in r.places), r.places)
    bare = at("Do the work as specs/target.md")
    check("a citation written bare in a fenced block is read to the heading it names",
          any(n.startswith(f"`specs/forms.md § Fences` line {bare}, in a fenced block: cites a section within it, as `specs/target.md § Target § Child`") for n in r.notes), notes)
    part = s.citers("specs/target.md § Target [Name: first-record]")
    check("a keyed part's citers are listed, with the places citing the section holding it told apart",
          tools.lines_of(part.places) == {(FORMS, at("A citation of a part of it"))} and sum(": cites the section holding it" in n for n in part.notes) >= 5, (part.places, part.notes))
    check("an annotation is given with the unit it stands over", "an annotation over the unit `Ledger`" in notes, notes)
    check("a place citing a section within it, a part of it or its file is told apart",
          "cites a section within it" in notes and "cites a part of it, `[Name: first-record]`" in notes and "cites its file" in notes, notes)
    check("the same search gives the same list and the same file's name", s.citers("specs/target.md § Target").name == r.name)
    check("a citation asked for with loose white space is the same citation", tools.lines_of(s.citers("specs/target.md  §   Target").places) == got)

    r = s.citers("specs/target.md")
    check("a technical-specs entry is listed with its file's citers, marked as a label",
          ("product/promise.md", 3) in tools.lines_of(r.places) and "a `technical-specs` label, not a citation" in "\n".join(r.notes), r.notes)

    r = s.citers("specs/target.md § Table")
    after = at("A citation after every fenced block")
    check("a citation after a fenced block is placed at its own line and under its own section, and is not marked as fenced",
          f"`specs/forms.md § After The Fences` line {after}" in r.places and not any(n.startswith(f"`specs/forms.md § After The Fences` line {after}:") for n in r.notes), (r.places, r.notes))
    check("an annotation in a language with no parser is still a citer", ("code/schema.sql", 1) in tools.lines_of(r.places) and ("code/sample.py", 3) in tools.lines_of(r.places), r.places)
    r = s.citers("specs/target.md § Target", ["code"])
    check("a search narrowed to a folder lists no place outside it", {p for p, _ in tools.lines_of(r.places)} == {"code/sample.py", "code/sample.ts", "code/settings.yaml"}, r.places)


@pytest.mark.action("--show-lines")
@pytest.mark.passes
def test_lines_gives_the_lines_a_citation_names(corpus, check):
    # the target spec holds text before its first section at lines 1-4, the section Target at 5-15 with a record at
    # 13-14, its child at 16-19, and a table whose row for the state closed stands at line 27
    root, s = corpus
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


@pytest.mark.action("--show-lines")
@pytest.mark.reports
def test_lines_reports_a_citation_that_does_not_resolve(corpus, check):
    # the target spec holds no section named Missing
    root, s = corpus
    r = s.lines("specs/target.md § Missing")
    check("a citation that does not resolve is reported with why", not r.places and "holds no section `Missing`" in r.notes[0], r.notes)


@pytest.mark.action("--show-lines", "--show-term-uses", "--show-pattern-matches", "--show-citers")
@pytest.mark.passes
def test_a_path_two_headings_share_is_cited_by_the_path_and_the_result_says_so(corpus, tools, check):
    # two headings of the forms spec share the path Twice: the index holds what both hold, a citation of the path
    # names it all together, and every result giving a place under either says the path stands more than once and
    # where, so its reader reads each. Each of the two holds a sentence of its own, a citation and one record
    root, s = corpus
    at = lambda words: tools.line_holding(root, FORMS, words)
    twice = [n for n, line in enumerate((root / FORMS).read_text(encoding="utf-8").split("\n"), 1) if line == "## Twice"]
    first, second = at("The first section"), at("The second section")
    said = f"the path `Twice` stands more than once in the file, 2 times, at lines {twice[0]}, {twice[1]}"
    r = s.lines("specs/forms.md § Twice")
    check("a citation of a path two headings share gives the lines of both, and the result says how many times the path stands and where",
          r.places == [f"`specs/forms.md § Twice` lines {twice[0]}-{twice[1] - 1}", f"`specs/forms.md § Twice` lines {twice[1]}-{at('## Terms') - 1}"]
          and any(said in n for n in r.notes), (r.places, r.notes))
    for kind, find in (("a term's use", s.terms), ("a pattern's match", s.pattern)):
        for which, words, line in (("first", "first section of this path", first), ("second", "second section of this path", second)):
            r = find(words)
            check(f"{kind} under the {which} of two headings sharing a path is cited by the path with its own line, and the result notes the path",
                  [str(p) for p in r.places] == [f"`specs/forms.md § Twice` line {line}"] and any(said in n for n in r.notes), (r.places, r.notes))
    wick, ferry = at("trims the lamp wick"), at("ferry across the estuary")
    r = s.citers("specs/forms.md § Terms")
    check("a citation under each of the two is found, each cited by the path with its own line",
          {f"`specs/forms.md § Twice` line {wick}", f"`specs/forms.md § Twice` line {ferry}"} <= set(r.places) and any(said in n for n in r.notes), (r.places, r.notes))
    for which, name in (("first", "lamp-first"), ("second", "lamp-second")):
        line = at(f"**Name:** {name}")
        r = s.lines(f"specs/forms.md § Twice [Name: {name}]")
        check(f"a keyed part under the {which} of them is given by its citation", r.places == [f"`specs/forms.md § Twice [Name: {name}]` lines {line}-{line + 1}"], (r.places, r.notes))
        r = s.terms(name)
        check("and a term's use within it is cited by that keyed part", [str(p) for p in r.places] == [f"`specs/forms.md § Twice [Name: {name}]` line {line}"], r.places)


@pytest.mark.action("--show-term-uses")
@pytest.mark.passes
def test_terms_finds_a_term_in_every_form_it_takes(corpus, tools, check):
    # the forms spec writes the term append entry as a function's name, a flag, a class's name, a plural and a
    # phrase broken across two lines, and once with its words standing apart; the code calls and defines it in three
    # languages; the glossary gives ledger entry the abbreviation LE and the other name journal line
    root, s = corpus
    at = lambda words: tools.line_holding(root, FORMS, words)
    r = s.terms("append entry")
    got = tools.lines_of(r.places)
    want = {(FORMS, at(w)) for w in ("function append_entry", "flag --append-entry", "class AppendEntry", "appending entries", "the clerk will append")}
    want |= {("code/sample.py", 19), ("code/sample.py", 27), ("code/sample.ts", 12), ("code/sample.ts", 18), ("code/sample.cs", 12), ("code/sample.cs", 15)}
    check("a term is found in every form it takes, in a spec and in code, and where its words only stand apart it is not", got == want, sorted(got ^ want))
    r = s.terms("ledger entry")
    got = tools.lines_of(r.places)
    check("a term is found under each other name the glossary gives it, and the result names the forms searched",
          (FORMS, at("The LE is posted once")) in got and ("specs/target.md", 7) in got and "`LE`" in r.run_as and "`journal line`" in r.run_as, (sorted(got), r.run_as))


@pytest.mark.action("--show-pattern-matches")
@pytest.mark.passes
def test_pattern_lists_every_place_an_expression_matches(corpus, tools, check):
    # one citation of the forms spec holds a doubled space, one carries a link and one breaks across two lines
    root, s = corpus
    at = lambda words: tools.line_holding(root, FORMS, words)
    r = s.pattern("§  +")
    check("a pattern lists every place it matches, and only those", tools.lines_of(r.places) == {(FORMS, at("a doubled space"))}, r.places)
    r = s.pattern(r"\]\(/specs/target\.md#target\)")
    check("a pattern reads a file's text as written, a citation's link among it", tools.lines_of(r.places) == {(FORMS, at("carrying its link"))}, r.places)
    r = s.pattern(r"§\nTarget")
    check("a pattern matches across lines, over a file's whole text", tools.lines_of(r.places) == {(FORMS, at("broken across lines"))}, r.places)


@pytest.mark.action("--show-code-structure")
@pytest.mark.passes
def test_code_structure_lists_the_units_holding_a_structure_in_each_language(corpus, check):
    # each of the three samples of code holds a class Ledger that extends Base, a method that constructs a Receipt
    # and calls the function appending an entry, and the same names inside a string and a comment; the YAML and the
    # SQL hold no units
    root, s = corpus

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


@pytest.mark.action("--check-result")
@pytest.mark.passes
def test_a_result_as_the_search_wrote_it_is_in_its_form_under_a_name_every_system_holds(corpus, search, check):
    root, s = corpus
    r = s.citers("specs/target.md § Table")
    check("a result's file holds its own name, says its places are places to read and whether they are every place",
          r.path.read_text(encoding="utf-8").count(r.name) == 1 and "places to read, never findings" in r.path.read_text(encoding="utf-8") and "**Completeness:** complete" in r.path.read_text(encoding="utf-8"))
    long = s.terms("append entry " + "and a very long question holding a section sign § brackets [ ] and slashes / \\ " * 6)
    check("a result's name is one every system holds", len(long.name) <= search.MAX_NAME and set(long.name) <= set("abcdefghijklmnopqrstuvwxyz0123456789-."), long.name)
    r = s.citers("specs/target.md § Target", ["code"])
    check("a result as the search wrote it passes the check of its form", search.Result.check(r.path) == [], search.Result.check(r.path))


@pytest.mark.action("--check-result")
@pytest.mark.reports
def test_a_result_whose_content_was_changed_no_longer_gives_the_hash_in_its_name(corpus, search, check):
    # the test's variant of a result: one the search wrote, with a place added to it by hand under the same name
    root, s = corpus
    r = s.pattern("retries")
    r.path.write_text(r.path.read_text(encoding="utf-8") + "      - `code/sample.py` line 1\n", encoding="utf-8", newline="\n")
    check("a result whose content was changed no longer gives the hash in its name", any("its content was changed" in p for p in search.Result.check(r.path)), search.Result.check(r.path))


@pytest.mark.action("--show-similar-passages")
@pytest.mark.passes
def test_meaning_ranks_a_place_saying_the_same_in_other_words(corpus, tools, check):
    # the product file says each posting is written exactly one time, which the passage asked says in other words;
    # the forms spec's section Citations cites the target spec's section Target; each of the two sections sharing
    # the path Twice holds one sentence, on a lighthouse keeper's lamp and on a ferry's passengers
    root, s = corpus
    r = s.meaning("specs/target.md § Target")
    check("a place whose section cites the passage's own section is listed apart from the ranking",
          not any(p.startswith("`specs/forms.md § Citations`") for p in r.places) and any(n.startswith("`specs/forms.md § Citations`") for n in r.notes), (r.places, r.notes))
    r = s.meaning("Every posting is recorded a single time and never twice.")
    check("a search by meaning ranks a place saying the same in other words, and says its places are the first of a ranking",
          r.completeness == "ranked" and any(p.startswith("`product/promise.md § What Is Promised`") for p in r.places[:3]), r.places[:5])
    ferry, wick = tools.line_holding(root, FORMS, "ferry across the estuary"), tools.line_holding(root, FORMS, "trims the lamp wick")
    r = s.meaning("A boat crossing the river mouth takes at most forty people while the high spring tide runs.")
    check("a search by meaning gives a passage under the second of two headings sharing a path, cited by the path with its own lines, and notes the path",
          f"`specs/forms.md § Twice` line {ferry}" in r.places[:5] and any("the path `Twice` stands more than once in the file, 2 times" in n for n in r.notes), (r.places[:5], r.notes))
    r = s.meaning("Each evening before dark the lighthouse keeper cuts back the wick of the lamp.")
    check("and a passage under the first of them", f"`specs/forms.md § Twice` line {wick}" in r.places[:5], r.places[:5])
    r = s.meaning("specs/forms.md § Twice", limit=200)
    check("asked by the path's citation, a search by meaning takes what both sections hold as what it was given, and gives back a passage of neither",
          bool(r.places) and not any(p.startswith("`specs/forms.md § Twice`") for p in r.places), (r.places[:5], r.notes))
