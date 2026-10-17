#!/usr/bin/env python3
"""The design document tooling the skills writing design documents share: checks what a proposal
quotes and cites, holds design documents to their form, lists a design's edits, and shows what a
Refactor and Refine cycle changed.

A proposal that says "replace X with Y" is applicable only if X appears in the
target file, exactly, once, and only if every heading it cites exists; a design
document must hold the form working-files.md sets, and the workstack its lineage
draws must hold together. Its actions are flags per specs/methodology/skills.md
§ Authoring a Skill. The exit status is 0 when every check passes, 1 when one finds a problem, and 2 for a
usage error.

Standard library only, git aside, which --show-refactor-and-refine-of-existing-specs reads through, and run by no agent directly: each skill writing design documents calls
main from its own entry script with its own plans folder, per specs/methodology/skills.md
§ Authoring a Skill.

The manifest --check-quoted-text reads is plain text. A line beginning '--- ' names a file;
everything up to the next '--- ' is one anchor, verbatim, newlines included. Lines beginning
'#' before the first '--- ' are comments:

    --- specs/application/product/example-domain/example.md
    the exact text an edit replaces, as the file holds it
"""

import argparse
import datetime
import difflib
import hashlib
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


REGISTRY = "specs/methodology/skills.md"
# @canon-spec specs/methodology/working-files.md § A Design Document § The Kinds of Change
KINDS = ("canon-specs", "application-specs", "code", "documentation", "other")
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
SECTIONS = ("The Problem", "Design Goals", "The Design Frame", "Steering Decisions", "The Design", IMPACT, "The Builder's Passes", "Deliberately Left Alone")
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
# an edit's bold lead-in, naming the file it edits: the text it replaces then its replacement, or a new file
EDIT_LEAD = re.compile(r"^\*\*`([^`]+)`\.\*\* (This text|A new file):\s*$")
# @canon-spec specs/methodology/working-files.md § A Design Document
# a lead-in naming a file in backticks, however many, and one naming an edit's form however it ends
FILE_LEAD = re.compile(r"^\*\*`*([^`]*)")
LEAD_WORDS = re.compile(r"^\*\*`[^`]+`\.\*\* (This text|A new file)\b")
# @canon-spec specs/methodology/spec-style.md § Bold Lead-ins
# a bold phrase opening a line and closing on a period or a question mark
LEAD_IN = re.compile(r"^\*\*[^*]+[.?]\*\* ")
# @canon-spec specs/methodology/working-files.md § Steering Decision
# where the Steering Decision type is declared: its fields and its Type's values are read from that declaration,
# this tooling holding no copy of them
STEER_HOME = ("specs/methodology/working-files.md", "Steering Decision")
# @canon-spec specs/methodology/working-files.md § Design Goal
GOAL_HOME = ("specs/methodology/working-files.md", "Design Goal")


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
    text = (base / path).read_text(encoding="utf-8").replace("\r\n", "\n")
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


# working-files.md § A Design Document: an adversarial review's or post-apply audit's pass,
# its lead-in and what follows it to the next, names the model and effort it ran on.
# @canon-spec specs/methodology/working-files.md § A Design Document
REVIEW = re.compile(r"^\*\*(?:Adversarial review|Post-apply audit)\b", re.I)
# @canon-spec specs/methodology/working-files.md § A Design Document
REVIEW_FORM = re.compile(r"^\*\*(?:Adversarial review|Post-apply audit)\b")
# @canon-spec specs/AGENTS.md § Design, Refactor, Refine
# @canon-spec specs/methodology/working-files.md § A Design Document
RAN_ON = re.compile(r"\bon [^\s,;]+(?: [^\s,;]+)*? (?:at (?:light|medium|high) effort|as the agent allows)\b", re.I)
# @canon-spec specs/methodology/working-files.md § A Design Document § The States It Moves Through
STATES = ("not-started", "in-progress", "approved", "applying", "complete", "abandoned")
# @canon-spec specs/methodology/working-files.md § A Design Document
FINISHED = ("complete", "abandoned")
# A field's value runs to the next line opening with a field's key, or to a blank line.
KEY = r"\*\*([A-Z][A-Za-z ]*):\*\*"
ROOT_FIELD = re.compile(r"^" + KEY + r" ?(.*?)(?=\n[ \t-]*\*\*[A-Z][A-Za-z ]*:\*\*|\n\s*\n|\Z)", re.M | re.S)


