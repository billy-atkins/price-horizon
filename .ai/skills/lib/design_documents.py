#!/usr/bin/env python3
"""The design document tooling the skills writing design documents share: the validation review, which holds a
design document to its form, drawing only on the document and the canon's declarations of its form, and stamps a
design that passes; and the builder's tools, which append a design's log entries, check the headings a proposal
cites, a Target against its Kind and the constructs a design or a file states, through the construct checks in
constructs.py, for its self-review, show and check the wording a design retires, list the files changed outside
its Target, check the work against the specs' and the code's script checks in spec_checks.py and code_checks.py, check
the workstack, show a validation, write citations' links, and show what a
Refactor and Refine cycle changed. A check's entry is appended only once its report, in the design's folder, holds the
form working-files.md § A Check's Report gives it and its records cover what that section has the design script check
of them, its counts taken from it; a reviewer's part of a review's report is checked by the same units before its
settlement.

A design document must hold the form working-files.md sets, and the workstack its lineage draws must hold
together. Its actions are flags per specs/methodology/skills.md § Authoring a Skill. The exit status is 0 when
every check passes, 1 when one finds a problem, and 2 for a usage error.

Standard library only, git aside, which --show-refactor-and-refine-of-existing-specs and --check-work read through, and run by
no agent directly: each skill writing design documents calls main from its own entry script with its own plans
folder, per specs/methodology/skills.md § Authoring a Skill.
"""

import argparse
import bisect
import collections
import contextlib
import datetime
import hashlib
import io
import json
import re
import subprocess
import sys
from pathlib import Path

import citation_links
import constructs
import layout
import record_types
from spec_text import REGISTRY, lineages, parse_citation, read, registry, scope_paths, sections, skill_dirs, spec_texts
from spec_text import strip_fences, tracked
from spec_text import resolve as resolve_citation


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
# @canon-spec specs/methodology/working-files.md § A Stamp
TIMESTAMP = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$")
# @canon-spec specs/methodology/working-files.md § A Design Document
# a design validated by hand, its record using a form the methodology is still adding
BY_HAND = "by hand"
# @canon-spec specs/methodology/working-files.md § A Design Document
# @canon-spec specs/methodology/working-files.md § A Stamp
UNSTAMPED = ("Validated", "Status")
# @canon-spec specs/methodology/working-files.md § A Design Document
LOG = "Design Log Entries"
# @canon-spec specs/methodology/working-files.md § A Stamp
UNSTAMPED_SECTIONS = (LOG,)  # an entry appended after the stamp leaves it current
# @canon-spec specs/methodology/working-files.md § A Design Document
IMPACT = "Impact on the Application Specs"  # a canon design's, and no other design's
# @canon-spec specs/methodology/working-files.md § A Design Document
RETIRED = "Retired Phrases"
# @canon-spec specs/methodology/working-files.md § A Design Document
SECTIONS = ("The Problem", "Design Goals", "The Design Frame", "Steering Decisions", "Design Plan Steps", RETIRED, IMPACT, LOG, "Out of Scope")
# @canon-spec specs/methodology/working-files.md § A Design Document
# the log is required once its first entry is appended, so a design with none holds no section
OPTIONAL = ("Steering Decisions", RETIRED, LOG)
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
# @canon-spec specs/methodology/working-files.md § Design Log Entry
LOG_HOME = ("specs/methodology/working-files.md", "Design Log Entry")
# @canon-spec specs/methodology/working-files.md § Retired Phrase
RETIRED_HOME = ("specs/methodology/working-files.md", "Retired Phrase")


def declaration(home, root=None):
    """-> (the text of the section declaring a type, or None, and the file's path)."""
    path, title = home
    # the checkout's root: the one given, or the nearest directory up from this file, or else from where it runs,
    # holding the declaration's file
    here = Path(__file__).resolve()
    base = Path(root) if root else next((p for p in (*here.parents, Path.cwd(), *Path.cwd().parents) if (p / path).exists()), Path.cwd())
    if not (base / path).exists():
        return None, path
    return section(read((base / path)).replace("\r\n", "\n"), title) or "", path


def declared_type(home, plural, root=None, key="Name"):
    """A record type as its declaration gives it -> (its table of record fields, a row to a field, problems with the
    declaration: no Record Form, a Plural Name other than the one a design's record section takes, a Reference Key
    other than the one given, or no table of its record fields)."""
    title = home[1]
    body, path = declaration(home, root)
    if body is None:
        return [], [(path, "no file declares the %s type" % title)]
    lines = [re.sub(r"\s*\\$", "", l).strip() for l in body.split("\n")]
    problems = [] if "**Construct:** `specs/methodology/modeling-constructs.md § Constructs § Record Form`" in lines \
        else ["no Record Form declares the %s type" % title]
    if "**Plural Name:** " + plural not in lines:
        problems.append("the %s type declares no Plural Name %s, the title a design's record section takes" % (title, plural))
    if "**Reference Key:** " + key not in lines:
        problems.append("the %s type declares no Reference Key %s" % (title, key))
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


def retired_type(root=None):
    """The Retired Phrase type as its declaration gives it -> (its fields in order, the fields it requires,
    problems with the declaration)."""
    rows, problems = declared_type(RETIRED_HOME, RETIRED, root, key="Phrase")
    return tuple(row[0] for row in rows), tuple(row[0] for row in rows if len(row) > 2 and row[2] == "yes"), problems


# a record's own fields, a design's header and every field's value are read through the one reader of a block of
# fields, record_types.read_block, wherever the form indents them (modeling-constructs.md § Fields)


def records_read(body):
    """-> the items of a section's Records field as the one reader gives them, wherever the form indents the key, or
    None where the section has no Records field (modeling-constructs.md § Fields)."""
    if body is None:
        return None
    lines = body.split("\n")
    i = next((i for i, l in enumerate(lines) if record_types.opens_key(l) and record_types.opens_key(l)["key"] == "Records"), None)
    if i is None:
        return None
    fields, _ = record_types.read_block(lines, i, record_types._indent(lines[i]), len(lines))
    field = next((f for f in fields if f["key"] == "Records"), None)
    return list(field["items"] or []) if field is not None else None


def records(body):
    """-> each record of a record section as [(field, value)], or None where it has no Records field; an item opening
    no field is a record of no fields."""
    items = records_read(body)
    if items is None:
        return None
    return [[(f["key"], str(record_types.value_of(f))) for f in it["fields"]] if it["fields"] is not None else [] for it in items]


# @canon-spec specs/methodology/working-files.md § A Design Document § The States It Moves Through
STATES = ("not-started", "in-progress", "approved", "applying", "complete", "abandoned")
# @canon-spec specs/methodology/working-files.md § A Design Document § The States It Moves Through
# the states its Trigger Classes table makes a design finish in
FINISHED = ("complete", "abandoned")
KEY = r"\*\*([A-Z][A-Za-z ]*):\*\*"


def read_design(f):
    """-> (file name, [(key, value)], [level-two heading], text) for one design document;
    its fields are read from the Design Document section, before its first level-two heading, as one block of fields
    through the one reader."""
    text = read(f).replace("\r\n", "\n")
    head = text.split("\n## ", 1)[0].split("\n")
    i = next((i for i, l in enumerate(head) if record_types.opens_key(l) and not record_types._indent(l)), None)
    fields = []
    if i is not None:
        block, _ = record_types.read_block(head, i, 0, len(head))
        fields = [(f["key"], " ".join(str(record_types.value_of(f)).split())) for f in block]
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


def content_hash(text, leave_out=UNSTAMPED, leave_out_sections=UNSTAMPED_SECTIONS):
    """working-files.md § A Stamp: SHA-256 of the text as UTF-8, line endings a line feed,
    the lines holding the left-out fields dropped, and each left-out section, its heading through the next heading
    of its level; its first 16 hexadecimal characters."""
    keys = "|".join(re.escape(k) for k in leave_out)
    lines, dropping = [], False
    for l in text.replace("\r\n", "\n").split("\n"):
        if l.startswith("## "):
            dropping = l[3:].strip() in leave_out_sections
        if not dropping and not re.match(r"\*\*(?:%s):\*\*" % keys, l):
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
    items = records_read(body)
    if items is None:
        return ["Steering Decisions has no Records field"]
    if not items:
        return ["Steering Decisions holds no record"]
    problems, seen = [], set()
    fields, types, declared = steer_type()
    if not fields:
        return [p for _, p in declared] or ["the Steering Decision type declares no fields"]
    for it in items:
        keys = [f["key"] for f in it["fields"] or []]
        if keys != list(fields):
            problems.append("a steering decision's fields are %s, not %s" % (", ".join(keys), ", ".join(fields)))
            continue
        values = {f["key"]: str(record_types.value_of(f)).strip() for f in it["fields"]}
        name, type_ = values["Name"], values.get("Type", "")
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
        keys = [f["key"] for f in it["fields"] or []]
        if keys != list(fields):
            problems.append("a design goal's fields are %s, not %s" % (", ".join(keys), ", ".join(fields)))
            continue
        name = str(record_types.value_of(it["fields"][0])).strip()
        # working-files.md § Design Goal: a Name in kebab-case, as a design document's Name is
        if kebab(name) != name:
            problems.append("a design goal's Name is not in kebab-case: " + name)
        if name in seen:
            problems.append("two design goals share the Name " + name)
        seen.add(name)
    return problems



