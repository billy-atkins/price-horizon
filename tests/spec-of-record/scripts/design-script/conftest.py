"""The design script's set of kept tests: which files are the design script's, and what the set's files share.

A test drives the design script as a design's work does: an entry script, .ai/skills/design-specs/scripts/design-specs.py
or .ai/skills/implement-specs/scripts/implement-specs.py, run as a process of its own in a project the test builds in
its own folder. A project holds, taken as the test runs, files of the canon FORM_FILES names and no other: the forms
the script reads and the indexes it finds them by, FORMS_ALONE, or, where its test runs the checks of the specs, the
whole of FORM_FILES. So each form the script reads is the one the checkout's canon declares, and a change to any file
of the canon a project is given runs these tests. Beside those it holds only what the test gives it: design documents, reports, diagnoses and other files
made from the test's fixtures. No test reads the checkout's plans folders, what the checkout holds uncommitted, or
where the checkout sits: git finds no repository above a run's folder, so a project is under version control only
where its test puts it there.

The builders here (`Project`, `a_design`, `a_report` and those made from them) take the fixtures, the folder and the
`check` of the test that is running, which `the_test` hands them as each test starts. So a builder makes its document
from the fixture the test's `reads` marker names, and a test that names none of a fixture a builder needs fails
saying which.

A test file takes these names by `from design_script_set import ...`, the name this file is registered under as the
runner loads it.

The entry scripts run are the checkout's own, or, where DESIGN_SCRIPT_TREE names a folder, those of that tree: a copy
of the skills holding a fault, which test_faults.py runs the tests against.
"""
import os
import re
import shutil
import subprocess
import sys
import types
from pathlib import Path

import pytest

# The files of the script these tests are of, the design script: its code, and each file of the canon it reads as it
# runs. Its code is the code the skills share, whole, which reads a form from some files of the canon, finds the specs
# by their indexes, and, in the checks of the specs --check-work runs, reads the methodology's files themselves. So
# FORM_FILES names every file of the canon a project of this set is given, and a change to any of them runs these
# tests. A path ending in a slash names each file beneath it.
SCRIPT_FILES = (".ai/skills/lib/", ".ai/skills/design-specs/scripts/", ".ai/skills/implement-specs/scripts/")
FORM_FILES = ("specs/AGENTS.md", "specs/architecture.md", "specs/index.md", "specs/methodology/")
ACTIONS_IN = ".ai/skills/lib/design_documents.py"
# what most projects take, each a file FORM_FILES names: the files the design script reads a form from, and the index
# of each folder from specs/ down to each, by which the script's walk of the specifications finds them and so reads
# each record type they declare
FORMS_READ = ("specs/methodology/working-files/main.md", "specs/methodology/design-workflow/order-of-a-designs-work.md", "specs/methodology/modeling-constructs.md",
              "specs/methodology/expressions.md", "specs/methodology/spec-style/markdown.md", "specs/methodology/skills/registered-skills.md",
              "specs/methodology/skills/authoring-a-skill.md")
FORMS_ALONE = FORMS_READ + tuple(sorted({"/".join(f.split("/")[:n]) + "/index.md" for f in FORMS_READ for n in range(1, f.count("/") + 1)}))


def within_form_files(path):
    """Whether a path lies within FORM_FILES: a file it names, a folder it names by a path ending in a slash, or a
    file or folder beneath such a folder."""
    return any(path == f or path + "/" == f or (f.endswith("/") and path.startswith(f)) for f in FORM_FILES)

CHECKOUT = Path(__file__).resolve().parents[4]
LIB = Path(".ai") / "skills" / "lib"
SET = "tests/spec-of-record/scripts/design-script"
TREE_NAMED = "DESIGN_SCRIPT_TREE"
# the tree whose entry scripts the tests run: the checkout's own, or a copy holding a fault
TREE = Path(os.environ.get(TREE_NAMED) or CHECKOUT).resolve()
if str(CHECKOUT / LIB) not in sys.path:
    sys.path.insert(0, str(CHECKOUT / LIB))
import design_documents  # noqa: E402  the checkout's own, for a stamp's hash and the values a test holds its own to
import spec_text  # noqa: E402