def read_design(f):
    """-> (file name, [(key, value)], [level-two heading], text) for one design document;
    its fields are read from the Design Document section, before its first level-two heading."""
    text = f.read_text(encoding="utf-8").replace("\r\n", "\n")
    head = text.split("\n## ", 1)[0]
    fields = [(k, " ".join(v.split())) for k, v in ROOT_FIELD.findall(head)]
    return f.stem, fields, re.findall(r"^## (.+?)\s*$", text, re.M), text


def is_design(f):
    return f.read_text(encoding="utf-8").lstrip("\ufeff").startswith("# Design Document")


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
    """The Name in kebab-case: lower case, each run of other characters a hyphen."""
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
        # working-files.md § Design Goal: a Name in kebab-case, as a design document's file name is
        if kebab(name) != name:
            problems.append("a design goal's Name is not in kebab-case: " + name)
        if name in seen:
            problems.append("two design goals share the Name " + name)
        seen.add(name)
    return problems


def steer_table_problems(root):
    """-> problems with the Steering Decision and Design Goal types' declarations, which this tooling reads their
    records' fields from."""
    return steer_type(root)[2] + goal_type(root)[1]


def check_form(design):
    """-> (1, [(file name, problem)]): one design document against its form."""
    problems, designs = [], [read_design(design)]
    for name, fields, sections, text in designs:
        if not text.startswith("# Design Document\n"):
            problems.append((name, "it does not open with the heading Design Document"))
        keys, values = [k for k, _ in fields], dict(fields)
        if keys != list(FIELDS):
            problems.append((name, "its fields are %s, not %s" % (", ".join(keys), ", ".join(FIELDS))))
        if values.get("Name") and kebab(values["Name"]) != name:
            problems.append((name, "the file is not named for its Name: %s.md" % kebab(values["Name"])))
        if values.get("Status", "") not in STATES:
            problems.append((name, "Status is not a state: " + values.get("Status", "")))
        if not values.get("Name"):
            problems.append((name, "Name is empty"))
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
                problems.append((name, "a review's lead-in is not written as the form sets it, Adversarial review or Post-apply audit: " + p[:40].strip()))
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
        for p in edit_form_problems(text):
            problems.append((name, p))
        body = section(text, "Steering Decisions")
        for p in check_steers(body) if body is not None else []:
            problems.append((name, p))
        goals = section(text, "Design Goals")
        for p in check_goals(goals) if goals is not None else []:
            problems.append((name, p))
        if goals is not None and goals.strip() == NOT_YET_STATED and values.get("Status") in ("approved", "applying", "complete"):
            problems.append((name, values["Status"] + ", but its design goals are not yet stated"))
        # specs/AGENTS.md § Design, Refactor, Refine: the frame cites the goals it rests on by Names the design holds
        held = set(re.findall(r"^- \*\*Name:\*\* (.+?)\s*$", goals or "", re.M))
        cites = re.findall(r"`§ Design Goals \[Name: ([^\]]+)\]`", section(text, "The Design Frame") or "")
        for cited in sorted({c.strip() for c in cites} - held - {"…"}):
            problems.append((name, "a citation of a goal the design does not hold: " + cited))
    return len(designs), problems


# @canon-spec specs/methodology/working-files.md § A Design Document § The Kinds of Change
def kind_of(path, skills):
    """canon-specs, application-specs, or None for any other file."""
    if path in ("specs/AGENTS.md", "specs/architecture.md") or path.startswith("specs/methodology/"):
        return "canon-specs"
    if any(path.startswith(".ai/skills/" + n + "/") for n in skills + ["lib"]):
        return "canon-specs"
    if path.startswith("specs/application/"):
        return "application-specs"
    return None


