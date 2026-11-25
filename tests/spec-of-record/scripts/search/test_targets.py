"""The targets of a search: the operative files and the fixture files, each as they stand and as a commit held them,
and the working files a search is given the paths of."""
import pytest

HERON = ("search-heron-project.md", "heron-spec", "stack-naming-one-code-root", "heron-function", "egret-function", "design-citing-the-heron",
         "plan-citing-the-heron", "follow-ups-naming-a-heron")
IBIS, EGRET = "\nThe ibis came with the second commit.\n", "\nThe egret is not yet committed.\n"


def a_repository_of_two_commits(root, fixtures, tools):
    """A project under git whose spec gains a sentence with its second commit, and since then one more sentence,
    while its stack comes to name `src` as its code root in place of `code` -> (the first commit, the second)."""
    tools.a_project(root, fixtures)
    tools.git(root, "init", "-q")
    tools.git(root, "add", "specs", "code")
    tools.git(root, "commit", "-q", "-m", "first")
    first = tools.git(root, "rev-parse", "HEAD")
    tools.put(root, "specs/target.md", fixtures["heron-spec"] + IBIS)
    tools.git(root, "add", "specs")
    tools.git(root, "commit", "-q", "-m", "second")
    second = tools.git(root, "rev-parse", "HEAD")
    # the test's variants of two fixtures: the spec with a sentence no commit holds, and the stack naming another
    # code root, so the files as they stand and the files a commit held give different answers
    tools.put(root, "specs/target.md", fixtures["heron-spec"] + IBIS + EGRET)
    tools.put(root, tools.HERON["stack-naming-one-code-root"], fixtures["stack-naming-one-code-root"].replace("`code`", "`src`"))
    return first, second


