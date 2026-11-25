"""The checkout: where the model is found, how long a result's path grows, and which checkout a search runs over.

The project these tests make stands in the file's own folder within the run's folder, whose path is short, since two
checks turn on how long a result's whole path is."""
import re
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

HERON = ("search-heron-project.md", "heron-spec", "stack-naming-one-code-root", "heron-function", "egret-function", "design-citing-the-heron",
         "plan-citing-the-heron", "follow-ups-naming-a-heron")
DEEP = 205  # the length of the path of the folder standing deep, which leaves a result's name room for some of the words asked


@pytest.mark.action("--show-term-uses")
@pytest.mark.passes
@pytest.mark.reads(*HERON)
@pytest.mark.reads("search-heron-project.md", "skill-folder-stand-in")
def test_a_search_runs_over_the_checkout_it_is_run_in_and_finds_the_model_in_the_main_one(fixtures, tools, search, script, shared, checkout, check):
    # a project of its own, holding a copy of the search's code as this checkout holds it as the test runs, under
    # version control, with a second checkout of it, a worktree kept among its own working files; a stand-in for the
    # skill's own file is committed, so each checkout of the project holds the skill's folder
    root, lib = shared.folder / "project", tools.SKILL_FOLDER.parent / "lib"
    shutil.copytree(checkout / lib, root / lib, ignore=shutil.ignore_patterns("__pycache__"))
    tools.a_project(root, fixtures)
    tools.put(root, (tools.SKILL_FOLDER / "SKILL.md").as_posix(), fixtures["skill-folder-stand-in"])
    tools.git(root, "init", "-q")
    tools.git(root, "add", "-A")
    tools.git(root, "commit", "-q", "-m", "a project made for a test")
    second = root / ".ai" / "tmp" / "worktrees" / "second"
    tools.git(root, "worktree", "add", "-q", "--detach", str(second), "HEAD")

    def model_of(where):
        """-> where the search whose code stands in a checkout looks for its model, asked of that code itself."""
        asked = subprocess.run([sys.executable, "-B", "-c", "import sys\nsys.path.insert(0, sys.argv[1])\nimport search\nprint(search.model_folder())", str(where / lib)],
                               capture_output=True, text=True, encoding="utf-8", cwd=where)
        return Path(asked.stdout.strip()).resolve() if asked.returncode == 0 and asked.stdout.strip() else asked.stderr[-300:]

    kept = (root / search.SCRATCH / "model").resolve()
    check("the search whose code stands in a project's main checkout looks for its model in that checkout's scratch space", model_of(root) == kept, model_of(root))
    check("the search whose code stands in a second checkout, a worktree, looks for its model where the main checkout keeps it", model_of(second) == kept, model_of(second))
    check("a checkout under no version control is its own main checkout, and a worktree's is the checkout holding the repository",
          search.main_checkout(root / "code") == root / "code" and search.main_checkout(second) == root and search.main_checkout(root) == root,
          (search.main_checkout(second), root))

    # a result written in a folder standing deep: its whole path stays one every system opens
    deep = root
    while len(str(deep / "a-folder-standing-deep")) <= DEEP - 2:
        deep = deep / "a-folder-standing-deep"
    deep = deep / ("d" * (DEEP - len(str(deep)) - 1))
    asked = "the lighthouse keeper trims the lamp wick each evening before dark and the ferry crosses the estuary at the turn of the tide " * 3
    result = search.Result("terms", asked, [], "each form searched as a phrase", "complete", [])
    try:
        written = result.write(deep / "results")
        wrote = written.is_file()
    except OSError as failed:
        written, wrote = deep / "results" / (result.name or ""), "the result could not be written: %s" % failed
    check("a result written in a folder standing deep keeps its whole path within the longest every system opens, and is written",
          len(str(deep)) == DEEP and wrote is True and len(str(written.resolve())) <= search.MAX_PATH, (wrote, len(str(deep)), len(str(written)), search.MAX_PATH))
    check("and its name still tells it apart by its two hashes, with the words asked that fit",
          wrote is True and bool(re.fullmatch(r"terms-the-lighthouse[a-z0-9-]*-[0-9a-f]{6}-[0-9a-f]{8}\.md", written.name)), written.name)
    shallow = search.Result("terms", asked, [], "each form searched as a phrase", "complete", []).write(root / "results")
    check("in a folder standing shallow the same result's name holds the words asked up to the length a name may take, and ends in the same two hashes",
          search.MAX_NAME - 1 <= len(shallow.name) <= search.MAX_NAME and shallow.name[-18:] == written.name[-18:], (len(shallow.name), shallow.name[-18:], written.name[-18:]))

    # a search naming no project answers over the checkout it is run in, whichever checkout holds the script: the
    # entry script of this checkout is run with the second checkout of the project as its working directory
    own = lambda: sorted(p.name for p in (checkout / search.SCRATCH / "results").glob("terms-heron-*.md"))
    before = own()
    ran, printed = script(second, "--show-term-uses", "heron")
    check("a search naming no project, run in a second checkout, answers over that checkout's files and writes its result there",
          ran == 0 and "`specs/target.md § Target` line 5" in printed and len(list((second / search.SCRATCH / "results").glob("terms-heron-*.md"))) == 1
          and not (root / search.SCRATCH / "results").exists(),
          (ran, printed[-400:], [p.name for p in (second / search.SCRATCH).glob("results/*")], (root / search.SCRATCH / "results").exists()))
    check("and writes none in the checkout holding the script that was run", own() == before, (before, own()))