def check_kind(design, root):
    """-> (1, [(file name, problem)]) where one design document's Target strays from its Kind."""
    reg = root / REGISTRY
    skills = re.findall(r"^\| `([a-z0-9-]+)` \|", reg.read_text(encoding="utf-8"), re.M) if reg.exists() else []
    if not skills:
        return 0, [(REGISTRY, "no registered skills read, so a skill's files cannot be classified")]
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
            problems.append((title, "Kind is not canon-specs, application-specs, code, documentation or other: " + value))
            continue
        if fields.get("Status") == "not-started" and target.lower() == "none":
            continue
        if not re.findall(r"`([^`]+)`", target):
            problems.append((title, "Target names no path"))
            continue
        for path in re.findall(r"`([^`]+)`", target):
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
# citation and is not checked here; see SKILL.md, Verifying a proposal. Its span opens with one backtick or more and closes
# on a run of as many, a run of another length inside it literal, as GitHub Flavored Markdown has a code span.
CITATION = re.compile(r'(?<!`)(?P<d>`+)(?!`)(?P<path>[\w./-]+\.md)\s+§\s+(?P<target>(?:[^`]|(?!(?P=d)(?!`))`+)+?)(?<!`)(?P=d)(?!`)')
SAME_FILE_CITATION = re.compile(r'(?<!`)`§\s+(?P<target>[^`]+)`(?!`)')


def lineages(text):
    """-> set of '§'-joined ancestor paths, one per heading.

    A level-1 heading is the file's own title rather than a section, so a lineage
    starts at level 2. Fenced blocks are blanked first: a heading shown inside an
    example is an illustration, not a section anything may cite.
    """
    live, inside = [], False
    for line in text.split("\n"):
        if line.startswith("```"):
            inside = not inside
            live.append("")
        else:
            live.append("" if inside else line)

    out, stack = set(), []
    for m in re.finditer(r'^(#{1,6})\s+(.*?)\s*$', "\n".join(live), re.M):
        lvl, title = len(m.group(1)), m.group(2)
        if lvl == 1:
            continue
        depth = lvl - 2
        stack = stack[:depth] + [None] * max(0, depth - len(stack)) + [title]
        out.add(" § ".join(t for t in stack if t))
    return out


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
    text = Path(proposal).read_text(encoding="utf-8")
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
        found = lineages(target_file.read_text(encoding="utf-8"))
        if target in found:
            results.append((True, path, target, ""))
            continue
        # A wrong ancestor is a different fix from a wrong title, so say which.
        leaf = target.split(" § ")[-1]
        near = [f for f in found if f.split(" § ")[-1] == leaf]
        note = f"right title, wrong lineage: {near[0]}" if near else "no such heading"
        results.append((False, path, target, note))
    return results


def collapse(text):
    """Whitespace-insensitive form, for reporting near-misses."""
    return " ".join(text.split())


def parse_manifest(text):
    """-> [(path, anchor)], in file order. Raises ValueError on a malformed manifest."""
    entries = []
    path = None
    buf = []
    seen_header = False

    for raw in text.splitlines():
        if raw.startswith("--- "):
            if path is not None:
                entries.append((path, "\n".join(buf).strip("\n")))
            path = raw[4:].strip()
            buf = []
            seen_header = True
            if not path:
                raise ValueError("a '--- ' line names no file")
        elif not seen_header:
            if raw.strip() and not raw.lstrip().startswith("#"):
                raise ValueError(
                    "content before the first '--- <file>' line: %r" % raw[:60]
                )
        else:
            buf.append(raw)

    if path is not None:
        entries.append((path, "\n".join(buf).strip("\n")))
    return entries


def check(path, anchor, root):
    """-> (status, detail). status is one of ok, missing, ambiguous, empty, no-file."""
    if not anchor:
        return "empty", "no anchor text given"

    target = (root / path).resolve()
    try:
        body = target.read_text(encoding="utf-8")
    except FileNotFoundError:
        return "no-file", "file does not exist"
    except OSError as exc:
        return "no-file", str(exc)

    n = body.count(anchor)
    if n == 1:
        return "ok", ""
    if n > 1:
        return "ambiguous", "%d matches; an edit against it is not deterministic" % n

    # Not found. Say why, since the cause changes the fix.
    if collapse(anchor) in collapse(body):
        return "missing", "matches only with whitespace collapsed; copy the exact text"
    head = collapse(anchor)[:40]
    if head and head in collapse(body):
        return "missing", "first 40 characters match; the anchor diverges after them"
    return "missing", "no match; check whether this text is in a different file"


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
    """Every check on one design: its form, its Target's kind, its quoted edits applying and its citations resolving
    while its edits are live, and what the workstack finds wrong with it. Any problem the form and kind checks report counts, whatever it
    is filed under, so a skills registry that cannot be read stops a stamp."""
    found = check_form(design)[1] + check_kind(design, Path.cwd())[1] + steer_table_problems(None)
    found += [(design.stem, p) for p in edit_apply_problems(design)] + [(design.stem, p) for p in citation_problems(design)]
    return found + [(t, p) for t, p in check_stack(design.parent)[1] if t == design.stem]


