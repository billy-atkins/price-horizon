"""A ranking by meaning: a sentence restated in a longer passage, and a ranking read in parts."""
import pytest

LENDING = ("search-library-lending.md", "library-membership", "library-loans", "library-overdue", "library-holds", "library-catalogue")
PREMISES = ("search-library-premises.md", "library-donations", "library-opening", "library-volunteers", "library-rooms", "library-events")
HERON = ("search-heron-project.md", "heron-spec", "stack-naming-one-code-root", "heron-function", "egret-function", "design-citing-the-heron",
         "plan-citing-the-heron", "follow-ups-naming-a-heron")
WADING = "A wading bird stands in the reeds at dusk and waits for the tide."


@pytest.mark.action("--show-similar-passages")
@pytest.mark.passes
@pytest.mark.reads("search-restated-sentence.md", "stocktake-rule-and-counts", "warehouse-notes")
def test_a_rule_restated_in_one_sentence_of_a_longer_passage_is_ranked_by_that_sentence(fixtures, tools, search, opened, monkeypatch, work, check):
    # one file holds a rule on counts and more than twenty short statements sharing its words; the other holds one
    # long paragraph on other subjects, one sentence of which restates the rule in other words
    root = work / "project"
    tools.put(root, "product/stocktake.md", fixtures["stocktake-rule-and-counts"])
    tools.put(root, "product/stock-notes.md", fixtures["warehouse-notes"])
    rule = fixtures["stocktake-rule-and-counts"].split("## The Rule")[1].split("##")[0].strip()

    def place_of_the_restating_passage(name):
        s = opened(root, cover=tools.files_under(root), scratch=work / name)
        places = s.meaning(rule, limit=100).places
        s.db.close()
        return next((n for n, place in enumerate(places, 1) if place.path == "product/stock-notes.md"), None), places

    at, places = place_of_the_restating_passage("index-sentences")
    notes = tools.line_holding(root, "product/stock-notes.md", "Whatever figure has gone into the book")
    check("a rule restated in one sentence of a longer passage stands among the first twenty places, the place given being the passage the sentence stands in",
          at is not None and at <= search.RANKED and places[at - 1].first <= notes <= places[at - 1].last, (at, places[:search.RANKED]))
    # the same search with no sentence ranked, the passages alone, shows the case is one the sentences decide
    monkeypatch.setattr(search, "sentences", lambda text: [])
    alone, _ = place_of_the_restating_passage("index-passages-alone")
    check("ranked by its passage alone, with no sentence ranked, the same passage stands outside the first twenty", alone is None or alone > search.RANKED, alone)


