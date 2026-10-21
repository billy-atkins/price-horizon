#!/usr/bin/env python3
"""The design document tooling the skills writing design documents share: the validation review, which holds a
design document to its form, drawing only on the document and the canon's declarations of its form, and stamps a
design that passes; and the builder's tools, which check the headings a proposal cites, a Target against its
Kind and the constructs a design or a file states, through the construct checks in constructs.py, for its
self-review, check the workstack, show a validation, write citations' links, and show what a
Refactor and Refine cycle changed.

A design document must hold the form working-files.md sets, and the workstack its lineage draws must hold
together. Its actions are flags per specs/methodology/skills.md § Authoring a Skill. The exit status is 0 when
every check passes, 1 when one finds a problem, and 2 for a usage error.

Standard library only, git aside, which --show-refactor-and-refine-of-existing-specs reads through, and run by
no agent directly: each skill writing design documents calls main from its own entry script with its own plans
folder, per specs/methodology/skills.md § Authoring a Skill.
"""

import argparse
import datetime
import hashlib
import re
import subprocess
import sys
from pathlib import Path

import citation_links
import constructs
from spec_text import REGISTRY, lineages, read, registry, sections, skill_dirs, spec_texts, strip_fences


# @canon-spec specs/methodology/working-files.md § A Design Document § The Kinds of Change
KINDS = ("canon-specs", "application-specs", "code", "documentation", "other")
KIND_LIST = ", ".join(KINDS[:-1]) + " or " + KINDS[-1]
# working-files.md § A Design Document and § Steering Decision
PLANS = ".ai/plans/design-specs"  # set by the entry script calling main
# @canon-spec specs/methodology/working-files.md § A Design Document
CODE_PLANS = "implement-specs"  # the plans folder of the designs changing code, whose kind is code
# @canon-spec specs/methodology/working-files.md § A Design Document
FIELDS = ("Name", "Status", "Source", "Kind", "Target", "Spawned By", "Depends On", "Validated")
# working-files.md § A Stamp: a UTC timestamp and a content hash; a design document's
# Validated stamp leaves out the Validated and Status fields.
STAMP = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z sha256:[0-9a-f]{16}$")
# @canon-spec specs/methodology/working-files.md § A Design Document
# @canon-spec specs/methodology/working-files.md § A Stamp
UNSTAMPED = ("Validated", "Status")
# @canon-spec specs/methodology/working-files.md § A Design Document
IMPACT = "Impact on the Application Specs"  # a canon design's, and no other design's
# @canon-spec specs/methodology/working-files.md § A Design Document
SECTIONS = ("The Problem", "Design Goals", "The Design Frame", "Steering Decisions", "Design Plan Steps", IMPACT, "The Builder's Passes", "Out of Scope")
# @canon-spec specs/methodology/working-files.md § A Design Document
OPTIONAL = ("Steering Decisions",)
# @canon-spec specs/methodology/working-files.md § A Design Document
# the goals, required as the frame is, but in a design complete or abandoned
UNTIL_FINISHED = ("Design Goals",)
# @canon-spec specs/methodology/working-files.md § A Design Document
# the design frame's level-three headings, in order, and the text a part not yet stated holds, which no design
# approved or further holds
FRAME = ("Scope", "Approach", "Outcomes")
NOT_YET_STATED = "Not yet stated."
# @canon-spec specs/methodology/working-files.md § A Design Document
# the text a step section holds until drafting states the steps, which no design approved or further holds
NOT_YET_DRAFTED = "Not yet drafted."
# @canon-spec specs/methodology/working-files.md § Steering Decision
# where the Steering Decision type is declared: its fields and its Type's values are read from that declaration,
# this tooling holding no copy of them
STEER_HOME = ("specs/methodology/working-files.md", "Steering Decision")
# @canon-spec specs/methodology/working-files.md § Design Goal
GOAL_HOME = ("specs/methodology/working-files.md", "Design Goal")
# @canon-spec specs/methodology/working-files.md § Design Plan Step
STEP_HOME = ("specs/methodology/working-files.md", "Design Plan Step")


def declared_type(home, plural, root=None):
    """A record type as its declaration gives it -> (its table of record fields, a row to a field, problems with the
    declaration: no Record Form, a Plural Name other than the one a design's record section takes, a Reference Key
    other than Name, or no table of its record fields)."""
    path, title = home
    # the checkout's root: the one given, or the nearest directory up from this file, or else from where it runs,
    # holding the declaration's file
    here = Path(__file__).resolve()
    base = Path(root) if root else next((p for p in (*here.parents, Path.cwd(), *Path.cwd().parents) if (p / path).exists()), Path.cwd())
    if not (base / path).exists():
        return [], [(path, "no file declares the %s type" % title)]
    text = read((base / path)).replace("\r\n", "\n")
    lines = [l.strip() for l in (section(text, title) or "").split("\n")]
    problems = [] if "**Construct:** `specs/methodology/modeling-constructs.md § Constructs § Record Form`" in lines \
        else ["no Record Form declares the %s type" % title]
    if "**Plural Name:** " + plural not in lines:
        problems.append("the %s type declares no Plural Name %s, the title a design's record section takes" % (title, plural))
    if "**Reference Key:** Name" not in lines:
        problems.append("the %s type declares no Reference Key Name" % title)
    head = next((i for i, l in enumerate(lines) if l.startswith("| Field | Unique | Required | Default Value | Values |")), None)
    rows = []
    for l in lines[head + 2:] if head is not None else []:
        if not l.startswith("|"):
            break
        rows.append([c.strip() for c in l.strip("|").split("|")])
    if not rows:
        problems.append("the %s type gives no table of its record fields" % title)
    return rows, [(path, p) for p in problems]