sys.modules["design_script_set"] = sys.modules[__name__]

NOW = types.SimpleNamespace(work=None, fixtures=None, check=None, made=0)


@pytest.fixture(autouse=True)
def the_test(work, fixtures, check):
    """Hands the builders the folder, the fixtures and the `check` of the test that is running."""
    NOW.work, NOW.fixtures, NOW.check, NOW.made = work, fixtures, check, 0
    yield
    NOW.work = NOW.fixtures = NOW.check = None


def check(name, holds, detail=""):
    """One check a builder makes for the test that is running, recorded as the test's own are."""
    NOW.check(name, holds, detail)


def base(key):
    """-> the snippet of a fixture the running test's `reads` marker names."""
    if key not in NOW.fixtures:
        raise AssertionError("the test builds from the fixture %s, which its `reads` marker does not name" % key)
    return NOW.fixtures[key]


def own_lib():
    """-> the design script's code as the checkout the tests are run in holds it, imported to work out a stamp's hash
    for a design made for a test, which no entry script gives without the whole validation review."""
    return design_documents


def git(root, *args):
    done = subprocess.run(["git", "-c", "user.name=design-script-tests", "-c", "user.email=design-script-tests@example.invalid",
                           "-c", "core.autocrlf=false", "-c", "commit.gpgsign=false", "-c", "init.defaultBranch=main"] + list(args),
                          cwd=root, capture_output=True, text=True, encoding="utf-8")
    if done.returncode:
        raise AssertionError("git %s: %s" % (" ".join(args), done.stderr))
    return done.stdout.strip()


def copy_files(source, root, files):
    """Copy files and folders, each a path from a root, from one tree into another, as the test runs."""
    for rel in files:
        if (source / rel).is_dir():
            shutil.copytree(source / rel, root / rel, ignore=shutil.ignore_patterns("__pycache__"), dirs_exist_ok=True)
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
    text = base("ferry-design").replace(NAME, name)
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

AGREED = (("entered", {"Reason": "taken up"}), ("goals-agreed", {}))
DRAFTED = AGREED + (("plan-change", {}),)
APPROVED = DRAFTED + (("plan-approval", {"Approval": "approved"}),)
APPLYING = APPROVED + (("apply", {}),)


class Project:
    """A project made for a test, in the test's own folder: the files of the canon the design script reads a form
    from, with their indexes, as the checkout the tests are run in holds them, a guide of its own for a design to
    change, and what the test puts in it. name says what the project is for, to a reader of the test; canon False
    gives it no file of the canon, and a tuple of paths gives it those in their place, each one lying within
    FORM_FILES, as FORM_FILES itself where a test runs the checks of the specs. It stands in a folder of a short
    name of its own, p1 for a test's first, since a project's files stand deep and the folder above it is long; root
    gives it another place, the folder the tests of a file share."""

    def __init__(self, name="", versioned=False, canon=True, under=None, root=None):
        self.root = Path(root) if root else a_place()
        if under:  # a checkout kept beneath another folder's files, as a worktree is kept beneath a checkout's
            self.root = self.root / under
        self.root.mkdir(parents=True)
        if canon:
            taken = FORMS_ALONE if canon is True else tuple(canon)
            outside = [path for path in taken if not within_form_files(path)]
            if outside:
                raise AssertionError("a project is given no file of the canon FORM_FILES does not name: " + ", ".join(outside))
            copy_files(CHECKOUT, self.root, taken)
        self.put("docs/guide.md", base("island-guide"))
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

    def run(self, *args, skill="design-specs", inside=""):
        """-> (the exit status, what it printed) of an entry script of the tree under test, run in this project as a
        design's work runs it: at its root, or in the folder inside it that is given."""
        entry = TREE / ".ai" / "skills" / skill / "scripts" / (skill + ".py")
        ran = subprocess.run([sys.executable, "-B", str(entry)] + [str(a) for a in args], cwd=self.root / inside, capture_output=True,
                             env=dict(os.environ, PYTHONIOENCODING="utf-8", PYTHONDONTWRITEBYTECODE="1"))
        return ran.returncode, (ran.stdout + ran.stderr).decode("utf-8", "replace").replace("\r\n", "\n")

    def held(self, under=".ai/plans"):
        """-> {path: bytes} of each file under a folder, to compare before and after an action."""
        return {p.relative_to(self.root).as_posix(): p.read_bytes() for p in sorted((self.root / under).rglob("*")) if p.is_file()}

    @classmethod
    def copied(cls, folder, versioned=False, left_out=()):
        """-> a project that is a copy of a folder, in the running test's own folder; versioned puts it under version
        control, its files committed, the paths left_out kept from version control."""
        p = cls.__new__(cls)
        p.root, p.versioned = a_place(), versioned
        shutil.copytree(folder, p.root)
        if versioned:
            git(p.root, "init", "-q")
            (p.root / ".git" / "info" / "exclude").write_text("".join(path + "/\n" for path in left_out), encoding="utf-8")
            p.commit()
        return p