@pytest.mark.action("--show-similar-passages", "--show-citers", "--check-result")
@pytest.mark.passes
@pytest.mark.reads(*LENDING)
@pytest.mark.reads(*PREMISES)
def test_parts_of_a_ranking_asked_one_after_another_make_up_the_one_ranking(fixtures, tools, search, opened, work, check):
    # the library's ten files hold well over a hundred passages; its section on renewals is cited from three other
    # sections, of the files on overdue items, on holds and on rooms; the passage asked restates that section's rule
    root = tools.a_library(work / "project", fixtures)
    s = opened(root, cover=tools.files_under(root), scratch=work / "index")
    asked = "A book that is out on loan may be kept longer only when no one else has asked for it."
    whole = s.meaning(asked, limit=100)
    check("a ranking read past its first places holds no place twice", len(whole.places) == 100 and len(set(whole.places)) == 100, len(whole.places))
    first = s.meaning(asked)
    check("a search asked for no part gives the first twenty places of its ranking, and its result says which part it holds",
          first.places == whole.places[:search.RANKED] and first.ranking_part() == "1 to 20" and "**Ranking Part:** 1 to 20" in first.path.read_text(encoding="utf-8"), first.ranking_part())
    for size in (20, 7, 64):
        parts = [s.meaning(asked, limit=size, start=at) for at in range(1, 101, size)]
        read = [place for part in parts for place in part.places][:100]
        check(f"parts of {size} places asked one after another make up the ranking, no place twice and none missed", read == whole.places,
              [(n, a, b) for n, (a, b) in enumerate(zip(read, whole.places), 1) if a != b][:3])
    third = s.meaning(asked, limit=20, start=41)
    check("a part further on says which places of the ranking it holds, and passes the check of a result's form",
          third.ranking_part() == "41 to 60" and search.Result.check(third.path) == [], (third.ranking_part(), search.Result.check(third.path)))
    check("a result of each part asked stands beside the others, none clearing another", first.path.exists() and third.path.exists() and first.path != third.path)
    # the test's variant of a result: a part's result saying it holds more places than it does
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

    renewals = ("specs/library/loans.md", "Renewals")
    cited = "specs/library/loans.md § Renewals"
    citing = {(place.path, place.lineage) for place in s.citers(cited).places}
    whole = s.meaning(cited, limit=80)
    parts = [s.meaning(cited, limit=20, start=at) for at in (1, 21, 41, 61)]
    check("asked by a section's citation, parts asked one after another make up the ranking", [place for part in parts for place in part.places] == whole.places and len(whole.places) == 80,
          len(whole.places))
    own = [place for place in whole.places if (place.path, place.lineage) == renewals]
    check("asked by a section's citation, no part of the ranking gives back that section", own == [], own)
    check("asked by a section's citation, no part of the ranking holds a place whose section cites it", len(citing) == 3 and [place for place in whole.places if (place.path, place.lineage) in citing] == [],
          (sorted(citing), [place for place in whole.places if (place.path, place.lineage) in citing][:3]))
    apart = [note for note in whole.notes if isinstance(note, search.Place)]
    passages = {(path, first) for path, lineage in citing
                for (first,) in s.db.execute("select p.line_start from passages p join files f on f.sha=p.sha where f.path=? and p.lineage=?", (path, lineage))}
    check("the places whose section cites it are listed apart, whole: every passage of every citing section, and no other place",
          bool(apart) and all((place.path, place.lineage) in citing for place in apart) and {(place.path, place.first) for place in apart} >= passages and len(set(apart)) == len(apart),
          (len(apart), len(passages)))
    check("the places listed apart are the same with every part", all(part.notes == whole.notes for part in parts), [len(part.notes) for part in parts])
    by_passage = s.meaning(asked, limit=120)
    check("asked by a passage and not a citation, the search leaves nothing out and lists nothing apart",
          by_passage.notes == [] and any((place.path, place.lineage) == renewals for place in by_passage.places),
          by_passage.notes[:2])


@pytest.mark.action("--show-similar-passages")
@pytest.mark.passes
@pytest.mark.reads(*HERON)
@pytest.mark.reads("search-heron-project.md", "seven-wading-birds")
def test_the_script_gives_the_part_of_a_ranking_its_limit_and_start_ask_for(fixtures, tools, script, work, check):
    # a small project with one spec more, of seven sections each one sentence about a wading bird at dusk, so a
    # ranking for a sentence about a wading bird holds more than four places
    root = tools.a_project(work / "project", fixtures)
    tools.put(root, "specs/birds.md", fixtures["seven-wading-birds"])
    code, out = script(root, "--show-similar-passages", WADING, "--limit", "3", "--start", "2")
    check("the script gives the part of a ranking its --limit and --start ask for", code == 0 and out.count("\n  `") == 3 and "3 places, ranked" in out, out[:300])


@pytest.mark.action("--show-similar-passages", "--show-citers")
@pytest.mark.reports
@pytest.mark.reads(*HERON)
def test_the_script_refuses_a_part_that_is_no_whole_number_or_is_asked_of_no_ranking(fixtures, tools, script, work, check):
    root = tools.a_project(work / "project", fixtures)
    cited = "specs/target.md § Target"
    for wrong in (["--show-similar-passages", WADING, "--limit", "0"], ["--show-similar-passages", WADING, "--start", "two"], ["--show-citers", cited, "--limit", "5"]):
        code, out = script(root, *wrong)
        check(f"the script refuses {' '.join(wrong[-2:])} {'of a search that is no ranking' if wrong[0] == '--show-citers' else 'as no whole number from 1'}", code == 2 and out.startswith("usage:"), (code, out[:80]))
    check("and a run it refuses writes nothing in the project", not (root / ".ai" / "tmp").exists(), list((root / ".ai").rglob("*")))
