"""The answers the search keeps: given again while nothing changed, computed anew once anything did."""
import pytest

HERON = ("search-heron-project.md", "heron-spec", "stack-naming-one-code-root", "heron-function", "egret-function", "design-citing-the-heron",
         "plan-citing-the-heron", "follow-ups-naming-a-heron")


@pytest.mark.action("--show-citers", "--show-cited-sections", "--show-lines", "--show-term-uses", "--show-code-structure", "--show-pattern-matches", "--show-similar-passages")
@pytest.mark.passes
@pytest.mark.reads(*HERON)
@pytest.mark.reads("search-heron-project.md", "heron-spec-cited-in-its-own-file", "heron-class", "plan-holding-a-class-line")
def test_an_answer_is_kept_while_what_was_asked_the_files_and_the_search_stand(fixtures, tools, search, opened, monkeypatch, work, check):
    # a small project committed whole, whose spec cites its own section Target and whose code defines a class Heron
    # and a function constructing it; each variant the test writes of a fixture is that fixture with a sentence
    # added or a heading retitled
    root, scratch = tools.a_project(work / "project", fixtures), work / "index"
    cited = fixtures["heron-spec-cited-in-its-own-file"]
    tools.put(root, "specs/target.md", cited)
    tools.put(root, "code/sample.py", fixtures["heron-class"])
    tools.git(root, "init", "-q")
    tools.git(root, "add", "specs", "code")
    tools.git(root, "commit", "-q", "-m", "first")
    paths_of, same_answer = tools.paths_of, tools.same_answer

    def searched(**given):
        return opened(root, scratch=scratch, **given)

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
    other = opened(root, scratch=work / "index-fresh")
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
    s = searched(target=search.COMMITTED_OPERATIVE)
    check("and one differing in its target, an answer kept for the files as they stand being none for the committed files", not s.terms("heron").kept and s.terms("heron").kept)
    last = s.commit
    s.db.close()
    s = searched(target=search.COMMITTED_OPERATIVE, commit=last)
    check("and one differing in the commit its asker named, though it names the last commit", not s.terms("heron").kept and s.terms("heron").commit == last)
    s.db.close()

    tools.moved_in_time(root / "specs" / "target.md")
    s = searched()
    check("a file whose time of change alone moved leaves the kept answer standing", s.read_count == 1 and s.terms("heron").kept)
    s.db.close()
    tools.put(root, "specs/target.md", cited + "\nA second heron came.\n")
    s = searched()
    r = s.terms("heron")
    check("once a file of the target holds something new, every answer is computed anew and gives the new place",
          not r.kept and len([p for p in r.places if p.path == "specs/target.md"]) == 2 and not s.citers("specs/target.md § Target").kept, (r.kept, r.places))
    check("and is then kept under the code the files now take", s.terms("heron").kept)
    s.db.close()
    s = searched(target=search.COMMITTED_OPERATIVE)
    check("an answer kept for the committed files stands while no commit changed them, whatever the files as they stand came to hold", s.terms("heron").kept)
    s.db.close()

    s = searched()
    reading = search.own_reading()
    with monkeypatch.context() as another_checkout:
        another_checkout.setattr(search, "_OWN_READING", "0" * 16)   # the search's own code as another checkout holds it
        changed = s.terms("heron")
        check("once the search's own code has changed, a kept answer is not given: the answer is computed anew by the code that runs", not changed.kept)
    check("the code of the search's own reading is built from its own script and the shared modules it imports",
          search.own_reading() == reading and bool(search.SNAPSHOT.fullmatch(reading)))
    check("and an answer that other code computed is not given by this code, which computes its own and keeps it", not s.terms("heron").kept and s.terms("heron").kept)

    m, n = s.meaning("The heron stands in the reeds."), s.meaning("The heron stands in the reeds.")
    c, d = s.code_structure("constructs", "Heron"), s.code_structure("constructs", "Heron")
    check("no answer is kept of a search by meaning or of a search for constructions, each computed whenever it is asked",
          not (m.kept or n.kept or c.kept or d.kept) and paths_of(c) == ["code/sample.py"], (m.kept, n.kept, c.kept, d.kept, c.places))
    s.db.close()
    tools.put(root, ".ai/plans/other-plan.md", fixtures["plan-holding-a-class-line"])
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
    tools.put(root, "specs/target.md", fixtures["heron-spec"].replace("## Target", "## Retitled"))
    s = searched(target=search.WORKING, paths=[".ai/plans/design-specs"])
    w = s.citers("specs/target.md § Target")
    check("and also under the code of the operative files as they stand, which it reads what its places cite against: an operative file changed, it is computed anew, no working file having changed",
          s.read_count == 1 and not w.kept and any("does not resolve" in n for n in w.notes), (s.read_count, w.kept, w.notes))
