#!/usr/bin/env python3
"""The kept comparison of the design script: which designs a change to the script, or to a form of the canon it reads,
reads differently.

  run with no argument               the designs of the project's own plans folders, each named for a skill
  run with PLANS_FOLDER ...          the designs of the plans folders given, with their reports

It stands in the design script's set of kept tests, whose shared module says which files are the design script's: the
design script runs it where a change holds one of them, and the runner takes it for no test.

It runs each action of the design script that reads a design over the same design documents and reports by each of its
sides: the script as the last commit held it, and the script as it stands. Each side is a copy of the project's files, which
version control makes as a worktree at the last commit under .ai/tmp/worktrees/ of the project the comparison is run
in, and removes as the run ends. The side at the last commit is that copy as it is made. The side as it stands is a
copy with the project's uncommitted work laid over it: each file changed or new copied in, and each file removed
taken out, so its changes show against the last commit as they do in the project. So each script reads the canon of
its own copy, the forms it reads as it runs among them, and each reads the last commit wherever the design script
does. No commit is made. The design documents of each plans folder given, and the reports and diagnoses in each
design's folder, are put into both copies at their own places, where version control tracks none of them, so
neither side reads the project's plans folders. The run writes nothing in the project but those copies, which it
removes whatever happens, a copy an earlier run left at either place removed first. It needs no second copy
made by hand. Where the project is under no version control, or holds no commit, the comparison cannot be made.

Each copy is given the index the project's search kept, where the project holds one and that side's
search writes the same form of index, so a side's search runs through the model only the passages its own copy holds
that the project's did not. The index given leaves each side's reading resting on its own copy's files alone, as
`seed_index` says. No model's files are copied: a search run in a copy finds them where the project root keeps them.

The actions are taken from each side's own table of flags: each check and each show taking a design or a proposal,
`--check-settled-report` over each report a design's log names, and each check and each show of a plans folder. An
action reading the project's uncommitted work rather than a design is left out, and so is an action writing a file.
An action only one side holds is named once, and compared for no design.

It lists each design the two sides read differently, with each action whose exit status or output differs and the
lines one side gave that the other did not, and no other design. The same lines given in another order are the same
reading. Each listed design stands on a line of its own, `design` and its path, which the design script reads the list
from. The run exits 0 where the comparison was made, whatever it lists, and 2 where it could not be made.

The comparison takes the project from the folder it is run in: the nearest folder at or above the working directory
holding the design script's code, or, run from outside every project, the one holding this file.
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

LIB = Path(".ai") / "skills" / "lib"
RUN_IN = Path.cwd().resolve()
# the project the comparison is run in, or, run from outside every project, the one holding this file
PROJECT = next((p for p in (RUN_IN, *RUN_IN.parents) if (p / LIB / "design_documents.py").is_file()), Path(__file__).resolve().parents[4])
# where the two sides' copies stand, among the project's working files
THEN = PROJECT / ".ai" / "tmp" / "worktrees" / "design-script-comparison-then"
NOW = PROJECT / ".ai" / "tmp" / "worktrees" / "design-script-comparison-now"
# the search's scratch space beside the files it works over, where its index stands, as the search places it
SEARCH_SCRATCH = Path(".ai") / "tmp" / "search-spec-of-record-scope"
# the actions reading the project's uncommitted work rather than a design: the side as it stands holds that work and
# the side at the last commit holds none, so each would list every design for the work alone
READS_THE_WORK = ("--check-work", "--check-changed-files", "--check-audits")
SHOWN = 8  # the differing lines shown of one action's output

# Runs in a copy of the project's files, by that copy's design script, each action reading a design, and prints what each gave.
SIDE = r'''
import contextlib, io, json, sys
from pathlib import Path
sys.dont_write_bytecode = True
side = Path(sys.argv[1])
sys.path.insert(0, str(side / ".ai" / "skills" / "lib"))
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
    """Remove the worktree holding a side's copy, registered or left as a bare folder, so none stands or stays registered
    at its place."""
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


def lay_over(side):
    """Lay the project's uncommitted work over a copy of its files at the last commit: each file changed against the last
    commit or new copied in, and each file the work removed taken out."""
    listed = [git("diff", "--name-only", "-z", "HEAD"), git("ls-files", "--others", "--exclude-standard", "-z")]
    if any(run.returncode for run in listed):
        raise RuntimeError("the project's uncommitted work could not be listed: " + " ".join(run.stderr.strip() for run in listed))
    for path in sorted({p for run in listed for p in run.stdout.split("\0") if p}):
        if (PROJECT / path).is_file():
            (side / path).parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(PROJECT / path, side / path)
        elif (side / path).is_file():
            (side / path).unlink()


def seed_index(side):
    """Give a side's copy the index the project's search kept, so its side's search runs through the model only
    the passages its own files hold that the project's did not -> whether it was given one. The search keeps a vector
    for each passage's text, and what each content holds under that content's own hash, so what the index given holds of a
    content is true of that content wherever it stands. Which content stands at which path is the side's own to say:
    the index is given with the time each file as it stood was changed set to none, so the side's search reads and
    hashes every file of its own, keeps what the index holds of a content its files hold, and takes out what it
    holds of a content they do not. An answer the search kept is reused by the search only under the snapshot
    code of the files it now reads and the code of its own reading. A side whose search writes another form of the
    index, or names another model, is given none and builds its own, and so is each side where the project holds no
    index. The index is copied through the database itself, so it is whole whatever is writing the project's index."""
    kept, code = PROJECT / SEARCH_SCRATCH / "index.sqlite", side / LIB / "search.py"
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
        (side / SEARCH_SCRATCH).mkdir(parents=True, exist_ok=True)
        copy = sqlite3.connect(side / SEARCH_SCRATCH / "index.sqlite")
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