def steer_type(root=None):
    """The Steering Decision type as its declaration gives it -> (its fields in order, its Type field's values,
    problems with the declaration)."""
    rows, problems = declared_type(STEER_HOME, "Steering Decisions", root)
    types = next((tuple(re.findall(r'"([^"]+)"', row[4])) for row in rows if row[0] == "Type" and len(row) > 4), ())
    return tuple(row[0] for row in rows), types, problems


def goal_type(root=None):
    """The Design Goal type as its declaration gives it -> (its fields in order, problems with the declaration)."""
    rows, problems = declared_type(GOAL_HOME, "Design Goals", root)
    return tuple(row[0] for row in rows), problems


def step_type(root=None):
    """The Design Plan Step type as its declaration gives it -> (its fields in order, problems with the declaration)."""
    rows, problems = declared_type(STEP_HOME, "Design Plan Steps", root)
    return tuple(row[0] for row in rows), problems


# working-files.md § A Design Document: an adversarial review's, a post-apply review's or an audit's pass,
# its lead-in and what follows it to the next, names the model and effort it ran on; a lead-in in another case,
# or the retired Post-apply audit lead-in, is caught to be reported.
# @canon-spec specs/methodology/working-files.md § A Design Document
REVIEW = re.compile(r"^\*\*(?:Adversarial review|Post-apply (?:review|audit)|Audit)(?![\w-])", re.I)
# @canon-spec specs/methodology/working-files.md § A Design Document
REVIEW_FORM = re.compile(r"^\*\*(?:Adversarial review|Post-apply review|Audit)(?![\w-])")
# @canon-spec specs/AGENTS.md § Design, Refactor, Refine
# @canon-spec specs/methodology/working-files.md § A Design Document
RAN_ON = re.compile(r"\bon [^\s,;]+(?: [^\s,;]+)*? (?:at (?:light|medium|high) effort|as the agent allows)\b", re.I)
# @canon-spec specs/methodology/working-files.md § A Design Document § The States It Moves Through
STATES = ("not-started", "in-progress", "approved", "applying", "complete", "abandoned")
# @canon-spec specs/methodology/working-files.md § A Design Document § The States It Moves Through
# the states its Trigger Classes table makes a design finish in
FINISHED = ("complete", "abandoned")
# A field's value runs to the next line opening with a field's key, or to a blank line.
KEY = r"\*\*([A-Z][A-Za-z ]*):\*\*"
ROOT_FIELD = re.compile(r"^" + KEY + r" ?(.*?)(?=\n[ \t-]*\*\*[A-Z][A-Za-z ]*:\*\*|\n\s*\n|\Z)", re.M | re.S)


def read_design(f):
    """-> (file name, [(key, value)], [level-two heading], text) for one design document;
    its fields are read from the Design Document section, before its first level-two heading."""
    text = read(f).replace("\r\n", "\n")
    head = text.split("\n## ", 1)[0]
    fields = [(k, " ".join(v.split())) for k, v in ROOT_FIELD.findall(head)]
    return f.stem, fields, re.findall(r"^## (.+?)\s*$", text, re.M), text


def is_design(f):
    return read(f).lstrip("\ufeff").startswith("# Design Document")


def read_designs(folder):
    """-> every design the workstack draws on: those in folder, named by file name, and those in each
    other skill's plans folder beside it, named by that folder's name, a slash and the file name, their
    Spawned By and Depends On named the same way, per working-files.md § A Design Document."""
    folder = Path(folder).resolve()
    out = [read_design(f) for f in sorted(folder.glob("*.md")) if is_design(f)] if folder.is_dir() else []
    for other in sorted(p for p in folder.parent.iterdir() if p.is_dir() and p != folder):
        for f in sorted(other.glob("*.md")):
            if not is_design(f):
                continue
            name, fields, sections, text = read_design(f)
            fields = [(k, rename(v, other.name, folder.name)) if k in ("Spawned By", "Depends On") else (k, v) for k, v in fields]
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
    """-> the design documents a Spawned By or Depends On value names; none for none."""
    if value.strip().lower() in ("", "none"):
        return []
    return [n.strip().strip("`") for n in value.split(";") if n.strip()]


def content_hash(text, leave_out=UNSTAMPED):
    """working-files.md § A Stamp: SHA-256 of the text as UTF-8, line endings a line feed,
    the lines holding the left-out fields dropped; its first 16 hexadecimal characters."""
    keys = "|".join(re.escape(k) for k in leave_out)
    lines = [l for l in text.replace("\r\n", "\n").split("\n") if not re.match(r"\*\*(?:%s):\*\*" % keys, l)]
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


def kebab(text):
    """The Name in kebab-case: lowercase, each run of other characters a hyphen."""
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