@pytest.mark.action("--show-term-uses", "--show-lines", "--show-citers", "--show-cited-sections")
@pytest.mark.passes
@pytest.mark.reads(*HERON)
@pytest.mark.reads("search-heron-project.md", "bittern-spec")
def test_a_search_answers_over_the_target_it_names_and_no_other(fixtures, tools, search, opened, script, work, check):
    # the project's spec names a heron, its code names one under `code` and one, with an egret, under `src`, and each
    # of its three working files names one, the design and the other plan citing the spec's section
    root, scratch = work / "project", work / "index"
    first, second = a_repository_of_two_commits(root, fixtures, tools)
    paths_of, changed = tools.paths_of, tools.changed

    def searched(**given):
        return opened(root, scratch=scratch, **given)

    s = searched()
    r = s.terms("heron")
    check("a search naming no target answers over the operative files as they stand, the code among them by the stack as it stands, and says so",
          paths_of(r) == ["specs/target.md", "src/other.py"] and r.target == search.CURRENT_OPERATIVE and r.commit is None and "**Target:** current-operative-files" in r.path.read_text(encoding="utf-8")
          and "**Commit:**" not in r.path.read_text(encoding="utf-8"), (paths_of(r), r.target))
    check("and finds a line not yet committed", paths_of(s.terms("egret")) == ["specs/target.md", "src/other.py"], paths_of(s.terms("egret")))
    s.db.close()

    s = searched(target=search.COMMITTED_OPERATIVE)
    r = s.terms("heron")
    check("a search of the committed target answers for the files as the last commit held them, the code among them by the code roots the stack named then",
          paths_of(r) == ["code/sample.py", "specs/target.md"], paths_of(r))
    check("and gives no line written since, whatever the files hold now", not s.terms("egret").places and paths_of(s.terms("ibis")) == ["specs/target.md"], s.terms("egret").places)
    held = r.path.read_text(encoding="utf-8")
    check("its result names the target and, its asker having named no commit, the last commit it read under a name of its own, and passes the check of a result's form",
          r.target == search.COMMITTED_OPERATIVE and r.commit is None and r.last_commit == second and f"**Last Commit:** {second}" in held and "**Commit:**" not in held and search.Result.check(r.path) == [],
          (r.commit, r.last_commit, search.Result.check(r.path)))
    check("a result of the committed files holding neither a Commit nor a Last Commit is not in its form",
          any("holds neither" in p for p in changed(r.path, f"    **Last Commit:** {second} \\\n", "")), changed(r.path, f"    **Last Commit:** {second} \\\n", ""))
    check("and one holding both is not in its form",
          any("holds both" in p for p in changed(r.path, f"    **Last Commit:** {second} \\\n", f"    **Commit:** {second} \\\n    **Last Commit:** {second} \\\n")))
    lines = s.lines("specs/target.md § Target")
    check("the lines a citation names are the commit's", [(p.first, p.last) for p in lines.places] == [(3, 8)], lines.places)
    s.db.close()

    s = searched(target=search.COMMITTED_OPERATIVE, commit=second)
    check("a search naming the last commit by its name holds it as the Commit its asker named", s.terms("heron").commit == second and s.terms("heron").last_commit is None, (s.terms("heron").commit, s.terms("heron").last_commit))
    s.db.close()

    s = searched(target=search.COMMITTED_OPERATIVE, commit=first)
    named = s.terms("heron")
    held = named.path.read_text(encoding="utf-8")
    check("a search naming another commit answers for that one, and its result names it",
          not s.terms("ibis").places and paths_of(named) == ["code/sample.py", "specs/target.md"] and named.commit == first, (s.terms("ibis").places, s.commit))
    check("a result holds a Commit only where its asker named one, and then no Last Commit, so a record copied from it pins a search only where one was asked for",
          named.last_commit is None and f"**Commit:** {first}" in held and "**Last Commit:**" not in held and search.Result.check(named.path) == [], (named.last_commit, search.Result.check(named.path)))
    check("a result of the operative files as they stand that names a commit is not in its form",
          any("its Target is not the committed files" in p for p in changed(named.path, "    **Target:** committed-operative-files \\\n", "    **Target:** current-operative-files \\\n")))
    s.db.close()

    for given, why in (({}, "is given none"), ({"paths": ["specs"]}, "is no working file")):
        try:
            searched(target=search.WORKING, **given)
            refused = ""
        except ValueError as e:
            refused = str(e)
        check(f"a search of the working files that {'is given no path' if not given else 'is given a path that is no working file'} is refused", why in refused, refused)
    s = searched(target=search.WORKING, paths=[".ai/plans/design-specs"])
    r = s.terms("heron")
    check("a search of the working files answers over the paths it is given alone, and its result names the target and the paths",
          paths_of(r) == [".ai/plans/design-specs/a-design.md"] and r.target == search.WORKING and r.narrowed == [".ai/plans/design-specs"] and search.Result.check(r.path) == [],
          (paths_of(r), r.narrowed, search.Result.check(r.path)))
    r = s.citers("specs/target.md § Target")
    check("it lists the working files' places citing an operative file's section, read against that file, and no place among the operative files",
          paths_of(r) == [".ai/plans/design-specs/a-design.md"] and not any("does not resolve" in n for n in r.notes), (r.places, r.notes))
    r = s.cited_sections()
    check("its listing of cited sections holds citing places of the working files alone, the operative file's section they cite named and no place",
          [str(p) for p in r.places] == ["`.ai/plans/design-specs/a-design.md § The Problem` line 5 cites `specs/target.md § Target`"], r.places)
    check("a result of the working files holding no path it was given is not in its form",
          any("holds no Narrowed To" in p for p in changed(r.path, "    **Narrowed To:**\n      - `.ai/plans/design-specs`\n\n", "")), changed(r.path, "    **Narrowed To:**\n      - `.ai/plans/design-specs`\n\n", ""))
    s.db.close()
    s = searched(target=search.WORKING, paths=[".ai/plans", ".ai/follow-ups.md"])
    check("given more paths it answers over more, a file and a folder among them",
          paths_of(s.terms("heron")) == [".ai/follow-ups.md", ".ai/plans/design-specs/a-design.md", ".ai/plans/other-plan.md"] and s.read_count == 2, (paths_of(s.terms("heron")), s.read_count))
    s.db.close()
    s = searched(target=search.WORKING, paths=[".ai/plans/design-specs"])
    check("given fewer again, it reads no file again and gives no place of a path it was not given", s.read_count == 0 and paths_of(s.terms("heron")) == [".ai/plans/design-specs/a-design.md"], (s.read_count, paths_of(s.terms("heron"))))
    s.db.close()

    # one index held all three: each target's search still gives its own files alone
    s = searched()
    check("after the other targets' searches, a search of the operative files as they stand gives no working file and no file only the commit held",
          paths_of(s.terms("heron")) == ["specs/target.md", "src/other.py"] and s.read_count == 0, (paths_of(s.terms("heron")), s.read_count))
    s.db.close()
    s = searched(target=search.COMMITTED_OPERATIVE)
    check("and a search of the committed target gives the commit's files alone, reading again only the one file the last commit holds otherwise than the commit searched before it",
          paths_of(s.terms("heron")) == ["code/sample.py", "specs/target.md"] and paths_of(s.terms("ibis")) == ["specs/target.md"] and s.read_count == 1, (paths_of(s.terms("heron")), s.read_count))
    s.db.close()

    ran, refused = script(root, "--show-term-uses", "ibis", "--target", search.COMMITTED_OPERATIVE, "--commit", first)[0], script(root, "--show-term-uses", "heron", "--target", search.WORKING)[0]
    check("the script takes the target and the commit, and refuses a search of the working files given no path", ran == 0 and refused == 2, (ran, refused))

    # a project standing in a folder of a larger repository is under git: the test's variant of the spec about a
    # bittern holds one sentence more than the commit does
    tools.put(root, "inner/specs/target.md", fixtures["bittern-spec"])
    tools.git(root, "add", "inner")
    tools.git(root, "commit", "-q", "-m", "third")
    tools.put(root, "inner/specs/target.md", fixtures["bittern-spec"] + "\nThe crane is not.\n")
    s = opened(root / "inner", scratch=work / "index-inner", target=search.COMMITTED_OPERATIVE)
    check("a project standing in a folder of a larger repository is read as under git, its committed files given by their paths from the project's root",
          search.version_control(root / "inner") == search.GIT and paths_of(s.terms("bittern")) == ["specs/target.md"] and not s.terms("crane").places, (paths_of(s.terms("bittern")), s.terms("crane").places))