# @canon-spec specs/methodology/working-files.md § A Design Document
# the record's checks The edits and References, while the design's edits are yet to be written; once they are, the
# files are the record, and a direct edit after the apply is settled by Changes After Approval
EDITS_LIVE = ("in-progress", "approved")


def edit_apply_problems(design):
    """-> a problem for each quoted edit that neither applies to its file exactly once nor is already applied there,
    as --with-edits-of takes an edit already applied; an edit whose file lies under a folder the files at hand do not
    hold, as code in the copy --with-edits-of builds, is left to the run that holds it."""
    text = design.read_text(encoding="utf-8").replace("\r\n", "\n")
    if dict(read_design(design)[1]).get("Status") not in EDITS_LIVE:
        return []
    out = []
    for line, f, old, new in quoted(text):
        if old is None:
            continue
        target = Path.cwd() / f
        top = Path.cwd() / Path(f).parts[0]
        if not target.is_file() and len(Path(f).parts) > 1 and not top.exists():
            continue
        now = target.read_text(encoding="utf-8").replace("\r\n", "\n") if target.is_file() else ""
        if now.count(old) != 1 and not (new in now and (old in new or old not in now)):
            out.append("the edit at line %d does not apply to %s exactly once, nor is it already applied" % (line, f))
    return out


def edited(design_text, path):
    """-> the texts of the file at path as the design's own quoted edits leave it and as it stood before them, the
    files at hand holding either, as a run with --with-edits-of holds the edits applied."""
    target = Path.cwd() / path
    now = target.read_text(encoding="utf-8").replace("\r\n", "\n") if target.is_file() else None
    after, before = now, now
    for _, f, old, new in quoted(design_text):
        if f != path:
            continue
        if old is None:
            after = new
        else:
            if after is not None and after.count(old) == 1:
                after = after.replace(old, new)
            if before is not None and before.count(new) == 1:
                before = before.replace(new, old)
    return [t for t in (after, before) if t is not None]


def fenced(text, at):
    """-> whether a position in text lies inside a fenced code block, by the fences opened before its line."""
    return sum(1 for l in text[:at].split("\n")[:-1] if l.startswith("```")) % 2 == 1


def citation_problems(design):
    """-> a problem for each citation the design document holds, its steers and its passes aside, which tell history,
    that resolves neither in the files as they stand nor in its file as the design's own edits leave it, while its
    edits are live."""
    if dict(read_design(design)[1]).get("Status") not in EDITS_LIVE:
        return []
    text = design.read_text(encoding="utf-8").replace("\r\n", "\n")
    kept = text
    for title in ("Steering Decisions", "The Builder's Passes"):
        body = section(kept, title)
        if body:
            kept = kept.replace(body, "")
    with tempfile.NamedTemporaryFile("w", suffix=".md", delete=False, encoding="utf-8") as tmp:
        tmp.write(kept)
    try:
        results = check_citations(tmp.name, Path.cwd())
    except OSError:
        return []
    finally:
        Path(tmp.name).unlink()
    out = []
    for ok, path, target, _ in results:
        if ok:
            continue
        found, _ = resolve(path, Path.cwd())
        rel = found.relative_to(Path.cwd()).as_posix() if found else path
        if any(target in lineages(t) for t in edited(text, rel)):
            continue
        out.append("a citation does not resolve: %s § %s" % (path, target))
    # a citation within one file names no path, so it resolves in the file the edit quoting it changes; a fenced
    # example's citations name the example's own file, so they are left alone, the fence read from the file as the
    # edit leaves it, since a quote may open inside one
    for _, f, _, new in quoted(text):
        if not f.endswith(".md"):
            continue
        texts = edited(text, f)
        found = set().union(*map(lineages, texts))
        after = texts[0] if texts else new
        at = after.find(new) if after.count(new) == 1 else -1
        for m in SAME_FILE_CITATION.finditer(new):
            inside = fenced(after, at + m.start()) if at >= 0 else fenced(new, m.start())
            if inside:
                continue
            target = re.sub(r'\s+\[[^\]]*\]$', '', " ".join(m.group("target").split()))
            if target not in found:
                out.append("a citation does not resolve: %s § %s" % (f, target))
    return out


