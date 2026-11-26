"""A search by meaning held to pairs of passages of the invented library: each pair one judgment of whether the
search, asked with the first passage, gives the second among the first twenty places of its ranking, the part a
caller asking for none is given. The file's tests share one index of the library, built once in the file's folder."""
import pytest

from search_set import LIBRARY, READS_LIBRARY, every_file, line_holding, project, search

pytestmark = READS_LIBRARY

SAME, RELATED = "the same", "something related"
IN, OUT = "in the result", "not in the result"

# Each pair names two passages of the library by words of each, says whether the second says the same as the first
# or only something related, and, apart from that, what the search is expected to do with it. Where the expectation
# parts from what the pair says, the pair records a limit of the search and names its kind, which the search's
# skill states. The judgments were made on this text by running the search: no pair was reworded to pass, and a pair
# whose second passage stood within a few places of the twentieth either way was left out, so no pair turns on a
# place or two of a ranking.
PAIRS = (
    # (the pair, words of the first passage, words of the second, what the second says, what is expected, the limit)
    ("renewing-while-another-waits", "A loan may be renewed twice, unless another member", "Once somebody has asked for a book that is out", SAME, IN, None),
    ("locking-up", "Whoever locks up makes sure the windows", "The last volunteer to leave checks that every window", SAME, IN, None),
    ("a-card-for-its-holder", "Nobody borrows on someone else's card", "A card is for its holder alone", SAME, IN, None),
    ("due-on-a-closed-day", "When the library closes for bad weather, every due date", "Nothing falls due on a day the doors are shut", SAME, IN, None),
    ("missing-at-two-counts", "Each shelf is counted once a year against the catalogue", "A book that cannot be found at two yearly checks", SAME, IN, None),
    ("junior-fines", "No fine is charged on an item borrowed on a junior card", "Children are never asked to pay", SAME, OUT, "other words"),
    ("junior-fines", "Children are never asked to pay", "No fine is charged on an item borrowed on a junior card", SAME, OUT, "other words"),
    ("locking-up", "The last volunteer to leave checks that every window", "Whoever locks up makes sure the windows", SAME, OUT, "one sentence among several"),
    ("a-card-for-its-holder", "A card is for its holder alone", "Nobody borrows on someone else's card", SAME, OUT, "shorter than a sentence ranked"),
    ("a-hold-uncollected", "A held item is kept at the desk for seven days", "A reservation not picked up within a week", SAME, OUT, "other words"),
    ("a-booking-not-taken-up", "A booking not taken up within fifteen minutes", "If a group has not arrived a quarter of an hour", SAME, OUT, "other words"),
    ("a-booking-not-taken-up", "If a group has not arrived a quarter of an hour", "A booking not taken up within fifteen minutes", SAME, OUT, "other words"),
    ("missing-at-two-counts", "A book that cannot be found at two yearly checks", "Each shelf is counted once a year against the catalogue", SAME, OUT, "one sentence among several"),
    ("shadowing-before-the-rota", "A new volunteer works three shifts beside", "Nobody is put on the rota by themselves", SAME, OUT, "other words"),
    ("shadowing-before-the-rota", "Nobody is put on the rota by themselves", "A new volunteer works three shifts beside", SAME, OUT, "other words"),
    ("renewing-while-another-waits", "Once somebody has asked for a book that is out", "A loan may be renewed twice, unless another member", SAME, OUT, "one sentence among several"),
    ("renewed-of-a-computer-session", "A loan may be renewed twice, unless another member", "A session at a computer lasts one hour", RELATED, OUT, None),
    ("fine-of-the-weather", "No fine is charged on an item borrowed on a junior card", "In fine weather the reading-room doors", RELATED, OUT, None),
    ("queue-at-the-desk", "Holds on one item are served in the order they were placed", "On Saturday mornings the queue at the desk", RELATED, OUT, None),
    ("card-of-the-old-index", "A card is for its holder alone", "The old card index is kept in the back room", RELATED, OUT, None),
    ("lost-of-lost-property", "A member who loses an item pays the price", "Lost property left in the library", RELATED, OUT, None),
    ("booking-of-story-time", "A booking not taken up within fifteen minutes", "No booking is needed, and a family", RELATED, OUT, None),
    ("renewed-of-a-membership", "A loan may be renewed twice, unless another member", "Membership is renewed each January", RELATED, IN, "shared words"),
    ("beside-the-renewal-rule", "A loan may be renewed twice, unless another member", "A renewal is made at the desk", RELATED, IN, "beside the original"),
    ("hold-of-a-key", "A member may place a hold on any item that is out on loan", "Two volunteers hold a key to the front door", RELATED, IN, "shared words"),
    ("desk-of-the-reading-room", "A held item is kept at the desk for seven days", "A desk in the reading room is kept for a reader", RELATED, IN, "shared words"),
    ("desk-never-left-empty", "A held item is kept at the desk for seven days", "The desk is never left empty", RELATED, IN, "shared words"),
    ("counted-of-the-cash-tin", "Each shelf is counted once a year against the catalogue", "The cash tin is counted, the takings", RELATED, IN, "shared words"),
)


