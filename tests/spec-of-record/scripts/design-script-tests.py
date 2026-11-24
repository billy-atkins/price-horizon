#!/usr/bin/env python3
"""The kept tests of the design script, .ai/skills/lib/design_documents.py, run through the two entry scripts that
call it, .ai/skills/design-specs/scripts/design-specs.py and .ai/skills/implement-specs/scripts/implement-specs.py.

  design-script-tests.py                 every suite but the two slow ones, faults and worktree
  design-script-tests.py --all           those two too, each taking some minutes more
  design-script-tests.py NAME ...        the suites named, a suite by its name with or without `_suite`, as `faults` or `worktree`
  design-script-tests.py --only WORDS    of the suites run, the tests whose name holds WORDS alone
  design-script-tests.py --test NAME     the test of that name alone, a flag given once for each test
  design-script-tests.py --tree FOLDER   the entry scripts of another tree, a copy of the checkout holding a fault

Each test drives the script as a design's work does: an entry script run as a process of its own, in a project made
for the test in a folder outside the checkout. A project holds a copy, taken as the test runs, of the canon of the
checkout the tests are run in, specs/AGENTS.md and specs/methodology/, so each form the script reads is the one that
checkout's canon declares, and a change to a form reaches the tests. Beside the canon it holds only what the test
gives it: design documents, reports, diagnoses and other files built from the base files under
tests/spec-of-record/scenarios/design-script/. No test reads the checkout's plans folders, what the checkout holds
uncommitted, or where the checkout sits. The searched suite holds the tests a real search answers: it has the search
read one project once, and gives each of its tests a copy of that project with the index the search built.

COVERAGE maps each action of the design script, a row of its FLAGS, and each Script Check record the canon gives the
design script, to the tests holding it: one in which it passes and one in which it reports. The coverage suite reads
FLAGS and the canon's records as they stand and fails where one of them has no passing or no reporting test in the
table, where the table names a test this file does not hold, and where a test it names did not pass in the run.

The faults suite proves the tests of the faults the design script was once found with: for each, it copies the
checkout's skills and canon to a folder of its own, puts the fault back by a small edit at an anchor, runs the
fault's tests against the copy and requires each to FAIL. A fault whose anchor is not found fails the suite loudly.
It puts back the faults of the search too, .ai/skills/lib/search.py, and requires the search's kept tests, run in the
copy, to fail in the check each breaks.

The worktree suite adds a worktree at the last commit under .ai/tmp/worktrees/ of the checkout, lays the checkout's
uncommitted work over it, runs the default run of these tests and of the search's kept tests there and in the
checkout, and requires each check to give the same result in both. It removes the worktree whatever happens.

A suite prints each check it makes, and the run exits 1 where any failed.
"""
import concurrent.futures
import gc
import os
import re
import shutil
import stat
import subprocess
import sys
import tempfile
import threading
import time
from pathlib import Path

sys.dont_write_bytecode = True

# The files of the script these tests are of: its code, and each file of the canon it reads a form from as it runs.
# A path ending in a slash names each file beneath it. The design script's kept comparison names the same files.
SCRIPT_FILES = (".ai/skills/lib/", ".ai/skills/design-specs/scripts/", ".ai/skills/implement-specs/scripts/")
FORM_FILES = ("specs/methodology/working-files/main.md", "specs/methodology/design-workflow/order-of-a-designs-work.md", "specs/methodology/modeling-constructs.md",
              "specs/methodology/expressions.md", "specs/methodology/spec-style/markdown.md", "specs/methodology/skills/registered-skills.md")

LIB = Path(".ai") / "skills" / "lib"
RUN_IN = Path.cwd().resolve()
# the checkout the tests are run in, or, run from outside every checkout, the one holding this file
PROJECT = next((p for p in (RUN_IN, *RUN_IN.parents) if (p / LIB / "design_documents.py").is_file()), Path(__file__).resolve().parents[3])
SCENARIOS = PROJECT / "tests" / "spec-of-record" / "scenarios" / "design-script"
# the tree whose entry scripts the tests run: the checkout's own, or a copy holding a fault
TREE = PROJECT
ONLY = ""
# the canon a project is given: the files a design's form is read from
CANON = ("specs/AGENTS.md", "specs/architecture.md", "specs/index.md", "specs/methodology")

NOW = threading.local()
RESULTS = {}   # a test's name -> whether each of its checks passed, for the coverage suite
FAILED = []
MADE = []      # the folders made outside the checkout, removed as the run ends
LOCK = threading.Lock()


def check(name, holds, detail=""):
    NOW.checks.append((name, bool(holds), detail))


def base(name):
    return (SCENARIOS / name).read_text(encoding="utf-8").replace("\r\n", "\n")


def git(root, *args):
    done = subprocess.run(["git", "-c", "user.name=design-script-tests", "-c", "user.email=design-script-tests@example.invalid",
                           "-c", "core.autocrlf=false", "-c", "commit.gpgsign=false", "-c", "init.defaultBranch=main"] + list(args),
                          cwd=root, capture_output=True, text=True, encoding="utf-8")
    if done.returncode:
        raise AssertionError("git %s: %s" % (" ".join(args), done.stderr))
    return done.stdout.strip()


def outside(name):
    """-> a new folder outside this checkout, so nothing above it is this project's repository."""
    folder = Path(tempfile.mkdtemp(prefix="dst-" + name[:24] + "-")).resolve()
    with LOCK:
        MADE.append(folder)
    return folder


def clear(folder):
    """Remove a folder made outside the checkout, git's own read-only files among it."""
    def writable(function, path, _):
        try:
            os.chmod(path, stat.S_IWRITE)
            function(path)
        except OSError:
            pass
    shutil.rmtree(folder, onerror=writable)


def copy_canon(source, root):
    for rel in CANON:
        if (source / rel).is_dir():
            shutil.copytree(source / rel, root / rel, ignore=shutil.ignore_patterns("__pycache__"))
        elif (source / rel).is_file():
            (root / rel).parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source / rel, root / rel)


# ---------------------------------------------------------------- a design document made for a test

NAME = "ferry-times-in-the-guide"
GOAL = "guide-says-when-the-ferry-runs"
OUTCOME = "crossing-planned-from-the-guide"
OBJECTIVE = "section-gives-the-first-and-last-crossing"
STEP = "ferry-times-stated"
NOT_STATED, NOT_DRAFTED = "Not yet stated.", "Not yet drafted."
CHECKS = ("design-refactor-refine", "self-review", "handed-off-judgment", "adversarial-review", "post-apply-review",
          "audit-specs", "verify-spec-implementation")
ROUNDS = ("adversarial-review", "post-apply-review", "audit-specs", "verify-spec-implementation")


def field(text, key, value):
    """-> a design's text with one field of its header set, or, value None, taken out."""
    head, sep, rest = text.partition("\n## ")
    lines = head.split("\n")
    at = next((i for i, l in enumerate(lines) if l.startswith("**%s:**" % key)), None)
    if at is None:
        raise AssertionError("the design holds no %s field" % key)
    if value is None:
        del lines[at]
    else:
        lines[at] = "**%s:** %s%s" % (key, value, " \\" if lines[at].endswith("\\") else "")
    return "\n".join(lines) + sep + rest


def part(text, title, body):
    """-> a text with the body under one of its headings replaced, the heading given with its marks, or, body None,
    the heading taken out with it."""
    lines = text.split("\n")
    at = lines.index(title)
    level = len(title.split(" ")[0])
    end = next((i for i in range(at + 1, len(lines)) if re.match(r"#{1,%d} " % level, lines[i])), len(lines))
    new = [] if body is None else [title, ""] + body.strip("\n").split("\n") + [""]
    return "\n".join(lines[:at] + new + lines[end:])