def a_place():
    """-> a folder not yet made for a project, within the running test's own folder."""
    NOW.made += 1
    return NOW.work / ("p%d" % NOW.made)


# ---------------------------------------------------------------- a report made for a test

SKILLS = ("design-specs", "implement-specs")
BUILDER_PARTS = ("## Hand-back", "## Script Output", "## Causes", "## Settlement")


def report_at(kind, n=1, name=NAME, skill="design-specs"):
    return ".ai/tmp/%s/%s/reports/%s/%d.md" % (skill, name, kind, n)


def a_report(which, name=NAME, skill="design-specs", entry=None, version=None):
    """-> the text of a report made from a base report, research, review or self-review, for the design and the entry
    given, its Reading holding the version given."""
    text = base("ferry-%s-report" % which).replace(NAME, name)
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

RESEARCH = (("handed-off-judgment", {}),)
APPROVED_RESEARCHED = AGREED + RESEARCH + (("plan-change", {}), ("plan-approval", {"Approval": "approved"}))
APPLYING_RESEARCHED = APPROVED_RESEARCHED + (("apply", {}),)


def researched(p, name=NAME, skill="design-specs", **given):
    """Write a design whose log names its research, with that research's report in its folder -> the design's path."""
    p.put(report_at("handed-off-judgment", 1, name, skill), a_report("research", name, skill))
    return p.design(name, skill=skill, **given)

# ---------------------------------------------------------------- a design naming another

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

# ---------------------------------------------------------------- a design's log

PAST_THE_FRAME = {"plan-change": (), "design-refactor-refine": CHECK_FIELDS, "self-review": CHECK_FIELDS, "another-round": (),
                  "plan-approval": ("Approval=approved",), "step-back": (), "apply": ()}
BLOCKED = "entry begins or continues work past the frame, and its Depends On Designs names %s, unfinished: a blocked design is worked no further than its agreed goals and frame"


def a_clean_report(kind, name=NAME, version="1.0.1", n=1):
    """-> the text of a report of a check that found nothing: a review's, the cold reviewer's Reading and the builder's
    Settlement, or the builder's triage of an audit, for the design, the entry and the version given."""
    text = base("review-report-finding-nothing" if kind in ("adversarial-review", "post-apply-review") else "audit-report-finding-nothing").replace(NAME, name)
    text = re.sub(r"^\*\*Entry:\*\* .*$", lambda m: "**Entry:** %s-%d" % (kind, n), text, count=1, flags=re.M)
    return re.sub(r"^\*\*Design Version:\*\* \S+", lambda m: "**Design Version:** " + version, text, count=1, flags=re.M)


def a_diagnosis(name=NAME, entry=1, flaws=True):
    text = swap(base("ferry-diagnosis").replace(NAME, name), "design-reassessment-1", "design-reassessment-%d" % entry)
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
    return own_lib().log_type(CHECKOUT)[2]

# ---------------------------------------------------------------- a design shown, and a design of the earlier rules

PROBLEM_WORDS, STEP_WORDS = "names the ferry without saying when it runs", "The section names the ferry and gives no time."
OLD_FIELD = "**Depends On:** "


def with_old_field(text, named):
    """-> a design's text holding the old Depends On field, naming a design, in place of its Depends On Designs."""
    return swap(text, "**Depends On Designs:** none", OLD_FIELD + named)