def check_quoted_text(source):
    if source == "-":
        text = sys.stdin.read()
    else:
        try:
            text = Path(source).read_text(encoding="utf-8")
        except OSError as exc:
            sys.stderr.write("cannot read manifest: %s\n" % exc)
            return 2
    try:
        entries = parse_manifest(text)
    except ValueError as exc:
        sys.stderr.write("malformed manifest: %s\n" % exc)
        return 2
    if not entries:
        sys.stderr.write("manifest contains no anchors\n")
        return 2
    print("== check-quoted-text")
    root, failed = Path.cwd(), 0
    width = max(len(p) for p, _ in entries)
    for path, anchor in entries:
        status, detail = check(path, anchor, root)
        if status != "ok":
            failed += 1
        line = "%-9s %-*s  %s" % (status, width, path, collapse(anchor)[:52] or "(empty)")
        if detail:
            line += "\n%s\\- %s" % (" " * 10, detail)
        print(line)
    print("%d anchor%s, %d failed\n" % (len(entries), "" if len(entries) == 1 else "s", failed))
    return 1 if failed else 0


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


def edits(text):
    """-> each edit of a design document's The Design, as (line, file, the words it removes, the words it adds),
    a new file adding every word it holds, its text read untruncated, its quote markers and fences set aside."""
    found = []
    for line, f, old, new in quoted(text):
        old_words, new_words = ([w for l in (s or "").splitlines() if not l.startswith("```") for w in l.split()] for s in (old, new))
        removed, added = [], []
        for tag, a1, a2, b1, b2 in difflib.SequenceMatcher(None, old_words, new_words, autojunk=False).get_opcodes():
            if tag in ("delete", "replace"):
                removed.append(" ".join(old_words[a1:a2]))
            if tag in ("insert", "replace"):
                added.append(" ".join(new_words[b1:b2]))
        found.append((line, f, removed, added))
    return found


def quoted(text):
    """-> each edit of a design document's The Design as it quotes it, (line, file, the text it replaces, its
    replacement), the text replaced None for a new file, its quote markers and fences set aside."""
    lines = text.split("\n")
    start = next((i for i, l in enumerate(lines) if l.rstrip() == "## The Design"), len(lines))
    end = next((i for i in range(start + 1, len(lines)) if lines[i].startswith("## ")), len(lines))
    out = []
    for i in range(start + 1, end):
        lead = EDIT_LEAD.match(lines[i])
        if lead:
            out.append([lead.group(1), lead.group(2) == "A new file", [], [], "old", i + 1])
        elif out and lines[i].rstrip() == "becomes:" and not out[-1][1]:
            out[-1][4] = "new"
        elif out and lines[i].startswith(">"):
            out[-1][3 if out[-1][1] or out[-1][4] == "new" else 2].append(re.sub(r"^>\s?", "", lines[i]))
        elif out and LEAD_IN.match(lines[i]):
            out.append([None, False, [], [], "old", i + 1])

    def body(quote, code):
        quote = list(quote)
        while quote and not quote[0].strip():
            quote.pop(0)
        while quote and not quote[-1].strip():
            quote.pop()
        if code and quote and quote[0].startswith("```") and quote[-1].startswith("```"):
            quote = quote[1:-1]
        return "\n".join(quote)
    return [(line, f, None if new_file else body(old, not f.endswith(".md")), body(new, not f.endswith(".md")))
            for f, new_file, old, new, _, line in out if f]


# @canon-spec specs/methodology/working-files.md § A Design Document
# a form the method is still adding: the checks run in a copy of the repository holding the edits of each design named
COPIED = ("specs", "docs", ".ai/skills", ".ai/plans")