def a_log(entries):
    """-> (a log's records, the version it gives): entries, each (kind, {field: value}), written as the design script
    appends them, each with its count among its kind, a time after the one before it, and the version of the design
    its work read, a check's the version as it stood before it unless its fields give one."""
    version, agreed, counts, out = (0, 1, 0), False, {}, []
    for n, (kind, fields) in enumerate(entries):
        fields = dict(fields)
        before = version
        if kind == "design-reassessment" or (kind == "reassessment" and fields.get("Decision") != "go on"):
            version = (version[0] + 1, 0, 0) if version[0] else version
        elif kind == "goals-agreed":
            version = version if version[0] else (1, 0, 0)
        elif kind == "steer" and fields.pop("material", False):
            version = (version[0], version[1] + 1, 0)
        elif kind == "plan-change":
            version = (version[0], version[1], version[2] + 1)
        fields.pop("material", None)
        counts[kind] = counts.get(kind, 0) + 1
        at = fields.pop("Design Version", "%d.%d.%d" % (before if kind in CHECKS else version))
        if kind in CHECKS:
            given = {"Model": "a model", "Effort": "medium", "Design Flaws": "0", "Implementation Flaws": "0", "Nits": "0", "Dropped": "0"}
            if kind in ROUNDS:
                given["Led To"] = "validating"
            if kind == "audit-specs":
                given["Settled Sub-scopes"] = "documentation"
            given.update(fields)
            fields = given
        own = ["- **Entry:** %s-%d" % (kind, counts[kind]), "  **Timestamp:** 2026-01-01T00:%02d:%02dZ" % (n // 60, n % 60)]
        own += [] if at == "0.1.0" else ["  **Design Version:** " + at]
        own += ["  **%s:** %s" % f for f in fields.items()]
        out.append("\n".join("  " + l + (" \\" if i < len(own) - 1 else "") for i, l in enumerate(own)))
    return "\n\n".join(out), "%d.%d.%d" % version


def a_design(name=NAME, status="in-progress", depends="none", log=(), skill="design-specs", stamped=None, **changes):
    """-> the text of a design document made from the base design: its Name, its Status and its Depends On Designs as
    given, its log holding the entries given and its header the version they give. `not-started` gives it no goals, no
    frame and no steps yet. Each other change names a field of the header to set, or, None, to take out. stamped says
    whether its Validated holds a stamp of its content: by default where its Status asks one."""
    text = base("design.md").replace(NAME, name)
    if status == "not-started":
        text = part(text, "## Design Goals", NOT_STATED)
        for title in ("### Scope", "### Assessed Areas", "### Approach", "### Frame Outcomes"):
            text = part(text, title, NOT_STATED)
        text = part(text, "## Design Plan Steps", NOT_DRAFTED)
        text = field(text, "Target", "none")
    text = field(field(text, "Status", status), "Depends On Designs", depends)
    if skill == "implement-specs":
        text = field(field(text, "Kind", "code"), "Target", "`src/ferry.py`").replace(".ai/tmp/design-specs/", ".ai/tmp/implement-specs/")
        for key in ("Area", "What"):
            text = text.replace("**%s:** `docs/guide.md § The Ferry`" % key, "**%s:** `src/ferry.py`" % key)
    for key, value in changes.items():
        text = field(text, key.replace("_", " "), value)
    if log:
        records, version = a_log(log)
        text = text.replace("\n## Out of Scope", "\n## Design Log Entries\n\n**Records:**\n%s\n\n## Out of Scope" % records)
        if version != "0.1.0":
            text = text.replace("**Name:** %s \\\n" % name, "**Name:** %s \\\n**Version:** %s \\\n" % (name, version))
    if stamped if stamped is not None else status in ("approved", "applying", "complete"):
        text = field(text, "Validated", "2026-01-01T00:00:00Z " + own_lib().content_hash(text))
    return text


_LIB = []


def own_lib():
    """-> the design script's code as the checkout the tests are run in holds it, imported to work out a stamp's hash
    for a design made for a test, which no entry script gives without the whole validation review."""
    with LOCK:
        if not _LIB:
            sys.path.insert(0, str(PROJECT / LIB))
            import design_documents
            _LIB.append(design_documents)
    return _LIB[0]


AGREED = (("entered", {"Reason": "taken up"}), ("goals-agreed", {}))
DRAFTED = AGREED + (("plan-change", {}),)
APPROVED = DRAFTED + (("plan-approval", {"Approval": "approved"}),)
APPLYING = APPROVED + (("apply", {}),)


class Project:
    """A project made for a test, in a folder outside the checkout: the canon of the checkout the tests are run in,
    a guide of its own for a design to change, and what the test puts in it."""

    def __init__(self, name, versioned=False, canon=True, under=None):
        self.root = outside(name)
        if under:  # a checkout kept beneath another folder's files, as a worktree is kept beneath a checkout's
            self.root = self.root / under
            self.root.mkdir(parents=True)
        if canon:
            copy_canon(PROJECT, self.root)
        self.put("docs/guide.md", base("guide.md"))
        self.versioned = versioned
        if versioned:
            git(self.root, "init", "-q")
            self.commit()

    def put(self, rel, text):
        f = self.root / rel
        f.parent.mkdir(parents=True, exist_ok=True)
        f.write_text(text, encoding="utf-8", newline="\n")
        return rel

    def read(self, rel):
        return (self.root / rel).read_text(encoding="utf-8").replace("\r\n", "\n")

    def commit(self):
        git(self.root, "add", "-A")
        git(self.root, "commit", "-q", "--allow-empty", "-m", "a commit made for a test")

    def design(self, name=NAME, skill="design-specs", folder=None, text=None, **given):
        """Write a design document into a plans folder, or into the folder given -> its path from the root."""
        return self.put("%s/%s.md" % (folder or ".ai/plans/" + skill, name), text if text is not None else a_design(name, skill=skill, **given))

    def run(self, *args, skill="design-specs"):
        """-> (the exit status, what it printed) of an entry script of the tree under test, run in this project as a
        design's work runs it."""
        entry = TREE / ".ai" / "skills" / skill / "scripts" / (skill + ".py")
        ran = subprocess.run([sys.executable, str(entry)] + [str(a) for a in args], cwd=self.root, capture_output=True,
                             env=dict(os.environ, PYTHONIOENCODING="utf-8", PYTHONDONTWRITEBYTECODE="1"))
        return ran.returncode, (ran.stdout + ran.stderr).decode("utf-8", "replace").replace("\r\n", "\n")

    def held(self, under=".ai/plans"):
        """-> {path: bytes} of each file under a folder, to compare before and after an action."""
        return {p.relative_to(self.root).as_posix(): p.read_bytes() for p in sorted((self.root / under).rglob("*")) if p.is_file()}


# ---------------------------------------------------------------- a report made for a test

SKILLS = ("design-specs", "implement-specs")
BUILDER_PARTS = ("## Hand-back", "## Script Output", "## Causes", "## Settlement")


def report_at(kind, n=1, name=NAME, skill="design-specs"):
    return ".ai/tmp/%s/%s/reports/%s/%d.md" % (skill, name, kind, n)


def a_report(which, name=NAME, skill="design-specs", entry=None, version=None):
    """-> the text of a report made from a base report, research, review or self-review, for the design and the entry
    given, its Reading holding the version given."""
    text = base(which + "-report.md").replace(NAME, name)
    if skill != "design-specs":
        text = text.replace(".ai/plans/design-specs/", ".ai/plans/%s/" % skill).replace(".ai/tmp/design-specs/", ".ai/tmp/%s/" % skill)
        if which == "research":
            text = text.replace("`docs/guide.md § The Ferry`", "`src/ferry.py`")
    if entry:
        text = re.sub(r"^\*\*Entry:\*\* .*$", lambda m: "**Entry:** " + entry, text, count=1, flags=re.M)
    if version:
        text = re.sub(r"^\*\*Design Version:\*\* \S+", lambda m: "**Design Version:** " + version, text, count=1, flags=re.M)
    return text


def cold_part(text):
    """-> the parts of a report its cold agent writes: the text before the first part the builder writes."""
    at = min([text.index("\n" + h) for h in BUILDER_PARTS if "\n" + h in text] or [len(text)])
    return text[:at].rstrip("\n") + "\n"


def builder_part(text):
    """-> the parts of a report the builder writes: its Causes and its Settlement."""
    at = min([text.index("\n" + h) for h in BUILDER_PARTS if "\n" + h in text] or [len(text)])
    return text[at:].strip("\n") + "\n"


def swap(text, was, now, count=1):
    """-> a text with one thing changed, the test failing where what it changes is not there."""
    if text.count(was) < 1:
        raise AssertionError("the text made for the test does not hold: " + was)
    return text.replace(was, now, count)


def taken_up(p, kind, text, n=1, name=NAME, skill="design-specs", settle=True):
    """Put a cold agent's report into a design's folder as it was handed back, take it up by the entry script, and,
    settle, add the parts the builder writes -> its path. The test fails where the take-up reports."""
    path = p.put(report_at(kind, n, name, skill), cold_part(text))
    got = p.run("--take-up-report", path, skill=skill)
    if got[0]:
        raise AssertionError("a report made for the test was not taken up: " + shown(got))
    if settle:
        p.put(path, p.read(path).rstrip("\n") + "\n\n" + builder_part(text))
    return path


CHECK_FIELDS = ("Model=a model", "Effort=medium")
ROUND_FIELDS = CHECK_FIELDS + ("Led To=validating",)


def passes(got, heading, said=""):
    """Whether a run passed: exit 0, the heading of the action it ran, and what it is to say."""
    code, out = got
    return code == 0 and heading in out and said in out


def reports(got, heading, said, status=1):
    """Whether a run reported what its check reports: the exit status, the heading of the action, and a distinctive
    part of the message of the check driven, so another check firing does not pass the test."""
    code, out = got
    return code == status and heading in out and all(s in out for s in ([said] if isinstance(said, str) else said))


def shown(got):
    return "exit %s\n%s" % (got[0], got[1][-1500:])


TESTS = {}   # a test's name -> its function, in the order written
SUITES = {}  # a suite's name -> the names of its tests


def test(suite, name):
    def keep(function):
        if name in TESTS:
            raise AssertionError("two tests share the name " + name)
        TESTS[name] = function
        SUITES.setdefault(suite, []).append(name)
        return function
    return keep


# ---------------------------------------------------------------- the form of a design

@test("form", "check-design-form passes a design in its form")
def _():
    p = Project("form")
    for status, log in (("not-started", ()), ("in-progress", AGREED), ("in-progress", DRAFTED), ("approved", APPROVED), ("applying", APPLYING)):
        got = p.run("--check-design-form", p.design(status=status, log=log))
        check("--check-design-form passes a design made for the tests, %s with %d log entries" % (status, len(log)),
              passes(got, "== check-design-form " + NAME, "0 problems"), shown(got))


@test("form", "check-design-form reports a field out of the form")
def _():
    p = Project("form-field")
    got = p.run("--check-design-form", p.design(text=a_design().replace("**Spawned By:** none \\\n", "**Spawned By:** none \\\n**Reviewed By:** nobody \\\n")))
    check("--check-design-form reports a header holding a field its form does not take, naming the field",
          reports(got, "== check-design-form " + NAME, ["its header", "Reviewed By"]), shown(got))


RESEARCH = (("handed-off-judgment", {}),)
APPROVED_RESEARCHED = AGREED + RESEARCH + (("plan-change", {}), ("plan-approval", {"Approval": "approved"}))
APPLYING_RESEARCHED = APPROVED_RESEARCHED + (("apply", {}),)


def researched(p, name=NAME, skill="design-specs", **given):
    """Write a design whose log names its research, with that research's report in its folder -> the design's path."""
    p.put(report_at("handed-off-judgment", 1, name, skill), a_report("research", name, skill))
    return p.design(name, skill=skill, **given)


@test("designs", "check-cited-headings passes a design citing a heading that stands")
def _():
    for skill in SKILLS:
        p = Project("cited")
        got = p.run("--check-cited-headings", p.design(skill=skill, log=DRAFTED), skill=skill)
        check("--check-cited-headings of %s passes a design whose every cited heading stands" % skill,
              passes(got, "== check-cited-headings", "1 citation, 0 broken"), shown(got))


@test("designs", "check-cited-headings reports a heading that does not stand")
def _():
    for skill in SKILLS:
        p = Project("cited-broken")
        text = swap(a_design(skill=skill, log=DRAFTED), "and `docs/guide.md § The Ferry` names", "and `docs/guide.md § The Harbour` names")
        got = p.run("--check-cited-headings", p.design(skill=skill, text=text), skill=skill)
        check("--check-cited-headings of %s reports a cited heading its file does not hold, as broken" % skill,
              reports(got, "== check-cited-headings", ["BROKEN", "§ The Harbour", "no such heading", "1 broken"]), shown(got))
    p = Project("cited-none")
    got = p.run("--check-cited-headings", p.put("notes.md", "# Notes\n\nNo citation stands here.\n"))
    check("--check-cited-headings of a proposal citing nothing says so and exits 2", got[0] == 2 and "no cross-file citations found" in got[1], shown(got))


@test("designs", "check-target-kind passes a Target of the design's Kind")
def _():
    p = Project("kind")
    got = p.run("--check-target-kind", p.design(log=DRAFTED))
    check("--check-target-kind passes a documentation design whose Target names the guide", passes(got, "== check-target-kind " + NAME, "0 problems"), shown(got))
    got = p.run("--check-target-kind", p.design("code-design", skill="implement-specs", log=DRAFTED), skill="implement-specs")
    check("--check-target-kind of implement-specs passes a code design whose Target names a file of no other kind",
          passes(got, "== check-target-kind code-design", "0 problems"), shown(got))


@test("designs", "check-target-kind reports a Target of another kind")
def _():
    p = Project("kind-strays")
    got = p.run("--check-target-kind", p.design(log=DRAFTED, Target="`docs/guide.md`; `specs/methodology/code.md`"))
    check("--check-target-kind reports a canon file in a documentation design's Target",
          reports(got, "== check-target-kind " + NAME, "Target names a canon-specs file in a documentation design: specs/methodology/code.md"), shown(got))
    got = p.run("--check-target-kind", p.design(log=DRAFTED, Target="`.ai/follow-ups.md`"))
    check("--check-target-kind reports a working file in a Target",
          reports(got, "== check-target-kind " + NAME, "Target names a working file, which no design changes: .ai/follow-ups.md"), shown(got))


@test("designs", "check-design passes an approved design whose research its log names")
def _():
    for skill in SKILLS:
        p = Project("validation")
        got = p.run("--check-design", researched(p, skill=skill, status="approved", log=APPROVED_RESEARCHED), skill=skill)
        check("--check-design of %s passes an approved design in its form, each Assessed Area resting on the research its log names" % skill,
              passes(got, "== check-design " + NAME, "0 problems"), shown(got))


@test("designs", "check-design reports a design not yet stated")
def _():
    p = Project("validation-reports")
    got = p.run("--check-design", p.design(status="not-started"))
    check("--check-design reports the goals, the frame and the steps a design has yet to state",
          reports(got, "== check-design " + NAME, ["its design goals are not yet stated", "its design frame's Scope is not yet stated", "its steps are not yet drafted"]), shown(got))
    got = p.run("--check-design", p.design(status="approved", log=APPROVED_RESEARCHED))
    check("--check-design reports an Assessed Area resting on a report that does not stand in the design's folder",
          reports(got, "== check-design " + NAME, "has no Read Assessment of its Area in the reports the validation review reads"), shown(got))


@test("designs", "show-dependents lists the parts naming a part")
def _():
    p = Project("dependents")
    design = p.design(log=DRAFTED)
    got = p.run("--show-dependents", design, GOAL)
    check("--show-dependents lists each part of the design naming a goal: its case, its principle, its Frame Outcome and its step Objective",
          passes(got, "== show-dependents %s %s (goal %s)" % (NAME, GOAL, GOAL), "4 parts name or cite " + GOAL)
          and all(w in got[1] for w in ("case visitor-planning-a-crossing", "principle times-stated-where-the-ferry-is-named", "frame outcome " + OUTCOME, OBJECTIVE)), shown(got))
    got = p.run("--show-dependents", design, OUTCOME)
    check("--show-dependents lists the one step Objective upholding a Frame Outcome", passes(got, "== show-dependents", "1 part names or cites " + OUTCOME), shown(got))


@test("designs", "show-dependents refuses a name the design does not hold")
def _():
    p = Project("dependents-none")
    got = p.run("--show-dependents", p.design(log=DRAFTED), "no-such-part")
    check("--show-dependents refuses a Name no part of the design takes, exit 2",
          got[0] == 2 and "holds no goal, case, principle, Frame Outcome, step or step Objective named no-such-part" in got[1], shown(got))


@test("designs", "show-validation shows a design validated")
def _():
    p = Project("shown-validated")
    got = p.run("--show-validation", p.design(status="approved", log=APPROVED))
    check("--show-validation shows a design whose stamp matches its content as validated", passes(got, "== show-validation", NAME + ": validated; stamped sha256:"), shown(got))


@test("designs", "show-validation shows a design stale or never stamped")
def _():
    p = Project("shown-stale")
    got = p.run("--show-validation", p.design(log=DRAFTED))
    check("--show-validation shows a design holding no stamp as never stamped", passes(got, "== show-validation", NAME + ": never stamped; stamped none"), shown(got))
    text = swap(a_design(status="approved", log=APPROVED), "without saying when it runs.", "without saying when it runs, or from where.")
    got = p.run("--show-validation", p.design(text=text))
    check("--show-validation shows a design edited since its stamp as stale", passes(got, "== show-validation", NAME + ": stale; stamped sha256:"), shown(got))


@test("designs", "stamp-validation stamps a design the validation review passes")
def _():
    for skill in SKILLS:
        p = Project("stamp")
        text = swap(a_design(skill=skill, status="applying", log=APPLYING_RESEARCHED), "without saying when it runs.", "without saying when it runs, or from where.")
        design = researched(p, skill=skill, text=text)
        was = p.run("--show-validation", design, skill=skill)
        got = p.run("--stamp-validation", design, skill=skill)
        now = p.run("--show-validation", design, skill=skill)
        check("--stamp-validation of %s writes the stamp of a design the validation review passes, which then reads validated" % skill,
              ": stale;" in was[1] and passes(got, "== stamp-validation\n**Validated:** ") and ": validated;" in now[1], shown(got) + shown(now))
        again = p.run("--stamp-validation", design, skill=skill)
        check("--stamp-validation of %s leaves a current stamp as it stands" % skill, passes(again, "== stamp-validation", "already validated, the stamp current"), shown(again))


@test("designs", "stamp-validation refuses a design the validation review reports")
def _():
    p = Project("stamp-refused")
    design = p.design(log=AGREED, text=part(a_design(log=AGREED), "## Design Plan Steps", NOT_DRAFTED))
    before = p.held()
    got = p.run("--stamp-validation", design)
    check("--stamp-validation refuses a design whose steps are not yet drafted, and writes nothing",
          reports(got, "== stamp-validation, not stamped", "its steps are not yet drafted") and p.held() == before, shown(got))
    kept = p.design(folder=".ai/plans/design-specs/archive", status="applying", log=APPLYING)
    before = p.held()
    got = p.run("--stamp-validation", kept)
    check("--stamp-validation refuses a design standing in no plans folder, and writes nothing",
          reports(got, "== stamp-validation, not stamped", "it stands in no plans folder") and p.held() == before, shown(got))


# ---------------------------------------------------------------- a design naming another

# the designs a name can be of: one standing unfinished in a plans folder, two standing there finished, and one
# standing in none; and what each name is read as
UNFINISHED, COMPLETE, ABANDONED, ABSENT = "quay-rebuilt", "harbour-dredged", "pier-closed", "tide-tables-printed"
READ_AS = {UNFINISHED: "unfinished", COMPLETE: "finished", ABANDONED: "finished", ABSENT: "gone"}
# each state of a design naming another: its Status, its log, and whether its steps are drafted
NAMING = {
    "not started": ("not-started", (), False),
    "in progress before its goals": ("in-progress", (("entered", {"Reason": "taken up"}),), False),
    "in progress after its goals": ("in-progress", DRAFTED, True),
    "waiting at its frame": ("in-progress", AGREED, False),
    "approved": ("approved", APPROVED, True),
    "applying": ("applying", APPLYING, True),
    "complete": ("complete", APPLYING, True),
    "abandoned": ("abandoned", AGREED, False),
}
AGREED_STATES = ("in progress after its goals", "waiting at its frame", "approved", "applying")
FINISHED_STATES = ("complete", "abandoned")
FREEING = "its foundation has changed, and no entry is appended to its log until --free-design frees it"


def naming(state, depends, name=NAME, skill="design-specs"):
    """-> the text of a design in one of the states of NAMING, naming the designs given."""
    status, log, drafted = NAMING[state]
    text = a_design(name, status=status, log=log, depends=depends, skill=skill)
    if status != "not-started" and not drafted:
        text = part(text, "## Design Plan Steps", NOT_DRAFTED)
    return text


def a_workstack(name):
    """-> a project holding the designs a name can be of: one in progress, one complete and one abandoned in the
    plans folder, and one in its archive, where no design of the workstack stands."""
    p = Project(name)
    p.design(UNFINISHED, log=AGREED)
    p.design(COMPLETE, status="complete", log=APPLYING)
    p.design(ABANDONED, status="abandoned", log=AGREED)
    p.design(ABSENT, folder=".ai/plans/design-specs/archive", status="complete", log=APPLYING)
    return p


def each_naming(p, test_name):
    """Yield (state, named design, the naming design's path, a label) for each state of a design naming each design a
    name can be of, the naming design written fresh each time."""
    for state in NAMING:
        for named in READ_AS:
            yield state, named, p.design(text=naming(state, named)), "a design %s naming a design %s" % (state, {UNFINISHED: "unfinished", COMPLETE: "complete", ABANDONED: "abandoned", ABSENT: "standing in no plans folder"}[named])


@test("names", "check-design-names reads each name from the plans folders")
def _():
    p = a_workstack("names")
    for state, named, design, label in each_naming(p, "names"):
        got = p.run("--check-design-names", design)
        if state in FINISHED_STATES:
            check("--check-design-names reports nothing of %s, the name its history" % label,
                  passes(got, "== check-design-names " + NAME, "is its history, and nothing follows from it\n0 problems"), shown(got))
        elif READ_AS[named] == "unfinished":
            check("--check-design-names lists %s as blocked, and reports nothing" % label,
                  passes(got, "== check-design-names " + NAME, "blocked by %s, unfinished: it is worked no further than its agreed goals and frame\n0 problems" % named), shown(got))
        else:
            why = "a design of that name stands in a plans folder complete or abandoned" if READ_AS[named] == "finished" else "no design of that name stands in a plans folder"
            check("--check-design-names reports %s as naming a design %s" % (label, READ_AS[named]),
                  reports(got, "== check-design-names " + NAME, ["its Depends On Designs names %s, %s: %s; its foundation has changed" % (named, READ_AS[named], why), "1 problem"]), shown(got))


@test("names", "check-design-names passes a design naming none and reports one in no plans folder")
def _():
    for skill in SKILLS:
        p = a_workstack("names-none")
        got = p.run("--check-design-names", p.design(skill=skill, log=AGREED), skill=skill)
        check("--check-design-names of %s passes a design naming no design" % skill, passes(got, "== check-design-names " + NAME, "0 problems") and "blocked by" not in got[1], shown(got))
        got = p.run("--check-design-names", p.design(skill=skill, folder=".ai/plans/%s/archive" % skill, log=AGREED, depends=COMPLETE), skill=skill)
        check("--check-design-names of %s reports a design standing in an archive as standing in no plans folder" % skill,
              reports(got, "== check-design-names " + NAME, "it stands in no plans folder, so it is read as no design of the workstack and written by no action"), shown(got))
    p = a_workstack("names-two")
    got = p.run("--check-design-names", p.design(log=AGREED, depends="%s; %s; %s" % (UNFINISHED, COMPLETE, ABSENT)))
    check("--check-design-names reports each finished and each gone name of a design naming several, with which it is, and lists the unfinished one",
          reports(got, "== check-design-names", ["names %s, finished" % COMPLETE, "names %s, gone" % ABSENT, "blocked by %s, unfinished" % UNFINISHED, "2 problems"]), shown(got))
    got = p.run("--check-design-names", p.design(log=AGREED, depends="implement-specs/" + ABSENT))
    check("--check-design-names reads a name of another skill's plans folder from that folder",
          reports(got, "== check-design-names", "names implement-specs/%s, gone" % ABSENT), shown(got))


@test("names", "show-workstack reads each name from the plans folders")
def _():
    p = a_workstack("stack-shown")
    for state, named, design, label in each_naming(p, "stack-shown"):
        got = p.run("--show-workstack")
        status = NAMING[state][0]
        line = next((l for l in got[1].split("\n") if l.startswith("  " + NAME + " [")), "")
        if state in FINISHED_STATES:
            want = line == "  %s [%s]" % (NAME, status)
            what = "shows nothing of the name of"
        elif READ_AS[named] == "unfinished":
            want = line.startswith("  %s [%s, blocked by %s" % (NAME, status, named)) and "waiting to be freed" not in line
            what = "shows as blocked"
        else:
            want = line.startswith("  %s [%s, waiting to be freed of %s %s" % (NAME, status, named, READ_AS[named])) and "blocked by" not in line \
                and "\n  free: %s [" % NAME in got[1]
            what = "shows as waiting to be freed, and to free first,"
        check("--show-workstack %s %s" % (what, label), got[0] == 0 and "== show-workstack\nWorkstack:" in got[1] and want, line + "\n" + shown(got))
    check("--show-workstack lists each finished design as one that may be deleted or moved, and none standing in the archive",
          "Finished, each one a design that may be deleted or moved at any time:\n" in got[1] and "  %s\n  %s\n" % (COMPLETE, ABANDONED) in got[1].split("Finished, each one")[1]
          and ABSENT not in got[1], shown(got))


@test("names", "check-workstack reads each name from the plans folders")
def _():
    p = a_workstack("stack-checked")
    for state, named, design, label in each_naming(p, "stack-checked"):
        got = p.run("--check-workstack")
        status = NAMING[state][0]
        if status in ("approved", "applying") and READ_AS[named] == "unfinished":
            check("--check-workstack reports %s" % label,
                  reports(got, "== check-workstack", ["%s, but its Depends On Designs names %s, unfinished: no agent takes a blocked design past its framing" % (status, named), "1 problem"]), shown(got))
        else:
            check("--check-workstack reports nothing of %s" % label, passes(got, "== check-workstack", "0 problems"), shown(got))


@test("names", "show-workstack and check-workstack read a plans folder given, and refuse a folder that is none")
def _():
    for skill in SKILLS:
        p = a_workstack("stack-folder")
        p.design("code-design", skill="implement-specs", log=AGREED, depends="design-specs/" + UNFINISHED)
        got = p.run("--show-workstack", skill=skill)
        own, other = ("code-design", "design-specs/" + UNFINISHED) if skill == "implement-specs" else ("implement-specs/code-design", UNFINISHED)
        check("--show-workstack of %s names the designs of its own plans folder by their names and those of the folder beside it by that folder" % skill,
              got[0] == 0 and "  %s [in-progress, blocked by %s]" % (own, other) in got[1], shown(got))
        got = p.run("--check-workstack", skill=skill)
        check("--check-workstack of %s passes a workstack in sync" % skill, passes(got, "== check-workstack", "0 problems"), shown(got))
        for flag in ("--show-workstack", "--check-workstack"):
            got = p.run(flag, ".ai/plans/design-specs/archive", skill=skill)
            check("%s of %s refuses a folder that is no plans folder, the archive beneath one among them, exit 2" % (flag, skill),
                  got[0] == 2 and "no plans folder, a skill's plans directory under .ai/plans/" in got[1], shown(got))


@test("names", "check-workstack reports a loop and a field out of the form")
def _():
    p = Project("stack-loop")
    p.design("first", log=AGREED, depends="second")
    p.design("second", log=AGREED, depends="first")
    got = p.run("--check-workstack")
    check("--check-workstack reports designs naming each other in a cycle", reports(got, "== check-workstack", "Depends On Designs runs in a cycle: first -> second -> first"), shown(got))
    p = Project("stack-spawned")
    p.design("first", log=AGREED, Spawned_By="second")
    p.design("second", log=AGREED, Spawned_By="first")
    got = p.run("--check-workstack")
    check("--check-workstack reports designs spawned by each other in a loop", reports(got, "== check-workstack", "Spawned By runs in a loop: first -> second -> first"), shown(got))


# ---------------------------------------------------------------- freeing a design

@test("freeing", "free-design frees a design of each finished or gone name, and reassesses one whose goals are agreed")
def _():
    p = a_workstack("freed")
    for state, named, design, label in each_naming(p, "freed"):
        others = {k: v for k, v in p.held().items() if k != design}
        before = p.read(design)
        got = p.run("--free-design", design)
        now = p.read(design)
        status = NAMING[state][0]
        same = {k: v for k, v in p.held().items() if k != design} == others
        if state in FINISHED_STATES:
            check("--free-design writes nothing to %s" % label, passes(got, "== free-design %s [%s]" % (NAME, status), "so it is never written") and now == before and same, shown(got))
        elif READ_AS[named] == "unfinished":
            check("--free-design writes nothing to %s" % label,
                  passes(got, "== free-design " + NAME, "its Depends On Designs names no finished or gone design, so nothing is written") and now == before and same, shown(got))
        elif state not in AGREED_STATES:
            check("--free-design frees %s of the name, and appends no entry: its goals are not agreed" % label,
                  passes(got, "== free-design " + NAME, ["freed of %s, %s; its Depends On Designs now none" % (named, READ_AS[named])][0])
                  and "its goals are not agreed in its current major version, so no entry is appended" in got[1]
                  and now == before.replace("**Depends On Designs:** " + named, "**Depends On Designs:** none") and same, shown(got))
        else:
            moved = status in ("approved", "applying")
            entries = re.findall(r"- \*\*Entry:\*\* (\S+)", now)[len(NAMING[state][1]):]
            check("--free-design frees %s, which then stands reassessed: at a new major version, in progress, the cause in its log%s"
                  % (label, ", with the entry of its return to in-progress" if moved else ""),
                  passes(got, "== free-design " + NAME, "reassessed, its goals to agree again")
                  and "**Depends On Designs:** none" in now and "**Version:** 2.0.0 \\\n**Status:** in-progress" in now
                  and entries == ["design-reassessment-1"] + (["entered-2"] if moved else [])
                  and "**Design Version:** 2.0.0 \\\n    **Cause:** changed foundation: %s %s\n" % (named, READ_AS[named]) in now
                  and ("**Reason:** freed" in now) == moved and "Decision" not in now.split("design-reassessment-1")[1] and "Diagnosis" not in now and same,
                  shown(got) + now[-900:])
            form = p.run("--check-design-form", design)
            check("and %s, freed, holds the form of a design" % label, passes(form, "== check-design-form " + NAME, "0 problems"), shown(form))
            again = p.run("--check-design-names", design)
            check("and %s, freed, names no finished or gone design, so an entry of its framing is appended to it" % label,
                  passes(again, "== check-design-names", "0 problems") and p.run("--log-entry", design, "goals-agreed")[0] == 0
                  and "**Version:** 2.0.0" in p.read(design), shown(again))


@test("freeing", "no report of the earlier major version binds a design freed and reassessed")
def _():
    for skill in SKILLS:
        p = a_workstack("freed-unbound")
        named = ("" if skill == "design-specs" else "design-specs/") + ABSENT
        design = researched(p, skill=skill, status="approved", log=APPROVED_RESEARCHED)
        bound = p.run("--check-design", design, skill=skill)
        p.put(design, swap(p.read(design), "**Depends On Designs:** none", "**Depends On Designs:** " + named))
        freed = p.run("--free-design", design, skill=skill)
        got = p.run("--check-design", design, skill=skill)
        check("--check-design of %s reads the research of an approved design until it is freed, and, freed of a gone design and reassessed, reads none of it: its Assessed Area rests on a report of no entry of its current major version" % skill,
              passes(bound, "== check-design " + NAME, "0 problems") and passes(freed, "== free-design " + NAME, "moved back from approved to in-progress")
              and reports(got, "== check-design " + NAME, "1 assessed area rests on %s, a report the validation review does not read: no handed-off-judgment entry of the design's current major version names it" % report_at(JUDGMENT, skill=skill))
              and "Read Assessment's Area covers" not in got[1] and "is named by no Search" not in got[1], shown(freed) + shown(got))


@test("freeing", "free-design keeps each unfinished name, and frees a design of another skill's plans folder")
def _():
    for skill in SKILLS:
        p = a_workstack("freed-kept")
        own = lambda n: n if skill == "design-specs" else "design-specs/" + n
        design = p.design(skill=skill, log=DRAFTED, depends="; ".join(own(n) for n in (COMPLETE, UNFINISHED, ABSENT)))
        got = p.run("--free-design", design, skill=skill)
        now = p.read(design)
        check("--free-design of %s removes each finished and each gone name of a design naming several, keeps the unfinished one, and names each in the one Cause" % skill,
              passes(got, "== free-design " + NAME, "freed of %s, finished; %s, gone; its Depends On Designs now %s" % (own(COMPLETE), own(ABSENT), own(UNFINISHED)))
              and "**Depends On Designs:** %s \\" % own(UNFINISHED) in now
              and "**Cause:** changed foundation: %s finished; %s gone\n" % (own(COMPLETE), own(ABSENT)) in now, shown(got))


@test("freeing", "free-design refuses a design in no plans folder")
def _():
    p = a_workstack("freed-outside")
    design = p.design(folder=".ai/plans/design-specs/archive", log=DRAFTED, depends=COMPLETE)
    before = p.held()
    got = p.run("--free-design", design)
    check("--free-design reports a design standing in an archive as standing in no plans folder, and writes nothing",
          reports(got, "== free-design, not freed", "it stands in no plans folder") and p.held() == before, shown(got))
    design = p.design(folder="elsewhere", log=DRAFTED, depends=COMPLETE)
    got = p.run("--free-design", design)
    check("--free-design reports a design standing outside every plans folder the same way", reports(got, "== free-design, not freed", "it stands in no plans folder"), shown(got))
    got = p.run("--free-design", ".ai/plans/design-specs/no-such-file.md")
    check("--free-design of a file that is not there says so, exit 2", got[0] == 2 and "no design document" in got[1], shown(got))


@test("freeing", "no entry is appended before the freeing")
def _():
    p = a_workstack("unfreed")
    kinds = {"entered": ("Reason=reopened",), "goals-agreed": (), "plan-change": (), "user-edit": ("Places=docs/guide.md",), "another-round": (),
             "plan-approval": ("Approval=approved",), "apply": (), "self-review": CHECK_FIELDS, "handed-off-judgment": CHECK_FIELDS}
    for state in NAMING:
        if state in FINISHED_STATES:
            continue
        for named in (COMPLETE, ABANDONED, ABSENT):
            for kind, fields in kinds.items():
                design = p.design(text=naming(state, named))
                before = p.held()
                got = p.run("--log-entry", design, kind, *fields)
                check("--log-entry appends no %s entry to a design %s naming a design %s, until it is freed" % (kind, state, READ_AS[named]) + (" (%s)" % named if named == ABANDONED else ""),
                      reports(got, "== log-entry, not logged", ["its Depends On Designs names %s, %s: " % (named, READ_AS[named]) + FREEING]) and p.held() == before, shown(got))


@test("freeing", "a finished design naming a finished or gone design takes an entry as it stood")
def _():
    p = a_workstack("finished-naming")
    for state in FINISHED_STATES:
        for named in (COMPLETE, ABSENT):
            design = p.design(text=naming(state, named))
            got = p.run("--log-entry", design, "entered", "Reason=reopened")
            check("--log-entry holds nothing back from a design %s for the %s design it names, the name its history" % (state, READ_AS[named]),
                  passes(got, "== log-entry", "**Entry:** entered-") and "**Depends On Designs:** " + named in p.read(design), shown(got))


@test("freeing", "the entries of a freeing are appended by the freeing alone")
def _():
    p = a_workstack("freeing-alone")
    design = p.design(log=DRAFTED)
    before = p.held()
    got = p.run("--log-entry", design, "design-reassessment", "Cause=changed foundation: %s finished" % COMPLETE)
    check("--log-entry refuses a design-reassessment entry whose Cause is a changed foundation, which the freeing alone appends",
          reports(got, "== log-entry, not logged", "an entry of a design freed for a changed foundation, which --free-design alone appends") and p.held() == before, shown(got))
    got = p.run("--log-entry", design, "entered", "Reason=freed")
    check("--log-entry refuses an entered entry whose Reason is freed, which the freeing alone appends",
          reports(got, "== log-entry, not logged", "an entry of a design freed for a changed foundation, which --free-design alone appends") and p.held() == before, shown(got))


# ---------------------------------------------------------------- a design's log

PAST_THE_FRAME = {"plan-change": (), "design-refactor-refine": CHECK_FIELDS, "self-review": CHECK_FIELDS, "another-round": (),
                  "plan-approval": ("Approval=approved",), "step-back": (), "apply": ()}
BLOCKED = "entry begins or continues work past the frame, and its Depends On Designs names %s, unfinished: a blocked design is worked no further than its agreed goals and frame"


def a_clean_report(kind, name=NAME, version="1.0.1", n=1):
    """-> the text of a report of a check that found nothing: a review's, the cold reviewer's Reading and the builder's
    Settlement, or the builder's triage of an audit."""
    text = "# Check's Report\n\n**Design:** %s \\\n**Entry:** %s-%d\n\n## Reading\n\n**Design Version:** %s \\\n" % (name, kind, n, version)
    if kind in ("adversarial-review", "post-apply-review"):
        text += "**Reviewer Readings:**\n  - **Reviewer:** reviewer-1 \\\n    **Collecting Reads:**\n      - `docs/guide.md`\n\n    **Earlier Reports:**\n      - none\n\n" \
                "    **Weighing Reads:**\n      - none\n\n## Settlement\n\n**Ending:** its own settling \\\n**Earlier Reports:**\n  - none\n\n**Settling Reads:**\n  - none\n"
    else:
        text += "**Reads:**\n  - `docs/guide.md`\n\n## Settlement\n\n" + ("**Ending:** its own settling \\\n" if kind != "design-refactor-refine" else "") + "**Earlier Reports:**\n  - none\n"
    return text


def a_diagnosis(name=NAME, entry=1, flaws=True):
    text = swap(base("diagnosis.md").replace(NAME, name), "design-reassessment-1", "design-reassessment-%d" % entry)
    return text


def other_entry(p, design, kind, name=NAME, version="1.0.1"):
    """Make what an entry of a kind that neither begins nor continues work past the frame needs, its report or its
    diagnosis among it -> the fields --log-entry is given for it, or None where the tests give the kind none."""
    given = {"entered": ("Reason=a dependency named",), "goals-agreed": (), "steer": ("Steering Decision=some-steer",), "user-edit": ("Places=docs/guide.md",),
             "passes-choice": ("Choice=feedback",), "direct-edit": ("Places=docs/guide.md",), "audit-bypass": ("Audit=specs",),
             "handed-off-judgment": CHECK_FIELDS, "adversarial-review": ROUND_FIELDS, "post-apply-review": ROUND_FIELDS,
             "audit-specs": ROUND_FIELDS + ("Settled Sub-scopes=documentation",), "verify-spec-implementation": ROUND_FIELDS,
             "design-reassessment": ("Cause=step back: the user's word", "Decision=rescope", "Diagnosis=.ai/tmp/design-specs/%s/diagnosis/1.md" % name)}
    if kind not in given:
        return None
    if kind == "handed-off-judgment":
        taken_up(p, kind, a_report("research", name, version="1.0.0"), name=name)
    elif kind in ("adversarial-review", "post-apply-review"):
        taken_up(p, kind, a_clean_report(kind, name, version), name=name)
    elif kind in ("audit-specs", "verify-spec-implementation"):
        p.put(report_at(kind, 1, name), a_clean_report(kind, name, version))
    elif kind == "design-reassessment":
        p.put(".ai/tmp/design-specs/%s/diagnosis/1.md" % name, a_diagnosis(name))
    return given[kind]


def log_kinds():
    """-> the kinds of entry the canon of the checkout gives a design's log, read from its declaration."""
    return own_lib().log_type(PROJECT)[2]


@test("log", "log-entry appends an entry of each kind in its type")
def _():
    p = Project("log-appended")
    design = p.design(log=AGREED)
    got = p.run("--log-entry", design, "plan-change")
    now = p.read(design)
    check("--log-entry appends an entry, its count among its kind, and writes the version the log then gives to the header",
          passes(got, "== log-entry", "- **Entry:** plan-change-1") and "**Design Version:** 1.0.1" in got[1] and "**Version:** 1.0.1 \\" in now and now.count("**Entry:**") == 3, shown(got))
    form = p.run("--check-design-form", design)
    check("and the design it wrote holds its form", passes(form, "== check-design-form", "0 problems"), shown(form))
    for skill in SKILLS:
        p = Project("log-first")
        design = p.design(skill=skill, status="not-started")
        got = p.run("--log-entry", design, "entered", "Reason=taken up", skill=skill)
        check("--log-entry of %s gives a design holding no log its log's section, where the form puts it" % skill,
              passes(got, "== log-entry", "- **Entry:** entered-1") and "## Design Log Entries\n\n**Records:**\n  - **Entry:** entered-1" in p.read(design)
              and p.read(design).index("## Design Log Entries") < p.read(design).index("## Out of Scope"), shown(got))


@test("log", "log-entry refuses an entry out of its type")
def _():
    p = Project("log-refused")
    design = p.design(log=AGREED)
    before = p.held()
    for label, args, said in (
            ("a kind its type does not give", ("no-such-kind",), "a log entry's kind is not one of"),
            ("a field its kind does not give", ("plan-change", "Reason=because"), "a plan-change entry"),
            ("a value outside its field's Values", ("plan-approval", "Approval=perhaps"), "a plan-approval entry's Approval is not one of approved, approved and apply: perhaps"),
            ("a Reason the entry reason does not take", ("entered", "Reason=sent back for a rest"), "an entered entry's Reason is not one of"),
            ("an old log's reassessment entry", ("reassessment", "Decision=go on"), "a `reassessment` entry, written in no entry now"),
            ("a Cuts Short", ("step-back", "Cuts Short=adversarial-review-1"), "a Cuts Short, written in no entry now"),
            ("a check's entry whose report does not stand", ("self-review",) + CHECK_FIELDS, "a check's entry whose report does not stand in the design's folder: " + report_at("self-review"))):
        got = p.run("--log-entry", design, *args)
        check("--log-entry refuses %s, and writes nothing" % label, reports(got, "== log-entry, not logged", said) and p.held() == before, shown(got))
    got = p.run("--log-entry", design)
    check("--log-entry given no kind says what it takes, exit 2", got[0] == 2 and "--log-entry takes a design document, a kind and the kind's fields as FIELD=VALUE" in got[1], shown(got))
    got = p.run("--log-entry", p.design(folder=".ai/plans/design-specs/archive", log=AGREED), "plan-change")
    check("--log-entry appends no entry to a design standing in no plans folder", reports(got, "== log-entry, not logged", "it stands in no plans folder"), shown(got))


@test("log", "work past the frame is refused on a blocked design")
def _():
    p = a_workstack("blocked")
    check("the tests hold each kind of entry the script refuses a blocked design", set(PAST_THE_FRAME) == set(own_lib().PAST_THE_FRAME), sorted(own_lib().PAST_THE_FRAME))
    for skill in SKILLS:
        named = UNFINISHED if skill == "design-specs" else "design-specs/" + UNFINISHED
        for state in NAMING:
            if state in FINISHED_STATES or (skill == "implement-specs" and state != "in progress after its goals"):
                continue
            for kind, fields in PAST_THE_FRAME.items():
                design = p.design(skill=skill, text=naming(state, named, skill=skill))
                before = p.held()
                got = p.run("--log-entry", design, kind, *fields, skill=skill)
                check("--log-entry of %s refuses a %s entry to a design %s naming an unfinished design" % (skill, kind, state),
                      reports(got, "== log-entry, not logged", kind + " " + BLOCKED % named) and p.held() == before, shown(got))


@test("log", "each other entry is appended to a blocked design")
def _():
    kinds = [k for k in log_kinds() if k not in PAST_THE_FRAME and k != "reassessment"]
    for kind in kinds:
        p = a_workstack("blocked-appended")
        applied = kind in ("post-apply-review", "audit-specs", "verify-spec-implementation", "direct-edit", "audit-bypass", "passes-choice")
        state = "applying" if applied else "in progress after its goals"
        design = p.design(text=naming(state, UNFINISHED))
        fields = other_entry(p, design, kind)
        if fields is None:
            check("the tests give an entry of the kind %s its fields, a kind the canon gives a design's log" % kind, False)
            continue
        got = p.run("--log-entry", design, kind, *fields)
        check("--log-entry appends a %s entry to a design %s naming an unfinished design, an entry of no work past its frame" % (kind, state),
              passes(got, "== log-entry", "- **Entry:** %s-" % kind) and "**Depends On Designs:** " + UNFINISHED in p.read(design), shown(got))
    p = a_workstack("blocked-complete")
    design = p.design(text=naming("complete", UNFINISHED))
    got = p.run("--log-entry", design, "plan-change")
    check("--log-entry holds nothing back from a complete design for the unfinished design it names", passes(got, "== log-entry", "- **Entry:** plan-change-"), shown(got))


@test("log", "a design-reassessment entry chosen at the step back holds its Cause, its Decision and its Diagnosis")
def _():
    for skill in SKILLS:
        p = Project("reassessed")
        design = p.design(skill=skill, log=DRAFTED)
        p.put(".ai/tmp/%s/%s/diagnosis/1.md" % (skill, NAME), a_diagnosis())
        for cause in ("a run of flaws", "a run of send-backs", "passes that did not converge", "the user's word")[:4 if skill == "design-specs" else 1]:
            p.design(skill=skill, log=DRAFTED)
            got = p.run("--log-entry", design, "design-reassessment", "Cause=step back: " + cause, "Decision=rescope",
                        "Diagnosis=.ai/tmp/%s/%s/diagnosis/1.md" % (skill, NAME), skill=skill)
            now = p.read(design)
            check("--log-entry of %s appends a design-reassessment entry whose Cause is the step back %s brought the design to, with what the user decided and its diagnosis" % (skill, cause),
                  passes(got, "== log-entry", "- **Entry:** design-reassessment-1") and "**Cause:** step back: %s \\\n    **Decision:** rescope \\\n    **Diagnosis:** " % cause in now
                  and "**Version:** 2.0.0" in now, shown(got))
        form = p.run("--check-design-form", design, skill=skill)
        check("and the design of %s it wrote holds its form" % skill, passes(form, "== check-design-form", "0 problems"), shown(form))


@test("log", "a design-reassessment entry is refused without its Cause, and with a Cause in neither form")
def _():
    p = Project("reassessed-refused")
    design = p.design(log=DRAFTED)
    p.put(".ai/tmp/design-specs/%s/diagnosis/1.md" % NAME, a_diagnosis())
    diagnosis = "Diagnosis=.ai/tmp/design-specs/%s/diagnosis/1.md" % NAME
    before = p.held()
    for label, args, said in (
            ("holding no Cause", ("Decision=rescope", diagnosis), "a design-reassessment entry holding no Cause: it states what caused the design reassessment"),
            ("holding no field at all", (), "a design-reassessment entry holding no Cause"),
            ("whose Cause is in neither form", ("Cause=the plan went stale", "Decision=rescope", diagnosis), "a design-reassessment entry's Cause is neither `changed foundation:`"),
            ("whose Cause is a step back naming nothing that brings a design to one", ("Cause=step back: a hunch", "Decision=rescope", diagnosis), "a design-reassessment entry's Cause is neither `changed foundation:`"),
            ("whose Cause is a step back and which holds no Decision", ("Cause=step back: the user's word", diagnosis), ["a design-reassessment entry", "Decision"]),
            ("whose Cause is a step back and which holds no Diagnosis", ("Cause=step back: the user's word", "Decision=rescope"), ["a design-reassessment entry", "Diagnosis"]),
            ("whose Cause is a step back and which holds neither", ("Cause=step back: the user's word",), ["a design-reassessment entry", "Decision", "Diagnosis"]),
            ("whose Decision is no design reassessment the user chooses", ("Cause=step back: the user's word", "Decision=carry on", diagnosis), "a design-reassessment entry's Decision is not one of rescope, split, a different approach: carry on"),
            ("whose Cause is a changed foundation, holding a Decision and a Diagnosis", ("Cause=changed foundation: quay-rebuilt finished", "Decision=rescope", diagnosis), "which --free-design alone appends")):
        got = p.run("--log-entry", design, "design-reassessment", *args)
        check("--log-entry refuses a design-reassessment entry %s, and writes nothing" % label, reports(got, "== log-entry, not logged", said) and p.held() == before, shown(got))


@test("log", "check-design-form reads each design-reassessment entry by its Cause")
def _():
    p = Project("reassessed-form")
    step_back = {"Cause": "step back: a run of flaws", "Decision": "split", "Diagnosis": "`.ai/tmp/design-specs/%s/diagnosis/1.md`" % NAME}
    foundation = {"Cause": "changed foundation: quay-rebuilt finished; pier-closed gone"}
    old = {"Decision": "rescope", "Diagnosis": "`.ai/tmp/design-specs/%s/diagnosis/1.md`" % NAME}
    for label, fields in (("chosen at the step back, holding its Decision and its Diagnosis", step_back), ("made for a changed foundation, holding neither", foundation),
                          ("appended before the entry held a Cause, read as one chosen at the step back", old)):
        got = p.run("--check-design-form", p.design(log=DRAFTED + (("design-reassessment", fields), ("goals-agreed", {}))))
        check("--check-design-form passes a log holding a design-reassessment entry " + label, passes(got, "== check-design-form", "0 problems"), shown(got))
    for label, fields, said in (
            ("made for a changed foundation and holding a Decision", dict(foundation, Decision="rescope"), ["log entry design-reassessment-1: a design-reassessment entry", "Decision"]),
            ("chosen at the step back and holding no Diagnosis", {"Cause": "step back: a run of flaws", "Decision": "split"}, ["log entry design-reassessment-1: a design-reassessment entry", "Diagnosis"]),
            ("whose Cause is in neither form", dict(step_back, Cause="it seemed time"), "log entry design-reassessment-1: a design-reassessment entry's Cause is neither `changed foundation:`")):
        got = p.run("--check-design-form", p.design(log=DRAFTED + (("design-reassessment", fields),)))
        check("--check-design-form reports a log holding a design-reassessment entry " + label, reports(got, "== check-design-form", said), shown(got))
    got = p.run("--check-design-form", p.design(log=DRAFTED + (("reassessment", {"Decision": "rescope", "Running Work": "none"}), ("goals-agreed", {}),
                                                         ("entered", {"Reason": "sent back for a dependency"}))))
    check("--check-design-form reads an old log's reassessment entry, and an entered entry holding a value of the earlier rules, as they were written, and reports neither",
          passes(got, "== check-design-form", "0 problems"), shown(got))


@test("log", "a diagnosis is held to its form as its entry is appended")
def _():
    path = ".ai/tmp/design-specs/%s/diagnosis/1.md" % NAME
    args = ("design-reassessment", "Cause=step back: a run of flaws", "Decision=a different approach", "Diagnosis=" + path)
    whole = a_diagnosis()
    for label, text, said in (
            ("that does not stand in the design's folder", None, "the design-reassessment entry's Diagnosis names no diagnosis standing in the design's folder"),
            ("holding no Scope", whole.split("## Scope")[0], "the diagnosis"),
            ("whose Scope holds no Answer", whole.split("**Answer:**")[0].rstrip(" \\\n") + "\n", "its Scope holds Question, not its Question and its Answer"),
            ("naming an entry other than the one naming it", swap(whole, "design-reassessment-1", "design-reassessment-4"), "its Design Reassessment is design-reassessment-4, not design-reassessment-1, the entry naming it"),
            ("whose Flaw names a Root Cause it does not hold", swap(whole, "**Root Cause:** one-season-assumed\n\n## Root", "**Root Cause:** another-cause\n\n## Root"), "names the Root Cause another-cause, which the diagnosis does not hold"),
            ("whose Flaw says neither that it still applies nor that it does not", swap(whole, "**Still Applies:** yes", "**Still Applies:** perhaps"), "Still Applies is neither yes nor no: perhaps"),
            ("whose Flaw no longer applies and says not why", swap(whole, "**Still Applies:** yes", "**Still Applies:** no"), "no longer applies, and holds no Why Not"),
            ("whose Root Cause holds no Account", swap(whole, " \\\n    **Account:** The rebuilt goals name each season.", ""), "Root Cause one-season-assumed holds no Account")):
        p = Project("diagnosis")
        design = p.design(log=DRAFTED)
        if text is not None:
            p.put(path, text)
        before = p.held()
        got = p.run("--log-entry", design, *args)
        check("--log-entry refuses the design-reassessment entry of a diagnosis " + label,
              reports(got, "== log-entry, not logged", [said, "[Name: diagnosis-whole-and-in-form]"]) and p.held() == before, shown(got))
    p = Project("diagnosis-second")
    design = p.design(log=DRAFTED)
    p.put(".ai/tmp/design-specs/%s/diagnosis/2.md" % NAME, whole)
    got = p.run("--log-entry", design, *args[:3], "Diagnosis=.ai/tmp/design-specs/%s/diagnosis/2.md" % NAME)
    check("--log-entry refuses a diagnosis numbered other than its count among the diagnoses the design's entries name",
          reports(got, "== log-entry, not logged", "not .ai/tmp/design-specs/%s/diagnosis/1.md, diagnosis 1 of the diagnoses" % NAME), shown(got))
    p = Project("diagnosis-after-a-freeing")
    design = p.design(log=DRAFTED + (("design-reassessment", {"Cause": "changed foundation: quay-rebuilt finished"}), ("goals-agreed", {}), ("plan-change", {})))
    p.put(path, swap(whole, "design-reassessment-1", "design-reassessment-2"))
    got = p.run("--log-entry", design, *args)
    check("--log-entry numbers a diagnosis among the diagnoses, so the first diagnosis of a design freed once before is diagnosis 1 of entry design-reassessment-2",
          passes(got, "== log-entry", "- **Entry:** design-reassessment-2") and "**Version:** 3.0.0" in p.read(design), shown(got))


@test("log", "a diagnosis leaving out a finding of its flaw set is refused")
def _():
    p = Project("diagnosis-flaws")
    design = p.design(log=DRAFTED)
    taken_up(p, "adversarial-review", a_report("review"))
    got = p.run("--log-entry", design, "adversarial-review", *ROUND_FIELDS)
    path = ".ai/tmp/design-specs/%s/diagnosis/1.md" % NAME
    args = ("design-reassessment", "Cause=step back: a run of flaws", "Decision=rescope", "Diagnosis=" + path)
    p.put(path, swap(a_diagnosis(), "reviewer-1-last-crossing-in-winter", "reviewer-1-another-finding"))
    refused = p.run("--log-entry", design, *args)
    check("--log-entry refuses a diagnosis leaving out a finding a Settlement of the design's checks kept as a flaw",
          got[0] == 0 and reports(refused, "== log-entry, not logged", "it leaves out adversarial-review/1.md [Finding: reviewer-1-last-crossing-in-winter], a finding of its flaw set"), shown(got) + shown(refused))
    p.put(path, a_diagnosis())
    got = p.run("--log-entry", design, *args)
    check("--log-entry appends the entry of a diagnosis holding a Flaw for each finding of its flaw set", passes(got, "== log-entry", "- **Entry:** design-reassessment-1"), shown(got))


# ---------------------------------------------------------------- a design shown, and a design of the earlier rules

PROBLEM_WORDS, STEP_WORDS = "names the ferry without saying when it runs", "The section names the ferry and gives no time."
OLD_FIELD = "**Depends On:** "
RELIANCE = "\n**Reliances:**\n  - **Design:** %s \\\n    **Version:** 1.0.0 \\\n    **Relies On:** The quay stands where the ferry leaves.\n\nThe sweep read the guide whole."


def with_old_field(text, named):
    """-> a design's text holding the old Depends On field, naming a design, in place of its Depends On Designs."""
    return swap(text, "**Depends On Designs:** none", OLD_FIELD + named)


def with_reliance(text, named):
    """-> a design's text whose Scope holds a Reliance on a design, as the earlier rules had one written."""
    return swap(text, "\nThe sweep read the guide whole.", RELIANCE % named)


@test("shown", "show-design shows the header and the goals of a design in a plans folder")
def _():
    for skill in SKILLS:
        p = a_workstack("shown")
        p.design("code-design", skill="implement-specs", log=DRAFTED)
        design = p.design(skill=skill, log=DRAFTED, depends=("" if skill == "design-specs" else "design-specs/") + UNFINISHED)
        before = p.held()
        for given in (design, NAME):
            got = p.run("--show-design", given, skill=skill)
            check("--show-design of %s shows the header and the goals of a design given by its %s, and nothing else of it" % (skill, "file" if given == design else "name"),
                  passes(got, "== show-design %s [in-progress]" % NAME, "0 problems")
                  and all(w in got[1] for w in ("Name: " + NAME, "Version: 1.0.1", "Status: in-progress", "Depends On Designs: ", "Validated: none",
                                                "Design Goals:\n  - Name: %s\n    Description: The guide says when the ferry runs." % GOAL))
                  and not any(w in got[1] for w in (PROBLEM_WORDS, STEP_WORDS, STEP, OUTCOME, "Entry:")) and p.held() == before, shown(got))
        other = "implement-specs/code-design" if skill == "design-specs" else "design-specs/" + UNFINISHED
        got = p.run("--show-design", other, skill=skill)
        check("--show-design of %s shows a design of the plans folder beside its own, by the name a Depends On Designs gives it" % skill,
              passes(got, "== show-design %s [in-progress]" % other, "0 problems") and "Name: " + other.split("/")[1] in got[1], shown(got))
    p = a_workstack("shown-unstated")
    got = p.run("--show-design", p.design(status="not-started"))
    check("--show-design shows the goals of a design that has stated none as the section holds them", passes(got, "== show-design %s [not-started]" % NAME, "Design Goals:\n  Not yet stated.\n0 problems"), shown(got))


@test("shown", "show-design shows a design in an older form as far as it reads, and names what is missing")
def _():
    p = a_workstack("shown-older")
    text = with_old_field(a_design(log=DRAFTED), UNFINISHED)
    text = swap(text, "**Kind:** documentation \\\n", "")
    text = part(text, "## Design Goals", "The guide is to say when the ferry runs.")
    design = p.design(text=text)
    before = p.held()
    got = p.run("--show-design", design)
    check("--show-design shows each field an older design holds, names each missing or not valid, and writes nothing",
          reports(got, "== show-design %s [in-progress]" % NAME, ["Name: " + NAME, "Depends On: " + UNFINISHED, "Design Goals:\n  The guide is to say when the ferry runs.",
                                                                 "Missing or not valid, so the design is old and suspect, and stays as it is until its own builder takes it up:",
                                                                 "its header", "Kind is not ", "Design Goals has no Records field"])
          and PROBLEM_WORDS not in got[1] and p.held() == before, shown(got))
    got = p.run("--show-design", p.design("no-goals", text=part(a_design("no-goals", status="in-progress", log=DRAFTED), "## Design Goals", None)))
    check("--show-design names the goals' section where a design holds none", reports(got, "== show-design no-goals", "it holds no Design Goals section"), shown(got))


@test("shown", "show-design shows nothing of a design outside the plans folders")
def _():
    p = a_workstack("shown-outside")
    before = p.held()
    for given, label in ((".ai/plans/design-specs/archive/%s.md" % ABSENT, "by its file in an archive"), (ABSENT, "by its name, standing in an archive alone"),
                         (p.design(folder="elsewhere", log=DRAFTED), "by its file outside every plans folder"), ("no-such-design", "by a name no design takes")):
        got = p.run("--show-design", given)
        check("--show-design shows nothing of a design given %s, and says it stands in no plans folder" % label,
              reports(got, "== show-design", "no design of that name stands in a plans folder, so nothing of it is shown")
              and "Name:" not in got[1] and "Design Goals" not in got[1], shown(got))
    check("and writes nothing", {k: v for k, v in p.held().items()} == before)


@test("earlier", "the old Depends On field is reported, and read by nothing")
def _():
    for skill in SKILLS:
        p = a_workstack("old-field")
        named = UNFINISHED if skill == "design-specs" else "design-specs/" + UNFINISHED
        design = p.design(skill=skill, text=with_old_field(a_design(skill=skill, log=DRAFTED), named))
        got = p.run("--check-design-form", design, skill=skill)
        check("--check-design-form of %s reports a design holding the old Depends On field, naming the field" % skill,
              reports(got, "== check-design-form " + NAME, "its header gives Depends On, a field its form does not take; leaves out Depends On Designs, a field its form requires"), shown(got))
        own = NAME if skill == "design-specs" else NAME
        got = p.run("--check-workstack", skill=skill)
        check("--check-workstack of %s reports it, naming the field" % skill,
              reports(got, "== check-workstack", "its header gives Depends On, a field its form does not take\n"), shown(got))
        got = p.run("--show-workstack", skill=skill)
        line = next((l for l in got[1].split("\n") if l.strip().startswith(own + " [")), "")
        check("--show-workstack of %s reads the old field as no name: the design is blocked by nothing" % skill, got[0] == 0 and line.strip() == own + " [in-progress]", line + shown(got))
        got = p.run("--check-design-names", design, skill=skill)
        check("--check-design-names of %s reads the old field as no name" % skill, passes(got, "== check-design-names", "0 problems") and "blocked by" not in got[1], shown(got))
        got = p.run("--free-design", p.design("old-finished", skill=skill, text=with_old_field(a_design("old-finished", skill=skill, log=DRAFTED), ("" if skill == "design-specs" else "design-specs/") + COMPLETE)), skill=skill)
        check("--free-design of %s reads the old field as no name, and writes nothing" % skill, passes(got, "== free-design old-finished", "names no finished or gone design, so nothing is written")
              and OLD_FIELD in p.read(".ai/plans/%s/old-finished.md" % skill), shown(got))
        got = p.run("--log-entry", design, "plan-change", skill=skill)
        check("--log-entry of %s reads the old field as no name: an entry of work past the frame is appended" % skill, passes(got, "== log-entry", "- **Entry:** plan-change-2"), shown(got))


@test("earlier", "a design holding a Reliance is reported by the check of its form")
def _():
    p = a_workstack("reliance")
    got = p.run("--check-design-form", p.design(text=with_reliance(a_design(log=DRAFTED, depends=UNFINISHED), UNFINISHED)))
    check("--check-design-form reports a design holding a Reliance on a design its Depends On Designs names",
          reports(got, "== check-design-form", "its Scope holds a Reliances field, which its form does not take: a design names the designs it depends on in its Depends On Designs alone")
          and "which its Depends On Designs does not" not in got[1], shown(got))
    got = p.run("--check-design-form", p.design(text=with_reliance(a_design(log=DRAFTED, depends=UNFINISHED), COMPLETE)))
    check("--check-design-form reports a design holding a Reliance on a design its Depends On Designs does not name, naming that design",
          reports(got, "== check-design-form", "its Scope holds a Reliances field, which its form does not take: a design names the designs it depends on in its Depends On Designs alone; "
                  "its Reliances name %s, which its Depends On Designs does not" % COMPLETE), shown(got))
    got = p.run("--check-design-names", p.design(text=with_reliance(a_design(log=DRAFTED), COMPLETE)))
    check("and no action reads which designs a design depends on from a Reliance: --check-design-names reports nothing of it", passes(got, "== check-design-names", "0 problems"), shown(got))
    got = p.run("--show-workstack")
    check("nor does --show-workstack", "waiting to be freed" not in got[1] and "  %s [in-progress]" % NAME in got[1], shown(got))


@test("earlier", "a design holding a Reliance on a finished design, brought to the form, is freed and reassessed")
def _():
    for named in (COMPLETE, ABSENT, UNFINISHED):
        p = a_workstack("reliance-brought")
        design = p.design(text=with_reliance(a_design(log=DRAFTED), named))
        check("until its builder brings it to the form, the check of its form reports it", reports(p.run("--check-design-form", design), "== check-design-form", "its Reliances name " + named))
        # the builder next working it brings it to the form: the Reliance's design a name in its Depends On Designs
        p.design(text=a_design(log=DRAFTED, depends=named))
        form = p.run("--check-design-form", design)
        names = p.run("--check-design-names", design)
        if named == UNFINISHED:
            got = p.run("--log-entry", design, "plan-change")
            check("brought to the form, a design that relied on an unfinished design holds its form and waits: an entry of work past its frame is refused",
                  passes(form, "== check-design-form", "0 problems") and passes(names, "== check-design-names", "blocked by " + named)
                  and reports(got, "== log-entry, not logged", "plan-change " + BLOCKED % named), shown(got))
        else:
            got = p.run("--free-design", design)
            check("brought to the form, a design that relied on a design %s is reported by the check of its names, and freed, stands reassessed" % READ_AS[named],
                  passes(form, "== check-design-form", "0 problems") and reports(names, "== check-design-names", "names %s, %s" % (named, READ_AS[named]))
                  and passes(got, "== free-design", "reassessed, its goals to agree again") and "**Version:** 2.0.0" in p.read(design), shown(got))


@test("earlier", "a design approved or applying while it names an unfinished design is reported until it is moved back")
def _():
    for state in ("approved", "applying"):
        p = a_workstack("earlier-approved")
        design = p.design(text=naming(state, UNFINISHED))
        got = p.run("--check-workstack")
        check("--check-workstack reports a design %s under the earlier rules while it names an unfinished design" % state,
              reports(got, "== check-workstack", "%s, but its Depends On Designs names %s, unfinished" % (state, UNFINISHED)), shown(got))
        shown_ = p.run("--show-workstack")
        check("and --show-workstack lists it to move back", "\n  move back: %s [%s, blocked by %s" % (NAME, state, UNFINISHED) in shown_[1], shown(shown_))
        # its builder next working it moves it back: its Status in-progress, and the entry of that move
        p.put(design, swap(p.read(design), "**Status:** " + state, "**Status:** in-progress"))
        moved = p.run("--log-entry", design, "entered", "Reason=" + ("a dependency named" if state == "approved" else "sent back for a dependency"))
        got = p.run("--check-workstack")
        refused = p.run("--log-entry", design, "plan-approval", "Approval=approved")
        check("moved back from %s, it is reported no longer, and waits: an entry of work past its frame is refused" % state,
              passes(moved, "== log-entry", "- **Entry:** entered-2") and passes(got, "== check-workstack", "0 problems")
              and reports(refused, "== log-entry, not logged", "plan-approval " + BLOCKED % UNFINISHED), shown(moved) + shown(got) + shown(refused))


@test("earlier", "a design drafted or reviewed while it named an unfinished design is reported by no check")
def _():
    p = a_workstack("earlier-drafted")
    log = DRAFTED + (("adversarial-review", {"Design Version": "1.0.1"}), ("plan-change", {}))
    design = p.design(log=log, depends=UNFINISHED)
    for flag, args, heading in (("--check-design-form", (design,), "== check-design-form"), ("--check-workstack", (), "== check-workstack"), ("--check-design-names", (design,), "== check-design-names")):
        got = p.run(flag, *args)
        check("%s reports nothing of a design whose steps were drafted and reviewed while it named an unfinished design" % flag, passes(got, heading, "0 problems"), shown(got))
    got = p.run("--log-entry", design, "another-round")
    check("and its work goes no further: an entry of that work is refused", reports(got, "== log-entry, not logged", "another-round " + BLOCKED % UNFINISHED), shown(got))


@test("earlier", "an old log's entry for a dependency is read as written, and appended by nothing")
def _():
    p = a_workstack("earlier-log")
    design = p.design(log=APPROVED + (("entered", {"Reason": "sent back to reassess"}), ("entered", {"Reason": "a dependency finished"})), status="in-progress")
    got = p.run("--check-design-form", design)
    check("--check-design-form reports nothing of a log holding an entered entry whose Reason the earlier rules gave", passes(got, "== check-design-form", "0 problems"), shown(got))
    before = p.read(design)
    for reason in ("sent back to reassess", "a dependency finished", "a dependency moved back"):
        got = p.run("--log-entry", design, "entered", "Reason=" + reason)
        check("--log-entry appends no entered entry whose Reason is `%s`, a value the entry reason no longer takes" % reason,
              reports(got, "== log-entry, not logged", "an entered entry's Reason is not one of") and p.read(design) == before, shown(got))


# ---------------------------------------------------------------- a check's report

REVIEW, JUDGMENT = "adversarial-review", "handed-off-judgment"
FINDING, CAUSE = "reviewer-1-last-crossing-in-winter", "times-by-season"
FERRY = "`docs/guide.md § The Ferry`"
RULE = "[Name: %s]"


def a_round(name="round", cold=None, own=None, log=DRAFTED, skill="design-specs", n=1, settle=True):
    """-> (a project, its design, the path of an adversarial review's report taken up and settled): the base review's
    report, its cold agent's parts changed by cold before the take-up and the builder's by own after it."""
    p = Project(name)
    design = p.design(skill=skill, log=log)
    text = a_report("review", skill=skill, entry="%s-%d" % (REVIEW, n))
    text = (cold or (lambda t: t))(cold_part(text)) + "\n" + (own or (lambda t: t))(builder_part(text))
    return p, design, taken_up(p, REVIEW, text, n=n, skill=skill, settle=settle)


def settled_reports(label, own, said, record=None, cold=None):
    """One reporting test of a check of the builder's parts: the settled report is reported by --check-settled-report,
    and its entry refused by --log-entry, each by the message of the check driven. record names the Script Check
    record the check carries out, which the script prints only for the checks it names by their record."""
    p, design, path = a_round("settled", cold=cold, own=own)
    before = p.read(design)
    got = p.run("--check-settled-report", path)
    check("--check-settled-report reports " + label, reports(got, "== check-settled-report " + path, [said] if isinstance(said, str) else said), shown(got))
    got = p.run("--log-entry", design, REVIEW, *ROUND_FIELDS)
    check("--log-entry refuses the entry of " + label, reports(got, "== log-entry, not logged", [said] if isinstance(said, str) else said) and p.read(design) == before, shown(got))


@test("reports", "check-handed-back passes a report its cold agent wrote in its form")
def _():
    for skill in SKILLS:
        p = Project("handed-back")
        p.design(skill=skill, log=DRAFTED)
        for kind, which in ((REVIEW, "review"), (JUDGMENT, "research")):
            path = p.put(report_at(kind, 1, skill=skill), cold_part(a_report(which, skill=skill)))
            before = p.held(".ai")
            got = p.run("--check-handed-back", path, skill=skill)
            check("--check-handed-back of %s passes the cold agent's part of %s report, and writes nothing" % (skill, "a review's" if kind == REVIEW else "a research"),
                  passes(got, "== check-handed-back " + path, "0 problems") and p.held(".ai") == before, shown(got))


@test("reports", "check-handed-back reports a cold agent's part out of its form")
def _():
    whole = cold_part(a_report("review"))
    for label, text, said, rule in (
            ("whose title names another entry", swap(whole, "**Entry:** adversarial-review-1", "**Entry:** adversarial-review-7"), "its title's Entry is adversarial-review-7, not adversarial-review-1", None),
            ("whose title names another design", swap(whole, "**Design:** " + NAME, "**Design:** another-design"), "its title's Design is another-design, not " + NAME, None),
            ("holding no Reading", whole.split("## Reading")[0] + "## Findings" + whole.split("## Findings")[1], "it holds no Reading part, which its form requires of it", None),
            ("whose parts stand out of their order", whole.split("## Findings")[0] + "## Searches" + whole.split("## Searches")[1].rstrip("\n") + "\n\n## Findings" + whole.split("## Findings")[1].split("## Searches")[0], "the report", None),
            ("holding a part the form does not give", whole + "\n## Afterthoughts\n\nNone.\n", "a part the form does not give: Afterthoughts", None),
            ("whose marked Finding holds no Decision", swap(whole, "    **Decision:** the times the section gives \\\n", ""), "Finding %s holds no Decision, which its form requires where its Verdict is a mark" % FINDING, None),
            ("whose Finding holds a Verdict out of its values", swap(whole, "**Verdict:** implementation flaw", "**Verdict:** a worry"), "a worry", None),
            ("holding a part the builder writes", whole + "\n" + builder_part(a_report("review")), "a part its cold agent does not write, the builder's or the design script's: Settlement", RULE % "cold-parts-kept"),
            ("whose Finding names a goal the design does not hold", swap(whole, "    **Affected Goals:**\n      - " + GOAL, "    **Affected Goals:**\n      - guide-says-what-the-ferry-costs"),
             "Finding %s's Affected Goals names guide-says-what-the-ferry-costs, which the design %s does not hold" % (FINDING, NAME), "§ A Check's Report § Finding"),
            ("whose marked Finding names no part of the design and cites no rule", swap(whole, "    **Affected Goals:**\n      - " + GOAL + "\n\n", ""),
             "Finding %s, marked a implementation flaw, names no goal, Frame Outcome or step Objective it bears on and cites no rule it breaks" % FINDING, "§ A Check's Report § Finding"),
            ("whose Reads hold what is no citation of a place", swap(whole, "      - `docs/guide.md`\n", "      - the guide\n"), "Collecting Reads holds an item that is no citation of a place with its path: the guide", None),
            ("whose Finding lands on a change not cited with its report", swap(whole, "        **Delivers:** An Objective giving the first and the last crossing of each season.\n",
                                                                           "        **Delivers:** An Objective giving the first and the last crossing of each season.\n\n    **Lands On:** times-by-season\n"),
             "Finding %s lands on an earlier change not cited with its report: times-by-season" % FINDING, None),
            ("citing a record of a report no entry names", swap(whole, "The section names one quay and no season.", "The section names one quay and no season, as `.ai/tmp/design-specs/%s/reports/adversarial-review/9.md § Findings [Finding: reviewer-1-another]` found." % NAME),
             "in a report no entry of the design's current major version names", None),
            ("whose reviewer's Search by meaning holds more Places than its Ranking Part spans", swap(whole, "**Ranking Part:** 1 to 20", "**Ranking Part:** none"),
             "Search reviewer-1-winter-hours's Ranking Part is none, and its Places hold 1", None),
            ("whose Search holds a Snapshot that is no snapshot code", swap(whole, "**Snapshot:** 0123456789abcdef", "**Snapshot:** yesterday"), "Search reviewer-1-winter-hours's Snapshot is yesterday, not a snapshot code", None)):
        p = Project("handed-back-reports")
        p.design(log=DRAFTED)
        path = p.put(report_at(REVIEW), text)
        got = p.run("--check-handed-back", path)
        check("--check-handed-back reports a review's report " + label, reports(got, "== check-handed-back " + path, said) and (rule is None or rule in got[1]), shown(got))
        before = p.read(path)
        got = p.run("--take-up-report", path)
        check("--take-up-report does not take up a review's report %s, and writes nothing" % label,
              reports(got, "== take-up-report, not taken up " + path, said) and p.read(path) == before, shown(got))
    p = Project("handed-back-usage")
    for flag in ("--check-handed-back", "--take-up-report"):
        got = p.run(flag, p.put(report_at("self-review"), a_report("self-review")))
        check("%s takes a review's or a handed-off judgment's report alone, exit 2" % flag, got[0] == 2 and "takes a review's or a handed-off judgment's report at its path" in got[1], shown(got))


@test("reports", "a report laid out other than its form's layout is reported")
def _():
    whole = cold_part(a_report("review"))
    p = Project("laid-out")
    p.design(log=DRAFTED)
    for label, text in (("a field's line ending with no backslash before the field after it", swap(whole, "**Verdict:** implementation flaw \\\n", "**Verdict:** implementation flaw\n")),
                        ("no blank line after a list a field holds", swap(whole, "      - " + GOAL + "\n\n    **Description:**", "      - " + GOAL + "\n    **Description:**"))):
        path = p.put(report_at(REVIEW), text)
        got = p.run("--check-handed-back", path)
        check("--check-handed-back reports a report holding " + label, reports(got, "== check-handed-back", "specs/methodology/modeling-constructs.md § Fields\n") or
              reports(got, "== check-handed-back", "specs/methodology/spec-style/markdown.md § Blank Lines\n"), shown(got))


@test("reports", "take-up-report writes a fingerprint of each part the cold agent wrote")
def _():
    for skill in SKILLS:
        p = Project("taken-up")
        p.design(skill=skill, log=DRAFTED)
        for kind, which, parts in ((REVIEW, "review", ("Title", "Reading", "Findings", "Searches")), (JUDGMENT, "research", ("Title", "Reading", "Searches", "Read Assessments"))):
            cold = cold_part(a_report(which, skill=skill))
            path = p.put(report_at(kind, skill=skill), cold)
            got = p.run("--take-up-report", path, skill=skill)
            now = p.read(path)
            marks = re.findall(r"^- ([A-Za-z -]+): [0-9a-f]{64}(, \d+ lines)?$", now.split("## Hand-back")[-1], re.M)
            check("--take-up-report of %s takes up %s report: it leaves each part the cold agent wrote as it was and writes a fingerprint of each" % (skill, "a review's" if kind == REVIEW else "a research"),
                  passes(got, "== take-up-report " + path, "0 problems") and now.startswith(cold.rstrip("\n") + "\n\n## Hand-back\n\n") and tuple(m[0] for m in marks) == parts
                  and [bool(m[1]) for m in marks] == [kind == REVIEW and m[0] == "Searches" for m in marks], shown(got) + now[-600:])


@test("reports", "check-settled-report passes a round settled in its form, and its entry takes its counts from the report")
def _():
    for skill in SKILLS:
        p, design, path = a_round("settled-passes", skill=skill)
        before = p.held(".ai")
        got = p.run("--check-settled-report", path, skill=skill)
        check("--check-settled-report of %s passes a taken-up review's report settled with a Cause, and writes nothing" % skill,
              passes(got, "== check-settled-report " + path, "0 problems") and p.held(".ai") == before, shown(got))
        got = p.run("--log-entry", design, REVIEW, *ROUND_FIELDS, skill=skill)
        check("--log-entry of %s appends the round's entry, its counts taken from its report and its version the one the report read" % skill,
              passes(got, "== log-entry", "- **Entry:** adversarial-review-1")
              and "**Design Version:** 1.0.1 \\\n    **Model:** a model \\\n    **Effort:** medium \\\n    **Design Flaws:** 0 \\\n    **Implementation Flaws:** 1 \\\n    **Nits:** 0 \\\n    **Dropped:** 0 \\\n    **Led To:** validating" in got[1], shown(got))
        again = p.run("--check-settled-report", path, skill=skill)
        form = p.run("--check-design-form", design, skill=skill)
        check("and the report read again once its entry stands, and the design, hold their forms", passes(again, "== check-settled-report", "0 problems") and passes(form, "== check-design-form", "0 problems"), shown(again) + shown(form))


@test("reports", "a count given a check's entry is refused")
def _():
    p, design, path = a_round("counts")
    before = p.read(design)
    got = p.run("--log-entry", design, REVIEW, *ROUND_FIELDS, "Nits=3")
    check("--log-entry refuses a count the builder gives, which is taken from the report alone",
          reports(got, "== log-entry, not logged", "a count given, which is taken from the check's report alone: Nits") and p.read(design) == before, shown(got))
    drop = lambda t: swap(swap(swap(t, "**Verdict:** implementation flaw", "**Verdict:** dropped"), "    **Fix Authority:** the builder's \\\n", ""), "    **Cause:** times-by-season \\\n", "    **Departure Reason:** The ferry keeps one set of hours. \\\n")
    p, design, path = a_round("counts-dropped", own=lambda t: drop("## Settlement" + t.split("## Settlement")[1]))
    got = p.run("--log-entry", design, REVIEW, *ROUND_FIELDS)
    check("--log-entry counts a finding by the last word of the Settlement settling it: one its reviewer marked a flaw and the builder dropped is counted dropped",
          passes(got, "== log-entry", "**Implementation Flaws:** 0 \\\n    **Nits:** 0 \\\n    **Dropped:** 1"), shown(got))


@test("reports", "a part its cold agent wrote is held to its fingerprint")
def _():
    p, design, path = a_round("cold-kept")
    p.put(path, swap(p.read(path), "A visitor in winter plans a crossing the ferry does not make.", "A visitor in winter is left on the quay."))
    got = p.run("--check-settled-report", path)
    now = p.read(path)
    check("--check-settled-report reports a part changed since the take-up, and the report goes back to its cold agent cleared of the builder's parts",
          reports(got, "== check-settled-report", ["the Findings part no longer holds what its cold agent handed back", RULE % "cold-parts-kept", "goes back to its cold agent"])
          and not any(h in now for h in BUILDER_PARTS) and "A visitor in winter is left on the quay." in now, shown(got) + now[-300:])
    p, design, path = a_round("cold-removed")
    text = p.read(path)
    p.put(path, text.split("## Searches")[0] + "## Hand-back" + text.split("## Hand-back")[1])
    got = p.run("--log-entry", design, REVIEW, *ROUND_FIELDS)
    check("--log-entry refuses the entry of a report whose cold agent's part was removed since the take-up",
          reports(got, "== log-entry, not logged", "the Searches part its cold agent handed back is removed"), shown(got))
    p = Project("cold-not-taken-up")
    design = p.design(log=DRAFTED)
    path = p.put(report_at(REVIEW), a_report("review"))
    got = p.run("--log-entry", design, REVIEW, *ROUND_FIELDS)
    check("--log-entry refuses the entry of a cold agent's report the builder settled without taking it up",
          reports(got, "== log-entry, not logged", ["it holds no Hand-back part: a report a cold agent wrote is taken up by --take-up-report", RULE % "cold-parts-kept"]), shown(got))


@test("reports", "a finding is settled once")
def _():
    twice = lambda t: t.rstrip("\n") + "\n\n  - **Settlement:** times-by-season-again \\" + t.split("- **Settlement:** times-by-season-kept \\")[1]
    settled_reports("a round whose Finding two Settlements settle", twice, "Finding %s is settled by 2 Settlements, not exactly one" % FINDING, RULE % "findings-settled-once")
    none = lambda t: swap(t, "    **Settled Findings:**\n      - " + FINDING, "    **Settled Findings:**\n      - reviewer-1-another-finding")
    settled_reports("a round whose Finding no Settlement settles", none, ["Finding %s is settled by 0 Settlements, not exactly one" % FINDING,
                                                                       "Settlement times-by-season-kept settles reviewer-1-another-finding, which no Finding of the report is"], RULE % "report-keys-name-records")


@test("reports", "a key a report cites names a record")
def _():
    settled_reports("a round whose Settlement names a Cause the report does not hold", lambda t: swap(t, "    **Cause:** times-by-season \\", "    **Cause:** times-by-tide \\"),
                    "Settlement times-by-season-kept names a Cause the report does not hold: times-by-tide", RULE % "report-keys-name-records")
    settled_reports("a round whose Settlement is carried by a step the design does not hold", lambda t: swap(t, "    **Cause:** times-by-season \\", "    **Cause:** times-by-season \\\n    **Carried By:** no-such-step \\"),
                    "Settlement times-by-season-kept is carried by a step the design does not hold: no-such-step", None)


@test("reports", "a settlement is justified by what requires it")
def _():
    settled_reports("a round whose Settlement names a goal the design does not hold as justifying it", lambda t: swap(t, "    **Justifying Goals:**\n      - " + GOAL, "    **Justifying Goals:**\n      - guide-says-what-the-ferry-costs"),
                    "Settlement times-by-season-kept's Justifying Goals name guide-says-what-the-ferry-costs, which is no design goal's Name", RULE % "settlements-justified")
    settled_reports("a round whose Settlement holds Justifying Goals where the rules require it", lambda t: swap(t, "**Required By:** the goals", "**Required By:** the rules"),
                    ["Settlement times-by-season-kept holds a Justifying Goals, which its form gives it only where its Required By names the goals",
                     "Settlement times-by-season-kept holds no Justifying Rules, which its form requires where its Required By names the rules"], RULE % "settlements-justified")
    settled_reports("a round whose Settlement gives the user's authority and holds no decision of the user's", lambda t: swap(t, "**Fix Authority:** the builder's", "**Fix Authority:** the user's"),
                    "Settlement times-by-season-kept holds no User Decision, which its form requires where its Fix Authority is the user's", RULE % "settlements-justified")
    flaw = lambda t: swap(t, "**Verdict:** implementation flaw", "**Verdict:** design flaw")
    settled_reports("a round whose Settlement keeps a design flaw on the builder's own authority", flaw,
                    "Settlement times-by-season-kept holds Fix Authority the builder's, where Whose Fix It Is gives the user the call: its Verdict is design flaw", RULE % "settlements-justified")


@test("reports", "an order follows its lineage")
def _():
    settled_reports("a round whose Settlement states an order deeper than its lineage gives", lambda t: swap(t, "    **Order:** primary \\\n    **Fix", "    **Order:** secondary \\\n    **Fix"),
                    "Settlement times-by-season-kept states Order secondary, where its lineage gives primary: it lands on no earlier change", RULE % "orders-follow-their-lineage")
    settled_reports("a round whose Changed Place states an order other than its lineage gives", lambda t: swap(t, "            **Order:** primary \\", "            **Order:** tertiary \\"),
                    "states Order tertiary, where its lineage gives primary: it names the findings whose fix it is", RULE % "orders-follow-their-lineage")


@test("reports", "a departure from a finding's writer is reasoned")
def _():
    settled_reports("a round whose Settlement departs from its Finding's Verdict and gives no reason", lambda t: swap(t, "    **Verdict:** implementation flaw \\\n    **Required", "    **Verdict:** nit \\\n    **Required"),
                    "Settlement times-by-season-kept departs from Finding %s in Verdict and holds no Departure Reason" % FINDING, RULE % "departures-reasoned")


@test("reports", "a round's settling reads cover its evidence")
def _():
    settled_reports("a round whose Settling Reads leave out a place its marked Finding's Evidence names", lambda t: swap(t, "**Settling Reads:**\n  - " + FERRY, "**Settling Reads:**\n  - `docs/guide.md § The Lighthouse`"),
                    "its Settling Reads leave out %s, a place the Evidence of a marked Finding names" % FERRY, RULE % "settling-reads-cover-the-evidence")


@test("reports", "a round settled out of its form is reported")
def _():
    settled_reports("a round holding a marked Finding and no Causes", lambda t: "## Settlement" + swap(t.split("## Settlement")[1], "    **Cause:** times-by-season \\\n", ""),
                    "it holds no Causes part, which its form requires of it", None)
    settled_reports("a round whose Settlement states no Ending", lambda t: swap(t, "**Ending:** its own settling \\\n", ""),
                    "its Settlement holds no Ending, which its form requires where the report owes the statement of how its check ended", None)
    settled_reports("a round whose Cause settling a flaw holds no Misses", lambda t: t.split("    **Misses:**")[0] + "    **Proposed Change:**" + t.split("    **Proposed Change:**")[1],
                    "Cause times-by-season holds no Misses, which its form requires where it settles a design flaw or an implementation flaw", None)
    settled_reports("a round whose revision names no decision it rewrites", lambda t: swap(t, "        **Decision Rewritten:** The Objective gives the first and the last crossing of each season. \\\n", ""),
                    "Cause times-by-season's Proposed Change holds no Decision Rewritten, which its form requires where its Kind is revision", None)


@test("reports", "a tactical fix names a search giving every place")
def _():
    search = "\n\n  - **Search:** each-season-named \\\n    **For:** every place naming one season alone \\\n    **Goals:**\n      - %s\n\n    **Kind:** meaning \\\n" \
             "    **Query:** The ferry keeps one set of hours. \\\n    **Ranking Part:** 1 to 20 \\\n    **Snapshot:** 0123456789abcdef \\\n    **Places:**\n      - %s\n" % (GOAL, FERRY)
    p, design, path = a_round("tactical")
    text = p.read(path)
    text = swap(text, "\n\n## Hand-back", search + "\n## Hand-back")
    text = swap(text, "      - **Kind:** revision \\\n        **Decision Rewritten:** The Objective gives the first and the last crossing of each season. \\",
                "      - **Kind:** tactical fix \\\n        **Search:** each-season-named \\\n        **Reason:** The Objective's meaning stands, and only its wording names one season. \\")
    p.put(path, text)
    got = p.run("--check-settled-report", path)
    check("--check-settled-report reports a tactical fix naming a Search by meaning, which gives a part of a ranking",
          reports(got, "== check-settled-report", ["Cause times-by-season's tactical fix names Search each-season-named, a search by meaning, which gives a part of a ranking and never every place its defect stands in",
                                                  "Cause times-by-season's tactical fix leaves out %s, a place its Search found" % FERRY]), shown(got))
    p.put(path, swap(text, "        **Search:** each-season-named \\", "        **Search:** no-such-search \\"))
    got = p.run("--check-settled-report", path)
    check("--check-settled-report reports a tactical fix citing a Search the report does not hold",
          reports(got, "== check-settled-report", "Cause times-by-season's Proposed Change cites a Search the report does not hold: no-such-search"), shown(got))


@test("reports", "a round names the earlier reports of its phase, and a finding landing on an earlier change is one order deeper")
def _():
    first = ".ai/tmp/design-specs/%s/reports/adversarial-review/1.md" % NAME
    lands = "`%s § Causes [Cause: %s]`" % (first, CAUSE)

    def second(earlier=True, order="secondary"):
        p, design, path = a_round("second-round")
        logged = p.run("--log-entry", design, REVIEW, *ROUND_FIELDS)
        text = a_report("review", entry="adversarial-review-2").replace("reviewer-1", "reviewer-2").replace(CAUSE, "times-by-season-again")
        text = swap(text, "        **Delivers:** An Objective giving the first and the last crossing of each season.\n",
                    "        **Delivers:** An Objective giving the first and the last crossing of each season.\n\n    **Lands On:** %s\n" % lands)
        text = swap(text, "    **Cause:** times-by-season-again \\\n", "    **Cause:** times-by-season-again \\\n    **Lands On:** %s \\\n" % lands)
        text = swap(text, "    **Order:** primary \\\n    **Fix", "    **Order:** %s \\\n    **Fix" % order)
        if earlier:
            text = swap(text, "**Earlier Reports:**\n  - none\n\n**Settling", "**Earlier Reports:**\n  - `%s`\n\n**Settling" % first)
            text = swap(text, "    **Earlier Reports:**\n      - none", "    **Earlier Reports:**\n      - `%s`" % first)
        return p, design, taken_up(p, REVIEW, text, n=2), logged

    p, design, path, logged = second()
    got = p.run("--check-settled-report", path)
    check("--check-settled-report passes a second round naming the first round's report among its Earlier Reports, its finding landing on the first round's change settled as secondary",
          logged[0] == 0 and passes(got, "== check-settled-report " + path, "0 problems"), shown(logged) + shown(got))
    got = p.run("--log-entry", design, REVIEW, *ROUND_FIELDS)
    check("and --log-entry appends its entry", passes(got, "== log-entry", "- **Entry:** adversarial-review-2"), shown(got))
    p, design, path, _ = second(earlier=False)
    got = p.run("--check-settled-report", path)
    check("--check-settled-report reports a second round whose Earlier Reports leave out the first round's report",
          reports(got, "== check-settled-report", "its Earlier Reports leave out `%s`, a report of the phase's record" % first), shown(got))
    p, design, path, _ = second(order="primary")
    got = p.run("--check-settled-report", path)
    check("--check-settled-report reports a Settlement stating primary for a finding landing on an earlier round's change",
          reports(got, "== check-settled-report", "states Order primary, where its lineage gives secondary: it lands on %s, whose order is primary" % lands), shown(got))


# ---------------------------------------------------------------- research, and the log's gates on a check's entry

LIGHTHOUSE = "`docs/guide.md § The Lighthouse`"
STEER = "\n## Steering Decisions\n\n**Records:**\n  - **Name:** winter-hours-count \\\n    **Prompted By:** the first share's assessment \\\n    **Type:** directive \\\n" \
        "    **Steer:** \"Give the winter hours too.\" \\\n    **Decision:** The guide gives each season's hours. \\\n    **Changes:**\n      - none\n\n## Design Plan Steps"


@test("research", "each place a research report read lies in an area it assesses")
def _():
    whole = cold_part(a_report("research"))
    p = Project("reads-assessed")
    p.design(log=AGREED)
    path = p.put(report_at(JUDGMENT), swap(whole, "**Reads:**\n  - " + FERRY, "**Reads:**\n  - %s\n  - %s" % (FERRY, LIGHTHOUSE)))
    for flag, heading in (("--check-handed-back", "== check-handed-back"), ("--take-up-report", "== take-up-report, not taken up")):
        got = p.run(flag, path)
        check("%s reports a research report whose Reads hold a place lying within no Read Assessment's Area" % flag,
              reports(got, heading, "%s, a place its Reads hold, lies within no Read Assessment's Area" % LIGHTHOUSE), shown(got))
    path = p.put(report_at(JUDGMENT), swap(whole, "**Reads:**\n  - " + FERRY, "**Reads:**\n  - %s\n  - `.ai/plans/design-specs/%s.md`" % (FERRY, NAME)))
    got = p.run("--check-handed-back", path)
    check("--check-handed-back passes a research report each of whose Reads lies in an Area it assesses, the design document aside", passes(got, "== check-handed-back", "0 problems"), shown(got))
    path = p.put(report_at(JUDGMENT), swap(whole, "    **Impact:**\n      - changes", "    **Impact:**\n      - changes\n      - none"))
    got = p.run("--check-handed-back", path)
    check("--check-handed-back reports a Read Assessment whose Impact holds none beside another", reports(got, "== check-handed-back", "Impact is not a list holding none alone"), shown(got))
    path = p.put(report_at(JUDGMENT), swap(whole, "    **Reason:** The section names the ferry and is where its times are to stand. \\\n    **Goals:**\n      - " + GOAL,
                                           "    **Reason:** The section names the ferry and is where its times are to stand. \\\n    **Goals:**\n      - guide-says-what-the-ferry-costs"))
    got = p.run("--check-handed-back", path)
    check("--check-handed-back reports a Read Assessment naming a goal the design does not hold", reports(got, "== check-handed-back", "Goals name guide-says-what-the-ferry-costs, which is no design goal's Name"), shown(got))


def second_share(cause=None, steer=False, area=FERRY):
    """-> (a project whose design's log names a first research report, the path of a second handed back, assessing an
    Area again): the second naming the cause given, the design holding a set of steers logged after the first where
    steer is set."""
    p = Project("assessed-again")
    log = AGREED + RESEARCH + ((("steer", {"Steering Decision": "winter-hours-count"}),) if steer else ())
    text = a_design(log=log)
    p.design(text=swap(text, "\n## Design Plan Steps", STEER) if steer else text)
    p.put(report_at(JUDGMENT, 1), a_report("research"))
    second = swap(cold_part(a_report("research", entry="handed-off-judgment-2")), "**Area:** " + FERRY, "**Area:** " + area).replace("**Reads:**\n  - " + FERRY, "**Reads:**\n  - " + area)
    if cause:
        second = second.rstrip("\n") + "\n\n    **Assessed Again For:** %s\n" % cause
    return p, p.put(report_at(JUDGMENT, 2), second)


@test("research", "an area assessed again names a cause that counts")
def _():
    first = ".ai/tmp/design-specs/%s/reports/handed-off-judgment/1.md" % NAME
    p, path = second_share()
    for flag, heading in (("--check-handed-back", "== check-handed-back"), ("--take-up-report", "== take-up-report, not taken up")):
        got = p.run(flag, path)
        check("%s reports a research report assessing again an Area a binding report assesses, naming no cause" % flag,
              reports(got, heading, ["Read Assessment %s assesses again an Area %s already assesses, and names no cause in its Assessed Again For" % (FERRY, first), RULE % "area-reassessments-name-their-cause"]), shown(got))
    p, path = second_share(cause="steer-1")
    got = p.run("--check-handed-back", path)
    check("--check-handed-back reports a cause naming a set of steers the design's log does not hold",
          reports(got, "== check-handed-back", "names steer-1, a set's entry the design's log does not hold"), shown(got))
    p, path = second_share(cause="a second look")
    got = p.run("--check-handed-back", path)
    check("--check-handed-back reports a cause that is neither a set of steers nor a finding", reports(got, "== check-handed-back", "names a second look, neither a set's steer entry nor a finding cited as a place"), shown(got))
    p, path = second_share(cause="steer-1", steer=True)
    got = p.run("--check-handed-back", path)
    check("--check-handed-back passes a research report assessing an Area again for a set of steers logged after the report that assessed it", passes(got, "== check-handed-back", "0 problems"), shown(got))
    got = p.run("--take-up-report", path)
    check("and --take-up-report takes it up", passes(got, "== take-up-report " + path, "0 problems"), shown(got))
    p, path = second_share(area=LIGHTHOUSE)
    got = p.run("--check-handed-back", path)
    check("--check-handed-back asks no cause of a research report assessing an Area no binding report assesses", passes(got, "== check-handed-back", "0 problems"), shown(got))


@test("research", "no check's entry stands before the agreement of its major version's goals")
def _():
    for skill in SKILLS:
        p = Project("goals-gate")
        design = p.design(skill=skill, log=(("entered", {"Reason": "taken up"}),))
        taken_up(p, JUDGMENT, a_report("research", skill=skill, version="0.1.0").replace("**Design Version:** 0.1.0 \\\n", "**Design Version:** 1.0.0 \\\n"), skill=skill)
        before = p.read(design)
        got = p.run("--log-entry", design, JUDGMENT, *CHECK_FIELDS, skill=skill)
        check("--log-entry of %s refuses a check's entry before the user's agreement to the goals" % skill,
              reports(got, "== log-entry, not logged", ["a check's entry with no goals-agreed entry before it in its major version", RULE % "goals-agreed-before-checks"]) and p.read(design) == before, shown(got))
        agreed = p.run("--log-entry", design, "goals-agreed", skill=skill)
        got = p.run("--log-entry", design, JUDGMENT, *CHECK_FIELDS, skill=skill)
        check("--log-entry of %s appends it once the goals are agreed" % skill, agreed[0] == 0 and passes(got, "== log-entry", "- **Entry:** handed-off-judgment-1"), shown(got))
        for flag in ("--check-design-form", "--check-design"):
            got = p.run(flag, p.design("gate-in-a-log", skill=skill, log=(("entered", {"Reason": "taken up"}),) + RESEARCH), skill=skill)
            check("%s of %s reports a log holding a check's entry with no goals-agreed entry before it" % (flag, skill),
                  reports(got, "== %s gate-in-a-log" % flag[2:], ["log entry handed-off-judgment-1 is a check's entry with no goals-agreed entry before it in its major version", RULE % "goals-agreed-before-checks"]), shown(got))


@test("research", "a check's entry stands at the version its report read")
def _():
    for skill in SKILLS:
        p = Project("version-read")
        design = p.design(skill=skill, log=DRAFTED)
        path = taken_up(p, JUDGMENT, a_report("research", skill=skill, version="1.0.0"), skill=skill)
        got = p.run("--log-entry", design, JUDGMENT, *CHECK_FIELDS, skill=skill)
        check("--log-entry of %s stamps a check's entry at the version its report read, an earlier one the log held, and leaves the header at the log's" % skill,
              passes(got, "== log-entry", "**Design Version:** 1.0.0 \\\n    **Model:**") and "**Version:** 1.0.1 \\" in p.read(design), shown(got))
        form = p.run("--check-design-form", design, skill=skill)
        check("and --check-design-form of %s passes the log it wrote" % skill, passes(form, "== check-design-form", "0 problems"), shown(form))
        p = Project("version-never-held")
        design = p.design(skill=skill, log=DRAFTED)
        taken_up(p, JUDGMENT, a_report("research", skill=skill, version="1.4.0"), skill=skill)
        before = p.read(design)
        got = p.run("--log-entry", design, JUDGMENT, *CHECK_FIELDS, skill=skill)
        check("--log-entry of %s refuses a check's entry whose report read a version the log never held" % skill,
              reports(got, "== log-entry, not logged", ["Reading holds Design Version 1.4.0, a version the design's log never held", RULE % "entry-at-the-version-read"]) and p.read(design) == before, shown(got))
        for flag in ("--check-design-form", "--check-design"):
            got = p.run(flag, p.design("version-in-a-log", skill=skill, log=AGREED + (("handed-off-judgment", {"Design Version": "1.4.0"}),)), skill=skill)
            check("%s of %s reports a log holding a check's entry at a version the log never held before it" % (flag, skill),
                  reports(got, "== %s version-in-a-log" % flag[2:], ["log entry handed-off-judgment-1's Design Version is 1.4.0, a version its log never held before it", RULE % "entry-at-the-version-read"]), shown(got))
    p = Project("version-form")
    got = p.run("--check-design-form", p.design(text=swap(a_design(log=DRAFTED), "**Version:** 1.0.1", "**Version:** 1.2.0")))
    check("--check-design-form reports a header whose Version is not the one its log gives", reports(got, "== check-design-form", "Version is 1.2.0, where its log gives 1.0.1"), shown(got))


@test("research", "the sub-scopes an audit's entry holds are sub-scopes, and keep each the design changed")
def _():
    for skill in SKILLS:
        p = Project("sub-scopes")
        for flag in ("--check-design-form", "--check-design"):
            good = p.run(flag, researched(p, skill=skill, status="applying", log=APPLYING_RESEARCHED + (("audit-specs", {"Design Version": "1.0.1", "Settled Sub-scopes": "documentation; other"}),)), skill=skill)
            check("%s of %s passes a log whose audit entry holds sub-scopes alone" % (flag, skill), passes(good, "== %s %s" % (flag[2:], NAME), "0 problems"), shown(good))
            got = p.run(flag, researched(p, skill=skill, status="applying", log=APPLYING_RESEARCHED + (("audit-specs", {"Design Version": "1.0.1", "Settled Sub-scopes": "documentation; the-attic"}),)), skill=skill)
            check("%s of %s reports a log whose audit entry names what is no sub-scope" % (flag, skill),
                  reports(got, "== %s %s" % (flag[2:], NAME), "an audit-specs entry's Settled Sub-scopes names the-attic, not one of core-canon, skills, application-specs, documentation, other"), shown(got))
        design = p.design(skill=skill, status="applying", log=APPLYING)
        p.put(report_at("audit-specs", skill=skill), a_clean_report("audit-specs"))
        before = p.read(design)
        got = p.run("--log-entry", design, "audit-specs", *ROUND_FIELDS, "Settled Sub-scopes=the-attic", skill=skill)
        check("--log-entry of %s refuses an audit's entry naming what is no sub-scope" % skill, reports(got, "== log-entry, not logged", "Settled Sub-scopes names the-attic, not one of") and p.read(design) == before, shown(got))
        kept, dropped = ("documentation", "core-canon") if skill == "design-specs" else ("other", "documentation")
        got = p.run("--log-entry", design, "audit-specs", *ROUND_FIELDS, "Settled Sub-scopes=" + dropped, skill=skill)
        check("--log-entry of %s refuses an audit's entry whose Settled Sub-scopes drop a sub-scope holding a file the design changed" % skill,
              reports(got, "== log-entry, not logged", "the audit-specs entry's Settled Sub-scopes drop %s, each holding a file the design changed" % kept) and p.read(design) == before, shown(got))
        got = p.run("--log-entry", design, "audit-specs", *ROUND_FIELDS, "Settled Sub-scopes=%s; %s" % (dropped, kept), skill=skill)
        check("--log-entry of %s appends an audit's entry whose Settled Sub-scopes keep each sub-scope the design changed" % skill, passes(got, "== log-entry", "**Settled Sub-scopes:** %s; %s" % (dropped, kept)), shown(got))


def outside_every_area(text):
    """-> a research report whose Search by meaning holds a place lying in no Area it assesses."""
    return swap(text, "    **Places:**\n      - " + FERRY, "    **Places:**\n      - %s\n      - %s" % (FERRY, LIGHTHOUSE))


COVERS = "Search ferry-times-by-meaning of %s holds %s, which no binding research report's Read Assessment's Area covers"
BY_TERMS = "the goal %s is named by no Search by terms of the durable files naming no commit, among the research binding the design" % GOAL


@test("research", "the research binding a design is read together before its plan's approval")
def _():
    for skill in SKILLS:
        p = Project("research-union")
        area = LIGHTHOUSE
        path = p.put(report_at(JUDGMENT, skill=skill), outside_every_area(a_report("research", skill=skill)) if skill == "design-specs"
                     else swap(a_report("research", skill=skill), "    **Places:**\n      - `src/ferry.py`", "    **Places:**\n      - `src/ferry.py`\n      - " + LIGHTHOUSE))
        design = p.design(skill=skill, log=AGREED + RESEARCH + (("plan-change", {}),))
        for flag in ("--check-design", "--stamp-validation"):
            got = p.run(flag, design, skill=skill)
            check("%s of %s reports, of a design not yet approved, a place its research's Search holds that no Area it assesses covers, and a goal no Search by terms names" % (flag, skill),
                  reports(got, "== " + ("check-design " + NAME if flag == "--check-design" else "stamp-validation, not stamped"),
                          [COVERS % (path, area), RULE % "research-covers-its-matches", BY_TERMS, RULE % "goals-searched-over-every-durable-file"]), shown(got))


@test("research", "the first check of the builder's after research is taken in reads the research together")
def _():
    p = Project("research-at-the-entry")
    design = p.design(log=AGREED + RESEARCH + (("plan-change", {}),))
    path = p.put(report_at(JUDGMENT), outside_every_area(a_report("research")))
    own = p.put(report_at("self-review"), a_report("self-review"))
    before = p.read(design)
    for flag, args, heading in (("--check-settled-report", (own,), "== check-settled-report"), ("--log-entry", (design, "self-review") + CHECK_FIELDS, "== log-entry, not logged")):
        got = p.run(flag, *args)
        check("%s refuses a self-review standing first after research whose Search holds a place no Area covers, and whose goal no Search by terms names" % flag,
              reports(got, heading, [COVERS % (path, LIGHTHOUSE), BY_TERMS]) and p.read(design) == before, shown(got))


@test("research", "an approved or applying design's research is not read against the files")
def _():
    for skill in SKILLS:
        for status, log in (("approved", APPROVED_RESEARCHED), ("applying", APPLYING_RESEARCHED), ("complete", APPLYING_RESEARCHED)):
            p = Project("research-frozen")
            design = p.design(skill=skill, status=status, log=log)
            p.put(report_at(JUDGMENT, skill=skill), outside_every_area(a_report("research")) if skill == "design-specs"
                  else swap(a_report("research", skill=skill), "    **Places:**\n      - `src/ferry.py`", "    **Places:**\n      - `src/ferry.py`\n      - " + LIGHTHOUSE))
            got = p.run("--check-design", design, skill=skill)
            check("--check-design of %s reports nothing of the research of a design that is %s: no place as unassessed, and no goal as unsearched" % (skill, status),
                  passes(got, "== check-design " + NAME, "0 problems"), shown(got))


# ---------------------------------------------------------------- the builder's self-review

SELF = "self-review"
RE_EVALUATION = "  - **Check:** problem-read-against-the-guide \\\n    **Kind:** problem re-evaluation \\\n    **Places Checked:**\n      - `docs/guide.md § The Ferry`\n\n" \
                "    **Result:** The section still names the ferry and gives no time.\n\n"
LINKED = "  - **Check:** work-handed-on \\\n    **Kind:** linked work \\\n    **Places Checked:**\n      - `.ai/plans/design-specs/%s.md § Out of Scope`\n\n    **Result:** The design hands no work on.\n\n" % NAME
TABLE = "\n**Construct:** `specs/methodology/modeling-constructs.md § Constructs § Decision Table` \\\n**Hit Policy:** First \\\n**Conditions:** Season\n\n" \
        "| Season | The ferry |\n|---|---|\n| \"winter\" | runs twice a day |\n| - | runs each hour |\n"
TRACE = "## Traces\n\n**Records:**\n  - **Trace:** hours-by-season \\\n    **Mechanism:** `docs/guide.md § The Ferry` \\\n    **Outcome:** name the mechanism\n\n## Builder Checks"


def a_check(key, kind, *places):
    return "  - **Check:** %s \\\n    **Kind:** %s \\\n    **Places Checked:**\n%s\n\n    **Result:** It holds.\n\n" % (key, kind, "\n".join("      - `%s`" % place for place in places))


def with_checks(text, *checks):
    """-> a self-review's report with Builder Checks added after those it holds."""
    return swap(text, "## Settlement", "".join(checks) + "## Settlement")


@test("self-review", "a self-review's entry is appended, its script checks' output written into its report")
def _():
    for skill in SKILLS:
        p = Project("self-review")
        design = p.design(skill=skill, log=DRAFTED)
        path = p.put(report_at(SELF, skill=skill), a_report("self-review", skill=skill))
        before = p.held(".ai")
        got = p.run("--check-settled-report", path, skill=skill)
        check("--check-settled-report of %s passes a self-review's report holding each Builder Check required of it, and writes nothing" % skill,
              passes(got, "== check-settled-report " + path, "0 problems") and p.held(".ai") == before, shown(got))
        got = p.run("--log-entry", design, SELF, *CHECK_FIELDS, skill=skill)
        now = p.read(path)
        check("--log-entry of %s appends its entry, and writes the output of the checks a self-review before the apply runs into its report, where the form orders the part" % skill,
              passes(got, "== log-entry", "- **Entry:** self-review-1") and "## Script Output\n\n```text\n$ --check-cited-headings %s\n" % design in now
              and "$ --check-target-kind %s\n== check-target-kind %s\n0 problems\n\nexit 0\n" % (design, NAME) in now
              and now.index("## Builder Checks") < now.index("## Script Output") < now.index("## Settlement") and "check-kept-tests" not in now, shown(got) + now[-900:])


@test("self-review", "a self-review holds each Builder Check required of it")
def _():
    whole = a_report("self-review")
    for label, text, said in (("no check of the work it hands on", swap(whole, LINKED, ""), "no Builder Check of linked work, which is required of it"),
                              ("no check of its steers", whole.split("  - **Check:** steers-read")[0] + "  - **Check:** work-handed-on" + whole.split("  - **Check:** work-handed-on")[1],
                               "no Builder Check of steers against the user's messages, which is required of it")):
        p = Project("builder-checks")
        design = p.design(log=DRAFTED)
        path = p.put(report_at(SELF), text)
        before = p.read(design)
        got = p.run("--check-settled-report", path)
        check("--check-settled-report reports a self-review holding " + label, reports(got, "== check-settled-report", said), shown(got))
        got = p.run("--log-entry", design, SELF, *CHECK_FIELDS)
        check("--log-entry refuses the entry of a self-review holding " + label, reports(got, "== log-entry, not logged", said) and p.read(design) == before, shown(got))


@test("self-review", "the first self-review of a major version records the re-evaluation of the Problem")
def _():
    for skill in SKILLS:
        whole = a_report("self-review", skill=skill)
        p = Project("re-evaluation")
        design = p.design(skill=skill, log=DRAFTED)
        path = p.put(report_at(SELF, skill=skill), swap(whole, RE_EVALUATION, ""))
        before = p.read(design)
        got = p.run("--log-entry", design, SELF, *CHECK_FIELDS, skill=skill)
        check("--log-entry of %s refuses the first self-review of a major version recording no re-evaluation of the Problem" % skill,
              reports(got, "== log-entry, not logged", "no Builder Check of problem re-evaluation, which is required of it") and p.read(design) == before, shown(got))
        text = swap(a_design(skill=skill, log=DRAFTED), "without saying when it runs.", "without saying when it runs, though %s gives the keeper's hours." % LIGHTHOUSE)
        design = p.design(skill=skill, text=text)
        p.put(path, whole)
        got = p.run("--log-entry", design, SELF, *CHECK_FIELDS, skill=skill)
        check("--log-entry of %s refuses one whose re-evaluation leaves out a place the Problem cites" % skill,
              reports(got, "== log-entry, not logged", "its Builder Checks of problem re-evaluation leave out " + LIGHTHOUSE) and p.read(design) == text, shown(got))
        p.put(path, swap(whole, "      - `docs/guide.md § The Ferry`\n\n    **Result:** The section still", "      - `docs/guide.md § The Ferry`\n      - %s\n\n    **Result:** The section still" % LIGHTHOUSE))
        got = p.run("--log-entry", design, SELF, *CHECK_FIELDS, skill=skill)
        check("--log-entry of %s appends one whose re-evaluation covers each place the Problem cites" % skill, passes(got, "== log-entry", "- **Entry:** self-review-1"), shown(got))
        p.put(report_at(SELF, 2, skill=skill), swap(a_report("self-review", skill=skill, entry="self-review-2"), RE_EVALUATION, ""))
        got = p.run("--log-entry", design, SELF, *CHECK_FIELDS, skill=skill)
        check("--log-entry of %s asks no re-evaluation of a later self-review of the same major version" % skill, passes(got, "== log-entry", "- **Entry:** self-review-2"), shown(got))
    p = Project("re-evaluation-again")
    log = DRAFTED + ((SELF, {}), ("design-reassessment", {"Cause": "changed foundation: quay-rebuilt finished"}), ("goals-agreed", {}), ("plan-change", {}))
    design = p.design(log=log)
    p.put(report_at(SELF, 2), swap(a_report("self-review", entry="self-review-2", version="2.0.1"), RE_EVALUATION, ""))
    got = p.run("--log-entry", design, SELF, *CHECK_FIELDS)
    check("--log-entry asks the re-evaluation again of the first self-review of the major version a design reassessment starts",
          reports(got, "== log-entry, not logged", "no Builder Check of problem re-evaluation, which is required of it"), shown(got))


@test("self-review", "a self-review traces each mechanism its phase gives it")
def _():
    whole = a_report("self-review")
    p = Project("traces")
    p.put("docs/guide.md", swap(base("guide.md"), "The ferry leaves from the north quay.\n", "The ferry leaves from the north quay.\n" + TABLE))
    design = p.design(log=DRAFTED)
    path = p.put(report_at(SELF), whole)
    before = p.read(design)
    got = p.run("--check-settled-report", path)
    check("--check-settled-report reports a self-review holding no Trace of a Decision Table a step's What names", reports(got, "== check-settled-report", "no Trace of the Decision Table at " + FERRY), shown(got))
    got = p.run("--log-entry", design, SELF, *CHECK_FIELDS)
    check("--log-entry refuses its entry", reports(got, "== log-entry, not logged", "no Trace of the Decision Table at " + FERRY) and p.read(design) == before, shown(got))
    p.put(path, swap(whole, "## Builder Checks", TRACE))
    got = p.run("--check-settled-report", path)
    check("--check-settled-report passes a self-review before the apply whose Trace of the mechanism holds the outcome of the mechanism's test", passes(got, "== check-settled-report", "0 problems"), shown(got))
    p.put(path, swap(whole, "## Builder Checks", swap(TRACE, " \\\n    **Outcome:** name the mechanism", "")))
    got = p.run("--check-settled-report", path)
    check("--check-settled-report reports a Trace before the apply holding no Outcome", reports(got, "== check-settled-report", "Trace hours-by-season holds no Outcome, which its form requires where the report is a self-review's before the apply"), shown(got))


@test("self-review", "a self-review following a round's change reads each place a Miss names, and works the round's cases")
def _():
    p, design, path = a_round("after-a-round")
    logged = p.run("--log-entry", design, REVIEW, *ROUND_FIELDS)
    worked = a_check("round-worked", "worked case", "%s § Causes [Cause: %s]" % (path, CAUSE), "%s § Findings [Finding: %s]" % (path, FINDING))
    own = p.put(report_at(SELF), with_checks(a_report("self-review"), worked))
    got = p.run("--check-settled-report", own)
    check("--check-settled-report passes a self-review after a round whose Reads cover each place a Miss names and whose worked case covers the round's Cause and its flaw",
          logged[0] == 0 and passes(got, "== check-settled-report", "0 problems"), shown(logged) + shown(got))
    p.put(own, swap(with_checks(a_report("self-review"), worked), "\n  - `docs/guide.md`\n", "\n"))
    got = p.run("--check-settled-report", own)
    check("--check-settled-report reports one whose Reads leave out a place a Miss of the phase names", reports(got, "== check-settled-report", "its Reads leave out %s, a place a Miss of the phase names" % FERRY), shown(got))
    p.put(own, a_report("self-review"))
    got = p.run("--log-entry", design, SELF, *CHECK_FIELDS)
    check("--log-entry refuses one working no case of the round's change", reports(got, "== log-entry, not logged", "no Builder Check of worked case, which is required of it"), shown(got))
    p.put(own, with_checks(a_report("self-review"), a_check("round-worked", "worked case", "%s § Causes [Cause: %s]" % (path, CAUSE))))
    got = p.run("--log-entry", design, SELF, *CHECK_FIELDS)
    check("--log-entry refuses one whose worked case leaves out the round's flaw",
          reports(got, "== log-entry, not logged", "its Builder Checks of worked case leave out `%s § Findings [Finding: %s]`" % (path, FINDING)), shown(got))


# ---------------------------------------------------------------- a taken-up report, and what the builder does after

@test("taken-up", "a taken-up Finding stands though the builder removes the goal it names")
def _():
    for skill in SKILLS:
        p, design, path = a_round("goal-removed", skill=skill, own=lambda t: t.replace(GOAL, "guide-gives-each-seasons-hours"))
        p.put(design, p.read(design).replace(GOAL, "guide-gives-each-seasons-hours"))
        before = p.read(path)
        got = p.run("--check-settled-report", path, skill=skill)
        check("--check-settled-report of %s passes a taken-up report whose Finding names a goal the builder renamed while settling: no check after the take-up reads a cold part against the design" % skill,
              passes(got, "== check-settled-report " + path, "0 problems") and p.read(path) == before, shown(got))
        got = p.run("--log-entry", design, REVIEW, *ROUND_FIELDS, skill=skill)
        check("and --log-entry of %s appends its entry" % skill, passes(got, "== log-entry", "- **Entry:** adversarial-review-1"), shown(got))
    p, design, path = a_round("objective-removed", cold=lambda t: swap(t, "    **Affected Goals:**\n      - " + GOAL, "    **Affected Goals:**\n      - %s\n\n    **Affected Step Objectives:**\n      - %s" % (GOAL, OBJECTIVE)))
    p.put(design, p.read(design).replace(OBJECTIVE, "section-gives-each-seasons-crossings"))
    got = p.run("--check-settled-report", path)
    check("--check-settled-report passes a taken-up report whose Finding names a step Objective the builder's revision replaced", passes(got, "== check-settled-report " + path, "0 problems"), shown(got))


@test("taken-up", "a taken-up report refused for a fault in the builder's parts stays with the builder")
def _():
    for skill in SKILLS:
        p, design, path = a_round("builders-fault", skill=skill, own=lambda t: swap(t, "    **Settled Findings:**\n      - " + FINDING, "    **Settled Findings:**\n      - reviewer-1-another-finding"))
        before = p.read(path)
        for flag, args, heading in (("--check-settled-report", (path,), "== check-settled-report"), ("--log-entry", (design, REVIEW) + ROUND_FIELDS, "== log-entry, not logged")):
            got = p.run(flag, *args, skill=skill)
            check("%s of %s refuses a taken-up report for a Finding the builder's Settlement leaves unsettled, and leaves the report with the builder, its cold parts and its settlement as they stand" % (flag, skill),
                  reports(got, heading, "Finding %s is settled by 0 Settlements, not exactly one" % FINDING) and "goes back to its cold agent" not in got[1] and p.read(path) == before, shown(got))


@test("taken-up", "a check cut short by a freeing has its entry appended")
def _():
    cut = lambda t: swap(swap(swap("## Settlement" + t.split("## Settlement")[1], "**Ending:** its own settling", "**Ending:** cut short, a design reassessment for a changed foundation"),
                              "    **Fix Authority:** the builder's \\\n    **Cause:** times-by-season \\\n", "    **Fix Authority:** the user's \\\n    **User Decision:** taken by a changed foundation \\\n"),
                         "The Objective was revised to give each season's first and last crossing.", "The design was freed, and is made afresh.")
    for skill in SKILLS:
        p = a_workstack("cut-short")
        design = p.design(skill=skill, log=DRAFTED, depends=("" if skill == "design-specs" else "design-specs/") + COMPLETE)
        text = a_report("review", skill=skill)
        path = p.put(report_at(REVIEW, skill=skill), cold_part(text))
        back = p.run("--check-handed-back", path, skill=skill)
        freed = p.run("--free-design", design, skill=skill)
        up = p.run("--take-up-report", path, skill=skill)
        p.put(path, p.read(path).rstrip("\n") + "\n\n" + cut(builder_part(text)))
        got = p.run("--check-settled-report", path, skill=skill)
        check("--check-settled-report of %s passes a round handed back before its design was freed, settled as cut short by the design reassessment, its findings taken by the changed foundation" % skill,
              back[0] == 0 and freed[0] == 0 and up[0] == 0 and passes(got, "== check-settled-report " + path, "0 problems"), shown(back) + shown(freed) + shown(up) + shown(got))
        got = p.run("--log-entry", design, REVIEW, *ROUND_FIELDS, skill=skill)
        now = p.read(design)
        check("--log-entry of %s appends its entry after the freeing, at the version its report read, though the goals of the new major version are not yet agreed" % skill,
              passes(got, "== log-entry", "- **Entry:** adversarial-review-1") and "**Design Version:** 1.0.1 \\\n    **Model:**" in got[1] and "**Version:** 2.0.0 \\" in now, shown(got))
        form = p.run("--check-design-form", design, skill=skill)
        check("and the design of %s holds its form" % skill, passes(form, "== check-design-form", "0 problems"), shown(form))


# ---------------------------------------------------------------- a script's kept tests, run by the design script

KEPT = "tests/spec-of-record/scripts/"
KEPT_FILE = "SCRIPT_FILES = (\"tools/guide.py\",)\nFORM_FILES = (\"docs/guide.md\",)\nimport sys\nprint(\"  %s  %s\")\nsys.exit(%d)\n"
KEPT_RULE = RULE % "kept-tests-pass-at-the-self-review"
OTHER_DESIGN = ".ai/plans/design-specs/other-design.md"


def kept_tests(p, verdict=0, comparison=None, lists=()):
    """Give a project a set of kept tests of a script of its own, the guide's, whose code is tools/guide.py and whose
    form is read from docs/guide.md, passing or failing as verdict says; and, comparison an exit status, a kept
    comparison beside it listing the designs given."""
    p.put(KEPT + "guide-tests.py", KEPT_FILE % ("FAIL" if verdict else "pass", "the guide's one test", verdict))
    p.put("tools/guide.py", "print('the guide')\n")
    if comparison is not None:
        listing = "\\n".join("design " + d for d in lists) or "0 designs read differently"
        p.put(KEPT + "guide-comparison.py", KEPT_FILE.replace("print(\"  %s  %s\")", "print(\"%s%s\")") % ("", listing, comparison))


def applied(p, skill="design-specs", log=APPLYING, checks=(), **given):
    """-> (the path of an applying design, the path of its first self-review's report over the applied work)."""
    design = p.design(skill=skill, status="applying", log=log, **given)
    return design, p.put(report_at(SELF, skill=skill), with_checks(a_report("self-review", skill=skill), *checks))


@test("kept", "a self-review over applied work is appended where the kept tests pass, their result in its report")
def _():
    for skill in SKILLS:
        p = Project("kept-pass")
        kept_tests(p)
        design, path = applied(p, skill, Target="`docs/guide.md`")
        got = p.run("--log-entry", design, SELF, *CHECK_FIELDS, skill=skill)
        now = p.read(path)
        check("--log-entry of %s runs the kept tests of a script whose form the design's changes hold, a change to a form alone, writes what the run gave into the report, and appends the entry" % skill,
              passes(got, "== log-entry", "- **Entry:** self-review-1")
              and "$ --check-kept-tests\n$ python %sguide-tests.py\nrun for docs/guide.md\n  pass  the guide's one test\nexit 0\n" % KEPT in now
              and now.index("$ --check-changed-files") < now.index("$ --check-kept-tests") < now.index("## Settlement"), shown(got) + now[-700:])
    p = Project("kept-code")
    kept_tests(p)
    design, path = applied(p, log=APPLYING + (("direct-edit", {"Places": "tools/guide.py"}),), Target="`docs/notes.md`")
    got = p.run("--log-entry", design, SELF, *CHECK_FIELDS)
    check("--log-entry runs them where the design's changes hold the script's code", passes(got, "== log-entry", "- **Entry:** self-review-1") and "run for tools/guide.py\n" in p.read(path), shown(got))


@test("kept", "a self-review over applied work is refused where a kept test fails")
def _():
    for skill in SKILLS:
        p = Project("kept-fail")
        kept_tests(p, verdict=1)
        design, path = applied(p, skill, Target="`docs/guide.md`")
        before = p.read(design)
        got = p.run("--log-entry", design, SELF, *CHECK_FIELDS, skill=skill)
        now = p.read(path)
        check("--log-entry of %s refuses the entry of a self-review over applied work where a kept test of a script the design changed fails, the tests' result written into its report" % skill,
              reports(got, "== log-entry, not logged", ["%s: %sguide-tests.py holds a test that fails, or could not be run, exit 1" % (path, KEPT), KEPT_RULE]) and p.read(design) == before
              and "$ --check-kept-tests\n$ python %sguide-tests.py\nrun for docs/guide.md\n  FAIL  the guide's one test\nexit 1\n" % KEPT in now, shown(got) + now[-500:])
        got = p.run("--check-settled-report", path, skill=skill)
        check("--check-settled-report of %s, made apart from the entry, runs no kept test: it passes the same report and names none" % skill,
              passes(got, "== check-settled-report " + path, "0 problems") and "guide-tests" not in got[1], shown(got))
    p = Project("kept-before-the-apply")
    kept_tests(p, verdict=1)
    design = p.design(log=DRAFTED)
    path = p.put(report_at(SELF), a_report("self-review"))
    got = p.run("--log-entry", design, SELF, *CHECK_FIELDS)
    check("--log-entry runs no kept test for a self-review before the apply", passes(got, "== log-entry", "- **Entry:** self-review-1") and "check-kept-tests" not in p.read(path), shown(got))


@test("kept", "a self-review over applied work runs no kept test where the design changed no file of a script holding them")
def _():
    p = Project("kept-none")
    kept_tests(p, verdict=1)
    design, path = applied(p, log=APPLYING + (("direct-edit", {"Places": "tools/other.py"}),), Target="`docs/notes.md`")
    got = p.run("--log-entry", design, SELF, *CHECK_FIELDS)
    now = p.read(path)
    check("--log-entry runs no kept test of a script none of whose files the design changed, says which changed script no set of kept tests names, and appends the entry",
          passes(got, "== log-entry", "- **Entry:** self-review-1") and "$ --check-kept-tests\nno set of kept tests names tools/other.py\n" in now and "guide-tests" not in now, shown(got) + now[-400:])


@test("kept", "a pass proving the fixes runs the kept tests too")
def _():
    p = Project("kept-pass-of-the-fixes")
    kept_tests(p, verdict=1)
    design = p.design(status="applying", log=APPLYING + ((SELF, {}), ("post-apply-review", {})), Target="`docs/guide.md`")
    path = p.put(report_at(SELF, 2), swap(a_report("self-review", entry="self-review-2"), RE_EVALUATION, ""))
    got = p.run("--log-entry", design, SELF, *CHECK_FIELDS)
    check("--log-entry refuses the entry of a pass proving the fixes, a self-review after the apply's review, where a kept test fails",
          reports(got, "== log-entry, not logged", ["guide-tests.py holds a test that fails, or could not be run, exit 1", KEPT_RULE]), shown(got))
    kept_tests(p)
    got = p.run("--log-entry", design, SELF, *CHECK_FIELDS)
    check("and appends it where they pass", passes(got, "== log-entry", "- **Entry:** self-review-2") and "run for docs/guide.md\n  pass  the guide's one test\nexit 0" in p.read(path), shown(got))


@test("kept", "a self-review judges each design a kept comparison lists")
def _():
    judged = a_check("comparison-judged", "differential test", OTHER_DESIGN)
    for label, checks, said in (("recording no differential test", (), "no Builder Check of differential test, which is required of it"),
                                ("whose differential test leaves out a design the comparison lists", (a_check("comparison-judged", "differential test", ".ai/plans/design-specs/%s.md" % NAME),),
                                 "its Builder Checks of differential test leave out `%s`" % OTHER_DESIGN),
                                ("whose differential test judges each design the comparison lists", (judged,), None)):
        p = Project("kept-comparison")
        kept_tests(p, comparison=0, lists=(OTHER_DESIGN,))
        design, path = applied(p, checks=checks, Target="`docs/guide.md`")
        got = p.run("--log-entry", design, SELF, *CHECK_FIELDS)
        if said:
            check("--log-entry runs the kept comparison of a script the design changed, and refuses the entry of a self-review " + label,
                  reports(got, "== log-entry, not logged", said) and "guide-comparison.py\nrun for docs/guide.md\ndesign %s\nexit 0" % OTHER_DESIGN in p.read(path), shown(got) + p.read(path)[-500:])
        else:
            check("--log-entry appends the entry of a self-review " + label, passes(got, "== log-entry", "- **Entry:** self-review-1") and "design " + OTHER_DESIGN in p.read(path), shown(got))
    p = Project("kept-comparison-failed")
    kept_tests(p, comparison=2)
    design, path = applied(p, Target="`docs/guide.md`")
    got = p.run("--log-entry", design, SELF, *CHECK_FIELDS)
    check("--log-entry refuses the entry where the comparison could not be made", reports(got, "== log-entry, not logged", ["%sguide-comparison.py could not be made, exit 2" % KEPT, KEPT_RULE]), shown(got))
    p = Project("kept-comparison-lists-none")
    kept_tests(p, comparison=0)
    design, path = applied(p, Target="`docs/guide.md`")
    got = p.run("--log-entry", design, SELF, *CHECK_FIELDS)
    check("--log-entry asks no differential test where the comparison lists no design", passes(got, "== log-entry", "- **Entry:** self-review-1") and "0 designs read differently" in p.read(path), shown(got))


@test("kept", "check-kept-tests runs the kept tests of each script the files given hold a file of")
def _():
    for skill in SKILLS:
        p = Project("kept-action")
        kept_tests(p, comparison=0, lists=(OTHER_DESIGN,))
        for given, held in ((("docs/guide.md",), "docs/guide.md"), (("tools/guide.py", "docs/notes.md"), "tools/guide.py")):
            got = p.run("--check-kept-tests", *given, skill=skill)
            check("--check-kept-tests of %s, given %s, runs the kept tests and the kept comparison of the script holding it, names no design, and passes whatever the comparison lists" % (skill, " and ".join(given)),
                  passes(got, "== check-kept-tests, over %d changed file%s" % (len(given), "" if len(given) == 1 else "s"), "0 problems")
                  and "$ python %sguide-tests.py\nrun for %s\n  pass  the guide's one test\nexit 0\n" % (KEPT, held) in got[1]
                  and "$ python %sguide-comparison.py\nrun for %s\n" % (KEPT, held) in got[1] and "design " + OTHER_DESIGN in got[1], shown(got))
        got = p.run("--check-kept-tests", "docs/notes.md", "tools/other.py", skill=skill)
        check("--check-kept-tests of %s, given no file of a script holding kept tests, runs none and says which changed script no set of kept tests names" % skill,
              passes(got, "== check-kept-tests, over 2 changed files", "no set of kept tests names tools/other.py\n\n0 problems") and "guide-tests" not in got[1], shown(got))
        got = p.run("--check-kept-tests", "docs/notes.md", skill=skill)
        check("--check-kept-tests of %s, given a file of no script, says no changed file is one" % skill,
              passes(got, "== check-kept-tests, over 1 changed file", "no changed file is a file of a script holding kept tests\n\n0 problems"), shown(got))


@test("kept", "check-kept-tests fails where a kept test fails or a kept file cannot be run")
def _():
    for skill in SKILLS:
        p = Project("kept-action-fails")
        kept_tests(p, verdict=1)
        got = p.run("--check-kept-tests", "docs/guide.md", skill=skill)
        check("--check-kept-tests of %s fails where a kept test fails, printing what the run gave" % skill,
              reports(got, "== check-kept-tests, over 1 changed file", ["  FAIL  the guide's one test\nexit 1", KEPT_RULE, "%sguide-tests.py holds a test that fails, or could not be run, exit 1" % KEPT, "1 problem"]), shown(got))
    p = Project("kept-action-unread")
    kept_tests(p)
    p.put(KEPT + "ledger-tests.py", "SCRIPT_FILES = \"tools/ledger.py\"\nprint('never run')\n")
    got = p.run("--check-kept-tests", "docs/notes.md")
    check("--check-kept-tests fails where a set of kept tests does not say which files are its script's, whatever files it is given",
          reports(got, "== check-kept-tests", ["%sledger-tests.py cannot be run: it names no SCRIPT_FILES and no FORM_FILES as a tuple of paths at its top level" % KEPT, KEPT_RULE]) and "never run" not in got[1], shown(got))
    p = Project("kept-action-comparison-alone")
    kept_tests(p, comparison=0)
    (p.root / KEPT / "guide-tests.py").unlink()
    got = p.run("--check-kept-tests", "docs/guide.md")
    check("--check-kept-tests fails where a comparison stands beside no set of kept tests of its script",
          reports(got, "== check-kept-tests", "%sguide-comparison.py is the comparison of a script holding no set of kept tests, %sguide-tests.py, so that script's kept tests cannot be run" % (KEPT, KEPT)), shown(got))
    p = Project("kept-action-names-differ")
    kept_tests(p, comparison=0)
    p.put(KEPT + "guide-comparison.py", p.read(KEPT + "guide-comparison.py").replace("FORM_FILES = (\"docs/guide.md\",)", "FORM_FILES = (\"docs/guide.md\", \"docs/notes.md\")"))
    got = p.run("--check-kept-tests", "docs/guide.md")
    check("--check-kept-tests fails where a comparison and its script's kept tests name different files",
          reports(got, "== check-kept-tests", "%sguide-comparison.py and %sguide-tests.py name different files as their script's, so which changes run them cannot be told" % (KEPT, KEPT)), shown(got))


@test("kept", "check-kept-tests given no file reads the files the checkout holds changed")
def _():
    p = Project("kept-action-changed")
    kept_tests(p, verdict=1)
    git(p.root, "init", "-q")
    p.commit()
    p.design(log=DRAFTED)
    got = p.run("--check-kept-tests")
    check("--check-kept-tests given no file runs nothing where the checkout holds only working files changed", passes(got, "== check-kept-tests, over 0 changed files", "0 problems"), shown(got))
    p.put("docs/guide.md", base("guide.md") + "\nThe ferry does not run on the feast day.\n")
    got = p.run("--check-kept-tests")
    check("--check-kept-tests given no file runs the kept tests of the script whose form the checkout holds changed against the last commit, and fails where one fails",
          reports(got, "== check-kept-tests, over 1 changed file", ["run for docs/guide.md", "guide-tests.py holds a test that fails, or could not be run, exit 1"]), shown(got))
    kept_tests(p)
    got = p.run("--check-kept-tests")
    check("and reads a kept file changed with it as a changed file, and passes where the tests pass", passes(got, "== check-kept-tests, over 2 changed files", "0 problems") and "run for docs/guide.md" in got[1], shown(got))


# ---------------------------------------------------------------- the checkout: its last commit, its changes, its place

RETITLED = "## The Ferry and Its Times"


@test("checkout", "an applying design's citations are read at the last commit")
def _():
    for skill in SKILLS:
        p = Project("applying-cited", versioned=True)
        design = p.design(skill=skill, status="applying", log=APPLYING)
        p.put("docs/guide.md", swap(base("guide.md"), "## The Ferry", RETITLED) + "\n## The Harbour\n\nThe harbour was dredged last spring.\n")
        got = p.run("--check-cited-headings", design, skill=skill)
        check("--check-cited-headings of %s reports nothing of an applying design citing a heading its own apply retitled" % skill,
              passes(got, "== check-cited-headings", "1 citation, 0 broken"), shown(got))
        text = swap(a_design("harbour-cited", skill=skill, status="applying", log=APPLYING), "and `docs/guide.md § The Ferry` names", "and `docs/guide.md § The Harbour` names")
        got = p.run("--check-cited-headings", p.design("harbour-cited", skill=skill, text=text), skill=skill)
        check("--check-cited-headings of %s reports an applying design citing a heading the last commit does not hold, one its apply wrote among them" % skill,
              reports(got, "== check-cited-headings", ["BROKEN", "§ The Harbour", "no such heading", "1 broken"]), shown(got))
        (p.root / "docs/guide.md").unlink()
        got = p.run("--check-cited-headings", design, skill=skill)
        check("--check-cited-headings of %s reports nothing of an applying design citing a file its own apply removed" % skill, passes(got, "== check-cited-headings", "1 citation, 0 broken"), shown(got))


@test("checkout", "check-changed-files passes changes within the Target, and reports one outside it")
def _():
    for skill in SKILLS:
        p = Project("changed-files", versioned=True)
        design = p.design(skill=skill, status="applying", log=APPLYING, Target="`docs/guide.md`; `docs/tides/`")
        p.put("docs/guide.md", base("guide.md") + "\nThe first ferry leaves at seven.\n")
        p.put("docs/tides/spring.md", "# Spring Tides\n\nThe spring tide runs high.\n")
        got = p.run("--check-changed-files", design, skill=skill)
        check("--check-changed-files of %s passes where each changed file is one the Target names, one created under a directory it names, or a working file" % skill,
              passes(got, "== check-changed-files " + NAME, "0 problems"), shown(got))
        p.put("docs/notes.md", "# Notes\n\nA note written beside the work.\n")
        got = p.run("--check-changed-files", design, skill=skill)
        check("--check-changed-files of %s reports a file changed outside the Target that no entry of the log names" % skill,
              reports(got, "== check-changed-files " + NAME, ["docs/notes.md\n  changed outside the Target, and no entry of the log names it", "1 problem"]), shown(got))
        design = p.design(skill=skill, status="applying", log=APPLYING + (("user-edit", {"Places": "`docs/notes.md`"}),), Target="`docs/guide.md`; `docs/tides/`")
        got = p.run("--check-changed-files", design, skill=skill)
        check("--check-changed-files of %s marks a file changed outside the Target that a user-edit entry names, and reports nothing" % skill,
              passes(got, "== check-changed-files " + NAME, "0 problems") and "docs/notes.md\n  changed outside the Target, the user's edit" in got[1], shown(got))


@test("checkout", "check-audits passes a design whose audits ran or were bypassed, and reports one owing an audit")
def _():
    for skill in SKILLS:
        p = Project("audits")
        got = p.run("--check-audits", p.design(skill=skill, status="applying", log=APPLYING), skill=skill)
        check("--check-audits of %s reports a design that changed a file of a sub-scope and whose log records neither the specs audit's run nor its bypass since its apply" % skill,
              reports(got, "== check-audits " + NAME, "neither run nor bypassed since the last apply entry: the specs audit, .ai/skills/audit-specs/"), shown(got))
        got = p.run("--check-audits", p.design(skill=skill, status="applying", log=APPLYING + (("audit-bypass", {"Audit": "specs"}),)), skill=skill)
        check("--check-audits of %s passes a design whose log records the user's bypass of the audit" % skill, passes(got, "== check-audits " + NAME, "0 problems"), shown(got))
        got = p.run("--check-audits", p.design(skill=skill, status="applying", log=APPLYING + (("audit-specs", {"Design Version": "1.0.1"}),)), skill=skill)
        check("--check-audits of %s passes a design whose log records the audit's run" % skill, passes(got, "== check-audits " + NAME, "0 problems"), shown(got))
        got = p.run("--check-audits", p.design(skill=skill, status="applying", log=APPLYING + (("audit-bypass", {"Audit": "specs"}), ("entered", {"Reason": "sent back"}), ("plan-approval", {"Approval": "approved"}), ("apply", {}))), skill=skill)
        check("--check-audits of %s reports a design whose audit was bypassed before its last apply entry alone" % skill, reports(got, "== check-audits " + NAME, "neither run nor bypassed since the last apply entry"), shown(got))


@test("checkout", "show-refactor-and-refine-of-existing-specs shows what changed since a baseline")
def _():
    p = Project("refactor-and-refine", canon=False)
    home = p.put("specs/birds.md", "# Birds\n\n## The Heron\n\nThe heron stands in the reeds at dusk and waits.\n\n## The Egret\n\nThe egret wades the shallows at first light alone.\n")
    git(p.root, "init", "-q")
    p.commit()
    p.put(home, swap(p.read(home), "The egret wades the shallows at first light alone.\n", "The heron stands in the reeds at dusk and waits.\n\nA crane flies over.\n"))
    got = p.run("--show-refactor-and-refine-of-existing-specs", "HEAD")
    check("--show-refactor-and-refine-of-existing-specs lists each line now repeated, lost and new since the baseline, with the file holding it",
          passes(got, "== show-refactor-and-refine-of-existing-specs since HEAD", "1 repeated, 1 lost, 1 new")
          and "repeated   The heron stands in the reeds at dusk and waits.\n           in " + home in got[1]
          and "lost       The egret wades the shallows at first light alone.\n" in got[1] and "new        A crane flies over.\n" in got[1], shown(got))


@test("checkout", "show-refactor-and-refine-of-existing-specs refuses a baseline that is no commit")
def _():
    p = Project("refactor-and-refine-refused", versioned=True)
    got = p.run("--show-refactor-and-refine-of-existing-specs", "no-such-commit")
    check("--show-refactor-and-refine-of-existing-specs refuses a baseline that is no commit, exit 2", got[0] == 2 and "no such commit: no-such-commit" in got[1], shown(got))
    p = Project("refactor-and-refine-no-git")
    got = p.run("--show-refactor-and-refine-of-existing-specs", "HEAD")
    check("--show-refactor-and-refine-of-existing-specs refuses a project under no version control, exit 2", got[0] == 2 and "run it from the repository's root" in got[1], shown(got))


@test("checkout", "refresh-links writes the link of each citation in a file a person reads")
def _():
    p = Project("links", canon=False)
    p.put("docs/notes.md", "# Notes\n\nThe ferry's quay is named in `docs/guide.md § The Ferry`.\n")
    got = p.run("--refresh-links", p.root)
    check("--refresh-links writes the link a citation lacks, and says how many files it changed",
          passes(got, "== refresh-links", "1 files changed") and "[`docs/guide.md § The Ferry`](/docs/guide.md#the-ferry)" in p.read("docs/notes.md"), shown(got) + p.read("docs/notes.md"))


@test("checkout", "refresh-links leaves a file whose links are current")
def _():
    p = Project("links-current", canon=False)
    p.put("docs/notes.md", "# Notes\n\nThe ferry's quay is named in [`docs/guide.md § The Ferry`](/docs/guide.md#the-ferry).\n")
    before = p.held("docs")
    got = p.run("--refresh-links", p.root)
    check("--refresh-links changes no file whose every citation carries its link", passes(got, "== refresh-links", "0 files changed") and p.held("docs") == before, shown(got))


@test("checkout", "check-constructs passes a file whose constructs hold their forms")
def _():
    p = Project("constructs")
    path = p.put("docs/guide.md", swap(base("guide.md"), "The ferry leaves from the north quay.\n", "The ferry leaves from the north quay.\n" + TABLE))
    got = p.run("--check-constructs", path)
    check("--check-constructs passes a file in scope whose Decision Table holds its form", passes(got, "== check-constructs docs/guide.md", "0 findings"), shown(got))


@test("checkout", "check-constructs reports a construct out of its form")
def _():
    p = Project("constructs-reports")
    path = p.put("docs/guide.md", swap(base("guide.md"), "The ferry leaves from the north quay.\n", "The ferry leaves from the north quay.\n" + swap(TABLE, "**Hit Policy:** First", "**Hit Policy:** Whenever")))
    got = p.run("--check-constructs", path)
    check("--check-constructs reports a Decision Table whose Hit Policy is none the construct gives", reports(got, "== check-constructs docs/guide.md", ["docs/guide.md:", "Hit Policy", "1 finding"]), shown(got))
    got = p.run("--check-constructs", p.design(log=DRAFTED))
    check("--check-constructs refuses a design document, whose Drafts the validation review checks, exit 2", got[0] == 2 and "no file in scope; a design's Drafts are checked by --check-design" in got[1], shown(got))


@test("checkout", "a shorthand citation resolves in a checkout kept beneath another's working files")
def _():
    for under in (None, ".ai/tmp/worktrees/elsewhere"):
        p = Project("place", under=under)
        p.put(".ai/tmp/design-specs/scratch/guide.md", "# A Draft of the Guide\n\n## The Ferry\n\nA draft kept among the skills' own output.\n")
        design = p.design(text=swap(a_design(log=DRAFTED), "and `docs/guide.md § The Ferry` names", "and `guide.md § The Ferry` names"))
        got = p.run("--check-cited-headings", design)
        check("--check-cited-headings resolves a file named in shorthand in a checkout %s, a file of the same name among the skills' own output aside"
              % ("standing under `%s` of another folder" % under if under else "standing anywhere"),
              passes(got, "== check-cited-headings", "2 citations, 0 broken") and "ok        guide.md" in got[1], shown(got))
        form = p.run("--check-design-form", design)
        names = p.run("--check-design-names", design)
        check("and the design's form and its names read the same there", passes(form, "== check-design-form", "0 problems") and passes(names, "== check-design-names", "0 problems"), shown(form) + shown(names))


@test("checkout", "a form is read from the checkout the script is run in")
def _():
    kinds = "| `apply` | none | none | as applying begins |\n"
    p = Project("form-run-in")
    home = "specs/methodology/working-files/main.md"
    p.put(home, swap(p.read(home), kinds, kinds + "| `ferry-sailed` | none | none | as the ferry sails |\n"))
    design = p.design(log=DRAFTED)
    got = p.run("--log-entry", design, "ferry-sailed")
    check("--log-entry appends an entry of a kind the canon of the checkout it is run in declares, whichever checkout holds the script's own file",
          passes(got, "== log-entry", "- **Entry:** ferry-sailed-1"), shown(got))
    form = p.run("--check-design-form", design)
    check("and --check-design-form reads the log it wrote by the same canon", passes(form, "== check-design-form", "0 problems"), shown(form))
    p = Project("form-as-it-stands")
    got = p.run("--log-entry", p.design(log=DRAFTED), "ferry-sailed")
    check("--log-entry refuses the same kind in a checkout whose canon declares none such", reports(got, "== log-entry, not logged", "a log entry's kind is not one of"), shown(got))


# ---------------------------------------------------------------- no design written but the one acted on

@test("writes", "no writing action writes a design other than the one it is run on")
def _():
    for skill in SKILLS:
        p = a_workstack("writes")
        own = (lambda n: n) if skill == "design-specs" else (lambda n: "design-specs/" + n)
        named = NAME if skill == "design-specs" else "implement-specs/" + NAME
        p.design("waits-on-it", log=AGREED, depends=named)
        p.design("approved-on-it", status="approved", log=APPROVED, depends=named)
        p.design("code-waits-on-it", skill="implement-specs", log=AGREED, depends=NAME if skill == "implement-specs" else "design-specs/" + NAME)
        p.design("kept-naming-it", folder=".ai/plans/%s/archive" % skill, status="applying", log=APPLYING, depends=NAME)
        p.design(NAME, folder=".ai/plans/%s/archive" % skill, log=DRAFTED, depends=own(COMPLETE))
        design = researched(p, skill=skill, text=swap(a_design(skill=skill, status="applying", log=APPLYING_RESEARCHED, depends=own(COMPLETE)), "without saying when it runs.", "without saying when it runs at all."))
        others = lambda: {k: v for k, v in p.held().items() if k != design}
        before = others()
        check("the workstack made for the test holds designs naming the one acted on, in its plans folder, in the folder beside it and in an archive, and a design of its name in the archive",
              len(before) == 9 and sum(NAME.encode() in v for v in before.values()) >= 5, sorted(before))
        for label, args in (("--stamp-validation", ("--stamp-validation", design)), ("--free-design", ("--free-design", design)), ("--log-entry", ("--log-entry", design, "goals-agreed")),
                            ("--log-entry of a second entry", ("--log-entry", design, "user-edit", "Places=docs/guide.md"))):
            was = p.read(design)
            got = p.run(*args, skill=skill)
            check("%s of %s writes the design it is run on, and leaves every other design byte for byte as it was, an archived one among them" % (label, skill),
                  got[0] == 0 and p.read(design) != was and others() == before, shown(got))
        path = p.put(report_at(REVIEW, skill=skill), cold_part(a_report("review", skill=skill, version="2.0.0")))
        was = p.read(design)
        got = p.run("--take-up-report", path, skill=skill)
        check("--take-up-report of %s writes the report alone, and no design" % skill, got[0] == 0 and "## Hand-back" in p.read(path) and p.read(design) == was and others() == before, shown(got))
        got = p.run("--refresh-links", p.root, skill=skill)
        check("--refresh-links of %s writes no design" % skill, got[0] == 0 and p.read(design) == was and others() == before, shown(got))


@test("writes", "a design finishing leaves each design naming it as it was, and each is read from the files")
def _():
    p = a_workstack("finishing")
    waits = p.design("waits-on-it", log=AGREED, depends=NAME)
    p.design("kept-naming-it", folder=".ai/plans/design-specs/archive", log=AGREED, depends=NAME)
    design = p.design(status="applying", log=APPLYING)
    others = lambda: {k: v for k, v in p.held().items() if k != design}
    before = others()
    blocked = p.run("--check-design-names", waits)
    # the design finishes: its builder appends its last entries and moves its Status to complete
    bypass = p.run("--log-entry", design, "audit-bypass", "Audit=specs")
    p.put(design, swap(p.read(design), "**Status:** applying", "**Status:** complete"))
    for flag, args in (("--check-design-form", (design,)), ("--check-workstack", ()), ("--show-workstack", ()), ("--check-design-names", (design,)), ("--free-design", (design,)), ("--show-design", (design,))):
        p.run(flag, *args)
    check("a design finishing writes nothing in the designs naming it: each stands byte for byte as it was, one in the archive among them", bypass[0] == 0 and others() == before, shown(bypass))
    got = p.run("--check-design-names", waits)
    check("and a design naming it, blocked by it until then, is read from the files as naming a finished design, to be freed as it is next worked",
          passes(blocked, "== check-design-names", "blocked by %s, unfinished" % NAME) and reports(got, "== check-design-names waits-on-it", "names %s, finished" % NAME), shown(got))
    (p.root / design).unlink()
    got = p.run("--check-design-names", waits)
    check("and, the finished design deleted, as naming a design that is gone", reports(got, "== check-design-names waits-on-it", "names %s, gone" % NAME) and others() == before, shown(got))


@test("writes", "no reading action writes a file")
def _():
    p = a_workstack("reads")
    design = researched(p, status="approved", log=APPROVED_RESEARCHED, depends=UNFINISHED)
    path = p.put(report_at(REVIEW), cold_part(a_report("review")))
    before = p.held(".")
    for args in (("--check-cited-headings", design), ("--check-design-form", design), ("--check-target-kind", design), ("--check-design", design), ("--check-workstack",), ("--show-workstack",),
                 ("--show-design", design), ("--check-design-names", design), ("--show-dependents", design, GOAL), ("--show-validation", design), ("--check-handed-back", path),
                 ("--check-audits", design), ("--check-changed-files", design), ("--check-constructs", "docs/guide.md")):
        p.run(*args)
    check("each action that checks or shows writes no file: the project stands byte for byte as it was after each", p.held(".") == before,
          sorted(k for k in set(before) | set(p.held(".")) if before.get(k) != p.held(".").get(k)))


# ---------------------------------------------------------------- the kept comparison

COMPARISON = "tests/spec-of-record/scripts/design-script-comparison.py"
SCRIPT = ".ai/skills/lib/design_documents.py"
MAIN = "specs/methodology/working-files/main.md"


def a_script_project(name):
    """-> a project holding the design script itself, a copy of the skills and the canon of the checkout the tests are
    run in, with the kept comparison, committed: a checkout the comparison reads the last commit's script from."""
    p = Project(name)
    shutil.copytree(PROJECT / ".ai" / "skills", p.root / ".ai" / "skills", ignore=shutil.ignore_patterns("__pycache__"))
    p.put(COMPARISON, (PROJECT / COMPARISON).read_text(encoding="utf-8"))
    git(p.root, "init", "-q")
    p.commit()
    return p


def compared(p, *args):
    ran = subprocess.run([sys.executable, str(p.root / COMPARISON)] + list(args), cwd=p.root, capture_output=True,
                         env=dict(os.environ, PYTHONIOENCODING="utf-8", PYTHONDONTWRITEBYTECODE="1"))
    return ran.returncode, (ran.stdout + ran.stderr).decode("utf-8", "replace").replace("\r\n", "\n")


def listed(got):
    return re.findall(r"^design (\S+)$", got[1], re.M)


def three_designs(p):
    p.design("first-design", log=DRAFTED)
    p.design("second-design", status="approved", log=APPROVED)
    p.design("odd-name", text=swap(a_design("odd-name", log=DRAFTED), "**Name:** odd-name", "**Name:** Odd Name"))
    return ".ai/plans/design-specs"


@test("comparison", "the comparison lists exactly the design a change to the script reads differently")
def _():
    p = a_script_project("compared")
    plans = three_designs(p)
    got = compared(p, plans)
    check("the comparison lists no design where the script stands as the last commit held it", got[0] == 0 and listed(got) == [] and "0 designs read differently, of 3" in got[1], shown(got))
    p.put(SCRIPT, swap(p.read(SCRIPT), "\"Name is not a slug: \"", "\"Name is no slug: \""))
    got = compared(p, plans)
    check("after a change to the message of one check, it lists the one design that check reports, with each action reading it differently, and no other",
          got[0] == 0 and listed(got) == [plans + "/odd-name.md"] and "1 design read differently, of 3" in got[1]
          and "--check-design-form: exit 1 at both, its output differing" in got[1] and "- Name is not a slug: Odd Name" in got[1] and "+ Name is no slug: Odd Name" in got[1], shown(got))
    check("and it leaves no worktree behind, and the checkout's own files as they were",
          not (p.root / ".ai/tmp/worktrees/design-script-comparison-then").exists() and not (p.root / ".ai/tmp/worktrees/design-script-comparison-now").exists()
          and git(p.root, "worktree", "list").count("\n") == 0 and git(p.root, "status", "--porcelain", "--", ".ai/skills", "specs") == "M " + SCRIPT, git(p.root, "status", "--porcelain"))


@test("comparison", "a form changed together with the code reading it lists no design the change leaves read alike")
def _():
    p = a_script_project("compared-form")
    plans = three_designs(p)
    form = swap(p.read(MAIN), "**Plural Name:** Design Goals", "**Plural Name:** Goals of a Design")
    p.put(MAIN, form)
    got = compared(p, plans)
    check("after a change to a form alone, the script as it stands reading it, the comparison lists each design the form's change reads differently: every one",
          got[0] == 0 and sorted(listed(got)) == sorted(plans + "/%s.md" % n for n in ("first-design", "second-design", "odd-name")) and "declares no Plural Name Design Goals" in got[1], shown(got))
    p.put(SCRIPT, swap(p.read(SCRIPT), "declared_type(GOAL_HOME, \"Design Goals\", root)", "declared_type(GOAL_HOME, \"Goals of a Design\", root)"))
    got = compared(p, plans)
    check("after the same change made together with the code reading it, each side reading the canon of its own tree, it lists no design",
          got[0] == 0 and listed(got) == [] and "0 designs read differently, of 3" in got[1], shown(got))


@test("comparison", "the comparison cannot be made of what is no plans folder, or under no version control")
def _():
    p = a_script_project("compared-refused")
    got = compared(p, "docs")
    check("the comparison refuses a folder that is no plans folder, exit 2", got[0] == 2 and "design-script-comparison takes plans folders" in got[1], shown(got))
    p = Project("compared-no-git")
    shutil.copytree(PROJECT / ".ai" / "skills", p.root / ".ai" / "skills", ignore=shutil.ignore_patterns("__pycache__"))
    p.put(COMPARISON, (PROJECT / COMPARISON).read_text(encoding="utf-8"))
    got = compared(p, three_designs(p))
    check("the comparison says it cannot be made where the project is under no version control, exit 2", got[0] == 2 and "cannot be made" in got[1], shown(got))


@test("comparison", "check-kept-tests runs the design script's own comparison over the checkout's plans folders")
def _():
    p = a_script_project("compared-by-the-script")
    three_designs(p)
    p.put(KEPT + "design-script-tests.py", "SCRIPT_FILES = %r\nFORM_FILES = %r\nprint('  pass  a stand-in for the design script\\'s kept tests')\n" % (SCRIPT_FILES, FORM_FILES))
    p.put(SCRIPT, swap(p.read(SCRIPT), "\"Name is not a slug: \"", "\"Name is no slug: \""))
    got = p.run("--check-kept-tests", SCRIPT)
    check("--check-kept-tests, given the design script's code, runs its kept tests and its kept comparison, which lists the one design read differently, and passes whatever it lists",
          passes(got, "== check-kept-tests, over 1 changed file", "0 problems") and "$ python %s\nrun for %s\n" % (COMPARISON, SCRIPT) in got[1]
          and "\ndesign .ai/plans/design-specs/odd-name.md\n" in got[1] and "1 design read differently, of 3" in got[1] and "a stand-in for the design script's kept tests\nexit 0" in got[1], shown(got))
    got = p.run("--check-kept-tests", MAIN)
    check("--check-kept-tests, given a file of the canon the design script reads a form from, runs them too: a change to a form alone",
          passes(got, "== check-kept-tests, over 1 changed file", "0 problems") and "$ python %s\nrun for %s\n" % (COMPARISON, MAIN) in got[1], shown(got))


# ---------------------------------------------------------------- the checks a real search answers

SEARCH_INDEX = ".ai/tmp/search-spec-of-record-scope"
NOTES = "# Notes\n\nA walker's notes: the north quay is slippery after rain.\n"
RETIRED = "\n## Retired Phrases\n\n**Records:**\n  - **Phrase:** %s \\\n    **Replacement:** north pier \\\n    **Stays Right:** none\n"
_SEARCHED = []
SEARCHED_LOCK = threading.Lock()


def a_searched_project(name, versioned=False):
    """-> a project the search has read: a copy of one base project, made once in a run, holding the canon, the guide
    and a walker's notes, with the index the search built of them, so each test's own search reads only what the test
    changes. versioned puts it under version control, its files committed and the search's index left out."""
    with SEARCHED_LOCK:
        if not _SEARCHED:
            made = Project("searched-base")
            made.put("docs/notes.md", NOTES)
            built = subprocess.run([sys.executable, "-c", "import sys\nsys.dont_write_bytecode = True\nsys.path.insert(0, sys.argv[1])\nimport search\n"
                                    "search.Search(sys.argv[2], quiet=True).db.close()\n", str(TREE / LIB), str(made.root)], capture_output=True, text=True)
            if built.returncode:
                raise AssertionError("the search could not read the project made for the tests: " + built.stderr[-800:])
            _SEARCHED.append(made)
    p = Project.__new__(Project)
    p.root, p.versioned = outside(name) / "checkout", versioned
    shutil.copytree(_SEARCHED[0].root, p.root)
    if versioned:
        git(p.root, "init", "-q")
        (p.root / ".git" / "info" / "exclude").write_text(SEARCH_INDEX + "/\n", encoding="utf-8")
        p.commit()
    return p


def retiring(text, phrase="north quay"):
    """-> a design's text retiring a phrase, its Retired Phrases where the form puts the section."""
    after = "\n## Design Log Entries" if "\n## Design Log Entries" in text else "\n## Out of Scope"
    return swap(text, after, RETIRED % phrase + after)


@test("searched", "show-reach lists each line of a durable file holding a retired phrase")
def _():
    for skill in SKILLS:
        p = a_searched_project("reach")
        got = p.run("--show-reach", p.design(skill=skill, text=retiring(a_design(skill=skill, log=DRAFTED))), skill=skill)
        inside = "" if skill == "design-specs" else "  (outside the Target)"
        check("--show-reach of %s lists each line of a durable file holding the phrase a design retires, marking those outside its Target" % skill,
              passes(got, "== show-reach " + NAME, "2 lines") and "docs/guide.md:7%s  [north quay]  The ferry leaves from the north quay." % inside in got[1]
              and "docs/notes.md:3  (outside the Target)  [north quay]  A walker's notes: the north quay is slippery after rain." in got[1], shown(got))


@test("searched", "show-reach lists no line where no durable file holds the phrase")
def _():
    p = a_searched_project("reach-none")
    got = p.run("--show-reach", p.design(text=retiring(a_design(log=DRAFTED), "south quay")))
    check("--show-reach lists no line for a phrase no durable file holds, the design document's own aside", passes(got, "== show-reach " + NAME, "\n0 lines") and "[south quay]" not in got[1], shown(got))
    got = p.run("--show-reach", ".ai/plans/design-specs/no-such-design.md")
    check("--show-reach of a file that is not there says so, exit 2", got[0] == 2 and "no design document" in got[1], shown(got))


@test("searched", "check-retired-wording passes a Target holding no retired phrase")
def _():
    for skill in SKILLS:
        p = a_searched_project("retired-pass")
        design = p.design(skill=skill, text=retiring(a_design(skill=skill, status="applying", log=APPLYING, Target="`docs/guide.md`")))
        p.put("docs/guide.md", swap(base("guide.md"), "north quay", "north pier"))
        got = p.run("--check-retired-wording", design, skill=skill)
        check("--check-retired-wording of %s passes where no file of the Target holds the retired phrase, a file outside it holding the phrase still" % skill,
              passes(got, "== check-retired-wording " + NAME, "0 problems"), shown(got))


@test("searched", "check-retired-wording reports a line of the Target holding a retired phrase")
def _():
    for skill in SKILLS:
        p = a_searched_project("retired-reports")
        design = p.design(skill=skill, text=retiring(a_design(skill=skill, status="applying", log=APPLYING, Target="`docs/guide.md`")))
        got = p.run("--check-retired-wording", design, skill=skill)
        check("--check-retired-wording of %s reports each line of the Target holding the retired phrase, with its replacement, and no line of a file outside it" % skill,
              reports(got, "== check-retired-wording " + NAME, ["docs/guide.md\n  line 7 holds north quay, retired for north pier: The ferry leaves from the north quay.", "1 problem"]), shown(got))


@test("searched", "check-work passes work adding no finding")
def _():
    for skill in SKILLS:
        p = a_searched_project("work-pass", versioned=True)
        design = p.design(skill=skill, status="applying", log=APPLYING)
        p.put("docs/guide.md", swap(base("guide.md"), "north quay.", "north quay, at seven and at five."))
        got = p.run("--check-work", design, skill=skill)
        check("--check-work of %s passes work whose change adds no finding to those the scope held at the last commit" % skill,
              passes(got, "== check-work " + NAME, "0 findings new against the last commit, over 1 changed file"), shown(got))


@test("searched", "check-work reports a finding the work added")
def _():
    for skill in SKILLS:
        p = a_searched_project("work-reports", versioned=True)
        design = p.design(skill=skill, status="applying", log=APPLYING)
        p.put("docs/guide.md", swap(base("guide.md"), "north quay.", "north quay, as `docs/guide.md § The Harbour Master` has it."))
        got = p.run("--check-work", design, skill=skill)
        check("--check-work of %s reports a finding the scope holds now and did not hold at the last commit: a citation of a heading that does not stand" % skill,
              reports(got, "== check-work " + NAME, ["docs/guide.md:7", "The Harbour Master", "1 finding new against the last commit, over 1 changed file"]), shown(got))


def searching_review(places=FERRY + "\n      - `docs/notes.md`"):
    """-> a review's report whose reviewer recorded a Search by terms, giving every place, with the places given."""
    text = a_report("review")
    text = swap(text, "    **Kind:** meaning \\\n    **Query:** In winter the ferry makes fewer crossings than in summer. \\\n    **Ranking Part:** 1 to 20 \\\n", "    **Kind:** terms \\\n    **Query:** north quay \\\n")
    return swap(text, "    **Snapshot:** 0123456789abcdef \\\n    **Places:**\n      - " + FERRY, "    **Snapshot:** 0123456789abcdef \\\n    **Places:**\n      - " + places)


SEARCH_GIVES = "Search reviewer-1-winter-hours gives %s, which its Places do not cover"


@test("searched", "a reviewer's Search is run as its report is handed back and taken up")
def _():
    for skill in SKILLS:
        p = a_searched_project("reviewers-search")
        p.design(skill=skill, log=DRAFTED)
        path = p.put(report_at(REVIEW, skill=skill), cold_part(searching_review()).replace(".ai/plans/design-specs/", ".ai/plans/%s/" % skill))
        got = p.run("--check-handed-back", path, skill=skill)
        check("--check-handed-back of %s passes a review's report whose Search by terms holds each place the search gives" % skill, passes(got, "== check-handed-back " + path, "0 problems"), shown(got))
        got = p.run("--take-up-report", path, skill=skill)
        check("--take-up-report of %s takes it up" % skill, passes(got, "== take-up-report " + path, "0 problems") and "## Hand-back" in p.read(path), shown(got))
        path = p.put(report_at(REVIEW, skill=skill), cold_part(searching_review("none")).replace(".ai/plans/design-specs/", ".ai/plans/%s/" % skill))
        for flag, heading in (("--check-handed-back", "== check-handed-back"), ("--take-up-report", "== take-up-report, not taken up")):
            got = p.run(flag, path, skill=skill)
            check("%s of %s reports a review's report whose Search by terms gives a place its Places leave out" % (flag, skill), reports(got, heading, SEARCH_GIVES % FERRY), shown(got))


@test("searched", "a taken-up report is not refused, and not sent back, for a fix writing the searched words somewhere new")
def _():
    unsettled = lambda t: swap(t, "    **Settled Findings:**\n      - " + FINDING, "    **Settled Findings:**\n      - reviewer-1-another-finding")
    for skill in SKILLS:
        p = a_searched_project("later-fix")
        design = p.design(skill=skill, log=DRAFTED)
        text = searching_review().replace(".ai/plans/design-specs/", ".ai/plans/%s/" % skill)
        path = taken_up(p, REVIEW, cold_part(text) + "\n" + unsettled(builder_part(text)), skill=skill)
        # the builder's fix writes the searched words in a section the reviewer's Search did not give
        p.put("docs/guide.md", swap(base("guide.md"), "trims the lamp at dusk.", "trims the lamp at dusk, and its beam reaches the north quay."))
        before = p.read(path)
        got = p.run("--check-settled-report", path, skill=skill)
        check("--check-settled-report of %s refuses the report for the fault in the builder's own Settlement alone, runs no Search of the reviewer's again, and leaves the report with the builder" % skill,
              reports(got, "== check-settled-report", "Finding %s is settled by 0 Settlements, not exactly one" % FINDING) and "its Places do not cover" not in got[1]
              and "goes back to its cold agent" not in got[1] and p.read(path) == before, shown(got))
        p.put(path, before.replace("      - reviewer-1-another-finding", "      - " + FINDING))
        got = p.run("--check-settled-report", path, skill=skill)
        check("--check-settled-report of %s passes it once the builder's part is put right, whatever the files have come to hold since the take-up" % skill,
              passes(got, "== check-settled-report " + path, "0 problems"), shown(got))
        got = p.run("--log-entry", design, REVIEW, *ROUND_FIELDS, skill=skill)
        check("and --log-entry of %s appends its entry" % skill, passes(got, "== log-entry", "- **Entry:** adversarial-review-1"), shown(got))
        fresh = p.put(report_at(REVIEW, 2, skill=skill), cold_part(text).replace("adversarial-review-1", "adversarial-review-2"))
        got = p.run("--check-handed-back", fresh, skill=skill)
        check("while the same Search in a report handed back after the fix is held to the files as they then stand, by --check-handed-back of %s" % skill,
              reports(got, "== check-handed-back", SEARCH_GIVES % LIGHTHOUSE), shown(got))


BY_TERMS_SEARCH = "\n\n  - **Search:** ferry-times-by-terms \\\n    **For:** every use of the quay the ferry leaves from \\\n    **Goals:**\n      - %s\n\n    **Kind:** terms \\\n    **Query:** %%s \\\n" \
                  "%%s    **Snapshot:** 0123456789abcdef \\\n    **Places:**\n      - %s\n\n## Read Assessments" % (GOAL, FERRY)


def whole_research(query="north quay", narrowed=""):
    """-> a research report naming its goal in a Search by meaning and in one by terms, which the search runs."""
    return swap(a_report("research"), "\n\n## Read Assessments", BY_TERMS_SEARCH % (query, narrowed))


@test("searched", "research searching each goal by meaning and by terms, each match assessed, passes the validation review")
def _():
    p = a_searched_project("research-whole")
    p.put("docs/notes.md", "# Notes\n\nA walker's notes on the island.\n")
    design = p.design(log=AGREED)
    path = p.put(report_at(JUDGMENT), cold_part(whole_research()))
    back = p.run("--check-handed-back", path)
    path = taken_up(p, JUDGMENT, whole_research())
    logged = p.run("--log-entry", design, JUDGMENT, *CHECK_FIELDS)
    change = p.run("--log-entry", design, "plan-change")
    check("a research report whose Searches the search runs is handed back, taken up and logged", back[0] == 0 and logged[0] == 0 and change[0] == 0, shown(back) + shown(logged))
    got = p.run("--check-design", design)
    check("--check-design passes a design not yet approved whose research names each goal in a Search by meaning and in one by terms of every durable file, each place they give lying in an Area it assesses",
          passes(got, "== check-design " + NAME, "0 problems"), shown(got))
    own = p.put(report_at(SELF), a_report("self-review"))
    got = p.run("--log-entry", design, SELF, *CHECK_FIELDS)
    check("--log-entry appends the first check of the builder's after that research, the research read together as its entry is appended", passes(got, "== log-entry", "- **Entry:** self-review-1"), shown(got))
    got = p.run("--stamp-validation", design)
    shown_ = p.run("--show-validation", design)
    check("--stamp-validation stamps the design, which then reads validated", passes(got, "== stamp-validation\n**Validated:** ") and ": validated;" in shown_[1], shown(got) + shown(shown_))


@test("searched", "research whose Search gives a place no Area covers, or leaves a durable file unsearched, is reported")
def _():
    p = a_searched_project("research-reports")
    design = p.design(log=AGREED + RESEARCH + (("plan-change", {}),))
    path = p.put(report_at(JUDGMENT), whole_research())
    got = p.run("--check-design", design)
    check("--check-design reports a place a research's Search by terms gives, run over the files as they stand, that no Area of the research covers",
          reports(got, "== check-design " + NAME, ["Search ferry-times-by-terms of %s gives `docs/notes.md`, which no binding research report's Read Assessment's Area covers" % path, RULE % "research-covers-its-matches"])
          and "is named by no Search" not in got[1], shown(got))
    p.put("docs/notes.md", "# Notes\n\nA walker's notes on the island.\n")
    p.put(path, whole_research(narrowed="    **Narrowed To:**\n      - `docs/guide.md`\n\n"))
    got = p.run("--check-design", design)
    check("--check-design reports a goal whose Searches by terms were narrowed to paths leaving a durable file out",
          reports(got, "== check-design " + NAME, ["the Searches by terms naming the goal %s were narrowed to paths that together leave out" % GOAL, RULE % "goals-searched-over-every-durable-file"]), shown(got))
    p.design(log=AGREED)
    path = p.put(report_at(JUDGMENT), cold_part(whole_research(query="...")))
    got = p.run("--check-handed-back", path)
    check("--check-handed-back reports a research report whose Search by terms reduces to no word", reports(got, "== check-handed-back", "Search ferry-times-by-terms asks nothing: its term or passage reduces to no word"), shown(got))


@test("searched", "a self-review over applied work under version control runs its checks and the kept tests of a changed form")
def _():
    for verdict in (0, 1):
        p = a_searched_project("applied-versioned", versioned=True)
        kept_tests(p, verdict=verdict)
        p.commit()
        design, path = applied(p)
        p.put("docs/guide.md", swap(base("guide.md"), "north quay.", "north quay, at seven and at five."))
        got = p.run("--log-entry", design, SELF, *CHECK_FIELDS)
        now = p.read(path)
        ran = "$ --check-work %s\n== check-work %s\n\n0 findings new against the last commit, over 1 changed file" % (design, NAME) in now \
            and "$ --check-kept-tests\n$ python %sguide-tests.py\nrun for docs/guide.md\n" % KEPT in now
        if verdict:
            check("--log-entry refuses the entry of a self-review over an apply that changed a form alone, read from the checkout's changes, where a kept test of the script reading it fails",
                  reports(got, "== log-entry, not logged", ["guide-tests.py holds a test that fails, or could not be run, exit 1", KEPT_RULE]) and ran, shown(got) + now[-900:])
        else:
            check("--log-entry appends it where they pass, the output of the checks over the work and of the kept tests in its report", passes(got, "== log-entry", "- **Entry:** self-review-1") and ran, shown(got) + now[-900:])


@test("searched", "a tactical fix covers each place its Search of the design document found")
def _():
    design_path = ".ai/plans/design-specs/%s.md" % NAME
    found = "`%s § Design Plan Steps [Name: %s]`" % (design_path, OBJECTIVE)
    step = "`%s § Design Plan Steps [Name: %s]`" % (design_path, STEP)
    search = "\n\n  - **Search:** first-crossing-named \\\n    **For:** every place of the design naming the first crossing \\\n    **Goals:**\n      - %s\n\n    **Kind:** terms \\\n" \
             "    **Query:** first crossing \\\n    **Target:** working-files \\\n    **Narrowed To:**\n      - `%s`\n\n    **Snapshot:** 0123456789abcdef \\\n    **Places:**\n      - %%s\n" % (GOAL, design_path)

    def settled(places=found, changed=found):
        p = a_searched_project("tactical-fix")
        design = p.design(log=DRAFTED)
        text = a_report("review")
        own = swap(builder_part(text), "      - **Kind:** revision \\\n        **Decision Rewritten:** The Objective gives the first and the last crossing of each season. \\",
                   "      - **Kind:** tactical fix \\\n        **Search:** first-crossing-named \\\n        **Reason:** The Objective's meaning stands, and only its wording names one season. \\")
        path = taken_up(p, REVIEW, cold_part(text) + "\n" + swap(own, "          - **Place:** " + step, "          - **Place:** " + changed))
        p.put(path, swap(p.read(path), "\n\n## Hand-back", search % places + "\n## Hand-back"))
        return p, design, path

    p, design, path = settled()
    got = p.run("--check-settled-report", path)
    check("--check-settled-report passes a round whose tactical fix names a Search by terms of the design document, run as the report is checked, and changes each place it found",
          passes(got, "== check-settled-report " + path, "0 problems"), shown(got))
    got = p.run("--log-entry", design, REVIEW, *ROUND_FIELDS)
    check("and --log-entry appends its entry", passes(got, "== log-entry", "- **Entry:** adversarial-review-1"), shown(got))
    p, design, path = settled(changed=step)
    got = p.run("--check-settled-report", path)
    check("--check-settled-report reports a tactical fix whose Places leave out a place its Search found", reports(got, "== check-settled-report", "Cause %s's tactical fix leaves out %s, a place its Search found" % (CAUSE, found)), shown(got))
    p, design, path = settled(places="none")
    got = p.run("--check-settled-report", path)
    check("--check-settled-report reports a Search of the builder's own, run as the settled report is checked, giving a place its Places leave out",
          reports(got, "== check-settled-report", "Search first-crossing-named gives %s, which its Places do not cover" % found), shown(got))


# ---------------------------------------------------------------- the faults put back

# Each fault the design script was once found with: what it was, the edits putting it back into a copy of the script,
# each (the text standing at its anchor, the text put there), and the tests that then fail.
FAULTS = (
    ("the old Depends On field read silently as a design's Depends On Designs",
     [('        fields = [(f["key"], " ".join(str(record_types.value_of(f)).split())) for f in block]\n    return f.stem, fields',
       '        fields = [(DEPENDS_ON if f["key"] == "Depends On" else f["key"], " ".join(str(record_types.value_of(f)).split())) for f in block]\n    return f.stem, fields')],
     ["the old Depends On field is reported, and read by nothing"]),
    ("a name of a design standing in no plans folder given a second meaning, a problem of the workstack",
     [('    problems = []\n    for n in designs:\n        problems += [(n, "its header " + fault) for fault in out_of_form[n]]\n',
       '    problems = []\n    for n in designs:\n        problems += [(n, "its header " + fault) for fault in out_of_form[n]]\n'
       '        problems += [(n, "its Depends On Designs names %s, which is no design" % d) for d, r in readings[n] if r == GONE_NAME]\n')],
     ["check-workstack reads each name from the plans folders"]),
    ("a freeing writing designs other than the one acted on, an archived one among them",
     [('    write_design(design, raw, text)\n    print("reassessed, its goals to agree again:\\n"',
       '    write_design(design, raw, text)\n    for other in design.parent.rglob("*.md"):\n        if other.resolve() != design.resolve():\n'
       '            other.write_bytes(other.read_bytes() + b"\\n")\n    print("reassessed, its goals to agree again:\\n"')],
     ["free-design frees a design of each finished or gone name, and reassesses one whose goals are agreed",
      "no writing action writes a design other than the one it is run on"]),
    ("a reviewer's Search, and each other check of a cold part, run again after the take-up",
     [('    taken_up = ctx["taken_up"] = cold_lines(rep, kind)\n', '    taken_up = ctx["taken_up"] = frozenset()\n')],
     ["a taken-up Finding stands though the builder removes the goal it names",
      "a taken-up report is not refused, and not sent back, for a fix writing the searched words somewhere new"]),
    ("a taken-up report returned to its cold agent for anything a check of the hand-back reports",
     [('    refused = unmatched_cold_parts(part_texts(text))\n    if not refused:\n        return []\n    path.write_text(cleared_report(text, kind), encoding="utf-8")',
       '    refused = unmatched_cold_parts(part_texts(text)) or handed_back_problems(root, design, kind, n, path)\n    if not refused:\n        return []\n'
       '    path.write_text(cleared_report(text, kind), encoding="utf-8")')],
     ["a taken-up report refused for a fault in the builder's parts stays with the builder"]),
    ("an applying design's citations read against the files as its apply left them",
     [('        applying = is_applying(text)\n        kept = tuple(', '        applying = False\n        kept = tuple(')],
     ["an applying design's citations are read at the last commit"]),
    ("the research of a design approved or applying read against the files",
     [('    if not approved:\n        entries = log_entries(text)\n        read_ = research_indexes(', '    if True:\n        entries = log_entries(text)\n        read_ = research_indexes(')],
     ["an approved or applying design's research is not read against the files"]),
    ("a path judged by the place of its checkout, so no shorthand citation resolves in one kept under .ai/tmp/",
     [('and not p.relative_to(root).as_posix().startswith(".ai/tmp/")', 'and ".ai/tmp" not in p.as_posix()')],
     ["a shorthand citation resolves in a checkout kept beneath another's working files"]),
    ("a form read from the checkout holding the script's file",
     [('    base = Path(root) if root else next((p for p in (Path.cwd(), *Path.cwd().parents) if (p / path).exists()), Path.cwd())\n',
       '    base = Path(root) if root else Path(__file__).resolve().parents[3]\n')],
     ["a form is read from the checkout the script is run in"]),
    ("the entry of a check cut short by a freeing refused, held to the goals of the major version the freeing started",
     [('        if not agreed_before(so_far + [(kind, count, {})], len(so_far), report_version(load_report(design, kind, count))):',
       '        if not agreed_before(so_far + [(kind, count, {})], len(so_far), None):')],
     ["a check cut short by a freeing has its entry appended"]),
    ("a loop in the check of a report's form reusing the name that holds the report's parts, so each review settled with Causes is refused",
     [('                asked, at = miss.get("Kind") == "question not asked", where + "\'s Miss " + miss.get("Miss", "")\n                for k in ("Place", "Reads"):\n'
       '                    require(cond, at, miss, k, not asked, "where its Kind is not question not asked")\n                for k in ("Question", "Answer"):\n'
       '                    require(cond, at, miss, k, asked, "where its Kind is question not asked")\n',
       '                asked, held = miss.get("Kind") == "question not asked", where + "\'s Miss " + miss.get("Miss", "")\n                for k in ("Place", "Reads"):\n'
       '                    require(cond, held, miss, k, not asked, "where its Kind is not question not asked")\n                for k in ("Question", "Answer"):\n'
       '                    require(cond, held, miss, k, asked, "where its Kind is question not asked")\n')],
     ["check-settled-report passes a round settled in its form, and its entry takes its counts from the report"]),
)
SEARCHING = "a taken-up report is not refused, and not sent back, for a fix writing the searched words somewhere new"
# for each of those tests, words of the check of it that fails with the fault put back, so a test failing in some other
# check, for some other reason, proves nothing of the fault
SYMPTOM = {
    "the old Depends On field is reported, and read by nothing": "reports a design holding the old Depends On field, naming the field",
    "check-workstack reads each name from the plans folders": "--check-workstack reports nothing of a design in progress after its goals naming a design standing in no plans folder",
    "free-design frees a design of each finished or gone name, and reassesses one whose goals are agreed": "--free-design frees a design in progress after its goals naming a design complete",
    "no writing action writes a design other than the one it is run on": "--free-design of design-specs writes the design it is run on, and leaves every other design byte for byte as it was",
    "a taken-up Finding stands though the builder removes the goal it names": "passes a taken-up report whose Finding names a goal the builder renamed while settling",
    SEARCHING: "runs no Search of the reviewer's again",
    "a taken-up report refused for a fault in the builder's parts stays with the builder": "refuses a taken-up report for a Finding the builder's Settlement leaves unsettled",
    "an applying design's citations are read at the last commit": "reports nothing of an applying design citing a heading its own apply retitled",
    "an approved or applying design's research is not read against the files": "reports nothing of the research of a design that is applying",
    "a shorthand citation resolves in a checkout kept beneath another's working files": "resolves a file named in shorthand in a checkout standing under",
    "a form is read from the checkout the script is run in": "appends an entry of a kind the canon of the checkout it is run in declares",
    "a check cut short by a freeing has its entry appended": "appends its entry after the freeing, at the version its report read",
    "check-settled-report passes a round settled in its form, and its entry takes its counts from the report": "passes a taken-up review's report settled with a Cause",
}


def a_tree(name, model=False):
    """-> a copy of the skills and the canon of the checkout the tests are run in, in a folder of its own, a tree
    whose design script a fault is put back into; model gives it the files the search needs beside those it reads."""
    tree = outside(name)
    shutil.copytree(PROJECT / ".ai" / "skills", tree / ".ai" / "skills", ignore=shutil.ignore_patterns("__pycache__"))
    copy_canon(PROJECT, tree)
    if model:
        sys.path.insert(0, str(PROJECT / LIB))
        import search
        shutil.copytree(search.model_folder(), tree / search.SCRATCH / "model")
    return tree


def run_against(tree, names):
    """-> ({a test's name: the count of its checks that failed}, the run's exit status, what it printed): the tests
    named, run by this file against another tree's entry scripts."""
    ran = subprocess.run([sys.executable, str(Path(__file__).resolve()), "--tree", str(tree)] + [a for n in names for a in ("--test", n)], cwd=PROJECT, capture_output=True,
                         env=dict(os.environ, PYTHONIOENCODING="utf-8", PYTHONDONTWRITEBYTECODE="1"))
    out = (ran.stdout + ran.stderr).decode("utf-8", "replace").replace("\r\n", "\n")
    return {m.group(1): int(m.group(3)) for m in re.finditer(r"^test (.+): (\d+) checks?, (\d+) failed$", out, re.M)}, ran.returncode, out


# The faults of the search this design fixed, the search being code the skills share, which the design script runs: what
# each was, the edits putting it back into a copy of .ai/skills/lib/search.py, and words of the check of the search's
# kept tests, the `checkout` suite of search-tests.py, that then fails.
SEARCH_TESTS = "tests/spec-of-record/scripts/search-tests.py"
SEARCH_FAULTS = (
    ("the search's model looked for under the checkout holding its own file, so a second checkout has none",
     [('        _HOME = main_checkout(Path(__file__).resolve().parents[3])\n', '        _HOME = Path(__file__).resolve().parents[3]\n')],
     "the search whose code stands in a second checkout, a worktree, looks for its model where the main checkout keeps it"),
    ("a result's name bounded and never its whole path, so in a folder standing deep the path grows longer than a system opens",
     [('        longest = min(MAX_NAME, MAX_PATH - len(str(Path(folder).resolve())) - 1)\n', '        longest = MAX_NAME\n')],
     "a result written in a folder standing deep keeps its whole path within the longest every system opens, and is written"),
    ("a search naming no project run over the checkout holding its script's file",
     [('    root = Path(root).resolve() if root else checkout_run_in()\n', '    root = Path(root).resolve() if root else Path(__file__).resolve().parents[3]\n')],
     "a search naming no project, run in a second checkout, answers over that checkout's files and writes its result there"),
)


def searchs_tests(tree):
    """-> (the check lines, the exit status, what was printed) of the `checkout` suite of the search's kept tests, the
    file of the checkout these tests are run in, run in another tree, so over that tree's search."""
    ran = subprocess.run([sys.executable, str(PROJECT / SEARCH_TESTS), "checkout"], cwd=tree, capture_output=True,
                         env=dict(os.environ, PYTHONIOENCODING="utf-8", PYTHONDONTWRITEBYTECODE="1"))
    out = (ran.stdout + ran.stderr).decode("utf-8", "replace").replace("\r\n", "\n")
    return [line for line in out.split("\n") if line.startswith(("  pass  ", "  FAIL  "))], ran.returncode, out


def planted(tree, edits, script="design_documents.py"):
    """Put a fault back into a tree's design script, or into another script of the code the skills share -> why it
    could not be planted, or None: each anchor standing exactly once, and the script still one Python reads."""
    path = tree / LIB / script
    text = path.read_text(encoding="utf-8").replace("\r\n", "\n")
    for anchor, put in edits:
        if text.count(anchor) != 1:
            return "its anchor stands %d times in %s, not once: %s" % (text.count(anchor), script, anchor.strip().split("\n")[0][:90])
        text = text.replace(anchor, put)
    try:
        compile(text, str(path), "exec")
    except SyntaxError as wrong:
        return "the script holding it is no Python: %s" % wrong
    path.write_text(text, encoding="utf-8", newline="\n")
    return None


@test("faults", "each fault put back fails its tests")
def _():
    names = [n for _, _, tests in FAULTS for n in tests]
    check("each test a fault names is a test of this file, with the check of it the fault breaks", all(n in TESTS and n in SYMPTOM for n in names), [n for n in names if n not in TESTS or n not in SYMPTOM])
    clean = a_tree("faults-clean", model=True)
    script = (clean / LIB / "design_documents.py").read_bytes()
    why = planted(clean, [("a line that stands nowhere in the design script", "")])
    check("a fault whose anchor does not stand in the script is not planted, and says so, the script left as it was",
          bool(why) and "stands 0 times" in why and (clean / LIB / "design_documents.py").read_bytes() == script, why)
    failed, status, out = run_against(clean, list(dict.fromkeys(names)))
    check("run against a copy of the tree holding no fault, each of those tests passes, so none fails for the copy alone",
          status == 0 and set(failed) == set(names) and not any(failed.values()), out[-3000:])

    def put_back(fault):
        what, edits, tests = fault
        tree = clean if SEARCHING in tests else a_tree("fault")
        why = planted(tree, edits)
        if why:
            return [("NOT PLANTED, so nothing is proved of it: %s: %s" % (what, why), False, "")]
        failed, status, out = run_against(tree, tests)
        fails = [line for line in out.split("\n") if line.startswith("  FAIL  ")]
        return [("put back, %s, the test fails, in the check the fault breaks: %s" % (what, n),
                 status == 1 and failed.get(n, 0) > 0 and "the test ran whole" not in out and any(SYMPTOM[n] in line for line in fails),
                 "the run against the tree holding the fault gave exit %s, where a check holding `%s` was to fail:\n%s" % (status, SYMPTOM[n], out[-1500:])) for n in tests]

    # the faults of the search, each put back in turn into the copy holding the search's model, which the search's own
    # kept tests need, and taken out again: the search's kept tests, run in that copy, test that copy's search
    lines, status, out = searchs_tests(clean)
    check("run in the copy holding no fault, each check of the `checkout` suite of the search's kept tests passes, each one a fault of the search breaks among them",
          status == 0 and all(any(line == "  pass  " + symptom for line in lines) for _, _, symptom in SEARCH_FAULTS), out[-2000:])
    searching = clean / LIB / "search.py"
    held = searching.read_bytes()
    for what, edits, symptom in SEARCH_FAULTS:
        why = planted(clean, edits, "search.py")
        if why:
            check("NOT PLANTED, so nothing is proved of it: %s: %s" % (what, why), False)
            continue
        lines, status, out = searchs_tests(clean)
        searching.write_bytes(held)
        check("put back, %s, the search's kept tests fail, in the check the fault breaks: %s" % (what, symptom),
              status == 1 and "  FAIL  " + symptom in lines and "Traceback" not in out,
              "the run in the tree holding the fault gave exit %s, where the check `%s` was to fail:\n%s" % (status, symptom, out[-1500:]))
    check("each fault of the search taken out again, the copy's search stands as the checkout's", searching.read_bytes() == held)

    # the fault whose test a real search answers is planted last, in the copy holding the search's model
    apart = [f for f in FAULTS if SEARCHING not in f[2]]
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        for checks in list(pool.map(put_back, apart)) + [put_back(f) for f in FAULTS if SEARCHING in f[2]]:
            for label, holds, detail in checks:
                check(label, holds, detail)


# ---------------------------------------------------------------- the kept tests whole in a worktree

# where the worktree the kept tests are run in stands, among the working files of the checkout these tests are run in,
# and the sets of kept tests run there and in that checkout, each by its default run
WORKTREE = PROJECT / ".ai" / "tmp" / "worktrees" / "kept-tests-in-a-worktree"
KEPT_SETS = ("tests/spec-of-record/scripts/design-script-tests.py", SEARCH_TESTS)


def remove_worktree(path):
    """Remove the worktree at a path, registered or left as a bare folder, so none stands or stays registered there."""
    subprocess.run(["git", "worktree", "remove", "--force", str(path)], cwd=PROJECT, capture_output=True)
    if path.exists():
        clear(path)
    subprocess.run(["git", "worktree", "prune"], cwd=PROJECT, capture_output=True)


def kept_set_run(run):
    """-> (the check lines, the exit status, the last lines printed) of a set of kept tests run whole in a checkout."""
    checkout, kept = run
    ran = subprocess.run([sys.executable, str(checkout / kept)], cwd=checkout, capture_output=True, env=dict(os.environ, PYTHONIOENCODING="utf-8", PYTHONDONTWRITEBYTECODE="1"))
    out = (ran.stdout + ran.stderr).decode("utf-8", "replace").replace("\r\n", "\n")
    return [line for line in out.split("\n") if line.startswith(("  pass  ", "  FAIL  "))], ran.returncode, out[-1500:]


@test("worktree", "the kept tests run whole in a worktree, each check giving the result it gives in the checkout")
def _():
    remove_worktree(WORKTREE)
    try:
        git(PROJECT, "worktree", "add", "-q", "--detach", str(WORKTREE), "HEAD")
        # the checkout's uncommitted work laid over the worktree, as the kept comparison lays it: each file changed or
        # new copied in, and each file removed taken out
        changed = [p for args in (("diff", "--name-only", "-z", "HEAD"), ("ls-files", "--others", "--exclude-standard", "-z")) for p in git(PROJECT, *args).split("\0") if p.strip()]
        for path in sorted(set(p.strip() for p in changed)):
            if (PROJECT / path).is_file():
                (WORKTREE / path).parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(PROJECT / path, WORKTREE / path)
            elif (WORKTREE / path).is_file():
                (WORKTREE / path).unlink()
        runs = [(checkout, kept) for kept in KEPT_SETS for checkout in (WORKTREE, PROJECT)]
        with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
            gave = dict(zip(runs, pool.map(kept_set_run, runs)))
    finally:
        remove_worktree(WORKTREE)
    for kept in KEPT_SETS:
        (there, there_status, there_end), (here, here_status, here_end) = gave[(WORKTREE, kept)], gave[(PROJECT, kept)]
        check("%s runs whole in the worktree and passes: %d checks, %d failed" % (kept, len(there), sum(l.startswith("  FAIL") for l in there)), there_status == 0 and bool(there), there_end)
        check("%s runs whole in the checkout and passes: %d checks, %d failed" % (kept, len(here), sum(l.startswith("  FAIL") for l in here)), here_status == 0 and bool(here), here_end)
        check("%s makes the same checks in the worktree as in the checkout, in the same order" % kept, [l[8:] for l in there] == [l[8:] for l in here],
              "\n".join(sorted(set(l[8:] for l in there) ^ set(l[8:] for l in here))[:20]))
        for a, b in zip(there, here):
            if a != b:
                check("%s: a check gives in the worktree the result it gives in the checkout: %s" % (kept, b[8:]), False, "in the worktree: %s\nin the checkout: %s" % (a[:8], b[:8]))
        check("%s: each check gives in the worktree the result it gives in the checkout" % kept, there == here)
    check("the worktree is removed, and none stays registered at its place", not WORKTREE.exists() and WORKTREE.name not in git(PROJECT, "worktree", "list"))


# ---------------------------------------------------------------- what holds each action and each record

P_HANDED, P_SETTLED = "check-handed-back passes a report its cold agent wrote in its form", "check-settled-report passes a round settled in its form, and its entry takes its counts from the report"
R_HANDED = "check-handed-back reports a cold agent's part out of its form"
T_CHANGED = "check-changed-files passes changes within the Target, and reports one outside it"
T_AUDITS = "check-audits passes a design whose audits ran or were bypassed, and reports one owing an audit"
T_GATE, T_VERSION = "no check's entry stands before the agreement of its major version's goals", "a check's entry stands at the version its report read"
T_SUB_SCOPES = "the sub-scopes an audit's entry holds are sub-scopes, and keep each the design changed"
T_SECOND = "a round names the earlier reports of its phase, and a finding landing on an earlier change is one order deeper"
P_RESEARCH = "research searching each goal by meaning and by terms, each match assessed, passes the validation review"
R_RESEARCH = "the research binding a design is read together before its plan's approval"
# Each action of the design script, a row of its FLAGS, and each Script Check record the canon gives the design script,
# by its Name: (the tests in which it passes, the tests in which it reports). A show's reporting test is the one in
# which it shows the other state or refuses what it is given.
COVERAGE = {
    "--check-cited-headings": (["check-cited-headings passes a design citing a heading that stands"], ["check-cited-headings reports a heading that does not stand"]),
    "--check-design-form": (["check-design-form passes a design in its form"], ["check-design-form reports a field out of the form"]),
    "--check-target-kind": (["check-target-kind passes a Target of the design's Kind"], ["check-target-kind reports a Target of another kind"]),
    "--check-design": (["check-design passes an approved design whose research its log names"], ["check-design reports a design not yet stated"]),
    "--check-workstack": (["show-workstack and check-workstack read a plans folder given, and refuse a folder that is none"], ["check-workstack reports a loop and a field out of the form", "check-workstack reads each name from the plans folders"]),
    "--show-workstack": (["show-workstack reads each name from the plans folders"], ["show-workstack and check-workstack read a plans folder given, and refuse a folder that is none"]),
    "--show-design": (["show-design shows the header and the goals of a design in a plans folder"],
                      ["show-design shows a design in an older form as far as it reads, and names what is missing", "show-design shows nothing of a design outside the plans folders"]),
    "--check-design-names": (["check-design-names passes a design naming none and reports one in no plans folder"], ["check-design-names reads each name from the plans folders"]),
    "--free-design": (["free-design frees a design of each finished or gone name, and reassesses one whose goals are agreed"], ["free-design refuses a design in no plans folder"]),
    "--show-dependents": (["show-dependents lists the parts naming a part"], ["show-dependents refuses a name the design does not hold"]),
    "--show-validation": (["show-validation shows a design validated"], ["show-validation shows a design stale or never stamped"]),
    "--stamp-validation": (["stamp-validation stamps a design the validation review passes"], ["stamp-validation refuses a design the validation review reports"]),
    "--log-entry": (["log-entry appends an entry of each kind in its type"], ["log-entry refuses an entry out of its type"]),
    "--check-handed-back": ([P_HANDED], [R_HANDED]),
    "--take-up-report": (["take-up-report writes a fingerprint of each part the cold agent wrote"], [R_HANDED]),
    "--check-settled-report": ([P_SETTLED], ["a finding is settled once"]),
    "--show-reach": (["show-reach lists each line of a durable file holding a retired phrase"], ["show-reach lists no line where no durable file holds the phrase"]),
    "--check-retired-wording": (["check-retired-wording passes a Target holding no retired phrase"], ["check-retired-wording reports a line of the Target holding a retired phrase"]),
    "--check-changed-files": ([T_CHANGED], [T_CHANGED]),
    "--check-audits": ([T_AUDITS], [T_AUDITS]),
    "--check-work": (["check-work passes work adding no finding"], ["check-work reports a finding the work added"]),
    "--check-kept-tests": (["check-kept-tests runs the kept tests of each script the files given hold a file of"], ["check-kept-tests fails where a kept test fails or a kept file cannot be run"]),
    "--refresh-links": (["refresh-links leaves a file whose links are current"], ["refresh-links writes the link of each citation in a file a person reads"]),
    "--check-constructs": (["check-constructs passes a file whose constructs hold their forms"], ["check-constructs reports a construct out of its form"]),
    "--show-refactor-and-refine-of-existing-specs": (["show-refactor-and-refine-of-existing-specs shows what changed since a baseline"], ["show-refactor-and-refine-of-existing-specs refuses a baseline that is no commit"]),
    "kept-tests-pass-at-the-self-review": (["a self-review over applied work is appended where the kept tests pass, their result in its report"], ["a self-review over applied work is refused where a kept test fails"]),
    "counts-taken-from-the-report": ([P_SETTLED], ["a count given a check's entry is refused"]),
    "goals-agreed-before-checks": ([T_GATE], [T_GATE]),
    "entry-at-the-version-read": ([T_VERSION], [T_VERSION]),
    "sub-scopes-named": ([T_SUB_SCOPES], [T_SUB_SCOPES]),
    "settled-sub-scopes-keep-what-changed": ([T_SUB_SCOPES], [T_SUB_SCOPES]),
    "audits-run-or-bypassed": ([T_AUDITS], [T_AUDITS]),
    "cold-parts-kept": (["take-up-report writes a fingerprint of each part the cold agent wrote", P_SETTLED], ["a part its cold agent wrote is held to its fingerprint", R_HANDED]),
    "report-in-its-form": ([P_HANDED, P_SETTLED], [R_HANDED, "a round settled out of its form is reported"]),
    "findings-anchored-in-the-design": ([P_HANDED, "a taken-up Finding stands though the builder removes the goal it names"], [R_HANDED]),
    "report-laid-out": ([P_HANDED, P_SETTLED], ["a report laid out other than its form's layout is reported"]),
    "findings-settled-once": ([P_SETTLED], ["a finding is settled once"]),
    "settlements-justified": ([P_SETTLED], ["a settlement is justified by what requires it"]),
    "orders-follow-their-lineage": ([T_SECOND], ["an order follows its lineage", T_SECOND]),
    "report-keys-name-records": ([P_SETTLED, T_SECOND], ["a key a report cites names a record", R_HANDED]),
    "departures-reasoned": ([P_SETTLED, "a count given a check's entry is refused"], ["a departure from a finding's writer is reasoned"]),
    "searches-cover-their-matches": ([P_HANDED, "a reviewer's Search is run as its report is handed back and taken up"],
                                     [R_HANDED, "a reviewer's Search is run as its report is handed back and taken up", "a tactical fix covers each place its Search of the design document found"]),
    "reads-assessed": (["each place a research report read lies in an area it assesses"], ["each place a research report read lies in an area it assesses"]),
    "area-reassessments-name-their-cause": (["an area assessed again names a cause that counts"], ["an area assessed again names a cause that counts"]),
    "research-covers-its-matches": ([P_RESEARCH], [R_RESEARCH, "research whose Search gives a place no Area covers, or leaves a durable file unsearched, is reported"]),
    "goals-searched-over-every-durable-file": ([P_RESEARCH], [R_RESEARCH, "research whose Search gives a place no Area covers, or leaves a durable file unsearched, is reported"]),
    "traces-name-their-paths": (["a self-review traces each mechanism its phase gives it"], ["a self-review traces each mechanism its phase gives it"]),
    "builder-checks-required": (["a self-review's entry is appended, its script checks' output written into its report"],
                                ["a self-review holds each Builder Check required of it", "the first self-review of a major version records the re-evaluation of the Problem"]),
    "reads-cover-the-misses": (["a self-review following a round's change reads each place a Miss names, and works the round's cases"], ["a self-review following a round's change reads each place a Miss names, and works the round's cases"]),
    "earlier-reports-listed": ([T_SECOND], [T_SECOND]),
    "settling-reads-cover-the-evidence": ([P_SETTLED], ["a round's settling reads cover its evidence"]),
    "tactical-fixes-cover-their-searches": (["a tactical fix covers each place its Search of the design document found"], ["a tactical fix names a search giving every place"]),
    "places-in-their-form": ([P_HANDED, P_SETTLED], [R_HANDED]),
    "diagnosis-whole-and-in-form": (["a design-reassessment entry chosen at the step back holds its Cause, its Decision and its Diagnosis", "a diagnosis leaving out a finding of its flaw set is refused"],
                                    ["a diagnosis is held to its form as its entry is appended", "a diagnosis leaving out a finding of its flaw set is refused"]),
}


def canon_records():
    """-> {Name: the flags of the design script carrying it out} for each Script Check record the canon of the checkout
    holds whose Carried Out By names an entry script of the design script, a record in a fenced block aside."""
    out = {}
    for path in sorted((PROJECT / "specs").rglob("*.md")):
        lines, heading, fenced = path.read_text(encoding="utf-8").replace("\r\n", "\n").split("\n"), "", False
        for i, line in enumerate(lines):
            if line.lstrip().startswith(("```", "~~~")):
                fenced = not fenced
            if line.startswith("#"):
                heading = line
            named = re.match(r"\s*- \*\*Name:\*\* (\S+)", line)
            if not named or fenced or "Script Checks" not in heading:
                continue
            end = next((j for j in range(i + 1, len(lines)) if re.match(r"\s*- \*\*Name:\*\*|#", lines[j])), len(lines))
            carried = "\n".join(lines[i:end]).partition("**Carried Out By:**")[2]
            flags = sorted(set(re.findall(r"`\.ai/skills/(?:design-specs|implement-specs)/` `(--[a-z-]+)`", carried)))
            if flags:
                out[named.group(1)] = flags
    return out


@test("coverage", "each action and each Script Check record is held by a passing test and a reporting test")
def _():
    flags, records = [row[0] for row in own_lib().FLAGS], canon_records()
    check("the design script holds actions, and the canon Script Check records it carries out, to hold to the table", len(flags) > 20 and len(records) > 20, (len(flags), len(records)))
    for kind, names in (("action", flags), ("Script Check record", list(records))):
        for name in names:
            holds = COVERAGE.get(name, ([], []))
            check("the %s %s is held by a test in which it passes and one in which it reports" % (kind, name), bool(holds[0]) and bool(holds[1]),
                  "the table of this file names no %s test for it" % ("passing" if not holds[0] else "reporting"))
    known = set(flags) | set(records)
    check("the table names no action and no record the script and the canon do not hold", set(COVERAGE) <= known, sorted(set(COVERAGE) - known))
    named = sorted({n for holds in COVERAGE.values() for tests in holds for n in tests})
    check("each test the table names is a test of this file", all(n in TESTS for n in named), [n for n in named if n not in TESTS])
    ran = [n for n in named if n in RESULTS]
    check("each test the table names that this run made passed: %d of %d were run" % (len(ran), len(named)), all(RESULTS[n] for n in ran), [n for n in ran if not RESULTS[n]])
    for name, (passing, reporting) in COVERAGE.items():
        for way, tests in (("passes", passing), ("reports", reporting)):
            if not any(n in RESULTS for n in tests) and tests and RESULTS and not ONLY:
                print("        not run in this run, a test in which %s %s: %s" % (name, way, tests[0]))


# The modules of the code the skills share whose own checks the design script only runs over a design's work, by
# --check-work, the specs' and the code's script checks, and the search, which holds kept tests of its own: a file of
# the canon one of them reads in place is no file the design script reads a form from.
RUN_OVER_THE_WORK = ("spec_checks.py", "code_checks.py", "search.py")
CANON_FILE = re.compile(r"specs/(?:AGENTS\.md|architecture\.md|main\.md|methodology/[\w/.-]+\.md)")


def forms_read():
    """-> {a file of the canon: [where the code holds its path]} for each file the design script reads a form from as
    it runs, read from the source of the code the skills share: each string that is the path of a file of the canon
    and nothing more, a path the code opens the file by or finds its text under. A path with a section after it names
    a rule in a message, a path in a docstring describes, and a path a comparison tests another path against sorts
    files by their kind: none of the three reads the file."""
    import ast
    out = {}
    for module in sorted((PROJECT / LIB).glob("*.py")):
        if module.name in RUN_OVER_THE_WORK:
            continue
        tree = ast.parse(module.read_text(encoding="utf-8"))
        compared = {id(n) for node in ast.walk(tree) if isinstance(node, ast.Compare) for n in ast.walk(node)}
        described = {id(n.body[0].value) for n in ast.walk(tree) if isinstance(n, (ast.Module, ast.FunctionDef, ast.ClassDef)) and n.body
                     and isinstance(n.body[0], ast.Expr) and isinstance(n.body[0].value, ast.Constant)}
        for node in ast.walk(tree):
            if isinstance(node, ast.Constant) and isinstance(node.value, str) and CANON_FILE.fullmatch(node.value) and id(node) not in compared | described:
                out.setdefault(node.value, []).append("%s line %d" % (module.name, node.lineno))
    return out


def declared_in(path, name):
    """-> the tuple a kept file declares under a name at its top level, read from its text."""
    import ast
    for node in ast.parse(path.read_text(encoding="utf-8")).body:
        if isinstance(node, ast.Assign) and len(node.targets) == 1 and getattr(node.targets[0], "id", None) == name:
            return ast.literal_eval(node.value)
    return None


@test("coverage", "FORM_FILES names each file of the canon the design script reads a form from, and no other")
def _():
    read = forms_read()
    check("the code the skills share holds the paths of files of the canon to read forms from", len(read) >= 3, read)
    for path, where in sorted(read.items()):
        check("the design script reads a form from %s, which FORM_FILES names" % path, path in FORM_FILES, "its path is held at " + ", ".join(where))
    for path in FORM_FILES:
        check("FORM_FILES names %s, a file the design script reads a form from" % path, path in read and (PROJECT / path).is_file(),
              "no code the skills share holds its path to read it by, or it does not stand")
    check("the kept comparison names the same files as its script's", declared_in(PROJECT / COMPARISON, "FORM_FILES") == FORM_FILES
          and declared_in(PROJECT / COMPARISON, "SCRIPT_FILES") == SCRIPT_FILES, declared_in(PROJECT / COMPARISON, "FORM_FILES"))


# ---------------------------------------------------------------- running the suites

def run_test(name):
    NOW.checks = []
    try:
        TESTS[name]()
    except Exception as raised:  # a test that could not be made is a test that failed
        import traceback
        NOW.checks.append((name + ": the test ran whole", False, traceback.format_exc()[-1500:]))
    if not NOW.checks:
        NOW.checks.append((name + ": the test made a check", False, ""))
    return NOW.checks


def run_suite(suite, workers, chosen=None):
    """Run a suite's tests, several at once, each in a project of its own, and print each check in the order the tests
    are written; chosen, where given, the tests to run of it, each then followed by a line counting its checks."""
    names = [n for n in SUITES[suite] if (n in chosen if chosen is not None else ONLY in n)]
    if not names:
        return
    print("%s: %d test%s" % (suite, len(names), "" if len(names) == 1 else "s"))
    with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as pool:
        for name, checks in zip(names, pool.map(run_test, names)):
            RESULTS[name] = all(holds for _, holds, _ in checks)
            for label, holds, detail in checks:
                print(("  pass  " if holds else "  FAIL  ") + label + ("" if holds or not detail else "\n        " + str(detail).replace("\n", "\n        ")))
                if not holds:
                    FAILED.append(label)
            if chosen is not None:
                print("test %s: %d check%s, %d failed" % (name, len(checks), "" if len(checks) == 1 else "s", sum(not holds for _, holds, _ in checks)))
    sys.stdout.flush()


# the suites a run naming none leaves out: the one putting each fault back, which runs this file again for each, and
# the one running both sets of kept tests whole in a worktree and in the checkout
SLOW = ("faults", "worktree")
# the suites whose one test runs others, or reads what the run made, which runs alone and last
LAST = ("faults", "worktree", "coverage")
WORKERS = min(8, os.cpu_count() or 2)


def taken(args, flag):
    """-> each value a flag is given among a run's arguments, taken out of them."""
    out = []
    while flag in args:
        at = args.index(flag)
        out.append(args[at + 1])
        del args[at:at + 2]
    return out


def main(argv):
    global TREE, ONLY
    for stream in (sys.stdout, sys.stderr):
        stream.reconfigure(encoding="utf-8")
    args = list(argv[1:])
    tree, only, chosen = taken(args, "--tree"), taken(args, "--only"), taken(args, "--test")
    TREE, ONLY = Path(tree[-1]).resolve() if tree else PROJECT, only[-1] if only else ""
    named = [a for a in args if not a.startswith("--")]
    missing = [n for n in named if n not in SUITES and n[:-len("_suite")] not in SUITES] + [n for n in chosen if n not in TESTS]
    if missing or [a for a in args if a.startswith("--") and a != "--all"]:
        print("no suite, test or flag named %s: the suites are %s, and the flags --all, --only, --test and --tree"
              % (", ".join(missing + [a for a in args if a.startswith("--") and a != "--all"]), ", ".join(SUITES)))
        return 2
    if chosen:
        suites = [s for s in SUITES if any(n in chosen for n in SUITES[s])]
    elif named:
        suites = [s for s in SUITES if s in named or s + "_suite" in named]
    else:
        suites = [s for s in SUITES if s not in SLOW or "--all" in args]
    suites = [s for s in suites if s not in LAST] + [s for s in LAST if s in suites]
    started = time.perf_counter()
    try:
        for suite in suites:
            run_suite(suite, WORKERS, chosen or None)
    finally:
        gc.collect()
        for folder in MADE:
            clear(folder)
    print("%d failed" % len(FAILED) if FAILED else "every check passed", "in %.0f seconds" % (time.perf_counter() - started))
    return 1 if FAILED else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