def with_reliance(text, named):
    """-> a design's text whose Scope holds a Reliance on a design, as the earlier rules had one written."""
    reliances = base("reliances-on-one-design").replace("quay-rebuilt", named)
    return swap(text, "\nThe sweep read the guide whole.", "\n" + reliances + "\nThe sweep read the guide whole.")


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


# ---------------------------------------------------------------- research, and the log's gates on a check's entry

LIGHTHOUSE = "`docs/guide.md § The Lighthouse`"


def second_share(cause=None, steer=False, area=FERRY):
    """-> (a project whose design's log names a first research report, the path of a second handed back, assessing an
    Area again): the second naming the cause given, the design holding a set of steers logged after the first where
    steer is set."""
    p = Project("assessed-again")
    log = AGREED + RESEARCH + ((("steer", {"Steering Decision": "winter-hours-count"}),) if steer else ())
    text = a_design(log=log)
    p.design(text=swap(text, "\n## Design Plan Steps", "\n" + base("steering-decisions-of-one-steer") + "\n## Design Plan Steps") if steer else text)
    p.put(report_at(JUDGMENT, 1), a_report("research"))
    second = swap(cold_part(a_report("research", entry="handed-off-judgment-2")), "**Area:** " + FERRY, "**Area:** " + area).replace("**Reads:**\n  - " + FERRY, "**Reads:**\n  - " + area)
    if cause:
        second = second.rstrip("\n") + "\n\n    **Assessed Again For:** %s\n" % cause
    return p, p.put(report_at(JUDGMENT, 2), second)


def outside_every_area(text):
    """-> a research report whose Search by meaning holds a place lying in no Area it assesses."""
    return swap(text, "    **Places:**\n      - " + FERRY, "    **Places:**\n      - %s\n      - %s" % (FERRY, LIGHTHOUSE))


COVERS = "Search ferry-times-by-meaning of %s holds %s, which no binding research report's Read Assessment's Area covers"
BY_TERMS = "the goal %s is named by no Search by terms of the operative files naming no commit, among the research binding the design" % GOAL


# ---------------------------------------------------------------- the builder's self-review

SELF = "self-review"
RE_EVALUATION = "  - **Check:** problem-read-against-the-guide \\\n    **Kind:** problem re-evaluation \\\n    **Places Checked:**\n      - `docs/guide.md § The Ferry`\n\n" \
                "    **Result:** The section still names the ferry and gives no time.\n\n"
LINKED = "  - **Check:** work-handed-on \\\n    **Kind:** linked work \\\n    **Places Checked:**\n      - `.ai/plans/design-specs/%s.md § Out of Scope`\n\n    **Result:** The design hands no work on.\n\n" % NAME
QUAY_LINE = "The ferry leaves from the north quay.\n"  # the line of the guide's section The Ferry


def a_check(key, kind, *places):
    return "  - **Check:** %s \\\n    **Kind:** %s \\\n    **Places Checked:**\n%s\n\n    **Result:** It holds.\n\n" % (key, kind, "\n".join("      - `%s`" % place for place in places))


def with_checks(text, *checks):
    """-> a self-review's report with Builder Checks added after those it holds."""
    return swap(text, "## Settlement", "".join(checks) + "## Settlement")


def applied(p, skill="design-specs", log=APPLYING, checks=(), **given):
    """-> (the path of an applying design, the path of its first self-review's report over the applied work)."""
    design = p.design(skill=skill, status="applying", log=log, **given)
    return design, p.put(report_at(SELF, skill=skill), with_checks(a_report("self-review", skill=skill), *checks))


# ---------------------------------------------------------------- a script's kept tests, run by the design script

KEPT = "tests/spec-of-record"
KEPT_RUN = ".ai/tmp/kept-tests"
KEPT_RULE = RULE % "kept-tests-pass-at-the-self-review"
# the registered runner as the checkout holds it: its settings and what every test is handed, and the code the skills
# share that the second reads, each copied into a project as its test runs
RUNNER = (KEPT + "/pytest.ini", KEPT + "/conftest.py")
RUNNER_READS = tuple(".ai/skills/lib/%s.py" % module for module in ("spec_text", "citation_links", "reading"))
GUIDE_SET, GUIDE_TESTS = KEPT + "/scripts/guide", KEPT + "/scripts/guide/test_guide.py"
OTHER_DESIGN = ".ai/plans/design-specs/other-design.md"


