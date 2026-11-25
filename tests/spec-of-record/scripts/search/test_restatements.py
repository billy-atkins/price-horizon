"""A search by meaning held to pairs of passages of the invented library: each pair one judgment of whether the
search, asked with the first passage, gives the second among the first twenty places of its ranking, the part a
caller asking for none is given."""
import pytest

pytestmark = [pytest.mark.reads("search-library-lending.md", "library-membership", "library-loans", "library-overdue", "library-holds", "library-catalogue"),
              pytest.mark.reads("search-library-premises.md", "library-donations", "library-opening", "library-volunteers", "library-rooms", "library-events")]

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
FOUND = 5  # of the pairs saying the same, those the search gives in the first twenty


@pytest.fixture
def library(shared, fixtures, tools):
    """-> (the library's root, a search over its ten files), written and indexed by the first test of the file."""
    def build():
        root = tools.a_library(shared.folder / "project", fixtures)
        return root, shared.opened(root, cover=tools.files_under(root), scratch=shared.folder / "index")
    return shared.once("library", build)


def place_of(root, tools, words):
    """-> (the file, the line) of the one line of the library holding the words."""
    found = [(rel, n) for rel in sorted(tools.LIBRARY.values()) for n, line in enumerate((root / rel).read_text(encoding="utf-8").split("\n"), 1) if words in line]
    assert len(found) == 1, (words, found)
    return found[0]


@pytest.mark.action("--show-similar-passages")
@pytest.mark.passes
def test_each_pair_of_passages_is_ranked_as_its_judgment_expects(library, tools, search, check):
    root, s = library
    failed, count = {IN: [], OUT: []}, {IN: 0, OUT: 0}
    for record, original, copy, says, expected, limit in PAIRS:
        (opath, oline), (cpath, cline) = place_of(root, tools, original), place_of(root, tools, copy)
        row = s.db.execute("select p.text from passages p join files f on f.sha=p.sha where f.path=? and p.line_start<=? and p.line_end>=? order by p.id limit 1", (opath, oline, oline)).fetchone()
        # a passage too short to be ranked is no passage of the index, and is asked with as its line holds it
        passage = row[0] if row else (root / opath).read_text(encoding="utf-8").split("\n")[oline - 1]
        result = s.meaning(passage)
        hit = any(place.path == cpath and place.first <= cline <= place.last for place in result.places)
        count[expected] += 1
        if hit != (expected == IN) or result.ranking_part() != f"1 to {search.RANKED}":
            failed[expected].append(record + ": " + copy)
    check("every pair holds one expectation, its second passage in the result or not in the result", all(pair[4] in (IN, OUT) and pair[3] in (SAME, RELATED) for pair in PAIRS))
    check(f"each of the {count[IN]} positive tests passes: the second passage stands among the first twenty places", not failed[IN], failed[IN])
    check(f"each of the {count[OUT]} negative tests passes: the second passage stands outside the first twenty places", not failed[OUT], failed[OUT])

    # A pair whose expectation parts from what it says records a limit of the search: a place saying the same that
    # the search does not find, or a related place it gives. Each such pair names the kind of its limit, and no other
    # pair names one, so a change that finds a restatement the search missed, or leaves out a related place it gave,
    # fails that pair's test and the pair is then judged again.
    parts = lambda pair: (pair[3] == SAME) != (pair[4] == IN)
    check("a pair's expectation parts from what the pair says only where the pair names the limit it records", not [p[0] for p in PAIRS if parts(p) and not p[5]], [p[0] for p in PAIRS if parts(p) and not p[5]])
    check("a pair the search meets names no limit, so it can never record one", not [p[0] for p in PAIRS if p[5] and not parts(p)], [p[0] for p in PAIRS if p[5] and not parts(p)])
    same = [pair for pair in PAIRS if pair[3] == SAME]
    check(f"over the whole set, {FOUND} of the {len(same)} places saying the same stand in the first twenty, the count the search gives of this text",
          sum(pair[4] == IN for pair in same) == FOUND and not failed[IN] and not failed[OUT], sum(pair[4] == IN for pair in same))


@pytest.mark.action("--show-similar-passages")
@pytest.mark.reports
def test_text_that_is_no_prose_is_never_ranked(library, tools, check):
    # the library's file on opening holds, in a fenced block alone, a notice that umbrellas are not carried between
    # the shelves; its file on holds says in a paragraph of twenty-one characters that a hold costs nothing
    root, s = library
    notice = tools.line_holding(root, "specs/library/opening.md", "Umbrellas drip in the porch stand")
    r = s.meaning("Wet umbrellas stay in the stand in the porch and are not taken among the shelves.", limit=500)
    check("a rule stated in a fenced block alone is given at no place of the whole ranking",
          len(r.places) > 100 and not any(p.path == "specs/library/opening.md" and p.first <= notice <= p.last for p in r.places), len(r.places))
    short = tools.line_holding(root, "specs/library/holds.md", "A hold costs nothing.")
    r = s.meaning("Placing a hold is free of charge.", limit=500)
    check("a paragraph shorter than the shortest passage ranked is given at no place of the whole ranking",
          len(r.places) > 100 and not any(p.path == "specs/library/holds.md" and p.first <= short <= p.last for p in r.places), len(r.places))