@pytest.fixture
def library(shared, fixtures):
    """-> a search over the library's ten files, written and indexed by the first test of the file."""
    def build():
        root = project(shared.folder / "project", fixtures, LIBRARY)
        return shared.opened(root, cover=every_file(root), scratch=shared.folder / "index")
    return shared.once("library", build)


def place_of(fixtures, words):
    """-> (the file, the line) of the one line of the library holding the words."""
    found = [(path, n) for key, path in sorted(LIBRARY.items(), key=lambda kp: kp[1])
             for n, line in enumerate(fixtures[key].split("\n"), 1) if words in line]
    assert len(found) == 1, (words, found)
    return found[0]


@pytest.mark.action("--show-similar-passages")
@pytest.mark.passes
@pytest.mark.parametrize("record, original, copy, says, expected, limit", PAIRS, ids=[f"{n:02d}-{pair[0]}" for n, pair in enumerate(PAIRS, 1)])
def test_a_pair_of_passages_is_ranked_as_its_judgment_expects(library, fixtures, record, original, copy, says, expected, limit):
    (opath, oline), (cpath, cline) = place_of(fixtures, original), place_of(fixtures, copy)
    row = library.db.execute("select p.text from passages p join files f on f.sha=p.sha where f.path=? and p.line_start<=? and p.line_end>=? order by p.id limit 1",
                             (opath, oline, oline)).fetchone()
    # a passage too short to be ranked is no passage of the index, and is asked with as its line holds it
    key = next(k for k, p in LIBRARY.items() if p == opath)
    result = library.meaning(row[0] if row else fixtures[key].split("\n")[oline - 1])
    hit = any(place.path == cpath and place.first <= cline <= place.last for place in result.places)
    assert hit == (expected == IN) and result.ranking_part() == f"1 to {search.RANKED}"


@pytest.mark.action("--show-similar-passages")
@pytest.mark.reports
@pytest.mark.parametrize("asked, key, words", [
    ("Wet umbrellas stay in the stand in the porch and are not taken among the shelves.", "library-opening", "Umbrellas drip in the porch stand"),
    ("Placing a hold is free of charge.", "library-holds", "A hold costs nothing."),
], ids=["a-rule-stated-in-a-fenced-block-alone", "a-paragraph-shorter-than-the-shortest-passage-ranked"])
def test_text_that_is_no_prose_ranked_is_given_at_no_place_of_the_whole_ranking(library, fixtures, asked, key, words):
    # the library's file on opening holds, in a fenced block alone, a notice that umbrellas are not carried between
    # the shelves; its file on holds says in a paragraph of twenty-one characters that a hold costs nothing
    line, path = line_holding(fixtures[key], words), LIBRARY[key]
    r = library.meaning(asked, limit=500)
    assert len(r.places) > 100 and not any(p.path == path and p.first <= line <= p.last for p in r.places)