def give(side, folders):
    """Copy the designs of each plans folder given, with their reports and diagnoses, into a side's copy at their own places,
    and -> what a side is asked to read: [(the plans folder, [(a design, its reports)])], each as a path in the copy."""
    asked = []
    for plans in folders:
        own, designs = Path(".ai") / "plans" / plans.name, []
        (side / own).mkdir(parents=True, exist_ok=True)
        for design, kept in designs_of(plans):
            shutil.copyfile(design, side / own / design.name)
            at = Path(".ai") / "tmp" / plans.name / design.stem
            for folder in kept:
                shutil.copytree(folder, side / at / folder.name)
            reports = sorted((side / at / "reports").glob("*/*.md")) if (side / at / "reports").is_dir() else []
            designs.append(((own / design.name).as_posix(), [r.relative_to(side).as_posix() for r in reports if r.stem.isdigit()]))
        asked.append((own.as_posix(), designs))
    return asked


def read_by(side, asked):
    """-> what the design script of a side's copy gave for each action reading a design: {"flags", "runs"}, the script
    run in its copy."""
    ran = subprocess.run([sys.executable, "-c", SIDE, str(side)], cwd=side, capture_output=True,
                         input=json.dumps({"folders": asked, "skipped": READS_THE_WORK}).encode("utf-8"),
                         env=dict(os.environ, PYTHONDONTWRITEBYTECODE="1", PYTHONIOENCODING="utf-8"))
    if ran.returncode:
        raise RuntimeError("the design script of %s could not be run:\n%s" % (side.name, ran.stderr.decode("utf-8", "replace")))
    return json.loads(ran.stdout.decode("utf-8"))


def as_read(text, side):
    """-> an action's output with the place of the side's copy taken out of it, so two sides' outputs compare."""
    for place in (str(side), side.as_posix(), str(side.resolve()), side.resolve().as_posix()):
        text = text.replace(place, "<files>")
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
    # given none, the project's own plans folders: each folder of its plans named for a skill it holds
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
        for side in (THEN, NOW):
            add_worktree(side)
        lay_over(NOW)
        for side in (THEN, NOW):
            asked = give(side, folders)
            seed_index(side)
        # the two sides share nothing, so they are read at once
        with concurrent.futures.ThreadPoolExecutor(max_workers=2) as sides:
            then, now = sides.map(lambda side: read_by(side, asked), (THEN, NOW))
        differs, one_side = compare(then, now)
    except RuntimeError as failed:
        sys.stderr.write("design-script-comparison could not be made: %s\n" % failed)
        return 2
    finally:
        for side in (THEN, NOW):
            remove_worktree(side)
    designs = [design for _, held in asked for design, _ in held]
    held_by_both = len([f for f in now["flags"] if f in then["flags"]])
    print("== design-script-comparison: the design script as the last commit, %s, held it beside the script as it stands, "
          "each reading the canon of its own copy of the project's files" % head.stdout.strip()[:10])
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