def check_steps(body):
    """-> problems with a Design Plan Steps section: `Not yet drafted.`, or a Records field and each record its type's
    fields in order, Objectives a list and the last field, its Name a slug, no two sharing a Name, each Why citing a
    goal, which check_form holds to the goals the design holds, and each step a step cites one the section holds."""
    if body.strip() == NOT_YET_DRAFTED:
        return []
    items = records_read(body)
    if items is None:
        return ["Design Plan Steps has no Records field"]
    if not items:
        return ["Design Plan Steps holds no record"]
    fields, declared = step_type()
    if not fields:
        return [p for _, p in declared] or ["the Design Plan Step type declares no fields"]
    problems, seen = [], set()
    for it in items:
        keys = [f["key"] for f in it["fields"] or []]
        if keys != list(fields):
            problems.append("a design plan step's fields are %s, not %s" % (", ".join(keys), ", ".join(fields)))
            continue
        name = str(record_types.value_of(it["fields"][0])).strip()
        # working-files.md § Design Plan Step: a Name in kebab-case, as a design document's Name is
        if kebab(name) != name:
            problems.append("a design plan step's Name is not in kebab-case: " + name)
        if name in seen:
            problems.append("two design plan steps share the Name " + name)
        seen.add(name)
        # the last field, Objectives, a list: its key on a line of its own and its items beneath
        last = it["fields"][-1]
        if last["inline"] or not last["items"]:
            problems.append("design plan step %s's %s is not a list" % (name, fields[-1]))
        why = next((f for f in it["fields"] if f["key"] == "Why"), None)
        cited = re.findall(r"`§ Design Goals \[Name: ([^\]]+)\]`", str(record_types.value_of(why)) if why else "")
        if not cited:
            problems.append("design plan step %s's Why cites no goal" % name)
    for step in sorted({c.strip() for c in re.findall(r"`§ Design Plan Steps \[Name: ([^\]]+)\]`", body)} - seen - {"…"}):
        problems.append("a citation of a step the design does not hold: " + step)
    return problems



def entry_problems(kind, fields, values, counts, kinds):
    """-> problems with one log entry's kind and its fields beside Entry and Timestamp, [(field, value)]: a kind the
    table does not give, its fields other than the kind gives, in the type's order, and a value outside its field's
    Values, a count not a whole number, or an empty value."""
    if kind not in kinds:
        return ["a log entry's kind is not one of %s: %s" % (", ".join(kinds), kind)]
    keys, an = [k for k, _ in fields], "an" if kind[0] in "aeiou" else "a"
    if keys != list(kinds[kind]):
        return ["%s %s entry's fields are %s, not %s" % (an, kind, ", ".join(keys) or "none", ", ".join(kinds[kind]) or "none")]
    problems = []
    for k, v in fields:
        if not v:
            problems.append("%s %s entry's %s is empty" % (an, kind, k))
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
        problems += ["log entry %s: %s" % (entry, p) for p in entry_problems(kind, [(k, v.strip()) for k, v in fields[2:]], values, counts, kinds)]
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
            problems.append("a retired phrase's fields are %s, not %s" % (", ".join(keys), ", ".join(fields)))
            continue
        phrase = record[0][1].strip()
        if phrase.lower() in seen:
            problems.append("two retired phrases share the Phrase " + phrase)
        seen.add(phrase.lower())
    return problems


def steer_table_problems(root):
    """-> problems with the Steering Decision, Design Goal, Design Plan Step, Design Log Entry and Retired Phrase
    types' declarations, which this tooling reads their records' fields from."""
    return steer_type(root)[2] + goal_type(root)[1] + step_type(root)[1] + log_type(root)[3] + retired_type(root)[2]


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
        if validated.lower() not in ("none", BY_HAND) and not STAMP.match(validated):
            problems.append((name, "Validated is neither none, %s nor a stamp: %s" % (BY_HAND, validated)))
        elif validated == BY_HAND:
            pass
        elif values.get("Status") == "approved" and not STAMP.match(validated):
            problems.append((name, "approved, but no validation review has stamped it"))
        elif values.get("Status") == "approved" and validated.split(" ")[1] != content_hash(text):
            problems.append((name, "approved, but edited since its validation review stamped it"))
        elif values.get("Status") in ("applying", "complete") and not STAMP.match(validated):
            problems.append((name, values["Status"] + ", but no validation review stamped it"))
        for p in check_log(section(text, LOG)) if section(text, LOG) is not None else []:
            problems.append((name, p))
        for p in check_retired(section(text, RETIRED)) if section(text, RETIRED) is not None else []:
            problems.append((name, p))
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
        # specs/AGENTS.md § Design, Refactor, Refine § The Goals and the Frame and specs/methodology/working-files.md § Design Plan Step: the frame and the steps cite the goals they rest on by Names the
        # design holds
        held = {dict(rec).get("Name", "").strip() for rec in records(goals) or []}
        steps = section(text, "Design Plan Steps")
        cites = re.findall(r"`§ Design Goals \[Name: ([^\]]+)\]`", (section(text, "The Design Frame") or "") + (steps or ""))
        for cited in sorted({c.strip() for c in cites} - held - {"…"}):
            problems.append((name, "a citation of a goal the design does not hold: " + cited))
        for p in check_steps(steps) if steps is not None else []:
            problems.append((name, p))
        if steps is not None and steps.strip() == NOT_YET_DRAFTED and values.get("Status") in ("approved", "applying", "complete"):
            problems.append((name, values["Status"] + ", but its steps are not yet drafted"))
        # modeling-constructs.md § Fields and spec-style.md § Blank Lines: the design's layout, each block of fields and
        # each list a field holds by the reader's checks, and each blank line by the layout check
        base = Path(design).resolve().parents[3]
        table, table_problems = layout.rules(base if (base / layout.HOME).is_file() else repo_root())
        problems += [(name, msg) for _, _, _, msg in table_problems]
        problems += [(name, "line %d: %s" % (line, msg)) for _, line, msg in layout.findings(text, table) + record_types.block_findings(text)]
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
    new, n = re.subn(r"^\*\*Validated:\*\*.*$", lambda m: "**Validated:** " + stamp(text) + (" \\" if m.group(0).rstrip().endswith("\\") else ""), text, count=1, flags=re.M)
    if not n:
        print("== stamp-validation\nno Validated field to stamp\n")
        return 1
    write_design(design, raw, new)
    print("== stamp-validation\n" + re.search(r"^\*\*Validated:\*\*.*$", new, re.M).group(0) + "\n")
    return 0


def write_design(design, raw, new):
    """Write a design's new text, keeping the line endings its file had."""
    design.write_bytes((new.replace("\n", "\r\n") if "\r\n" in raw else new).encode("utf-8"))


