"""What the search requires: checked before any search reads or writes, listed on request, and the model's files
installed by the one action that reaches the network.

No test here downloads anything. The run that installs the model is made where the model's files already stand, with
the model's library told to stay off the network, so it finds them and fetches nothing; the model's files stand where
the search installs them once on a machine, outside every run's folder, and are no run's output."""
import pytest

HERON = ("search-heron-project.md", "heron-spec", "stack-naming-one-code-root", "heron-function", "egret-function", "design-citing-the-heron",
         "plan-citing-the-heron", "follow-ups-naming-a-heron")
ABSENT = ("search-absent-requirement.md", "python-without-fastembed")
OFFLINE = {"HF_HUB_OFFLINE": "1"}


def without_fastembed(work, fixtures, tools):
    """-> the environment of a process whose Python finds no fastembed: the fixture stands on its path as its site
    customization, and nothing else of the process is changed."""
    tools.put(work / "no-fastembed", "sitecustomize.py", fixtures["python-without-fastembed"])
    return dict(OFFLINE, PYTHONPATH=str(work / "no-fastembed"))


@pytest.mark.action("--show-citers", "--show-lines", "--show-term-uses", "--show-pattern-matches", "--show-similar-passages", "--show-code-structure")
@pytest.mark.reports
@pytest.mark.reads("search-corpus-specs.md", "target-spec")
def test_with_a_requirement_absent_every_kind_of_search_stops_before_it_reads_or_writes(fixtures, tools, search, monkeypatch, work, check):
    # a project of one spec, searched by a search told of one requirement more, which nothing can make present
    root, scratch = work / "project", work / "index"
    tools.put(root, "specs/target.md", fixtures["target-spec"])
    monkeypatch.setattr(search, "REQUIREMENTS", search.REQUIREMENTS + [search.Requirement("a package that is absent", "a test takes it away", "python -m pip install it", lambda root: False)])
    for kind in ("citers", "lines", "terms", "pattern", "meaning", "code_structure"):
        try:
            search.Search(root, cover=[], scratch=scratch, quiet=True)
            stopped, text = False, ""
        except search.MissingRequirements as e:
            stopped, text = True, str(e)
        check(f"with a requirement absent a search by {kind.replace('_', ' ')} stops before it reads or writes",
              stopped and not scratch.exists() and "a package that is absent: a test takes it away" in text and "to install it: python -m pip install it" in text, text)


@pytest.mark.action("--check-requirements")
@pytest.mark.passes
@pytest.mark.reads(*HERON)
def test_check_requirements_lists_each_thing_the_search_requires_as_present(fixtures, tools, search, script, work, check):
    root = tools.a_project(work / "project", fixtures)
    ran, printed = script(root, "--check-requirements", env=OFFLINE)
    check("where everything the search requires is present, the script says so, names each thing with why the search needs it, and exits 0",
          ran == 0 and "everything the search requires is present" in printed and printed.count("  present  ") == len(search.REQUIREMENTS) and "MISSING" not in printed
          and all(r.name + ": " + r.why in printed for r in search.REQUIREMENTS), (ran, printed))
    check("and it writes nothing in the project it is run in", not (root / search.SCRATCH).exists())


@pytest.mark.action("--check-requirements", "--show-term-uses")
@pytest.mark.reports
@pytest.mark.reads(*HERON)
@pytest.mark.reads(*ABSENT)
def test_check_requirements_names_what_is_missing_with_the_command_installing_it(fixtures, tools, search, script, work, check):
    root = tools.a_project(work / "project", fixtures)
    env = without_fastembed(work, fixtures, tools)
    ran, printed = script(root, "--check-requirements", env=env)
    check("in a Python holding no fastembed, the script says the search cannot run, marks fastembed alone as missing with the command installing it, and exits 1",
          ran == 1 and "the search cannot run" in printed and "1 is missing" in printed and "  MISSING  fastembed: " in printed and "to install it: python -m pip install fastembed" in printed
          and printed.count("  MISSING  ") == 1 and printed.count("  present  ") == len(search.REQUIREMENTS) - 1, (ran, printed))
    ran, said = script(root, "--show-term-uses", "heron", env=env)
    check("and a search run there stops with the same report, exits 1 and writes nothing",
          ran == 1 and "  MISSING  fastembed: " in said and "Traceback" not in said and not (root / search.SCRATCH).exists(), (ran, said))


@pytest.mark.action("--install-model")
@pytest.mark.passes
@pytest.mark.reads(*HERON)
def test_install_model_where_the_models_files_stand_finds_them_and_says_where(fixtures, tools, search, script, work, check):
    # the run is kept off the network, so it passes only by finding the model's files where they already stand
    root = tools.a_project(work / "project", fixtures)
    held = search.model_folder()
    before = sorted(p.relative_to(held).as_posix() for p in held.rglob("*") if p.is_file()) if held.is_dir() else []
    ran, printed = script(root, "--install-model", env=OFFLINE)
    after = sorted(p.relative_to(held).as_posix() for p in held.rglob("*") if p.is_file()) if held.is_dir() else []
    check("run where the model's files stand and kept off the network, the script says where the model's files are, the main checkout's scratch space, and exits 0",
          ran == 0 and "the model's files are in " + held.as_posix() in printed and "where every checkout of the project finds them" in printed, (ran, printed))
    check("and it fetches no file and writes none in the project it is run in", before == after and bool(after) and not (root / search.SCRATCH).exists(), (len(before), len(after)))


@pytest.mark.action("--install-model")
@pytest.mark.reports
@pytest.mark.reads(*HERON)
@pytest.mark.reads(*ABSENT)
def test_install_model_is_refused_where_the_package_that_downloads_it_is_missing(fixtures, tools, search, script, work, check):
    root = tools.a_project(work / "project", fixtures)
    ran, printed = script(root, "--install-model", env=without_fastembed(work, fixtures, tools))
    check("in a Python holding no fastembed, the script refuses, saying fastembed is missing and how to install it, and exits 1 with no traceback",
          ran == 1 and "fastembed is missing, and it downloads the model's files" in printed and "python -m pip install fastembed" in printed and "Traceback" not in printed, (ran, printed))