def with_applied(withs, argv):
    """--with-edits-of: runs the other actions asked for in a copy of the repository, its root files, specs, skills and plans, holding the
    quoted edits of each design named, and copies back a design document a stamp wrote; -> the actions' exit status."""
    root = Path.cwd()
    copy = Path(tempfile.mkdtemp(prefix="design-specs-with-"))
    try:
        for d in COPIED:
            if (root / d).is_dir():
                shutil.copytree(root / d, copy / d, ignore=shutil.ignore_patterns("__pycache__"))
        for f in root.iterdir():
            if f.is_file():
                shutil.copy2(f, copy / f.name)
        for value in withs:
            design = design_file(value)
            if design is None:
                return 2
            for _, f, old, new in quoted(design.read_text(encoding="utf-8").replace("\r\n", "\n")):
                target = copy / f
                if old is None:
                    target.parent.mkdir(parents=True, exist_ok=True)
                    target.write_text(new + "\n", encoding="utf-8", newline="\n")
                    continue
                now = target.read_text(encoding="utf-8").replace("\r\n", "\n") if target.is_file() else ""
                # already applied, as while the design is applying: its replacement there and, unless the replacement
                # holds the text it replaces, that text gone
                if new in now and (old in new or old not in now):
                    continue
                if now.count(old) == 1:
                    target.write_text(now.replace(old, new), encoding="utf-8", newline="\n")
                else:
                    sys.stderr.write("--with-edits-of %s: an edit's text is not in %s exactly once, nor its replacement already there\n" % (value, f))
                    return 2
        rest, skip = [], False
        for a in argv[1:]:
            if skip:
                skip = False
            elif a == "--with-edits-of":
                skip = True
            elif not a.startswith("--with-edits-of="):
                flag, eq, value = a.partition("=")
                path = Path(value if eq else a)
                full = (path if path.is_absolute() else root / path).resolve()
                if not a.startswith("-") or eq:
                    under = full.relative_to(root.resolve()).parts if full.is_relative_to(root.resolve()) else ()
                    if full.exists() and any(under[:len(Path(d).parts)] == Path(d).parts for d in COPIED):
                        shown = full.relative_to(root.resolve()).as_posix()
                    elif full.exists():
                        shown = str(full)
                    else:
                        shown = value if eq else a
                    a = flag + "=" + shown if eq else shown
                rest.append(a)
        try:
            entry = Path(argv[0]).resolve().relative_to(root.resolve())
        except ValueError:
            sys.stderr.write("--with-edits-of: run the entry script from the repository's root\n")
            return 2
        stamped = [rest[i + 1] for i, a in enumerate(rest[:-1]) if a == "--stamp-validation"]
        stamped += [a.split("=", 1)[1] for a in rest if a.startswith("--stamp-validation=")]
        for value in stamped:
            if Path(value).is_absolute():
                sys.stderr.write("--with-edits-of: a design stamped lies outside the copied folders, so its stamp could not be copied back: %s\n" % value)
                return 2
        status = subprocess.run([sys.executable, str(copy / entry)] + rest, cwd=copy).returncode
        for value in stamped:
            mine, theirs = copy / value, root / value
            if mine.is_file() and theirs.is_file() and mine.read_bytes() != theirs.read_bytes():
                theirs.write_bytes(mine.read_bytes())
        return status
    finally:
        shutil.rmtree(copy, ignore_errors=True)


def show_edits(value):
    """Print every edit of a design document, for a reader to match what the design does against; decides nothing."""
    design = design_file(value)
    if design is None:
        return 2
    found = edits(read_design(design)[3])
    sys.stdout.reconfigure(encoding="utf-8")  # the quoted text's characters, whatever the console's code page
    print("== show-edits %s" % design.stem)
    for line, path, removed, added in found:
        print("%d %s" % (line, path))
        for words in removed:
            print("  - %s" % words)
        for words in added:
            print("  + %s" % words)
    print("%d edits" % len(found))
    return 0