# @canon-spec specs/methodology/working-files.md § Design Log Entry
# @canon-spec specs/methodology/working-files.md § Design Log Entry § Script Checks [Name: counts-taken-from-the-report]
def append_entry(value):
    """--append-entry DESIGN KIND [FIELD=VALUE ...]: appends an entry to the design's log, its count among its kind and
    the UTC time it is appended, refusing one out of its type; a check's entry only once its report stands in the
    design's folder, in its form and its records covering what its check had to cover, its counts taken from the
    report; -> 0, 1 where it is refused, 2 for a usage error."""
    if len(value) < 2:
        sys.stderr.write("--append-entry takes a design document, a kind and the kind's fields as FIELD=VALUE\n")
        return 2
    design = design_file(value[0])
    if design is None:
        return 2
    kind, pairs = value[1], value[2:]
    if any("=" not in p for p in pairs):
        sys.stderr.write("--append-entry: each field is given as FIELD=VALUE\n")
        return 2
    fields = [tuple(s.strip() for s in p.split("=", 1)) for p in pairs]
    values, counts, kinds, declared = log_type()
    if declared or kind not in kinds:
        return report("append-entry, not appended", [(design.stem, p) for p in
                                                     [p for _, p in declared] + entry_problems(kind, fields, values, counts, kinds)])
    given = [k for k, _ in fields if counts.get(k)]
    if given:
        return report("append-entry, not appended", [(COUNT_RULE, "a count given, which is taken from the check's report "
                                                      "alone: " + ", ".join(given))])
    raw = design.read_bytes().decode("utf-8")
    text = raw.replace("\r\n", "\n")
    body = section(text, LOG)
    count = 1 + len(re.findall(r"^\s*- \*\*Entry:\*\* %s-\d+(?: \\)?\s*$" % re.escape(kind), body or "", re.M))
    # a check's entry, one holding a Model, names its report, which stands in the design's folder before the entry does
    if "Model" in kinds[kind]:
        root = repo_root()
        report_path = report_file(design, kind, count)
        if not report_path.is_file():
            return report("append-entry, not appended", [(design.stem, "a check's entry whose report does not stand in "
                                                          "the design's folder: " + rel_to(report_path, root))])
        # a self-review's Script Output, which a report the work moved past holds none of
        if kind == "self-review" and not moved_past(read_report(read(report_path))):
            write_script_output(report_path, self_review_output(root, design, text))
        problems, found = entry_report_problems(root, design, text, kind, count)
        if problems:
            return report("append-entry, not appended", problems)
        taken = report_counts(found)
        # the kind's fields in the type's order, each count the report's; a field the kind does not give kept, so it
        # is refused as one out of its type
        fields = [(k, str(taken[k])) if counts.get(k) else (k, dict(fields)[k]) for k in kinds[kind]
                  if counts.get(k) or k in dict(fields)] + [(k, v) for k, v in fields if k not in kinds[kind]]
    problems = entry_problems(kind, fields, values, counts, kinds)
    if problems:
        return report("append-entry, not appended", [(design.stem, p) for p in problems])
    now = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    # modeling-constructs.md § Fields: the entry a record, an item two spaces beyond its key, each line a line opening
    # a field's key follows ending with a space and a backslash
    own = ["- **Entry:** %s-%d" % (kind, count), "  **Timestamp:** " + now] + ["  **%s:** %s" % f for f in fields]
    block = "\n".join("  " + l + (" \\" if n < len(own) - 1 else "") for n, l in enumerate(own))
    if body is not None and not re.search(r"^\*\*Records:\*\*\s*$", body, re.M):
        # a section copied from the form holds its placeholder alone, which the first entry replaces
        m = re.search(r"^## %s\s*$" % re.escape(LOG), text, re.M)
        text = text[:m.start()] + text[m.end() + len(body):].lstrip("\n")
        body = None
    if body is None:
        # the section stands where the form puts it, before the sections that follow it
        after = SECTIONS[SECTIONS.index(LOG) + 1:]
        m = next((m for m in (re.search(r"^## %s\s*$" % re.escape(s), text, re.M) for s in after) if m), None)
        at = m.start() if m else len(text.rstrip("\n")) + 1
        new = text[:at] + "## %s\n\n**Records:**\n%s\n\n" % (LOG, block) + text[at:]
    else:
        m = re.search(r"^## %s\s*$" % re.escape(LOG), text, re.M)
        end = m.end() + len(body)
        new = text[:m.end()] + body.rstrip("\n") + "\n\n" + block + "\n" + ("\n" if end < len(text) else "") + text[end:]
    write_design(design, raw, new)
    print("== append-entry\n" + block + "\n")
    return 0


# ---------------------------------------------------------------- a check's report

WF = "specs/methodology/working-files.md"
# @canon-spec specs/methodology/working-files.md § A Check's Report
# where a report's form is declared: its parts are read from that declaration and its record types through the one
# reader of the record types the specs declare
REPORT_HOME = (WF, "A Check's Report")
FORM_RULE = WF + " § A Check's Report"
COUNT_RULE = WF + " § Design Log Entry"
FIELDS_RULE = "specs/methodology/modeling-constructs.md § Fields"
BLANK_LINES_RULE = "specs/methodology/spec-style.md § Blank Lines"
# @canon-spec specs/methodology/working-files.md § A Check's Report
REPORT_TITLE = "# Check's Report"
TITLE_FIELDS = ("Design", "Entry")
REVIEWS = ("adversarial-review", "post-apply-review")
JUDGMENT = "handed-off-judgment"
# the Reading's field, a review's and every other report's; the Settlement's fields, in their order; and what the
# checks read of a report whose Settlement holds Moved Past, its records and its Settlement's fields, alone
REVIEW_READING, OWN_READING = "Reviewer Readings", "Reads"
SETTLEMENT_FIELDS = ("Earlier Reports", "Settling Reads", "Moved Past", "Settlements")
MOVED_PAST_RECORDS = ("Findings", REVIEW_READING)
MOVED_PAST_FIELDS = ("Earlier Reports", "Moved Past")
# the parts a reviewer writes, and the parts holding records, each by its type's Plural Name
REVIEWER_PARTS = ("Reading", "Findings", "Searches")
RECORD_PARTS = ("Findings", "Searches", "Traces", "Builder Checks", "Causes")
# @canon-spec specs/methodology/working-files.md § A Check's Report § Verdicts
MARKS = ("design flaw", "implementation flaw", "nit")
FLAWS = MARKS[:2]
# @canon-spec specs/methodology/working-files.md § Design Log Entry
# each count of a check's entry, by the last word in its report it counts
COUNTED = {"Design Flaws": "design flaw", "Implementation Flaws": "implementation flaw", "Nits": "nit", "Dropped": "dropped"}
# @canon-spec specs/methodology/working-files.md § A Check's Report
# the fields holding places, by the Plural Name of the type giving them or the part holding them; the one holding a
# single place, and those holding `none` where they hold no place
PLACE_FIELDS = {"Reading": ("Reads",), "Settlement": ("Earlier Reports", "Settling Reads"),
                "Reviewer Readings": ("Collecting Reads", "Earlier Reports", "Weighing Reads"),
                "Findings": ("Affected Parts", "Broken Rules"), "Report Evidence Items": ("Places",),
                "Searches": ("Places",), "Builder Checks": ("Places Checked",), "Causes": ("Conflicting Steers",),
                "Misses": ("Place", "Reads"), "Proposed Changes": ("Places",)}
ONE_PLACE = {("Misses", "Place")}
NONE_HELD = {("Reading", "Reads"), ("Settlement", "Earlier Reports"), ("Settlement", "Settling Reads"),
             ("Reviewer Readings", "Collecting Reads"),
             ("Reviewer Readings", "Earlier Reports"), ("Reviewer Readings", "Weighing Reads"), ("Searches", "Places")}
# @canon-spec specs/methodology/working-files.md § A Check's Report § Kinds of Builder Check
# the checks every self-review requires, and those it requires for each item its phase gives
EVERY_SELF_REVIEW = ("steers against the user's messages", "linked work", "review's questions")
USER_EDIT, WORKED_CASE, MISS_QUESTION, DIFFERENTIAL = "user edit", "worked case", "miss's question", "differential test"
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