def section(text, title):
    m = re.search(r"^## " + re.escape(title) + r"\s*$", text, re.M)
    if not m:
        return None
    rest = text[m.end():]
    nxt = re.search(r"^## ", rest, re.M)
    return rest[:nxt.start()] if nxt else rest


def frame_parts(text):
    """The design frame's parts, each heading with what it holds."""
    parts = re.split(r"^### (.+?)\s*$", section(text, "The Design Frame") or "", flags=re.M)[1:]
    return dict(zip(parts[::2], (p.strip() for p in parts[1::2])))


def check_steers(body):
    """-> problems with a Steering Decisions section: a Records field, and each record its
    type's fields in order, its Type one of the field's values, no two sharing a Name."""
    if not re.search(r"^\*\*Records:\*\*\s*$", body, re.M):
        return ["Steering Decisions has no Records field"]
    items = re.split(r"^- ", body.split("**Records:**", 1)[1], flags=re.M)[1:]
    if not items:
        return ["Steering Decisions holds no record"]
    problems, seen = [], set()
    fields, types, declared = steer_type()
    if not fields:
        return [p for _, p in declared] or ["the Steering Decision type declares no fields"]
    for item in items:
        keys = re.findall(r"^[ \t]*" + KEY, item, re.M)
        if keys != list(fields):
            problems.append("a steering decision's fields are %s, not %s" % (", ".join(keys), ", ".join(fields)))
            continue
        name = re.match(KEY + r" ?(.*)", item).group(2).strip()
        type_ = re.search(r"^[ \t]*\*\*Type:\*\* ?(.*)$", item, re.M).group(1).strip()
        if type_ not in types:
            problems.append("steering decision %s has a Type that is not one of %s: %s" % (name, ", ".join(types), type_))
        if name in seen:
            problems.append("two steering decisions share the Name " + name)
        seen.add(name)
    return problems


def check_goals(body):
    """-> problems with a Design Goals section: `Not yet stated.`, or a Records field and each record its type's
    fields in order, its Name a slug, no two sharing a Name."""
    if body.strip() == NOT_YET_STATED:
        return []
    if not re.search(r"^\*\*Records:\*\*\s*$", body, re.M):
        return ["Design Goals has no Records field"]
    items = re.split(r"^- ", body.split("**Records:**", 1)[1], flags=re.M)[1:]
    if not items:
        return ["Design Goals holds no record"]
    fields, declared = goal_type()
    if not fields:
        return [p for _, p in declared] or ["the Design Goal type declares no fields"]
    problems, seen = [], set()
    for item in items:
        keys = re.findall(r"^[ \t]*" + KEY, item, re.M)
        if keys != list(fields):
            problems.append("a design goal's fields are %s, not %s" % (", ".join(keys), ", ".join(fields)))
            continue
        name = re.match(KEY + r" ?(.*)", item).group(2).strip()
        # working-files.md § Design Goal: a Name in kebab-case, as a design document's Name is
        if kebab(name) != name:
            problems.append("a design goal's Name is not in kebab-case: " + name)
        if name in seen:
            problems.append("two design goals share the Name " + name)
        seen.add(name)
    return problems


# a record's own fields: the first opening its list item, the rest indented two spaces, so a record nested in an
# Objective, indented further, holds fields of its own
STEP_KEY = re.compile(r"^(?:- |  )" + KEY, re.M)


def check_steps(body):
    """-> problems with a Design Plan Steps section: `Not yet drafted.`, or a Records field and each record its type's
    fields in order, Objectives a list and the last field, its Name a slug, no two sharing a Name, each Why citing a
    goal, which check_form holds to the goals the design holds, and each step a step cites one the section holds."""
    if body.strip() == NOT_YET_DRAFTED:
        return []
    if not re.search(r"^\*\*Records:\*\*\s*$", body, re.M):
        return ["Design Plan Steps has no Records field"]
    items = re.split(r"^- ", body.split("**Records:**", 1)[1], flags=re.M)[1:]
    if not items:
        return ["Design Plan Steps holds no record"]
    fields, declared = step_type()
    if not fields:
        return [p for _, p in declared] or ["the Design Plan Step type declares no fields"]
    problems, seen = [], set()
    for item in items:
        item = "- " + item
        keys = STEP_KEY.findall(item)
        if keys != list(fields):
            problems.append("a design plan step's fields are %s, not %s" % (", ".join(keys), ", ".join(fields)))
            continue
        name = re.match(r"- " + KEY + r" ?(.*)", item).group(2).strip()
        # working-files.md § Design Plan Step: a Name in kebab-case, as a design document's Name is
        if kebab(name) != name:
            problems.append("a design plan step's Name is not in kebab-case: " + name)
        if name in seen:
            problems.append("two design plan steps share the Name " + name)
        seen.add(name)
        # the last field, Objectives, a list: what follows its key is list items
        last = item.split("**%s:**" % fields[-1], 1)[1]
        if last.split("\n", 1)[0].strip() or not re.search(r"^[ \t]+- ", last, re.M):
            problems.append("design plan step %s's %s is not a list" % (name, fields[-1]))
        why = re.search(r"^  \*\*Why:\*\* ?(.*?)(?=^  \*\*|\Z)", item, re.M | re.S)
        cited = re.findall(r"`§ Design Goals \[Name: ([^\]]+)\]`", why.group(1) if why else "")
        if not cited:
            problems.append("design plan step %s's Why cites no goal" % name)
    for step in sorted({c.strip() for c in re.findall(r"`§ Design Plan Steps \[Name: ([^\]]+)\]`", body)} - seen - {"…"}):
        problems.append("a citation of a step the design does not hold: " + step)
    return problems