def kept_tests(p, tests=None, comparison=None):
    """Give a project the registered runner and a set of kept tests of a script of its own, the guide's, whose code
    is tools/guide.py and whose form is read from docs/guide.md: the set's conftest.py, its file of two tests, the
    fixture file one of them reads and the fixtures' index. tests, where given, is the text of the set's file of
    tests, and comparison the text of a kept comparison standing in the set."""
    copy_files(CHECKOUT, p.root, RUNNER + RUNNER_READS)
    p.put("tools/guide.py", base("guide-script"))
    p.put(GUIDE_SET + "/conftest.py", base("guide-set-conftest"))
    p.put(GUIDE_TESTS, base("guide-set-tests") if tests is None else tests)
    p.put(KEPT + "/fixtures/guide.md", base("fixture-file-of-one-line"))
    p.put(KEPT + "/fixtures/index.md", base("index-listing-one-file"))
    if comparison is not None:
        p.put(GUIDE_SET + "/comparison.py", comparison)


def failing(tests):
    """-> the guide's file of tests with one check that does not hold: its sum given a wrong answer."""
    return swap(tests, "2 + 2 == 4", "2 + 2 == 5")


def outside_the_run(p):
    """-> {path: bytes} of each file of a project standing outside the folder a run of its kept tests writes within."""
    return {path: held for path, held in p.held(".").items() if not path.startswith(KEPT_RUN + "/")}


def run_holds(p):
    """-> the name of each thing standing in the folder a run of a project's kept tests writes within."""
    return sorted(held.name for held in (p.root / KEPT_RUN).iterdir()) if (p.root / KEPT_RUN).is_dir() else None


def a_run(checkout_run_in, folder, args, tree=None):
    """Make a run of kept tests as a process of its own, in a checkout, writing within a folder of its own inside the
    folder of the run that started it; tree, where given, names the tree whose entry scripts the design script's tests
    then run -> (the run's exit status; what its report holds of each test, as the design script reads a run's report,
    or None; what it printed)."""
    env = dict(os.environ, PYTHONIOENCODING="utf-8", PYTHONDONTWRITEBYTECODE="1", **{spec_text.KEPT_RUN_NAMED: str(folder)})
    env.pop(TREE_NAMED, None)
    if tree:
        env[TREE_NAMED] = str(tree)
    ran = subprocess.run([sys.executable, "-B", "-m", "pytest"] + [str(a) for a in args], cwd=checkout_run_in, capture_output=True, env=env)
    cases, _ = design_documents.read_kept_report(Path(folder) / spec_text.KEPT_REPORT)
    return ran.returncode, cases, (ran.stdout + ran.stderr).decode("utf-8", "replace").replace("\r\n", "\n")


# ---------------------------------------------------------------- the kept comparison

COMPARISON = SET + "/comparison.py"
SCRIPT = ".ai/skills/lib/design_documents.py"
MAIN = "specs/methodology/working-files/main.md"


def a_script_project(name, versioned=True):
    """-> a project holding the design script itself, a copy of the skills of the checkout the tests are run in, taken
    as the test runs, with the kept comparison, committed: a checkout the comparison reads the last commit's script
    from."""
    p = Project(name)
    copy_files(CHECKOUT, p.root, (".ai/skills", COMPARISON))
    if versioned:
        git(p.root, "init", "-q")
        p.commit()
    return p


def compared(p, *args):
    ran = subprocess.run([sys.executable, "-B", str(p.root / COMPARISON)] + list(args), cwd=p.root, capture_output=True,
                         env=dict(os.environ, PYTHONIOENCODING="utf-8", PYTHONDONTWRITEBYTECODE="1"))
    return ran.returncode, (ran.stdout + ran.stderr).decode("utf-8", "replace").replace("\r\n", "\n")


def listed(got):
    return re.findall(r"^design (\S+)$", got[1], re.M)