def canon_rule(rule):
    """-> a rule the shared readers name by its file's name alone, cited with its path."""
    return rule if rule.startswith("specs/") else "specs/methodology/" + rule


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
    its title is one written before the form, read as holding no records."""
    text = text.replace("\r\n", "\n")
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


def place_of(text):
    """-> (path, lineage or None, selector or None) for one citation with its path, as
    specs/methodology/sourcing-and-citation.md § Writing a Citation writes one, alone in its text; else None."""
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


# @canon-spec specs/methodology/working-files.md § A Check's Report
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


# @canon-spec specs/methodology/working-files.md § A Check's Report § Script Checks [Name: places-in-their-form]
def places_problems(rep, types):
    """-> [(rule, message)]: each value holding places in a report out of the form § A Check's Report gives it, a list
    of citations with their paths, one to an item, or one such citation alone; `none` where its field holds it."""
    out = []

    def check(where, owner, key, value):
        items = [l.strip() for l in str(value).split("\n") if l.strip()]
        if items == ["none"] and (owner, key) in NONE_HELD:
            return
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
                    check("line %d, a record of %s" % (line + 1, plural), plural, key, value)
    for plural, recs in held_records(rep).items():
        walk(plural, recs)
    for part, fields in rep["blocks"].items():
        for f in fields:
            if f["key"] in PLACE_FIELDS.get(part, ()):
                check("line %d, the %s part" % (f["line"] + 1, part), part, f["key"], record_types.value_of(f))
    return [(FORM_RULE, p) for p in out]


def settled_findings(settlement):
    """-> the keys of the Findings a Settlement settles, one to an item of its Settled Findings."""
    return [k.strip().strip("`").strip() for k in settlement.get("Settled Findings", "").split("\n") if k.strip()]


def last_words(rep):
    """-> {a Finding's key: its last word in the report}: the Verdict of the Settlement settling it, else its own."""
    out = {f.get("Finding", ""): f.get("Verdict", "") for f in rep["records"]["Findings"]}
    for s in rep["settlements"]:
        for k in settled_findings(s):
            if k in out:
                out[k] = s.get("Verdict", "")
    return out


def moved_past(rep):
    return any(f["key"] == "Moved Past" for f in rep["blocks"].get("Settlement", []))


def held_records(rep):
    """-> {plural: records as the one reader gives them} the checks read: of a report whose Settlement holds Moved Past,
    its Findings and its Reading's alone."""
    return {p: r for p, r in rep["raw"].items() if not moved_past(rep) or p in MOVED_PAST_RECORDS}


# @canon-spec specs/methodology/working-files.md § Design Log Entry § Script Checks [Name: counts-taken-from-the-report]
def report_counts(rep):
    """-> each count of a check's entry from its report, each Finding counted once by its last word."""
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


# @canon-spec specs/methodology/working-files.md § A Check's Report § Script Checks [Name: report-in-its-form]
def form_problems(rep, ctx, types, parts):
    """-> [(rule, message)]: a report out of the form § A Check's Report gives it: its title, its parts in their order
    and those its kind and its settling require, its Reading's and its Settlement's fields, and each record of the type
    its part or field cites, with each field its conditions require and no other; of a report whose Settlement holds
    Moved Past, no Causes and no Settlement record, and its Reading, its Findings and its Settlement alone; and
    ctx["reviewer"] holds the reviewer's part alone to the form."""
    import spec_checks
    if not rep["in_form"]:
        return [(FORM_RULE, "the report does not open with its title, %s" % REPORT_TITLE)]
    out = [(canon_rule(rule), "line %d: %s" % (line, msg)) for rule, line, msg in rep["problems"]]
    reviewer, kind, review, rule = ctx["reviewer"], ctx["kind"], ctx["kind"] in REVIEWS, ctx["rule"]
    # its title
    title = rep["title"]
    if list(title) != list(TITLE_FIELDS):
        out.append((FORM_RULE, "its title's fields are %s, not %s" % (", ".join(title) or "none", ", ".join(TITLE_FIELDS))))
    for key, want in (("Design", ctx["design"]), ("Entry", ctx["entry"])):
        if key in title and title[key][0] != want:
            out.append((FORM_RULE, "its title's %s is %s, not %s" % (key, title[key][0], want)))
    # its parts, in their order, each once, those required, and, where it was moved past, no other
    order = [p for p, _, _, _ in parts]
    held = [p for p, _ in rep["parts"]]
    out += [(FORM_RULE, "a part the form does not give: " + p) for p in held if p not in order]
    known = [p for p in held if p in order]
    if known != sorted(known, key=order.index) or len(set(known)) != len(known):
        out.append((FORM_RULE, "its parts are %s, not in the order the form gives them, each once" % ", ".join(known)))
    moved, recs = moved_past(rep), rep["records"]
    settlements = rep["settlements"] + ctx["judgment_settlements"]
    required = {"Reading"} if reviewer else {"Reading", "Settlement"}
    if not reviewer and not moved:
        if kind == "self-review":
            required.add("Script Output")
        if review and any(s.get("Verdict") in MARKS for s in settlements):
            required.add("Causes")
    for p in sorted(required - set(held), key=order.index):
        out.append((rule(p), "it holds no %s part, which its form requires of it" % p))
    if moved and "Causes" in held:
        out.append((rule("Causes"), "it holds a Causes part, though its Settlement holds Moved Past"))
    # its Reading's field, and its Settlement's fields, in their order
    keys = [f["key"] for f in rep["blocks"].get("Reading", [])]
    want = [REVIEW_READING if review else OWN_READING]
    if "Reading" in held and keys != want:
        out.append((rule("Reading"), "its Reading's fields are %s, not %s" % (", ".join(keys) or "none", want[0])))
    cond = []
    if "Settlement" in held and not reviewer:
        keys = [f["key"] for f in rep["blocks"].get("Settlement", [])]
        if keys != [k for k in SETTLEMENT_FIELDS if k in keys] or any(k not in SETTLEMENT_FIELDS for k in keys):
            out.append((rule("Settlement"), "its Settlement's fields are %s, not of %s in that order"
                        % (", ".join(keys) or "none", ", ".join(SETTLEMENT_FIELDS))))
        has = dict.fromkeys(keys)
        require(cond, "its Settlement", has, "Earlier Reports", True, "always")
        if moved:
            cond += ["its Settlement holds %s, though it holds Moved Past" % k for k in keys if k not in MOVED_PAST_FIELDS]
        else:
            require(cond, "its Settlement", has, "Settling Reads", review, "where the report is a review's and its round is settled")
            require(cond, "its Settlement", has, "Settlements", bool(recs["Findings"]), "where the report holds a Finding")
    out += [(rule("Settlement"), c) for c in cond]
    # each record of its type, a part's or a field's, its required fields and its values
    found, raw = [], held_records(rep)
    for plural in RECORD_PARTS + (REVIEW_READING, "Settlements"):
        if reviewer and plural not in REVIEWER_PARTS + (REVIEW_READING,):
            continue
        if plural in raw and plural in types:
            spec_checks._check_records(raw[plural], types[plural], WF, "the report", lambda i: i + 1, found, "its %s" % plural)
    out += [(canon_rule(r), "line %d: %s" % (line, msg)) for r, _, line, msg in found]
    # each field its conditions require, and no other
    cond = []
    for f in recs["Findings"]:
        where, mark = "line %d, Finding %s" % (f["_line"] + 1, f.get("Finding", "")), f.get("Verdict") in MARKS
        for key in ("Decision", "Possible Fix"):
            require(cond, where, f, key, mark, "where its Verdict is a mark")
        require(cond, where, f, "Affected Parts", mark and "Broken Rules" not in f, "where its Verdict is a mark and it holds no Broken Rules")
        require(cond, where, f, "Broken Rules", mark and "Affected Parts" not in f, "where its Verdict is a mark and it holds no Affected Parts")
        require(cond, where, f, "Evidence", f.get("Verdict") != "review observation", "where its Verdict is not a review observation")
        require(cond, where, f, "Lies In", mark and ctx["applied"], "where its Verdict is a mark and the report lies over applied work")
        for fix in f.get("Possible Fix") or []:
            if isinstance(fix, dict):
                require(cond, where + "'s Possible Fix", fix, "Fix", fix.get("Kind") == "tactical fix", "where its Kind is tactical fix")
                require(cond, where + "'s Possible Fix", fix, "Delivers", fix.get("Kind") == "revision", "where its Kind is revision")
    out += [(rule("Findings"), c) for c in cond]
    if reviewer or moved:
        return out
    cond = []
    for t in recs["Traces"]:
        require(cond, "line %d, Trace %s" % (t["_line"] + 1, t.get("Trace", "")), t, "Outcome", ctx["trace_outcome"],
                "where the report is a self-review's before the apply, and no plan-approval entry of the phase stands "
                "before it but one an another-round entry follows")
    out += [(rule("Traces"), c) for c in cond]
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
        # a judgment's Settlement cites the round's Cause where it is settled with a round, checked at the round's entry
        if kind != JUDGMENT or "Cause" not in s:
            require(cond, where, s, "Cause", mark and "Causes" in held, "where the report holds Causes and its Verdict is a mark")
    causes = {c.get("Cause") for c in recs["Causes"]}
    cond += ["a handed-off judgment's Settlement %s, settled with the round, cites no Cause of its report by the report "
             "and the Cause's key" % s.get("Settlement", "") for s in ctx["judgment_settlements"]
             if s.get("Verdict") in MARKS and not (place_of(s.get("Cause", "")) and cause_key(s["Cause"], ctx["report_rel"]) in causes)]
    out += [(rule("Settlement"), c) for c in cond]
    return out


# @canon-spec specs/methodology/working-files.md § A Check's Report § Script Checks [Name: report-laid-out]
def layout_problems(rep, root):
    """-> [(rule, message)]: the report laid out otherwise than modeling-constructs.md § Fields and spec-style.md
    § Blank Lines have a block of fields laid out."""
    found = record_types.block_findings(rep["text"]) + layout.findings(rep["text"], layout.rules(root)[0])
    return [(FIELDS_RULE if "Fields" in rule else BLANK_LINES_RULE, "line %d: %s" % (line, msg)) for rule, line, msg in found]


# @canon-spec specs/methodology/working-files.md § A Check's Report § Script Checks [Name: findings-settled-once]
def settled_problems(rep, ctx):
    """-> [(rule, message)]: a Finding settled by no Settlement, or by more than one, but in a report whose Settlement
    holds Moved Past."""
    if moved_past(rep):
        return []
    times = collections.Counter(k for s in rep["settlements"] for k in settled_findings(s))
    return [(ctx["rule"]("Settlement"), "Finding %s is settled by %d Settlements, not exactly one" % (f.get("Finding", ""), times[f.get("Finding", "")]))
            for f in rep["records"]["Findings"] if times[f.get("Finding", "")] != 1]


# @canon-spec specs/methodology/working-files.md § A Check's Report § Script Checks [Name: report-keys-name-records]
def key_problems(rep, ctx, named):
    """-> [(rule, message)]: a key the report cites naming no record a report the design's log names holds, this report
    among them: a Finding a Settlement settles, the Cause it lies in and the Search a Proposed Change cites, each by its
    key alone in this report; and each record a citation of a report in the design's folder names, the Cause a Cause
    continues or a Settlement weighs again by such a citation; none in a report whose Settlement holds Moved Past."""
    recs, out = rep["records"], []
    if moved_past(rep):
        return out
    keys = lambda part, field: {r.get(field) for r in recs[part]}
    settling, causing = ctx["rule"]("Settlement"), ctx["rule"]("Causes")
    for s in rep["settlements"]:
        where = "Settlement %s" % s.get("Settlement", "")
        out += [(settling, "%s settles %s, which no Finding of the report is" % (where, k))
                for k in settled_findings(s) if k not in keys("Findings", "Finding")]
        if "Cause" in s and place_of(s["Cause"]) is None and s["Cause"] not in keys("Causes", "Cause"):
            out.append((settling, "%s names a Cause the report does not hold: %s" % (where, s["Cause"])))
        if "Weighs Again" in s and place_of(s["Weighs Again"]) is None:
            out.append((settling, "%s weighs again a Cause not cited with its report: %s" % (where, s["Weighs Again"])))
    for c in recs["Causes"]:
        if "Continues" in c and place_of(c["Continues"]) is None:
            out.append((causing, "Cause %s continues a Cause not cited with its report: %s" % (c.get("Cause", ""), c["Continues"])))
        for change in c.get("Proposed Change") or []:
            if isinstance(change, dict) and "Search" in change and change["Search"] not in keys("Searches", "Search"):
                out.append((causing, "Cause %s's Proposed Change cites a Search the report does not hold: %s" % (c.get("Cause", ""), change["Search"])))
    reports = dict(named, **{ctx["report_rel"]: rep})
    for place in cited_places(strip_fences(rep["text"])):
        path, part, selector = place
        if not path.startswith(ctx["folder"]) or not part or not selector or ": " not in selector:
            continue
        key, value = selector.split(": ", 1)
        held = reports.get(path)
        if held is None:
            out.append((FORM_RULE, "it cites %s, in a report the design's log does not name" % cite(place)))
        elif not any(r.get(key) == value for r in (held["settlements"] if part == "Settlement" else held["records"].get(part, []))):
            out.append((FORM_RULE, "it cites %s, a record that report does not hold" % cite(place)))
    return out


def text_at(root, path, kept):
    """-> a file's text as a search reads it: at the last commit where a send-back's kept changes stand, as
    working-files.md § A Design Document § The States It Moves Through § A Send-back has a reading made, else as it
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
    lines = design_text.split("\n")
    start = next((i for i, l in enumerate(lines) if re.match(r"^## Design Plan Steps\s*$", l)), None)
    if start is None:
        return {}
    end = next((i for i in range(start + 1, len(lines)) if lines[i].startswith("## ")), len(lines))
    out = {}
    for step in records_read("\n".join(lines[start:end])) or []:
        if step["fields"]:
            name = str(record_types.value_of(step["fields"][0])).strip()
            out.update({start + n: name for n in step["lines"]})
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


# @canon-spec specs/methodology/working-files.md § A Design Document § The Kinds of Change
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


# @canon-spec specs/methodology/working-files.md § A Check's Report
def search_ground(root, design_rel, design_text, target, kept):
    """-> a function giving a Search's ground as {path: text}, read once: the design document and the files of each
    kind of those its Target names, with, for canon-specs, every file of Spec of Record's scope but code, and, for
    application-specs, the code; the working files aside."""
    held = {}

    def ground():
        if not held:
            import code_checks
            skills, code = skill_dirs(root), code_checks.code_roots(root) or ([], [])
            kind = lambda p: file_kind(p, skills, code)
            kinds = {kind(p) for p in target}
            scope = set(scope_files(root)) if "canon-specs" in kinds else set()
            for path in sorted(tracked(root, others=True) or scope_files(root)):
                k = kind(path)
                if k in kinds or (path in scope and k != "code") or ("application-specs" in kinds and k == "code"):
                    text = text_at(root, path, kept)
                    if text is not None:
                        held[path] = text
            held[design_rel] = design_text
        return held
    return ground


# @canon-spec specs/methodology/working-files.md § A Check's Report § Script Checks [Name: searches-cover-their-matches]
def search_problems(rep, ctx):
    """-> [(rule, message)]: each match of a Search's Pattern, run again over its ground, in a place its Places do not
    cover; none in a report whose Settlement holds Moved Past. A reviewer's Search, its key naming its Reviewer Reading
    before it, is run again by --check-report alone, before the round's change is made."""
    out = []
    reviewers = tuple(as_record(r).get("Reviewer", "") + "-" for r in rep["raw"].get(REVIEW_READING, []) if r and r[0][0] is not None)
    for s in rep["records"]["Searches"] if not moved_past(rep) else []:
        if not ctx["reviewer"] and s.get("Search", "").startswith(tuple(r for r in reviewers if r != "-")):
            continue
        pattern = s.get("Pattern", "")
        pattern = pattern[1:-1] if len(pattern) > 1 and pattern[0] == pattern[-1] == "`" else pattern
        try:
            compiled = re.compile(pattern)
        except re.error as exc:
            out.append("Search %s's Pattern is no regular expression Python's re reads: %s" % (s.get("Search", ""), exc))
            continue
        listed, missed = place_list(s.get("Places", "")), []
        for path, text in ctx["ground"]().items():
            place_at = line_places(path, text, ctx["steps"] if path == ctx["design_rel"] else None)
            starts = [0] + [m.end() for m in re.finditer("\n", text)]
            for m in compiled.finditer(text):
                if m.end() == m.start():
                    continue
                place = place_at(bisect.bisect_right(starts, m.start()) - 1)
                if not covered(listed, place) and place not in missed:
                    missed.append(place)
        out += ["Search %s's Pattern matches in %s, which its Places do not cover" % (s.get("Search", ""), cite(p)) for p in missed]
    return [(ctx["rule"]("Searches"), p) for p in out]


def log_entries(text):
    """-> each entry of a design's log as (kind, count, {field: value}), in the order the entries stand."""
    out = []
    for record in records(section(text, LOG)) or []:
        f = {k: v.strip() for k, v in record}
        m = re.fullmatch(r"([a-z-]+?)-(\d+)", f.get("Entry", ""))
        if m:
            out.append((m.group(1), int(m.group(2)), f))
    return out


# @canon-spec specs/methodology/working-files.md § A Check's Report
def over_applied(entries):
    """Whether an entry appended after these lies over applied work: after the design's last apply entry, with no
    entered entry after that."""
    applies = [i for i, e in enumerate(entries) if e[0] == "apply"]
    return bool(applies) and not any(e[0] == "entered" for e in entries[applies[-1] + 1:])


# @canon-spec specs/methodology/working-files.md § A Check's Report
def phase_start(entries, applied):
    """-> where the phase an entry appended after these stands in starts: a post-apply review's after the design's last
    apply entry, and an adversarial review's after its last reassessment entry deciding other than go on or its last
    entered entry sent back, whichever stands later, or at the log's start."""
    if applied:
        return max(i for i, e in enumerate(entries) if e[0] == "apply") + 1
    return max([i + 1 for i, (k, _, f) in enumerate(entries)
                if (k == "reassessment" and f.get("Decision") != "go on") or (k == "entered" and f.get("Reason") == "sent back")],
               default=0)


def phase_record(design, entries, applied, root):
    """-> [(path, report)] for each report of the phase's record, its review entries' and its handed-off judgments'."""
    review = REVIEWS[1] if applied else REVIEWS[0]
    return [(rel_to(report_file(design, k, n), root), load_report(design, k, n))
            for k, n, _ in entries[phase_start(entries, applied):] if k in (review, JUDGMENT)]


def load_report(design, kind, n):
    path = report_file(design, kind, n)
    return read_report(read(path)) if path.is_file() else read_report("")


def named_reports(design, entries, root):
    """-> {path: report} for each report a check's entry of the design's log names."""
    kinds = log_type()[2]
    return {rel_to(report_file(design, k, n), root): load_report(design, k, n)
            for k, n, _ in entries if "Model" in kinds.get(k, ())}


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


def traced_constructs(ctx):
    """-> [(the places citing it, construct, its paths)] for each Decision Table and State Machine a self-review's phase
    traces: before the apply, each a step's Objectives state whole, cited by the step or its section; at it, each a
    section the diff changed holds."""
    if ctx["applied"]:
        text_of = spec_texts(ctx["root"])
        return [([place], name, paths) for path, lines in sorted(ctx["changes"].items()) if path in text_of
                for place, name, paths in constructs_in(path, text_of[path], lines)]
    out = []
    for step, _, item in objectives_stating_constructs(ctx["design_text"]):
        placed = construct_block(item)
        if placed:
            path, lineage, block = placed
            for _, name, fields, tables, _ in constructs.declarations("\n".join(block), {}):
                if name in WHOLE:
                    out.append(([(ctx["design_rel"], "Design Plan Steps", "Name: " + step), (path, lineage, None)],
                                name, constructs.paths(name, fields, tables)))
    return out


def path_name(text):
    return re.sub(r"\s*,\s*", ", ", re.sub(r"\s+", " ", text.replace("`", ""))).strip()


def required_checks(ctx):
    """-> [(Builder Check kind, the places its Places Checked must cover)] for each Builder Check a self-review's phase
    requires, as § A Check's Report § Kinds of Builder Check gives it."""
    entries, out = ctx["entries"], [(k, []) for k in EVERY_SELF_REVIEW]
    last = max((i for i, e in enumerate(entries) if e[0] == "self-review"), default=-1)
    # an edit's place read as a citation, a part a keyed instance holds among them
    out += [(USER_EDIT, [p for p in (place_of("`%s`" % " § ".join(x for x in ps if x)) for ps in places(f.get("Places", ""))) if p])
            for k, _, f in entries[last + 1:] if k == "user-edit"]
    if ctx["round"]:
        path, rep = ctx["round"]
        worked = [(path, "Causes", "Cause: " + c.get("Cause", "")) for c in rep["records"]["Causes"] if c.get("Proposed Change")]
        worked += [(path, "Findings", "Finding: " + k) for k, w in last_words(rep).items() if w == "implementation flaw"]
        asked = [(p, "Causes", "Cause: " + c.get("Cause", "")) for p, r in ctx["record"] for c in r["records"]["Causes"]
                 if any(isinstance(m, dict) and m.get("Kind") == "question not asked" for m in c.get("Misses") or [])]
        out += [(k, items) for k, items in ((WORKED_CASE, worked), (MISS_QUESTION, asked)) if items]
    if ctx["applied"]:
        import code_checks
        skills, code = skill_dirs(ctx["root"]), code_checks.code_roots(ctx["root"]) or ([], [])
        # the code the specs govern is no script, its tests checking it
        scripts = [(p, None, None) for p in sorted(ctx["changes"]) if p.endswith(SCRIPTS) and file_kind(p, skills, code) != "code"]
        out += [(DIFFERENTIAL, scripts)] if scripts else []
    return out


# @canon-spec specs/methodology/working-files.md § A Check's Report § Script Checks [Name: traces-name-their-paths]
def trace_problems(rep, ctx):
    """-> [(rule, message)]: a construct a self-review's phase traces with no Trace, or a Trace leaving out a path."""
    out, rule = [], ctx["rule"]
    for mechanisms, name, paths in traced_constructs(ctx):
        traced = [t for t in rep["records"]["Traces"] if set(cited_places(t.get("Mechanism", ""))) & set(mechanisms)]
        if not traced:
            out.append((rule("Traces"), "no Trace of the %s at %s" % (name, cite(mechanisms[-1]))))
            continue
        done = {path_name(p.get("Path", "")) for t in traced for p in t.get("Paths") or [] if isinstance(p, dict)}
        # a row named by all its cells names its condition cells first
        out += [(rule("Traces"), "the Trace of the %s at %s leaves out a path: %s" % (name, cite(mechanisms[-1]), p))
                for p in paths if not any(d == path_name(p) or d.startswith(path_name(p) + ", ") for d in done)]
    return out


# @canon-spec specs/methodology/working-files.md § A Check's Report § Script Checks [Name: builder-checks-required]
def builder_check_problems(rep, ctx):
    """-> [(rule, message)]: a Builder Check a self-review's phase requires missing, or not covering its items."""
    out, rule = [], ctx["rule"]
    for check, items in required_checks(ctx):
        made = [b for b in rep["records"]["Builder Checks"] if b.get("Kind") == check]
        if not made:
            out.append((rule("Builder Checks"), "no Builder Check of %s, which its phase requires" % check))
            continue
        checked = [p for b in made for p in place_list(b.get("Places Checked", ""))]
        out += [(rule("Builder Checks"), "its Builder Checks of %s leave out %s" % (check, cite(p)))
                for p in items if not covered(checked, p)]
    return out


# @canon-spec specs/methodology/working-files.md § A Check's Report § Script Checks [Name: reads-cover-the-misses]
def miss_read_problems(rep, ctx):
    """-> [(rule, message)]: a place a Miss of the phase names that the Reads of a self-review following a round's
    change leave out."""
    if not ctx["round"]:
        return []
    reads = place_list(next((record_types.value_of(f) for f in rep["blocks"].get("Reading", []) if f["key"] == OWN_READING), ""))
    missed = [place_of(m.get("Place", "")) for _, r in ctx["record"] for c in r["records"]["Causes"]
              for m in c.get("Misses") or [] if isinstance(m, dict)]
    return [(ctx["rule"]("Reading"), "its Reads leave out %s, a place a Miss of the phase names" % cite(p))
            for p in sorted(set(p for p in missed if p), key=place_key) if not covered(reads, p)]


def settlement_block(rep):
    return {f["key"]: record_types.value_of(f) for f in rep["blocks"].get("Settlement", [])}


# @canon-spec specs/methodology/working-files.md § A Check's Report § Script Checks [Name: earlier-reports-listed]
def earlier_report_problems(rep, ctx):
    """-> [(rule, message)]: a report of the phase's record a round's Earlier Reports leave out."""
    earlier = place_list(settlement_block(rep).get("Earlier Reports", ""))
    return [(ctx["rule"]("Settlement"), "its Earlier Reports leave out `%s`, a report of the phase's record" % p)
            for p, _ in ctx["record"] if not covered(earlier, (p, None, None))]


# @canon-spec specs/methodology/working-files.md § A Check's Report § Script Checks [Name: settling-reads-cover-the-evidence]
def settling_read_problems(rep, ctx):
    """-> [(rule, message)]: a place the Evidence of a marked Finding names that a round's Settling Reads leave out."""
    reads = place_list(settlement_block(rep).get("Settling Reads", ""))
    evidence = {p for f in rep["records"]["Findings"] if f.get("Verdict") in MARKS for ev in f.get("Evidence") or []
                if isinstance(ev, dict) for p in place_list(ev.get("Places", ""))}
    return [(ctx["rule"]("Settlement"), "its Settling Reads leave out %s, a place the Evidence of a marked Finding names" % cite(p))
            for p in sorted(evidence, key=place_key) if not covered(reads, p)]


# @canon-spec specs/methodology/working-files.md § A Check's Report § Script Checks [Name: tactical-fixes-cover-their-searches]
def tactical_fix_problems(rep, ctx):
    """-> [(rule, message)]: a place a tactical fix's Search found that its Places leave out."""
    out, searches = [], {s.get("Search"): s for s in rep["records"]["Searches"]}
    for c in rep["records"]["Causes"]:
        for change in c.get("Proposed Change") or []:
            if isinstance(change, dict) and change.get("Kind") == "tactical fix" and change.get("Search") in searches:
                wrote = place_list(change.get("Places", ""))
                out += [(ctx["rule"]("Causes"), "Cause %s's tactical fix leaves out %s, a place its Search found" % (c.get("Cause"), cite(p)))
                        for p in place_list(searches[change["Search"]].get("Places", "")) if not covered(wrote, p)]
    return out


def cover_problems(rep, ctx):
    """-> [(rule, message)]: what a self-review's records or a round's settlement leave uncovered of what § A Check's
    Report has the design script check of them, by the unit of each record; nothing of a report whose Settlement holds
    Moved Past."""
    if moved_past(rep) or ctx["kind"] not in REVIEWS + ("self-review",):
        return []
    units = ((trace_problems, builder_check_problems, miss_read_problems) if ctx["kind"] == "self-review"
             else (earlier_report_problems, settling_read_problems, tactical_fix_problems))
    return [p for unit in units for p in unit(rep, ctx)]


def report_context(root, design, design_text, kind, n, entries, reviewer=False):
    """-> what a report's checks read of its design and its log: its kind and entry, the design's Name, whether it lies
    over applied work, whether its Traces give their Outcome, the Settlements of the judgments settled with a round, a Search's ground, the phase's record, the round whose change a
    self-review follows, the diff's changes over applied work, and the rules each part's Holds cites."""
    applied = over_applied(entries)
    start = phase_start(entries, applied)
    approvals = [i for i, e in enumerate(entries) if i >= start and e[0] == "plan-approval"
                 and not any(x[0] == "another-round" for x in entries[i + 1:])]
    kept = [] if applied else kept_changes(root, design_text)
    fields = dict(read_design(design)[1])
    path = report_file(design, kind, n)
    commit = last_commit(root) if applied and kind == "self-review" and not reviewer else None
    rules = {p: ", ".join(r) or FORM_RULE for p, _, _, r in report_parts(root)}
    return {"root": root, "kind": kind, "entry": "%s-%d" % (kind, n), "design": fields.get("Name", design.stem),
            "applied": applied, "reviewer": reviewer, "entries": entries, "design_rel": rel_to(design, root),
            "design_text": design_text, "steps": step_lines(design_text), "report_rel": rel_to(path, root),
            "folder": rel_to(path.parents[1], root) + "/",
            "trace_outcome": kind == "self-review" and not applied and not approvals,
            "judgment_settlements": judgment_settlements(design, entries) if kind in REVIEWS and not reviewer else [],
            "ground": search_ground(root, rel_to(design, root), design_text,
                                    re.findall(r"`([^`]+)`", fields.get("Target", "")), kept),
            "record": phase_record(design, entries, applied, root) if not reviewer else [],
            "round": round_change_followed(design, entries, applied, root) if kind == "self-review" else None,
            "changes": work_changes(root, commit)[0] if commit else {},
            "rule": lambda part: rules.get(part, FORM_RULE)}


def entry_report_problems(root, design, design_text, kind, n):
    """-> ([(rule, message)] refusing a check's entry, the report read): the report held to its form and its layout,
    each value holding places in its form, each Finding settled once, each key naming a record, each Search's matches
    covered, and its records covering what its check had to cover."""
    entries = log_entries(design_text)
    path = report_file(design, kind, n)
    rep = read_report(read(path))
    ctx = report_context(root, design, design_text, kind, n, entries)
    problems = form_problems(rep, ctx, report_types(root), report_parts(root))
    if rep["in_form"]:
        problems += layout_problems(rep, root) + places_problems(rep, report_types(root)) + settled_problems(rep, ctx)
        problems += key_problems(rep, ctx, named_reports(design, entries, root)) + search_problems(rep, ctx)
        problems += cover_problems(rep, ctx)
    return [(rule, "%s: %s" % (ctx["report_rel"], msg)) for rule, msg in problems], rep


def self_review_output(root, design, design_text):
    """-> the output of the design script's checks the self-review runs for its phase: before the apply,
    --check-cited-headings, --check-target-kind, --check-constructs on a design .ai/skills/design-specs/ writes, and
    --show-reach where it records Retired Phrases; at the apply, --check-constructs on each file of the Target holding a
    construct the diff changed, --check-work, --check-retired-wording and --check-changed-files."""
    value = str(design)
    if not over_applied(log_entries(design_text)):
        runs = [("--check-cited-headings", check_cited_headings, value), ("--check-target-kind", check_target_kind, value)]
        if Path(design).resolve().parent.name == "design-specs":
            runs.append(("--check-constructs", check_constructs, value))
        if retired_phrases(design_text):
            runs.append(("--show-reach", show_reach, value))
    else:
        commit = last_commit(root)
        changes = work_changes(root, commit)[0] if commit else {}
        target = set(re.findall(r"`([^`]+)`", dict(read_design(design)[1]).get("Target", "")))
        text_of = spec_texts(root)
        runs = [("--check-constructs", check_constructs, str(root / p)) for p in sorted(changes)
                if p in target and p in text_of and constructs_in(p, text_of[p], changes[p])]
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
    text = re.sub(r"\n{3,}", "\n\n", "\n".join(lines).rstrip("\n") + "\n")
    path.write_bytes((text.replace("\n", "\r\n") if "\r\n" in raw else text).encode("utf-8"))


def report_of(value):
    """-> (design, kind, count) of a report at its path in a design's folder,
    `.ai/tmp/<skill-name>/<design>/reports/<kind>/{n}.md`, its design `.ai/plans/<skill-name>/<design>.md`; or None."""
    path = Path(value).resolve()
    if len(path.parents) < 6 or not path.stem.isdigit() or path.parents[1].name != "reports" or path.parents[4].name != "tmp":
        return None
    design = path.parents[5] / "plans" / path.parents[3].name / (path.parents[2].name + ".md")
    return (design, path.parent.name, int(path.stem)) if design.is_file() else None


# @canon-spec specs/methodology/working-files.md § A Check's Report § Script Checks [Name: places-in-their-form]
# @canon-spec specs/methodology/working-files.md § A Check's Report § Script Checks [Name: report-in-its-form]
# @canon-spec specs/methodology/working-files.md § A Check's Report § Script Checks [Name: report-laid-out]
# @canon-spec specs/methodology/working-files.md § A Check's Report § Script Checks [Name: searches-cover-their-matches]
def check_report(value):
    """--check-report REPORT: a review's report, before its settlement, its reviewer's part held to its form, its
    Searches run again; writes no file; -> 1 where it reports, 0 where it reports nothing, 2 for a usage error."""
    root = repo_root()
    found = report_of(value) if Path(value).is_file() else None
    if found is None or found[1] not in REVIEWS:
        sys.stderr.write("--check-report takes a review's report at its path in a design's folder, "
                         ".ai/tmp/<skill-name>/<design>/reports/<kind>/{n}.md: %s\n" % value)
        return 2
    design, kind, n = found
    design_text = read(design).replace("\r\n", "\n")
    rep = read_report(read(Path(value)))
    ctx = report_context(root, design, design_text, kind, n, log_entries(design_text), reviewer=True)
    problems = form_problems(rep, ctx, report_types(root), report_parts(root))
    if rep["in_form"]:
        problems += layout_problems(rep, root) + places_problems(rep, report_types(root)) + search_problems(rep, ctx)
    return report("check-report " + rel_to(value, root), problems)


def retired_phrases(text):
    """-> each of a design's retired phrases as (phrase, replacement, [(path, section or None)] it stays right in)."""
    out = []
    for record in records(section(text, RETIRED)) or []:
        f = dict((k, v.strip()) for k, v in record)
        stays = "" if f.get("Stays Right", "none").lower() == "none" else f["Stays Right"]
        out.append((f.get("Phrase", ""), f.get("Replacement", ""), places(stays)))
    return out


# @canon-spec specs/methodology/working-files.md § Design Log Entry
# @canon-spec specs/methodology/working-files.md § Retired Phrase
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


def phrase_lines(path, phrases):
    """-> (line number, line, phrase, replacement) for each line of a file holding a retired phrase as whole words,
    regardless of case, outside the places it stays right."""
    try:
        text = read(Path(path)).replace("\r\n", "\n")
    except (OSError, UnicodeDecodeError):
        return []
    out, stack = [], []
    for i, line in enumerate(text.split("\n"), 1):
        h = re.match(r"^(#{2,6})\s+(.*?)\s*$", line)
        if h:
            depth = len(h.group(1)) - 2
            stack = stack[:depth] + [h.group(2)]
        lineage = " § ".join(stack)
        for phrase, replacement, places in phrases:
            if not re.search(r"(?<![\w-])%s(?![\w-])" % re.escape(phrase), line, re.I):
                continue
            if any(p == path and (s is None or lineage == s or lineage.startswith(s + " § ")) for p, s in places):
                continue
            out.append((i, line.strip(), phrase, replacement))
    return out


def scope_files(root):
    """-> the files in Spec of Record's scope, tracked or new, the working files aside."""
    scope = scope_paths(root)
    found = subprocess.run(["git", "ls-files", "--cached", "--others", "--exclude-standard", "--"] + scope,
                           capture_output=True, text=True, encoding="utf-8", cwd=root)
    paths = found.stdout.split("\n") if found.returncode == 0 else \
        [s for s in scope if (root / s).is_file()] + \
        [p.relative_to(root).as_posix() for s in scope if (root / s).is_dir() for p in (root / s).rglob("*") if p.is_file()]
    return sorted(p for p in paths if p and not is_working_file(p))


def show_reach(value):
    """--show-reach DESIGN: each line in scope holding a retired phrase, those outside the Target marked; -> 0."""
    design = design_file(value)
    if design is None:
        return 2
    _, fields, _, text = read_design(design)
    phrases, target = retired_phrases(text), set(re.findall(r"`([^`]+)`", dict(fields).get("Target", "")))
    print("== show-reach " + design.stem)
    n = 0
    for path in scope_files(Path.cwd()):
        for i, line, phrase, _ in phrase_lines(path, phrases):
            n += 1
            print("%s:%d%s  [%s]  %s" % (path, i, "" if path in target else "  (outside the Target)", phrase, line[:160]))
    print("%d line%s\n" % (n, "" if n == 1 else "s"))
    return 0


def check_retired_wording(value):
    """--check-retired-wording DESIGN: each line of the Target's files holding a retired phrase, with its
    replacement; -> 1 where any stands."""
    design = design_file(value)
    if design is None:
        return 2
    _, fields, _, text = read_design(design)
    phrases = retired_phrases(text)
    problems = [(path, "line %d holds %s, retired for %s: %s" % (i, phrase, replacement, line[:160]))
                for path in re.findall(r"`([^`]+)`", dict(fields).get("Target", ""))
                for i, line, phrase, replacement in phrase_lines(path, phrases)]
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
    outside the working files and the Target, a user's edit or a direct edit the log names marked; -> 1 where one
    stands that no entry names."""
    design = design_file(value)
    if design is None:
        return 2
    _, fields, _, text = read_design(design)
    try:
        found = subprocess.run(["git", "status", "--porcelain=v1", "-uall", "-z"], capture_output=True, text=True, encoding="utf-8")
    except FileNotFoundError:
        found = None
    if found is None or found.returncode:
        print("== check-changed-files %s\nno version control, so the files changed cannot be listed\n" % design.stem)
        return 0
    paths, parts = [], found.stdout.split("\0")
    i = 0
    while i < len(parts):
        entry = parts[i]
        if len(entry) > 3:
            paths.append(entry[3:])
            if entry[0] in "RC":
                i += 1  # a rename's or a copy's source follows it
        i += 1
    target = set(re.findall(r"`([^`]+)`", dict(fields).get("Target", "")))
    users, directs = logged_places(text, "user-edit"), logged_places(text, "direct-edit")
    problems, marked = [], []
    for path in sorted(set(paths)):
        if is_working_file(path) or path in target:
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
    return [re.sub(r"\s*\\$", "", re.sub(r"^#+ ", "", l).strip()).strip() for l in text.replace("\r\n", "\n").split("\n")
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
    try:
        found = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True)
    except FileNotFoundError:  # no git on the machine
        return Path.cwd()
    return Path(found.stdout.strip()) if found.returncode == 0 else Path.cwd()


def objectives_stating_constructs(text):
    """-> [(step, design line of the Objective, its lines)] for each Objective of a Design Plan Step holding a
    **Construct:** field declaring one of WHOLE, its lines as written: the Objective item's own lines, ending where
    spec-style.md § Markdown has a list item end, as the one reader reads it."""
    lines, out = text.split("\n"), []
    start = next((i for i, l in enumerate(lines) if re.match(r"^## Design Plan Steps\s*$", l)), None)
    if start is None:
        return out
    end = next((i for i in range(start + 1, len(lines)) if lines[i].startswith("## ")), len(lines))
    for step in records_read("\n".join(lines[start:end])) or []:
        if step["fields"] is None:
            continue
        name = str(record_types.value_of(step["fields"][0])).strip()
        objectives = next((f for f in step["fields"] if f["key"] == "Objectives"), None)
        for it in (objectives["items"] if objectives else None) or []:
            at = start + it["line"]
            item = [lines[start + n] for n in it["lines"]]
            if any(l.strip().startswith("**Construct:**") and any(w in l for w in WHOLE) for l in item):
                out.append((name, at + 1, item))
    return out



def kept_changes(root, design_text):
    """-> the paths the checkout holds changed against the last commit, where the design is not applying, so its
    reading is the last commit's, as working-files.md § A Design Document § The States It Moves Through § A Send-back
    has a reading made while kept changes stand; else none."""
    if re.search(r"^\*\*Status:\*\* applying(?: \\)?\s*$", design_text, re.M):
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
from pathlib import Path
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
    commit, each tree by the checks as they stood in it, or as they stand where the commit holds none of the modules."""
    lib = str(Path(__file__).resolve().parent)
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
    specs/AGENTS.md § Design, Refactor, Refine § Measure Twice, Cut Once has the builder zoom out."""
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


CITED_SPAN = re.compile(r"`([^`]*?(?:§|\.md)[^`]*)`")


def markdown_reach(text_of, changes):
    """-> {path: 0-based lines} the builder zooms out to from each line a change wrote in a Markdown file in scope:
    around, up, and across, each passage citing what it read around, an ancestor or the file whole, read around and
    up in turn."""
    reach, read_names = {}, {}
    for path, lines in changes.items():
        if path not in text_of:
            continue
        for line in lines:
            got, names = around_and_up(text_of[path], line)
            reach.setdefault(path, set()).update(got)
            read_names.setdefault(path, set()).update(names)
    for host, text in text_of.items():
        for n, line in enumerate(strip_fences(text).split("\n"), 1):
            for m in CITED_SPAN.finditer(line):
                cited, lineage = resolve_citation(m.group(1), host)
                if cited in read_names and (lineage in read_names[cited] or not lineage):
                    got, _ = around_and_up(text, n)
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
    units calling it, as specs/AGENTS.md § Design, Refactor, Refine § Measure Twice, Cut Once gives it; a script not
    in Python read whole."""
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
        reach = {p: {n + 1 for n in lines} for p, lines in markdown_reach(text_of, changes).items()}
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
    ("--append-entry", "DESIGN KIND [FIELD=VALUE ...]", append_entry,
     "append an entry to a design document's log, its count among its kind and the UTC time it is appended, refusing a kind, a field or a value out of the Design Log Entry type; for a check's entry, reading its report at reports/<kind>/{n}.md in the design's folder, writing a self-review's script checks' output into it, refusing the entry where the report is out of its form, its layout or the form of its values holding places, leaves a finding unsettled or settles one twice, cites a key naming no record, holds a Search whose matches its Places do not cover, or holds records not covering what working-files.md § A Check's Report has the script check of them, and taking the entry's counts from it, refusing any the builder gives; the builder appends every entry through it"),
    ("--check-report", "REPORT", check_report,
     "check a review's report at its path in a design's folder before its settlement: its reviewer's part, its title, its Reading, its Findings and its Searches, held to the form working-files.md § A Check's Report gives it and to its layout, its values holding places in their form, and each Search run again; writes no file; the reviewer runs it before handing the report back, and the builder as settling starts"),
    ("--show-reach", "DESIGN", show_reach,
     "list each line in Spec of Record's scope holding a phrase the design's Retired Phrases record, outside its Stays Right, marking those outside the Target; the builder runs it at drafting"),
    ("--check-retired-wording", "DESIGN", check_retired_wording,
     "report each line of the Target's files holding a retired phrase outside its Stays Right, with its replacement; the builder runs it at its self-review before the post-apply review"),
    ("--check-changed-files", "DESIGN", check_changed_files,
     "list each file changed against the last commit outside the working files that the Target does not name, marking the user's edits and the direct edits the log names; the builder runs it at its self-review before the post-apply review"),
    ("--check-work", "DESIGN", check_work,
     "run the specs' and the code's script checks over the design's work, the files changed against the last commit, whatever they touch: each finding the scope holds now that it did not hold then, each tree by the checks as they stood in it, matched by its rule, its file and its message, its repeats counted, a matched finding on a line the change added reported too; then, apart, each candidate in the reach the builder zooms out to from what the change wrote; with no version control, every finding the scope holds; writes no file; the builder runs it at its self-review, and the post-apply review runs it"),
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
        elif flag == "--append-entry":
            parser.add_argument(flag, metavar="ARG", nargs="+", action="append", help=metavar + ": " + help_text)
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