def steer_table_problems(root):
    """-> problems with the Steering Decision, Design Goal and Design Plan Step types' declarations, which this tooling
    reads their records' fields from."""
    return steer_type(root)[2] + goal_type(root)[1] + step_type(root)[1]


def check_form(design):
    """-> (1, [(file name, problem)]): one design document against its form."""
    problems, designs = [], [read_design(design)]
    for name, fields, sections, text in designs:
        if not text.startswith("# Design Document\n"):
            problems.append((name, "it does not open with the heading Design Document"))
        keys, values = [k for k, _ in fields], dict(fields)
        if keys != list(FIELDS):
            problems.append((name, "its fields are %s, not %s" % (", ".join(keys), ", ".join(FIELDS))))
        # working-files.md § A Design Document: the Name is the design's slug, and its file is {Name}.md
        if values.get("Name") and kebab(values["Name"]) != values["Name"]:
            problems.append((name, "Name is not a slug: " + values["Name"]))
        elif values.get("Name") and values["Name"] != name:
            problems.append((name, "Name is not its file name without .md: " + values["Name"]))
        if values.get("Status", "") not in STATES:
            problems.append((name, "Status is not a state: " + values.get("Status", "")))
        if not values.get("Name"):
            problems.append((name, "Name is empty"))
        if values.get("Kind", "") not in KINDS:
            problems.append((name, "Kind is not %s: %s" % (KIND_LIST, values.get("Kind", ""))))
        # working-files.md § A Design Document § A Design Changing Code: the folder sets the kind
        if values.get("Kind") and (values["Kind"] == "code") != (design.parent.name == CODE_PLANS):
            problems.append((name, "Kind is code for a design under .ai/plans/%s/ and for no other: %s" % (CODE_PLANS, values["Kind"])))
        target = values.get("Target", "")
        unknown = values.get("Status") == "not-started" and target.lower() == "none"
        if not unknown and not all(re.fullmatch(r"`[^`]+`", p.strip()) for p in (target.split(";") if target else [""])):
            problems.append((name, "Target is not paths in backticks separated by semicolons: " + target))
        validated = values.get("Validated", "")
        if validated.lower() != "none" and not STAMP.match(validated):
            problems.append((name, "Validated is neither none nor a stamp: " + validated))
        elif values.get("Status") == "approved" and not STAMP.match(validated):
            problems.append((name, "approved, but no validation review has stamped it"))
        elif values.get("Status") == "approved" and validated.split(" ")[1] != content_hash(text):
            problems.append((name, "approved, but edited since its validation review stamped it"))
        elif values.get("Status") in ("applying", "complete") and not STAMP.match(validated):
            problems.append((name, values["Status"] + ", but no validation review stamped it"))
        for p in re.split(r"(?m)^(?=\*\*\S)", section(text, "The Builder's Passes") or ""):
            if REVIEW.match(p) and not REVIEW_FORM.match(p):
                problems.append((name, "a review's lead-in is not written as the form sets it, Adversarial review, Post-apply review or Audit: " + p[:40].strip()))
            if REVIEW.match(p) and not RAN_ON.search(p):
                problems.append((name, "a review's pass names no model and reasoning effort, as on {model} at {effort} effort or on {model} as the agent allows: " + p[:60].strip()))
        want = [s for s in SECTIONS if (s in sections or (s not in OPTIONAL and (s not in UNTIL_FINISHED or values.get("Status") not in FINISHED))) and (s != IMPACT or values.get("Kind") == "canon-specs")]
        if sections != want:
            problems.append((name, "its sections are %s, not %s" % (", ".join(sections), ", ".join(want))))
        frame = frame_parts(text)
        heads = re.findall(r"^### (.+?)\s*$", section(text, "The Design Frame") or "", re.M)
        if "The Design Frame" in sections and heads != list(FRAME):
            problems.append((name, "its design frame's headings are %s, not %s" % (", ".join(heads) or "none", ", ".join(FRAME))))
        if values.get("Status") in ("approved", "applying", "complete"):
            for part in [p for p in FRAME if frame.get(p) == NOT_YET_STATED]:
                problems.append((name, values["Status"] + ", but its design frame's " + part + " is not yet stated"))
        body = section(text, "Steering Decisions")
        for p in check_steers(body) if body is not None else []:
            problems.append((name, p))
        goals = section(text, "Design Goals")
        for p in check_goals(goals) if goals is not None else []:
            problems.append((name, p))
        if goals is not None and goals.strip() == NOT_YET_STATED and values.get("Status") in ("approved", "applying", "complete"):
            problems.append((name, values["Status"] + ", but its design goals are not yet stated"))
        # specs/AGENTS.md § Design, Refactor, Refine: the frame and the steps cite the goals they rest on by Names the
        # design holds
        held = set(re.findall(r"^- \*\*Name:\*\* (.+?)\s*$", goals or "", re.M))
        steps = section(text, "Design Plan Steps")
        cites = re.findall(r"`§ Design Goals \[Name: ([^\]]+)\]`", (section(text, "The Design Frame") or "") + (steps or ""))
        for cited in sorted({c.strip() for c in cites} - held - {"…"}):
            problems.append((name, "a citation of a goal the design does not hold: " + cited))
        for p in check_steps(steps) if steps is not None else []:
            problems.append((name, p))
        if steps is not None and steps.strip() == NOT_YET_DRAFTED and values.get("Status") in ("approved", "applying", "complete"):
            problems.append((name, values["Status"] + ", but its steps are not yet drafted"))
    return len(designs), problems


