"""The failures of a design's research the search answers for, each a test of what the search does: words that only
look alike, words standing apart, and a question asked in place of the rule's own words."""
import pytest

LENDING = ("search-library-lending.md", "library-membership", "library-loans", "library-overdue", "library-holds", "library-catalogue")
PREMISES = ("search-library-premises.md", "library-donations", "library-opening", "library-volunteers", "library-rooms", "library-events")


@pytest.mark.action("--show-term-uses")
@pytest.mark.passes
@pytest.mark.reads("search-words-apart.md", "read-again-and-read-against", "run-again-together-and-apart")
def test_a_term_is_found_as_a_phrase_and_not_where_its_words_only_look_alike_or_stand_apart(fixtures, tools, opened, work, check):
    # one file says `read against` in one sentence and `read again` in another; the other says `runs each Search
    # again`, its words apart, in one sentence and `is run again` in another
    root = work / "project"
    tools.put(root, "specs/reading.md", fixtures["read-again-and-read-against"])
    tools.put(root, "specs/running.md", fixtures["run-again-together-and-apart"])
    s = opened(root, cover=tools.files_under(root), scratch=work / "index")
    lines_of, line_holding = tools.lines_of, tools.line_holding
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


@pytest.mark.action("--show-similar-passages")
@pytest.mark.reports
@pytest.mark.reads(*LENDING)
@pytest.mark.reads(*PREMISES)
def test_a_question_does_not_find_the_rule_answering_it_and_the_rule_in_other_words_does(fixtures, tools, search, opened, work, check):
    # the library's file on loans holds, as a paragraph of one sentence, the rule that a member owing more than five
    # pounds borrows nothing until the debt is cleared; the question asked shares none of its words but `member`
    root = tools.a_library(work / "project", fixtures)
    s = opened(root, cover=tools.files_under(root), scratch=work / "index")
    loans = "specs/library/loans.md"
    rule = tools.line_holding(root, loans, "A member owing more than five pounds borrows nothing")

    def place_of_the_rule(result):
        return next((n for n, p in enumerate(result.places, 1) if p.path == loans and p.first <= rule <= p.last), None)

    r = s.meaning("When does a member lose the right to take anything out?")
    # a limit of the search, stated in its skill: asked a question, it ranks the places worded as the question is,
    # and the rule answering it, which shares almost none of its words, stands outside the first twenty
    check("a search by meaning asked when a member loses the right to borrow does not give, among its first twenty places, the rule on a member's debt: a limit the skill states",
          place_of_the_rule(r) is None and r.ranking_part() == f"1 to {search.RANKED}", [str(p) for p in r.places[:5]])
    asked = "Someone with unpaid charges above five pounds may not take anything out until they settle up."
    question, reworded = place_of_the_rule(s.meaning("When does a member lose the right to take anything out?", limit=40)), place_of_the_rule(s.meaning(asked, limit=40))
    check("asked with the rule in other words, it gives that rule among its first forty places, where the question gives it nowhere among them",
          question is None and reworded is not None, (question, reworded))
