"""The snapshot code: the state of a target's files, on every result and on request."""
import pytest

HERON = ("search-heron-project.md", "heron-spec", "stack-naming-one-code-root", "heron-function", "egret-function", "design-citing-the-heron",
         "plan-citing-the-heron", "follow-ups-naming-a-heron")


@pytest.mark.action("--show-snapshot-code", "--show-term-uses", "--show-citers")
@pytest.mark.passes
@pytest.mark.reads(*HERON)
def test_one_code_stands_for_the_files_of_a_target_and_changes_only_as_they_do(fixtures, tools, search, opened, script, work, check):
    # a small project committed whole, so the files as they stand and the files the last commit held hold the same
    # until the test changes one; each variant the test writes of a fixture is that fixture with a few words changed
    root, scratch = tools.a_project(work / "project", fixtures), work / "index"
    tools.git(root, "init", "-q")
    tools.git(root, "add", "specs", "code")
    tools.git(root, "commit", "-q", "-m", "first")
    spec, changed = fixtures["heron-spec"], tools.changed

    def searched(**given):
        return opened(root, scratch=scratch, **given)

    s = searched()
    r, narrow, cite = s.terms("heron"), s.terms("heron", ["specs"]), s.citers("specs/target.md § Target")
    code = r.snapshot
    check("every result carries a snapshot code, sixteen hexadecimal digits, which its file holds, and passes the check of a result's form",
          bool(search.SNAPSHOT.fullmatch(code or "")) and f"**Snapshot:** {code} \\" in r.path.read_text(encoding="utf-8") and search.Result.check(r.path) == [], (code, search.Result.check(r.path)))
    check("one code stands for the whole target, whatever a search was narrowed to and whatever its kind", narrow.snapshot == code == cite.snapshot and narrow.narrowed == ["specs"], (code, narrow.snapshot, cite.snapshot))
    check("a result whose Snapshot is not in a code's form fails the check of its form",
          any("not a snapshot code" in p for p in changed(r.path, f"**Snapshot:** {code}", "**Snapshot:** the-files-as-i-found-them")), changed(r.path, f"**Snapshot:** {code}", "**Snapshot:** the-files-as-i-found-them"))
    check("and one holding none fails it", any("holds no Snapshot" in p for p in changed(r.path, f"    **Snapshot:** {code} \\\n", "")))
    s.db.close()
    check("the search gives the present code on request, equal to a result's while no file of the target holds anything new", search.snapshot(root, scratch=scratch) == code, search.snapshot(root, scratch=scratch))
    ran, printed = script(root, "--show-snapshot-code")
    check("the script gives it too, from an index of its own, the code built from the files and never from an index", ran == 0 and code in printed.split("\n"), (ran, printed))
    s = searched(target=search.COMMITTED_OPERATIVE)
    check("the code is built one way whatever the target: the files the last commit held take the code the files as they stand take, each file holding the same",
          s.terms("heron").snapshot == code and search.snapshot(root, target=search.COMMITTED_OPERATIVE, scratch=scratch) == code, s.terms("heron").snapshot)
    s.db.close()

    tools.moved_in_time(root / "specs" / "target.md")
    s = searched()
    check("a file whose time of change alone moved is read again and leaves the code as it was", s.read_count == 1 and s.terms("heron").snapshot == code, (s.read_count, s.terms("heron").snapshot))
    s.db.close()

    tools.put(root, "specs/target.md", spec + "\nThe egret is not yet committed.\n")
    s = searched()
    after = s.terms("heron").snapshot
    check("once a file of the target holds something new the code differs, on a result and on request", after != code and search.snapshot(root, scratch=scratch) == after, (code, after))
    s.db.close()
    check("and the code of the committed files stands as it did, no commit having changed", search.snapshot(root, target=search.COMMITTED_OPERATIVE, scratch=scratch) == code)
    tools.put(root, "specs/target.md", spec)
    check("a file brought back to what it held brings the code back", search.snapshot(root, scratch=scratch) == code)

    s = searched(target=search.WORKING, paths=[".ai/plans/design-specs"])
    one = s.terms("heron").snapshot
    s.db.close()
    check("a result of the working files holds the code of the paths it names, which the search gives on request for those paths",
          bool(search.SNAPSHOT.fullmatch(one)) and one != code and search.snapshot(root, target=search.WORKING, paths=[".ai/plans/design-specs"], scratch=scratch) == one, one)
    check("and other paths take another code", search.snapshot(root, target=search.WORKING, paths=[".ai/plans"], scratch=scratch) != one)
    tools.put(root, ".ai/plans/other-plan.md", fixtures["plan-citing-the-heron"].replace(", citing `specs/target.md § Target` too.", ", changed."))
    tools.put(root, "specs/target.md", spec.replace("in the reeds.", "in the reeds, changed."))
    check("a working file changed outside the paths named, and an operative file changed, leave that code as it was: it stands for the paths named alone",
          search.snapshot(root, target=search.WORKING, paths=[".ai/plans/design-specs"], scratch=scratch) == one)
    tools.put(root, ".ai/plans/design-specs/a-design.md", fixtures["design-citing-the-heron"].replace(" is cited as `specs/target.md § Target` from this design.", ", changed."))
    check("and a working file changed under them changes it", search.snapshot(root, target=search.WORKING, paths=[".ai/plans/design-specs"], scratch=scratch) != one)


@pytest.mark.action("--show-snapshot-code")
@pytest.mark.reports
@pytest.mark.reads(*HERON)
def test_the_code_of_a_commits_files_is_refused_where_no_version_control_holds_the_project(fixtures, tools, search, script, work, check):
    # a small project with no repository at or above it below the run's folder
    root = tools.a_project(work / "project", fixtures)
    ran, printed = script(root, "--show-snapshot-code", "--target", search.COMMITTED_OPERATIVE)
    check("asked for the code of the committed files of a project under no version control, the script stops, says so and gives no code",
          ran == 1 and "under no version control the search reads" in printed and not any(search.SNAPSHOT.fullmatch(line) for line in printed.split("\n")), (ran, printed))
    check("and it leaves no index behind", not (root / search.SCRATCH).exists(), list((root / ".ai").rglob("*")))