# @canon-spec specs/methodology/working-files.md § A Design Document § The Kinds of Change
def kind_of(path, skills):
    """canon-specs, application-specs, or None for any other file; skills, the registered skills' directories and lib."""
    if path in ("specs/AGENTS.md", "specs/architecture.md") or path.startswith("specs/methodology/"):
        return "canon-specs"
    if any(path.startswith(".ai/skills/" + n + "/") for n in skills):
        return "canon-specs"
    if path.startswith("specs/application/"):
        return "application-specs"
    return None


# @canon-spec specs/methodology/working-files.md § The Working Files
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


def check_stack(folder):
    """-> (report lines, [(file name, problem)]): the workstack each design document's
    Spawned By and Depends On draw, and where its Status is out of sync with what it
    depends on, per working-files.md § A Design Document."""
    read = read_designs(folder)
    designs = {name: dict(fields) for name, fields, _, _ in read}
    checked = {name: validation(text, fields)[0] for name, fields, _, text in read}
    status = lambda n: designs[n].get("Status", "")
    names = lambda n, key: named(designs[n].get(key, ""))
    deps = lambda n: [d for d in names(n, "Depends On") if d in designs]
    blocked_by = lambda n: [d for d in deps(n) if status(d) not in FINISHED]
    landed = lambda n: [d for d in deps(n) if status(d) in FINISHED]
    problems = []
    for n in designs:
        for d in names(n, "Depends On"):
            if d not in designs:
                problems.append((n, "Depends On names no design document: " + d))
        s = status(n)
        unapproved = [d for d in blocked_by(n) if status(d) not in ("approved", "applying")]
        if s == "approved" and unapproved:
            problems.append((n, "approved, but its Depends On names %s, not approved; it goes back to in progress" % "; ".join(unapproved)))
        elif s == "approved" and landed(n):
            problems.append((n, "approved, but %s has finished; it goes back to in progress to take it in" % "; ".join(landed(n))))
        elif s in ("applying", "complete") and names(n, "Depends On"):
            problems.append((n, "%s, but its Depends On names %s; a design is applied once it names none" % (s, "; ".join(names(n, "Depends On")))))

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
        for d in deps(n):
            hit = dep_cycles(d, path + [n])
            if hit:
                return hit
        return None
    reported = set()
    for n in designs:
        hit = dep_cycles(n, [])
        if hit and frozenset(hit) not in reported:
            reported.add(frozenset(hit))
            problems.append((n, "Depends On runs in a cycle: " + " -> ".join(hit)))
    parent = lambda n: [p for p in names(n, "Spawned By")[:1] if p in designs]
    for n, loop in loops(parent):
        problems.append((n, "Spawned By runs in a loop: " + " -> ".join(loop)))

    waits_on = {n: set() for n in designs}
    for n in designs:
        if status(n) not in FINISHED:
            for d in deps(n):
                waits_on[d].add(n)

    def behind(n, seen):
        for w in waits_on[n] - seen:
            seen.add(w)
            behind(w, seen)
        return seen

    def label(n):
        notes = [status(n)]
        if status(n) not in FINISHED and blocked_by(n):
            notes.append("blocked by " + "; ".join(blocked_by(n)))
        if status(n) not in FINISHED and landed(n):
            notes.append("to take in " + "; ".join(landed(n)))
        if status(n) in ("in-progress", "approved") and checked[n] != "none":
            notes.append("validated" if checked[n] == "validated" else "validation stale")
        return "%s [%s]" % (n, ", ".join(notes))

    children, drawn = {}, set()
    for n in designs:
        children.setdefault((parent(n) or [None])[0], []).append(n)
    lines = ["Workstack:"]

    def draw(n, depth, up):
        drawn.add(n)
        lines.append("%s%s%s" % ("  " * depth, label(n), ", blocks " + up if up and n in deps(up) and status(n) not in FINISHED else ""))
        for child in sorted(children.get(n, [])):
            if child not in drawn:
                draw(child, depth + 1, n)
    for n in sorted(children.get(None, [])):
        draw(n, 1, None)
    for n in sorted(designs):
        if n not in drawn:
            draw(n, 1, None)

    def action(n):
        s = status(n)
        if landed(n):
            return "revise"
        return {"not-started": "start", "in-progress": "design", "approved": "apply", "applying": "finish applying"}[s]
    ready = [n for n in designs if status(n) in STATES and status(n) not in FINISHED and not blocked_by(n)]
    ready.sort(key=lambda n: (-len(behind(n, set())), n))
    lines.append("Work next:")
    lines += ["  %s: %s, %d waiting on it" % (action(n), label(n), len(behind(n, set()))) for n in ready] or ["  none"]
    held = sorted(n for n in designs if status(n) in STATES and status(n) not in FINISHED and blocked_by(n))
    lines.append("Blocked, approved once what it depends on is approved, and applied once that finishes:")
    lines += ["  %s: %s" % ("revise" if landed(n) else "wait" if status(n) == "approved" else "design", label(n)) for n in held] or ["  none"]
    stale = sorted(n for n in designs if status(n) in FINISHED and not any(n in deps(m) for m in designs))
    lines.append("May be deleted:")
    lines += ["  " + n for n in stale] or ["  none"]
    return lines, problems