def edit_form_problems(text):
    """working-files.md § A Design Document: each edit of The Design in a form that section gives,
    `This text:` then `becomes:`, or `A new file:`; an edit in another form is reported, as is a `This text:`
    with no `becomes:`, since the listing reads only those forms."""
    lines = (section(text, "The Design") or "").split("\n")
    out, fenced = [], False
    for i, line in enumerate(lines):
        if re.sub(r"^>\s?", "", line).startswith("```"):
            fenced = not fenced
            continue
        if fenced or not line.startswith("**`"):
            continue
        lead = EDIT_LEAD.match(line)
        rest = lines[i + 1:]
        if lead and lead.group(2) == "This text":
            end = next((j for j, l in enumerate(rest) if LEAD_IN.match(l)), len(rest))
            if "becomes:" not in (l.rstrip() for l in rest[:end]):
                out.append("an edit quoting the text it replaces with no becomes: " + FILE_LEAD.match(line).group(1))
        elif not lead and (LEAD_WORDS.match(line) or line.rstrip().endswith(":") and next((l for l in rest if l.strip()), "").startswith((">", "```"))):
            out.append("an edit in neither form, This text: then becomes:, or A new file: " + FILE_LEAD.match(line).group(1))
    return out


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
    # working-files.md § A Design Document: validated once each design its Depends On names is approved or applying
    others = {n: dict(f).get("Status", "") for n, f, _, _ in read_designs(design.parent)}
    depends = named(dict(fields).get("Depends On", ""))
    missing = [d for d in depends if d not in others]
    finished = [d for d in depends if others.get(d) in FINISHED]
    waiting = [d for d in depends if d in others and d not in finished and others[d] not in ("approved", "applying")]
    if missing or finished or waiting:
        print("== stamp-validation, not stamped\n" + "".join("its Depends On names no design document: %s\n" % d for d in missing) + "".join("its Depends On names %s, finished; take it in and remove it first\n" % d for d in finished) + "".join("its Depends On names %s, not approved; a design is validated once each design it names is approved or applying\n" % d for d in waiting))
        return 1
    if validation(text, fields)[0] == "validated":
        print("== stamp-validation\nalready validated, the stamp current: %s\n" % dict(fields)["Validated"])
        return 0
    # every check but the stamp's own absence, which this is about to write
    problems = [(t, p) for t, p in design_problems(design) if "validation review" not in p]
    # working-files.md § A Design Document: no design approved or further holds a part of its frame not yet stated
    if dict(fields).get("Status") not in ("approved", "applying", "complete"):
        problems += [(name, "its design frame's %s is not yet stated" % p) for p in FRAME
                     if frame_parts(text).get(p) == NOT_YET_STATED]
        if (section(text, "Design Goals") or "").strip() == NOT_YET_STATED:
            problems.append((name, "its design goals are not yet stated"))
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
    # a table's separator row, a code fence or a frontmatter fence carries no text of its own
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
    now, where = count((f, Path(f).read_text(encoding="utf-8")) for f in now_files if Path(f).is_file())
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
FLAGS = (
    ("--check-quoted-text", "MANIFEST", check_quoted_text,
     "confirm each text the manifest quotes appears exactly once in the file it names; - reads the manifest from stdin"),
    ("--check-cited-headings", "PROPOSAL", check_cited_headings,
     "confirm every cross-file citation in the proposal points to a heading that exists"),
    ("--check-design-form", "DESIGN", check_design_form,
     "confirm a design document holds the form working-files.md sets"),
    ("--check-target-kind", "DESIGN", check_target_kind,
     "confirm every file a design document's Target names is of the kind its Kind field declares"),
    ("--check-design", "DESIGN", check_design,
     "run every check on one design document: its form, its Target's kind, its quoted edits applying, its citations resolving, and its place in the workstack"),
    ("--check-workstack", "PLANS_DIR", check_workstack,
     "report what is out of sync in the workstack: a Status out of sync with what a design depends on, a Depends On naming no design, and a loop; reads the skill's plans folder, and those beside it, unless given a directory"),
    ("--show-workstack", "PLANS_DIR", show_workstack,
     "draw the workstack and list what to work next, what is blocked and what may be deleted; reads the skill's plans folder, and those beside it, unless given a directory"),
    ("--show-validation", "DESIGN", show_validation,
     "print a design document's stamped hash, its hash now, and whether it is validated, stale or never stamped"),
    ("--stamp-validation", "DESIGN", stamp_validation,
     "run every check on one design document and, if it passes, write its validation stamp; the builder runs it at validating"),
    ("--show-edits", "DESIGN", show_edits,
     "list every edit a design document quotes in the forms working-files.md § A Design Document gives, untruncated: its line, the file it edits, and the words it removes and adds; decides nothing"),
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
        else:
            parser.add_argument(flag, metavar=metavar, action="append", help=help_text)
    parser.add_argument("--with-edits-of", metavar="DESIGN", action="append", help="run the other actions with the edits of this design document applied, in a copy of the repository, for a record using a form a design changing the method adds; given more than once, each design's edits applied in turn")
    args = vars(parser.parse_args(argv[1:]))
    if args["with_edits_of"]:
        return with_applied(args["with_edits_of"], argv)
    chosen = [(run, value) for flag, _, run, _ in FLAGS for value in args[flag[2:].replace("-", "_")] or []]
    if not chosen:
        parser.print_usage(sys.stderr)
        return 2
    return max(run(value) for run, value in chosen)


if __name__ == "__main__":
    sys.stderr.write("run a skill's entry script, not this shared code: specs/methodology/skills.md § Authoring a Skill\n")
    sys.exit(2)
