"""The check of a result's file: in the form the search writes it, its name holding the hash of its content."""
import pytest

from search_set import result_file, search

pytestmark = pytest.mark.reads("search-results.md", "result-as-the-search-wrote-it", "result-whose-place-was-changed", "cited-sections-listing",
                               "cited-sections-listing-of-the-kind-citers", "result-whose-snapshot-is-no-code", "result-holding-no-snapshot",
                               "committed-result-naming-its-last-commit", "committed-result-naming-the-commit-asked-for", "committed-result-naming-no-commit",
                               "committed-result-naming-both-commits", "current-result-naming-a-commit", "working-files-result-naming-its-paths",
                               "working-files-result-naming-no-path", "ranked-result-holding-its-part", "ranked-result-whose-part-holds-more-places",
                               "ranked-result-past-the-ranking")


@pytest.mark.action("--check-result")
@pytest.mark.passes
@pytest.mark.parametrize("key", ["result-as-the-search-wrote-it", "cited-sections-listing", "committed-result-naming-its-last-commit",
                                 "committed-result-naming-the-commit-asked-for", "working-files-result-naming-its-paths", "ranked-result-holding-its-part",
                                 "ranked-result-past-the-ranking"])
def test_a_result_as_the_search_writes_it_is_in_its_form(fixtures, work, key):
    assert search.Result.check(result_file(work, fixtures[key])) == []


@pytest.mark.action("--check-result")
@pytest.mark.reports
@pytest.mark.parametrize("key, said", [
    ("result-whose-place-was-changed", "its content was changed since the search wrote it"),
    ("cited-sections-listing-of-the-kind-citers", "a place saying what it cites, in a result that is no listing of cited sections"),
    ("result-whose-snapshot-is-no-code", "its Snapshot is `the-files-as-i-found-them`, not a snapshot code"),
    ("result-holding-no-snapshot", "it holds no Snapshot"),
    ("committed-result-naming-no-commit", "holds neither the Commit its asker named nor the Last Commit it read"),
    ("committed-result-naming-both-commits", "holds both a Commit and a Last Commit"),
    ("current-result-naming-a-commit", "it names a Commit, and its Target is not the committed files"),
    ("working-files-result-naming-no-path", "it answered over the working files and holds no Narrowed To"),
    ("ranked-result-whose-part-holds-more-places", "its Ranking Part is `41 to 70`, and it holds 2 places"),
])
def test_a_result_out_of_its_form_is_reported_for_what_it_breaks_alone(fixtures, work, key, said):
    problems = search.Result.check(result_file(work, fixtures[key]))
    assert len(problems) == 1 and said in problems[0]