# `path/to/file.md § Parent § Child`. A span carrying no path is a same-file
# citation and is not checked here; see .ai/skills/design-specs/SKILL.md, Verifying a proposal. Its span opens with one backtick or more and closes
# on a run of as many, a run of another length inside it literal, as GitHub Flavored Markdown has a code span.
CITATION = re.compile(r'(?<!`)(?P<d>`+)(?!`)(?P<path>[\w./-]+\.md)\s+§\s+(?P<target>(?:[^`]|(?!(?P=d)(?!`))`+)+?)(?<!`)(?P=d)(?!`)')


def resolve(path, root):
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
    hits = sorted(
        p for p in root.rglob("*.md")
        if p.as_posix().endswith(tail) and ".ai/tmp" not in p.as_posix()
    )
    if len(hits) == 1:
        return hits[0], ""
    if not hits:
        return None, "no such file"
    names = ", ".join(h.relative_to(root).as_posix() for h in hits[:3])
    return None, "ambiguous shorthand, %d files match: %s" % (len(hits), names)


def check_citations(proposal, root):
    """-> [(ok, path, target, note)] for each cross-file citation, in order."""
    text = read(Path(proposal))
    seen, results = set(), []
    for m in CITATION.finditer(text):
        path, target = m.group("path"), " ".join(m.group("target").split())
        # a record citation's [...] selector names a record; only its section resolves here
        target = re.sub(r'\s+\[[^\]]*\]$', '', target)
        if (path, target) in seen:
            continue
        seen.add((path, target))

        target_file, note = resolve(path, root)
        if target_file is None:
            results.append((False, path, target, note))
            continue
        found = lineages(read(target_file))
        if target in found:
            results.append((True, path, target, ""))
            continue
        # A wrong ancestor is a different fix from a wrong title, so say which.
        leaf = target.split(" § ")[-1]
        near = [f for f in found if f.split(" § ")[-1] == leaf]
        note = f"right title, wrong lineage: {near[0]}" if near else "no such heading"
        results.append((False, path, target, note))
    return results


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


def design_problems(design):
    """The validation review's checks on one design: its form, its records and the references within it, drawing
    only on the document and the canon's declarations of its form, per working-files.md § A Design Document; by
    validating, no goal, no part of its frame and no step section not yet stated. Any problem a declaration reports
    counts, so a type that cannot be read stops a stamp."""
    name, fields, _, text = read_design(design)
    found = check_form(design)[1] + steer_table_problems(None)
    if dict(fields).get("Status") not in ("approved", "applying", "complete"):
        found += [(name, "its design frame's %s is not yet stated" % p) for p in FRAME if frame_parts(text).get(p) == NOT_YET_STATED]
        if (section(text, "Design Goals") or "").strip() == NOT_YET_STATED:
            found.append((name, "its design goals are not yet stated"))
        if (section(text, "Design Plan Steps") or "").strip() == NOT_YET_DRAFTED:
            found.append((name, "its steps are not yet drafted"))
    return found


def check_cited_headings(proposal):
    try:
        results = check_citations(proposal, Path.cwd())
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


def check_design(value):
    design = design_file(value)
    return 2 if design is None else report("check-design " + design.stem, design_problems(design))


def plans_folder(value, heading):
    """-> the plans directory, or an exit status: 2 for a directory given that is not
    there, 0 when the default is not there yet, since no design has been written."""
    folder = Path(value)
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
    name, fields, _, text = read_design(design)
    if validation(text, fields)[0] == "validated":
        print("== stamp-validation\nalready validated, the stamp current: %s\n" % dict(fields)["Validated"])
        return 0
    # every check but the stamp's own absence, which this is about to write; the design's place in the workstack is
    # --check-workstack's, which runs before each validation
    problems = [(t, p) for t, p in design_problems(design) if "validation review" not in p]
    if problems:
        report("stamp-validation, not stamped", problems)
        return 1
    raw = design.read_bytes().decode("utf-8")
    new, n = re.subn(r"^\*\*Validated:\*\*.*$", lambda m: "**Validated:** " + stamp(text), text, count=1, flags=re.M)
    if not n:
        print("== stamp-validation\nno Validated field to stamp\n")
        return 1
    design.write_bytes((new.replace("\n", "\r\n") if "\r\n" in raw else new).encode("utf-8"))
    print("== stamp-validation\n" + re.search(r"^\*\*Validated:\*\*.*$", new, re.M).group(0) + "\n")
    return 0


REFACTOR_AND_REFINE_PATHS = ("specs", ".ai/skills")  # the canon's specs and skills, and the application's specs


