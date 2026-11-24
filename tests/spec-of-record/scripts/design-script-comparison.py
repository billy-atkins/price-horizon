#!/usr/bin/env python3
"""The kept comparison of the design script, .ai/skills/lib/design_documents.py: which designs a change to the script,
or to a form of the canon it reads, reads differently.

  design-script-comparison.py                      the designs of the checkout's own plans folders, each named for a skill
  design-script-comparison.py PLANS_FOLDER ...     the designs of the plans folders given, with their reports

It runs each action of the design script that reads a design over the same design documents and reports by each of its
sides: the script as the last commit held it, and the script as it stands. Each side is a checkout of its own, a
worktree version control makes at the last commit under .ai/tmp/worktrees/ of the checkout the comparison is run in,
and removes as the run ends. The side at the last commit is that worktree as it is made. The side as it stands is a
worktree with the checkout's uncommitted work laid over it: each file changed or new copied in, and each file removed
taken out, so its changes show against the last commit as they do in the checkout. So each script reads the canon of
its own tree, the forms it reads as it runs among them, and each reads the last commit wherever the design script
does. No commit is made. The design documents of each plans folder given, and the reports and diagnoses in each
design's folder, are copied into both worktrees at their own places, where version control tracks none of them, so
neither side reads the checkout's plans folders. The run writes nothing in the checkout but those worktrees, which it
removes whatever happens, a worktree an earlier run left at either place removed first. It needs no second checkout
made by hand. Where the project is under no version control, or holds no commit, the comparison cannot be made.

Each worktree is given a copy of the index the checkout's search kept, where the checkout holds one and that side's
search writes the same form of index, so a side's search runs through the model only the passages its own tree holds
that the checkout's did not. The copy leaves each side's reading resting on its own tree's files alone, as `seed_index`
says. No model's files are copied: a worktree's search finds them where the main checkout keeps them.

The actions are taken from each side's own table of flags: each check and each show taking a design or a proposal,
`--check-settled-report` over each report a design's log names, and each check and each show of a plans folder. An
action reading the checkout's uncommitted work rather than a design is left out, and so is an action writing a file.
An action only one side holds is named once, and compared for no design.

It lists each design the two sides read differently, with each action whose exit status or output differs and the
lines one side gave that the other did not, and no other design. The same lines given in another order are the same
reading. Each listed design stands on a line of its own, `design` and its path, which the design script reads the list
from. The run exits 0 where the comparison was made, whatever it lists, and 2 where it could not be made.

The comparison takes the project from the checkout it is run in: the nearest folder at or above the working directory
holding the design script's code, whichever checkout holds this file.
"""
import collections
import concurrent.futures
import json
import os
import re
import shutil
import sqlite3
import stat
import subprocess
import sys
from pathlib import Path

sys.dont_write_bytecode = True

# The files of the script this comparison is of: its code, and each file of the canon it reads a form from as it runs.
# A path ending in a slash names each file beneath it. The design script's kept tests name the same files.
SCRIPT_FILES = (".ai/skills/lib/", ".ai/skills/design-specs/scripts/", ".ai/skills/implement-specs/scripts/")
FORM_FILES = ("specs/methodology/working-files/main.md", "specs/methodology/design-workflow/order-of-a-designs-work.md", "specs/methodology/modeling-constructs.md",
              "specs/methodology/expressions.md", "specs/methodology/spec-style/markdown.md", "specs/methodology/skills/registered-skills.md")

LIB = Path(".ai") / "skills" / "lib"
RUN_IN = Path.cwd().resolve()
# the checkout the comparison is run in, or, run from outside every checkout, the one holding this file
PROJECT = next((p for p in (RUN_IN, *RUN_IN.parents) if (p / LIB / "design_documents.py").is_file()), Path(__file__).resolve().parents[3])
# where the two sides' worktrees stand, among the checkout's working files
THEN = PROJECT / ".ai" / "tmp" / "worktrees" / "design-script-comparison-then"
NOW = PROJECT / ".ai" / "tmp" / "worktrees" / "design-script-comparison-now"
# the search's scratch space in a checkout, where its index stands, as .ai/skills/lib/search.py places it
SEARCH_SCRATCH = Path(".ai") / "tmp" / "search-spec-of-record-scope"
# the actions reading the checkout's uncommitted work rather than a design: the side as it stands holds that work and
# the side at the last commit holds none, so each would list every design for the work alone
READS_THE_WORK = ("--check-work", "--check-changed-files", "--check-audits")
SHOWN = 8  # the differing lines shown of one action's output