@pytest.mark.action("--show-term-uses", "--show-pattern-matches", "--show-citers", "--show-cited-sections", "--show-code-structure", "--show-similar-passages", "--show-lines")
@pytest.mark.passes
@pytest.mark.reads(*HERON)
@pytest.mark.reads("search-heron-project.md", "reeds-spec", "herons-text-holding-a-sentence-of-the-reeds", "heron-kept-test")
def test_each_kind_of_durable_file_is_listed_read_and_ranked_apart(fixtures, tools, search, opened, script, work, check):
    # a fixture file holds a sentence that an operative spec, the one about the reeds, holds word for word, and
    # beside it a citation of an operative file's section and a sentence about a spoonbill no other file holds; a
    # kept test's own code, which is an operative file, names a heron too
    root, scratch = work / "project", work / "index"
    first, second = a_repository_of_two_commits(root, fixtures, tools)
    paths_of = tools.paths_of
    folder, fixture, kept_test = search.spec_text.FIXTURES, search.spec_text.FIXTURES + "/herons.md", "tests/spec-of-record/scripts/heron-tests.py"
    said = "A heron waits among the reeds at the water's edge for a fish."
    tools.put(root, "specs/reeds.md", fixtures["reeds-spec"])
    tools.put(root, kept_test, fixtures["heron-kept-test"])

    def searched(**given):
        return opened(root, scratch=scratch, **given)

    def in_fixtures(result):
        return [str(p) for p in result.places if folder + "/" in str(p)]

    def of_each_kind(s):
        return [s.terms("heron"), s.pattern("heron"), s.citers("specs/target.md § Target"), s.cited_sections(), s.code_structure("defines", "heron_test"), s.meaning(said), s.meaning("specs/reeds.md § Herons")]

    s = searched()
    ranked = [str(p) for p in s.meaning(said).places]
    s.db.close()
    tools.put(root, fixture, fixtures["herons-text-holding-a-sentence-of-the-reeds"])
    tools.git(root, "add", "tests", "specs/reeds.md")
    tools.git(root, "commit", "-q", "-m", "fourth")
    fourth = tools.git(root, "rev-parse", "HEAD")
    # the test's variant of the fixture file: one sentence more than the last commit holds
    tools.put(root, fixture, fixtures["herons-text-holding-a-sentence-of-the-reeds"] + "\nThe avocet came to the fixture after the last commit, and no commit holds it.\n")

    check("the listing of the operative files holds no fixture file, the kept tests' own code standing among them, and the listing of the fixture files holds the fixture files alone, as the files stand and as the last commit held them",
          not [f for f in search.operative_files(root) + search.operative_files(root, committed=True) if f.startswith(folder)] and kept_test in search.operative_files(root)
          and search.fixture_files(root) == [fixture] == search.fixture_files(root, committed=True) == search.listed(root, root, search.spec_text.FIXTURE),
          (search.fixture_files(root), [f for f in search.operative_files(root) if f.startswith("tests/")]))
    s = searched()
    answers = of_each_kind(s)
    check("a search of the operative files gives no place in a fixture file, a fixture file holding text an operative file holds, whatever its kind of search",
          not any(in_fixtures(r) for r in answers) and paths_of(answers[0]) == ["specs/reeds.md", "specs/target.md", "src/other.py", kept_test], [in_fixtures(r) for r in answers] + [paths_of(answers[0])])
    check("it reads no fixture file, and its index holds no word of one",
          s.read_count == 0 and not s.terms("spoonbill").places and not s.db.execute("select count(*) from terms where terms match 'spoonbill'").fetchone()[0]
          and not s.db.execute("select count(*) from placed where path like ?", (folder + "/%",)).fetchone()[0], (s.read_count, s.terms("spoonbill").places))
    r = s.lines(fixture + " § Herons")
    check("and a citation of a fixture file's section names it no place", not r.places and r.names_nothing == [search.NO_PLACE], (r.places, r.names_nothing))
    check("its ranking by meaning is unchanged by a fixture file added, the fixture holding a passage of the ranking word for word",
          len(ranked) > 1 and [str(p) for p in answers[5].places] == ranked, (ranked, [str(p) for p in answers[5].places]))
    s.db.close()
    s = searched(target=search.COMMITTED_OPERATIVE)
    check("and a search of the operative files as a commit held them gives no place in a fixture file the commit holds", not any(in_fixtures(r) for r in of_each_kind(s)) and "specs/reeds.md" in paths_of(s.terms("heron")),
          [in_fixtures(r) for r in of_each_kind(s)])
    s.db.close()

    s = searched(target=search.CURRENT_FIXTURE)
    answers = of_each_kind(s)
    r = answers[0]
    check("a search of the fixture files gives places in fixture files alone, whatever its kind of search, and its result names the target",
          all(len(in_fixtures(a)) == len(a.places) for a in answers) and paths_of(r) == [fixture] and paths_of(answers[5]) == [fixture] and paths_of(answers[2]) == [fixture]
          and r.target == search.CURRENT_FIXTURE and "**Target:** current-fixture-files" in r.path.read_text(encoding="utf-8") and search.Result.check(r.path) == [],
          ([[str(p) for p in a.places] for a in answers], search.Result.check(r.path)))
    check("it finds a line of a fixture file not yet committed, and its index holds no word that stands in an operative file alone",
          paths_of(s.terms("avocet")) == [fixture] and not s.db.execute("select count(*) from terms where terms match 'egret'").fetchone()[0], paths_of(s.terms("avocet")))
    s.db.close()
    s = searched(target=search.COMMITTED_FIXTURE)
    r = s.terms("heron")
    check("a search of the fixture files as a commit held them gives the commit's fixture files alone, no line written since, and its result holds the last commit it read",
          paths_of(r) == [fixture] and not s.terms("avocet").places and paths_of(s.terms("spoonbill")) == [fixture] and r.target == search.COMMITTED_FIXTURE and r.last_commit == fourth and r.commit is None
          and search.Result.check(r.path) == [], (paths_of(r), s.terms("avocet").places, r.last_commit, search.Result.check(r.path)))
    s.db.close()
    s = searched(target=search.COMMITTED_FIXTURE, commit=second)
    check("and, naming a commit that held no fixture file, it gives no place and holds the Commit named", not s.terms("heron").places and s.terms("heron").commit == second, s.terms("heron").places)
    s.db.close()
    try:
        searched(target=search.CURRENT_FIXTURE, commit=fourth)
        refused = ""
    except ValueError as e:
        refused = str(e)
    check("a search of the fixture files as they stand that names a commit is refused", "a commit is named" in refused, refused)
    ran, printed = script(root, "--show-term-uses", "heron", "--target", search.CURRENT_FIXTURE)
    check("the script takes each target of the fixture files, and a search naming none gives no fixture file",
          ran == 0 and fixture in printed and "specs/reeds.md" not in printed and script(root, "--show-term-uses", "heron", "--target", search.COMMITTED_FIXTURE)[0] == 0
          and folder not in script(root, "--show-term-uses", "heron")[1], (ran, printed))
