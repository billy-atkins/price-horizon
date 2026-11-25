"""A question naming nothing to ask of: told to the caller, each case apart."""
import pytest

CORPUS_SPECS = ("search-corpus-specs.md", "forms-spec", "target-spec", "promise-product-file", "ledger-glossary")
CORPUS_CODE = ("search-corpus-code.md", "ledger-python", "ledger-typescript", "ledger-csharp", "ledger-table-sql", "ledger-settings-yaml")
HERON = ("search-heron-project.md", "heron-spec", "stack-naming-one-code-root", "heron-function", "egret-function", "design-citing-the-heron",
         "plan-citing-the-heron", "follow-ups-naming-a-heron")


@pytest.mark.action("--show-citers", "--show-lines", "--show-similar-passages", "--show-term-uses", "--show-pattern-matches")
@pytest.mark.reports
@pytest.mark.reads(*CORPUS_SPECS)
@pytest.mark.reads(*CORPUS_CODE)
def test_a_question_naming_nothing_is_told_by_its_case(fixtures, tools, search, opened, work, check):
    # the corpus holds a spec at `specs/target.md` with a section Target, no section named No Such Section, no file
    # `specs/no-such-file.md` and no folder named nowhere
    root = tools.a_corpus(work / "project", fixtures)
    s = opened(root, cover=tools.files_under(root), scratch=work / "index")
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
    check("an answer the search kept tells it as the answer computed did", again.kept and again.names_nothing == [search.NO_FILE] and tools.same_answer(again, s.terms("posting", ["specs/nowhere"])))


@pytest.mark.action("--show-citers", "--show-term-uses")
@pytest.mark.reports
@pytest.mark.reads(*HERON)
def test_the_script_says_what_a_question_named_nothing_by(fixtures, tools, search, opened, script, work, check):
    # a small project whose one spec holds a section Target, with no folder `.ai/plans/no-such-plans` and no folder
    # `specs/nowhere`
    root = tools.a_project(work / "project", fixtures)
    w = opened(root, scratch=work / "index", target=search.WORKING, paths=[".ai/plans/no-such-plans"])
    r = w.terms("heron")
    check("a search of the working files given a path holding no file is told so", r.names_nothing == [search.NO_FILE] and r.places == [], (r.names_nothing, r.places))
    ran, printed = script(root, "--show-citers", "specs/target.md § No Such Section")
    check("the script says it of a question it ran, in words of its own for each case", ran == 0 and "the question names nothing to ask of: " + search.NO_PLACE in printed, printed)
    ran, printed = script(root, "--show-term-uses", "heron", "--paths", "specs/nowhere")
    check("and of a path holding no file", ran == 0 and "the question names nothing to ask of: " + search.NO_FILE in printed, printed)