# Runs in a tree of its own, by that tree's design script, each action reading a design, and prints what each gave.
SIDE = r'''
import contextlib, io, json, sys
from pathlib import Path
sys.dont_write_bytecode = True
tree = Path(sys.argv[1])
sys.path.insert(0, str(tree / ".ai" / "skills" / "lib"))
import design_documents as dd
given = json.load(sys.stdin)
skipped = set(given["skipped"])
flags = [(flag, metavar) for flag, metavar, _, _ in dd.FLAGS if flag.startswith(("--check-", "--show-")) and flag not in skipped]
of_a_design = [flag for flag, metavar in flags if metavar in ("DESIGN", "PROPOSAL")]
of_a_report = [flag for flag, metavar in flags if flag == "--check-settled-report"]
of_a_folder = [flag for flag, metavar in flags if metavar == "PLANS_DIR"]
runs = []


def run(key, plans, flag, value):
    out = io.StringIO()
    try:
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(out):
            status = dd.main(["design-script", flag, value], plans=plans)
    except SystemExit as stopped:
        status = stopped.code
    except Exception as raised:  # a side that cannot read a design reads it differently from one that can
        status = "%s: %s" % (type(raised).__name__, raised)
    runs.append([key, flag, value, status, out.getvalue()])


for plans, designs in given["folders"]:
    for flag in of_a_folder:
        run("", plans, flag, plans)
    for design, reports in designs:
        for flag in of_a_design:
            run(design, plans, flag, design)
        for report in reports:
            for flag in of_a_report:
                run(design, plans, flag, report)
sys.stdout.reconfigure(encoding="utf-8")
json.dump({"flags": of_a_design + of_a_report + of_a_folder, "runs": runs}, sys.stdout)
'''


def git(*args, cwd=PROJECT):
    return subprocess.run(["git", *args], cwd=cwd, capture_output=True, text=True, encoding="utf-8")


def remove_worktree(path):
    """Remove a side's worktree, registered or left as a bare folder, so none stands or stays registered at its place."""
    registered = {Path(line[len("worktree "):]).resolve() for line in git("worktree", "list", "--porcelain").stdout.splitlines()
                  if line.startswith("worktree ")}
    if path.resolve() in registered:
        git("worktree", "remove", "--force", str(path))
    if path.exists():  # a folder version control no longer holds as a worktree, or could not remove whole
        def writable(remove, held, _):
            os.chmod(held, stat.S_IWRITE)
            remove(held)
        shutil.rmtree(path, onerror=writable)
    git("worktree", "prune")