def refactor_and_refine_lines(text):
    """-> the lines of text a Refactor and Refine cycle carries, blank lines and bare markup set
    aside, and a heading read without its level, since a move raises or lowers it."""
    # a table's separator row, a code fence or a front matter fence carries no text of its own
    return [re.sub(r"^#+ ", "", l).strip() for l in text.replace("\r\n", "\n").split("\n")
            if l.strip() and not re.fullmatch(r"[|:\- ]+|```\w*", l.strip())]


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


# Actions are flags per specs/methodology/skills.md § Authoring a Skill.
# @canon-spec specs/methodology/sourcing-and-citation.md § Writing a Citation § A Citation's Link
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


# @canon-spec specs/methodology/working-files.md § Design Plan Step
# the constructs the drafting check reads whole, the ones a construct's own block decides
WHOLE = ("Decision Table", "State Machine")
OPENING_CITATION = re.compile(r"^\s*- `([^`§]+?) § ([^`]+)`[:.,]?\s*(.*)$")
LEFT_TO_THE_APPLY = ("left to the apply's self-review and the audit: a part a step changes, an Algorithm, a DAG or a "
                     "Constraint, and what a change brings in another file")


def repo_root():
    found = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True)
    return Path(found.stdout.strip()) if found.returncode == 0 else Path.cwd()


def objectives_stating_constructs(text):
    """-> [(step, design line of the Objective, its lines)] for each Objective of a Design Plan Step holding a
    **Construct:** field declaring one of WHOLE, its lines as written, the Objective's own and those indented under it."""
    lines, out = text.split("\n"), []
    start = next((i for i, l in enumerate(lines) if re.match(r"^## Design Plan Steps\s*$", l)), None)
    if start is None:
        return out
    step, i = None, start + 1
    while i < len(lines) and not lines[i].startswith("## "):
        m = re.match(r"^- \*\*Name:\*\* (.+?)\s*$", lines[i])
        if m:
            step = m.group(1)
        if step and re.match(r"^  - ", lines[i]):
            j = i + 1
            while j < len(lines) and (lines[j].startswith("    ") or not lines[j].strip()) and not lines[j].startswith("## "):
                j += 1
            item = lines[i:j]
            if any(l.strip().startswith("**Construct:**") and any(w in l for w in WHOLE) for l in item):
                out.append((step, i + 1, item))
            i = j
            continue
        i += 1
    return out


def kept_changes(root, design_text):
    """-> the paths the checkout holds changed against the last commit, where the design is not applying, so its
    reading is the last commit's, as working-files.md § A Design Document § The States It Moves Through § A Send-back
    has a reading made while kept changes stand; else none."""
    if re.search(r"^\*\*Status:\*\* applying\s*$", design_text, re.M):
        return []
    changed = subprocess.run(["git", "diff", "--name-only", "HEAD"], capture_output=True, text=True, cwd=root)
    added = subprocess.run(["git", "ls-files", "--others", "--exclude-standard"], capture_output=True, text=True, cwd=root)
    return [p for run in (changed, added) if run.returncode == 0 for p in run.stdout.split()]


def at_last_commit(root, text_of, paths):
    for p in paths:
        if not p.endswith(".md"):
            continue
        shown = subprocess.run(["git", "show", "HEAD:" + p], capture_output=True, text=True, encoding="utf-8", cwd=root)
        if shown.returncode == 0:
            text_of[p] = citation_links.strip(shown.stdout)
        else:
            text_of.pop(p, None)
    return text_of


def construct_block(item):
    """-> (path, lineage, the section's text) from an Objective's lines: its opening citation names the place, the rest
    of its first line opens the section as its description, and the lines under it are dedented as they will stand."""
    m = OPENING_CITATION.match(item[0])
    if not m:
        return None
    body = [l for l in item[1:]]
    indent = min((len(l) - len(l.lstrip()) for l in body if l.strip()), default=0)
    return m.group(1).strip(), m.group(2).strip(), [m.group(3).strip(), ""] + [l[indent:] for l in body]


def in_place(file_text, lineage, block):
    """-> (the file's text with the section holding block, the 0-based line block opens at): the named section's own
    text is replaced where it stands; a section the step adds opens at the end of its deepest ancestor there, or of
    the file, under each ancestor not there; a file it adds is empty."""
    parts = lineage.split(" § ")
    lines = file_text.split("\n") if file_text else ["# (a file the step adds)"]
    found = sections(file_text) if file_text else {}
    if lineage in found:
        h, end = found[lineage]
        return "\n".join(lines[:h + 1] + [""] + block + [""] + lines[end:]), h + 2
    k = len(parts) - 1
    while k and " § ".join(parts[:k]) not in found:
        k -= 1
    at = len(lines)
    if k:
        # the ancestor's whole subtree ends at the next heading of its level or above, fences aside
        h, inside = found[" § ".join(parts[:k])][0], False
        for n in range(h + 1, len(lines)):
            if lines[n].startswith("```"):
                inside = not inside
            elif not inside and re.match(r"^#{1,%d} " % (k + 1), lines[n]):
                at = n
                break
    opened = [l for d in range(k, len(parts)) for l in ("", "#" * (d + 2) + " " + parts[d], "")]
    return "\n".join(lines[:at] + opened + block + [""] + lines[at:]), at + len(opened)


