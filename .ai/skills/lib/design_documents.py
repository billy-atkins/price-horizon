#!/usr/bin/env python3
"""The design document tooling the skills writing design documents share: the validation review, which holds a
design document to its form, its references within, the lineage from research to its steps and each construct a
step's Draft holds, through the construct checks in constructs.py, before the apply, drawing only on the document, the
reports of the handed-off judgments its log names that read_entries gives, the canon's declarations of its form and,
for a Draft's constructs, the specs as they stand, and stamps a design that passes; and the builder's tools, which
append a design's log entries, check a design's own names and free it of each finished or gone design it names, check the headings a proposal cites, a Target against its Kind and the constructs a
file in scope states, through the same checks, for its self-review at the apply, show and check the wording a design
retires, list the files changed outside
its Target, check the work against the specs' and the code's script checks in spec_checks.py and code_checks.py, check
the workstack, show a design's header and goals, show a validation, list the parts of a design naming one of its
parts, write citations' links, run the kept tests of each script a set of changed files holds a file of, with the
design script's own comparison of the designs a change reads differently, and show what a
Refactor and Refine cycle changed. A check's entry is appended only once its report, in the design's folder, holds the
form working-files/main.md § A Check's Report gives it and its records cover what § A Check's Report § What the Design
Script Checks has the design script check of them, its counts taken from it; a reviewer's part of a review's report, and a handed-off judgment's report, is
checked by the same units before it is taken in.

A design document must hold the form working-files/main.md sets, and the workstack its lineage draws must hold
together. Its actions are flags per specs/methodology/skills/authoring-a-skill.md § Authoring a Skill. The exit status is 0 when
every check passes, 1 when one finds a problem, and 2 for a usage error.

Standard library only, git aside, which --show-refactor-and-refine-of-existing-specs and --check-work read through, and run by
no agent directly: each skill writing design documents calls main from its own entry script with its own plans
folder, per specs/methodology/skills/authoring-a-skill.md § Authoring a Skill.
"""

import argparse
import bisect
import collections
import contextlib
import datetime
import hashlib
import io
import json
import os
import re
import subprocess
import sys
from pathlib import Path, PurePosixPath

import citation_links
import constructs
import layout
import reading
import record_types
from spec_text import REGISTRY, lineages, parse_citation, read, registry, scope_paths, sections, skill_dirs, spec_texts
from spec_text import CommitTree, indexed, strip_fences, tracked
from spec_text import resolve as resolve_citation


# @canon-spec specs/methodology/working-files/main.md § A Design Document § The Kinds of Change
KINDS = ("canon-specs", "application-specs", "code", "documentation", "other")
KIND_LIST = ", ".join(KINDS[:-1]) + " or " + KINDS[-1]
# @canon-spec specs/methodology/design-workflow/designs-reviews.md § A Design's Reviews
# the Sub-scopes of the Sub-scopes table, the one copy the audit's script and the log's check both read
SUB_SCOPES = ("core-canon", "skills", "application-specs", "documentation", "other")
# working-files/main.md § A Design Document and § Steering Decision
PLANS = ".ai/plans/design-specs"  # set by the entry script calling main
# @canon-spec specs/methodology/working-files/main.md § A Design Document
CODE_PLANS = "implement-specs"  # the plans folder of the designs changing code, whose kind is code
# @canon-spec specs/methodology/working-files/main.md § A Design Document
FIELDS = ("Name", "Version", "Status", "Source", "Kind", "Target", "Spawned By", "Depends On Designs", "Validated")
# @canon-spec specs/methodology/working-files/main.md § A Design Document § The Design's Version
# a design holding no version is read as 0.1.0, the version's default, left out
UNVERSIONED = tuple(f for f in FIELDS if f != "Version")
# @canon-spec specs/methodology/working-files/main.md § A Design Document
# the one field naming the designs a design depends on
DEPENDS_ON = "Depends On Designs"
# working-files/main.md § A Stamp: a UTC timestamp and a content hash; a design document's
# Validated stamp leaves out the Validated and Status fields.
STAMP = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z sha256:[0-9a-f]{16}$")
# @canon-spec specs/methodology/working-files/main.md § A Stamp
TIMESTAMP = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$")
# @canon-spec specs/methodology/working-files/main.md § A Design Document
# @canon-spec specs/methodology/working-files/main.md § A Stamp
UNSTAMPED = ("Validated", "Status")
# @canon-spec specs/methodology/working-files/main.md § A Design Document
LOG = "Design Log Entries"
# @canon-spec specs/methodology/working-files/main.md § A Stamp
UNSTAMPED_SECTIONS = (LOG,)  # an entry appended after the stamp leaves it current
# @canon-spec specs/methodology/working-files/main.md § A Design Document
IMPACT = "Impact on the Application Specs"  # a canon design's, and no other design's
# @canon-spec specs/methodology/working-files/main.md § A Design Document
RETIRED = "Retired Phrases"
# @canon-spec specs/methodology/working-files/main.md § A Design Document
SECTIONS = ("The Problem", "Design Goals", "The Design Frame", "Steering Decisions", "Design Plan Steps", RETIRED, IMPACT, LOG, "Out of Scope")
# @canon-spec specs/methodology/working-files/main.md § A Design Document
# the log is required once its first entry is appended, so a design with none holds no section
OPTIONAL = ("Steering Decisions", RETIRED, LOG)
# @canon-spec specs/methodology/working-files/main.md § A Design Document
# the goals, required as the frame is, but in a design complete or abandoned
UNTIL_FINISHED = ("Design Goals",)
# @canon-spec specs/methodology/working-files/main.md § A Design Document
# the design frame's level-three headings, in order, and the text a part not yet stated holds, which no design
# approved or further holds; two of them record sections
FRAME = ("Scope", "Assessed Areas", "Approach", "Frame Outcomes")
AREAS, OUTCOMES = "Assessed Areas", "Frame Outcomes"
# @canon-spec specs/methodology/working-files/main.md § A Design Document § Approach Principle
# @canon-spec specs/methodology/working-files/main.md § A Design Document § Scope Case
# the Scope's cases and the Approach's principles, each by its frame part, its field, its label and its own type's
# Plural Name
FRAME_RECORDS = (("Scope", "Cases", "a case", "Scope Cases"), ("Approach", "Principles", "a principle", "Approach Principles"))
# @canon-spec specs/methodology/working-files/main.md § A Design Document § Frame Part
# the types extending the Frame Part, each part named and resting on goals
FRAME_PART_TYPES = ("Frame Outcomes", "Scope Cases", "Approach Principles")
NOT_YET_STATED = "Not yet stated."
# @canon-spec specs/methodology/working-files/main.md § A Design Document
# the text a step section holds until drafting states the steps, which no design approved or further holds
NOT_YET_DRAFTED = "Not yet drafted."
# @canon-spec specs/methodology/working-files/main.md § Steering Decision
# where the Steering Decision type is declared: its fields and its Type's values are read from that declaration,
# this tooling holding no copy of them
STEER_HOME = ("specs/methodology/working-files/main.md", "Steering Decision")
# @canon-spec specs/methodology/working-files/main.md § Design Goal
GOAL_HOME = ("specs/methodology/working-files/main.md", "Design Goal")
# @canon-spec specs/methodology/working-files/main.md § Design Plan Step
STEP_HOME = ("specs/methodology/working-files/main.md", "Design Plan Step")
# @canon-spec specs/methodology/working-files/main.md § Design Log Entry
LOG_HOME = ("specs/methodology/working-files/main.md", "Design Log Entry")
# @canon-spec specs/methodology/working-files/main.md § Retired Phrase
RETIRED_HOME = ("specs/methodology/working-files/main.md", "Retired Phrase")
# @canon-spec specs/methodology/working-files/main.md § A Design Document § Assessed Area
AREA_HOME = ("specs/methodology/working-files/main.md", "A Design Document § Assessed Area")
# @canon-spec specs/methodology/working-files/main.md § A Design Document § Frame Outcome
OUTCOME_HOME = ("specs/methodology/working-files/main.md", "A Design Document § Frame Outcome")
# @canon-spec specs/methodology/working-files/main.md § A Design Document § Scope Case
CASE_HOME = ("specs/methodology/working-files/main.md", "A Design Document § Scope Case")
# @canon-spec specs/methodology/working-files/main.md § A Design Document § Approach Principle
PRINCIPLE_HOME = ("specs/methodology/working-files/main.md", "A Design Document § Approach Principle")
# @canon-spec specs/methodology/working-files/main.md § Design Plan Step § Step Objective
OBJECTIVE_HOME = ("specs/methodology/working-files/main.md", "Design Plan Step § Step Objective")
# @canon-spec specs/methodology/working-files/main.md § A Check's Report § Read Assessment
ASSESSMENT_HOME = ("specs/methodology/working-files/main.md", "A Check's Report § Read Assessment")
# @canon-spec specs/methodology/working-files/main.md § A Check's Report § Read Assessment § Read Assessment Impacts
IMPACTS_HOME = ("specs/methodology/working-files/main.md", "A Check's Report § Read Assessment § Read Assessment Impacts")


def declaration(home, root=None):
    """-> (the text of the section declaring a type, or None, and the file's path): a level-two section whole, or a
    section beneath one, named by its lineage, its own text, to its next heading."""
    path, title = home
    # the checkout's root: the one given, or the nearest directory at or above where the script is run that holds the
    # declaration's file, so a form is read from the checkout the script is run in, whichever checkout holds this file
    base = Path(root) if root else next((p for p in (Path.cwd(), *Path.cwd().parents) if (p / path).exists()), Path.cwd())
    if not (base / path).exists():
        return None, path
    text = read((base / path)).replace("\r\n", "\n")
    if " § " not in title:
        return section(text, title) or "", path
    found = sections(text).get(title)
    return ("\n".join(text.split("\n")[found[0] + 1:found[1]]) if found else ""), path


# @canon-spec specs/methodology/modeling-constructs.md § Constructs § Record Form
def declared_type(home, plural, root=None, key="Name"):
    """A record type as its declaration gives it -> (its table of record fields, a row to a field, its base's first
    where it extends one, problems with the declaration: no Record Form, a Plural Name other than the one a design's
    record section takes, a Reference Key other than the one given, its own or its base's, or no table of record
    fields, its own or its base's)."""
    title = home[1]
    body, path = declaration(home, root)
    if body is None:
        return [], [(path, "no file declares the %s type" % title)]
    lines = [re.sub(r"\s*\\$", "", l).strip() for l in body.split("\n")]
    problems = [] if "**Construct:** `specs/methodology/modeling-constructs.md § Constructs § Record Form`" in lines \
        else ["no Record Form declares the %s type" % title]
    if plural and "**Plural Name:** " + plural not in lines:
        problems.append("the %s type declares no Plural Name %s, the title a design's record section takes" % (title, plural))
    # a type extending another takes its base's fields first, and its base's Reference Key
    extends = next((re.search(r"`§ ([^`]+)`", l) for l in lines if l.startswith("**Extends:** ")), None)
    base, base_problems = declared_type((home[0], extends.group(1)), None, root, key=key) if extends else ([], [])
    if not extends and "**Reference Key:** " + key not in lines:
        problems.append("the %s type declares no Reference Key %s" % (title, key))
    head = next((i for i, l in enumerate(lines) if l.startswith("| Field | Unique | Required | Default Value | Values |")), None)
    rows = []
    for l in lines[head + 2:] if head is not None else []:
        if not l.startswith("|"):
            break
        rows.append([c.strip() for c in l.strip("|").split("|")])
    if not rows and not base:
        problems.append("the %s type gives no table of its record fields" % title)
    return base + rows, base_problems + [(path, p) for p in problems]


def steer_type(root=None):
    """The Steering Decision type as its declaration gives it -> (its fields in order, the fields it requires always,
    {field: its quoted values} for each field giving them, problems with the declaration)."""
    rows, problems = declared_type(STEER_HOME, "Steering Decisions", root)
    values = {row[0]: tuple(re.findall(r'"([^"]+)"', row[4])) for row in rows if len(row) > 4 and '"' in row[4]}
    return tuple(row[0] for row in rows), tuple(row[0] for row in rows if len(row) > 2 and row[2] == "yes"), values, problems


# @canon-spec specs/methodology/working-files/main.md § Steering Decision
# the field a Steering Decision holds where a `steer` entry names it, and its values naming the goals or a part of the
# frame, a steer changing one of them material (specs/AGENTS.md § Design, Refactor, Refine § Measure Twice, Cut Once
# § The Order of a Design's Parts)
CHANGES = "Changes"
# @canon-spec specs/methodology/working-files/main.md § Steering Decision § A Steer's Type
# the old names of a steer's types, each read as the type it was renamed
OLD_STEER_TYPES = {"selection": "agreement", "perspective": "directive"}
MATERIAL = ("the goals", "the Scope", "the Assessed Areas", "the Approach", "the Frame Outcomes")
# the value of Changes for a steer approving an item of the design's Out of Scope as it is written
OUT_OF_SCOPE_ITEM = "Out of Scope item"


def steer_changes(text):
    """-> {Name: Changes} of each Steering Decision a design holds, an empty Changes where it holds none."""
    return {dict(r).get("Name", "").strip(): dict(r).get(CHANGES, "").strip()
            for r in records(section(text, "Steering Decisions")) or []}


def changes_parts(value):
    """-> the parts a Steering Decision's Changes names: its list's items, a single value a list of one."""
    return [p.strip() for p in str(value or "").split("\n") if p.strip()]


def set_names(entry):
    """-> the Names of the Steering Decisions a `steer` entry names, the set it marks, separated by semicolons."""
    return [n.strip().strip("`") for n in entry[2].get("Steering Decision", "").split(";") if n.strip()]


def material(entry, changes):
    """Whether a log entry, (kind, count, {field: value}), is a `steer` entry marking a set whose highest part, by
    changes as steer_changes gives them, is the goals or a part of the frame: one of its Steering Decisions' Changes
    names one."""
    return entry[0] == "steer" and any(p in MATERIAL for n in set_names(entry) for p in changes_parts(changes.get(n)))


# @canon-spec specs/methodology/working-files/main.md § A Design Document § The Design's Version
VERSION = re.compile(r"^(\d+)\.(\d+)\.(\d+)$")
# a design starts in initial development, at 0.1.0, the version's default, left out in the header and on an entry; the
# user's agreement to its goals raises it to 1.0.0
FIRST_VERSION = (0, 1, 0)
AGREED_VERSION = (1, 0, 0)
# the entry the user's agreement to the goals appends
GOALS_AGREED = "goals-agreed"


def parse_version(value):
    """-> a version written major.minor.revision as a tuple of its counters, or None where it is not one."""
    m = VERSION.match((value or "").strip())
    return tuple(int(x) for x in m.groups()) if m else None


def version_text(version):
    return "%d.%d.%d" % version


# @canon-spec specs/methodology/working-files/main.md § Design Log Entry
# the entry recording a design reassessment, and the old entry an earlier log holds in its place
DESIGN_REASSESSMENT, OLD_REASSESSMENT = "design-reassessment", "reassessment"
# @canon-spec specs/methodology/working-files/main.md § Design Log Entry
# the Cause a `design-reassessment` entry holds: the word opening each of its two forms, what a changed foundation says
# of each design the design was freed from, what brings a design to the step back, and the fields the entry holds
# only where its Cause is a step back
CAUSE = "Cause"
CHANGED_FOUNDATION, STEP_BACK = "changed foundation", "step back"
FINISHED_NAME, GONE_NAME = "finished", "gone"
STEP_BACK_CAUSES = ("a run of flaws", "a run of send-backs", "passes that did not converge", "the user's word")
STEP_BACK_FIELDS = ("Decision", "Diagnosis")


# @canon-spec specs/methodology/working-files/main.md § Design Log Entry
def read_cause(value):
    """-> a `design-reassessment` entry's Cause as (the word opening its form, what it holds): for a changed
    foundation, [(design, `finished` or `gone`)], each design the design was freed from; for a step back, what brought
    the design to it; or None where the value holds neither form."""
    form, _, held = value.partition(":")
    form, held = form.strip(), held.strip()
    if form == STEP_BACK:
        return (STEP_BACK, held) if held in STEP_BACK_CAUSES else None
    if form == CHANGED_FOUNDATION:
        freed = [re.fullmatch(r"(\S+) (%s|%s)" % (FINISHED_NAME, GONE_NAME), item.strip()) for item in held.split(";")]
        return (CHANGED_FOUNDATION, [(m.group(1).strip("`"), m.group(2)) for m in freed]) if all(freed) else None
    return None


# @canon-spec specs/methodology/working-files/main.md § Design Log Entry
def cause_fields(fields, given):
    """-> the fields a `design-reassessment` entry holding fields, {field: value}, takes of those its kind gives, by
    its Cause: its Cause alone for a changed foundation; every field for a step back; and, for an entry holding no
    Cause, appended before the entry held one and read as one chosen at the step back, every field but the Cause."""
    if CAUSE not in fields:
        return tuple(k for k in given if k != CAUSE)
    cause = read_cause(fields[CAUSE])
    if cause is not None and cause[0] == CHANGED_FOUNDATION:
        return tuple(k for k in given if k not in STEP_BACK_FIELDS)
    return tuple(given)


# @canon-spec specs/methodology/design-workflow/order-of-a-designs-work.md § The Order of a Design's Work § Facts
# the entry reason's values for a send-back, a blocked design's, the step back's and an old log's among them, and its
# value for a design freed while it is approved or applying, which the freeing alone writes
SENT_BACK = ("sent back", "sent back for a dependency", "sent back to the step back", "sent back to reassess")
FREED = "freed"


# @canon-spec specs/methodology/working-files/main.md § A Design Document § The Design's Version
def starts_major(entry):
    """Whether a log entry, (kind, count, {field: value}), starts a major version: a `design-reassessment` entry, or an
    old log's `reassessment` entry, read as one, deciding other than `go on`."""
    return entry[0] == DESIGN_REASSESSMENT or (entry[0] == OLD_REASSESSMENT and entry[2].get("Decision", "").strip() != "go on")


# @canon-spec specs/methodology/working-files/main.md § A Design Document § The Design's Version
def raised(version, entry, changes):
    """-> the version after a log entry raises it, the counter its part of the design gives raised and each counter
    after it cleared: in initial development, the major 0, a goals-agreed entry raises the version to 1.0.0 and a
    design reassessment nothing, a design with no report having nothing to make afresh; after it, one starting a
    major version raises the major and a goals-agreed entry nothing; a steer marking a set material by changes raises the
    minor, once for the set, a plan-change the revision, and any other entry nothing."""
    major, minor, revision = version
    if starts_major(entry):
        return (major + 1, 0, 0) if major else version
    if entry[0] == GOALS_AGREED:
        return version if major else AGREED_VERSION
    if material(entry, changes):
        return major, minor + 1, 0
    if entry[0] == "plan-change":
        return major, minor, revision + 1
    return version


def versions(entries, changes):
    """-> the design's version after each of its log entries, worked out by the entries raising it in the order they
    stand, from 0.1.0."""
    out, version = [], FIRST_VERSION
    for e in entries:
        version = raised(version, e, changes)
        out.append(version)
    return out


def design_version(entries, changes):
    """-> the design's version its log gives, 0.1.0 for a log holding no entry."""
    return (versions(entries, changes) or [FIRST_VERSION])[-1]


# @canon-spec specs/methodology/working-files/main.md § Design Log Entry
def entry_version(entry):
    """-> the version an entry is stamped at, its Design Version, or 0.1.0, the default, where it holds none: the
    version of the design its work read, a check's taken from its report, and any other's the version as it was
    appended."""
    return parse_version(entry[2].get(VERSIONED, "")) or FIRST_VERSION


# @canon-spec specs/methodology/working-files/main.md § A Check's Report § Over Applied Work, and a Phase's Record
def major_starts(entries):
    """-> the indexes of the entries raising the major as a design reassessment: each entry starts_major gives with a
    `goals-agreed` entry before it, a design reassessment in initial development raising nothing."""
    out, agreed = [], False
    for i, e in enumerate(entries):
        agreed = agreed or e[0] == GOALS_AGREED
        if starts_major(e) and agreed:
            out.append(i)
    return out


# @canon-spec specs/methodology/working-files/main.md § A Check's Report § Over Applied Work, and a Phase's Record
def major_start(entries):
    """-> where the design's current major version starts among its log entries: after its last design reassessment
    raising the major, or at the log's start."""
    return max([i + 1 for i in major_starts(entries)], default=0)


def current_major(entries):
    """-> the major of the version the log gives, which no steer or plan-change raises: 0 in initial development, 1
    from the first goals-agreed entry, raised once by each design reassessment raising the major."""
    return (1 if any(e[0] == GOALS_AGREED for e in entries) else 0) + len(major_starts(entries))


# @canon-spec specs/methodology/working-files/main.md § A Check's Report § Over Applied Work, and a Phase's Record
def of_current_major(entries):
    """-> the indexes of the log entries of the design's current major version, by the major of the version each is
    stamped at, so research handed off before a design reassessment and handed back after it is of the major version it read."""
    major = current_major(entries)
    return [i for i, e in enumerate(entries) if entry_version(e)[0] == major]


# @canon-spec specs/methodology/working-files/main.md § A Check's Report § Over Applied Work, and a Phase's Record
def cut_short(entries):
    """-> the (kind, count) of each check a `reassessment` entry's or a `steer` entry's Cuts Short names, separated by
    semicolons: a check a reassessment on the user's word, or the user's call at a set's close, cut short, whose report
    binds nothing."""
    out = set()
    for k, _, f in entries:
        if k not in ("reassessment", "steer"):
            continue
        for named_ in f.get("Cuts Short", "").split(";"):
            m = re.fullmatch(r"([a-z-]+?)-(\d+)", named_.strip().strip("`"))
            if m:
                out.add((m.group(1), int(m.group(2))))
    return out


def binding(entries, design=None):
    """-> the indexes of the log entries whose reports may bind the design, by the two questions of § Over Applied Work,
    and a Phase's Record a report's place and its own statement answer: of the current major version, and not cut
    short, read from the report's Ending where the design is given and the report states one, else from an old log's
    Cuts Short. Without the design, as for the stamp's hash, the Cuts Short alone is read, so a cut-short report's
    entry stamped there only makes the stamp go stale sooner."""
    cut = cut_short(entries)

    def stopped(i):
        k, n, _ = entries[i]
        if design is not None and owes_ending(k):
            path = report_file(design, k, n)
            ending = report_ending(read_report(read(path))) if path.is_file() else None
            if ending is not None:
                return ending == CUT_SHORT
        return (k, n) in cut
    return [i for i in of_current_major(entries) if not stopped(i)]


# the script checks of the log the design script carries out, by the rules naming them
GOALS_AGREED_RULE = "specs/methodology/working-files/main.md § Design Log Entry § Script Checks [Name: goals-agreed-before-checks]"
ENTRY_AT_VERSION_READ = "specs/methodology/working-files/main.md § Design Log Entry § Script Checks [Name: entry-at-the-version-read]"


# @canon-spec specs/methodology/working-files/main.md § Design Log Entry § Script Checks [Name: goals-agreed-before-checks]
def agreed_before(entries, i, read=None):
    """Whether a `goals-agreed` entry of a major version stands before the entry at index i. Given read, the version a
    check's work read, the major version is that version's, wherever the entry stands in the log: the entries from the
    design reassessment starting it, or from the log's start, to the one starting the next, so a check's entry appended
    after a design reassessment, at the earlier version its report read, is held to that version's agreement, and one
    whose own major version holds none is refused. With no read, the major version is the one the entry stands in:
    after the last design reassessment raising the major before it, or from the log's start."""
    starts = major_starts(entries[:i])
    if read is None:
        return any(e[0] == GOALS_AGREED for e in entries[max([s + 1 for s in starts], default=0):i])
    major = read[0]
    if not 1 <= major <= len(starts) + 1:
        return False
    start = starts[major - 2] + 1 if major > 1 else 0
    return any(e[0] == GOALS_AGREED for e in entries[start:starts[major - 1] if major <= len(starts) else i])


# @canon-spec specs/methodology/working-files/main.md § Design Log Entry § Script Checks [Name: goals-agreed-before-checks]
def gate_problems(entries, checks):
    """-> problems with the log's order over the whole log: each check's entry, one of the kinds in checks, with no
    `goals-agreed` entry before it in its major version, the one of the Design Version it is stamped at, or, where it
    holds none, the one it stands in, so no report is of major version 0 and the goals come before the research they
    direct."""
    return ["log entry %s-%d is a check's entry with no goals-agreed entry before it in its major version (%s)"
            % (k, n, GOALS_AGREED_RULE) for i, (k, n, f) in enumerate(entries)
            if k in checks and not agreed_before(entries, i, entry_version(entries[i]) if VERSIONED in f else None)]


def goal_type(root=None):
    """The Design Goal type as its declaration gives it -> (its fields in order, problems with the declaration)."""
    rows, problems = declared_type(GOAL_HOME, "Design Goals", root)
    return tuple(row[0] for row in rows), problems


def log_type(root=None):
    """The Design Log Entry type as its declaration gives it -> ({field: its quoted values, or () for any text},
    {field: whether it holds a count}, {kind: its fields beside Entry and Timestamp, in the type's order}, problems
    with the declaration). A count's Holds opens "the count"."""
    rows, problems = declared_type(LOG_HOME, LOG, root, key="Entry")
    values = {row[0]: tuple(re.findall(r'"([^"]+)"', row[4])) for row in rows if len(row) > 5}
    counts = {row[0]: row[5].startswith("the count") for row in rows if len(row) > 5}
    body = declaration(LOG_HOME, root)[0] or ""
    kinds, table = {}, body.split("**Reference Key:** Kind", 1)
    for line in (table[1].split("\n") if len(table) > 1 else []):
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if line.startswith("| `") and len(cells) == 4:
            given = [] if cells[1] == "none" else [f.strip() for f in cells[1].split(",")]
            kinds[cells[0].strip("`")] = tuple(f for f in values if f in given)
    if not kinds:
        problems.append((LOG_HOME[0], "the Design Log Entry type gives no table of its kinds"))
    return values, counts, kinds, problems


# @canon-spec specs/methodology/working-files/main.md § Design Log Entry
# the field an entry holds its design's version in, right after its Timestamp, stamped by --log-entry
VERSIONED = "Design Version"


def optional_entry_fields(root=None):
    """-> the Design Log Entry type's fields it requires of no entry, its Required `no`, each held only where it is
    given, Design Version and Cuts Short among them."""
    rows, _ = declared_type(LOG_HOME, LOG, root, key="Entry")
    return tuple(row[0] for row in rows if len(row) > 2 and row[2] == "no")


def retired_type(root=None):
    """The Retired Phrase type as its declaration gives it -> (its fields in order, the fields it requires,
    problems with the declaration)."""
    rows, problems = declared_type(RETIRED_HOME, RETIRED, root, key="Phrase")
    return tuple(row[0] for row in rows), tuple(row[0] for row in rows if len(row) > 2 and row[2] == "yes"), problems


# the record types of a design's frame, of its steps and of a step's Objectives, and of a report's Read Assessments, each
# by its home, its Plural Name and its Reference Key, read from its declaration as the others are
PLAN_TYPES = {AREAS: (AREA_HOME, "Area"), OUTCOMES: (OUTCOME_HOME, "Name"), "Scope Cases": (CASE_HOME, "Name"),
              "Approach Principles": (PRINCIPLE_HOME, "Name"), "Design Plan Steps": (STEP_HOME, "Name"),
              "Step Objectives": (OBJECTIVE_HOME, "Name"), "Read Assessments": (ASSESSMENT_HOME, "Area")}


def plan_type(plural, root=None):
    """One of PLAN_TYPES as its declaration gives it -> (its fields in order, the fields it requires, problems with the
    declaration)."""
    home, key = PLAN_TYPES[plural]
    rows, problems = declared_type(home, plural, root, key=key)
    return tuple(row[0] for row in rows), tuple(row[0] for row in rows if len(row) > 2 and row[2] == "yes"), problems


def impact_members(root=None):
    """-> the members of § A Check's Report § Read Assessment § Read Assessment Impacts, the rows of its table keyed by
    Impact, in order, and problems with the declaration."""
    body, path = declaration(IMPACTS_HOME, root)
    lines = (body or "").split("\n")
    head = next((i for i, l in enumerate(lines) if l.startswith("| Impact |")), None)
    members = []
    for l in lines[head + 2:] if head is not None else []:
        if not l.startswith("|"):
            break
        members.append(l.strip().strip("|").split("|")[0].strip().strip("`"))
    return tuple(members), [] if members else [(path, "no table gives the members of Read Assessment Impacts")]


# a record's own fields, a design's header and every field's value are read through the one reader of a block of
# fields, record_types.read_block, wherever the form indents them (modeling-constructs.md § Fields)


def field_of(body, key):
    """-> a section's field key as the one reader gives it, wherever the form indents the key, or None where the
    section has no such field (modeling-constructs.md § Fields)."""
    if body is None:
        return None
    lines = body.split("\n")
    i = next((i for i, l in enumerate(lines) if record_types.opens_key(l) and record_types.opens_key(l)["key"] == key), None)
    if i is None:
        return None
    fields, _ = record_types.read_block(lines, i, record_types._indent(lines[i]), len(lines))
    return next((f for f in fields if f["key"] == key), None)


def records_read(body, key="Records"):
    """-> the items of a section's Records field, or of its field key holding records, as the one reader gives them,
    wherever the form indents the key, or None where the section has no such field (modeling-constructs.md § Fields)."""
    field = field_of(body, key)
    return list(field["items"] or []) if field is not None else None


def records(body):
    """-> each record of a record section as [(field, value)], or None where it has no Records field; an item opening
    no field is a record of no fields."""
    items = records_read(body)
    if items is None:
        return None
    return [[(f["key"], str(record_types.value_of(f))) for f in it["fields"]] if it["fields"] is not None else [] for it in items]


# @canon-spec specs/methodology/working-files/main.md § A Design Document § The States It Moves Through
STATES = ("not-started", "in-progress", "approved", "applying", "complete", "abandoned")
# @canon-spec specs/methodology/working-files/main.md § A Design Document § What Blocks What
# the states a design finishes in
FINISHED = ("complete", "abandoned")
KEY = r"\*\*([A-Z][A-Za-z ]*):\*\*"


def read_design(f):
    """-> (file name, [(key, value)], [level-two heading], text) for one design document;
    its fields are read from the Design Document section, before its first level-two heading, as one block of fields
    through the one reader, each under the key it is written with."""
    text = read(f).replace("\r\n", "\n")
    head = text.split("\n## ", 1)[0].split("\n")
    i = next((i for i, l in enumerate(head) if record_types.opens_key(l) and not record_types._indent(l)), None)
    fields = []
    if i is not None:
        block, _ = record_types.read_block(head, i, 0, len(head))
        fields = [(f["key"], " ".join(str(record_types.value_of(f)).split())) for f in block]
    return f.stem, fields, [title for title, _ in level_two(text)], text


def is_design(f):
    return read(f).lstrip("\ufeff").startswith("# Design Document")


# @canon-spec specs/methodology/working-files/main.md § A Design Document § What Blocks What
def is_plans_folder(folder):
    """Whether a directory is a plans folder, a skill's plans directory, `.ai/plans/<skill-name>/`, there yet or not."""
    folder = Path(folder).resolve()
    return folder.parent.name == "plans" and folder.parent.parent.name == ".ai"


# @canon-spec specs/methodology/working-files/main.md § A Design Document § What Blocks What
def read_designs(folder):
    """-> every design of the workstack, each standing in a plans folder, its file directly in it: those in folder,
    named by file name, and those in each other skill's plans folder beside it, named by that folder's name, a slash
    and the file name, their Spawned By and Depends On Designs named the same way, per working-files/main.md § A
    Design Document; none where folder is no plans folder, so a design standing anywhere else, in an archive beneath
    a plans folder among them, is read as no design of the workstack, whatever folder an action is run from."""
    folder = Path(folder).resolve()
    if not is_plans_folder(folder):
        return []
    out = [read_design(f) for f in sorted(folder.glob("*.md")) if is_design(f)] if folder.is_dir() else []
    for other in sorted(p for p in folder.parent.iterdir() if p.is_dir() and p != folder):
        for f in sorted(other.glob("*.md")):
            if not is_design(f):
                continue
            name, fields, sections, text = read_design(f)
            fields = [(k, rename(v, other.name, folder.name)) if k in ("Spawned By", DEPENDS_ON) else (k, v) for k, v in fields]
            out.append((other.name + "/" + name, fields, sections, text))
    return out


def rename(value, own, base):
    """A list of design names as a design in folder own writes it, named as one in folder base reads them."""
    out = []
    for d in named(value):
        full = d if "/" in d else own + "/" + d
        out.append(full.split("/", 1)[1] if full.startswith(base + "/") else full)
    return "; ".join(out) or "none"


def named(value):
    """-> the design documents a Spawned By or Depends On Designs value names; none for none."""
    if value.strip().lower() in ("", "none"):
        return []
    return [n.strip().strip("`") for n in value.split(";") if n.strip()]


BLOCKS_RULE = "specs/methodology/working-files/main.md § A Design Document § What Blocks What"
# @canon-spec specs/methodology/working-files/main.md § A Design Document § What Blocks What
# what a name of a design standing unfinished in a plans folder is read as, beside FINISHED_NAME and GONE_NAME; the
# kinds of entry that begin or continue work past a design's frame; and what is said of a design standing in no plans
# folder
UNFINISHED_NAME = "unfinished"
PAST_THE_FRAME = ("plan-change", "design-refactor-refine", "self-review", "another-round", "plan-approval", "step-back", "apply")
NO_PLANS_FOLDER = "it stands in no plans folder, so it is read as no design of the workstack and written by no action (%s)" % BLOCKS_RULE


# @canon-spec specs/methodology/working-files/main.md § A Design Document § What Blocks What
def read_name(designs, name):
    """-> what a name in a Depends On Designs means, read from the designs of the plans folders as they stand,
    {name: {field: value}} as read_designs names them: GONE_NAME where no design of that name stands in a plans
    folder, FINISHED_NAME where one stands there complete or abandoned, and UNFINISHED_NAME where one stands there in
    any other Status."""
    if name not in designs:
        return GONE_NAME
    return FINISHED_NAME if designs[name].get("Status", "") in FINISHED else UNFINISHED_NAME


# @canon-spec specs/methodology/working-files/main.md § A Design Document § What Blocks What
def own_names(design):
    """-> [(name, what it means)] for each design the Depends On Designs of the design at this path names, each read
    by read_name from the plans folders as they stand, in the order the field holds them; or None where the design
    stands in no plans folder."""
    folder = Path(design).resolve().parent
    if not is_plans_folder(folder):
        return None
    designs = {name: dict(fields) for name, fields, _, _ in read_designs(folder)}
    held = rename(dict(read_design(Path(design))[1]).get(DEPENDS_ON, ""), folder.name, folder.name)
    return [(d, read_name(designs, d)) for d in named(held)]


# @canon-spec specs/methodology/working-files/main.md § A Design Document § What Blocks What
def held_back(design, kind):
    """-> why --log-entry appends no entry of kind to the design at this path, by where it stands and what its Depends
    On Designs names, or [] where the entry may be appended: a design in no plans folder is written by no action; one
    naming a finished or gone design takes no entry until it is freed; and one naming an unfinished design takes no
    entry that begins or continues work past its frame. A complete or an abandoned design's names are its history,
    and hold nothing back."""
    names = own_names(design)
    if names is None:
        return [NO_PLANS_FOLDER]
    if dict(read_design(Path(design))[1]).get("Status", "") in FINISHED:
        return []
    changed = ["%s, %s" % (d, r) for d, r in names if r != UNFINISHED_NAME]
    if changed:
        return ["its Depends On Designs names %s: its foundation has changed, and no entry is appended to its log until "
                "--free-design frees it (%s)" % ("; ".join(changed), BLOCKS_RULE)]
    blocking = [d for d, r in names if r == UNFINISHED_NAME]
    if blocking and kind in PAST_THE_FRAME:
        return ["%s %s entry begins or continues work past the frame, and its Depends On Designs names %s, unfinished: a "
                "blocked design is worked no further than its agreed goals and frame (%s)"
                % ("an" if kind[0] in "aeiou" else "a", kind, "; ".join(blocking), BLOCKS_RULE)]
    return []


# @canon-spec specs/methodology/working-files/main.md § A Design Document § The Record's Checks
def read_entries(entries, changes, design=None):
    """-> the indexes, among a design's log entries as log_entries gives them, of each `handed-off-judgment` entry whose
    report the validation review reads: each binding it, of the design's current major version and not cut short, but one standing after the log's last `plan-approval` entry, where neither an `entered` entry nor
    a `steer` entry material by changes, as steer_changes gives them, follows that approval. So the validation reads
    the research binding the design, shared among agents by area or assessing an area again for a cause; research
    logged after the plan's approval, the frame frozen, leaves the validation as it stood; and a design sent back, or
    one whose goals or frame a set of steers changed after the approval, reads the research rebuilt for it."""
    approvals = [i for i, e in enumerate(entries) if e[0] == "plan-approval" and i >= major_start(entries)]
    last = approvals[-1] if approvals else None
    if last is not None and any(e[0] == "entered" or material(e, changes) for e in entries[last + 1:]):
        last = None
    return [i for i in binding(entries, design) if (last is None or i < last) and entries[i][0] == JUDGMENT]


# @canon-spec specs/methodology/working-files/main.md § A Stamp
def stamped_entry_lines(lines):
    """-> the 0-based lines of each log entry naming a report the validation review reads, which a design's stamp takes
    in, though it leaves out the rest of its Design Log Entries."""
    twos = level_two("\n".join(lines))
    head = next((n for title, n in twos if title == LOG), None)
    if head is None:
        return set()
    end = next((n for _, n in twos if n > head), len(lines))
    items = records_read("\n".join(lines[head + 1:end])) or []
    entries, spans = [], []
    for it in items:
        f = {x["key"]: str(record_types.value_of(x)).strip() for x in it["fields"] or []}
        m = re.fullmatch(r"([a-z-]+?)-(\d+)", f.get("Entry", ""))
        if m:
            entries.append((m.group(1), int(m.group(2)), f))
            spans.append(it["lines"])
    return {head + 1 + n for i in read_entries(entries, steer_changes("\n".join(lines))) for n in spans[i]}


def content_hash(text, leave_out=UNSTAMPED, leave_out_sections=UNSTAMPED_SECTIONS):
    """working-files/main.md § A Stamp: SHA-256 of the text as UTF-8, line endings a line feed,
    the lines holding the left-out fields dropped, and each left-out section, its heading through the next heading
    of its level, but for each log entry naming a report the validation review reads; its first 16 hexadecimal
    characters."""
    keys = "|".join(re.escape(k) for k in leave_out)
    raw = text.replace("\r\n", "\n").split("\n")
    kept = stamped_entry_lines(raw) if LOG in leave_out_sections else set()
    lines, dropping = [], False
    twos = {n: title for title, n in level_two("\n".join(raw))}
    for n, l in enumerate(raw):
        if n in twos:
            dropping = twos[n] in leave_out_sections
        if (not dropping or n in kept) and not re.match(r"\*\*(?:%s):\*\*" % keys, l):
            lines.append(l)
    return "sha256:" + hashlib.sha256("\n".join(lines).encode("utf-8")).hexdigest()[:16]


def stamp(text):
    """A stamp for the text as it stands: the UTC time to the second, and its content hash."""
    now = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    return now + " " + content_hash(text)


def validation(text, fields):
    """-> (state, stamped hash, current hash): whether a design's Validated stamp matches
    it as it stands, read rather than recorded: none, validated or stale."""
    value, current = dict(fields).get("Validated", ""), content_hash(text)
    if not STAMP.match(value):
        return "none", None, current
    stamped = value.split(" ")[1]
    return ("validated" if stamped == current else "stale"), stamped, current


# @canon-spec specs/methodology/spec-placement/kebab-case-conversion.md § Kebab-Case Conversion
def kebab(text):
    """The text in kebab-case, by the canon's one conversion: letters lowercased, an ampersand the word and, an
    apostrophe dropped, the letters a to z and the digits kept, each run of any other characters one hyphen, none
    leading or trailing."""
    text = text.lower().replace("&", " and ").replace("'", "").replace("’", "")
    return re.sub(r"[^a-z0-9]+", "-", text).strip("-")


def level_two(text):
    """-> [(title, the 0-based line of its heading)] for each level-two heading of a text, as the one reading gives a
    heading (reading.py), so a line of a fenced block is none."""
    return [(h.title, h.line - 1) for h in reading.headings(text) if h.level == 2]


def level_three(text):
    """-> [(title, the text beneath it, to the next level-three heading)] for each level-three heading of a text."""
    lines = text.split("\n")
    heads = [h.line - 1 for h in reading.headings(text) if h.level == 3]
    titles = [h.title for h in reading.headings(text) if h.level == 3]
    return [(title, "\n".join(lines[at + 1:heads[n + 1] if n + 1 < len(heads) else len(lines)])) for n, (title, at) in enumerate(zip(titles, heads))]


def part_span(text, title):
    """-> (the offset the level-two heading of that title starts at, the offset its part's text is read from) of the
    first such heading, or None. The part's text is read from the last line break before its first text, the blank
    lines beneath the heading set aside."""
    starts, at = [], 0
    for line in text.split("\n"):
        starts.append(at)
        at += len(line) + 1
    for found, n in level_two(text):
        if found == title:
            line_end = starts[n + 1] - 1 if n + 1 < len(starts) else len(text)
            after = line_end - (len(text[starts[n]:line_end]) - len(text[starts[n]:line_end].rstrip()))
            first = next((i for i in range(after, len(text)) if not text[i].isspace()), len(text))
            return starts[n], len(text) if first == len(text) else text.rfind("\n", after, first)
    return None


def section(text, title):
    """-> the text of the document's part under the level-two heading of that title, to the next level-two heading,
    or None where it holds none."""
    span = part_span(text, title)
    if span is None:
        return None
    lines, at = text.split("\n"), 0
    for n, line in enumerate(lines):
        if at > span[0] and any(n == k for _, k in level_two(text)):
            return text[span[1]:at]
        at += len(line) + 1
    return text[span[1]:]


# @canon-spec specs/methodology/working-files/main.md § A Design Document
def not_stated(body):
    """-> whether a frame part reads `Not yet stated.`."""
    if body is None:
        return False
    b = body.strip()
    return b == NOT_YET_STATED or scope_holding_sub_scopes_alone(b)


# @canon-spec specs/methodology/working-files/main.md § A Check's Report § What the Design Script Checks
def scope_holding_sub_scopes_alone(b):
    """-> whether a Scope written before research searched every durable file reads `Not yet stated.` with its
    Search Sub-scopes field alone after it, which is read as not yet stated."""
    rest = b[len(NOT_YET_STATED):].strip() if b.startswith(NOT_YET_STATED + "\n") else ""
    keys = re.findall(r"^\*\*([^*]+):\*\*", rest, re.M)
    return keys == [SEARCH_SUB_SCOPES] and field_of(rest, SEARCH_SUB_SCOPES) is not None


def frame_parts(text):
    """The design frame's parts, each heading with what it holds."""
    return {title: body.strip() for title, body in level_three(section(text, "The Design Frame") or "")}


def check_steers(body, logged=()):
    """-> problems with a Steering Decisions section: a Records field, and each record its type's fields in order,
    those it requires always present, Changes present where a `steer` entry names the record, by logged, and absent
    where none does, each field giving values holding one of them, no two sharing a Name."""
    items = records_read(body)
    if items is None:
        return ["Steering Decisions has no Records field"]
    if not items:
        return ["Steering Decisions holds no record"]
    problems, seen = [], set()
    fields, required, given, declared = steer_type()
    if not fields:
        return [p for _, p in declared] or ["the Steering Decision type declares no fields"]
    for it in items:
        keys = [f["key"] for f in record_types.record_fields(it)]
        if keys != [k for k in fields if k in keys] or not set(required) <= set(keys):
            problems.append(constructs.block_refusal("a steering decision", keys, fields, required))
            continue
        values = {f["key"]: str(record_types.value_of(f)).strip() for f in it["fields"]}
        name = values["Name"]
        require(problems, "steering decision " + name, values, CHANGES, name in logged, "where a steer entry names it")
        for k, v in values.items():
            # working-files/main.md § Steering Decision: Changes holds a list, each item one of its values
            for item in (changes_parts(v) if k == CHANGES else [v]):
                # working-files/main.md § Steering Decision § A Steer's Type: a design written before the names
                # changed is read under its old ones
                if k == "Type" and item in OLD_STEER_TYPES:
                    continue
                if given.get(k) and item not in given[k]:
                    problems.append("steering decision %s has a %s that is not one of %s: %s" % (name, k, ", ".join(given[k]), item))
        if name in seen:
            problems.append("two steering decisions share the Name " + name)
        seen.add(name)
    return problems



def check_goals(body):
    """-> problems with a Design Goals section: `Not yet stated.`, or a Records field and each record its type's
    fields in order, its Name a slug, no two sharing a Name."""
    if body.strip() == NOT_YET_STATED:
        return []
    items = records_read(body)
    if items is None:
        return ["Design Goals has no Records field"]
    if not items:
        return ["Design Goals holds no record"]
    fields, declared = goal_type()
    if not fields:
        return [p for _, p in declared] or ["the Design Goal type declares no fields"]
    problems, seen = [], set()
    for it in items:
        keys = [f["key"] for f in record_types.record_fields(it)]
        if keys != list(fields):
            problems.append(constructs.block_refusal("a design goal", keys, fields, fields))
            continue
        name = str(record_types.value_of(it["fields"][0])).strip()
        # working-files/main.md § Design Goal: a Name in kebab-case, as a design document's Name is
        if kebab(name) != name:
            problems.append("a design goal's Name is not in kebab-case: " + name)
        if name in seen:
            problems.append("two design goals share the Name " + name)
        seen.add(name)
    return problems



def names_of(field):
    """-> the Names a field naming parts of the design holds, a list, one Name to an item, or `none`; None where it
    holds text on its key's line other than `none`, or nothing, so it is no such list (working-files/main.md § Design Goal)."""
    if field["items"] is None:
        return [] if field["value"].strip().strip("`") == "none" else None
    if field["value"] or any(it["fields"] is not None for it in field["items"]):
        return None
    return [it["text"].strip().strip("`").strip() for it in field["items"]]


def values_of(it):
    return {f["key"]: f for f in record_types.record_fields(it)}


def typed(it, fields, required):
    """Whether a record holds its type's fields in their order, each it requires among them."""
    keys = [f["key"] for f in record_types.record_fields(it)]
    return [k for k in fields if k in keys] == keys and set(required) <= set(keys)


def read_steps(text):
    """-> the design's steps as its Design Plan Steps section holds them, read through the one reader, each {"name",
    "fields" {key: field}, "line", "lines", "item", "objectives", "draft"}, its lines 0-based in the design's text and its
    Objectives' lines apart, each Objective {"name", "fields", "line", "lines", "state", "item"}, its lines any block
    nested beneath its State among them (modeling-constructs.md § Fields § A Nested Construct), which objective_constructs
    reports, and "state" the State's line followed by that block's, and "draft" the fenced blocks its Draft holds, each as
    record_types._read_fenced gives it, its lines in the design's text; or None where the section holds no Records
    field."""
    lines = text.split("\n")
    twos = level_two(text)
    start = next((n for title, n in twos if title == "Design Plan Steps"), None)
    if start is None:
        return None
    end = next((n for _, n in twos if n > start), len(lines))
    at = start + 1
    items = records_read("\n".join(lines[at:end]))
    if items is None:
        return None
    steps = []
    for it in items:
        values = values_of(it)
        objectives = []
        for ob in (values["Objectives"]["items"] if "Objectives" in values else None) or []:
            state = next((f for f in ob["fields"] or [] if f["key"] == "State"), None)
            own = [at + n for n in ob["lines"]]
            under = [at + n for n in state["nested"]["lines"]] if state is not None and state["nested"] else []
            objectives.append({"name": str(record_types.value_of(ob["fields"][0])).strip() if ob["fields"] else None,
                               "fields": values_of(ob), "line": at + ob["line"], "lines": own, "item": ob,
                               "state": [at + state["line"]] + under if state is not None else own})
        held = {n for ob in objectives for n in ob["lines"]}
        draft = (values["Draft"]["blocks"] if "Draft" in values else None) or []
        steps.append({"name": str(record_types.value_of(it["fields"][0])).strip() if it["fields"] else "",
                      "fields": values, "line": at + it["line"], "item": it, "objectives": objectives,
                      "lines": [at + n for n in it["lines"] if at + n not in held],
                      "draft": [dict(b, line=at + b["line"], lines=[at + n for n in b["lines"]]) for b in draft]})
    return steps


def objective_constructs(objective, text):
    """-> the 1-based lines of the design opening each construct or table a step Objective holds, which it holds none
    of (working-files/main.md § Design Plan Step § Step Objective): a **Construct:** field, or a table's first line."""
    lines = text.split("\n")
    own = sorted(set(objective["lines"]) | set(objective["state"]))
    table = lambda n: lines[n].lstrip().startswith("|")
    return [n + 1 for k, n in enumerate(own)
            if lines[n].lstrip().startswith("**Construct:**") or (table(n) and (k == 0 or not table(own[k - 1])))]


def check_steps(body, text=None):
    """-> problems with a Design Plan Steps section: `Not yet drafted.`, or a Records field and each record its type's
    fields in order, each it requires among them, Objectives a list of Step Objective records and the last field, a
    Draft, where one stands, fenced blocks alone, Depends On Steps `none` or a list of Names, its Name a slug, no two
    sharing a Name, each Objective its type's fields in order, its Goals and its Upholds Frame Outcomes each a list of
    Names, its Name a slug, and no construct and no table in it; and each step a step cites one the section holds.
    check_form holds the Names to the parts the design holds, and a Draft's constructs to their forms."""
    if body.strip() == NOT_YET_DRAFTED:
        return []
    steps = read_steps(text) if text is not None else None
    if steps is None:
        items = records_read(body)
        if items is None:
            return ["Design Plan Steps has no Records field"]
        steps = [{"name": "", "fields": values_of(it), "item": it, "objectives": []} for it in items]
    if not steps:
        return ["Design Plan Steps holds no record"]
    fields, required, declared = plan_type("Design Plan Steps")
    if not fields:
        return [p for _, p in declared] or ["the Design Plan Step type declares no fields"]
    ob_fields, ob_required, ob_declared = plan_type("Step Objectives")
    problems, seen = [], set()
    for step in steps:
        it = step["item"]
        keys = [f["key"] for f in record_types.record_fields(it)]
        if not typed(it, fields, required):
            problems.append(constructs.block_refusal("a design plan step", keys, fields, required))
            continue
        name = step["name"]
        # working-files/main.md § Design Plan Step: a Name in kebab-case, as a design document's Name is
        if kebab(name) != name:
            problems.append("a design plan step's Name is not in kebab-case: " + name)
        if name in seen:
            problems.append("two design plan steps share the Name " + name)
        seen.add(name)
        # the last field, Objectives, a list: its key on a line of its own and its items beneath
        last = it["fields"][-1]
        if last["inline"] or not last["items"]:
            problems.append("design plan step %s's %s is not a list" % (name, fields[-1]))
        # working-files/main.md § Design Plan Step § A Draft: a Draft's value its fenced blocks, as modeling-constructs.md
        # § Fields has them
        draft = step["fields"].get("Draft")
        if draft is not None and (draft["value"] or draft["items"] is not None or not draft["blocks"]):
            problems.append("design plan step %s's Draft is not fenced blocks beneath its key" % name)
        if "Depends On Steps" in step["fields"] and names_of(step["fields"]["Depends On Steps"]) is None:
            problems.append("design plan step %s's Depends On Steps is neither none nor a list of steps' Names, one to an item" % name)
        if text is None:
            continue
        if not ob_fields:
            problems += [p for _, p in ob_declared] or ["the Step Objective type declares no fields"]
            break
        plain = [ob for ob in step["objectives"] if ob["item"]["fields"] is None]
        if plain:
            problems.append("design plan step %s's Objectives hold %d item%s that %s no Step Objective record"
                            % (name, len(plain), "" if len(plain) == 1 else "s", "is" if len(plain) == 1 else "are"))
        for ob in step["objectives"]:
            label = "design plan step %s's Objective %s" % (name, ob["name"] or "at line %d" % (ob["line"] + 1))
            for line in objective_constructs(ob, text):
                problems.append("%s holds a construct or a table at line %d, where an Objective states an outcome alone" % (label, line))
            if ob["item"]["fields"] is None:
                continue
            if not typed(ob["item"], ob_fields, ob_required) or [f["key"] for f in record_types.record_fields(ob["item"])] != list(ob_fields):
                problems.append(constructs.block_refusal(label, [f["key"] for f in record_types.record_fields(ob["item"])], ob_fields,
                                                       ob_fields))
                continue
            if kebab(ob["name"]) != ob["name"]:
                problems.append("a step objective's Name is not in kebab-case: " + ob["name"])
            for key in ("Goals", "Upholds Frame Outcomes"):
                if not names_of(ob["fields"][key]):
                    problems.append("%s's %s is not a list of Names, one to an item" % (label, key))
    for step in sorted({c.strip() for c in re.findall(r"`§ Design Plan Steps \[Name: ([^\]]+)\]`", body)} - seen - {"…"}):
        problems.append("a citation of a step the design does not hold: " + step)
    return problems


# @canon-spec specs/methodology/working-files/main.md § A Design Document § Approach Principle
# @canon-spec specs/methodology/working-files/main.md § A Design Document § Assessed Area
# @canon-spec specs/methodology/working-files/main.md § A Design Document § Frame Outcome
# @canon-spec specs/methodology/working-files/main.md § A Design Document § Frame Part
# @canon-spec specs/methodology/working-files/main.md § A Design Document § Scope Case
def check_frame_records(plural, body, field="Records", label=None):
    """-> problems with the frame's Assessed Areas or Frame Outcomes, or with the Scope's Cases or the Approach's
    Principles, each read by field against its own kind's type, its base's fields first, under its label: `Not yet
    stated.`, or the field and each record its type's fields in order, an Assessed Area's Area one place used once, its
    Impact a list of the members of Read Assessment Impacts other than `none` and its Assessment one place; each Frame
    Part's Name a slug used once and its Goals a list of Names."""
    if body is None or not_stated(body):
        return []
    where = plural if field == "Records" else "the frame's " + field
    items = records_read(body, field)
    if items is None:
        return ["%s has no %s field" % (plural if field == "Records" else "the frame", field)]
    if not items:
        return ["%s holds no record" % where]
    fields, required, declared = plan_type(plural)
    if not fields:
        return [p for _, p in declared] or ["the %s type declares no fields" % PLAN_TYPES[plural][0][1].split(" § ")[-1]]
    label = label or ("an assessed area" if plural == AREAS else "a frame outcome")
    members = [m for m in impact_members()[0] if m != "none"]
    problems, seen = [], set()
    for it in items:
        keys = [f["key"] for f in record_types.record_fields(it)]
        if not typed(it, fields, required):
            problems.append(constructs.block_refusal(label, keys, fields, required))
            continue
        values = values_of(it)
        key = str(record_types.value_of(values[PLAN_TYPES[plural][1]])).strip()
        if key in seen:
            problems.append("two %ss share the %s %s" % (label.split(" ", 1)[1], PLAN_TYPES[plural][1], key))
        seen.add(key)
        if plural in FRAME_PART_TYPES:
            noun = label.split(" ", 1)[1]
            if kebab(key) != key:
                problems.append("%s's Name is not in kebab-case: %s" % (label, key))
            if not names_of(values["Goals"]):
                problems.append("%s %s's Goals is not a list of goals' Names, one to an item" % (noun, key))
            continue
        for k in ("Area", "Assessment"):
            if not place_of(str(record_types.value_of(values[k]))):
                problems.append("assessed area %s's %s is no one place cited with its path" % (key, k))
        impact = names_of(values["Impact"])
        if not impact or any(i not in members for i in impact) or len(set(impact)) != len(impact):
            problems.append("assessed area %s's Impact is not a list of %s, one to an item" % (key, " or ".join(members)))
    return problems


def read_plan(text):
    """-> the design's keyed parts by their Names, read from its records: {"goals": [Name], "cases": {Name: [goal]},
    "principles": {Name: [goal]}, "outcomes": {Name: [goal]},
    "steps": [step as read_steps gives it], "objectives": {Name: (step, its Goals, its Upholds Frame Outcomes)}, "areas":
    [(Area, [Impact], Assessment)], "whole": whether each step and each Objective holds its type's fields}."""
    goals = [str(record_types.value_of(values_of(it)["Name"])).strip() for it in records_read(section(text, "Design Goals")) or []
             if "Name" in values_of(it)]
    frame = frame_parts(text)
    areas = []
    # the frame's named parts, each read by its Name with the goals it rests on: its cases, its principles and its
    # Frame Outcomes
    framed = {}
    for part, field in [(p, f) for p, f, _, _ in FRAME_RECORDS] + [(OUTCOMES, "Records")]:
        framed[part] = {}
        for it in records_read(frame.get(part), field) or []:
            v = values_of(it)
            if "Name" in v:
                framed[part][str(record_types.value_of(v["Name"])).strip()] = names_of(v["Goals"]) or [] if "Goals" in v else []
    outcomes = framed[OUTCOMES]
    for it in records_read(frame.get(AREAS)) or []:
        v = values_of(it)
        if "Area" in v:
            areas.append((str(record_types.value_of(v["Area"])).strip(),
                          names_of(v["Impact"]) or [] if "Impact" in v else [],
                          str(record_types.value_of(v["Assessment"])).strip() if "Assessment" in v else ""))
    steps, objectives = read_steps(text) or [], {}
    (fields, required, _), ob_fields = plan_type("Design Plan Steps"), plan_type("Step Objectives")[0]
    whole = bool(steps)
    for step in steps:
        whole = whole and typed(step["item"], fields, required) and bool(step["objectives"])
        for ob in step["objectives"]:
            v = ob["fields"]
            whole = whole and list(v) == list(ob_fields)
            if ob["name"] and "Goals" in v and "Upholds Frame Outcomes" in v:
                objectives[ob["name"]] = (step["name"], names_of(v["Goals"]) or [], names_of(v["Upholds Frame Outcomes"]) or [])
    return {"goals": goals, "cases": framed["Scope"], "principles": framed["Approach"], "outcomes": outcomes,
            "steps": steps, "objectives": objectives, "areas": areas, "whole": whole}


# @canon-spec specs/methodology/working-files/main.md § A Design Document § The Record's Checks
def reference_problems(text, plan):
    """-> problems with the references within a design, the References check of working-files/main.md § A Design Document § The Record's Checks:
    each Name a Frame Outcome's Goals, a step's Depends On Steps, and a step Objective's Goals and Upholds Frame
    Outcomes hold, and a case's and a principle's Goals, naming a part the design holds; no Name two kinds of part take; each goal served by a step Objective
    and each Frame Outcome upheld by one, once each step and each Objective holds its type's fields; and no step
    depending on itself through the steps it depends on, nor standing before a step it depends on."""
    problems = []
    goals, outcomes = plan["goals"], plan["outcomes"]
    steps = [s["name"] for s in plan["steps"] if s["name"]]
    kinds = collections.defaultdict(list)
    for kind, names in (("a goal", goals), ("a case", plan["cases"]), ("a principle", plan["principles"]),
                        ("a frame outcome", outcomes), ("a step", steps), ("a step objective", plan["objectives"])):
        for n in dict.fromkeys(names):
            kinds[n].append(kind)
    problems += ["the Name %s is taken by %s, where one part of the design takes a Name" % (n, " and ".join(k))
                 for n, k in kinds.items() if len(k) > 1]
    for noun, held in (("case", plan["cases"]), ("principle", plan["principles"]), ("frame outcome", outcomes)):
        for name, named_goals in held.items():
            problems += ["%s %s's Goals names %s, no goal the design holds" % (noun, name, g) for g in named_goals if g not in goals]
    depends = {}
    for s in plan["steps"]:
        field = s["fields"].get("Depends On Steps")
        depends[s["name"]] = (names_of(field) or []) if field is not None else []
        problems += ["design plan step %s's Depends On Steps names %s, no step the design holds" % (s["name"], d)
                     for d in depends[s["name"]] if d not in steps]
    for name, (_, named_goals, upholds) in plan["objectives"].items():
        problems += ["step objective %s's Goals names %s, no goal the design holds" % (name, g) for g in named_goals if g not in goals]
        problems += ["step objective %s's Upholds Frame Outcomes names %s, no Frame Outcome the design holds" % (name, o)
                     for o in upholds if o not in outcomes]
    if plan["whole"]:
        served = {g for _, gs, _ in plan["objectives"].values() for g in gs}
        upheld = {o for _, _, os in plan["objectives"].values() for o in os}
        problems += ["goal %s is served by no step Objective naming it" % g for g in goals if g not in served]
        problems += ["frame outcome %s is upheld by no step Objective naming it" % o for o in outcomes if o not in upheld]
    reported = set()

    def cycle(n, path):
        if n in path:
            return path[path.index(n):] + [n]
        for d in depends.get(n, []):
            hit = cycle(d, path + [n])
            if hit:
                return hit
        return None
    for n in steps:
        hit = cycle(n, [])
        if hit and frozenset(hit) not in reported:
            reported.add(frozenset(hit))
            problems.append("Depends On Steps runs in a cycle: " + " -> ".join(hit))
    order = {n: i for i, n in enumerate(steps)}
    problems += ["design plan step %s stands before %s, a step it depends on" % (n, d)
                 for n in steps for d in depends.get(n, []) if d != n and order.get(d, -1) > order[n]]
    return problems



# @canon-spec specs/methodology/working-files/main.md § Design Log Entry § Script Checks [Name: sub-scopes-named]
# the fields holding sub-scopes, each a list of Sub-scopes
SUB_SCOPE_FIELDS = ("Settled Sub-scopes",)


# @canon-spec specs/methodology/working-files/main.md § Design Log Entry § Script Checks [Name: sub-scopes-named]
def sub_scope_problems(an, kind, field, value):
    """-> problems with a field holding sub-scopes: each of its semicolon-separated items a Sub-scope, taken one at a time."""
    return ["%s %s entry's %s names %s, not one of %s" % (an, kind, field, item or "nothing", ", ".join(SUB_SCOPES))
            for item in (s.strip() for s in value.split(";")) if item not in SUB_SCOPES]


def entry_problems(kind, fields, values, counts, kinds):
    """-> problems with one log entry's kind and its fields beside Entry and Timestamp, [(field, value)]: a kind the
    table does not give, its fields other than the kind gives, in the type's order, a `design-reassessment` entry's
    those its Cause gives it, and a value outside its field's Values, a Cause in neither of its forms, a count not a
    whole number, or an empty value."""
    if kind not in kinds:
        return ["a log entry's kind is not one of %s: %s" % (", ".join(kinds), kind)]
    keys, an = [k for k, _ in fields], "an" if kind[0] in "aeiou" else "a"
    given = cause_fields(dict(fields), kinds[kind]) if kind == DESIGN_REASSESSMENT else kinds[kind]
    # a field the type requires of no entry, Cuts Short among them, is held only where it is given
    optional = optional_entry_fields()
    if keys != [k for k in given if k in keys or k not in optional]:
        return [constructs.block_refusal("%s %s entry" % (an, kind), keys, given, [k for k in given if k not in optional],
                                         owner="its kind")]
    problems = []
    for k, v in fields:
        if not v:
            problems.append("%s %s entry's %s is empty" % (an, kind, k))
        elif k == CAUSE and read_cause(v) is None:
            problems.append("%s %s entry's %s is neither `%s:` and each design the design was freed from, followed by %s "
                            "or %s, separated by semicolons, nor `%s:` and one of %s: %s"
                            % (an, kind, k, CHANGED_FOUNDATION, FINISHED_NAME, GONE_NAME, STEP_BACK, ", ".join(STEP_BACK_CAUSES), v))
        elif k in SUB_SCOPE_FIELDS:
            problems += sub_scope_problems(an, kind, k, v)
        elif values.get(k) and v not in values[k]:
            problems.append("%s %s entry's %s is not one of %s: %s" % (an, kind, k, ", ".join(values[k]), v))
        elif counts.get(k) and not re.fullmatch(r"\d+", v):
            problems.append("%s %s entry's %s is not a whole number: %s" % (an, kind, k, v))
    return problems


def check_log(body):
    """-> problems with a Design Log Entries section: a Records field, and each entry its kind's fields, its Entry
    its kind and its count among its kind from 1 in the order the entries stand, and its Timestamp a UTC time no
    earlier than the one before it."""
    entries = records(body)
    if entries is None:
        return ["%s has no Records field" % LOG]
    if not entries:
        return ["%s holds no entry" % LOG]
    values, counts, kinds, declared = log_type()
    if not kinds:
        return [p for _, p in declared]
    problems, seen, last = [], {}, ""
    for fields in entries:
        if [k for k, _ in fields[:2]] != ["Entry", "Timestamp"]:
            problems.append("a log entry does not open with Entry and Timestamp: " + ", ".join(k for k, _ in fields))
            continue
        entry, stamp_ = fields[0][1].strip(), fields[1][1].strip()
        m = re.fullmatch(r"([a-z-]+?)-(\d+)", entry)
        if not m:
            problems.append("a log entry's Entry is not its kind and its count: " + entry)
            continue
        kind = m.group(1)
        seen[kind] = seen.get(kind, 0) + 1
        if int(m.group(2)) != seen[kind]:
            problems.append("log entry %s is not counted in order, it is %s-%d" % (entry, kind, seen[kind]))
        if not TIMESTAMP.match(stamp_):
            problems.append("log entry %s's Timestamp is not a UTC time as a stamp writes one: %s" % (entry, stamp_))
        elif stamp_ < last:
            problems.append("log entry %s's Timestamp is earlier than the one before it: %s" % (entry, stamp_))
        else:
            last = stamp_
        # an entry's Design Version stands right after its Timestamp, held to the log's version by check_form
        rest = [(k, v.strip()) for k, v in fields[2:]]
        rest = rest[1:] if rest and rest[0][0] == VERSIONED else rest
        problems += ["log entry %s: %s" % (entry, p) for p in entry_problems(kind, rest, values, counts, kinds)]
    return problems


def check_retired(body):
    """-> problems with a Retired Phrases section: a Records field, and each record its type's fields in order, those
    it requires present, no two sharing a Phrase."""
    phrases = records(body)
    if phrases is None:
        return ["%s has no Records field" % RETIRED]
    if not phrases:
        return ["%s holds no record" % RETIRED]
    fields, required, declared = retired_type()
    if not fields:
        return [p for _, p in declared]
    problems, seen = [], set()
    for record in phrases:
        keys = [k for k, _ in record]
        if [k for k in fields if k in keys] != keys or not set(required) <= set(keys):
            problems.append(constructs.block_refusal("a retired phrase", keys, fields, required))
            continue
        phrase = record[0][1].strip()
        if phrase.lower() in seen:
            problems.append("two retired phrases share the Phrase " + phrase)
        seen.add(phrase.lower())
    return problems


def steer_table_problems(root):
    """-> problems with the Steering Decision, Design Goal, Assessed Area, Frame Outcome, Design Plan Step, Step
    Objective, Read Assessment, Design Log Entry and Retired Phrase types' declarations, and with Read Assessment
    Impacts', which this tooling reads their records' fields and values from."""
    return steer_type(root)[3] + goal_type(root)[1] + log_type(root)[3] + retired_type(root)[2] \
        + [p for plural in PLAN_TYPES for p in plan_type(plural, root)[2]] + impact_members(root)[1]


# @canon-spec specs/methodology/working-files/main.md § A Design Document
def reliance_problems(scope, depends_on, own):
    """-> the problem of a design whose Scope holds a Reliances field, which its form does not take, a design naming
    the designs it depends on in its Depends On Designs alone: it names each design a Reliance names that depends_on,
    the design's Depends On Designs, does not, each name read as a design in the folder own writes it; [] where the
    Scope holds no such field."""
    items = records_read(scope, "Reliances")
    if items is None:
        return []
    relied = [str(record_types.value_of(values_of(it)["Design"])).strip().strip("`") for it in items if "Design" in values_of(it)]
    held = named(rename(depends_on, own, own))
    missing = [d for d in dict.fromkeys(named(rename("; ".join(relied), own, own))) if d not in held]
    return ["its Scope holds a Reliances field, which its form does not take: a design names the designs it depends on in "
            "its Depends On Designs alone" + ("; its Reliances name %s, which its Depends On Designs does not"
                                              % "; ".join(missing) if missing else "")]


# @canon-spec specs/methodology/working-files/main.md § A Design Document
# @canon-spec specs/methodology/working-files/main.md § A Design Document § The Design's Version
def header_problems(design, fields, text):
    """-> problems with the header of the design at this path, its fields [(key, value)] as read_design gives them and
    text its text, each naming the field it is a problem of: a field its form does not take, one it requires left
    out, or its fields out of their order; a Version that is no version, is written at its default or is not the one
    the design's log gives; a Name that is empty, no slug or not its file's name; a Status that is no state; a Kind
    that is no kind, or not the one its plans folder sets; a Target that is not paths; and a Validated that is neither
    none nor a stamp, or not the stamp its Status asks."""
    problems, keys, values = [], [k for k, _ in fields], dict(fields)
    if keys not in (list(FIELDS), list(UNVERSIONED)):
        problems.append(constructs.block_refusal("its header", keys, FIELDS, UNVERSIONED, owner="its form"))
    # the header's Version the one the log gives, never written at 0.1.0, its default
    given = design_version(log_entries(text), steer_changes(text))
    if "Version" in values and parse_version(values["Version"]) is None:
        problems.append("Version is not major.minor.revision: " + values["Version"])
    elif "Version" in values and parse_version(values["Version"]) == FIRST_VERSION:
        problems.append("Version is written at its default, %s" % version_text(FIRST_VERSION))
    elif "Version" in values and parse_version(values["Version"]) != given:
        problems.append("Version is %s, where its log gives %s" % (values["Version"], version_text(given)))
    # the Name is the design's slug, and its file is {Name}.md
    if not values.get("Name"):
        problems.append("Name is empty")
    elif kebab(values["Name"]) != values["Name"]:
        problems.append("Name is not a slug: " + values["Name"])
    elif values["Name"] != design.stem:
        problems.append("Name is not its file name without .md: " + values["Name"])
    if values.get("Status", "") not in STATES:
        problems.append("Status is not a state: " + values.get("Status", ""))
    if values.get("Kind", "") not in KINDS:
        problems.append("Kind is not %s: %s" % (KIND_LIST, values.get("Kind", "")))
    # working-files/main.md § A Design Document § A Design Changing Code: the folder sets the kind
    if values.get("Kind") and (values["Kind"] == "code") != (design.resolve().parent.name == CODE_PLANS):
        problems.append("Kind is code for a design under .ai/plans/%s/ and for no other: %s" % (CODE_PLANS, values["Kind"]))
    target = values.get("Target", "")
    unknown = values.get("Status") == "not-started" and target.lower() == "none"
    if not unknown and not all(re.fullmatch(r"`[^`]+`", p.strip()) for p in (target.split(";") if target else [""])):
        problems.append("Target is not paths in backticks separated by semicolons: " + target)
    # working-files/main.md § A Design Document § A Form the Methodology Is Still Adding: no design is validated by hand
    validated = values.get("Validated", "")
    if validated.lower() != "none" and not STAMP.match(validated):
        problems.append("Validated is neither none nor a stamp: %s" % validated)
    elif values.get("Status") == "approved" and not STAMP.match(validated):
        problems.append("approved, but no validation review has stamped it")
    elif values.get("Status") == "approved" and validated.split(" ")[1] != content_hash(text):
        problems.append("approved, but edited since its validation review stamped it")
    elif values.get("Status") in ("applying", "complete") and not STAMP.match(validated):
        problems.append(values["Status"] + ", but no validation review stamped it")
    return problems


# @canon-spec specs/methodology/working-files/main.md § A Design Document
def sections_owed(sections, values):
    """-> the sections the form gives a design holding these level-two headings and these header values, in the
    form's order: each it holds, and each it requires that it does not, the goals required but in a design complete or
    abandoned, and the Impact on the Application Specs a canon design's alone."""
    return [s for s in SECTIONS
            if (s in sections or (s not in OPTIONAL and (s not in UNTIL_FINISHED or values.get("Status") not in FINISHED)))
            and (s != IMPACT or values.get("Kind") == "canon-specs")]


# @canon-spec specs/methodology/working-files/main.md § A Design Document
# @canon-spec specs/methodology/working-files/main.md § Design Goal
def goals_problems(goals, values):
    """-> problems with a design's Design Goals section, goals its body, or None where the design holds none, and
    values its header's: the problems check_goals gives of its records, and goals not yet stated in a design approved
    or further."""
    if goals is None:
        return []
    problems = check_goals(goals)
    if goals.strip() == NOT_YET_STATED and values.get("Status") in ("approved", "applying", "complete"):
        problems.append(values["Status"] + ", but its design goals are not yet stated")
    return problems


def check_form(design):
    """-> (1, [(file name, problem)]): one design document against its form, its header by header_problems, its
    sections by sections_owed and its goals by goals_problems, the three the showing of a design reads too."""
    name, fields, sections, text = read_design(design)
    values = dict(fields)
    problems = ["it does not open with the heading Design Document"] if not text.startswith("# Design Document\n") else []
    problems += header_problems(design, fields, text)
    # working-files/main.md § A Design Document § The Design's Version: each entry's Design Version the version of the
    # design its work read: a check's a version the log held before it, any other's the version as it was appended;
    # none written at 0.1.0, its default
    # @canon-spec specs/methodology/working-files/main.md § Design Log Entry § Script Checks [Name: entry-at-the-version-read]
    entries = log_entries(text)
    given = versions(entries, steer_changes(text))
    checks = {k for k, fs in log_type()[2].items() if "Model" in fs}
    for i, ((kind, n, f), version) in enumerate(zip(entries, given)):
        stamped = parse_version(f["Design Version"]) if "Design Version" in f else FIRST_VERSION
        if stamped is None:
            problems.append("log entry %s-%d's Design Version is not major.minor.revision: %s" % (kind, n, f["Design Version"]))
        elif "Design Version" in f and stamped == FIRST_VERSION:
            problems.append("log entry %s-%d's Design Version is written at its default, %s" % (kind, n, version_text(FIRST_VERSION)))
        elif kind in checks and stamped not in [FIRST_VERSION] + given[:i]:
            problems.append("log entry %s-%d's Design Version is %s, a version its log never held before it, "
                            "where a check's entry stands at the version its report read (%s)"
                            % (kind, n, version_text(stamped), ENTRY_AT_VERSION_READ))
        elif kind not in checks and stamped != version:
            problems.append("log entry %s-%d's Design Version is %s, where its log gives %s"
                            % (kind, n, version_text(stamped), version_text(version)))
    # working-files/main.md § Design Log Entry § Script Checks [Name: goals-agreed-before-checks], read over the whole log
    problems += gate_problems(entries, checks)
    problems += check_log(section(text, LOG)) if section(text, LOG) is not None else []
    problems += check_retired(section(text, RETIRED)) if section(text, RETIRED) is not None else []
    want = sections_owed(sections, values)
    if sections != want:
        problems.append(constructs.block_refusal("the design", sections, [s for s in SECTIONS if s != IMPACT or values.get("Kind") == "canon-specs"],
                                                 want, noun="section", owner="its form"))
    frame = frame_parts(text)
    heads = [title for title, _ in level_three(section(text, "The Design Frame") or "")]
    if "The Design Frame" in sections and heads != list(FRAME):
        problems.append(constructs.block_refusal("its design frame", heads, FRAME, FRAME, noun="heading", owner="its form"))
    if values.get("Status") in ("approved", "applying", "complete"):
        problems += [values["Status"] + ", but its design frame's " + part + " is not yet stated" for part in FRAME if not_stated(frame.get(part))]
    for plural in (AREAS, OUTCOMES):
        problems += check_frame_records(plural, frame.get(plural))
    for part, field, label, plural in FRAME_RECORDS:
        problems += check_frame_records(plural, frame.get(part), field, label)
    problems += reliance_problems(frame.get("Scope"), values.get(DEPENDS_ON, ""), design.resolve().parent.name)
    # working-files/main.md § Design Log Entry: a steer entry names a Steering Decision the design holds
    body = section(text, "Steering Decisions")
    logged = [n for e in entries if e[0] == "steer" for n in set_names(e)]
    problems += check_steers(body, logged) if body is not None else []
    problems += ["a steer entry names a Steering Decision the design does not hold: " + s
                 for s in sorted(set(logged) - set(steer_changes(text)))]
    goals = section(text, "Design Goals")
    problems += goals_problems(goals, values)
    # specs/methodology/working-files/main.md § Design Goal: a goal cited in the frame's or the steps' prose is
    # one the design holds
    held = {dict(rec).get("Name", "").strip() for rec in records(goals) or []}
    steps = section(text, "Design Plan Steps")
    cites = re.findall(r"`§ Design Goals \[Name: ([^\]]+)\]`", (section(text, "The Design Frame") or "") + (steps or ""))
    problems += ["a citation of a goal the design does not hold: " + cited for cited in sorted({c.strip() for c in cites} - held - {"…"})]
    problems += check_steps(steps, text) if steps is not None else []
    if steps is not None and steps.strip() == NOT_YET_DRAFTED and values.get("Status") in ("approved", "applying", "complete"):
        problems.append(values["Status"] + ", but its steps are not yet drafted")
    problems += reference_problems(text, read_plan(text))
    # modeling-constructs.md § Fields and spec-style/markdown.md § Blank Lines: the design's layout, each block of fields and
    # each list a field holds by the reader's checks, and each blank line by the layout check
    base = Path(design).resolve().parents[3]
    table, table_problems = layout.rules(base if (base / layout.HOME).is_file() else repo_root())
    problems += [msg for _, _, _, msg in table_problems]
    problems += ["line %d: %s" % (line, msg) for _, line, msg in layout.findings(text, table) + record_types.block_findings(text)]
    # working-files/main.md § A Design Document § The Record's Checks: each construct a step's Draft holds, by the
    # construct checks
    problems += draft_problems(design, text, base if (base / layout.HOME).is_file() else repo_root())
    return 1, [(name, p) for p in problems]


# @canon-spec specs/methodology/working-files/main.md § Design Plan Step § A Draft
def draft_problems(design, text, root):
    """-> problems with the constructs each step's Draft holds: the construct checks' findings over each of its
    `markdown` blocks, each read as a file of its own, by its block's path, beside the specs as they stand, which give
    what it reads and does not declare, as constructs.run_checks reads every file; a block of code is checked by none.
    The checks run only where a Draft holds a `markdown` block."""
    blocks = [(s["name"], b) for s in read_steps(text) or [] for b in s["draft"] if b["info"] == layout.MARKDOWN_INFO]
    if not blocks:
        return []
    try:
        rel = Path(design).resolve().relative_to(Path(root).resolve()).as_posix()
    except ValueError:
        rel = Path(design).name
    text_of, held = dict(spec_texts(root)), {}
    for step, b in blocks:
        path = record_types.block_path(rel, b["line"])
        text_of[path], held[path] = b["text"], (step, b["line"])
    found, _, _ = constructs.run_checks(text_of)
    return ["design plan step %s's Draft, line %d: %s: %s" % (held[path][0], held[path][1] + 1 + line, rule, msg)
            for rule, path, line, msg in sorted(found, key=lambda f: (str(f[1]), f[2] or 0)) if path in held]


# @canon-spec specs/methodology/working-files/main.md § A Design Document § The Kinds of Change
def kind_of(path, skills):
    """canon-specs, application-specs, or None for any other file; skills, the registered skills' directories and lib."""
    if path in ("specs/AGENTS.md", "specs/main.md", "specs/architecture.md") or path.startswith("specs/methodology/"):
        return "canon-specs"
    if any(path.startswith(".ai/skills/" + n + "/") for n in skills):
        return "canon-specs"
    if path.startswith("specs/application/"):
        return "application-specs"
    return None


# @canon-spec specs/methodology/working-files/main.md § The Working Files
WORKING_FILES = (".ai/plans/", ".ai/follow-ups.md", ".ai/tmp/")  # a working file is of no kind of change


def is_working_file(path):
    path = path.removeprefix("./")
    return any(path == w.rstrip("/") or path.startswith(w) for w in WORKING_FILES)


def check_kind(design, root):
    """-> (1, [(file name, problem)]) where one design document's Target strays from its Kind."""
    if not registry(root)[0]:
        return 0, [(REGISTRY, "no registered skills read, so a skill's files cannot be classified")]
    skills = skill_dirs(root)
    problems, designs = [], [read_design(design)]
    for title, fields, _, _ in designs:
        fields = dict(fields)
        value, target = fields.get("Kind"), fields.get("Target")
        if not value:
            problems.append((title, "no Kind field"))
            continue
        if not target:
            problems.append((title, "no Target field"))
            continue
        if value not in KINDS:
            problems.append((title, "Kind is not %s: %s" % (KIND_LIST, value)))
            continue
        if fields.get("Status") == "not-started" and target.lower() == "none":
            continue
        if not re.findall(r"`([^`]+)`", target):
            problems.append((title, "Target names no path"))
            continue
        for path in re.findall(r"`([^`]+)`", target):
            if is_working_file(path):
                problems.append((title, "Target names a working file, which no design changes: " + path))
                continue
            k = kind_of(path, skills)
            if k and k != value:
                article = lambda w: ("an " if w[0] in "aeiou" else "a ") + w
                problems.append((title, "Target names %s file in %s design: %s" % (article(k), article(value), path)))
    return len(designs), problems


# @canon-spec specs/methodology/working-files/main.md § A Design Document § What Blocks What
def check_stack(folder):
    """-> (report lines, [(file name, problem)]): the workstack the designs standing in the plans folders draw by
    their Spawned By and Depends On Designs, each name of a design not yet finished read by read_name from the plans
    folders as they stand, per working-files/main.md § A Design Document § What Blocks What: a name of an unfinished
    design blocks the design naming it, and a name of a finished or gone design leaves it waiting to be freed. The
    lines draw the tree, list what to work next, a design waiting to be freed first freed, list the blocked designs,
    and list each finished design, which may be deleted or moved at any time. The problems are a field of a design's
    header that its form does not take, named as check_form names it, since the workstack is drawn from the fields the
    form gives and from no other; an approved or applying design naming an unfinished design; and a loop in Depends On
    Designs or in Spawned By. A name a complete or an abandoned design holds is its history, and reads as nothing."""
    read = read_designs(folder)
    designs = {name: dict(fields) for name, fields, _, _ in read}
    # working-files/main.md § A Design Document: the header's fields are the ones its table of parts gives
    out_of_form = {name: constructs.block_faults([k for k, _ in fields if k not in FIELDS], FIELDS, owner="its form")
                   for name, fields, _, _ in read}
    checked = {name: validation(text, fields)[0] for name, fields, _, text in read}
    status = lambda n: designs[n].get("Status", "")
    names = lambda n, key: named(designs[n].get(key, ""))
    readings = {n: [(d, read_name(designs, d)) for d in names(n, DEPENDS_ON)] if status(n) not in FINISHED else []
                for n in designs}
    blocked_by = lambda n: [d for d, r in readings[n] if r == UNFINISHED_NAME]
    # the finished or gone designs a design waits to be freed from, each with which of the two it is
    changed = lambda n: ["%s %s" % (d, r) for d, r in readings[n] if r != UNFINISHED_NAME]
    problems = []
    for n in designs:
        problems += [(n, "its header " + fault) for fault in out_of_form[n]]
        if status(n) in ("approved", "applying") and blocked_by(n):
            problems.append((n, "%s, but its Depends On Designs names %s, unfinished: no agent takes a blocked design past "
                                "its framing, so it goes back to in-progress as its builder next works it" % (status(n), "; ".join(blocked_by(n)))))

    def loops(edges):
        found, seen = [], set()
        for n in designs:
            path, cur = [n], edges(n)
            while cur:
                if cur[0] in path:
                    loop = path[path.index(cur[0]):] + [cur[0]]
                    if frozenset(loop) not in seen:
                        seen.add(frozenset(loop))
                        found.append((n, loop))
                    break
                path.append(cur[0])
                cur = edges(cur[0])
        return found

    def dep_cycles(n, path):
        if n in path:
            return path[path.index(n):] + [n]
        for d in blocked_by(n):
            hit = dep_cycles(d, path + [n])
            if hit:
                return hit
        return None
    reported = set()
    for n in designs:
        hit = dep_cycles(n, [])
        if hit and frozenset(hit) not in reported:
            reported.add(frozenset(hit))
            problems.append((n, "Depends On Designs runs in a cycle: " + " -> ".join(hit)))
    parent = lambda n: [p for p in names(n, "Spawned By")[:1] if p in designs]
    for n, loop in loops(parent):
        problems.append((n, "Spawned By runs in a loop: " + " -> ".join(loop)))

    waits_on = {n: set() for n in designs}
    for n in designs:
        for d in blocked_by(n):
            waits_on[d].add(n)

    def behind(n, seen):
        for w in waits_on[n] - seen:
            seen.add(w)
            behind(w, seen)
        return seen

    def label(n):
        notes = [status(n)]
        if blocked_by(n):
            notes.append("blocked by " + "; ".join(blocked_by(n)))
        if changed(n):
            notes.append("waiting to be freed of " + "; ".join(changed(n)))
        if status(n) in ("in-progress", "approved") and checked[n] != "none":
            notes.append("validated" if checked[n] == "validated" else "validation stale")
        return "%s [%s]" % (n, ", ".join(notes))

    children, drawn = {}, set()
    for n in designs:
        children.setdefault((parent(n) or [None])[0], []).append(n)
    lines = ["Workstack:"]

    def draw(n, depth, up):
        drawn.add(n)
        lines.append("%s%s%s" % ("  " * depth, label(n), ", blocks " + up if up and n in blocked_by(up) else ""))
        for child in sorted(children.get(n, [])):
            if child not in drawn:
                draw(child, depth + 1, n)
    for n in sorted(children.get(None, [])):
        draw(n, 1, None)
    for n in sorted(designs):
        if n not in drawn:
            draw(n, 1, None)

    def action(n):
        if changed(n):
            return "free"
        return {"not-started": "start", "in-progress": "design", "approved": "apply", "applying": "finish applying"}[status(n)]
    unfinished = [n for n in designs if status(n) in STATES and status(n) not in FINISHED]
    ready = [n for n in unfinished if not blocked_by(n)]
    ready.sort(key=lambda n: (-len(behind(n, set())), n))
    lines.append("Work next:")
    lines += ["  %s: %s, %d waiting on it" % (action(n), label(n), len(behind(n, set()))) for n in ready] or ["  none"]
    held = sorted(n for n in unfinished if blocked_by(n))
    lines.append("Blocked, worked no further than its agreed goals and frame:")
    lines += ["  %s: %s" % ("free" if changed(n) else "move back" if status(n) in ("approved", "applying") else "frame or wait",
                            label(n)) for n in held] or ["  none"]
    lines.append("Finished, each one a design that may be deleted or moved at any time:")
    lines += ["  " + n for n in sorted(designs) if status(n) in FINISHED] or ["  none"]
    return lines, problems

# `path/to/file.md § Parent § Child`. A span carrying no path is a same-file
# citation and is not checked here; see .ai/skills/design-specs/SKILL.md, Verifying a proposal. Its span opens with one backtick or more and closes
# on a run of as many, a run of another length inside it literal, as GitHub Flavored Markdown has a code span.
def cross_file_citations(text):
    """-> [(the offset of its span, the path it names, its heading path)] for each citation of a section of another
    Markdown file, the span and the citation's form each as the one reading reads them (reading.py), a keyed part
    left off."""
    out = []
    for at, held in reading.spans(text):
        c = reading.parse_citation(held)
        if c is not None and c.lineage and c.file.endswith(".md"):
            out.append((at, c.file, c.path))
    return out


def folder_file(folder, target=""):
    """-> the file of a document laid out as a folder holding the section `target` names, its main file tried first
    where it holds one; with no target, its main file where it holds one; else None."""
    files = sorted((p for p in folder.glob("*.md") if p.name != "index.md"), key=lambda p: (p.name != "main.md", p.name))
    if not target:
        return next((p for p in files if p.name == "main.md"), None)
    return next((p for p in files if target in lineages(read(p))), None)


def resolve(path, root, target=""):
    """-> (Path, note). A proposal is prose, so it may name a file in shorthand.

    An exact path wins. Otherwise the path is treated as a suffix, which is how a
    proposal refers back to a file whose full path it gave earlier. A suffix
    matching more than one file is not resolved: in a tree with several
    architecture.md files, a bare one names nothing in particular, and saying so
    is more useful than guessing which was meant.
    """
    exact = root / path
    if exact.is_file():
        return exact, ""
    tail = "/" + path.lstrip("./")
    # the specifications' files as the index walk finds them, and every other Markdown file under the root, the skills'
    # own output aside: each judged by its place within the root, so the root's own place decides nothing, a checkout
    # kept beneath another's working files resolving as any other does
    walked = [p for p in indexed(root, "specs")]
    hits = sorted(
        p for p in walked + [p for p in root.rglob("*.md") if not p.relative_to(root).as_posix().startswith("specs/")]
        if ("/" + p.relative_to(root).as_posix()).endswith(tail) and not p.relative_to(root).as_posix().startswith(".ai/tmp/")
    )
    if len(hits) == 1:
        return hits[0], ""
    # a document laid out as a folder, named by its bare file name, is read through its files: the one holding the
    # section named, its main file first where it holds one (spec-placement/where-a-file-goes.md § Where a File Goes); a bare main.md
    # names no one document, every folder's main file sharing the name, and a folder's index.md is never a document
    if not hits and path.endswith(".md") and PurePosixPath(path).name not in ("main.md", "index.md"):
        index, _ = resolve(path[:-3] + "/index.md", root)
        # a section none of its files holds is reported at its main file, where it holds one, as no such heading
        found = index is not None and (folder_file(index.parent, target) or folder_file(index.parent))
        if found:
            return found, ""
    if not hits:
        return None, "no such file"
    names = ", ".join(h.relative_to(root).as_posix() for h in hits[:3])
    return None, "ambiguous shorthand, %d files match: %s" % (len(hits), names)


# @canon-spec specs/methodology/working-files/main.md § A Design Document § The States It Moves Through § A Send-back
def check_citations(proposal, root, kept=(), extra=""):
    """-> [(ok, path, target, note)] for each cross-file citation, in order, of the proposal and of extra, the file it
    names found and read by citation_file."""
    text = read(Path(proposal)).replace("\r\n", "\n") + "\n" + extra
    head = CommitTree(root) if kept else None
    seen, results = set(), []
    # working-files/main.md § Design Plan Step § A Draft: a Draft's construct cites sections as the files will stand once
    # the design's steps apply, a heading another of its Drafts creates among them
    spans, drafted = draft_spans(text) if is_design(Path(proposal)) else ([], set())
    # a record citation's [...] selector names a record; only its section resolves here
    for at, path, target in cross_file_citations(text):
        if (path, target) in seen:
            continue
        seen.add((path, target))
        target_file, note = citation_file(path, root, target, head, kept)
        if target_file is None:
            results.append((False, path, target, note))
            continue
        found = lineages(read(target_file))
        if target not in found and any(a <= at < b for a, b in spans) and drafted_heading(target, found, drafted):
            results.append((True, path, target, "a heading the design's Drafts create"))
            continue
        results.append((True, path, target, "") if target in found else
                       (False, path, target, citation_miss(target, found)))
    return results


def draft_spans(text):
    """-> ([(start, end)] of each `markdown` block a step's Draft holds in a design's text, {the lineage of each heading
    those blocks hold, from its block's top})."""
    spans, drafted = [], set()
    for s in read_steps(text) or []:
        for b in s["draft"]:
            if b["info"] != layout.MARKDOWN_INFO:
                continue
            at = text.find(b["text"])
            if at >= 0:
                spans.append((at, at + len(b["text"])))
            drafted |= set(lineages(b["text"]))
    return spans, drafted


def drafted_heading(target, found, drafted):
    """Whether a section a Draft cites is one a Draft creates: its lineage ends with a heading's lineage a Draft holds,
    and what stands above it is a section the file holds as it stands, or none."""
    for lineage in drafted:
        if target == lineage:
            return True
        if target.endswith(" § " + lineage) and target[:-len(" § " + lineage)] in found:
            return True
    return False


def citation_file(path, root, target, head, kept):
    """-> (file, note): the file a citation names, found in the files as they stand; while a send-back's or a
    design reassessment's kept changes stand, head the last commit's tree and kept the paths they change, found in the files
    at the last commit, a file they moved or removed among them, and a working file, which no commit holds, alone found
    as it stands."""
    if head is None:
        return resolve(path, root, target)
    found, note = resolve(path, head, target)
    if found is not None or note != "no such file":
        return found, note
    here, _ = resolve(path, root, target)
    if here is not None and here.relative_to(root).as_posix() not in kept:
        return here, ""
    return None, "no such file at the last commit"

def citation_miss(target, found):
    """-> why a section is missing from a file's lineages: a wrong ancestor is a different fix from a wrong title, so
    say which."""
    leaf = target.split(" § ")[-1]
    near = [f for f in found if f.split(" § ")[-1] == leaf]
    return f"right title, wrong lineage: {near[0]}" if near else "no such heading"


def report(heading, problems):
    """Print a check's problems under its heading; -> its exit status."""
    print("== " + heading)
    for title, problem in problems:
        print("%s\n  %s" % (title, problem))
    print("%d problem%s\n" % (len(problems), "" if len(problems) == 1 else "s"))
    return 1 if problems else 0


def design_file(value):
    design = Path(value)
    if not design.is_file():
        sys.stderr.write("no design document: %s\n" % value)
        return None
    return design


def named_places(text):
    """-> each place a step's What names, a citation with a path to a file or a directory, as
    specs/methodology/sourcing-and-citation/writing-a-citation.md § Writing a Citation writes one."""
    return [p for p in cited_places(text) if "/" in p[0] or re.search(r"\.\w+$", p[0])]


def reaches(a, b):
    """Whether place a reaches place b, as a What reaches an Area: a is b, lies within it or holds it, a directory
    holding each file under it and a part a keyed instance holds lying within its section."""
    inside = lambda x, y: x[0] == y[0] or (y[0].endswith("/") and x[0].startswith(y[0]))
    within = lambda x, y: inside(x, y) and (y[1] is None or (x[1] is not None and (x[1] == y[1] or x[1].startswith(y[1] + " § "))))
    return within(a, b) or within(b, a)


# @canon-spec specs/methodology/working-files/main.md § A Design Document § Assessed Area
# @canon-spec specs/methodology/working-files/main.md § A Design Document § The Record's Checks
def lineage_problems(design, text, plan=None):
    """-> each break of the lineage from research to the steps, the Lineage check of working-files/main.md § A Design
    Document § The Record's Checks, read against the Read Assessments of the reports of the handed-off judgments the design's log names,
    but those read_entries leaves out: a place a step's What names reaching no Assessed Area whose Impact holds
    `changes`; such an Assessed Area no What reaches; an Assessed Area whose Impact and Assessment are not those of the
    latest Read Assessment of its Area, an Assessment naming a report the review does not read reported once for the
    report; and an Area whose latest Read Assessment holds an Impact other than `none` neither an Assessed Area nor, its
    Impact holding `changes`, named right after the bold lead-in of an item of the Out of Scope or, a canon design's
    alone holding the section, of the Impact on the Application Specs. None where the frame
    holds no Assessed Areas yet, its form reported apart."""
    body = frame_parts(text).get(AREAS)
    if body is None or body.strip() == NOT_YET_STATED or records_read(body) is None:
        return []
    plan = plan or read_plan(text)
    root = repo_root()
    entries = log_entries(text)
    reports = [(rel_to(report_file(design, entries[i][0], entries[i][1]), root),
                load_report(design, entries[i][0], entries[i][1])) for i in read_entries(entries, steer_changes(text), design)]
    latest = {}
    for path, rep in reports:
        for ra in rep["records"].get("Read Assessments", []):
            place = place_of(ra.get("Area", ""))
            if place:
                latest[place_key(place)] = (path, sorted(names_of_text(ra.get("Impact", ""))), place)
    problems = []
    areas = [(place_of(a), a, impact, place_of(assessment)) for a, impact, assessment in plan["areas"]]
    changing = [p for p, _, impact, _ in areas if p and "changes" in impact]
    whats = [(s["name"], named_places(str(record_types.value_of(s["fields"]["What"]))))
             for s in plan["steps"] if "What" in s["fields"]]
    for step, places_ in whats:
        problems += ["design plan step %s's What names %s, which reaches no Assessed Area whose Impact holds changes"
                     % (step, cite(p)) for p in dict.fromkeys(places_) if not any(reaches(p, a) for a in changing)]
    named_anywhere = [p for _, ps in whats for p in ps]
    problems += ["assessed area %s holds changes, and no step's What reaches it" % cite(p)
                 for p in changing if not any(reaches(w, p) for w in named_anywhere)]
    read = {path for path, _ in reports}
    unread = collections.OrderedDict()
    for p, area, impact, assessment in areas:
        if not p:
            continue
        if assessment and assessment[0] not in read:
            unread.setdefault(assessment[0], []).append(area)
            continue
        found = latest.get(place_key(p))
        if found is None:
            problems.append("assessed area %s has no Read Assessment of its Area in the reports the validation review reads" % cite(p))
            continue
        if sorted(impact) != found[1]:
            problems.append("assessed area %s's Impact is %s, not %s, the Impact of the latest Read Assessment of its Area, in %s"
                            % (cite(p), ", ".join(impact) or "none", ", ".join(found[1]) or "none", found[0]))
        if assessment and assessment[0] != found[0]:
            problems.append("assessed area %s's Assessment is %s, not %s, the report holding the latest Read Assessment of its Area"
                            % (cite(p), assessment[0], found[0]))
    problems += ["%d assessed area%s rest%s on %s, a report the validation review does not read: no handed-off-judgment "
                 "entry of the design's current major version names it, its check was cut short, or its entry stands after the last plan-approval entry with neither an "
                 "entered entry nor a steer entry changing the goals or a part of the frame after that"
                 % (len(a), "" if len(a) == 1 else "s", "s" if len(a) == 1 else "", path) for path, a in unread.items()]
    held = {place_key(p) for p, _, _, _ in areas if p}
    items = (section(text, "Out of Scope") or "") + "\n" + (section(text, IMPACT) or "")
    left_out = {place_key(p) for p in (place_of("`%s`" % m) for m in re.findall(
        r"^\s*- \*\*[^\n]+?\*\*\s*`([^`]+)`", items, re.M)) if p}
    for key, (path, impact, place) in latest.items():
        if impact and impact != ["none"] and key not in held and not ("changes" in impact and key in left_out):
            problems.append("%s, assessed %s in %s, is neither an Assessed Area nor, its Impact holding changes, named right "
                            "after the bold lead-in of an item of the Out of Scope or of the Impact on the Application "
                            "Specs" % (cite(place), ", ".join(impact), path))
    return problems


def names_of_text(value):
    """-> the items of a list field's value as the one reader gives it, one to a line, backticks and list markers aside."""
    return [l.strip(" -`") for l in str(value or "").split("\n") if l.strip(" -`")]


def design_problems(design):
    """The validation review's checks on one design: its form, its records, the references within it, the lineage from
    research to its steps and each construct a step's Draft holds, drawing only on the document, the reports of the
    handed-off judgments its log names, but those read_entries leaves out, the canon's declarations of its form and, for
    a Draft's constructs, the specs as they stand, per working-files/main.md § A
    Design Document § The Record's Checks; by validating, no goal, no part of its frame and no step section not yet stated. Any problem a
    declaration reports counts, so a type that cannot be read stops a stamp."""
    name, fields, _, text = read_design(design)
    found = check_form(design)[1] + steer_table_problems(None)
    found += [(name, p) for p in lineage_problems(design, text)]
    # working-files/main.md § A Check's Report § Script Checks [Name: research-covers-its-matches] and
    # [Name: goals-searched-over-every-durable-file], over the research reports the validation review reads, of a design
    # not yet approved alone: once the plan is approved the frame is frozen and the files come to hold the apply's
    # writing, so research taken in from then on is held as the entry of the round taking it in is appended
    approved = dict(fields).get("Status") in ("approved", "applying", "complete")
    if not approved:
        entries = log_entries(text)
        read_ = research_indexes(design, entries, read_entries(entries, steer_changes(text), design))
        found += [(name, "%s (%s)" % (msg, rule)) for rule, msg in
                  union_coverage_problems(repo_root(), design, text, entries, among=read_)
                  + goals_searched_problems(repo_root(), design, text, entries, among=read_)]
    found += [(name, p) for p in item_citation_problems(text)]
    if not approved:
        found += [(name, "its design frame's %s is not yet stated" % p) for p in FRAME if not_stated(frame_parts(text).get(p))]
        if (section(text, "Design Goals") or "").strip() == NOT_YET_STATED:
            found.append((name, "its design goals are not yet stated"))
        if (section(text, "Design Plan Steps") or "").strip() == NOT_YET_DRAFTED:
            found.append((name, "its steps are not yet drafted"))
    return found


# @canon-spec specs/methodology/working-files/main.md § A Design Document § The States It Moves Through § A Send-back
# @canon-spec specs/methodology/working-files/main.md § Design Plan Step § Step Objective
def check_cited_headings(proposal):
    """--check-cited-headings: each heading a proposal cites resolved against the files as they stood before its
    apply. Those are the files as they stand, but in two cases, each read at the last commit: for a design that is
    applying, whose plan was written before the apply's writing, so a heading its own apply removed or retitled is
    not reported; and for a design whose send-back's or design reassessment's changes are kept, each Area its current
    major version's research assessed read among its citations; -> 1 where one is broken, 2 where none is cited."""
    root, kept, extra = Path.cwd(), (), ""
    if Path(proposal).is_file() and is_design(Path(proposal)):
        root = repo_root()
        text = read(Path(proposal)).replace("\r\n", "\n")
        applying = is_applying(text)
        kept = tuple(uncommitted_changes(root) if applying else [] if over_applied(log_entries(text)) else kept_changes(root, text))
        if kept and not applying:
            entries = log_entries(text)
            extra = "\n".join(a.get("Area", "") for i in read_entries(entries, steer_changes(text), Path(proposal))
                              for a in load_report(Path(proposal), entries[i][0], entries[i][1])["records"]["Read Assessments"])
    try:
        results = check_citations(proposal, root, kept, extra)
    except OSError as exc:
        sys.stderr.write("cannot read proposal: %s\n" % exc)
        return 2
    if not results:
        sys.stderr.write("no cross-file citations found\n")
        return 2
    print("== check-cited-headings")
    width, failed = max(len(p) for _, p, _, _ in results), 0
    for ok, path, target, note in results:
        if not ok:
            failed += 1
        print("%-9s %-*s  § %s" % ("ok" if ok else "BROKEN", width, path, target))
        if note:
            print("%s\\- %s" % (" " * 10, note))
    print("%d citation%s, %d broken\n" % (len(results), "" if len(results) == 1 else "s", failed))
    return 1 if failed else 0


def check_design_form(value):
    design = design_file(value)
    return 2 if design is None else report("check-design-form " + design.stem, check_form(design)[1])


def check_target_kind(value):
    design = design_file(value)
    return 2 if design is None else report("check-target-kind " + design.stem, check_kind(design, Path.cwd())[1])


# @canon-spec specs/methodology/working-files/main.md § A Design Document
STEER_CITED = re.compile(r"§ Steering Decisions \[Name: ([^\]]+)\]")


def item_citation_problems(text):
    """The Out of Scope check of working-files/main.md § A Design Document § The Record's Checks: each item of the
    design's Out of Scope, a list item opening at the line's start, cites a steer of its Steering Decisions whose Changes
    holds `Out of Scope item`, read of this design alone."""
    changes = steer_changes(text)
    out = []
    for item in re.split(r"(?m)^- ", section(text, "Out of Scope") or "")[1:]:
        if not any(OUT_OF_SCOPE_ITEM in changes_parts(changes.get(n.strip())) for n in STEER_CITED.findall(item)):
            out.append("its Out of Scope item %s cites no steer whose Changes holds `%s`"
                       % (item.split("\n")[0].strip()[:80], OUT_OF_SCOPE_ITEM))
    return out


def check_design(value):
    design = design_file(value)
    return 2 if design is None else report("check-design " + design.stem, design_problems(design))


def plan_parts(text):
    """-> the design's parts in the order specs/AGENTS.md § Design, Refactor, Refine § Measure Twice, Cut Once § The Order
    of a Design's Parts gives a change, as [(label, kind, Name, [0-based lines])]: its goals; its frame, each case of its
    Scope then the rest of the Scope, its Assessed Areas, each principle of its Approach, then its Frame Outcomes; then
    its steps in their Depends On Steps order, each followed by its Objectives."""
    lines, found, out = text.split("\n"), sections(text), []

    def records_in(lineage, key, field="Records"):
        if lineage not in found:
            return []
        h, end = found[lineage]
        return [(str(record_types.value_of(values_of(it)[key])).strip(), [h + 1 + n for n in it["lines"]])
                for it in records_read("\n".join(lines[h + 1:end]), field) or [] if key in values_of(it)]

    def framed(part, field, label):
        # a frame part's records under field, each by its Name, then the rest of the part
        noun = label.split(" ", 1)[1]
        recs = records_in(frame + part, "Name", field)
        own = {n for _, ls in recs for n in ls}
        h, end = found.get(frame + part, (0, 0))
        rest = [n for n in range(h + 1, end) if n not in own and lines[n].strip()]
        return [(noun + " " + n, noun, n, ls) for n, ls in recs] + [("the rest of the " + part, part.lower(), None, rest)]

    out += [("goal " + n, "goal", n, ls) for n, ls in records_in("Design Goals", "Name")]
    frame = "The Design Frame § "
    out += framed(*FRAME_RECORDS[0][:3])
    out += [("assessed area " + a, "area", a, ls) for a, ls in records_in(frame + "Assessed Areas", "Area")]
    out += framed(*FRAME_RECORDS[1][:3])
    out += [("frame outcome " + n, "outcome", n, ls) for n, ls in records_in(frame + "Frame Outcomes", "Name")]
    steps = [s for s in read_steps(text) or [] if s["name"]]
    placed, ordered = set(), []
    while len(ordered) < len(steps):
        # each step after the steps it depends on, else in the order the design holds them; a loop is reported apart
        left = [s for s in steps if s["name"] not in placed]
        needs = lambda s: set(names_of(s["fields"]["Depends On Steps"]) or []) - {"none"} if "Depends On Steps" in s["fields"] else set()
        ready = [s for s in left if needs(s) <= placed] or left
        ordered.append(ready[0])
        placed.add(ready[0]["name"])
    for s in ordered:
        out.append(("step " + s["name"], "step", s["name"], s["lines"]))
        out += [("step objective %s, of step %s" % (ob["name"], s["name"]), "objective", ob["name"], sorted(ob["lines"]))
                for ob in s["objectives"] if ob["name"]]
    return [p for p in out if p[3]]


def show_dependents(value):
    """--show-dependents DESIGN NAME: each part of the design naming or citing the goal, case, principle, Frame
    Outcome, step or step Objective NAME names, in the order a change runs down; writes no file and decides nothing;
    -> 0, or 2 where the design or NAME is not found."""
    path, name = value
    design = design_file(path)
    if design is None:
        return 2
    text = read(design).replace("\r\n", "\n")
    lines, parts = text.split("\n"), plan_parts(text)
    name = name.strip().strip("`")
    target = next((p for p in parts if p[2] == name and p[1] != "area"), None)
    if target is None:
        sys.stderr.write("%s holds no goal, case, principle, Frame Outcome, step or step Objective named %s\n"
                         % (design.name, name))
        return 2
    naming = re.compile(r"(?<![\w-])%s(?![\w-])" % re.escape(name))
    print("== show-dependents %s %s (%s)" % (design.stem, name, target[0]))
    count = 0
    for label, _, _, own in parts:
        if (label, own) == (target[0], target[3]):
            continue
        at = [n + 1 for n in own if naming.search(lines[n])]
        if at:
            count += 1
            print("%s: line%s %s" % (label, "" if len(at) == 1 else "s", ", ".join(map(str, at))))
    print("%d part%s name%s or cite%s %s\n" % (count, "" if count == 1 else "s", "s" if count == 1 else "",
                                               "s" if count == 1 else "", name))
    return 0


def plans_folder(value, heading):
    """-> the plans directory, or an exit status: 2 for a directory given that is not there or is no plans folder,
    since no design standing outside the plans folders is read as a design of the workstack, and 0 when the default
    is not there yet, since no design has been written."""
    folder = Path(value)
    if not is_plans_folder(folder):
        sys.stderr.write("no plans folder, a skill's plans directory under .ai/plans/: %s\n" % folder)
        return 2
    # the skill's own folder not there yet still reads the plans folders beside it
    if folder.is_dir() or (value == PLANS and folder.parent.is_dir()):
        return folder
    if value != PLANS:
        sys.stderr.write("no plans directory: %s\n" % folder)
        return 2
    print("== %s\n0 design documents: %s is not there yet\n" % (heading, folder))
    return 0


def show_workstack(value):
    folder = plans_folder(value, "show-workstack")
    if not isinstance(folder, Path):
        return folder
    print("== show-workstack\n" + "\n".join(check_stack(folder)[0]) + "\n")
    return 0


def check_workstack(value):
    folder = plans_folder(value, "check-workstack")
    return folder if not isinstance(folder, Path) else report("check-workstack", check_stack(folder)[1])


# @canon-spec specs/methodology/working-files/main.md § A Check's Report § Kinds of Builder Check
def show_design(value):
    """--show-design DESIGN: shows the header and the goals of one design standing in a plans folder, and nothing else
    of it, so a builder learns what a design it links to decides without opening it. DESIGN is the design's file, or
    its name as a Depends On Designs of the skill's own plans folder names it. The design is found among those
    read_designs gives, so one standing in no plans folder, in an `archive/` beneath one among them, is not shown.
    Its header is held to its form by header_problems and its goals by sections_owed and goals_problems, the checks
    check_form makes of them: where they report, each field the design holds is still shown as far as it reads, and
    each field missing or not valid is named after them. Writes no file; -> 0 where the header and the goals hold the
    form, 1 where a field is missing or not valid or the design stands in no plans folder."""
    given = Path(value)
    by_file = given.is_file()
    folder = given.resolve().parent if by_file else Path(PLANS).resolve()
    name = given.stem if by_file else "; ".join(named(rename(str(value), folder.name, folder.name)))
    held = {n: (fields, sections, text) for n, fields, sections, text in read_designs(folder)}
    if name not in held:
        print("== show-design %s\nno design of that name stands in a plans folder, so nothing of it is shown (%s)\n"
              % (name or value, BLOCKS_RULE))
        return 1
    fields, sections, text = held[name]
    values = dict(fields)
    # the design's file, which gives its header's Name and Kind what they are held to: a name holding a slash is of
    # another skill's plans folder, beside this one
    design = given if by_file else Path("%s.md" % ((folder.parent if "/" in name else folder) / name))
    goals = section(text, "Design Goals")
    problems = header_problems(design, fields, text)
    problems += ["it holds no Design Goals section"] if goals is None and "Design Goals" in sections_owed(sections, values) else []
    problems += goals_problems(goals, values)
    print("== show-design %s [%s]" % (name, values.get("Status") or "no Status"))
    for key, held_value in fields:
        print("%s: %s" % (key, held_value))
    print("Design Goals:")
    shown = [rec for rec in records(goals) or [] if rec] if goals is not None else []
    for rec in shown:
        print("\n".join("  %s%s: %s" % ("- " if i == 0 else "  ", k, " ".join(v.split())) for i, (k, v) in enumerate(rec)))
    if not shown:
        # goals not held as records are shown as the section holds them, `Not yet stated.` among them
        stated = " ".join(goals.split()) if goals is not None and records(goals) is None else ""
        print("  " + (stated or "none held"))
    if problems:
        print("Missing or not valid, so the design is old and suspect, and stays as it is until its own builder takes it up:")
        print("\n".join("  " + p for p in problems))
    print("%d problem%s\n" % (len(problems), "" if len(problems) == 1 else "s"))
    return 1 if problems else 0


# @canon-spec specs/methodology/working-files/main.md § A Design Document § What Blocks What § Freeing a Design
def check_design_names(value):
    """--check-design-names DESIGN: reports each design the design's own Depends On Designs names that is finished or
    gone, and which of the two, read from the plans folders as they stand, so a misspelled name is seen before
    --free-design writes anything; lists beside them each unfinished design it names, which blocks it; reports a
    design standing in no plans folder, which no action works; a complete or an abandoned design's names are its
    history, and none is reported; writes no file; -> 0, 1 where it reports, 2 where the design is not found."""
    design = design_file(value)
    if design is None:
        return 2
    names = own_names(design)
    if names is None:
        return report("check-design-names " + design.stem, [(design.stem, NO_PLANS_FOLDER)])
    status = dict(read_design(design)[1]).get("Status", "")
    print("== check-design-names %s [%s]" % (design.stem, status or "no Status"))
    if status in FINISHED:
        print("%s, so each design its Depends On Designs names is its history, and nothing follows from it\n0 problems\n" % status)
        return 0
    for d, reading in names:
        if reading == UNFINISHED_NAME:
            print("blocked by %s, unfinished: it is worked no further than its agreed goals and frame" % d)
    problems = [(design.stem, "its Depends On Designs names %s, %s: %s; its foundation has changed, and --free-design frees "
                              "it before any other act on it (%s)"
                 % (d, reading, "a design of that name stands in a plans folder complete or abandoned" if reading == FINISHED_NAME
                    else "no design of that name stands in a plans folder", BLOCKS_RULE))
                for d, reading in names if reading != UNFINISHED_NAME]
    for title, problem in problems:
        print("%s\n  %s" % (title, problem))
    print("%d problem%s\n" % (len(problems), "" if len(problems) == 1 else "s"))
    return 1 if problems else 0


# @canon-spec specs/methodology/working-files/main.md § A Design Document § What Blocks What § Freeing a Design
# @canon-spec specs/methodology/working-files/main.md § Design Log Entry
def free_design(value):
    """--free-design DESIGN: frees the design of each finished or gone design its Depends On Designs names, read from
    the plans folders as they stand, writing that design alone, once: it removes each such name; where the user's
    agreement to its goals stands in its log in its current major version, it appends the `design-reassessment`
    entry, its Cause a changed foundation naming each design it was freed from and whether that design finished or
    is gone; and where the design then stood approved or applying, it moves its Status to in-progress and appends the
    `entered` entry of that move, its Reason freed. A complete or an abandoned design, one naming no finished or gone
    design and one standing in no plans folder are left as they stand; -> 0, 1 where the design stands in no plans
    folder, 2 where it is not found."""
    design = design_file(value)
    if design is None:
        return 2
    names = own_names(design)
    if names is None:
        return report("free-design, not freed", [(design.stem, NO_PLANS_FOLDER)])
    raw = design.read_bytes().decode("utf-8")
    text = raw.replace("\r\n", "\n")
    status = dict(read_design(design)[1]).get("Status", "")
    changed = [(d, reading) for d, reading in names if reading != UNFINISHED_NAME]
    print("== free-design %s [%s]" % (design.stem, status or "no Status"))
    if status in FINISHED:
        print("%s, so it is never written: each design its Depends On Designs names is its history\n" % status)
        return 0
    if not changed:
        print("its Depends On Designs names no finished or gone design, so nothing is written\n")
        return 0
    kept = [d for d, reading in names if reading == UNFINISHED_NAME]
    m = re.search(r"^\*\*%s:\*\*[ \t]*(.*?)([ \t]*\\)?[ \t]*$" % DEPENDS_ON, text, re.M)
    text = text[:m.start()] + "**%s:** %s%s" % (DEPENDS_ON, "; ".join(kept) or "none", m.group(2) or "") + text[m.end():]
    print("freed of %s; its Depends On Designs now %s" % ("; ".join("%s, %s" % c for c in changed), "; ".join(kept) or "none"))
    entries = log_entries(text)
    if not agreed_before(entries, len(entries)):
        print("its goals are not agreed in its current major version, so no entry is appended: its work goes on from its Problem\n")
        write_design(design, raw, text)
        return 0
    cause = "%s: %s" % (CHANGED_FOUNDATION, "; ".join("%s %s" % c for c in changed))
    text, block = with_entry(text, DESIGN_REASSESSMENT, [(CAUSE, cause)])
    blocks = [block]
    if status in ("approved", "applying"):
        text = re.sub(r"^(\*\*Status:\*\*[ \t]*)%s\b" % status, r"\1in-progress", text, count=1, flags=re.M)
        text, block = with_entry(text, "entered", [("Reason", FREED)])
        blocks.append(block)
        print("moved back from %s to in-progress" % status)
    write_design(design, raw, text)
    print("reassessed, its goals to agree again:\n" + "\n".join(blocks) + "\n")
    return 0


def show_validation(value):
    design = design_file(value)
    if design is None:
        return 2
    name, fields, _, text = read_design(design)
    state, stamped, current = validation(text, fields)
    print("== show-validation\n%s: %s; stamped %s, content now %s\n" % (name, {"none": "never stamped"}.get(state, state), stamped or "none", current))
    return 0


def stamp_validation(value):
    design = design_file(value)
    if design is None:
        return 2
    # working-files/main.md § A Design Document § What Blocks What: a design in no plans folder is written by no action
    if own_names(design) is None:
        return report("stamp-validation, not stamped", [(design.stem, NO_PLANS_FOLDER)])
    name, fields, _, text = read_design(design)
    if validation(text, fields)[0] == "validated":
        print("== stamp-validation\nalready validated, the stamp current: %s\n" % dict(fields)["Validated"])
        return 0
    # every check but the stamp's own absence, which this is about to write; the design's place in the workstack is
    # --check-workstack's, which runs before each validation
    problems = [(t, p) for t, p in design_problems(design) if not re.search(r"validation review (has )?stamped", p)]
    if problems:
        report("stamp-validation, not stamped", problems)
        return 1
    raw = design.read_bytes().decode("utf-8")
    new, n = re.subn(r"^\*\*Validated:\*\*.*$", lambda m: "**Validated:** " + stamp(text) + (" \\" if m.group(0).rstrip().endswith("\\") else ""), text, count=1, flags=re.M)
    if not n:
        print("== stamp-validation\nno Validated field to stamp\n")
        return 1
    write_design(design, raw, new)
    print("== stamp-validation\n" + re.search(r"^\*\*Validated:\*\*.*$", new, re.M).group(0) + "\n")
    return 0


# @canon-spec specs/methodology/working-files/main.md § A Design Document § The Design's Version
def with_version(text, version):
    """-> a design's text with its header's Version set to version, the field added right after its Name where it holds
    none, and left out at 0.1.0, its default."""
    head, sep, rest = text.partition("\n## ")
    if version == version_text(FIRST_VERSION):
        head = re.sub(r"( \\)?\n\*\*Version:\*\* \S+( \\)?$", lambda m: m.group(2) or "", head, count=1, flags=re.M)
    elif re.search(r"^\*\*Version:\*\* ", head, re.M):
        head = re.sub(r"^(\*\*Version:\*\* )\S+", lambda m: m.group(1) + version, head, count=1, flags=re.M)
    else:
        head = re.sub(r"^(\*\*Name:\*\* [^\n]*?)( \\)?$", lambda m: m.group(1) + " \\\n**Version:** " + version + (m.group(2) or ""),
                      head, count=1, flags=re.M)
    return head + sep + rest


LOG_RULE = WF_LOG = "specs/methodology/working-files/main.md § Design Log Entry"
CUTS_SHORT = "Cuts Short"
DIAGNOSIS_RULE = "specs/methodology/working-files/main.md § A Diagnosis § Script Checks [Name: diagnosis-whole-and-in-form]"
# @canon-spec specs/methodology/working-files/main.md § A Diagnosis
# a diagnosis's Title fields, as its parts table gives them, and the fields a Root Cause record requires, as its
# record type declares them
DIAGNOSIS_FIELDS = ("Design", "Design Reassessment", "Flaw Set", "Earlier Diagnoses")
ROOT_CAUSE_FIELDS = ("Root Cause", "Question", "Description", "Account")


def design_folder(design):
    """-> a design's folder of working files, `.ai/tmp/<skill-name>/<design>/`."""
    return design.parents[2] / "tmp" / design.parent.name / design.stem


# @canon-spec specs/methodology/design-workflow/order-of-a-designs-work.md § The Order of a Design's Work § Facts
def fact_values(name, root=None):
    """-> the quoted Values of a Fact the design's work states declare."""
    body = read((root or repo_root()) / "specs/methodology/design-workflow/order-of-a-designs-work.md")
    m = re.search(r"- \*\*Name:\*\* %s \\\n(?:\s+\*\*[A-Za-z ]+:\*\*[^\n]*\n)*?\s+\*\*Values:\*\* ([^\n]*)" % re.escape(name), body)
    return tuple(re.findall(r'"([^"]+)"', m.group(1))) if m else ()


def diagnosis_file(design, entry_fields):
    """-> the diagnosis a `design-reassessment` entry's Diagnosis names, a path in the design's folder, given from the
    repository's root or from the folder."""
    value = entry_fields.get("Diagnosis", "").strip().strip("`")
    root, folder = repo_root(), design_folder(design)
    for path in (root / value, folder / value):
        if value and path.is_file():
            return path
    return None


def read_diagnosis(text):
    """-> (its title's fields {key: value}, its Flaws [{field: value}], its Root Causes [{field: value}], its Scope's
    fields {key: value}, the level-two headings it holds) of a diagnosis."""
    text = text.replace("\r\n", "\n")
    head = text.split("\n## ", 1)[0]

    def block(part):
        return {m.group(1): m.group(2).strip() for m in re.finditer(r"^\*\*([^*]+):\*\*[ \t]*(.*?)(?:[ \t]*\\)?[ \t]*$", part, re.M)}
    recs = lambda name: [{k: str(v).strip() for k, v in r} for r in records(section(text, name)) or []]
    return (block(head) if head.startswith("# Diagnosis") else None, recs("Flaws"), recs("Root Causes"),
            block(section(text, "Scope") or ""), [title for title, _ in level_two(text)])


# @canon-spec specs/methodology/working-files/main.md § A Diagnosis § Script Checks [Name: diagnosis-whole-and-in-form]
def flaw_set(design, entries):
    """-> {(kind, n, Finding)} for each finding a Settlement of the design's checks keeps as a design flaw or an
    implementation flaw, read from the reports of every major version, a report cut short among them."""
    kinds = log_type()[2]
    return {(k, n, f) for k, n, _ in entries if "Model" in kinds.get(k, ())
            for f, verdict in last_words(load_report(design, k, n)).items() if verdict in FLAWS}


FLAW_KEY = re.compile(r"([a-z-]+)/(\d+)\.md\s*(?:§[^\[]*)?\[Finding:\s*([^\]]+?)\s*\]")


# @canon-spec specs/methodology/working-files/main.md § A Diagnosis § Script Checks [Name: diagnosis-whole-and-in-form]
def diagnosis_problems(root, design, text, count, entry_fields):
    """-> problems with the diagnosis a `design-reassessment` entry whose Cause is a step back names, the entry being
    appended to the design's text as its count among its kind: one standing in the design's folder at
    `diagnosis/{n}.md`, n counting the diagnoses the design's `design-reassessment` entries name, whatever the count of
    the entry naming it; its title's fields and its parts as its form gives them, its Design Reassessment the entry
    naming it; a Flaw for each finding of its flaw set, each holding its Still Applies, its Root Cause, that Root Cause
    one the diagnosis holds, and its Why Not where it no longer applies; each Root Cause holding its fields; and its
    Scope its Question and Answer."""
    path = diagnosis_file(design, entry_fields)
    entries = log_entries(text)
    nth = 1 + sum(1 for k, _, f in entries if k == DESIGN_REASSESSMENT and "Diagnosis" in f)
    want = design_folder(design) / "diagnosis" / ("%d.md" % nth)
    if path is None:
        return ["the design-reassessment entry's Diagnosis names no diagnosis standing in the design's folder: %s (%s)"
                % (entry_fields.get("Diagnosis", "none"), DIAGNOSIS_RULE)]
    if path.resolve() != want.resolve():
        return ["the design-reassessment entry's Diagnosis is %s, not %s, diagnosis %d of the diagnoses the design's "
                "design-reassessment entries name (%s)" % (rel_to(path, root), rel_to(want, root), nth, DIAGNOSIS_RULE)]
    title, flaws, causes, scope, parts = read_diagnosis(read(path))
    out = []
    if title is None:
        return ["%s does not open with its title, # Diagnosis (%s)" % (rel_to(path, root), DIAGNOSIS_RULE)]
    if list(title) != list(DIAGNOSIS_FIELDS):
        out.append(constructs.block_refusal("its title", list(title), list(DIAGNOSIS_FIELDS), DIAGNOSIS_FIELDS, owner="its form"))
    elif title["Design Reassessment"].strip("`") != "%s-%d" % (DESIGN_REASSESSMENT, count):
        out.append("its Design Reassessment is %s, not %s-%d, the entry naming it" % (title["Design Reassessment"], DESIGN_REASSESSMENT, count))
    if parts != ["Flaws", "Root Causes", "Scope"]:
        out.append(constructs.block_refusal("the diagnosis", parts, ["Flaws", "Root Causes", "Scope"], noun="part", owner="its form"))
    if list(scope) != ["Question", "Answer"] or not all(scope.values()):
        out.append("its Scope holds %s, not its Question and its Answer" % (", ".join(scope) or "no field"))
    keys = {c.get("Root Cause", "") for c in causes}
    for c in causes:
        missing = [f for f in ROOT_CAUSE_FIELDS if not c.get(f)]
        out += ["Root Cause %s holds no %s" % (c.get("Root Cause", "?"), f) for f in missing]
    held = set()
    for f in flaws:
        key = f.get("Flaw", "")
        m = FLAW_KEY.search(key)
        if m:
            held.add((m.group(1), int(m.group(2)), m.group(3).strip()))
        applies = f.get("Still Applies", "").strip("`")
        if applies not in ("yes", "no"):
            out.append("Flaw %s's Still Applies is neither yes nor no: %s" % (key, applies or "none"))
        elif applies == "no" and not f.get("Why Not"):
            out.append("Flaw %s no longer applies, and holds no Why Not" % key)
        if not f.get("Root Cause"):
            out.append("Flaw %s holds no Root Cause" % key)
        elif f.get("Root Cause").strip("`") not in keys:
            out.append("Flaw %s names the Root Cause %s, which the diagnosis does not hold" % (key, f.get("Root Cause")))
    out += ["it leaves out %s/%d.md [Finding: %s], a finding of its flaw set" % k
            for k in sorted(flaw_set(design, entries) - held)]
    return ["%s: %s (%s)" % (rel_to(path, root), p, DIAGNOSIS_RULE) for p in out]


def write_design(design, raw, new):
    """Write a design's new text, keeping the line endings its file had."""
    design.write_bytes((new.replace("\n", "\r\n") if "\r\n" in raw else new).encode("utf-8"))


# @canon-spec specs/methodology/working-files/main.md § Design Log Entry
def next_count(text, kind):
    """-> the count an entry of kind appended to a design's text takes, among its kind from 1."""
    return 1 + len(re.findall(r"^\s*- \*\*Entry:\*\* %s-\d+(?: \\)?\s*$" % re.escape(kind), section(text, LOG) or "", re.M))


# @canon-spec specs/methodology/working-files/main.md § A Design Document § The Design's Version
# @canon-spec specs/methodology/working-files/main.md § Design Log Entry
def with_entry(text, kind, fields, read_version=None):
    """-> (a design's text with an entry of kind holding fields, [(field, value)], appended to its log, the entry as
    it is written): the entry takes its count among its kind and the UTC time it is appended; the header's Version is
    set to the version the log gives with the entry appended; the entry is stamped at the version its work read, a
    check's the version its report read, read_version, and any other's the version as it is appended, each left out
    at 0.1.0, its default; and the log's section is created where the design holds none, where the form puts it."""
    count, body = next_count(text, kind), section(text, LOG)
    now = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    version = version_text(design_version(log_entries(text) + [(kind, count, dict(fields))], steer_changes(text)))
    text = with_version(text, version)
    at = version_text(read_version) if read_version is not None else version
    stamp = [] if at == version_text(FIRST_VERSION) else ["  **%s:** %s" % (VERSIONED, at)]
    # modeling-constructs.md § Fields: the entry a record, an item two spaces beyond its key, each line a line opening
    # a field's key follows ending with a space and a backslash
    own = ["- **Entry:** %s-%d" % (kind, count), "  **Timestamp:** " + now] + stamp + ["  **%s:** %s" % f for f in fields]
    block = "\n".join("  " + l + (" \\" if n < len(own) - 1 else "") for n, l in enumerate(own))
    if body is not None and not re.search(r"^\*\*Records:\*\*\s*$", body, re.M):
        # a section copied from the form holds its placeholder alone, which the first entry replaces
        m = part_span(text, LOG)
        text = text[:m[0]] + text[m[1] + len(body):].lstrip("\n")
        body = None
    if body is None:
        # the section stands where the form puts it, before the sections that follow it
        after = SECTIONS[SECTIONS.index(LOG) + 1:]
        m = next((m for m in (part_span(text, s) for s in after) if m), None)
        start = m[0] if m else len(text.rstrip("\n")) + 1
        return text[:start] + "## %s\n\n**Records:**\n%s\n\n" % (LOG, block) + text[start:], block
    m = part_span(text, LOG)
    end = m[1] + len(body)
    return text[:m[1]] + body.rstrip("\n") + "\n\n" + block + "\n" + ("\n" if end < len(text) else "") + text[end:], block


# @canon-spec specs/methodology/working-files/main.md § A Design Document § What Blocks What
# @canon-spec specs/methodology/working-files/main.md § Design Log Entry
# @canon-spec specs/methodology/working-files/main.md § Design Log Entry § Script Checks [Name: counts-taken-from-the-report]
# @canon-spec specs/methodology/working-files/main.md § Design Log Entry § When an Entry Is Appended
def log_entry(value):
    """--log-entry DESIGN KIND [FIELD=VALUE ...]: appends an entry to the design's log, its count among its kind and
    the UTC time it is appended, refusing one out of its type; an entry the freeing of a design alone appends; any
    entry to a design standing in no plans folder, or naming a finished or gone design and not yet freed; an entry of
    work past the frame to a design naming an unfinished design, as held_back gives them; and a check's entry until
    its report stands in the design's folder, in its form and its records covering what its check had to cover, its
    counts taken from the report; -> 0, 1 where it is refused, 2 for a usage error."""
    if len(value) < 2:
        sys.stderr.write("--log-entry takes a design document, a kind and the kind's fields as FIELD=VALUE\n")
        return 2
    design = design_file(value[0])
    if design is None:
        return 2
    kind, pairs = value[1], value[2:]
    if any("=" not in p for p in pairs):
        sys.stderr.write("--log-entry: each field is given as FIELD=VALUE\n")
        return 2
    fields = [tuple(s.strip() for s in p.split("=", 1)) for p in pairs]
    values, counts, kinds, declared = log_type()
    if declared or kind not in kinds:
        return report("log-entry, not logged", [(design.stem, p) for p in
                                                     [p for _, p in declared] + entry_problems(kind, fields, values, counts, kinds)])
    # working-files/main.md § Design Log Entry: the old entry and the old field, read only in a log written before
    # them, are written in no entry now
    if kind == OLD_REASSESSMENT:
        return report("log-entry, not logged", [(LOG_RULE, "a `reassessment` entry, written in no entry now: the step "
                                                 "back takes a `step-back` entry, and a design reassessment a "
                                                 "`design-reassessment` entry")])
    if any(k == CUTS_SHORT for k, _ in fields):
        return report("log-entry, not logged", [(LOG_RULE, "a Cuts Short, written in no entry now: a check's report "
                                                 "states how it ended, and the Running Work holds the calls on work "
                                                 "that had handed nothing back")])
    given = [k for k, _ in fields if counts.get(k)]
    if given:
        return report("log-entry, not logged", [(COUNT_RULE, "a count given, which is taken from the check's report "
                                                      "alone: " + ", ".join(given))])
    # working-files/main.md § Design Log Entry: a design reassessment's entry states its cause, and holds what the
    # user decided and its diagnosis where that cause is a step back, and neither for a changed foundation
    held = dict(fields)
    if kind == DESIGN_REASSESSMENT and CAUSE not in held:
        return report("log-entry, not logged", [(LOG_RULE, "a design-reassessment entry holding no Cause: it states "
                                                 "what caused the design reassessment, `%s:` and each design the design "
                                                 "was freed from, or `%s:` and what brought the design to the step back"
                                                 % (CHANGED_FOUNDATION, STEP_BACK))])
    # working-files/main.md § A Design Document § What Blocks What § Freeing a Design: the entries of a design freed
    # for a changed foundation are appended by the freeing alone, with the names it removes
    freeing = (kind == DESIGN_REASSESSMENT and (read_cause(held[CAUSE]) or ("",))[0] == CHANGED_FOUNDATION) \
        or (kind == "entered" and held.get("Reason") == FREED)
    if freeing:
        return report("log-entry, not logged", [(BLOCKS_RULE, "an entry of a design freed for a changed foundation, which "
                                                 "--free-design alone appends, as it removes each name of a finished or "
                                                 "gone design from the design's Depends On Designs")])
    refused = held_back(design, kind)
    if refused:
        return report("log-entry, not logged", [(design.stem, p) for p in refused])
    raw = design.read_bytes().decode("utf-8")
    text = raw.replace("\r\n", "\n")
    count = next_count(text, kind)
    # a check's entry, one holding a Model, names its report, which stands in the design's folder before the entry does
    read_version = None
    if "Model" in kinds[kind]:
        root = repo_root()
        report_path = report_file(design, kind, count)
        if not report_path.is_file():
            return report("log-entry, not logged", [(design.stem, "a check's entry whose report does not stand in "
                                                          "the design's folder: " + rel_to(report_path, root))])
        # working-files/main.md § Design Log Entry § Script Checks [Name: goals-agreed-before-checks]: no check's entry
        # before the agreement of its major version's goals, the major version its report's Reading records, or,
        # where the Reading records none, the design's current one
        so_far = log_entries(text)
        if not agreed_before(so_far + [(kind, count, {})], len(so_far), report_version(load_report(design, kind, count))):
            return report("log-entry, not logged", [(GOALS_AGREED_RULE, "a check's entry with no goals-agreed entry "
                                                     "before it in its major version, the one its report's Reading "
                                                     "records, or the design's current one where it records none")])
        # a self-review's Script Output: its script checks' output and, over applied work, what the kept tests of each
        # script the design's changes hold a file of gave, with the comparison's, each run here and by no check of
        # the settled report made apart from the entry; a test that fails or cannot be run refuses the entry
        unpassed, compared = [], None
        if kind == "self-review":
            output = self_review_output(root, design, text)
            if over_applied(so_far):
                kept_output, unpassed, compared = kept_tests_run(root, {p for p in design_changes(root, text) if not is_working_file(p)})
                output += "$ --check-kept-tests\n" + kept_output
            write_script_output(report_path, output)
        problems, found = entry_report_problems(root, design, text, kind, count, compared=compared)
        problems = [(rule, "%s: %s" % (rel_to(report_path, root), msg)) for rule, msg in unpassed] + problems
        if problems:
            return report("log-entry, not logged", returned_report(root, design, kind, count, report_path) or problems)
        # the entry stamped at the version its report read, one the log held
        # @canon-spec specs/methodology/working-files/main.md § Design Log Entry § Script Checks [Name: entry-at-the-version-read]
        read_version = report_version(found)
        versions_held = [FIRST_VERSION] + versions(so_far, steer_changes(text))
        if read_version is not None and read_version not in versions_held:
            return report("log-entry, not logged", [(ENTRY_AT_VERSION_READ, "%s's Reading holds Design Version %s, a "
                                                     "version the design's log never held"
                                                     % (rel_to(report_path, root), version_text(read_version)))])
        taken = report_counts(found)
        # the kind's fields in the type's order, each count the report's; a field the kind does not give kept, so it
        # is refused as one out of its type
        fields = [(k, str(taken[k])) if counts.get(k) else (k, dict(fields)[k]) for k in kinds[kind]
                  if counts.get(k) or k in dict(fields)] + [(k, v) for k, v in fields if k not in kinds[kind]]
    problems = entry_problems(kind, fields, values, counts, kinds)
    if kind == DESIGN_REASSESSMENT and not problems:
        decisions = fact_values("design reassessment")
        if dict(fields).get("Decision") not in decisions:
            problems.append("a design-reassessment entry's Decision is not one of %s: %s"
                            % (", ".join(decisions), dict(fields).get("Decision")))
        problems += diagnosis_problems(repo_root(), design, text, count, dict(fields))
    # the Reason of an `entered` entry is a value the entry reason takes now, so an old log's value is appended in
    # no entry
    # @canon-spec specs/methodology/design-workflow/order-of-a-designs-work.md § The Order of a Design's Work § Facts
    if kind == "entered" and not problems:
        reasons = fact_values("entry reason")
        if dict(fields).get("Reason") not in reasons:
            problems.append("an entered entry's Reason is not one of %s: %s" % (", ".join(reasons), dict(fields).get("Reason")))
    # the Settled Sub-scopes keep each sub-scope holding a file the design changed, read as the entry is appended,
    # since the changes then stand no longer once the design commits
    # @canon-spec specs/methodology/working-files/main.md § Design Log Entry § Script Checks [Name: settled-sub-scopes-keep-what-changed]
    settled = dict(fields).get("Settled Sub-scopes")
    if settled and not problems:
        dropped = sorted(changed_sub_scopes(repo_root(), text) - {s.strip() for s in settled.split(";")})
        problems += ["the %s entry's Settled Sub-scopes drop %s, each holding a file the design changed"
                     % (kind, ", ".join(dropped))] if dropped else []
    if problems:
        return report("log-entry, not logged", [(design.stem, p) for p in problems])
    # working-files/main.md § A Design Document § The Design's Version: the version after this entry raises it, written to
    # the header, and stamped on the entry, a check's at the version its report read
    new, block = with_entry(text, kind, fields, read_version)
    write_design(design, raw, new)
    print("== log-entry\n" + block + "\n")
    return 0


# ---------------------------------------------------------------- a check's report

WF = "specs/methodology/working-files/main.md"
# @canon-spec specs/methodology/working-files/main.md § A Check's Report
# where a report's form is declared: its parts are read from that declaration and its record types through the one
# reader of the record types the specs declare
REPORT_HOME = (WF, "A Check's Report")
FORM_RULE = WF + " § A Check's Report"
COUNT_RULE = WF + " § Design Log Entry § What a Check Counts"
FIELDS_RULE = "specs/methodology/modeling-constructs.md § Fields"
BLANK_LINES_RULE = "specs/methodology/spec-style/markdown.md § Blank Lines"
# @canon-spec specs/methodology/working-files/main.md § A Check's Report
REPORT_TITLE = "# Check's Report"
# the title's fields, and the one an adversarial review's report whose round stopped at the structure holds, with its
# one value
TITLE_FIELDS = ("Design", "Entry")
STOPPED_AT, THE_STRUCTURE = "Stopped At", "the structure"
REVIEWS = ("adversarial-review", "post-apply-review")
JUDGMENT = "handed-off-judgment"
# @canon-spec specs/methodology/working-files/main.md § Design Log Entry
# the kinds of the entry naming the builder's triage of an audit
AUDITS = ("audit-specs", "verify-spec-implementation")
# the Reading's fields: the version of the design the check read, first, written by whoever writes the Reading; then a
# review's field or every other report's; and the Settlement's fields, in their order
READ_VERSION = "Design Version"
REVIEW_READING, OWN_READING = "Reviewer Readings", "Reads"
SETTLEMENT_FIELDS = ("Ending", "Earlier Reports", "Settling Reads", "Settlements")
# @canon-spec specs/methodology/working-files/main.md § A Check's Report § The Reading and the Settlement
# the endings a report's Settlement states, the first held alone and each other followed by a comma and what ended it
OWN_SETTLING, DECIDED, CUT_SHORT = "its own settling", "decided", "cut short"
# @canon-spec specs/methodology/working-files/main.md § A Check's Report § Who Writes Each Part
# the parts a cold agent writes in a review's or a handed-off judgment's report, its Title among them, the parts the
# builder and the design script write in it, and the parts holding records, each by its type's Plural Name
REVIEWER_PARTS = ("Title", "Reading", "Findings", "Searches", "Read Assessments", "Traces", "Builder Checks")
BUILDER_PARTS = ("Hand-back", "Script Output", "Causes", "Settlement")
HAND_BACK = "Hand-back"
# a Hand-back line: a part's name and the fingerprint of its text, and, for a review's Searches, the lines it covers
FINGERPRINT = re.compile(r"^- (?P<part>[A-Z][A-Za-z -]*?): (?P<sha>[0-9a-f]{64})(?:, (?P<n>\d+) lines)?$")
RECORD_PARTS = ("Findings", "Searches", "Read Assessments", "Traces", "Builder Checks", "Causes")
# @canon-spec specs/methodology/working-files/main.md § A Check's Report § Finding
# a Finding's fields naming the parts of the design it bears on, by their Names, and the one citing the rules it breaks
ANCHORS = {"Affected Goals": "goals", "Affected Frame Outcomes": "outcomes", "Affected Step Objectives": "objectives"}
BROKEN_RULES = "Broken Rules"
# @canon-spec specs/methodology/working-files/main.md § A Check's Report § Verdicts
MARKS = ("design flaw", "implementation flaw", "nit")
FLAWS = MARKS[:2]
# @canon-spec specs/methodology/working-files/main.md § A Check's Report § Settlement § Orders
ORDERS = ("primary", "secondary", "tertiary")
# @canon-spec specs/methodology/working-files/main.md § A Check's Report § Settlement § Requirements
# what requires a Settlement's findings, by the Justifying fields each member names
REQUIRED_BY = {"the goals": ("Justifying Goals",), "the rules": ("Justifying Rules",),
               "the goals and the rules": ("Justifying Goals", "Justifying Rules"), "nothing": ()}
# @canon-spec specs/methodology/working-files/main.md § A Check's Report § Settlement § Fix Authorities
AUTHORITIES = ("the builder's", "the user's")
# @canon-spec specs/methodology/working-files/main.md § A Check's Report § Settlement
# a finding's lineage, a Finding's as its writer traces it and a Settlement's as the builder settles it, and the field
# holding the builder's reason for a departure from a finding's writer
LANDS_ON, DEPARTURE_REASON = "Lands On", "Departure Reason"
# @canon-spec specs/methodology/working-files/main.md § A Check's Report § Settlement § User Decisions
# the decision taking a tertiary line in, whose fix counts for no line
WIDEN = "widen the goals"
# @canon-spec specs/methodology/working-files/main.md § A Check's Report § What the Design Script Checks
# the fields a Settlement holds with its two indicators, none of which a report settled before them holds
INDICATORS = ("Required By", "Fix Authority", "User Decision")
# @canon-spec specs/methodology/working-files/main.md § A Check's Report § Settlement § User Decisions
# the decisions under which no fix of a Settlement's findings is made
UNFIXED = ("left as it stands", "sent back", "carried by the approval", "carried by a steer", "cut at the secondary",
           "hand on", "taken by the step back", "taken by a changed foundation")
# @canon-spec specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: report-in-its-form]
# the fields a Settlement holds with its assessment and its order, none of which a report settled before them holds
ASSESSED = ("Justifying Goals", "Justifying Rules", "Assessment", "Order", "Places") + INDICATORS
# @canon-spec specs/methodology/working-files/main.md § A Check's Report § Verdicts
# each count of a check's entry, by the last word in its report it counts
COUNTED = {"Design Flaws": "design flaw", "Implementation Flaws": "implementation flaw", "Nits": "nit", "Dropped": "dropped"}
# @canon-spec specs/methodology/working-files/main.md § A Check's Report
# the fields holding places, by the Plural Name of the type giving them or the part holding them; the one holding a
# single place, and those holding `none` where they hold no place
PLACE_FIELDS = {"Reading": ("Reads",), "Settlement": ("Earlier Reports", "Settling Reads"),
                "Reviewer Readings": ("Collecting Reads", "Earlier Reports", "Weighing Reads"),
                "Findings": (BROKEN_RULES,), "Report Evidence Items": ("Places",),
                "Searches": ("Places",), "Read Assessments": ("Area",), "Builder Checks": ("Places Checked",),
                "Causes": ("Conflicting Steers",), "Misses": ("Place", "Reads"), "Settlements": ("Justifying Rules",),
                "Changed Places": ("Place", "Follows")}
ONE_PLACE = {("Misses", "Place"), ("Read Assessments", "Area"), ("Changed Places", "Place"), ("Changed Places", "Follows")}
NONE_HELD = {("Reading", "Reads"), ("Settlement", "Earlier Reports"), ("Settlement", "Settling Reads"),
             ("Reviewer Readings", "Collecting Reads"),
             ("Reviewer Readings", "Earlier Reports"), ("Reviewer Readings", "Weighing Reads"), ("Searches", "Places"),
             ("Findings", BROKEN_RULES)}
# @canon-spec specs/methodology/working-files/main.md § A Check's Report § Kinds of Builder Check
# the checks every self-review requires, and those it requires for each item its phase gives
EVERY_SELF_REVIEW = ("steers against the user's messages", "linked work")
USER_EDIT, WORKED_CASE, MISS_QUESTION, DIFFERENTIAL = "user edit", "worked case", "miss's question", "differential test"
CARRIED = "carried finding"
DIAGNOSIS_ANSWERED = "diagnosis answered"
# the check the first self-review of a major version requires, for each place the design's Problem cites
PROBLEM_RE_EVALUATION = "problem re-evaluation"
# the check every self-review over applied work of a design of these Kinds requires
CONSTRUCT_CHOICE, SPEC_KINDS = "construct choice", ("canon-specs", "application-specs")
SCRIPTS = (".py", ".ps1", ".sh")


def report_file(design, kind, n):
    """-> a check's report in its design's folder, `.ai/tmp/<skill-name>/<design>/reports/<kind>/{n}.md`."""
    return design.parents[2] / "tmp" / design.parent.name / design.stem / "reports" / kind / ("%d.md" % n)


def rel_to(path, root):
    try:
        return Path(path).resolve().relative_to(Path(root).resolve()).as_posix()
    except ValueError:
        return Path(path).as_posix()


def report_parts(root=None):
    """-> [(part, heading, required, the rules its Holds cites)] from § A Check's Report's table of parts, in order."""
    body, path = declaration(REPORT_HOME, root)
    lines = (body or "").split("\n")
    head = next((i for i, l in enumerate(lines) if l.startswith("| Part | Heading |")), None)
    out = []
    for l in lines[head + 2:] if head is not None else []:
        if not l.startswith("|"):
            break
        cells = [c.strip() for c in l.strip().strip("|").split("|")]
        if len(cells) < 4:
            continue
        heading = re.match(r"`([^`]+)`", cells[1])
        rules = [path + " " + c if c.startswith("§") else c for c in re.findall(r"`([^`]+)`", cells[3])]
        out.append((cells[0], heading.group(1) if heading else "", cells[2], rules))
    return out


# @canon-spec specs/methodology/spec-placement/where-a-file-goes.md § Where a File Goes
def canon_rule(rule, root=None):
    """-> a rule the shared readers name by its file's name alone, cited with its path: a document laid out as a folder
    named by its bare file name resolves to the file of its folder holding the section named, its main file first
    where it holds one, and a bare `main.md`, which every folder's main file shares, names no one document and is left
    as written. The folder is read from the root given, or from the checkout the script is run in."""
    if rule.startswith("specs/"):
        return rule
    name, sep, rest = rule.partition(" § ")
    if name == "main.md":
        return rule
    base = Path(root) if root is not None else repo_root()
    folder = base / "specs/methodology" / name[:-3]
    if not (base / "specs/methodology" / name).is_file() and folder.is_dir():
        found = folder_file(folder, rest)
        if found:
            return f"specs/methodology/{name[:-3]}/{found.name}{sep}{rest}"
    return "specs/methodology/" + rule


def report_types(root):
    """-> the record types the specs declare, by their Plural Names, read once through the one reader."""
    if not record_types.TYPES:
        record_types.declared_types(spec_texts(root))
    return record_types.TYPES


def as_record(rec):
    """-> a record as the one reader gives it, [(key, value, line)], as {key: value, "_line": its 0-based line}, a
    field holding records giving them as such records in turn."""
    out = {"_line": rec[0][2] if rec else 0}
    for key, value, _ in rec:
        if key is not None:
            out[key] = [as_record(r) for r in value] if isinstance(value, list) else str(value).strip()
    return out


def read_report(text):
    """-> a check's report as its form reads it: {"in_form", "title" {field: (value, 0-based line)}, "parts"
    [(part, 0-based line)], "blocks" {part: [field]}, "raw" {plural: records as the one reader gives them}, "records"
    {plural: [record]}, "settlements", "lines", "problems" [(rule, 1-based line, message)]}. A report not opening with
    its title is one written before the form, read as holding no records. A Weighs Again, the field's name before Lands
    On, is read as its Lands On, as working-files/main.md § A Check's Report § What the Design Script Checks has a logged
    report read."""
    text = re.sub(r"^(\s*(?:- )?)\*\*Weighs Again:\*\*", r"\1**%s:**" % LANDS_ON, text.replace("\r\n", "\n"), flags=re.M)
    lines = text.split("\n")
    out = {"in_form": False, "title": {}, "parts": [], "blocks": {}, "raw": {}, "records": {p: [] for p in RECORD_PARTS},
           "settlements": [], "lines": lines, "problems": [], "text": text}
    first = next((i for i, l in enumerate(lines) if l.strip()), None)
    if first is None or lines[first].strip() != REPORT_TITLE:
        return out
    out["in_form"] = True
    k = record_types._next_nonblank(lines, first + 1, len(lines))
    if k < len(lines) and record_types.opens_key(lines[k]) and not record_types._indent(lines[k]):
        block, _ = record_types.read_block(lines, k, 0, len(lines))
        out["title"] = {f["key"]: (str(record_types.value_of(f)).strip(), f["line"]) for f in block}
    for lineage, (h, end) in sorted(sections(text).items(), key=lambda s: s[1][0]):
        if " § " in lineage:
            out["problems"].append((FORM_RULE, h + 1, "a heading beneath a part's, where the form gives none: " + lineage))
            continue
        out["parts"].append((lineage, h))
        if lineage in RECORD_PARTS:
            recs, problems = record_types.parse_records(text, lineage)
            out["problems"] += [(rule, i + 1, msg) for rule, i, msg in problems]
            out["raw"][lineage] = recs
            out["records"][lineage] = [as_record(r) for r in recs if r and r[0][0] is not None]
        elif lineage in ("Reading", "Settlement"):
            k = next((i for i in range(h + 1, end) if record_types.opens_key(lines[i]) and not record_types._indent(lines[i])), None)
            block, j = record_types.read_block(lines, k, 0, end) if k is not None else ([], h + 1)
            out["blocks"][lineage] = block
            rest = record_types._next_nonblank(lines, j, end)
            if rest < end:
                out["problems"].append((FORM_RULE, rest + 1, "the %s part holds something other than its fields" % lineage))
            # a field of the part holding records: the Reading's Reviewer Readings and the Settlement's Settlements
            for f in block:
                value = record_types.value_of(f)
                if (lineage, f["key"]) in (("Reading", REVIEW_READING), ("Settlement", "Settlements")):
                    recs = value if isinstance(value, list) else []
                    out["raw"][f["key"]] = recs
                    if f["key"] == "Settlements":
                        out["settlements"] = [as_record(r) for r in recs if r and r[0][0] is not None]
    return out


# @canon-spec specs/methodology/working-files/main.md § A Check's Report § The Reading and the Settlement
def report_version(rep):
    """-> the version of the design a report's check read, its Reading's Design Version, or None where it holds none,
    a report written before the field."""
    value = next((str(record_types.value_of(f)) for f in rep["blocks"].get("Reading", []) if f["key"] == READ_VERSION), "")
    return parse_version(value.strip().strip("`"))


def place_of(text):
    """-> (path, lineage or None, selector or None) for one citation with its path, as
    specs/methodology/sourcing-and-citation/writing-a-citation.md § Writing a Citation writes one, alone in its text; else None."""
    m = re.fullmatch(r"\s*`([^`]+)`\s*", text or "")
    if not m or m.group(1).strip().startswith("§"):
        return None
    path, target, selector = parse_citation(m.group(1), None)
    if not path or " " in path:
        return None
    return path, target or None, re.sub(r"\s*:\s*", ": ", selector.strip()) if selector else None


def place_list(value):
    """-> the places a value holding places lists, `none` listing none."""
    return [p for p in (place_of(l) for l in str(value or "").split("\n")
                        if l.strip() and l.strip(" -`") != "none") if p]


def cited_places(text):
    """-> each place a text cites with its path, wherever in the text it stands."""
    return [p for p in (place_of("`%s`" % s) for s in re.findall(r"`([^`]+)`", text or "")) if p]


def place_key(place):
    return place[0], place[1] or "", place[2] or ""


def cite(place):
    path, lineage, selector = place
    return "`%s%s%s`" % (path, " § " + lineage if lineage else "", " [%s]" % selector if selector else "")


# @canon-spec specs/methodology/working-files/main.md § A Check's Report § A Value Holding Places
def covers(a, b):
    """Whether place a covers place b: a file each of its sections, a section each section beneath it, and a part a
    keyed instance holds itself alone, each matched as it is cited."""
    if a[0] != b[0]:
        return False
    if a[1] is None:
        return a[2] is None
    if a[2] is not None:
        return a == b
    return b[1] is not None and (b[1] == a[1] or b[1].startswith(a[1] + " § "))


def covered(listed, place):
    return any(covers(a, place) for a in listed)


# @canon-spec specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: places-in-their-form]
def places_problems(rep, types, taken_up=frozenset()):
    """-> [(rule, message)]: each value holding places in a report out of the form § A Check's Report gives it, a list
    of citations with their paths, one to an item, or one such citation alone; `none` where its field holds it; a
    value standing at a line taken_up gives passed over."""
    out = []

    def check(line, where, owner, key, value):
        items = [l.strip() for l in str(value).split("\n") if l.strip()]
        if line in taken_up or (items == ["none"] and (owner, key) in NONE_HELD):
            return
        where = "line %d, %s" % (line + 1, where)
        if (owner, key) in ONE_PLACE and len(items) != 1:
            out.append("%s's %s holds %d places, where it holds one citation" % (where, key, len(items)))
        out.extend("%s's %s holds an item that is no citation of a place with its path: %s" % (where, key, i)
                   for i in items if not place_of(i))

    def walk(plural, recs):
        for rec in recs:
            for key, value, line in rec:
                if key is None:
                    continue
                if isinstance(value, list):
                    held = types.get(plural, {}).get("holds", {}).get(key)
                    if held:
                        walk(held[0], value)
                elif key in PLACE_FIELDS.get(plural, ()):
                    check(line, "a record of %s" % plural, plural, key, value)
    for plural, recs in rep["raw"].items():
        walk(plural, recs)
    for part, fields in rep["blocks"].items():
        for f in fields:
            if f["key"] in PLACE_FIELDS.get(part, ()):
                check(f["line"], "the %s part" % part, part, f["key"], record_types.value_of(f))
    return [(FORM_RULE, p) for p in out]


def settled_findings(settlement):
    """-> the keys of the Findings a Settlement settles, one to an item of its Settled Findings."""
    return [k.strip().strip("`").strip() for k in settlement.get("Settled Findings", "").split("\n") if k.strip()]


def last_words(rep):
    """-> {a Finding's key: the verdict it is counted by}: the Verdict of the Settlement settling it, as What a
    Check Counts has a finding counted, else its own while no Settlement settles it."""
    out = {f.get("Finding", ""): f.get("Verdict", "") for f in rep["records"]["Findings"]}
    for s in rep["settlements"]:
        for k in settled_findings(s):
            if k in out:
                out[k] = s.get("Verdict", "")
    return out


# @canon-spec specs/methodology/working-files/main.md § Design Log Entry § Script Checks [Name: counts-taken-from-the-report]
def report_counts(rep):
    """-> each count of a check's entry from its report, each Finding counted once, by the Verdict of the
    Settlement settling it."""
    words = collections.Counter(last_words(rep).values())
    return {field: words[word] for field, word in COUNTED.items()}


def require(out, where, rec, key, required, condition):
    """Holds a field its condition requires to the record, and one its condition does not give out of it."""
    if required and key not in rec:
        out.append("%s holds no %s, which its form requires %s" % (where, key, condition))
    elif not required and key in rec:
        out.append("%s holds a %s, which its form gives it only %s" % (where, key, condition))


def cause_key(value, report_rel):
    """-> the key of the Cause of the report at report_rel a value names, by its key alone or by a citation; else None."""
    place = place_of(value)
    if place is None:
        return value.strip() or None
    if place[0] == report_rel and place[1] == "Causes" and (place[2] or "").startswith("Cause: "):
        return place[2][len("Cause: "):]
    return None


# @canon-spec specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: report-in-its-form]
def form_problems(rep, ctx, types, parts):
    """-> [(rule, message)]: a report out of the form § A Check's Report gives it: its title, its parts in their order
    and those its kind and its settling require, its Reading's and its Settlement's fields, and each record of the type
    its part or field cites, with each field its conditions require and no other. Which hand's parts it holds turns on
    when it reads the report: ctx["reviewer"], as a cold agent's report is handed back or taken up, holds the parts
    that agent wrote, and no check after the take-up holds them again, each line ctx["taken_up"] gives being passed
    over, so such a report is then held in the builder's parts and in the order of its parts alone. A report the
    builder writes alone is held whole. A round the user ended, by the plan's approval or by a set of steers changing
    the goals or the frame, is settled with no Causes."""
    import spec_checks
    if not rep["in_form"]:
        return [(FORM_RULE, "the report does not open with its title, %s" % REPORT_TITLE)]
    taken_up, at = ctx["taken_up"], dict(rep["parts"])
    out = [(canon_rule(rule), "line %d: %s" % (line, msg)) for rule, line, msg in rep["problems"] if line - 1 not in taken_up]
    reviewer, kind, review, rule = ctx["reviewer"], ctx["kind"], ctx["kind"] in REVIEWS, ctx["rule"]
    # its title, which opens the report at its first line
    titled = 0 not in taken_up
    title = rep["title"] if titled else {}
    if titled and list(title) not in (list(TITLE_FIELDS), list(TITLE_FIELDS) + [STOPPED_AT]):
        out.append((FORM_RULE, constructs.block_refusal("its title", list(title), list(TITLE_FIELDS) + [STOPPED_AT], TITLE_FIELDS,
                                                  owner="its form")))
    for key, want in (("Design", ctx["design"]), ("Entry", ctx["entry"])):
        if key in title and title[key][0] != want:
            out.append((FORM_RULE, "its title's %s is %s, not %s" % (key, title[key][0], want)))
    # the mark of an adversarial round stopped at the structure, held in no other report
    if STOPPED_AT in title and kind != REVIEWS[0]:
        out.append((FORM_RULE, "its title holds %s, which only an adversarial review's report holds" % STOPPED_AT))
    elif STOPPED_AT in title and title[STOPPED_AT][0].strip("`") != THE_STRUCTURE:
        out.append((FORM_RULE, "its title's %s is %s, not %s" % (STOPPED_AT, title[STOPPED_AT][0], THE_STRUCTURE)))
    # its parts, in their order, each once, and those required: the order is the whole report's, held at every check
    order = [p for p, _, _, _ in parts]
    held = [p for p, _ in rep["parts"]]
    out += [(FORM_RULE, "a part the form does not give: " + p) for p in held if p not in order]
    known = [p for p in held if p in order]
    if known != sorted(known, key=order.index) or len(set(known)) != len(known):
        out.append((FORM_RULE, constructs.block_refusal("the report", known, order, noun="part", owner="its form")))
    # recs, every record the report holds, which a check of another part reads; own, the records this reading holds to
    # the form
    recs = rep["records"]
    own = {plural: [r for r in found if r["_line"] not in taken_up] for plural, found in recs.items()}
    settlements = rep["settlements"] + ctx["judgment_settlements"]
    required = {"Reading"} if reviewer else {"Settlement"} if taken_up else {"Reading", "Settlement"}
    # whether the round ended other than by its own settling: read from its Ending where it states one, else, for a
    # report written before the statement, from the log
    ending = report_ending(rep)
    ended = ctx.get("ended", False) if ending is None else ending != OWN_SETTLING
    if not reviewer:
        if kind == "self-review":
            required.add("Script Output")
        if review and ended is False and any(s.get("Verdict") in MARKS for s in settlements):
            required.add("Causes")
    for p in sorted(required - set(held), key=order.index):
        out.append((rule(p), "it holds no %s part, which its form requires of it" % p))
    if ended and "Causes" in held:
        out.append((rule("Causes"), "it holds a Causes part, though its round ended %s" % (
            "by the user" if ending is None else "`%s`" % ending)))
    # its Reading's field, and its Settlement's fields, in their order
    # a report the log holds already, written before its Reading held the version read, read under the fields it was
    # written with
    keys = [f["key"] for f in rep["blocks"].get("Reading", [])]
    want = [READ_VERSION, REVIEW_READING if review else OWN_READING]
    reading = "Reading" in held and at["Reading"] not in taken_up
    if reading and keys != want and not (ctx.get("logged") and keys == want[1:]):
        out.append((rule("Reading"), constructs.block_refusal("its Reading", keys, want, want, owner="its form")))
    elif reading and READ_VERSION in keys and report_version(rep) is None:
        out.append((rule("Reading"), "its Reading's %s is not major.minor.revision" % READ_VERSION))
    cond = []
    if "Settlement" in held and not reviewer:
        keys = [f["key"] for f in rep["blocks"].get("Settlement", [])]
        if keys != [k for k in SETTLEMENT_FIELDS if k in keys] or any(k not in SETTLEMENT_FIELDS for k in keys):
            out.append((rule("Settlement"), constructs.block_refusal("its Settlement", keys, SETTLEMENT_FIELDS, owner="its form")))
        has = dict.fromkeys(keys)
        # a report the log holds already, written before its Settlement stated how its check ended, read under the
        # fields it was written with
        owed = owes_ending(kind) and not (ctx.get("logged") and "Ending" not in keys)
        require(cond, "its Settlement", has, "Ending", owed, "where the report owes the statement of how its check ended")
        if "Ending" in keys and owes_ending(kind):
            ending = report_ending(rep)
            if ending is None:
                cond.append("its Settlement's Ending is neither `%s` nor `%s` or `%s` followed by a comma and what ended it"
                            % (OWN_SETTLING, DECIDED, CUT_SHORT))
            elif ending == DECIDED and not review:
                cond.append("its Settlement's Ending is `%s`, which only a review's round is" % DECIDED)
        require(cond, "its Settlement", has, "Earlier Reports", True, "always")
        require(cond, "its Settlement", has, "Settling Reads", review, "where the report is a review's")
        require(cond, "its Settlement", has, "Settlements", bool(recs["Findings"]), "where the report holds a Finding")
    out += [(rule("Settlement"), c) for c in cond]
    # each record of its type, a part's or a field's, its required fields and its values
    found, raw = [], rep["raw"]
    before = ctx.get("settled_before_orders")
    for plural in RECORD_PARTS + (REVIEW_READING, "Settlements"):
        if reviewer and plural not in REVIEWER_PARTS + (REVIEW_READING,):
            continue
        if plural in raw and plural in types:
            spec, got = types[plural], []
            # a report settled before a Settlement held its assessment and its order, or its two indicators, read as it
            # stands
            if plural == "Settlements" and (before or ctx.get("settled_before_indicators")):
                unheld = ASSESSED if before else INDICATORS
                spec = dict(spec, required=[f for f in spec["required"] if f not in unheld])
            rows = [r for r in raw[plural] if not r or r[0][2] not in taken_up]
            if plural == "Searches" and ctx.get("logged"):
                # a Search of a report the log holds, written before its record held a Kind, read under the field names
                # it was written with
                logged = [r for r in rows if logged_form({k: v for k, v, _ in r})]
                rows = [r for r in rows if r not in logged]
                was = dict(spec, fields=list(LOGGED_SEARCH_FIELDS), required=list(LOGGED_SEARCH_FIELDS[:4]), values={}, defaults={})
                spec_checks._check_records(logged, was, WF, "the report", lambda i: i + 1, got, "its %s" % plural)
            spec_checks._check_records(rows, spec, WF, "the report", lambda i: i + 1, got, "its %s" % plural)
            found += [g for g in got if not (before and plural == "Causes" and legacy_places(g[3]))]
    out += [(canon_rule(r), "line %d: %s" % (line, msg)) for r, _, line, msg in found]
    # each field its conditions require, and no other
    cond = []
    for f in own["Findings"]:
        where, mark = "line %d, Finding %s" % (f["_line"] + 1, f.get("Finding", "")), f.get("Verdict") in MARKS
        for key in ("Decision", "Possible Fix"):
            require(cond, where, f, key, mark, "where its Verdict is a mark")
        require(cond, where, f, "Evidence", f.get("Verdict") != "review observation", "where its Verdict is not a review observation")
        require(cond, where, f, "Lies In", mark and ctx["applied"], "where its Verdict is a mark and the report lies over applied work")
        for fix in f.get("Possible Fix") or []:
            if isinstance(fix, dict):
                require(cond, where + "'s Possible Fix", fix, "Fix", fix.get("Kind") == "tactical fix", "where its Kind is tactical fix")
                require(cond, where + "'s Possible Fix", fix, "Delivers", fix.get("Kind") == "revision", "where its Kind is revision")
    out += [(rule("Findings"), c) for c in cond]
    # a Read Assessment's Impact, a list of the members of Read Assessment Impacts: `none` alone, or one or both others
    members = impact_members(ctx["root"])[0]
    for a in own["Read Assessments"]:
        if "Impact" not in a:  # a record wanting its Impact is out of its type, reported with the record's form
            continue
        impact = names_of_text(a["Impact"])
        if not impact or any(i not in members for i in impact) or len(set(impact)) != len(impact) \
                or ("none" in impact and len(impact) > 1):
            out.append((rule("Read Assessments"), "line %d, Read Assessment %s's Impact is not a list holding none alone, "
                        "or one or both of %s, one to an item" % (a["_line"] + 1, a.get("Area", ""),
                                                                   " and ".join(m for m in members if m != "none"))))
    # a Read Assessment's Goals, and a Search's: each item a goal's Name the design holds. A Search written before its
    # record held a Kind holds its Goals in a report of research alone, as it was written. One written in the form
    # names its goals whoever recorded it, or `none` alone where it was made for a check, a finding or a defect naming
    # no goal of the design
    cond = []
    for r in own["Read Assessments"]:
        where = "line %d, Read Assessment %s" % (r["_line"] + 1, r.get("Area", ""))
        require(cond, where, r, "Goals", True, "of every Read Assessment")
        cond += ["%s's Goals name %s, which is no design goal's Name" % (where, g)
                 for g in names_of_text(r.get("Goals", "")) if g not in ctx["goals"]]
    out += [(rule("Read Assessments"), c) for c in cond]
    cond = []
    for s in own["Searches"]:
        where = "line %d, Search %s" % (s["_line"] + 1, s.get("Search", ""))
        named = names_of_text(s.get("Goals", ""))
        if logged_form(s):
            require(cond, where, s, "Goals", bool(recs["Read Assessments"]), "where it stands in a report of research")
        else:
            cond += search_form_problems(s, where)
            if named == ["none"]:
                if not serves_no_goal(s, rep, ctx):
                    cond.append("%s's Goals hold none, which a reviewer's Search, one in the report of an audit's triage and one a "
                                "tactical fix names whose settled Findings each name no goal alone may hold" % where)
                continue
            if "none" in named:
                cond.append("%s's Goals hold none beside a goal, where none stands alone" % where)
        cond += ["%s's Goals name %s, which is no design goal's Name" % (where, g) for g in named if g not in ctx["goals"] and g != "none"]
    out += [(rule("Searches"), c) for c in cond]
    cond = []
    for t in own["Traces"]:
        require(cond, "line %d, Trace %s" % (t["_line"] + 1, t.get("Trace", "")), t, "Outcome", ctx["trace_outcome"],
                "where the report is a self-review's before the apply, and no plan-approval entry of the phase stands "
                "before it but one an another-round entry follows")
        require(cond, "line %d, Trace %s" % (t["_line"] + 1, t.get("Trace", "")), t, "Paths", ctx["applied"],
                "where the report lies over applied work")
    out += [(rule("Traces"), c) for c in cond]
    # the parts the builder writes, which a report handed back does not hold yet
    if reviewer:
        return out
    cond = []
    for c in recs["Causes"]:
        where = "line %d, Cause %s" % (c["_line"] + 1, c.get("Cause", ""))
        naming = [s for s in settlements if cause_key(s.get("Cause", ""), ctx["report_rel"]) == c.get("Cause")]
        flaw = any(s.get("Verdict") in FLAWS for s in naming)
        unwritten = kind == REVIEWS[1] and any(s.get("Lies In") in ("the plan", "handed on") for s in naming)
        require(cond, where, c, "Outcome", "Continues" in c, "where Continues is held")
        require(cond, where, c, "Misses", flaw, "where it settles a design flaw or an implementation flaw")
        # a Cause settling only nits may hold the change that fixes them
        if flaw or "Proposed Change" not in c:
            require(cond, where, c, "Proposed Change", flaw and not unwritten,
                    "where it settles a flaw, no Settlement naming it giving Lies In the plan or handed on in a post-apply round")
        for miss in c.get("Misses") or []:
            if isinstance(miss, dict):
                asked, at = miss.get("Kind") == "question not asked", where + "'s Miss " + miss.get("Miss", "")
                for k in ("Place", "Reads"):
                    require(cond, at, miss, k, not asked, "where its Kind is not question not asked")
                for k in ("Question", "Answer"):
                    require(cond, at, miss, k, asked, "where its Kind is question not asked")
        for change in c.get("Proposed Change") or []:
            if isinstance(change, dict):
                for k in ("Search", "Reason"):
                    require(cond, where + "'s Proposed Change", change, k, change.get("Kind") == "tactical fix", "where its Kind is tactical fix")
                require(cond, where + "'s Proposed Change", change, "Decision Rewritten", change.get("Kind") == "revision", "where its Kind is revision")
    out += [(rule("Causes"), c) for c in cond]
    cond = []
    for s in rep["settlements"]:
        where, mark = "line %d, Settlement %s" % (s["_line"] + 1, s.get("Settlement", "")), s.get("Verdict") in MARKS
        require(cond, where, s, "Lies In", mark and ctx["applied"], "where its Verdict is a mark and the report lies over applied work")
        # a Settlement answers each earlier change a finding it settles names, a change or none
        if any(f.get(LANDS_ON, "").strip("` ") not in ("", "none") for f in findings_of(rep, s)):
            require(cond, where, s, LANDS_ON, True, "where a finding it settles names an earlier change it lands on")
        # a judgment's Settlement cites the round's Cause where it is settled with a round, checked at the round's entry
        if kind != JUDGMENT or "Cause" not in s:
            require(cond, where, s, "Cause", mark and "Causes" in held, "where the report holds Causes and its Verdict is a mark")
        # a fix made with no Cause carrying it, as an audit's triage, a self-review and a pass make one, records its places;
        # a nit's fix, or a design flaw's the user triaged, may
        if not before:
            fixed = s.get("Verdict") == FLAWS[1] and "Causes" not in held and kind not in REVIEWS + (JUDGMENT,) \
                and s.get("Lies In") not in ("the plan", "handed on") and "Carried By" not in s \
                and s.get("User Decision") not in UNFIXED
            if fixed or "Places" not in s or "Cause" in s:
                require(cond, where, s, "Places", fixed, "where its findings' fix is made and no Cause of the report carries it")
    causes = {c.get("Cause") for c in recs["Causes"]}
    # a judgment settled with a round holding no Causes, one proposing no change, cites none
    cond += ["a handed-off judgment's Settlement %s, settled with the round, cites no Cause of its report by the report "
             "and the Cause's key" % s.get("Settlement", "") for s in ctx["judgment_settlements"]
             if s.get("Verdict") in MARKS and "Causes" in held and not (place_of(s.get("Cause", "")) and cause_key(s["Cause"], ctx["report_rel"]) in causes)]
    out += [(rule("Settlement"), c) for c in cond]
    return out


# @canon-spec specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: report-laid-out]
def layout_problems(rep, root, taken_up=frozenset()):
    """-> [(rule, message)]: the report laid out otherwise than modeling-constructs.md § Fields and spec-style/markdown.md
    § Blank Lines have a block of fields laid out, each line taken_up gives passed over."""
    found = record_types.block_findings(rep["text"]) + layout.findings(rep["text"], layout.rules(root)[0])
    return [(FIELDS_RULE if "Fields" in rule else BLANK_LINES_RULE, "line %d: %s" % (line, msg)) for rule, line, msg in found
            if line - 1 not in taken_up]


# @canon-spec specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: findings-settled-once]
def settled_problems(rep, ctx):
    """-> [(rule, message)]: a Finding settled by no Settlement, or by more than one."""
    times = collections.Counter(k for s in rep["settlements"] for k in settled_findings(s))
    return [(ctx["rule"]("Settlement"), "Finding %s is settled by %d Settlements, not exactly one" % (f.get("Finding", ""), times[f.get("Finding", "")]))
            for f in rep["records"]["Findings"] if times[f.get("Finding", "")] != 1]


def change_places(change):
    """-> the places a change records: each Changed Place's Place, or, in a report settled before a change recorded
    its Changed Places, each item of its Places."""
    value = change.get("Places", "")
    if isinstance(value, list):
        return [p for r in value if isinstance(r, dict) for p in [place_of(r.get("Place", ""))] if p]
    return place_list(value)


def cause_change(s, rep, report_rel):
    """-> the Changed Places of the Proposed Change of the Cause of the report a Settlement names, else []."""
    key = cause_key(s.get("Cause", ""), report_rel)
    return [p for c in rep["records"]["Causes"] if key and c.get("Cause") == key
            for change in c.get("Proposed Change") or [] if isinstance(change, dict)
            for p in (change.get("Places") if isinstance(change.get("Places"), list) else []) if isinstance(p, dict)]


def own_places(s):
    """-> the Changed Places a Settlement's own Places records, else []."""
    return [p for p in (s.get("Places") if isinstance(s.get("Places"), list) else []) if isinstance(p, dict)]


# @canon-spec specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: settlements-justified]
def findings_of(rep, s):
    """-> the Findings of a report a Settlement settles, in the order the report holds them."""
    keys = set(settled_findings(s))
    return [f for f in rep["records"]["Findings"] if f.get("Finding") in keys]


def users_call(s, rep, report_rel, kind):
    """-> why the report or its entry shows Whose Fix It Is giving the user the call on a Settlement's findings, else
    None: the report the builder's triage of an audit and its Verdict other than dropped, its Verdict or a finding's it
    settles a design flaw, a review observation, set aside or not caused, its Lies In or a finding's the plan or handed
    on, its findings tertiary or a change settling them reaching a tertiary place, or a change settling them made, its
    Places or its Cause's Proposed Change recording it, where its Required By is nothing."""
    # a finding dropped has no fix, so no call on one is given anyone
    if s.get("Verdict") == "dropped":
        return None
    change = own_places(s) + cause_change(s, rep, report_rel)
    found = findings_of(rep, s)
    if kind in AUDITS:
        return "the report is the builder's triage of an audit, its entry's kind %s" % kind
    # a departure from a finding's writer never moves its fix to the builder's own authority (specs/AGENTS.md § Design,
    # Refactor, Refine § Settling a Round § Order and Lineage): the writer's Verdict and Lies In read beside the builder's
    for who, rec in [("its", s)] + [("Finding %s's" % f.get("Finding", ""), f) for f in found]:
        if rec.get("Verdict") in (MARKS[0], "review observation", "set aside", "not caused"):
            return "%s Verdict is %s" % (who, rec["Verdict"])
    # a finding lying handed on is settled as Changes After Approval settles an audit's finding, the user's call
    placed = next((rec["Lies In"] for rec in [s] + found if rec.get("Lies In") in ("the plan", "handed on")), None)
    if placed:
        return "its findings lie %s, by its own Lies In or a Finding's" % ("in the plan" if placed == "the plan" else placed)
    if s.get("Order") == ORDERS[2] or any(p.get("Order") == ORDERS[2] for p in change):
        return "its findings are tertiary, or a change settling them reaches a tertiary place"
    if change and s.get("Required By") == "nothing":
        return "a change settling its findings is made, and nothing requires them"
    return None


# @canon-spec specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: settlements-justified]
def justified_problems(rep, ctx):
    """-> [(rule, message)]: a Settlement holding Justifying Goals or Justifying Rules other than its Required By names,
    or naming in its Justifying Goals a goal the design does not hold; one holding its Fix Authority the builder's where
    the report shows the call the user's; and one holding a User Decision where its Fix Authority is not the
    user's, or none where it is."""
    out, rule, cond = [], ctx["rule"]("Settlement"), []
    for s in rep["settlements"]:
        where = "line %d, Settlement %s" % (s["_line"] + 1, s.get("Settlement", ""))
        named = REQUIRED_BY.get(s.get("Required By"))
        if named is not None:
            for key in ("Justifying Goals", "Justifying Rules"):
                require(cond, where, s, key, key in named, "where its Required By names the %s" % key.split()[1].lower())
        out += [(rule, "%s's Justifying Goals name %s, which is no design goal's Name" % (where, g))
                for g in names_of_text(s.get("Justifying Goals", "")) if g not in ctx["goals"]]
        # a Fix Authority held only where the finding is kept, a dropped finding having no fix
        require(cond, where, s, "Fix Authority", s.get("Verdict") != "dropped", "where its Verdict is other than dropped")
        why = users_call(s, rep, ctx["report_rel"], ctx["kind"])
        if why and s.get("Fix Authority") == AUTHORITIES[0]:
            out.append((rule, "%s holds Fix Authority %s, where Whose Fix It Is gives the user the call: %s"
                        % (where, AUTHORITIES[0], why)))
        if s.get("Fix Authority") in AUTHORITIES:
            require(cond, where, s, "User Decision", s["Fix Authority"] == AUTHORITIES[1], "where its Fix Authority is the user's")
    return out + [(rule, c) for c in cond]


# @canon-spec specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: departures-reasoned]
def departure_problems(rep, ctx):
    """-> [(rule, message)]: a Settlement departing from a finding it settles, in Verdict, in Lies In or in Lands On,
    holding no Departure Reason. A Lands On is compared by the place it cites, `none` or no Lands On naming none, and a
    Lies In only where the finding holds one."""
    out, rule = [], ctx["rule"]("Settlement")
    lands = lambda rec: place_key(place_of(rec.get(LANDS_ON, "")) or ("", None, None))
    for s in rep["settlements"]:
        if DEPARTURE_REASON in s:
            continue
        where = "line %d, Settlement %s" % (s["_line"] + 1, s.get("Settlement", ""))
        for f in findings_of(rep, s):
            departs = [field for field, differs in (
                ("Verdict", f.get("Verdict") != s.get("Verdict")),
                ("Lies In", "Lies In" in f and f.get("Lies In") != s.get("Lies In")),
                (LANDS_ON, lands(f) != lands(s))) if differs]
            if departs:
                out.append((rule, "%s departs from Finding %s in %s and holds no %s"
                            % (where, f.get("Finding", ""), " and ".join(departs), DEPARTURE_REASON)))
    return out


# @canon-spec specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: report-in-its-form]
def legacy_places(message):
    """-> whether a record check's message is one a Proposed Change's Places draws where written as a list of paths,
    as a report settled before a Changed Place was a record writes it."""
    return message == "a field holding records whose value is no list of records: Places" \
        or message.startswith("an item of the Places field ")


def deeper(order):
    """-> the order one deeper than an order, a tertiary's staying tertiary."""
    return ORDERS[min(ORDERS.index(order) + 1, len(ORDERS) - 1)] if order in ORDERS else ORDERS[0]


def earlier_order(place, reports):
    """-> (the order of the earlier change a Lands On cites, whether that change starts its line again), as § A Check's
    Report § What the Design Script Checks works it out: the shallowest Order among the Settlements naming the Cause
    whose Proposed Change made it, or the Order of the Settlement whose Places record it, primary where a report settled
    before Orders holds none, the change starting its line again where those Settlements hold the User Decision widen the
    goals; None where no report of the design's current major version holds it."""
    path, part, selector = place
    held = reports.get(path)
    if held is None or not selector or ": " not in selector:
        return None
    key, value = selector.split(": ", 1)
    if part == "Causes" and key == "Cause":
        if not any(c.get("Cause") == value for c in held["records"]["Causes"]):
            return None
        naming = [x for x in held["settlements"] if cause_key(x.get("Cause", ""), path) == value]
    elif part == "Settlement" and key == "Settlement":
        naming = [x for x in held["settlements"] if x.get("Settlement") == value][:1]
        if not naming:
            return None
    else:
        return None
    orders = [x.get("Order") for x in naming if x.get("Order") in ORDERS]
    return (min(orders, key=ORDERS.index) if orders else ORDERS[0]), any(x.get("User Decision") == WIDEN for x in naming)


def is_change(place):
    """Whether a Lands On's place names an earlier change: a Cause or a Settlement, by its report and its key."""
    return bool(place) and (place[1], (place[2] or "").split(": ", 1)[0]) in (("Causes", "Cause"), ("Settlement", "Settlement"))


def place_order_problems(value, settles, where, rule):
    """-> [(rule, message)]: a change's Changed Place stating an order other than its lineage gives, primary where it
    names in Settles the findings its change settles, and one deeper than the place of its own change it Follows."""
    recs = [r for r in value if isinstance(r, dict)] if isinstance(value, list) else []
    by_place = {place_of(r.get("Place", "")): r for r in recs}
    out = []
    for r in recs:
        at = "%s's Changed Place %s" % (where, r.get("Place", ""))
        if "Order" not in r:
            continue
        if ("Settles" in r) == ("Follows" in r):
            out.append((rule, "%s holds %s Settles and Follows, where it holds one" % (at, "both" if "Settles" in r else "neither")))
            continue
        if "Settles" in r:
            derived, why = ORDERS[0], "it names the findings whose fix it is"
            out += [(rule, "%s names %s in its Settles, a finding its change does not settle" % (at, k))
                    for k in names_of_text(r["Settles"]) if k not in settles]
        else:
            followed = by_place.get(place_of(r["Follows"]))
            if followed is None or followed is r:
                out.append((rule, "%s follows %s, which is no other place of its own change" % (at, r["Follows"])))
                continue
            derived = deeper(followed.get("Order"))
            why = "it follows %s, whose order is %s" % (r["Follows"], followed.get("Order"))
        if r["Order"] != derived:
            out.append((rule, "%s states Order %s, where its lineage gives %s: %s" % (at, r["Order"], derived, why)))
    return out


# @canon-spec specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: orders-follow-their-lineage]
def order_problems(rep, ctx, named):
    """-> [(rule, message)]: a Settlement or a Changed Place stating an order other than its lineage gives, as § A
    Check's Report § What the Design Script Checks works it out: a Settlement's from its own Lands On and from the Lands
    On of each finding it settles, taking the deeper. A Lands On counts only where the report it cites is of the
    design's current major version and not cut short, and the change it names counts
    for a line, one taken in by
    widening the goals starting its line again."""
    out, settling, causing = [], ctx["rule"]("Settlement"), ctx["rule"]("Causes")
    reports = dict(named, **{ctx["report_rel"]: rep})

    def reading(value):
        """-> (the order a Lands On's value gives, why), or None where it names no change a report holds, its key
        reported apart."""
        place = place_of(value or "")
        if not place:
            return ORDERS[0], "it lands on no earlier change"
        earlier = earlier_order(place, reports) if is_change(place) else None
        if earlier is None:
            return None
        if place[0] not in ctx["counted"]:
            return ORDERS[0], "it lands on %s, of no report binding the design in its current major version" % value
        if earlier[1]:
            return ORDERS[0], "it lands on %s, a fix the user took in by widening the goals, which starts its line again" % value
        return deeper(earlier[0]), "it lands on %s, whose order is %s" % (value, earlier[0])

    for s in rep["settlements"]:
        where = "line %d, Settlement %s" % (s["_line"] + 1, s.get("Settlement", ""))
        if s.get("Order") not in ORDERS:
            continue
        # the builder's reading and each writer's, the deeper deciding (specs/AGENTS.md § Design, Refactor, Refine
        # § Settling a Round § Order and Lineage)
        readings = [reading(s.get(LANDS_ON))] + [reading(f.get(LANDS_ON)) for f in findings_of(rep, s) if f.get(LANDS_ON)]
        readings = [r for r in readings if r is not None]
        if not readings:
            continue
        derived, why = max(readings, key=lambda r: ORDERS.index(r[0]))
        if s["Order"] != derived:
            out.append((settling, "%s states Order %s, where its lineage gives %s: %s" % (where, s["Order"], derived, why)))
    for c in rep["records"]["Causes"]:
        settles = {k for s in rep["settlements"] + ctx["judgment_settlements"]
                   if cause_key(s.get("Cause", ""), ctx["report_rel"]) == c.get("Cause") for k in settled_findings(s)}
        for change in c.get("Proposed Change") or []:
            if isinstance(change, dict):
                out += place_order_problems(change.get("Places"), settles, "Cause %s's Proposed Change" % c.get("Cause", ""), causing)
    for s in rep["settlements"]:
        out += place_order_problems(s.get("Places"), set(settled_findings(s)), "Settlement %s" % s.get("Settlement", ""), settling)
    return out


# @canon-spec specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: report-keys-name-records]
def key_problems(rep, ctx, named, handed_back=False):
    """-> [(rule, message)]: a key the report cites naming no record a report of the design's current major version holds, this
    report among them: a Finding a Settlement settles, the Cause it lies in and the Search a Proposed Change cites, each
    by its key alone in this report; each Lands On, a Finding's or a Settlement's, other than `none` naming a Cause or a
    Settlement by its report and its key; and each record a citation of a report in the design's folder names, the
    Cause a Cause continues or a Lands On names by such a citation. As the report is handed back, before the builder's
    Settlement names its Earlier Reports, a citation of a report standing in the design's folder that no entry names yet,
    the round being settled, is read from that report; settling holds it to the Earlier Reports. A key a cold agent
    cited is held as its report is handed back and as it is taken up, and by no check after: each line
    ctx["taken_up"] gives is passed over."""
    recs, out, taken_up = rep["records"], [], ctx["taken_up"]
    keys = lambda part, field: {r.get(field) for r in recs[part]}
    settling, causing = ctx["rule"]("Settlement"), ctx["rule"]("Causes")
    for s in rep["settlements"]:
        where = "Settlement %s" % s.get("Settlement", "")
        out += [(settling, "%s settles %s, which no Finding of the report is" % (where, k))
                for k in settled_findings(s) if k not in keys("Findings", "Finding")]
        if "Cause" in s and place_of(s["Cause"]) is None and s["Cause"] not in keys("Causes", "Cause"):
            out.append((settling, "%s names a Cause the report does not hold: %s" % (where, s["Cause"])))
        if s.get("Carried By", "").strip() not in ("", "none") \
                and s["Carried By"].strip() not in set(step_lines(ctx["design_text"]).values()):
            out.append((settling, "%s is carried by a step the design does not hold: %s" % (where, s["Carried By"])))
    # each Lands On, a Finding's as it is handed back and a Settlement's as it is settled, `none` or naming a Cause or a
    # Settlement by its report and its key
    for rule, one, rec in [(ctx["rule"]("Findings"), "Finding %s" % f.get("Finding", ""), f) for f in recs["Findings"]
                           if f["_line"] not in taken_up] \
            + [(settling, "Settlement %s" % s.get("Settlement", ""), s) for s in rep["settlements"]]:
        value = rec.get(LANDS_ON, "").strip()
        if not value or value.strip("`") == "none":
            continue
        if place_of(value) is None:
            out.append((rule, "%s lands on an earlier change not cited with its report: %s" % (one, value)))
        elif not is_change(place_of(value)):
            out.append((rule, "%s lands on %s, which is neither a Cause nor a Settlement" % (one, value)))
    for c in recs["Causes"]:
        if "Continues" in c and place_of(c["Continues"]) is None:
            out.append((causing, "Cause %s continues a Cause not cited with its report: %s" % (c.get("Cause", ""), c["Continues"])))
        for change in c.get("Proposed Change") or []:
            if isinstance(change, dict) and "Search" in change and change["Search"] not in keys("Searches", "Search"):
                out.append((causing, "Cause %s's Proposed Change cites a Search the report does not hold: %s" % (c.get("Cause", ""), change["Search"])))
    reports = dict(named, **{ctx["report_rel"]: rep})
    # a report of research names among its Earlier Reports the round being settled, whose report stands handed back in
    # the design's folder while its entry waits on the settling's end, so a cause naming that round's finding is read
    # from the report so named
    if rep["records"]["Read Assessments"]:
        for path in earlier_paths(rep) - set(reports):
            if path.startswith(ctx["folder"]) and (Path(ctx["root"]) / path).is_file():
                reports[path] = read_report(read(Path(ctx["root"]) / path))
    cited = [p for i, line in enumerate(strip_fences(rep["text"]).split("\n")) if i not in taken_up for p in cited_places(line)]
    for place in cited:
        path, part, selector = place
        if not path.startswith(ctx["folder"]) or not part or not selector or ": " not in selector:
            continue
        key, value = selector.split(": ", 1)
        held = reports.get(path)
        if held is None and handed_back and (Path(ctx["root"]) / path).is_file():
            # the round being settled, its report handed back while its entry waits on the settling's end; the
            # report's Earlier Reports, the builder's part, does not exist yet to name it
            held = reports[path] = read_report(read(Path(ctx["root"]) / path))
        if held is None:
            out.append((FORM_RULE, "it cites %s, in a report no entry of the design's current major version names" % cite(place)))
        elif not any(r.get(key) == value for r in (held["settlements"] if part == "Settlement" else held["records"].get(part, []))):
            out.append((FORM_RULE, "it cites %s, a record that report does not hold" % cite(place)))
    return out


def text_at(root, path, kept):
    """-> a file's text as a search reads it: at the last commit where a send-back's kept changes stand, as
    working-files/main.md § A Design Document § The States It Moves Through § A Send-back has a reading made, else as it
    stands; None where it cannot be read."""
    if path in kept:
        shown = subprocess.run(["git", "show", "HEAD:" + path], capture_output=True, cwd=root)
        return shown.stdout.decode("utf-8", "replace").replace("\r\n", "\n") if shown.returncode == 0 else None
    try:
        return (root / path).read_text(encoding="utf-8").replace("\r\n", "\n")
    except (OSError, UnicodeDecodeError):
        return None


def step_lines(design_text):
    """-> {0-based line: the Name of the design's step holding it}."""
    out = {}
    for step in read_steps(design_text) or []:
        if step["item"]["fields"]:
            out.update({n: step["name"] for n in step["lines"] + [n for ob in step["objectives"] for n in ob["lines"]]})
    return out


def line_places(path, text, steps=None):
    """-> each 0-based line's place: in a design's step, that step; in a Markdown file, the section holding it; else, or
    before a file's first section, the file."""
    holding = {}
    if path.endswith(".md"):
        for lineage, (h, end) in sections(text).items():
            holding.update({n: lineage for n in range(h, end)})
    steps = steps or {}
    return lambda n: (path, "Design Plan Steps", "Name: " + steps[n]) if n in steps else (path, holding.get(n), None)


# @canon-spec specs/methodology/working-files/main.md § A Design Document § The Kinds of Change
def file_kind(path, skills, code):
    """-> a file's kind of change, or None for a working file; code, the code roots and the paths excluded from them."""
    if is_working_file(path):
        return None
    roots, excluded = code
    inside = lambda p, dirs: any(p == d or p.startswith(d + "/") for d in dirs)
    if inside(path, roots) and not inside(path, excluded):
        return "code"
    if path == "README.md" or path.startswith("docs/"):
        return "documentation"
    return kind_of(path, skills) or "other"


# @canon-spec specs/methodology/design-workflow/designs-reviews.md § A Design's Reviews
# the Files of the Sub-scopes table, each sub-scope's files by the kinds it holds, the one copy the audit's script and the
# log's check both read
def sub_scope_of(path, kind):
    """-> the sub-scope a file of the kind file_kind gives it lies in, or None for code and the working files."""
    if kind == "canon-specs":
        return "skills" if path.startswith(".ai/skills/") else "core-canon"
    return kind if kind in SUB_SCOPES else None


# @canon-spec specs/methodology/working-files/main.md § A Design Document § Applying and Committing
def design_changes(root, design_text):
    """-> the paths of a design's changes, read the one way: with version control, the files changed against the last
    commit, a file added, edited or removed, the untracked files among them; with none, the files and directories its
    Target names, a directory read in place of the files created under it, and the places its direct-edit and
    user-edit entries log."""
    try:
        runs = [subprocess.run(args, capture_output=True, text=True, cwd=root)
                for args in (["git", "diff", "--name-only", "HEAD"], ["git", "ls-files", "--others", "--exclude-standard"])]
    except FileNotFoundError:
        runs = []
    if runs and all(run.returncode == 0 for run in runs):
        return {p.strip() for run in runs for p in run.stdout.splitlines() if p.strip()}
    target = re.search(r"^\*\*Target:\*\*(.*)$", design_text, re.M)
    paths = set(re.findall(r"`([^`]+)`", target.group(1))) if target else set()
    paths |= {place.split(" § ")[0].strip().strip("`") for kind, _, f in log_entries(design_text)
              if kind in ("direct-edit", "user-edit") for place in f.get("Places", "").split(";") if place.strip()}
    return {p.rstrip("/") for p in paths if p}


def changed_kinds(root, design_text):
    """-> each file kind file_kind gives the design's changes, with the sub-scope each lies in."""
    import code_checks
    skills, code = skill_dirs(root), code_checks.code_roots(root) or ([], [])
    kinds = {(p, file_kind(p, skills, code)) for p in design_changes(root, design_text)}
    return {k for _, k in kinds if k}, {s for s in (sub_scope_of(p, k) for p, k in kinds) if s}


# @canon-spec specs/methodology/working-files/main.md § Design Log Entry § Script Checks [Name: settled-sub-scopes-keep-what-changed]
def changed_sub_scopes(root, design_text):
    """-> the sub-scopes holding a file the design changed."""
    return changed_kinds(root, design_text)[1]


# @canon-spec specs/methodology/working-files/main.md § Design Log Entry § Script Checks [Name: audits-run-or-bypassed]
def check_audits(value):
    """--check-audits DESIGN: refuses a design whose log, after its last apply entry, records neither the run nor the
    user's bypass of an audit the design must run, the specs audit where it changed a file of any sub-scope and the
    code audit where it changed code; -> 0, or 1 naming each audit missing."""
    design = design_file(value)
    if design is None:
        return 2
    text = design.read_bytes().decode("utf-8").replace("\r\n", "\n")
    kinds, sub_scopes = changed_kinds(repo_root(), text)
    owed = ({"specs"} if sub_scopes else set()) | ({"code"} if "code" in kinds else set())
    entries = log_entries(text)
    applies = [i for i, e in enumerate(entries) if e[0] == "apply"]
    after = entries[applies[-1] + 1:] if applies else []
    ran = {"audit-specs": "specs", "verify-spec-implementation": "code"}
    accounted = {ran[k] for k, _, _ in after if k in ran} | {f.get("Audit") for k, _, f in after if k == "audit-bypass"}
    names = {"specs": "the specs audit, .ai/skills/audit-specs/", "code": "the code audit, .ai/skills/verify-spec-implementation/"}
    return report("check-audits " + design.stem, [(design.stem, "neither run nor bypassed since the last apply entry: "
                                                    + names[a]) for a in sorted(owed - accounted)])


# @canon-spec specs/methodology/working-files/main.md § A Check's Report § What the Design Script Checks
# the field a canon design's Scope held before research searched every durable file, naming the sub-scopes its
# research was settled on: read only for the ground of a Search logged before a Search held a Kind
SEARCH_SUB_SCOPES = "Search Sub-scopes"


# @canon-spec specs/methodology/working-files/main.md § A Check's Report § What the Design Script Checks
def search_ground(root, design_rel, design_text, target, kept):
    """-> a function giving a Search's ground as {path: text}, read once: the design document and the files of each
    kind of those its Target names, a canon design's own kind among them, with, for canon-specs, the files of each sub-scope its frame's Search Sub-scopes
    names, and, for application-specs, the code; the working files aside."""
    held = {}

    def ground():
        if not held:
            import code_checks
            skills, code = skill_dirs(root), code_checks.code_roots(root) or ([], [])
            kind = lambda p: file_kind(p, skills, code)
            # a canon design's ground holds the two sub-scopes its kind spans before its Target names a file
            design_kind = re.search(r"^\*\*Kind:\*\*\s*(\S+)", design_text, re.M)
            kinds = {kind(p) for p in target} | ({"canon-specs"} if design_kind and design_kind.group(1) == "canon-specs" else set())
            field = field_of(frame_parts(design_text).get("Scope"), SEARCH_SUB_SCOPES)
            settled = set(names_of(field) or []) if "canon-specs" in kinds and field is not None else set()
            scope = set(scope_files(root)) if settled else set()
            for path in sorted(tracked(root, others=True) or scope_files(root)):
                k = kind(path)
                if k in kinds or (path in scope and sub_scope_of(path, k) in settled) \
                        or ("application-specs" in kinds and k == "code"):
                    text = text_at(root, path, kept)
                    if text is not None:
                        held[path] = text
            held[design_rel] = design_text
        return held
    return ground


# @canon-spec specs/methodology/working-files/main.md § A Check's Report § Search
# the fields a Search held before its record held a Kind, under which a report the log holds is still read
LOGGED_SEARCH_FIELDS = ("Search", "For", "Pattern", "Places", "Goals")
# the kind of search giving a part of a ranking, every other giving every place
MEANING = "meaning"
SEARCH_KINDS = ("citers", "cited sections", "lines", "terms", "code structure", MEANING, "pattern")
CURRENT_FILES, COMMITTED_FILES, WORKING_FILES_TARGET = "current-durable-files", "committed-durable-files", "working-files"
# the moments a Search is read as its own report is checked: as a cold agent hands its report back, as the builder
# takes it up, and as the settled report is checked and its entry appended
HANDED_BACK, TAKEN_UP, SETTLED = "handed back", "taken up", "settled"
# where a question names nothing to ask of, as the search tells its caller, by what each refusal of a research's report
# turns on: the Query alone, or what the checkout holds
NAMES_NO_WORD = "a term or a passage reducing to no word"
NAMES_NO_PLACE = "a citation naming no place among the files the search reads"
NAMES_NO_FILE = "a path under which no file of the target stands"
SNAPSHOT_CODE = re.compile(r"[0-9a-f]{16}")


def logged_form(s):
    """Whether a Search is written as one was before its record held a Kind: it holds a Pattern and no Kind."""
    return "Pattern" in s and "Kind" not in s


def unquoted(value):
    """-> a field's value with the one pair of backticks or quotes around the whole of it taken off."""
    value = str(value or "").strip()
    return value[1:-1] if len(value) > 1 and value[0] == value[-1] and value[0] in "`\"" else value


def search_target(s):
    """-> (the target a Search names, the commit it holds or None, the paths it is narrowed to)."""
    commit = unquoted(s.get("Commit", ""))
    return (unquoted(s.get("Target", "")) or CURRENT_FILES, commit if commit and commit != "none" else None,
            [n for n in names_of_text(s.get("Narrowed To", "")) if n != "the whole"])


def reviewer_keys(rep):
    """-> what the key of a reviewer's Search opens with, its Reviewer Reading's key and a hyphen, for each reviewer."""
    return tuple(k for k in (as_record(r).get("Reviewer", "") + "-" for r in rep["raw"].get(REVIEW_READING, []) if r and r[0][0] is not None) if k != "-")


# @canon-spec specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: searches-cover-their-matches]
def serves_no_goal(s, rep, ctx):
    """Whether a Search may hold `none` in its Goals: a reviewer's, one in the report of an audit's triage, or one a
    tactical fix's Proposed Change names where each Finding its Cause settles names no goal in its Affected Goals. A
    Search in a report of research never may."""
    if rep["records"].get("Read Assessments"):
        return False
    key = s.get("Search", "")
    if ctx["kind"] in AUDITS or (reviewer_keys(rep) and key.startswith(reviewer_keys(rep))):
        return True
    for c in rep["records"]["Causes"]:
        if any(isinstance(ch, dict) and ch.get("Kind") == "tactical fix" and ch.get("Search") == key for ch in c.get("Proposed Change") or []):
            settled = [f for st in rep["settlements"] if cause_key(st.get("Cause", ""), ctx["report_rel"]) == c.get("Cause") for f in findings_of(rep, st)]
            if settled and not any(names_of_text(f.get("Affected Goals", "")) for f in settled):
                return True
    return False


# @canon-spec specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: searches-cover-their-matches]
def search_form_problems(s, where):
    """-> [message]: a Search written in the form out of what its fields' conditions give: its Snapshot no snapshot
    code, its Narrowed To wanting where its Target is the working files, and, where its Kind is a ranking's, its
    Ranking Part wanting or its Places more than that part spans, or `none` other than where the part is none."""
    out, kind = [], unquoted(s.get("Kind", ""))
    if "Snapshot" in s and not SNAPSHOT_CODE.fullmatch(unquoted(s["Snapshot"])):
        out.append("%s's Snapshot is %s, not a snapshot code, sixteen hexadecimal digits" % (where, s["Snapshot"]))
    require(out, where, s, "Narrowed To", search_target(s)[0] == WORKING_FILES_TARGET or "Narrowed To" in s, "where its Target is working-files")
    require(out, where, s, "Ranking Part", kind == MEANING, "where its Kind is meaning")
    if kind == MEANING and "Ranking Part" in s:
        part, held = unquoted(s["Ranking Part"]), len(place_list(s.get("Places", "")))
        span = re.fullmatch(r"(\d+) to (\d+)", part)
        if not span and part != "none":
            out.append("%s's Ranking Part is %s, neither none nor its first place's number in the ranking and its last's, as 1 to 20" % (where, part))
        elif part == "none" and held:
            out.append("%s's Ranking Part is none, and its Places hold %d" % (where, held))
        elif span and (int(span.group(1)) < 1 or held > int(span.group(2)) - int(span.group(1)) + 1):
            out.append("%s holds %d Places, more than its Ranking Part, %s, spans" % (where, held, part))
        elif span and not held and "".join(names_of_text(s.get("Places", ""))) == "none":
            out.append("%s's Places hold none, which a Search by meaning holds only where its Ranking Part is none" % where)
    return out


def search_place(place):
    """-> a place the search gave as a place a report cites, (path, lineage or None, selector or None), or None."""
    m = re.match(r"`([^`]+)`", str(place))
    return place_of("`%s`" % m.group(1)) if m else None


# @canon-spec specs/methodology/working-files/main.md § A Check's Report § What the Design Script Checks
def run_search(s, ctx):
    """-> (the places a Search written in the form gives, where its question names nothing, None), run through the
    search the skills share exactly as it was asked: its Kind and its Query, over the files its Target asks of, within
    the paths it was narrowed to; or (None, None, why, whether the search itself refused what was asked) where it
    cannot be run. A Search naming the durable files as they stand is run over them as every reading of the files as
    they stand is made, at the last commit where ctx["kept"] has such a reading take it; one naming the committed files
    is run over the commit it holds, and over the last commit where it holds none; and the working files it names are
    read as they stand. Each Search is run once for each reading, and the design script keeps nothing of a run: the
    search gives the answer it kept where what was asked, the files and its own reading stand."""
    kind, query = unquoted(s.get("Kind", "")), unquoted(s.get("Query", ""))
    target, commit, narrowed = search_target(s)
    asked = (kind, query, target, commit, tuple(narrowed))
    held = ctx.setdefault("runs", {})
    if asked in held:
        return held[asked]
    try:
        import search as searching
    except ImportError as exc:
        held[asked] = (None, None, "the search the skills share cannot be loaded: %s" % exc, False)
        return held[asked]
    reads = COMMITTED_FILES if target == CURRENT_FILES and ctx.get("kept") else target
    try:
        engines = ctx.setdefault("engines", {})
        at = (reads, commit, tuple(narrowed) if reads == WORKING_FILES_TARGET else ())
        if at not in engines:
            engines[at] = searching.Search(ctx["root"], quiet=True, target=reads, commit=commit, paths=narrowed if reads == WORKING_FILES_TARGET else None)
        engine = engines[at]
        if kind == "citers":
            result = engine.citers(query, narrowed)
        elif kind == "cited sections":
            result = engine.cited_sections(narrowed)
        elif kind == "lines":
            result = engine.lines(query)
        elif kind == "terms":
            result = engine.terms(query, narrowed)
        elif kind == "code structure":
            structure, _, name = query.partition(" ")
            result = engine.code_structure(structure, name.strip(), narrowed)
        elif kind == "pattern":
            result = engine.pattern(query, narrowed)
        else:
            raise ValueError("no kind of search giving every place: %s" % (kind or "none named"))
        places = [p for p in (search_place(x) for x in result.places) if p]
        held[asked] = ([p for i, p in enumerate(places) if p not in places[:i]], list(result.names_nothing), None, False)
    except searching.MissingRequirements as exc:
        held[asked] = (None, None, "the search cannot be run, since something it requires is missing: %s" % exc, False)
    except searching.CannotSearch as exc:
        held[asked] = (None, None, str(exc), True)
    except (ValueError, re.error) as exc:
        held[asked] = (None, None, "the search refuses what it asks: %s" % exc, True)
    return held[asked]


# @canon-spec specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: searches-cover-their-matches]
def search_problems(rep, ctx, moment=SETTLED):
    """-> [(rule, message)]: each Search of a report read as its own report is checked, at the moment given. A Search
    whose Kind gives every place, in a report other than research's, is run as it was asked and each place it gives
    must stand among its Places; one the search refuses refuses the report. A Search a cold agent recorded, a
    reviewer's or any in a handed-off judgment's report, is run as its report is handed back and as it is taken up,
    and by no check after: it stands at a line ctx["taken_up"] gives and is passed over, the part holding it then
    held to its fingerprint alone, by cold_parts_problems. The builder's own is run as the settled report is
    checked. A Search in a report of research, one holding Read Assessments, is held as its report is handed back and
    taken up to nothing it gives: its report is refused where the search refuses what the Search asks or its term or
    passage reduces to no word, and, as it is handed back alone, where its citation names no place or a path it is
    narrowed to holds no file. A Search by meaning is never run. A Search logged holding a Pattern is read as it was
    before the record held a Kind, its Pattern run over its ground and its matches held to its Places, a research's
    held here to nothing."""
    out, research = [], bool(rep["records"].get("Read Assessments"))
    for s in rep["records"]["Searches"]:
        key = s.get("Search", "")
        if s["_line"] in ctx["taken_up"]:
            continue
        if logged_form(s):
            if research:
                continue
            matched = search_matches(s, ctx)
            if isinstance(matched, re.error):
                out.append("Search %s's Pattern is no regular expression Python's re reads: %s" % (key, matched))
                continue
            listed = place_list(s.get("Places", ""))
            out += ["Search %s's Pattern matches in %s, which its Places do not cover" % (key, cite(p))
                    for p in matched if not covered(listed, p)]
            continue
        if unquoted(s.get("Kind", "")) == MEANING:
            continue
        places, nothing, why, _ = run_search(s, ctx)
        if why:
            out.append("Search %s cannot be run as it was asked: %s" % (key, why))
        elif research:
            if NAMES_NO_WORD in nothing:
                out.append("Search %s asks nothing: its term or passage reduces to no word" % key)
            if moment == HANDED_BACK and NAMES_NO_PLACE in nothing:
                out.append("Search %s asks nothing: its citation names no place among the files its Target asks of" % key)
            if moment == HANDED_BACK and NAMES_NO_FILE in nothing:
                out.append("Search %s asks nothing under a path it is narrowed to, where no file of its Target stands" % key)
        else:
            listed = place_list(s.get("Places", ""))
            out += ["Search %s gives %s, which its Places do not cover" % (key, cite(p)) for p in places if not covered(listed, p)]
    return [(ctx["rule"]("Searches"), p) for p in out]


def search_matches(s, ctx):
    """-> the places the Pattern of a Search logged before its record held a Kind matches in, run again over its ground
    by the design script's own reading of a regular expression, `^` and `$` matching where a file's text starts and
    ends, each once in the order found, or the error where Python's re reads no regular expression in it; run once for
    each such Search a report holds."""
    pattern = s.get("Pattern", "")
    pattern = pattern[1:-1] if len(pattern) > 1 and pattern[0] == pattern[-1] == "`" else pattern
    held = ctx.setdefault("matches", {})
    if pattern in held:
        return held[pattern]
    try:
        compiled = re.compile(pattern)
    except re.error as exc:
        held[pattern] = exc
        return exc
    found = []
    for path, text in ctx["ground"]().items():
        place_at = line_places(path, text, ctx["steps"] if path == ctx["design_rel"] else None)
        starts = [0] + [m.end() for m in re.finditer("\n", text)]
        for m in compiled.finditer(text):
            if m.end() == m.start():
                continue
            place = place_at(bisect.bisect_right(starts, m.start()) - 1)
            if place not in found:
                found.append(place)
    held[pattern] = found
    return found


# @canon-spec specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: reads-assessed]
def reads_assessed_problems(rep, ctx):
    """-> [(rule, message)]: in a report holding Read Assessments, a place outside the design document its Reads holds,
    the places the builder named, lying within no Read Assessment's Area of its own, as § A Check's Report has one place
    cover another; its Searches' matches are held over the union of the binding research by
    research-covers-its-matches. The Reads and the Read Assessments are a cold agent's, held as its report is handed
    back and as it is taken up, and by no check after, where ctx["taken_up"] gives their lines."""
    assessed = [a for a in rep["records"]["Read Assessments"] if a["_line"] not in ctx["taken_up"]]
    if not assessed:
        return []
    areas = [p for p in (place_of(a.get("Area", "")) for a in assessed) if p]
    reads = place_list(next((record_types.value_of(f) for f in rep["blocks"].get("Reading", []) if f["key"] == OWN_READING), ""))
    out = []
    places = [(p, "its Reads hold") for p in reads]
    seen = set()
    for place, how in places:
        if place[0] == ctx["design_rel"] or place_key(place) in seen or covered(areas, place):
            continue
        seen.add(place_key(place))
        out.append((ctx["rule"]("Read Assessments"), "%s, a place %s, lies within no Read Assessment's Area" % (cite(place), how)))
    return out


# @canon-spec specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: findings-anchored-in-the-design]
def anchor_problems(rep, ctx):
    """-> [(rule, message)]: a Finding whose Verdict is a mark naming in its Affected Goals, Affected Frame Outcomes and
    Affected Step Objectives no part of the design and citing in its Broken Rules no rule it breaks, or naming a goal, a
    Frame Outcome or a step Objective the design its Title names does not hold. A cold agent's Finding is read against
    the design as its report is handed back and as it is taken up, and by no check after, where ctx["taken_up"] gives
    its line: a part of the design the builder removes while settling leaves the taken-up Finding naming it standing."""
    plan, out = read_plan(ctx["design_text"]), []
    rule = WF + " § A Check's Report § Finding"
    for f in rep["records"]["Findings"]:
        if f.get("Verdict") not in MARKS or f["_line"] in ctx["taken_up"]:
            continue
        where = "line %d, Finding %s" % (f["_line"] + 1, f.get("Finding", ""))
        named = {key: [n for n in names_of_text(f.get(key, "")) if n != "none"] for key in ANCHORS}
        if not any(named.values()) and not place_list(f.get(BROKEN_RULES, "")):
            out.append((rule, "%s, marked a %s, names no goal, Frame Outcome or step Objective it bears on and cites no rule "
                              "it breaks" % (where, f.get("Verdict"))))
        for key, kind in ANCHORS.items():
            out += [(rule, "%s's %s names %s, which the design %s does not hold" % (where, key, n, ctx["design"]))
                    for n in named[key] if n not in plan[kind]]
    return out


def log_entries(text):
    """-> each entry of a design's log as (kind, count, {field: value}), in the order the entries stand."""
    out = []
    for record in records(section(text, LOG)) or []:
        f = {k: v.strip() for k, v in record}
        m = re.fullmatch(r"([a-z-]+?)-(\d+)", f.get("Entry", ""))
        if m:
            out.append((m.group(1), int(m.group(2)), f))
    return out


# @canon-spec specs/methodology/working-files/main.md § A Check's Report § Over Applied Work, and a Phase's Record
def over_applied(entries):
    """Whether an entry appended after these lies over applied work: after the design's last apply entry, with no
    entered entry after that."""
    applies = [i for i, e in enumerate(entries) if e[0] == "apply"]
    return bool(applies) and not any(e[0] == "entered" for e in entries[applies[-1] + 1:])


# @canon-spec specs/methodology/working-files/main.md § A Check's Report § Over Applied Work, and a Phase's Record
def phase_start(entries, applied):
    """-> where the phase an entry appended after these stands in starts: a post-apply review's after the design's last
    apply entry, and an adversarial review's after its last `design-reassessment` entry, an old reassessment read as
    one, or its last entered entry sent back, to the step back or not, whichever stands later, or at the log's start."""
    if applied:
        return max(i for i, e in enumerate(entries) if e[0] == "apply") + 1
    return max([i + 1 for i, e in enumerate(entries)
                if starts_major(e) or (e[0] == "entered" and e[2].get("Reason") in SENT_BACK)],
               default=0)


# @canon-spec specs/methodology/working-files/main.md § A Check's Report § Over Applied Work, and a Phase's Record
def phase_record(design, entries, applied, root):
    """-> [(path, report)] for each report of the phase's record: the reports binding the design whose entries stand in
    the phase, its review entries' and its handed-off judgments', of the current major version and none cut short; no steer
    unbinds one."""
    review = REVIEWS[1] if applied else REVIEWS[0]
    start, held = max(phase_start(entries, applied), major_start(entries)), set(binding(entries, design))
    return [(rel_to(report_file(design, k, n), root), load_report(design, k, n))
            for i, (k, n, _) in enumerate(entries) if i >= start and i in held and k in (review, JUDGMENT)]


# @canon-spec specs/methodology/working-files/main.md § A Check's Report § Over Applied Work, and a Phase's Record
def carried_reports(entries, design=None):
    """-> [(kind, n)] for each check's entry over an apply the design was sent back from whose report binds the design
    still: one of the current major version and not cut short, standing after that
    apply entry and before the next
    entered entry, no post-apply-review entry standing after a later apply entry."""
    out, held = [], set(binding(entries, design))
    for a, (k, _, _) in enumerate(entries):
        if k != "apply" or a not in held:
            continue
        back = next((i for i in range(a + 1, len(entries)) if entries[i][0] == "entered"), None)
        if back is None:
            continue
        later = next((i for i in range(back, len(entries)) if entries[i][0] == "apply"), None)
        if later is not None and any(e[0] == REVIEWS[1] for e in entries[later + 1:]):
            continue
        out += [(kk, n) for i, (kk, n, _) in enumerate(entries) if a < i < back and i in held
                and kk in REVIEWS + (JUDGMENT, "audit-specs", "verify-spec-implementation")]
    return out


def load_report(design, kind, n):
    path = report_file(design, kind, n)
    return read_report(read(path)) if path.is_file() else read_report("")


# @canon-spec specs/methodology/working-files/main.md § A Check's Report § What the Design Script Checks
def named_reports(design, entries, root):
    """-> {path: report} for each report a check's entry of the design's current major version names, the reports whose
    records a key a report cites must name."""
    kinds = log_type()[2]
    return {rel_to(report_file(design, k, n), root): load_report(design, k, n)
            for k, n, _ in (entries[i] for i in of_current_major(entries)) if "Model" in kinds.get(k, ())}


def round_change_followed(design, entries, applied, root):
    """-> (path, report) of the round whose change a self-review appended after these follows: the last review entry of
    its phase after the design's last self-review entry, where its report holds a Proposed Change; else None."""
    last = max((i for i, e in enumerate(entries) if e[0] == "self-review"), default=-1)
    review = REVIEWS[1] if applied else REVIEWS[0]
    rounds = [i for i, e in enumerate(entries) if i > max(last, phase_start(entries, applied) - 1) and e[0] in REVIEWS]
    if not rounds or entries[rounds[-1]][0] != review:
        return None
    k, n, _ = entries[rounds[-1]]
    rep = load_report(design, k, n)
    return (rel_to(report_file(design, k, n), root), rep) if any(c.get("Proposed Change") for c in rep["records"]["Causes"]) else None


def judgment_settlements(design, entries):
    """-> the Settlements of each handed-off judgment settled with a round appended after these: its report standing in
    the design's folder, no entry naming it."""
    done = sum(1 for e in entries if e[0] == JUDGMENT)
    folder = report_file(design, JUDGMENT, 1).parent
    return [s for path in (sorted(folder.glob("*.md")) if folder.is_dir() else [])
            if path.stem.isdigit() and int(path.stem) > done for s in read_report(read(path))["settlements"]]


def constructs_in(path, text, lines1=None):
    """-> [(place, construct, its paths)] for each Decision Table and State Machine a file states, or, given 1-based
    lines, each standing in a section those lines change."""
    secs, out = sections(text), []
    for _, name, fields, tables, lineage in constructs.declarations(strip_fences(text), secs):
        if name not in WHOLE or lineage not in secs:
            continue
        h, end = secs[lineage]
        if lines1 is None or any(h <= n - 1 < end for n in lines1):
            out.append(((path, lineage, None), name, constructs.paths(name, fields, tables)))
    return out


def traced_constructs(ctx, reads=None):
    """-> [(the places citing it, construct, its paths)] for each Decision Table and State Machine a self-review's phase
    records a Trace of (working-files/main.md § A Check's Report § What the Design Script Checks): before the apply, each
    standing in a section a step's What names, in the files as they stand, its Trace holding the mechanism test's
    Outcome and no paths; over applied work, each a section the diff changed holds, its paths traced; for a self-review
    proving the fixes, given its Reads, only those its Reads cover, its Reads holding the reach of those fixes."""
    text_of = spec_texts(ctx["root"])
    if ctx["applied"]:
        found = [([place], name, paths) for path, lines in sorted(ctx["changes"].items()) if path in text_of
                 for place, name, paths in constructs_in(path, text_of[path], lines)]
        return [f for f in found if reads is None or covered(reads, f[0][0])]
    out, seen = [], set()
    for step in read_plan(ctx["design_text"])["steps"]:
        if "What" not in step["fields"]:
            continue
        for path, lineage, _ in named_places(str(record_types.value_of(step["fields"]["What"]))):
            if path not in text_of:
                continue
            for place, name, _ in constructs_in(path, text_of[path]):
                if place_key(place) not in seen and (lineage is None or place[1] == lineage
                                                     or place[1].startswith(lineage + " § ")):
                    seen.add(place_key(place))
                    out.append(([place], name, []))
    return out


def path_name(text):
    return re.sub(r"\s*,\s*", ", ", re.sub(r"\s+", " ", text.replace("`", ""))).strip()


def required_checks(ctx, reads=None):
    """-> [(Builder Check kind, the places its Places Checked must cover)] for each Builder Check required of a
    self-review, as § A Check's Report § Kinds of Builder Check gives it: the construct choice over applied work alone,
    and, for a pass proving the fixes, given its Reads, a differential test of each script they cover;
    after a send-back and before the plan's next approval, a carried finding for each Finding a binding report over the
    apply gives Lies In the plan or a Carried By; and, of the first self-review of a major version, the one no
    `self-review` entry stands before since that major version's start, a problem re-evaluation for each place the
    design's Problem cites, so a self-review of a major version whose first the log already holds owes none."""
    entries, out = ctx["entries"], [(k, []) for k in EVERY_SELF_REVIEW]
    own = next((i for i, (k, m, _) in enumerate(entries) if "%s-%d" % (k, m) == ctx["entry"]), len(entries))
    if not any(e[0] == "self-review" for e in entries[major_start(entries[:own]):own]):
        out.append((PROBLEM_RE_EVALUATION, list(dict.fromkeys(named_places(section(ctx["design_text"], "The Problem") or "")))))
    back = max((i for i, e in enumerate(entries) if e[0] == "entered" and e[2].get("Reason") in SENT_BACK), default=-1)
    if back > max((i for i, e in enumerate(entries) if e[0] == "apply"), default=-1) \
            and not any(e[0] == "plan-approval" for e in entries[back + 1:]):
        carried = [(rel_to(report_file(ctx["design_path"], k, n), ctx["root"]), "Findings", "Finding: " + f)
                   for k, n in carried_reports(entries, ctx["design_path"])
                   for s in load_report(ctx["design_path"], k, n)["settlements"]
                   if (s.get("Lies In") == "the plan" or s.get("Carried By", "").strip() not in ("", "none"))
                   and s.get("Verdict") in MARKS for f in settled_findings(s)]
        out += [(CARRIED, carried)] if carried else []
    out += [(CONSTRUCT_CHOICE, [])] if ctx.get("design_kind") in SPEC_KINDS and ctx["applied"] else []
    last = max((i for i, e in enumerate(entries) if e[0] == "self-review"), default=-1)
    # an edit's place read as a citation, a part a keyed instance holds among them
    out += [(USER_EDIT, [p for p in (place_of("`%s`" % " § ".join(x for x in ps if x)) for ps in places(f.get("Places", ""))) if p])
            for k, _, f in entries[last + 1:] if k == "user-edit"]
    # one item for each question a Miss of the phase names, in every self-review
    asked = [(p, "Causes", "Cause: " + c.get("Cause", "")) for p, r in ctx["record"] for c in r["records"]["Causes"]
             for m in c.get("Misses") or [] if isinstance(m, dict) and m.get("Kind") == "question not asked"]
    out += [(MISS_QUESTION, asked)] if asked else []
    if ctx["round"]:
        path, rep = ctx["round"]
        worked = [(path, "Causes", "Cause: " + c.get("Cause", "")) for c in rep["records"]["Causes"] if c.get("Proposed Change")]
        worked += [(path, "Findings", "Finding: " + k) for k, w in last_words(rep).items() if w == "implementation flaw"]
        out += [(WORKED_CASE, worked)] if worked else []
    # the self-review before a rebuilt design's first adversarial round: each Root Cause, and each Flaw, of the
    # diagnosis the design is rebuilt from, a flaw a later change fixed among them
    starts = [i for i in major_starts(entries) if i < own]
    if starts and entries[starts[-1]][0] == DESIGN_REASSESSMENT and not any(e[0] == REVIEWS[0] for e in entries[starts[-1] + 1:own]):
        path = diagnosis_file(ctx["design_path"], entries[starts[-1]][2])
        if path is not None:
            _, flaws, causes, _, _ = read_diagnosis(read(path))
            rel = rel_to(path, ctx["root"])
            answered = [(rel, "Root Causes", "Root Cause: " + c.get("Root Cause", "")) for c in causes] + \
                       [(rel, "Flaws", "Flaw: " + f.get("Flaw", "").strip("`")) for f in flaws]
            out += [(DIAGNOSIS_ANSWERED, answered)] if answered else []
    if ctx["applied"]:
        import code_checks
        skills, code = skill_dirs(ctx["root"]), code_checks.code_roots(ctx["root"]) or ([], [])
        # the code the specs govern is no script, its tests checking it
        scripts = [(p, None, None) for p in sorted(ctx["changes"]) if p.endswith(SCRIPTS) and file_kind(p, skills, code) != "code"
                   and (reads is None or any(r[0] == p for r in reads))]
        # and, where the entry's appending ran the design script's kept comparison, each design it listed, whose
        # reading the builder judges as a difference the change meant or a fault
        scripts += [(p, None, None) for p in ctx.get("compared") or []]
        out += [(DIFFERENTIAL, scripts)] if scripts else []
    return out


# @canon-spec specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: traces-name-their-paths]
def trace_problems(rep, ctx):
    """-> [(rule, message)]: a construct a self-review's phase traces with no Trace, or a Trace leaving out a path."""
    out, rule = [], ctx["rule"]
    reads = own_reads(rep) if ctx.get("proving") else None
    for mechanisms, name, paths in traced_constructs(ctx, reads):
        traced = [t for t in rep["records"]["Traces"] if set(cited_places(t.get("Mechanism", ""))) & set(mechanisms)]
        if not traced:
            out.append((rule("Traces"), "no Trace of the %s at %s" % (name, cite(mechanisms[-1]))))
            continue
        done = {path_name(p.get("Path", "")) for t in traced for p in t.get("Paths") or [] if isinstance(p, dict)}
        # a row named by all its cells names its condition cells first
        out += [(rule("Traces"), "the Trace of the %s at %s leaves out a path: %s" % (name, cite(mechanisms[-1]), p))
                for p in paths if not any(d == path_name(p) or d.startswith(path_name(p) + ", ") for d in done)]
    return out


def own_reads(rep):
    """-> the places a report's own Reads hold."""
    return place_list(next((record_types.value_of(f) for f in rep["blocks"].get("Reading", []) if f["key"] == OWN_READING), ""))


# @canon-spec specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: builder-checks-required]
def builder_check_problems(rep, ctx):
    """-> [(rule, message)]: a Builder Check required of a self-review missing, or not covering its items."""
    out, rule = [], ctx["rule"]
    for check, items in required_checks(ctx, own_reads(rep) if ctx.get("proving") else None):
        made = [b for b in rep["records"]["Builder Checks"] if b.get("Kind") == check]
        if not made:
            out.append((rule("Builder Checks"), "no Builder Check of %s, which is required of it" % check))
            continue
        # an item asked more than once, a Cause naming several questions, takes a check for each time
        for p in dict.fromkeys(items):
            n = sum(1 for b in made if covered(place_list(b.get("Places Checked", "")), p))
            if not n:
                out.append((rule("Builder Checks"), "its Builder Checks of %s leave out %s" % (check, cite(p))))
            elif n < items.count(p):
                out.append((rule("Builder Checks"), "%s names %d questions, and only %d of its Builder Checks of %s cite it"
                            % (cite(p), items.count(p), n, check)))
    return out


# @canon-spec specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: reads-cover-the-misses]
def miss_read_problems(rep, ctx):
    """-> [(rule, message)]: a place a Miss of the phase names that the Reads of a self-review following a round's
    change leave out."""
    if not ctx["round"]:
        return []
    reads = own_reads(rep)
    missed = [place_of(m.get("Place", "")) for _, r in ctx["record"] for c in r["records"]["Causes"]
              for m in c.get("Misses") or [] if isinstance(m, dict)]
    return [(ctx["rule"]("Reading"), "its Reads leave out %s, a place a Miss of the phase names" % cite(p))
            for p in sorted(set(p for p in missed if p), key=place_key) if not covered(reads, p)]


def settlement_block(rep):
    return {f["key"]: record_types.value_of(f) for f in rep["blocks"].get("Settlement", [])}


# @canon-spec specs/methodology/working-files/main.md § A Check's Report § Ending Statement Owed
def owes_ending(kind):
    """Whether the report of a check of this kind states how its check ended: a review's round, a research share or a
    handed-off judgment, and the audit's triage, but not the builder's own pass or self-review."""
    return kind in REVIEWS + (JUDGMENT,) + AUDITS


# @canon-spec specs/methodology/working-files/main.md § A Check's Report § Check Ending
def report_ending(rep):
    """-> the ending a report's Settlement states, `its own settling`, `decided` or `cut short`; None where it states
    none, or one out of the field's form."""
    value = str(settlement_block(rep).get("Ending", "") or "").replace("`", "").strip()
    if value == OWN_SETTLING:
        return OWN_SETTLING
    for ending in (DECIDED, CUT_SHORT):
        if value.startswith(ending + ",") and value[len(ending) + 1:].strip():
            return ending
    return None


# @canon-spec specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: earlier-reports-listed]
def earlier_report_problems(rep, ctx):
    """-> [(rule, message)]: a report of the phase's record a round's Earlier Reports leave out."""
    earlier = place_list(settlement_block(rep).get("Earlier Reports", ""))
    return [(ctx["rule"]("Settlement"), "its Earlier Reports leave out `%s`, a report of the phase's record" % p)
            for p, _ in ctx["record"] if not covered(earlier, (p, None, None))]


# @canon-spec specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: settling-reads-cover-the-evidence]
def settling_read_problems(rep, ctx):
    """-> [(rule, message)]: a place the Evidence of a marked Finding names that a round's Settling Reads leave out and
    no Read Assessment's Area covers, of the reports of the handed-off judgments the design's log names."""
    reads = place_list(settlement_block(rep).get("Settling Reads", "")) + ctx["assessed"]()
    evidence = {p for f in rep["records"]["Findings"] if f.get("Verdict") in MARKS for ev in f.get("Evidence") or []
                if isinstance(ev, dict) for p in place_list(ev.get("Places", ""))}
    return [(ctx["rule"]("Settlement"), "its Settling Reads leave out %s, a place the Evidence of a marked Finding names, "
                                        "and no Read Assessment of a logged handed-off judgment's report covers it" % cite(p))
            for p in sorted(evidence, key=place_key) if not covered(reads, p)]


# @canon-spec specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: tactical-fixes-cover-their-searches]
def tactical_fix_problems(rep, ctx):
    """-> [(rule, message)]: a tactical fix naming a Search by meaning, or one of files its defect cannot stand in, the
    durable files as they stand with no path it is narrowed to in a report over applied work and the working files with
    the design document among its paths in any other; and a place a tactical fix's Search found that its Places leave
    out. A Search logged before its record held a Kind is held to its Places alone, as it was."""
    out, searches = [], {s.get("Search"): s for s in rep["records"]["Searches"]}
    for c in rep["records"]["Causes"]:
        for change in c.get("Proposed Change") or []:
            if isinstance(change, dict) and change.get("Kind") == "tactical fix" and change.get("Search") in searches:
                s, where = searches[change["Search"]], "Cause %s's tactical fix" % c.get("Cause")
                if not logged_form(s):
                    target, _, narrowed = search_target(s)
                    if unquoted(s.get("Kind", "")) == MEANING:
                        out.append((ctx["rule"]("Causes"), "%s names Search %s, a search by meaning, which gives a part of a ranking and "
                                                           "never every place its defect stands in" % (where, s.get("Search"))))
                    elif ctx["applied"] and (target != CURRENT_FILES or narrowed):
                        out.append((ctx["rule"]("Causes"), "%s names Search %s, which over applied work is to name %s and be narrowed "
                                                           "to no path, so it reads every durable file" % (where, s.get("Search"), CURRENT_FILES)))
                    elif not ctx["applied"] and (target != WORKING_FILES_TARGET or ctx["design_rel"] not in narrowed):
                        out.append((ctx["rule"]("Causes"), "%s names Search %s, which before the apply is to name %s with the design "
                                                           "document among the paths it is narrowed to" % (where, s.get("Search"), WORKING_FILES_TARGET)))
                wrote = change_places(change)
                out += [(ctx["rule"]("Causes"), "%s leaves out %s, a place its Search found" % (where, cite(p)))
                        for p in place_list(s.get("Places", "")) if not covered(wrote, p)]
    return out


def cover_problems(rep, ctx):
    """-> [(rule, message)]: what a self-review's records or a round's settlement leave uncovered of what § A Check's
    Report has the design script check of them, by the unit of each record."""
    if ctx["kind"] not in REVIEWS + ("self-review",):
        return []
    units = ((trace_problems, builder_check_problems, miss_read_problems) if ctx["kind"] == "self-review"
             else (earlier_report_problems, settling_read_problems, tactical_fix_problems))
    return [p for unit in units for p in unit(rep, ctx)]


# @canon-spec specs/methodology/working-files/main.md § Design Log Entry
def steer_cut(design_text, kind, n, read_at=None):
    """Whether a set of steers ended a round, read from the version and the log's order together -> True, False, or None
    where the log cannot tell: a set whose highest Changes holds the goals or a part of the frame, its steer entry
    standing before the round's entry, or before the entry the round is to be appended as, and its version past
    read_at, the version the round's report read. A Steering Decision recorded and named by no steer entry ends
    nothing. A round whose report holds no version read, one written before the field, is read as its entry stamps it,
    a steer entry standing right after it, past the judgments settled with it, leaving it undecided."""
    full, changes = log_entries(design_text), steer_changes(design_text)
    own = next((i for i, (k, m, _) in enumerate(full) if k == kind and m == n), None)
    if read_at is None:
        if own is None:
            return None
        after = [k for k, _, _ in full[own + 1:]]
        while after and after[0] == JUDGMENT:
            after.pop(0)
        return None if after and after[0] == "steer" else False
    before = full if own is None else full[:own]
    return any(material(e, changes) and entry_version(e) > read_at for e in before)


# @canon-spec specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: orders-follow-their-lineage]
def counted_reports(root, design, entries):
    """-> the reports of the checks' entries among these of the design's current major version and not
    cut short, whose changes count in a later finding's order; a set of steers changing the
    goals leaves every line counting."""
    kinds = log_type()[2]
    return {rel_to(report_file(design, entries[i][0], entries[i][1]), root) for i in binding(entries, design)
            if "Model" in kinds.get(entries[i][0], ())}


def report_context(root, design, design_text, kind, n, entries, reviewer=False):
    """-> what a report's checks read of its design and its log: its kind and entry, the design's Name and Kind, whether it lies
    over applied work, whether its Traces give their Outcome, the Settlements of the judgments settled with a round, a Search's ground, the phase's record, the round whose change a
    self-review follows, the diff's changes over applied work, the rules each part's Holds cites, and the lines of the
    report a check passes over, none until entry_report_problems gives those a taken-up report's cold agent wrote."""
    applied = over_applied(entries)
    start = phase_start(entries, applied)
    approvals = [i for i, e in enumerate(entries) if i >= start and e[0] == "plan-approval"
                 and not any(x[0] == "another-round" for x in entries[i + 1:])]
    kept = [] if applied else kept_changes(root, design_text)
    fields = dict(read_design(design)[1])
    path = report_file(design, kind, n)
    commit = last_commit(root) if applied and kind == "self-review" and not reviewer else None
    rules = {p: ", ".join(r) or FORM_RULE for p, _, _, r in report_parts(root)}
    # the report's own entry, where the log holds it already, or the entry it is to be appended as, after the rest
    own = next((i for i, (k, m, _) in enumerate(entries) if k == kind and m == n), len(entries))
    held = []

    def assessed():
        """-> the Area of each Read Assessment in the report of a handed-off judgment the design's log names, read once."""
        if not held:
            # the research of the current major version alone stands (working-files/main.md § A Design Document § Assessed Area)
            held.append([p for k, m, _ in (entries[i] for i in binding(entries, design)) if k == JUDGMENT
                         for a in load_report(design, k, m)["records"]["Read Assessments"]
                         for p in [place_of(a.get("Area", ""))] if p])
        return held[0]

    return {"assessed": assessed, "design_path": design,
            # a round the user ended: an adversarial round whose phase holds the approval before its entry, or one a
            # set of steers changing the goals or the frame ended while it ran or was settled
            # True, False, or None where a logged round's steer leaves it undecided, held then to neither rule of Causes
            "ended": kind == REVIEWS[0] and (any(i < own for i in approvals) or steer_cut(
                design_text, kind, n, report_version(read_report(read(path))) if path.is_file() else None)),
            "root": root, "kind": kind, "entry": "%s-%d" % (kind, n), "design": fields.get("Name", design.stem),
            "design_kind": fields.get("Kind", "").strip(), "applied": applied, "reviewer": reviewer, "entries": entries, "design_rel": rel_to(design, root),
            "design_text": design_text, "steps": step_lines(design_text), "report_rel": rel_to(path, root),
            "folder": rel_to(path.parents[1], root) + "/",
            "trace_outcome": kind == "self-review" and not applied and not approvals,
            # a pass proving the fixes: a self-review standing after a post-apply-review entry of the apply
            "proving": kind == "self-review" and applied and any(e[0] == REVIEWS[1] for e in entries[start:own]),
            "judgment_settlements": judgment_settlements(design, entries) if kind in REVIEWS and not reviewer else [],
            "ground": search_ground(root, rel_to(design, root), design_text,
                                    re.findall(r"`([^`]+)`", fields.get("Target", "")), kept),
            "kept": bool(kept),
            "record": phase_record(design, entries, applied, root) if not reviewer else [],
            "goals": {dict(r).get("Name", "").strip() for r in records(section(design_text, "Design Goals")) or []},
            "counted": counted_reports(root, design, entries[:own]) | {rel_to(path, root)},
            "round": round_change_followed(design, entries, applied, root) if kind == "self-review" else None,
            "changes": work_changes(root, commit)[0] if commit else {},
            "taken_up": frozenset(),
            "rule": lambda part: rules.get(part, FORM_RULE)}


def entry_report_problems(root, design, design_text, kind, n, report_text=None, compared=None):
    """-> ([(rule, message)] refusing a check's entry, the report read): the report held to its form and its layout,
    each value holding places in its form, each Finding settled once, each key naming a record, each Search's matches
    covered, each place its Reads hold assessed where it holds Read Assessments, each marked Finding anchored in the
    design, and its records covering what its check had to cover. A report the builder writes alone is held so in
    every part. One a cold agent wrote was held so in that agent's parts as it was handed back and as it was taken up,
    by handed_back_problems, and is held here in the builder's parts alone: each check passes over the lines cold_lines
    gives, so nothing the design or the files have come to hold since the take-up refuses a part the cold agent wrote,
    which cold_parts_problems holds to its fingerprint as the entry is appended. A report whose entry the log holds
    already is read against the log as it stood before that entry; report_text, where given, is read in place of the
    file; compared, where the entry's appending ran the design script's kept comparison, gives the designs it listed,
    each of which a self-review's differential test then covers."""
    full = log_entries(design_text)
    own = next((i for i, (k, m, _) in enumerate(full) if k == kind and m == n), None)
    entries = full[:len(full) if own is None else own]
    path = report_file(design, kind, n)
    rep = read_report(read(path) if report_text is None else report_text)
    ctx = report_context(root, design, design_text, kind, n, entries)
    ctx["logged"], ctx["compared"] = own is not None, compared
    taken_up = ctx["taken_up"] = cold_lines(rep, kind)
    # a report the log holds already, settled before each field none of its Settlements holds: one holding no Order
    # read as it stands and refused for neither its assessment nor its order, and one holding no Required By refused for
    # neither indicator
    ctx["settled_before_orders"] = own is not None and not any("Order" in s for s in rep["settlements"])
    ctx["settled_before_indicators"] = own is not None and not any("Required By" in s for s in rep["settlements"])
    # and one holding no Departure Reason refused for no departure
    ctx["settled_before_departures"] = own is not None and not any(DEPARTURE_REASON in s for s in rep["settlements"])
    problems = form_problems(rep, ctx, report_types(root), report_parts(root))
    if rep["in_form"]:
        named = named_reports(design, entries, root)
        problems += layout_problems(rep, root, taken_up) + places_problems(rep, report_types(root), taken_up)
        problems += settled_problems(rep, ctx) + key_problems(rep, ctx, named) + search_problems(rep, ctx)
        problems += reads_assessed_problems(rep, ctx) + anchor_problems(rep, ctx) + cover_problems(rep, ctx)
        if not ctx["settled_before_orders"]:
            problems += order_problems(rep, ctx, named)
        if not ctx["settled_before_indicators"]:
            problems += justified_problems(rep, ctx)
        if not ctx["settled_before_departures"]:
            problems += departure_problems(rep, ctx)
        # the checks run only as an entry is appended: a cold agent's parts against their fingerprints, and the
        # coverage of the binding research where the entry is the one it sits at
        if own is None:
            if kind in REVIEWS + (JUDGMENT,):
                problems += cold_parts_problems(rep, kind)
            if coverage_due(design, kind, entries):
                problems += union_coverage_problems(root, design, design_text, entries, ctx)
                problems += goals_searched_problems(root, design, design_text, entries)
    return [(rule, "%s: %s" % (ctx["report_rel"], msg)) for rule, msg in problems], rep


# the script checks of research the design script carries out, by the rules naming them
CAUSE_RULE = WF + " § A Check's Report § Script Checks [Name: area-reassessments-name-their-cause]"
RESEARCH_COVERS_RULE = WF + " § A Check's Report § Script Checks [Name: research-covers-its-matches]"
# @canon-spec specs/methodology/working-files/main.md § A Check's Report § Read Assessment
# the field a Read Assessment names the cause of assessing an area again in
ASSESSED_AGAIN_FOR = "Assessed Again For"


def earlier_paths(rep):
    """-> the paths of the reports a report's Settlement lists in its Earlier Reports."""
    value = next((record_types.value_of(f) for f in rep["blocks"].get("Settlement", []) if f["key"] == "Earlier Reports"), "")
    return {p[0] for p in place_list(value)}


def research_indexes(design, entries, among):
    """-> the indexes among `among` of the `handed-off-judgment` entries whose reports hold Read Assessments, research."""
    return [i for i in among if entries[i][0] == JUDGMENT
            and load_report(design, entries[i][0], entries[i][1])["records"]["Read Assessments"]]


# @canon-spec specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: area-reassessments-name-their-cause]
def cause_problems(rep, ctx, design, entries, named):
    """-> [(rule, message)]: in a research report as its cold agent hands it back and as the builder takes it up, each
    Read Assessment assessing again an Area a binding research report the log holds already assesses, holding no
    Assessed Again For, or naming a cause that earlier report could have weighed: a set counts where its steer entry
    stands after the earlier report's entry or its version is past the version the earlier report read, and a finding
    where it is of a report the earlier report's Earlier Reports does not name, read from the report it names, one a
    check's entry of the current major version names or one standing in the design's folder that no entry names yet,
    the round being settled, the report's own Earlier Reports being the builder's part and not yet written. Two reports
    overlap on the same Area alone. The Read Assessments are a cold agent's, so no check after the take-up asks this."""
    if ctx["kind"] != JUDGMENT or not rep["records"]["Read Assessments"]:
        return []
    root, by_area = ctx["root"], {}
    for i in research_indexes(design, entries, binding(entries, design)):
        k, n, _ = entries[i]
        erep = load_report(design, k, n)
        for a in erep["records"]["Read Assessments"]:
            p = place_of(a.get("Area", ""))
            if p:
                by_area.setdefault(place_key(p), []).append((i, rel_to(report_file(design, k, n), root), erep))
    out = []

    def why_not(cause, i, epath, erep):
        steer = re.fullmatch(r"steer-(\d+)", cause)
        if steer:
            j = next((x for x, e in enumerate(entries) if e[0] == "steer" and e[1] == int(steer.group(1))), None)
            if j is None:
                return "names %s, a set's entry the design's log does not hold" % cause
            read_at = report_version(erep) or entry_version(entries[i])
            if j > i or entry_version(entries[j]) > read_at:
                return None
            return ("names %s, a set %s could have weighed: its entry stands before that report's, and its version is not "
                    "past the version that report read" % (cause, epath))
        place = place_of("`%s`" % cause.strip("`"))
        if not place or place[1] != "Findings" or not (place[2] or "").startswith("Finding: "):
            return "names %s, neither a set's steer entry nor a finding cited as a place" % cause
        fpath, key = place[0], place[2][len("Finding: "):]
        source = named.get(fpath)
        if source is None and fpath.startswith(ctx["folder"]) and (Path(root) / fpath).is_file():
            source = read_report(read(Path(root) / fpath))
        if source is None:
            return ("names a finding of %s, a report no check's entry of the design's current major version names and "
                    "none standing in the design's folder" % fpath)
        if key not in {f.get("Finding") for f in source["records"]["Findings"]}:
            return "names Finding %s, which %s does not hold" % (key, fpath)
        if fpath == epath or fpath in earlier_paths(erep):
            return "names a finding of %s, which %s could have weighed, its Earlier Reports naming it" % (fpath, epath)
        return None

    for a in rep["records"]["Read Assessments"]:
        p = place_of(a.get("Area", ""))
        earlier = by_area.get(place_key(p), []) if p else []
        if not earlier:
            continue
        where = "Read Assessment %s" % cite(p)
        cause = a.get(ASSESSED_AGAIN_FOR, "").strip().strip("`")
        if not cause:
            out.append((CAUSE_RULE, "%s assesses again an Area %s already assess%s, and names no cause in its %s"
                        % (where, ", ".join(e[1] for e in earlier), "es" if len(earlier) == 1 else "", ASSESSED_AGAIN_FOR)))
            continue
        out += [(CAUSE_RULE, "%s %s" % (where, why)) for why in dict.fromkeys(
            why_not(cause, i, epath, erep) for i, epath, erep in earlier) if why]
    return out


# @canon-spec specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: research-covers-its-matches]
def coverage_due(design, kind, entries):
    """Whether the entry of a check of this kind, appended after these, sits where the binding research is read
    together: the builder's first check after research is taken in, other than a handed-off judgment's, a round whose
    settling took research in after the plan's last approval among them."""
    checks = {k for k, fs in log_type()[2].items() if "Model" in fs}
    if kind == JUDGMENT or kind not in checks:
        return False
    research = research_indexes(design, entries, binding(entries, design))
    last_other = max((i for i, e in enumerate(entries) if e[0] in checks and e[0] != JUDGMENT), default=-1)
    return bool(research) and research[-1] > last_other


# @canon-spec specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: research-covers-its-matches]
def union_coverage_problems(root, design, design_text, entries, ctx=None, among=None):
    """-> [(rule, message)]: each place a Search of any of the design's binding research reports gives or holds, lying
    within no Read Assessment's Area of any of them. A Search of the durable files giving every place is run as it was
    asked, over the files its Target asks of and within the paths it was narrowed to, and is not held to its own
    Places; a Search by meaning is not run, and each place its record holds is read; a research's Search of the working
    files is read at no moment but the check of its own report; and a Search the search refuses gives no place and is
    passed over. A Search logged holding a Pattern is read as it was, its Pattern run over its ground and each match
    outside the design document read. among, where given, the indexes of the research entries read, else every binding
    research report."""
    idx = research_indexes(design, entries, binding(entries, design)) if among is None else among
    reports = [(rel_to(report_file(design, entries[i][0], entries[i][1]), root),
                load_report(design, entries[i][0], entries[i][1])) for i in idx]
    if not reports:
        return []
    if ctx is None:
        fields = dict(read_design(design)[1])
        kept = [] if over_applied(entries) else kept_changes(root, design_text)
        ctx = {"ground": search_ground(root, rel_to(design, root), design_text,
                                       re.findall(r"`([^`]+)`", fields.get("Target", "")), kept),
               "kept": bool(kept), "root": root,
               "steps": step_lines(design_text), "design_rel": rel_to(design, root)}
    areas = [p for _, rep in reports for a in rep["records"]["Read Assessments"] for p in [place_of(a.get("Area", ""))] if p]
    out, seen = [], set()
    for path, rep in reports:
        for s in rep["records"]["Searches"]:
            if logged_form(s):
                matched = search_matches(s, ctx)
                gave, verb = [] if isinstance(matched, re.error) else matched, "matches in"
            elif unquoted(s.get("Kind", "")) == MEANING:
                gave, verb = place_list(s.get("Places", "")), "holds"
            elif search_target(s)[0] == WORKING_FILES_TARGET:
                continue
            else:
                places, _, why, refused = run_search(s, ctx)
                if why and not refused:
                    out.append((RESEARCH_COVERS_RULE, "Search %s of %s cannot be run: %s" % (s.get("Search", ""), path, why)))
                gave, verb = places or [], "gives"
            for p in gave:
                if p[0] == ctx["design_rel"] or covered(areas, p) or place_key(p) in seen:
                    continue
                seen.add(place_key(p))
                out.append((RESEARCH_COVERS_RULE, "Search %s of %s %s %s, which no binding research report's "
                            "Read Assessment's Area covers" % (s.get("Search", ""), path, verb, cite(p))))
    return out


GOALS_SEARCHED_RULE = WF + " § A Check's Report § Script Checks [Name: goals-searched-over-every-durable-file]"
# the kinds of search that between them read the whole of what a file holds, and what each reads
COVERING_KINDS = ((MEANING, "by meaning"), ("terms", "by terms"))


# @canon-spec specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: goals-searched-over-every-durable-file]
def covering_files(root):
    """-> the durable files a design's research is asked to have searched: those the last commit holds, or those
    standing where the project is under no version control or holds no commit yet. No search is run and no index
    opened."""
    import search as searching
    return searching.durable_files(root, committed=last_commit(root) is not None)


# @canon-spec specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: goals-searched-over-every-durable-file]
def goals_searched_problems(root, design, design_text, entries, among=None, files=None):
    """-> [(rule, message)]: among the research binding a design, read together, each goal the design holds named by
    no Search by meaning of the durable files naming no commit, or by none by terms, and each goal whose Searches of
    one of those kinds were narrowed to paths that together leave a durable file out, naming the goal, the kind of
    search and the files. A Search narrowed to no path covers every file. A Search of the working files, one of a
    commit by name, one of any other Kind and one logged before a Search held a Kind count for nothing. The check runs
    no search: it reads the paths each Search was narrowed to against the durable files the last commit holds, so a
    file an apply has written and not committed is not asked for. among, where given, the indexes of the research
    entries read, else every binding research report; files, given by a test, the durable files asked of."""
    idx = research_indexes(design, entries, binding(entries, design)) if among is None else among
    reports = [load_report(design, entries[i][0], entries[i][1]) for i in idx]
    if not reports:
        return []
    asked = {}
    for rep in reports:
        for s in rep["records"]["Searches"]:
            kind = unquoted(s.get("Kind", ""))
            target, commit, narrowed = search_target(s)
            if logged_form(s) or kind not in dict(COVERING_KINDS) or target not in (CURRENT_FILES, COMMITTED_FILES) or commit:
                continue
            for goal in names_of_text(s.get("Goals", "")):
                asked.setdefault((goal, kind), []).append([n.rstrip("/") for n in narrowed])
    out, held = [], None
    for goal in read_plan(design_text)["goals"]:
        for kind, how in COVERING_KINDS:
            narrowings = asked.get((goal, kind))
            if not narrowings:
                out.append((GOALS_SEARCHED_RULE, "the goal %s is named by no Search %s of the durable files naming no commit, among "
                            "the research binding the design" % (goal, how)))
                continue
            if any(not n for n in narrowings):
                continue
            if held is None:
                try:
                    held = covering_files(root) if files is None else list(files)
                except Exception as exc:  # the search's own account of why the committed files cannot be listed
                    return out + [(GOALS_SEARCHED_RULE, "the durable files the last commit holds cannot be listed: %s" % exc)]
            paths = [n for narrowed in narrowings for n in narrowed]
            left = [f for f in held if not any(f == n or f.startswith(n + "/") for n in paths)]
            if left:
                out.append((GOALS_SEARCHED_RULE, "the Searches %s naming the goal %s were narrowed to paths that together leave out %s%s"
                            % (how, goal, ", ".join("`%s`" % f for f in left[:5]),
                               ", and %d more durable file%s" % (len(left) - 5, "" if len(left) == 6 else "s") if len(left) > 5 else "")))
    return out


# @canon-spec specs/methodology/skills/authoring-a-skill.md § Authoring a Skill
# where a script's kept tests stand, outside Spec of Record's scope; what a file there is named for, the script it is
# of and then its kind, a set of kept tests or a kept comparison; and the two names by which each says which files are
# its script's, its code and each file of the canon it reads a form from as it runs
KEPT = "tests/spec-of-record/scripts"
KEPT_TESTS, KEPT_COMPARISON = "-tests.py", "-comparison.py"
KEPT_FILES = ("SCRIPT_FILES", "FORM_FILES")
KEPT_TESTS_RULE = "specs/methodology/skills/authoring-a-skill.md § Authoring a Skill § Script Checks [Name: kept-tests-pass-at-the-self-review]"
# the lines of a run's output written into a report where it prints more: each line reporting a failure, and its last
KEPT_OUTPUT, KEPT_FAILURE = 40, "FAIL"
# a line of the comparison's output naming a design the two sides read differently
COMPARED = re.compile(r"^design (\S+)$", re.M)


# @canon-spec specs/methodology/skills/authoring-a-skill.md § Authoring a Skill
def kept_scripts(root):
    """-> [(a kept file's path from the root, the script it is named for, whether it is a comparison, the files it says
    are its script's or None, why it cannot be read or None)] for each set of kept tests and each kept comparison
    standing under KEPT, read from the file's text and never run: the two names of KEPT_FILES, each a tuple of paths
    written out at the file's top level."""
    import ast
    out, folder = [], Path(root) / KEPT
    for path in sorted(folder.glob("*.py")) if folder.is_dir() else []:
        ending = next((e for e in (KEPT_TESTS, KEPT_COMPARISON) if path.name.endswith(e)), None)
        if ending is None:
            continue
        rel, named = rel_to(path, root), {}
        try:
            for node in ast.parse(read(path)).body:
                if isinstance(node, ast.Assign) and len(node.targets) == 1 and getattr(node.targets[0], "id", None) in KEPT_FILES:
                    named[node.targets[0].id] = ast.literal_eval(node.value)
        except (SyntaxError, ValueError) as exc:
            out.append((rel, path.name[:-len(ending)], ending == KEPT_COMPARISON, None, "it cannot be read: %s" % exc))
            continue
        wrong = [k for k in KEPT_FILES if not isinstance(named.get(k), (tuple, list)) or not all(isinstance(p, str) for p in named[k])]
        files = None if wrong else tuple(p for k in KEPT_FILES for p in named[k])
        out.append((rel, path.name[:-len(ending)], ending == KEPT_COMPARISON, files,
                    "it names no %s as a tuple of paths at its top level" % " and no ".join(wrong) if wrong else None))
    return out


def kept_file_holds(files, path):
    """Whether a path is among the files a kept file names: one it names, or one beneath a folder it names, a path
    ending in a slash."""
    return any(path == f or (f.endswith("/") and path.startswith(f)) for f in files)


# @canon-spec specs/methodology/skills/authoring-a-skill.md § Authoring a Skill § Script Checks [Name: kept-tests-pass-at-the-self-review]
def kept_tests_run(root, changed):
    """Runs the kept tests of each script whose files a set of changed files holds, a script's files being its code
    and each file of the canon it reads a form from as it runs, as its kept tests name them, and each kept comparison
    whose script's files they hold -> (what each run gave, as text; [(rule, message)] for each test that fails and
    each kept file that cannot be run; the designs a comparison lists as read differently, each a path, or None where
    none was run). Which kept files the changed files call for is worked out first. Those are then run at once, each
    alone in a process of its own, by this Python, from the checkout's root, and all are waited for: the kept files
    share no working space, each keeping to folders of its own, so none waits on another. A kept file passes where it
    exits 0. What each gave is written in the order kept_scripts gives the kept files, whichever ended first, so the
    text reads the same from run to run. A comparison's listing is no failure: the builder judges each design it
    lists. A changed script no kept file names is said to hold no kept tests, and refuses nothing. A comparison of a
    script holding no set of kept tests is run, and reported as a script whose kept tests cannot be run, since a
    comparison stands beside its script's tests."""
    import code_checks
    import concurrent.futures
    kept, changed = kept_scripts(root), sorted(changed)
    lines, problems, listed = [], [(KEPT_TESTS_RULE, "%s cannot be run: %s" % (rel, why)) for rel, _, _, _, why in kept if why], None
    tested = {script: files for _, script, comparison, files, why in kept if not comparison and not why}
    # the kept files the changed files call for, in the order kept_scripts gives them, each with the changed files it
    # is run for
    called = [(rel, script, comparison, files, [p for p in changed if kept_file_holds(files, p)])
              for rel, script, comparison, files, _ in kept if files is not None]
    called = [c for c in called if c[4]]

    def run(rel):
        return subprocess.run([sys.executable, str(Path(root) / rel)], cwd=root, capture_output=True,
                              env=dict(os.environ, PYTHONIOENCODING="utf-8", PYTHONDONTWRITEBYTECODE="1"))
    with concurrent.futures.ThreadPoolExecutor(max_workers=max(1, len(called))) as at_once:
        ran_all = list(at_once.map(run, [rel for rel, _, _, _, _ in called]))
    for (rel, script, comparison, files, held), ran in zip(called, ran_all):
        if comparison and script not in tested:
            problems.append((KEPT_TESTS_RULE, "%s is the comparison of a script holding no set of kept tests, %s/%s%s, so "
                                              "that script's kept tests cannot be run" % (rel, KEPT, script, KEPT_TESTS)))
        elif comparison and set(tested[script]) != set(files):
            problems.append((KEPT_TESTS_RULE, "%s and %s/%s%s name different files as their script's, so which changes run "
                                              "them cannot be told" % (rel, KEPT, script, KEPT_TESTS)))
        gave = (ran.stdout + ran.stderr).decode("utf-8", "replace").replace("\r\n", "\n").rstrip("\n").split("\n")
        if not comparison and len(gave) > KEPT_OUTPUT:
            gave = [l for l in gave[:-1] if KEPT_FAILURE in l] + gave[-1:]
        lines += ["$ python %s" % rel, "run for %s" % ", ".join(held)] + gave + ["exit %d" % ran.returncode, ""]
        if comparison and ran.returncode == 0:
            listed = (listed or []) + COMPARED.findall("\n".join(gave))
        elif ran.returncode:
            problems.append((KEPT_TESTS_RULE, "%s %s, exit %d" % (rel, "could not be made" if comparison else "holds a test that fails, or "
                                                                    "could not be run", ran.returncode)))
    skills, code = skill_dirs(root), code_checks.code_roots(root) or ([], [])
    named = [files for _, _, _, files, _ in kept if files is not None]
    untested = [p for p in changed if p.endswith(SCRIPTS) and not p.startswith("tests/") and file_kind(p, skills, code) not in (None, "code")
                and not any(kept_file_holds(files, p) for files in named)]
    lines += ["no set of kept tests names %s" % p for p in untested]
    if not lines:
        lines = ["no changed file is a file of a script holding kept tests"]
    return "\n".join(lines).rstrip("\n") + "\n", problems, listed


def check_kept_tests(value):
    """--check-kept-tests [FILE ...]: the kept tests of each script whose files the changed files given hold, and each
    kept comparison whose script's files they hold, run, with what each gave; given no file, the files the checkout
    holds changed against the last commit, the working files aside. It names no design, so a direct edit outside a
    design runs it; -> 1 where a test fails or a kept file cannot be run, else 0, whatever a comparison lists."""
    root = repo_root()
    changed = {rel_to(v, root) for v in value} if value else {p for p in uncommitted_changes(root) if not is_working_file(p)}
    output, problems, _ = kept_tests_run(root, changed)
    print("== check-kept-tests, over %d changed file%s\n%s" % (len(changed), "" if len(changed) == 1 else "s", output))
    for rule, problem in problems:
        print("%s\n  %s" % (rule, problem))
    print("%d problem%s\n" % (len(problems), "" if len(problems) == 1 else "s"))
    return 1 if problems else 0


def self_review_output(root, design, design_text):
    """-> the output of the design script's checks the self-review runs for its phase: before the apply,
    --check-cited-headings, --check-target-kind, and --show-reach where it records Retired Phrases; at the apply, --check-constructs on each file of the Target holding a
    construct the diff changed, --check-work, --check-retired-wording and --check-changed-files. The kept tests are no
    part of it: kept_tests_run runs them as the entry is appended alone."""
    value = str(design)
    if not over_applied(log_entries(design_text)):
        runs = [("--check-cited-headings", check_cited_headings, value), ("--check-target-kind", check_target_kind, value)]
        if retired_phrases(design_text):
            runs.append(("--show-reach", show_reach, value))
    else:
        commit = last_commit(root)
        changes = work_changes(root, commit)[0] if commit else {}
        target = set(re.findall(r"`([^`]+)`", dict(read_design(design)[1]).get("Target", "")))
        created = created_paths()
        text_of = spec_texts(root)
        runs = [("--check-constructs", check_constructs, str(root / p)) for p in sorted(changes)
                if within_target(p, target, created) and p in text_of and constructs_in(p, text_of[p], changes[p])]
        runs += [("--check-work", check_work, value), ("--check-retired-wording", check_retired_wording, value),
                 ("--check-changed-files", check_changed_files, value)]
    out = io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(out):
        for flag, run, arg in runs:
            print("$ %s %s" % (flag, rel_to(arg, root)))
            print("exit %d\n" % run(arg))
    return out.getvalue()


def write_script_output(path, output):
    """Write a self-review's Script Output part into its report, replacing any it holds, where the form orders it."""
    raw = path.read_bytes().decode("utf-8")
    text = with_script_output(raw, output)
    path.write_bytes((text.replace("\n", "\r\n") if "\r\n" in raw else text).encode("utf-8"))


def with_script_output(raw, output):
    """-> a self-review's report text with its Script Output part replaced by output, or added where the form orders
    it."""
    lines = raw.replace("\r\n", "\n").rstrip("\n").split("\n")
    fence = "````" if "```" in output else "```"
    part = ["## Script Output", "", fence + "text"] + output.rstrip("\n").split("\n") + [fence]
    secs = sections("\n".join(lines))
    order = [p for p, _, _, _ in report_parts(repo_root())]
    if "Script Output" in secs:
        h, end = secs["Script Output"]
        lines = lines[:h] + part + [""] + lines[end:]
    else:
        later = order[order.index("Script Output") + 1:] if "Script Output" in order else []
        at = min((secs[p][0] for p in later if p in secs), default=None)
        lines = lines + [""] + part if at is None else lines[:at] + part + [""] + lines[at:]
    return re.sub(r"\n{3,}", "\n\n", "\n".join(lines).rstrip("\n") + "\n")


def report_of(value):
    """-> (design, kind, count) of a report at its path in a design's folder,
    `.ai/tmp/<skill-name>/<design>/reports/<kind>/{n}.md`, its design `.ai/plans/<skill-name>/<design>.md`; or None."""
    path = Path(value).resolve()
    if len(path.parents) < 6 or not path.stem.isdigit() or path.parents[1].name != "reports" or path.parents[4].name != "tmp":
        return None
    design = path.parents[5] / "plans" / path.parents[3].name / (path.parents[2].name + ".md")
    return (design, path.parent.name, int(path.stem)) if design.is_file() else None


# @canon-spec specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: area-reassessments-name-their-cause]
# @canon-spec specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: findings-anchored-in-the-design]
# @canon-spec specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: places-in-their-form]
# @canon-spec specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: reads-assessed]
# @canon-spec specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: report-in-its-form]
# @canon-spec specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: report-keys-name-records]
# @canon-spec specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: report-laid-out]
# @canon-spec specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: searches-cover-their-matches]
def check_handed_back(value):
    """--check-handed-back REPORT: a review's report, before its settlement, or a handed-off judgment's, before the builder
    takes it in, the cold agent's part held to its form, its Searches run again, each place it read assessed where it
    holds Read Assessments, each marked Finding anchored in the design, each key it cites, a Finding's Lands On among
    them, naming a record a report of the design's current major version holds; writes no file; -> 1 where it reports, 0 where
    it reports nothing, 2 for a usage error."""
    root = repo_root()
    found = report_of(value) if Path(value).is_file() else None
    if found is None or found[1] not in REVIEWS + (JUDGMENT,):
        sys.stderr.write("--check-handed-back takes a review's or a handed-off judgment's report at its path in a design's "
                         "folder, .ai/tmp/<skill-name>/<design>/reports/<kind>/{n}.md: %s\n" % value)
        return 2
    design, kind, n = found
    design_text = read(design).replace("\r\n", "\n")
    rep = read_report(read(Path(value)))
    ctx = report_context(root, design, design_text, kind, n, log_entries(design_text), reviewer=True)
    return report("check-handed-back " + rel_to(value, root), handed_back_problems(root, design, kind, n, value, moment=HANDED_BACK))


def handed_back_problems(root, design, kind, n, value, moment=TAKEN_UP):
    """-> [(rule, message)]: a review's or a handed-off judgment's report as its cold agent hands it back, its parts held
    to their form, its Searches run, and no part held that the builder or the design script writes. moment says which
    reading it is: as the cold agent hands the report back, which alone asks of a research's Search what turns on the
    checkout, or as the builder takes it up. These are the two readings of a cold agent's parts: no check after the
    take-up makes this one again."""
    design_text = read(design).replace("\r\n", "\n")
    rep = read_report(read(Path(value)))
    ctx = report_context(root, design, design_text, kind, n, log_entries(design_text), reviewer=True)
    problems = form_problems(rep, ctx, report_types(root), report_parts(root))
    if rep["in_form"]:
        problems += layout_problems(rep, root) + places_problems(rep, report_types(root)) + search_problems(rep, ctx, moment)
        named = named_reports(design, ctx["entries"], root)
        problems += reads_assessed_problems(rep, ctx) + anchor_problems(rep, ctx)
        problems += key_problems(rep, ctx, named, handed_back=True)
        problems += cause_problems(rep, ctx, design, ctx["entries"], named)
        problems += [(COLD_PARTS_KEPT, "a part its cold agent does not write, the builder's or the design script's: " + p)
                     for p, _ in rep["parts"] if p in BUILDER_PARTS]
    return problems


# @canon-spec specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: cold-parts-kept]
COLD_PARTS_KEPT = WF + " § A Check's Report § Script Checks [Name: cold-parts-kept]"


def part_texts(text):
    """-> {part: [its lines, trailing blank lines dropped]} of a report: its Title, the lines from its title to its first
    part's heading, and each part, its heading among its lines."""
    lines = text.replace("\r\n", "\n").split("\n")
    heads = sorted((h, lineage) for lineage, (h, _) in sections(text).items() if " § " not in lineage)
    out = {}
    bounds = [(0, "Title")] + [(h, p) for h, p in heads]
    for k, (h, p) in enumerate(bounds):
        end = bounds[k + 1][0] if k + 1 < len(bounds) else len(lines)
        part = [l.rstrip() for l in lines[h:end]]
        while part and not part[-1]:
            part.pop()
        out[p] = part
    return out


def fingerprint(lines):
    """-> the SHA-256 of lines joined by line feeds, as UTF-8."""
    return hashlib.sha256("\n".join(lines).encode("utf-8")).hexdigest()


def hand_back_part(text, kind):
    """-> the Hand-back part's lines for a report as its cold agent handed it back: a fingerprint of each part it wrote,
    in the report's order, a review's Searches with the count of the lines it covers."""
    out = ["## " + HAND_BACK, ""]
    for p, lines in part_texts(text).items():
        if p not in REVIEWER_PARTS:
            continue
        if p == "Searches" and kind in REVIEWS:
            out.append("- %s: %s, %d lines" % (p, fingerprint(lines), len(lines)))
        else:
            out.append("- %s: %s" % (p, fingerprint(lines)))
    return out


def fingerprinted(texts):
    """-> {part: the count of its lines its fingerprint covers, or None where it covers the part whole} for each part a
    report's Hand-back holds a fingerprint of; texts as part_texts gives a report's parts."""
    found = (FINGERPRINT.match(line.strip()) for line in texts.get(HAND_BACK, [])[1:])
    return {m["part"]: int(m["n"]) if m["n"] else None for m in found if m}


# @canon-spec specs/methodology/working-files/main.md § A Check's Report § Who Writes Each Part
def cold_lines(rep, kind):
    """-> the 0-based lines of a review's or a handed-off judgment's report that its cold agent wrote, which each check
    made after the take-up passes over: each part its Hand-back holds a fingerprint of, from its heading to the next
    part's, the Title from the report's first line, and a review's Searches over the lines its fingerprint covers
    alone, so the builder's own Searches after them are held. A report holding no Hand-back, one logged before the
    part or one not yet taken up, which cold_parts_problems refuses, gives each part a cold agent writes. A report the
    builder writes alone gives no line."""
    if kind not in REVIEWS + (JUDGMENT,) or not rep["in_form"]:
        return frozenset()
    texts = part_texts(rep["text"])
    counts = fingerprinted(texts) if HAND_BACK in texts else dict.fromkeys(texts)
    starts = sorted([(0, "Title")] + [(h, p) for p, h in rep["parts"]])
    out = set()
    for k, (h, part) in enumerate(starts):
        if part in REVIEWER_PARTS and part in counts:
            end = starts[k + 1][0] if k + 1 < len(starts) else len(rep["lines"])
            out |= set(range(h, end if counts[part] is None else min(end, h + counts[part])))
    return frozenset(out)


def unmatched_cold_parts(texts):
    """-> [(rule, message)]: each part of a report taken up that no longer matches the fingerprint its Hand-back holds
    of it, changed or removed since the take-up, a review's Searches matched over the lines its fingerprint covers, so
    the builder's own Searches after them aside; texts as part_texts gives a report's parts."""
    out = []
    for line in texts.get(HAND_BACK, [])[1:]:
        m = FINGERPRINT.match(line.strip())
        now = texts.get(m["part"]) if m else None
        if m and now is None:
            out.append((COLD_PARTS_KEPT, "the %s part its cold agent handed back is removed" % m["part"]))
        elif m and fingerprint(now[:int(m["n"])] if m["n"] else now) != m["sha"]:
            out.append((COLD_PARTS_KEPT, "the %s part no longer holds what its cold agent handed back" % m["part"]))
    return out


def cold_parts_problems(rep, kind):
    """-> [(rule, message)]: a report a cold agent wrote, taken up by the builder: a Hand-back holding a fingerprint of
    each part the cold agent wrote, each part still matching it, as unmatched_cold_parts reads them, and no part the
    cold agent writes added after the take-up."""
    texts = part_texts(rep["text"])
    if HAND_BACK not in texts:
        return [(COLD_PARTS_KEPT, "it holds no Hand-back part: a report a cold agent wrote is taken up by "
                                  "--take-up-report before the builder writes its parts")]
    lines = [line.strip() for line in texts[HAND_BACK][1:] if line.strip()]
    held = {m["part"] for m in map(FINGERPRINT.match, lines) if m}
    out = [(COLD_PARTS_KEPT, "a Hand-back line that is no part's fingerprint: " + line) for line in lines if not FINGERPRINT.match(line)]
    out += unmatched_cold_parts(texts)
    for p in texts:
        if p in REVIEWER_PARTS and p not in held:
            out.append((COLD_PARTS_KEPT, "a part its cold agent writes, added after the builder took the report up: " + p))
    return out


# @canon-spec specs/methodology/working-files/main.md § A Check's Report § Who Writes Each Part § The Report's Workflow
def cleared_report(text, kind):
    """-> a report's text holding the parts its cold agent wrote alone, every part the builder and the take-up wrote
    cleared: its Hand-back, its Script Output, its Causes, its Settlement, and the builder's Searches after a review's."""
    texts, lines = part_texts(text), []
    counts = fingerprinted(texts)
    for p, held in texts.items():
        if p in REVIEWER_PARTS:
            lines += held[:counts.get(p)] + [""]
    return "\n".join(lines).rstrip("\n") + "\n"


# @canon-spec specs/methodology/working-files/main.md § A Check's Report § Who Writes Each Part § The Report's Workflow
def returned_report(root, design, kind, n, path):
    """-> [(rule, message)] where a part the cold agent wrote of a review's or a handed-off judgment's report taken up
    no longer matches the fingerprint the take-up wrote of it, changed or removed since, the report then written back
    cleared of every part the builder and the take-up wrote, so it goes back to its cold agent; [] where each such part
    matches, the report left as it stands, with the builder, whatever a check refuses it for. It reads the report
    alone, and runs no Search and no check of the hand-back again, so nothing the files have come to hold since the
    take-up returns a report. A report whose entry the log holds already is never returned, since the return comes
    before its entry is appended."""
    if kind not in REVIEWS + (JUDGMENT,) or not path.is_file():
        return []
    if any(k == kind and m == n for k, m, _ in log_entries(read(design).replace("\r\n", "\n"))):
        return []
    text = read(path).replace("\r\n", "\n")
    refused = unmatched_cold_parts(part_texts(text))
    if not refused:
        return []
    path.write_text(cleared_report(text, kind), encoding="utf-8")
    return refused + [(REPORT_WORKFLOW, "%s goes back to its cold agent, every part the builder and the take-up wrote "
                                        "cleared: the cold agent puts the refused part right and hands it back" % rel_to(path, root))]


REPORT_WORKFLOW = WF + " § A Check's Report § Who Writes Each Part § The Report's Workflow"


# @canon-spec specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: cold-parts-kept]
def take_up_report(value):
    """--take-up-report REPORT: the builder takes up a review's or a handed-off judgment's report its cold agent handed
    back: the hand-back check run again and, where it passes, the report's Hand-back part written, a fingerprint of each
    part the cold agent wrote; -> 1 where it reports, writing nothing, 0 where it writes the part, 2 for a usage error."""
    root = repo_root()
    found = report_of(value) if Path(value).is_file() else None
    if found is None or found[1] not in REVIEWS + (JUDGMENT,):
        sys.stderr.write("--take-up-report takes a review's or a handed-off judgment's report at its path in a design's "
                         "folder, .ai/tmp/<skill-name>/<design>/reports/<kind>/{n}.md: %s\n" % value)
        return 2
    design, kind, n = found
    problems = handed_back_problems(root, design, kind, n, value)
    if problems:
        return report("take-up-report, not taken up " + rel_to(value, root), problems)
    text = read(Path(value)).replace("\r\n", "\n").rstrip("\n")
    Path(value).write_text(text + "\n\n" + "\n".join(hand_back_part(text, kind)) + "\n", encoding="utf-8")
    return report("take-up-report " + rel_to(value, root), [])


def check_settled_report(value):
    """--check-settled-report REPORT: a check's report at its path in a design's folder, once settled, held to every
    check --log-entry holds it to as it logs the check's entry, a self-review's not yet logged read with the Script
    Output --log-entry would write into it; writes no file; -> 1
    where it reports, 0 where it reports nothing, 2 for a usage error."""
    root = repo_root()
    found = report_of(value) if Path(value).is_file() else None
    kinds = log_type()[2]
    if found is None or "Model" not in kinds.get(found[1], ()):
        sys.stderr.write("--check-settled-report takes a check's report at its path in a design's folder, "
                         ".ai/tmp/<skill-name>/<design>/reports/<kind>/{n}.md: %s\n" % value)
        return 2
    design, kind, n = found
    text = read(design).replace("\r\n", "\n")
    # a self-review's report read with the Script Output --log-entry would write into it, unless the log holds its entry
    logged = any(k == kind and m == n for k, m, _ in log_entries(text))
    held = with_script_output(read(Path(value)), self_review_output(root, design, text)) \
        if kind == "self-review" and not logged else None
    problems, _ = entry_report_problems(root, design, text, kind, n, held)
    if problems:
        problems = returned_report(root, design, kind, n, Path(value)) or problems
    return report("check-settled-report " + rel_to(value, root), problems)


def retired_phrases(text):
    """-> each of a design's retired phrases as (phrase, replacement, [(path, section or None)] it stays right in)."""
    out = []
    for record in records(section(text, RETIRED)) or []:
        f = dict((k, v.strip()) for k, v in record)
        stays = "" if f.get("Stays Right", "none").lower() == "none" else f["Stays Right"]
        out.append((f.get("Phrase", ""), f.get("Replacement", ""), places(stays)))
    return out


# @canon-spec specs/methodology/working-files/main.md § Design Log Entry
# @canon-spec specs/methodology/working-files/main.md § Retired Phrase
def places(value):
    """-> [(path, section or None)] for a Places or a Stays Right value: places separated by semicolons, each a path,
    its section after it, written as `path` § Section, as the citation `path § Section`, or bare."""
    out = []
    for p in value.split(";"):
        p = p.strip().replace("`", "")
        if p:
            path, _, sect = p.partition("§")
            out.append((path.strip(), sect.strip() or None))
    return out


# @canon-spec specs/methodology/working-files/main.md § Retired Phrase
def phrase_places(root, phrases, committed=False):
    """-> [(path, line number, line, phrase, replacement)] for each line of a durable file holding a retired phrase in
    whatever form it takes, a plural and an identifier among them, outside the places it stays right: found by the
    search the skills share as it finds a term, over the durable files as they stand or, committed, as the last
    commit held them. A file outside Spec of Record's scope is no durable file and is not read."""
    import search as searching
    engine = searching.Search(root, quiet=True, target=searching.COMMITTED if committed else searching.CURRENT)
    out, texts = [], {}
    try:
        for phrase, replacement, stays in phrases:
            for place in engine.terms(phrase).places:
                path, lineage = place.path, place.lineage or ""
                if any(p == path and (s is None or lineage == s or lineage.startswith(s + " § ")) for p, s in stays):
                    continue
                if path not in texts:
                    try:
                        data = (engine.tree / path).read_bytes() if committed else (Path(root) / path).read_bytes()
                        texts[path] = data.decode("utf-8", "replace").replace("\r\n", "\n").split("\n")
                    except (OSError, ValueError, KeyError):
                        texts[path] = []
                for n in range(place.first, place.last + 1):
                    line = texts[path][n - 1].strip() if n <= len(texts[path]) else ""
                    if (path, n, phrase) not in {(a, b, c) for a, b, _, c, _ in out}:
                        out.append((path, n, line, phrase, replacement))
    finally:
        engine.db.close()
    return sorted(out)


def scope_files(root):
    """-> the files in Spec of Record's scope, tracked or new, the working files aside."""
    scope = scope_paths(root)
    found = subprocess.run(["git", "ls-files", "--cached", "--others", "--exclude-standard", "--"] + scope,
                           capture_output=True, text=True, encoding="utf-8", cwd=root)
    paths = found.stdout.split("\n") if found.returncode == 0 else \
        [s for s in scope if (root / s).is_file()] + \
        [p.relative_to(root).as_posix() for s in scope if (root / s).is_dir() for p in (root / s).rglob("*") if p.is_file()]
    # the specifications' files as the index walk finds them, so a file no index names is the index check's to report
    walked = {p.relative_to(root).as_posix() for p in indexed(root, "specs")}
    return sorted(p for p in paths if p and not is_working_file(p) and (not p.startswith("specs/") or p in walked))


def git_changes():
    """-> [(status, path)] for each file git reports changed against the last commit, a new untracked one among
    them, a rename's or a copy's new path alone; or None where there is no version control."""
    try:
        found = subprocess.run(["git", "status", "--porcelain=v1", "-uall", "-z"], capture_output=True, text=True, encoding="utf-8")
    except FileNotFoundError:
        return None
    if found.returncode:
        return None
    out, parts = [], found.stdout.split("\0")
    i = 0
    while i < len(parts):
        entry = parts[i]
        if len(entry) > 3:
            out.append((entry[:2], entry[3:]))
            if entry[0] in "RC":
                i += 1  # a rename's or a copy's source follows it
        i += 1
    return out


def created_paths():
    """-> the paths git reports new against the last commit, added or untracked: the files an apply created."""
    return {path for status, path in git_changes() or [] if status == "??" or status[0] == "A"}


# @canon-spec specs/methodology/working-files/main.md § A Design Document
# @canon-spec specs/methodology/working-files/main.md § A Design Document § Applying and Committing
def within_target(path, target, created):
    """-> whether path lies within the Target: a file it names, or a file created under a directory it names, a
    path ending in a slash, `./` naming the project's root, which every path lies under; a file standing under such a
    directory before the apply lies outside it."""
    return path in target or (path in created and any(t.endswith("/") and (t == "./" or path.startswith(t)) for t in target))


def target_files(target, created):
    """-> the files the Target's readers read: each file it names, and each file created under a directory it names."""
    return sorted({t for t in target if not t.endswith("/")} | {p for p in created if within_target(p, target, created)})


# @canon-spec specs/methodology/working-files/main.md § Retired Phrase
def show_reach(value):
    """--show-reach DESIGN: each line of a durable file holding a retired phrase in whatever form it takes, those
    outside the Target marked, found by the search the skills share over the durable files as they stand, and as the
    last commit held them while a design's uncommitted changes are kept; -> 0, and 2 where the search cannot be run."""
    design = design_file(value)
    if design is None:
        return 2
    _, fields, _, text = read_design(design)
    phrases, target = retired_phrases(text), set(re.findall(r"`([^`]+)`", dict(fields).get("Target", "")))
    created, root = created_paths(), repo_root()
    kept = [] if over_applied(log_entries(text)) else kept_changes(root, text)
    try:
        found = phrase_places(root, phrases, committed=bool(kept)) if phrases else []
    except Exception as exc:  # the search's own account of what it requires and lacks
        sys.stderr.write("--show-reach finds a retired phrase by the search the skills share, which cannot be run: %s\n" % exc)
        return 2
    print("== show-reach " + design.stem)
    for path, i, line, phrase, _ in found:
        inside = within_target(path, target, created)
        print("%s:%d%s  [%s]  %s" % (path, i, "" if inside else "  (outside the Target)", phrase, line[:160]))
    print("%d line%s\n" % (len(found), "" if len(found) == 1 else "s"))
    return 0


def check_retired_wording(value):
    """--check-retired-wording DESIGN: each line of the Target's durable files, and of the durable files created under
    a Target directory, holding a retired phrase in whatever form it takes, with its replacement, found by the search
    the skills share over the durable files as they stand; a file of the Target outside Spec of Record's scope is not
    read; -> 1 where any stands, and 2 where the search cannot be run."""
    design = design_file(value)
    if design is None:
        return 2
    _, fields, _, text = read_design(design)
    phrases = retired_phrases(text)
    target = set(re.findall(r"`([^`]+)`", dict(fields).get("Target", "")))
    read_ = set(target_files(target, created_paths()))
    try:
        found = phrase_places(repo_root(), phrases) if phrases else []
    except Exception as exc:  # the search's own account of what it requires and lacks
        sys.stderr.write("--check-retired-wording finds a retired phrase by the search the skills share, which cannot be run: %s\n" % exc)
        return 2
    problems = [(path, "line %d holds %s, retired for %s: %s" % (i, phrase, replacement, line[:160]))
                for path, i, line, phrase, replacement in found if path in read_]
    return report("check-retired-wording " + design.stem, problems)


def logged_places(text, kind):
    """-> the paths a design's log entries of one kind name in their Places."""
    out = set()
    for record in records(section(text, LOG)) or []:
        f = dict(record)
        if f.get("Entry", "").startswith(kind + "-"):
            out |= {path for path, _ in places(f.get("Places", ""))}
    return out


def check_changed_files(value):
    """--check-changed-files DESIGN: each file changed against the last commit, a new untracked one among them,
    outside the working files and the Target, a file created under a Target directory within it, a user's edit or a
    direct edit the log names marked; -> 1 where one stands that no entry names."""
    design = design_file(value)
    if design is None:
        return 2
    _, fields, _, text = read_design(design)
    changes = git_changes()
    if changes is None:
        print("== check-changed-files %s\nno version control, so the files changed cannot be listed\n" % design.stem)
        return 0
    created = {path for status, path in changes if status == "??" or status[0] == "A"}
    target = set(re.findall(r"`([^`]+)`", dict(fields).get("Target", "")))
    users, directs = logged_places(text, "user-edit"), logged_places(text, "direct-edit")
    problems, marked = [], []
    for path in sorted({path for _, path in changes}):
        if is_working_file(path) or within_target(path, target, created):
            continue
        if path in users:
            marked.append((path, "changed outside the Target, the user's edit"))
        elif path in directs:
            marked.append((path, "changed outside the Target, a direct edit"))
        else:
            problems.append((path, "changed outside the Target, and no entry of the log names it"))
    for path, note in marked:
        print("%s\n  %s" % (path, note))
    return report("check-changed-files " + design.stem, problems)


REFACTOR_AND_REFINE_PATHS = ("specs", ".ai/skills")  # the canon's specs and skills, and the application's specs


def refactor_and_refine_lines(text):
    """-> the lines of text a Refactor and Refine cycle carries, blank lines and bare markup set
    aside, and a heading read without its level, since a move raises or lowers it."""
    # a table's separator row, a code fence or a front matter fence carries no text of its own
    text = text.replace("\r\n", "\n")
    found = reading.blocks(text)
    fences = {n for b in found for n in ((b.opens, b.closes) if b.closed else (b.opens,))}
    return [re.sub(r"\s*\\$", "", (re.sub(r"^#+ ", "", ln.text.strip()) if ln.kind == reading.HEADING else ln.text).strip()).strip()
            for ln in reading.lines(text)
            if ln.text.strip() and ln.number not in fences and not re.fullmatch(r"[|:\- ]+", ln.text.strip())]


def show_refactor_and_refine_of_existing_specs(baseline):
    """What a Refactor and Refine cycle changed since its baseline commit, for a reader to trace:
    every line of six words or more now repeated more often than at the baseline, every line now
    held fewer times than at the baseline, and every line held more times, each with the files
    holding it. It decides nothing, since whether a repeat is a second home or one made by design,
    and whether a loss or a gain is a steer, is judgment."""
    def git(*a):
        return subprocess.run(["git", *a], capture_output=True, text=True, encoding="utf-8")
    try:
        top = git("rev-parse", "--show-toplevel")
    except FileNotFoundError:
        sys.stderr.write("show-refactor-and-refine-of-existing-specs: git is not installed, and this reads through it\n")
        return 2
    if top.returncode or Path(top.stdout.strip()).resolve() != Path.cwd().resolve():
        sys.stderr.write("show-refactor-and-refine-of-existing-specs: run it from the repository's root\n")
        return 2
    if git("rev-parse", "--verify", "--quiet", baseline + "^{commit}").returncode:
        sys.stderr.write("show-refactor-and-refine-of-existing-specs: no such commit: %s\n" % baseline)
        return 2

    def count(texts):
        n, where = {}, {}
        for path, text in texts:
            for t in refactor_and_refine_lines(text):
                n[t] = n.get(t, 0) + 1
                where.setdefault(t, []).append(path)
        return n, where
    then_files = git("ls-tree", "-r", "--name-only", baseline, "--", *REFACTOR_AND_REFINE_PATHS).stdout.split()
    now_files = sorted(set(git("ls-files", "--", *REFACTOR_AND_REFINE_PATHS).stdout.split())
                       | set(git("ls-files", "--others", "--exclude-standard", "--", *REFACTOR_AND_REFINE_PATHS).stdout.split()))
    then, then_where = count((f, git("show", "%s:%s" % (baseline, f)).stdout) for f in then_files)
    now, where = count((f, read(Path(f))) for f in now_files if Path(f).is_file())
    # a line of six words or more repeats only by being copied or by design; a shorter line,
    # a heading or a table's header, repeats by nature, so a gain in one is listed as new instead
    repeated = sorted(t for t in now if now[t] > 1 and now[t] > then.get(t, 0) and len(t.split()) >= 6)
    lost = sorted(t for t in then if then[t] > now.get(t, 0))
    new = sorted(t for t in now if now[t] > then.get(t, 0) and t not in repeated)
    print("== show-refactor-and-refine-of-existing-specs since %s" % baseline)
    for label, lines, held in (("repeated", repeated, where), ("lost", lost, then_where), ("new", new, where)):
        for t in lines:
            print("%-10s %s\n           in %s" % (label, t, ", ".join(sorted(set(held[t])))))
    print("%d repeated, %d lost, %d new; each for a reader to trace to a steer, the move map, or a repeat made by design\n" % (len(repeated), len(lost), len(new)))
    return 0


# Actions are flags per specs/methodology/skills/authoring-a-skill.md § Authoring a Skill.
# @canon-spec specs/methodology/sourcing-and-citation/writing-a-citation.md § Writing a Citation § A Citation's Link
def refresh_links(value):
    """--refresh-links: writes and refreshes each citation's link in the files a person reads; -> 0."""
    root = Path(value).resolve()
    if value == ".":
        # run from anywhere in the repository, the links are written over the whole of it
        found = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True)
        root = Path(found.stdout.strip()) if found.returncode == 0 else root
    changed = citation_links.refresh_tree(root)
    report("refresh-links", [])
    print("%d files changed" % len(changed))
    return 0


# @canon-spec specs/methodology/working-files/main.md § A Check's Report § What the Design Script Checks
# the constructs a self-review traces by its paths, the ones a construct's own block decides
WHOLE = ("Decision Table", "State Machine")


def repo_root():
    try:
        found = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True)
    except FileNotFoundError:  # no git on the machine
        return Path.cwd()
    return Path(found.stdout.strip()) if found.returncode == 0 else Path.cwd()


def is_applying(design_text):
    """Whether a design's Status reads applying."""
    return bool(re.search(r"^\*\*Status:\*\* applying(?: \\)?\s*$", design_text, re.M))


def uncommitted_changes(root):
    """-> the paths the checkout holds changed against the last commit, a new untracked one among them."""
    changed = subprocess.run(["git", "diff", "--name-only", "HEAD"], capture_output=True, text=True, cwd=root)
    added = subprocess.run(["git", "ls-files", "--others", "--exclude-standard"], capture_output=True, text=True, cwd=root)
    return [p for run in (changed, added) if run.returncode == 0 for p in run.stdout.split()]


def kept_changes(root, design_text):
    """-> the paths the checkout holds changed against the last commit, where the design is not applying, so its
    reading is the last commit's, as working-files/main.md § A Design Document § The States It Moves Through § A Send-back
    has a reading made while kept changes stand; else none. While a design is applying, the changes are its apply's
    own writing: a reading of the files takes them as they stand, and a reading of the plan's citations alone takes the
    last commit, which check_cited_headings asks for itself."""
    return [] if is_applying(design_text) else uncommitted_changes(root)


def check_constructs(value):
    """--check-constructs: the construct checks a file in scope takes, read as the audit reads them, the specs alone,
    since a design's Drafts are checked by the design check (working-files/main.md § A Design Document § The Record's
    Checks); -> 1 where a finding is reported, else 0, and 2 for a path that is no file in scope, a design among them."""
    root, target = repo_root(), Path(value).resolve()
    try:
        rel = target.relative_to(root).as_posix()
    except ValueError:
        rel = None
    if not target.is_file() or rel is None:
        sys.stderr.write("no file in the repository: %s\n" % value)
        return 2
    text_of = spec_texts(root)
    if rel not in text_of:
        sys.stderr.write("no file in scope; a design's Drafts are checked by --check-design: %s\n" % value)
        return 2
    print("== check-constructs " + rel)
    found, _, cands = constructs.run_checks(text_of)
    findings = [(rule, line, msg) for rule, path, line, msg in found if path == rel]
    candidates = [(line, name, context) for path, line, name, context in cands if path == rel]
    for rule, line, msg in sorted(findings, key=lambda f: f[1]):
        print("%s:%d  %s\n  %s" % (rel, line, rule, msg))
    for line, name, context in candidates:
        print("candidate %s:%d  [%s]\n  %s" % (rel, line, name, context))
    print("%d finding%s, %d candidate%s\n" % (len(findings), "" if len(findings) == 1 else "s", len(candidates),
                                              "" if len(candidates) == 1 else "s"))
    return 1 if findings else 0


# the shared modules --check-work runs, the specs' and the code's script checks and candidate lists
WORK_MODULES = ("spec_checks", "code_checks")
# Runs the shared checks over one tree in a process of their own, so no state a module keeps reaches the other tree's
# run, and prints them as JSON: the working tree with the checks as they stand, or a commit read through git in memory
# with the checks as they stood in it, or as they stand where it holds none of WORK_MODULES. It writes no file.
WORK_RUN = r'''
import importlib.abc, importlib.util, json, subprocess, sys
sys.dont_write_bytecode = True
repo, commit, lib = sys.argv[1], sys.argv[2], sys.argv[3]
if lib == "commit":
    listed = subprocess.run(["git", "ls-tree", commit, ".ai/skills/lib/"], cwd=repo, capture_output=True, check=True)
    entries = [l.split(None, 3) for l in listed.stdout.decode("utf-8").splitlines()]
    sources = {e[3].rsplit("/", 1)[1][:-3]: subprocess.run(["git", "cat-file", "blob", e[2]], cwd=repo,
               capture_output=True, check=True).stdout.decode("utf-8") for e in entries if e[3].endswith(".py")}

    class Commit(importlib.abc.MetaPathFinder, importlib.abc.Loader):
        def find_spec(self, name, path, target=None):
            return importlib.util.spec_from_loader(name, self) if path is None and name in sources else None

        def create_module(self, spec):
            return None

        def exec_module(self, module):
            module.__file__ = commit + ":.ai/skills/lib/" + module.__name__ + ".py"
            exec(compile(sources[module.__name__], module.__file__, "exec"), module.__dict__)
    sys.meta_path.insert(0, Commit())
else:
    sys.path.insert(0, lib)
from pathlib import Path, PurePosixPath
import code_checks, spec_checks, spec_text
tree = Path(repo) if commit == "-" else spec_text.CommitTree(repo, commit)
groups = [(h, [list(c) for c in rows]) for h, rows, _ in spec_checks.candidate_groups(tree)]
json.dump({"findings": [list(f) for f in spec_checks.check(tree)],
           "code": [[code_checks.rule_of(f)] + list(f) for f in code_checks.check_annotations(tree)],
           "candidates": groups,
           "code_candidates": [list(c) for c in code_checks.list_candidates(tree)]}, sys.stdout)
'''


def last_commit(root):
    """-> the last commit's hash, or None where the project has no version control or no commit yet."""
    try:
        found = subprocess.run(["git", "rev-parse", "--verify", "-q", "HEAD"], capture_output=True, text=True, cwd=root)
    except FileNotFoundError:
        return None
    return found.stdout.strip() if found.returncode == 0 and found.stdout.strip() else None


def checks_over(root, commit):
    """-> the shared checks' findings, candidates and code candidates over the working tree, commit None, or over a
    commit, each tree by the checks as they stood in it: the working tree by the modules the checkout the script is run
    in holds, and a commit by its own, or, where either holds none of the modules, by the ones beside this file."""
    lib = Path(root) / ".ai" / "skills" / "lib"
    lib = str(lib if all((lib / (m + ".py")).is_file() for m in WORK_MODULES) else Path(__file__).resolve().parent)
    if commit:
        held = subprocess.run(["git", "ls-tree", "--name-only", commit, ".ai/skills/lib/"], capture_output=True,
                              text=True, cwd=root).stdout.split()
        if all(".ai/skills/lib/%s.py" % m in held for m in WORK_MODULES):
            lib = "commit"
    run = subprocess.run([sys.executable, "-c", WORK_RUN, str(root), commit or "-", lib], capture_output=True,
                         cwd=root)
    if run.returncode:
        raise RuntimeError("the checks over %s failed:\n%s" % (commit or "the working tree",
                                                                run.stderr.decode("utf-8", "replace")))
    return json.loads(run.stdout.decode("utf-8"))


def work_changes(root, commit):
    """-> ({path: the lines the change added or changed, a deletion marking the line it stands before},
    {path: the lines the diff added alone}) for each file changed against the commit, a new untracked one among them,
    the working files aside."""
    status = subprocess.run(["git", "status", "--porcelain=v1", "-uall", "-z"], capture_output=True, text=True,
                            encoding="utf-8", cwd=root).stdout.split("\0")
    paths, i = [], 0
    while i < len(status):
        entry = status[i]
        if len(entry) > 3:
            paths.append(entry[3:])
            if entry[0] in "RC":
                i += 1  # a rename's or a copy's source follows it
        i += 1
    out, added = {}, {}
    for path in sorted(set(paths)):
        if is_working_file(path) or not (root / path).is_file():
            continue
        diff = subprocess.run(["git", "diff", "-U0", "--no-color", commit, "--", path], capture_output=True,
                              text=True, encoding="utf-8", errors="replace", cwd=root).stdout
        length = len((root / path).read_text(encoding="utf-8", errors="replace").split("\n"))
        lines, wrote = set(), set()
        for m in re.finditer(r"^@@ -\d+(?:,\d+)? \+(\d+)(?:,(\d+))? @@", diff, re.M):
            start, count = int(m.group(1)), int(m.group(2) or 1)
            wrote |= set(range(start, start + count))
            # git gives a deletion the line before it, and the deletion stands before the line after
            lines |= set(range(start, start + count)) if count else {min(start + 1, length)}
        if not diff:  # a file git does not yet track: every line is the change's
            lines = wrote = set(range(1, length + 1))
        out[path], added[path] = lines, wrote
    return out, added


def whole_section(secs, lineage):
    """-> the 0-based lines of a section with every section within it."""
    start, end = secs[lineage]
    for other, (_, e) in secs.items():
        if other.startswith(lineage + " § "):
            end = max(end, e)
    return set(range(start, end))


def around_and_up(text, line):
    """-> (the 0-based lines read around and up from a 1-based line, the lineages read around and up), as
    specs/AGENTS.md § Design, Refactor, Refine § Measure Twice, Cut Once § The Zoom-Out has the builder zoom out."""
    secs = sections(text)
    at = line - 1
    holding = next((l for l, (s, e) in secs.items() if s <= at < e), None)
    tops = sorted((s, l) for l, (s, _) in secs.items() if " § " not in l)
    first = tops[0][0] if tops else len(text.split("\n"))
    lines, names = set(range(0, first)), set()  # a file's text before its first section, read up from every line
    if holding is None or " § " not in holding:
        place = [l for _, l in tops].index(holding) if holding in [l for _, l in tops] else -1
        near = [l for n, (_, l) in enumerate(tops) if abs(n - place) <= 1] if place >= 0 else [l for _, l in tops[:1]]
    else:
        near = [holding.rsplit(" § ", 1)[0]]
    for lineage in near:
        lines |= whole_section(secs, lineage)
        names |= {l for l in secs if l == lineage or l.startswith(lineage + " § ")}
    parts = (holding or "").split(" § ")
    for depth in range(1, len(parts)):
        ancestor = " § ".join(parts[:depth])
        if ancestor in secs:
            names.add(ancestor)
            lines |= set(range(*secs[ancestor]))
    return lines, names


# @canon-spec specs/AGENTS.md § Design, Refactor, Refine § Measure Twice, Cut Once § The Zoom-Out
def citing_places(root):
    """-> [(the file a citation stands in, its 1-based line, the file it cites, the heading path it cites or "")] for
    each citation the durable files as they stand hold, found by the search the skills share, its search for every
    cited section, and by no pattern of the design script's own."""
    import search as searching
    engine = searching.Search(root, quiet=True)
    try:
        given = engine.cited_sections().places
    finally:
        engine.db.close()
    out = []
    for place in given:
        m = re.match(r"`([^`]+)` lines? (\d+).* cites `([^`]+)`$", str(place))
        if not m:
            continue
        cited, _, lineage = re.sub(r" \[[^\]]*\]$", "", m.group(3)).partition(" § ")
        out.append((m.group(1).split(" § ")[0], int(m.group(2)), cited, lineage))
    return out


def markdown_reach(text_of, changes, citing):
    """-> {path: 0-based lines} the builder zooms out to from each line a change wrote in a Markdown file in scope:
    around, up, and across, each passage citing what it read around, an ancestor or the file whole, read around and
    up in turn. citing gives each citation the durable files hold, as citing_places finds them by the search."""
    reach, read_names = {}, {}
    for path, lines in changes.items():
        if path not in text_of:
            continue
        for line in lines:
            got, names = around_and_up(text_of[path], line)
            reach.setdefault(path, set()).update(got)
            read_names.setdefault(path, set()).update(names)
    for host, n, cited, lineage in citing:
        if host in text_of and cited in read_names and (lineage in read_names[cited] or not lineage):
            got, _ = around_and_up(text_of[host], n)
            reach.setdefault(host, set()).update(got)
    return reach


def script_units(text):
    """-> [(first line, last line, name, names it calls)] for each function and class of a Python script, and each
    statement outside them, 1-based."""
    import ast
    try:
        tree = ast.parse(text)
    except SyntaxError:
        return [(1, len(text.split("\n")), None, set())]
    out = []

    def calls(node):
        return {c.func.id if isinstance(c.func, ast.Name) else c.func.attr for c in ast.walk(node)
                if isinstance(c, ast.Call) and isinstance(c.func, (ast.Name, ast.Attribute))}
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            out.append((node.lineno, node.end_lineno, node.name, calls(node)))
    for node in tree.body:
        if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            out.append((node.lineno, node.end_lineno, None, calls(node)))
    return out


def script_reach(root, changes):
    """-> {path: 1-based lines} of the reach in a script: the unit holding each change, the units it calls and the
    units calling it, as specs/AGENTS.md § Design, Refactor, Refine § Measure Twice, Cut Once § The Zoom-Out gives it; a
    script not in Python read whole."""
    scripts = {p: (root / p).read_text(encoding="utf-8", errors="replace") for s in scope_paths(root)
               for p in ([s] if (root / s).is_file() else
                         [f.relative_to(root).as_posix() for f in (root / s).rglob("*") if f.is_file()]
                         if (root / s).is_dir() else [])
               if p.endswith((".py", ".ps1", ".sh"))}
    units = {p: script_units(t) for p, t in scripts.items() if p.endswith(".py")}
    reach = {}
    for path, lines in changes.items():
        if path not in scripts:
            continue
        if path not in units:
            reach.setdefault(path, set()).update(range(1, len(scripts[path].split("\n")) + 1))
            continue
        for line in lines:
            holding = [u for u in units[path] if u[0] <= line <= u[1]]
            if not holding:
                continue
            first, last, name, called = min(holding, key=lambda u: u[1] - u[0])
            reach.setdefault(path, set()).update(range(first, last + 1))
            for other, its in units.items():
                for f, l, n, c in its:
                    if (n and n in called) or (name and name in c):
                        reach.setdefault(other, set()).update(range(f, l + 1))
    return reach


def check_work(value):
    """--check-work DESIGN: the specs' and the code's script checks over the work, the files changed against the last
    commit: each finding new against it, by the checks as they stood in each tree, and each candidate in the reach the
    builder zooms out to; -> 1 where a finding is reported."""
    design = design_file(value)
    if design is None:
        return 2
    root = repo_root()
    commit = last_commit(root)
    now = checks_over(root, None)
    found = [tuple(f) for f in now["findings"]] + [tuple(f) for f in now["code"]]
    print("== check-work " + design.stem)
    if commit is None:
        reported, candidates = found, [(h, [tuple(c) for c in rows]) for h, rows in now["candidates"]]
        code_candidates = [tuple(c) for c in now["code_candidates"]]
        heading = ("no version control, so no last commit was read: %d finding%s the scope holds, each to read against "
                   "the builder's own account of the files it changed")
        changes = None
    else:
        then = checks_over(root, commit)
        changes, added_lines = work_changes(root, commit)
        before = collections.Counter((r, p, m) for r, p, _, m in
                                     [tuple(f) for f in then["findings"]] + [tuple(f) for f in then["code"]])
        reported = []
        by_key = {}
        for f in found:
            by_key.setdefault((f[0], f[1], f[3]), []).append(f)
        for key, now_found in by_key.items():
            # matched by rule, file and message, its repeats counted, never by its line; a matched finding on a line
            # the change added is reported too, the change having rewritten what holds it
            added = [f for f in now_found if f[2] and f[2] in added_lines.get(f[1], ())]
            others = sorted((f for f in now_found if f not in added), key=lambda f: f[2])
            new = max(0, len(now_found) - before[key])
            reported += added + others[:max(0, new - len(added))]
        text_of = {p: t for p, t in spec_texts(root).items()}
        try:
            citing = citing_places(root)
        except Exception as exc:  # the search's own account of what it requires and lacks
            sys.stderr.write("--check-work finds the places citing what the work changed by the search the skills share, which "
                             "cannot be run: %s\n" % exc)
            return 2
        reach = {p: {n + 1 for n in lines} for p, lines in markdown_reach(text_of, changes, citing).items()}
        for p, lines in script_reach(root, changes).items():
            reach.setdefault(p, set()).update(lines)
        candidates = [(h, [tuple(c) for c in rows if c[0] in reach and (not c[1] or c[1] in reach[c[0]])])
                      for h, rows in now["candidates"]]
        before_code = {(c[0], c[2]) for c in then["code_candidates"]}
        code_candidates = [tuple(c) for c in now["code_candidates"] if c[0] in changes or (c[0], c[2]) not in before_code]
        heading = "%d finding%s new against the last commit, over " + "%d changed file%s" % (
            len(changes), "" if len(changes) == 1 else "s")
    by_rule = {}
    for rule, path, line, msg in reported:
        by_rule.setdefault(rule, []).append((path, line, msg))
    for rule in sorted(by_rule):
        print("\n%s" % rule)
        for path, line, msg in sorted(by_rule[rule]):
            print("  %s\n    %s" % ("%s:%s" % (path, line) if line else path, msg))
    print("\n" + heading % (len(reported), "" if len(reported) == 1 else "s"))
    listed = [(h, rows) for h, rows in candidates if rows]
    if code_candidates:
        listed.append(("Candidates for verify-spec-implementation's reading, on a file the change added or changed or "
                       "new against the last commit: places to read, not findings",
                       [(p, n, "", what) for p, n, what in code_candidates]))
    if listed:
        print("\nCandidates %s, never findings" % ("in the reach the builder zooms out to" if changes is not None
                                                   else "over the whole scope"))
    for h, rows in listed:
        print("\n" + h)
        for path, line, name, context in sorted(rows):
            print("  %s:%s%s\n    %s" % (path, line, "  [%s]" % name if name else "", context))
    print()
    return 1 if reported else 0


FLAGS = (
    ("--check-cited-headings", "PROPOSAL", check_cited_headings,
     "confirm every cross-file citation in the proposal points to a heading that exists"),
    ("--check-design-form", "DESIGN", check_design_form,
     "confirm a design document holds the form working-files/main.md sets"),
    ("--check-target-kind", "DESIGN", check_target_kind,
     "confirm every file a design document's Target names is of the kind its Kind field declares, and that it names no working file"),
    ("--check-design", "DESIGN", check_design,
     "run the validation review on one design document, writing no stamp: its form, its records, the references within it, the lineage from research to its steps and, by the construct checks, each construct a step's Draft holds, drawing only on the document, the reports of the handed-off judgments of its current major version its log names, as working-files/main.md § A Design Document § The Record's Checks bounds them, the canon's declarations of its form and, for a Draft's constructs, the specs as they stand; the builder runs it at validating before each adversarial round"),
    ("--check-workstack", "PLANS_DIR", check_workstack,
     "report what is out of sync in the workstack, each name in a Depends On Designs read from the plans folders as they stand: a field of a design's header its form does not take, an approved or applying design naming an unfinished design, and a loop in Depends On Designs or Spawned By; a name of a finished or gone design is no problem of the workstack, and a complete or an abandoned design's names are its history; the builder runs it before each validation; reads the skill's plans folder, and those beside it, unless given another plans folder, and no design standing outside the plans folders"),
    ("--show-workstack", "PLANS_DIR", show_workstack,
     "draw the workstack and list what to work next, each name in a Depends On Designs read from the plans folders as they stand: a design blocked by each unfinished design it names, a design waiting to be freed of each finished or gone design it names, the blocked designs apart, and each finished design, which may be deleted or moved at any time; writes no file; reads the skill's plans folder, and those beside it, unless given another plans folder, and no design standing outside the plans folders"),
    ("--show-design", "DESIGN", show_design,
     "show the header and the goals of a design standing in a plans folder, given by its file or by its name as a Depends On Designs names it, and nothing else of it, so a builder learns what a design it links to decides without opening it; of a design whose header or goals do not hold the form working-files/main.md sets, show each field it can read and name each that is missing or not valid; of a design standing in no plans folder, show nothing and say so; writes no file and brings no design to its form"),
    ("--check-design-names", "DESIGN", check_design_names,
     "report each design a design's own Depends On Designs names that is finished or gone, and which of the two, read from the plans folders as they stand, listing beside them each unfinished design it names, which blocks it; reports a design standing in no plans folder, and nothing of a complete or an abandoned design, whose names are its history; writes no file; the builder runs it before any other act on a design, so a misspelled name is seen before --free-design writes anything"),
    ("--free-design", "DESIGN", free_design,
     "free a design of each finished or gone design its Depends On Designs names, writing that design alone: remove each such name and, where its goals are agreed in its current major version, append its design-reassessment entry, its Cause a changed foundation naming each design it was freed from, and, where it stood approved or applying, move its Status to in-progress and append its entered entry; writes nothing to a complete or an abandoned design, to one naming no such design, or to one standing in no plans folder; the builder runs it after --check-design-names, before any other act on the design"),
    ("--show-dependents", "DESIGN NAME", show_dependents,
     "list each part of a design naming or citing one of its goals, cases, principles, Frame Outcomes, steps or step Objectives by its Name, in the order specs/AGENTS.md § Design, Refactor, Refine § Measure Twice, Cut Once § The Order of a Design's Parts gives a change; writes no file and decides nothing; the builder runs it as a steer, a settlement or a pass changes a part"),
    ("--show-validation", "DESIGN", show_validation,
     "print a design document's stamped hash, its hash now, and whether it is validated, stale or never stamped"),
    ("--stamp-validation", "DESIGN", stamp_validation,
     "run the validation review on one design document and, if it passes, write its validation stamp, taking in each log entry naming a report the review reads; refuses a design standing in no plans folder; the builder runs it at validating on the way to the user's approval"),
    ("--log-entry", "DESIGN KIND [FIELD=VALUE ...]", log_entry,
     "append an entry to a design document's log, its count among its kind and the UTC time it is appended, refusing a kind, a field or a value out of the Design Log Entry type, a design-reassessment entry holding no Cause, an entry --free-design alone appends, any entry to a design standing in no plans folder or naming a finished or gone design and not yet freed, and an entry that begins or continues work past the frame to a design naming an unfinished design; for a check's entry, reading its report at reports/<kind>/{n}.md in the design's folder, writing a self-review's script checks' output into it, and, for a self-review over applied work, running --check-kept-tests over the design's changes, writing what each run gave into the report with that output and refusing the entry where a kept test fails or cannot be run or the report's differential test leaves out a design the comparison lists; refusing the entry too where the report is out of its form, its layout or the form of its values holding places, leaves a finding unsettled or settles one twice, cites a key naming no record, holds a Search of the builder's whose matches its Places do not cover, holds a marked Finding of the builder's anchored in no part of the design, or holds records not covering what working-files/main.md § A Check's Report § What the Design Script Checks has the script check of them, and taking the entry's counts from it, refusing any the builder gives; the builder appends every entry through it"),
    ("--check-handed-back", "REPORT", check_handed_back,
     "check a review's report at its path in a design's folder before its settlement, or a handed-off judgment's before the builder takes it in: the cold agent's part, its title, its Reading, its Findings, its Searches and its Read Assessments, held to the form working-files/main.md § A Check's Report gives it and to its layout, its values holding places in their form, each Search run again, each place it read lying within a Read Assessment's Area and each area it assesses again naming a cause that counts where it holds Read Assessments, and each marked Finding naming the parts of the design it bears on, or the rules it breaks; writes no file; the cold agent runs it before handing the report back, and the builder as settling starts"),
    ("--take-up-report", "REPORT", take_up_report,
     "take up a review's or a handed-off judgment's report its cold agent handed back, as working-files/main.md § A Check's Report § Who Writes Each Part § The Report's Workflow has it: the hand-back check run again and, where it passes, the report's Hand-back part written, a fingerprint of each part the cold agent wrote; where it reports, nothing is written and the report goes back to its cold agent"),
    ("--check-settled-report", "REPORT", check_settled_report,
     "check a check's report at its path in a design's folder once it is settled, by every check --log-entry runs on it as it logs the check's entry: its form, its layout, its values holding places in their form, each finding settled once, each key naming a record, each Search's matches covered, each marked Finding anchored in the design, and its records covering what working-files/main.md § A Check's Report § What the Design Script Checks has the script check of them; of a report a cold agent wrote it reads the builder's parts alone, holding each part that agent wrote to the fingerprint the take-up wrote of it and to nothing the design or the files have come to hold since; writes no file, a self-review's report read with the Script Output --log-entry would write into it; the builder runs it as a check's settling ends, before logging its entry"),
    ("--show-reach", "DESIGN", show_reach,
     "list each line of a durable file holding a phrase the design's Retired Phrases record in whatever form it takes, outside its Stays Right, marking those outside the Target, found by the search the skills share, at the last commit while a design's uncommitted changes are kept; the builder runs it at drafting"),
    ("--check-retired-wording", "DESIGN", check_retired_wording,
     "report each line of the Target's durable files holding a retired phrase in whatever form it takes outside its Stays Right, with its replacement, found by the search the skills share; the builder runs it at its self-review before the post-apply review"),
    ("--check-changed-files", "DESIGN", check_changed_files,
     "list each file changed against the last commit outside the working files that the Target does not name, marking the user's edits and the direct edits the log names; the builder runs it at its self-review before the post-apply review"),
    ("--check-audits", "DESIGN", check_audits,
     "refuse a design whose log, after its last apply entry, records neither the run nor the user's bypass of an audit it must run, the specs audit where it changed a file of any sub-scope and the code audit where it changed code, its changes read as working-files/main.md § A Design Document § Applying and Committing has them read; writes no file; the builder runs it before it brings the user the commit, or, with no version control, before the design becomes applied"),
    ("--check-work", "DESIGN", check_work,
     "run the specs' and the code's script checks over the design's work, the files changed against the last commit, whatever they touch: each finding the scope holds now that it did not hold then, each tree by the checks as they stood in it, matched by its rule, its file and its message, its repeats counted, a matched finding on a line the change added reported too; then, apart, each candidate in the reach the builder zooms out to from what the change wrote, the places citing it found by the search the skills share; with no version control, every finding the scope holds; writes no file; the builder runs it at its self-review, and the post-apply review runs it"),
    ("--check-kept-tests", "[FILE ...]", check_kept_tests,
     "run the kept tests of each script whose files the changed files given hold, a script's files being its code and each file of the canon it reads a form from as it runs, as its kept tests under tests/spec-of-record/scripts/ name them, and each kept comparison whose script's files they hold, the design script's among them, printing what each gave; given no file, read the files the checkout holds changed against the last commit, the working files aside; names no design, so a direct edit of such a file runs it before the user approves the edit; fails where a test fails or a kept file cannot be run, and never for what a comparison lists; --log-entry runs it as it appends the entry of a self-review over applied work, over the design's changes"),
    ("--refresh-links", "ROOT", refresh_links,
     "write and refresh the link every citation in a file a person reads on GitHub carries, README.md, the files under docs/ and every spec but specs/AGENTS.md; the apply runs it once the text its steps call for is written; reads the repository holding the current directory unless given a root"),
    ("--check-constructs", "FILE", check_constructs,
     "run the construct checks on a file in scope, the file's constructs as the audit checks them, the specs alone, since a design's Drafts are checked by --check-design; candidates are listed apart; the builder runs it on the applied files at its self-review at the apply"),
    ("--show-refactor-and-refine-of-existing-specs", "BASELINE", show_refactor_and_refine_of_existing_specs,
     "show what a Refactor and Refine cycle over existing specs changed since the baseline commit, for a reader to trace: lines now repeated, lost and new, each with the files holding it; decides nothing; run from the repository's root on a tree with the cycle's changes applied"),
)


def main(argv, plans=PLANS):
    global PLANS
    PLANS = plans
    parser = argparse.ArgumentParser(prog=Path(argv[0]).name, description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter, allow_abbrev=False)
    for flag, metavar, _, help_text in FLAGS:
        # a flag given more than once runs once for each value it is given
        if flag in ("--check-workstack", "--show-workstack"):
            parser.add_argument(flag, metavar=metavar, nargs="?", const=PLANS, action="append", help=help_text)
        elif flag == "--refresh-links":
            parser.add_argument(flag, metavar=metavar, nargs="?", const=".", action="append", help=help_text)
        elif flag == "--show-dependents":
            parser.add_argument(flag, metavar=("DESIGN", "NAME"), nargs=2, action="append", help=help_text)
        elif flag == "--log-entry":
            parser.add_argument(flag, metavar="ARG", nargs="+", action="append", help=metavar + ": " + help_text)
        elif flag == "--check-kept-tests":
            parser.add_argument(flag, metavar="FILE", nargs="*", action="append", help=help_text)
        else:
            parser.add_argument(flag, metavar=metavar, action="append", help=help_text)
    args = vars(parser.parse_args(argv[1:]))
    chosen = [(run, value) for flag, _, run, _ in FLAGS for value in args[flag[2:].replace("-", "_")] or []]
    if not chosen:
        parser.print_usage(sys.stderr)
        return 2
    return max(run(value) for run, value in chosen)


if __name__ == "__main__":
    sys.stderr.write("run a skill's entry script, not this shared code: specs/methodology/skills/authoring-a-skill.md § Authoring a Skill\n")
    sys.exit(2)