def three_designs(p):
    p.design("first-design", log=DRAFTED)
    p.design("second-design", status="approved", log=APPROVED)
    p.design("odd-name", text=swap(a_design("odd-name", log=DRAFTED), "**Name:** odd-name", "**Name:** Odd Name"))
    return ".ai/plans/design-specs"


# ---------------------------------------------------------------- the checks a real search answers

SEARCH_INDEX = ".ai/tmp/search-spec-of-record-scope"
# builds the search's index of a project, by the search of the tree whose entry scripts the tests run
BUILD_INDEX = "import sys\nsys.dont_write_bytecode = True\nsys.path.insert(0, sys.argv[1])\nimport search\nsearch.Search(sys.argv[2], quiet=True).db.close()\n"


@pytest.fixture(scope="module")
def shared_folder(request, run_folder):
    """The folder the tests of one file share, within the run's folder and named for the file: made empty as the
    file's first test asks for it, and removed as the file ends."""
    folder = run_folder / Path(str(request.path)).stem
    spec_text.clear_run(folder)
    yield folder
    spec_text.clear_run(folder)
    folder.rmdir()


@pytest.fixture
def a_searched_project(request, shared_folder):
    """-> a function giving a project the search has read: a copy, in the test's own folder, of the one project the
    file's tests share, which the first of them to ask builds in the file's folder: the files a form is read from, with
    what the file's SHARED_PROJECT_TAKES names more, the guide and a walker's notes, and the index the search builds of them. So
    a test's own search reads only what the test changes. versioned puts the copy under version control, its files
    committed and the search's index left out."""
    def copy(name, versioned=False):
        read = shared_folder / "read"
        if not read.is_dir():
            made = Project("the project the file's tests share", canon=getattr(request.module, "SHARED_PROJECT_TAKES", True), root=shared_folder / "building")
            made.put("docs/notes.md", base("walkers-notes"))
            built = subprocess.run([sys.executable, "-B", "-c", BUILD_INDEX, str(TREE / LIB), str(made.root)], capture_output=True, text=True)
            if built.returncode:
                raise AssertionError("the search could not read the project made for the tests: " + built.stderr[-800:])
            made.root.rename(read)
        return Project.copied(read, versioned, left_out=(SEARCH_INDEX,))
    return copy


def retiring(text, phrase="north quay"):
    """-> a design's text retiring a phrase, its Retired Phrases where the form puts the section."""
    after = "\n## Design Log Entries" if "\n## Design Log Entries" in text else "\n## Out of Scope"
    return swap(text, after, "\n" + base("retired-phrases-of-one-phrase").replace("north quay", phrase) + after)


def searching_review(places=FERRY + "\n      - `docs/notes.md`"):
    """-> a review's report whose reviewer recorded a Search by terms, giving every place, with the places given."""
    text = a_report("review")
    text = swap(text, "    **Kind:** meaning \\\n    **Query:** In winter the ferry makes fewer crossings than in summer. \\\n    **Ranking Part:** 1 to 20 \\\n", "    **Kind:** terms \\\n    **Query:** north quay \\\n")
    return swap(text, "    **Snapshot:** 0123456789abcdef \\\n    **Places:**\n      - " + FERRY, "    **Snapshot:** 0123456789abcdef \\\n    **Places:**\n      - " + places)


SEARCH_GIVES = "Search reviewer-1-winter-hours gives %s, which its Places do not cover"


def whole_research(query="north quay", narrowed="", target="", by_meaning_narrowed=""):
    """-> a research report naming its goal in a Search by meaning and in one by terms, which the search runs: the one
    by terms asking the query given, each holding the Narrowed To given it, and, target given, each naming that
    target."""
    named = "    **Target:** %s \\\n" % target if target else ""
    by_terms = swap(swap(base("search-by-terms-for-the-quay"), "**Query:** north quay", "**Query:** " + query), "    **Snapshot:**", named + narrowed + "    **Snapshot:**")
    by_meaning = swap(a_report("research"), "    **Snapshot:**", named + by_meaning_narrowed + "    **Snapshot:**")
    return swap(by_meaning, "\n\n## Read Assessments", "\n\n" + by_terms + "\n## Read Assessments")