def add_worktree(path):
    """A worktree at the last commit, detached, at a place cleared of any an earlier run left there."""
    remove_worktree(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    made = git("worktree", "add", "--detach", str(path), "HEAD")
    if made.returncode:
        raise RuntimeError("a worktree at the last commit could not be made at %s: %s" % (path, made.stderr.strip()))


def lay_over(tree):
    """Lay the checkout's uncommitted work over a worktree at the last commit: each file changed against the last
    commit or new copied in, and each file the work removed taken out."""
    listed = [git("diff", "--name-only", "-z", "HEAD"), git("ls-files", "--others", "--exclude-standard", "-z")]
    if any(run.returncode for run in listed):
        raise RuntimeError("the checkout's uncommitted work could not be listed: " + " ".join(run.stderr.strip() for run in listed))
    for path in sorted({p for run in listed for p in run.stdout.split("\0") if p}):
        if (PROJECT / path).is_file():
            (tree / path).parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(PROJECT / path, tree / path)
        elif (tree / path).is_file():
            (tree / path).unlink()


def seed_index(tree):
    """Give a worktree a copy of the index the checkout's search kept, so its side's search runs through the model only
    the passages its own tree holds that the checkout's did not -> whether it was given one. The search keeps a vector
    for each passage's text, and what each content holds under that content's own hash, so what the copy holds of a
    content is true of that content wherever it stands. Which content stands at which path is the tree's own to say:
    the copy is given with the time each file as it stood was changed set to none, so the side's search reads and
    hashes every file of its own tree, keeps what the copy holds of a content its tree holds, and takes out what it
    holds of a content its tree does not. An answer the search kept is reused by the search only under the snapshot
    code of the files it now reads and the code of its own reading. A side whose search writes another form of the
    index, or names another model, is given none and builds its own, and so is each side where the checkout holds no
    index. The copy is taken through the database itself, so it is whole whatever is writing the checkout's index."""
    kept, code = PROJECT / SEARCH_SCRATCH / "index.sqlite", tree / LIB / "search.py"
    if not kept.is_file() or not code.is_file():
        return False
    text = code.read_text(encoding="utf-8")
    form = [re.search(r'^%s = "([^"]+)"' % name, text, re.M) for name in ("SCHEMA", "MODEL")]
    if not all(form):
        return False
    source = sqlite3.connect("file:%s?mode=ro" % kept.as_posix(), uri=True)
    try:
        try:
            held = source.execute("select value from meta where key='schema'").fetchone()
        except sqlite3.Error:
            return False
        if not held or held[0] != form[0].group(1) + "/" + form[1].group(1):
            return False
        (tree / SEARCH_SCRATCH).mkdir(parents=True, exist_ok=True)
        copy = sqlite3.connect(tree / SEARCH_SCRATCH / "index.sqlite")
        try:
            source.backup(copy)
            copy.execute("update placed set size = -1, mtime_ns = -1 where stamp = ''")
            copy.commit()
        finally:
            copy.close()
    finally:
        source.close()
    return True


def designs_of(plans):
    """-> [(a design document of a plans folder, the reports and diagnoses folders of its design's folder)]: each
    Markdown file standing in the folder itself, none beneath it."""
    out = []
    for design in sorted(plans.glob("*.md")):
        folder = plans.parents[1] / "tmp" / plans.name / design.stem
        out.append((design, [folder / kept for kept in ("reports", "diagnosis") if (folder / kept).is_dir()]))
    return out


def give(tree, folders):
    """Copy the designs of each plans folder given, with their reports and diagnoses, into a tree at their own places,
    and -> what a side is asked to read: [(the plans folder, [(a design, its reports)])], each as a path in the tree."""
    asked = []
    for plans in folders:
        own, designs = Path(".ai") / "plans" / plans.name, []
        (tree / own).mkdir(parents=True, exist_ok=True)
        for design, kept in designs_of(plans):
            shutil.copyfile(design, tree / own / design.name)
            at = Path(".ai") / "tmp" / plans.name / design.stem
            for folder in kept:
                shutil.copytree(folder, tree / at / folder.name)
            reports = sorted((tree / at / "reports").glob("*/*.md")) if (tree / at / "reports").is_dir() else []
            designs.append(((own / design.name).as_posix(), [r.relative_to(tree).as_posix() for r in reports if r.stem.isdigit()]))
        asked.append((own.as_posix(), designs))
    return asked


def read_by(tree, asked):
    """-> what a tree's own design script gave for each action reading a design: {"flags", "runs"}, the script run in
    its tree."""
    ran = subprocess.run([sys.executable, "-c", SIDE, str(tree)], cwd=tree, capture_output=True,
                         input=json.dumps({"folders": asked, "skipped": READS_THE_WORK}).encode("utf-8"),
                         env=dict(os.environ, PYTHONDONTWRITEBYTECODE="1", PYTHONIOENCODING="utf-8"))
    if ran.returncode:
        raise RuntimeError("the design script of %s could not be run:\n%s" % (tree.name, ran.stderr.decode("utf-8", "replace")))
    return json.loads(ran.stdout.decode("utf-8"))


def as_read(text, tree):
    """-> an action's output with the tree's own place taken out of it, so two trees' outputs compare."""
    for place in (str(tree), tree.as_posix(), str(tree.resolve()), tree.resolve().as_posix()):
        text = text.replace(place, "<checkout>")
    return [line.rstrip() for line in text.replace("\r\n", "\n").split("\n")]


def compare(then, now):
    """-> ({key: [what differs]} for each design, and the workstack under "", the two sides read differently, the
    actions only one side holds): each action both hold whose exit status or output differs."""
    both = [flag for flag in now["flags"] if flag in then["flags"]]
    one_side = [(flag, "the last commit") for flag in then["flags"] if flag not in now["flags"]] + \
               [(flag, "the script as it stands") for flag in now["flags"] if flag not in then["flags"]]
    was = {(key, flag, value): (status, as_read(out, THEN)) for key, flag, value, status, out in then["runs"]}
    differs = {}
    for key, flag, value, status, out in now["runs"]:
        if flag not in both or (key, flag, value) not in was:
            continue
        old_status, old = was[(key, flag, value)]
        new = as_read(out, NOW)
        # the lines one side gave and the other did not, however many times: the same lines in another order are the
        # same reading
        gone, come = collections.Counter(old) - collections.Counter(new), collections.Counter(new) - collections.Counter(old)
        if old_status == status and not gone and not come:
            continue
        what = ["%s%s: " % (flag, "" if value == key else " " + value)
                + ("exit %s at the last commit, %s as it stands" % (old_status, status) if old_status != status
                   else "exit %s at both, its output differing" % status)]
        lines = ["- " + l for l in gone.elements()] + ["+ " + l for l in come.elements()]
        what += ["    " + l[:2] + l[2:].strip()[:300] for l in lines[:SHOWN]]
        if len(lines) > SHOWN:
            what.append("    ... %d more lines differ" % (len(lines) - SHOWN))
        differs.setdefault(key, []).extend(what)
    return differs, one_side


def main(argv):
    for stream in (sys.stdout, sys.stderr):
        stream.reconfigure(encoding="utf-8")
    # given none, the checkout's own plans folders: each folder of its plans named for a skill it holds
    folders = [Path(a).resolve() for a in argv[1:]] or sorted(p for p in (PROJECT / ".ai" / "plans").glob("*")
                                                              if p.is_dir() and (PROJECT / ".ai" / "skills" / p.name).is_dir())
    wrong = [str(f) for f in folders if not f.is_dir() or f.parent.name != "plans"]
    if wrong:
        sys.stderr.write("design-script-comparison takes plans folders, each a folder of design documents under a `plans` "
                         "folder, its designs' folders under the `tmp` folder beside that: %s\n" % ", ".join(wrong))
        return 2
    try:
        head = git("rev-parse", "--verify", "-q", "HEAD")
    except FileNotFoundError:
        head = None
    if head is None or head.returncode or not head.stdout.strip():
        sys.stderr.write("design-script-comparison cannot be made: it compares the design script with the last commit's, and "
                         "the project is under no version control or holds no commit: %s\n" % PROJECT)
        return 2
    try:
        for tree in (THEN, NOW):
            add_worktree(tree)
        lay_over(NOW)
        for tree in (THEN, NOW):
            asked = give(tree, folders)
            seed_index(tree)
        # the two sides share nothing, so they are read at once
        with concurrent.futures.ThreadPoolExecutor(max_workers=2) as sides:
            then, now = sides.map(lambda tree: read_by(tree, asked), (THEN, NOW))
        differs, one_side = compare(then, now)
    except RuntimeError as failed:
        sys.stderr.write("design-script-comparison could not be made: %s\n" % failed)
        return 2
    finally:
        for tree in (THEN, NOW):
            remove_worktree(tree)
    designs = [design for _, held in asked for design, _ in held]
    held_by_both = len([f for f in now["flags"] if f in then["flags"]])
    print("== design-script-comparison: the design script as the last commit, %s, held it beside the script as it stands, "
          "each reading its own tree's canon" % head.stdout.strip()[:10])
    print("%d design%s of %s, by %d action%s both hold" % (
        len(designs), "" if len(designs) == 1 else "s", ", ".join(plans for plans, _ in asked),
        held_by_both, "" if held_by_both == 1 else "s"))
    for flag, side in one_side:
        print("%s is held by %s alone, and compared for no design" % (flag, side))
    for design in designs:
        if design in differs:
            print("\ndesign %s" % design)
            print("\n".join("  " + line for line in differs[design]))
    if "" in differs:
        print("\nthe workstack, read of a plans folder whole")
        print("\n".join("  " + line for line in differs[""]))
    listed = [d for d in designs if d in differs]
    print("\n%d design%s read differently, of %d\n" % (len(listed), "" if len(listed) == 1 else "s", len(designs)))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