def check_constructs(value):
    """--check-constructs: the construct checks a design's or a file's constructs take, read as the audit reads them;
    -> 1 where a finding is reported, else 0."""
    root, target = repo_root(), Path(value).resolve()
    try:
        rel = target.relative_to(root).as_posix()
    except ValueError:
        rel = None
    if not target.is_file() or rel is None:
        sys.stderr.write("no file in the repository: %s\n" % value)
        return 2
    text_of = spec_texts(root)
    is_design = rel.startswith(PLANS.rstrip("/") + "/")
    if not is_design and rel not in text_of:
        sys.stderr.write("neither a design in %s nor a file in scope: %s\n" % (PLANS, value))
        return 2
    print("== check-constructs " + rel)
    findings, candidates = [], []
    if is_design:
        design = read(target)
        text_of = at_last_commit(root, text_of, kept_changes(root, design))
        for step, at, item in objectives_stating_constructs(design):
            placed = construct_block(item)
            if not placed:
                findings.append((step, at, "working-files.md § Design Plan Step",
                                 "an Objective stating a construct whole opens with no citation of its section"))
                continue
            path, lineage, block = placed
            file_text, opens = in_place(text_of.get(path, ""), lineage, block)
            span = range(opens, opens + len(block))
            # the whole run, the cross-file checks among it, with the construct in its file; kept to its own lines
            found, _, cands = constructs.run_checks(dict(text_of, **{path: file_text}))
            at_line = lambda line: at + max(line - 1 - opens - 1, 0)
            findings += [(step, at_line(line), rule, msg) for rule, p, line, msg in found if p == path and line - 1 in span]
            candidates += [(step, at_line(line), name, context) for p, line, name, context in cands
                           if p == path and line - 1 in span]
        for step, line, rule, msg in findings:
            print("%s:%d  [%s]  %s\n  %s" % (rel, line, step, rule, msg))
        for step, line, name, context in candidates:
            print("candidate %s:%d  [%s]  %s\n  %s" % (rel, line, step, name, context))
    else:
        found, _, cands = constructs.run_checks(text_of)
        findings = [(rule, line, msg) for rule, path, line, msg in found if path == rel]
        candidates = [(line, name, context) for path, line, name, context in cands if path == rel]
        for rule, line, msg in sorted(findings, key=lambda f: f[1]):
            print("%s:%d  %s\n  %s" % (rel, line, rule, msg))
        for line, name, context in candidates:
            print("candidate %s:%d  [%s]\n  %s" % (rel, line, name, context))
    print("%d finding%s, %d candidate%s; %s\n" % (len(findings), "" if len(findings) == 1 else "s", len(candidates),
                                                  "" if len(candidates) == 1 else "s", LEFT_TO_THE_APPLY))
    return 1 if findings else 0


FLAGS = (
    ("--check-cited-headings", "PROPOSAL", check_cited_headings,
     "confirm every cross-file citation in the proposal points to a heading that exists"),
    ("--check-design-form", "DESIGN", check_design_form,
     "confirm a design document holds the form working-files.md sets"),
    ("--check-target-kind", "DESIGN", check_target_kind,
     "confirm every file a design document's Target names is of the kind its Kind field declares, and that it names no working file"),
    ("--check-design", "DESIGN", check_design,
     "run the validation review on one design document, writing no stamp: its form, its records and the references within it, drawing only on the document and the canon's declarations of its form; the builder runs it at validating before each adversarial round"),
    ("--check-workstack", "PLANS_DIR", check_workstack,
     "report what is out of sync in the workstack: a Status out of sync with what a design depends on, a Depends On naming no design, and a loop; the builder runs it before each validation; reads the skill's plans folder, and those beside it, unless given a directory"),
    ("--show-workstack", "PLANS_DIR", show_workstack,
     "draw the workstack and list what to work next, what is blocked and what may be deleted; reads the skill's plans folder, and those beside it, unless given a directory"),
    ("--show-validation", "DESIGN", show_validation,
     "print a design document's stamped hash, its hash now, and whether it is validated, stale or never stamped"),
    ("--stamp-validation", "DESIGN", stamp_validation,
     "run the validation review on one design document and, if it passes, write its validation stamp; the builder runs it at validating on the way to the user's approval"),
    ("--refresh-links", "ROOT", refresh_links,
     "write and refresh the link every citation in a file a person reads on GitHub carries, README.md, the files under docs/ and every spec but specs/AGENTS.md; the apply runs it once the text its steps call for is written; reads the repository holding the current directory unless given a root"),
    ("--check-constructs", "DESIGN_OR_FILE", check_constructs,
     "run the construct checks: on a design, a path in the skill's plans folder, each Decision Table or State Machine an Objective states whole, read in the section its opening citation names; on a spec file, the file's constructs as the audit checks them; candidates are listed apart; design-specs' builder runs it at drafting and on the applied files at its self-review, a code design stating no construct"),
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
        else:
            parser.add_argument(flag, metavar=metavar, action="append", help=help_text)
    args = vars(parser.parse_args(argv[1:]))
    chosen = [(run, value) for flag, _, run, _ in FLAGS for value in args[flag[2:].replace("-", "_")] or []]
    if not chosen:
        parser.print_usage(sys.stderr)
        return 2
    return max(run(value) for run, value in chosen)


if __name__ == "__main__":
    sys.stderr.write("run a skill's entry script, not this shared code: specs/methodology/skills.md § Authoring a Skill\n")
    sys.exit(2)
