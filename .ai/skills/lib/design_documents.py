#!/usr/bin/env python3
"""The design document tooling the skills writing design documents share: checks what a proposal
quotes and cites, holds design documents to their form, and shows what a Refactor and Refine cycle
changed.

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
import hashlib
import re
import subprocess
import sys
from pathlib import Path


REGISTRY = "specs/methodology/skills.md"
KINDS = ("canon", "application", "code", "neither")
# working-files.md § A Design Document and § A Steering Decision
PLANS = ".ai/plans/design-specs"  # set by the entry script calling main
CODE_PLANS = "implement-specs"  # the plans folder of the designs changing code, whose kind is code
FIELDS = ("Name", "Status", "Source", "Specs", "Target", "Spawned By", "Depends On", "Validated")
# working-files.md § A Stamp: a UTC timestamp and a content hash; a design document's
# Validated stamp leaves out the Validated and Status fields.
STAMP = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z sha256:[0-9a-f]{16}$")
UNSTAMPED = ("Validated", "Status")
IMPACT = "Impact on the Application Specs"  # a canon design's, and no other design's
SECTIONS = ("The Problem", "Scope", "Steering Decisions", "The Design", IMPACT, "The Builder's Passes", "Deliberately Left Alone")
OPTIONAL = ("Steering Decisions",)
STEER_FIELDS = ("Name", "Prompted By", "Steer", "Decision")
# working-files.md § A Design Document: an adversarial DRR's or post-apply audit's pass,
# its lead-in and what follows it to the next, names the model and effort it ran on.
REVIEW = re.compile(r"^\*\*(?:Adversarial DRR|Post-apply audit)\b", re.I)
REVIEW_FORM = re.compile(r"^\*\*(?:Adversarial DRR|Post-apply audit)\b")
RAN_ON = re.compile(r"\bon [^\s,;]+(?: [^\s,;]+)*? (?:at (?:light|medium|high) effort|as the agent allows)\b", re.I)
STATES = ("not-started", "in-progress", "approved", "applying", "complete", "abandoned")
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


def check_steers(body):
    """-> problems with a Steering Decisions section: a Records field, and each record its
    type's fields in order, no two sharing a Name."""
    if not re.search(r"^\*\*Records:\*\*\s*$", body, re.M):
        return ["Steering Decisions has no Records field"]
    items = re.split(r"^- ", body.split("**Records:**", 1)[1], flags=re.M)[1:]
    if not items:
        return ["Steering Decisions holds no record"]
    problems, seen = [], set()
    for item in items:
        keys = re.findall(r"^[ \t]*" + KEY, item, re.M)
        if keys != list(STEER_FIELDS):
            problems.append("a steering decision's fields are %s, not %s" % (", ".join(keys), ", ".join(STEER_FIELDS)))
            continue
        name = re.match(KEY + r" ?(.*)", item).group(2).strip()
        if name in seen:
            problems.append("two steering decisions share the Name " + name)
        seen.add(name)
    return problems


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
        if values.get("Specs") and (values["Specs"] == "code") != (design.parent.name == CODE_PLANS):
            problems.append((name, "Specs is code for a design under .ai/plans/%s/ and for no other: %s" % (CODE_PLANS, values["Specs"])))
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
        if values.get("Status") in ("approved", "applying", "complete"):
            if not re.search(r"^\*\*Adversarial DRR\b", section(text, "The Builder's Passes") or "", re.M):
                problems.append((name, values["Status"] + ", but its passes name no adversarial DRR"))
        for p in re.split(r"(?m)^(?=\*\*\S)", section(text, "The Builder's Passes") or ""):
            if REVIEW.match(p) and not REVIEW_FORM.match(p):
                problems.append((name, "a review's lead-in is not written as the form sets it, Adversarial DRR or Post-apply audit: " + p[:40].strip()))
            if REVIEW.match(p) and not RAN_ON.search(p):
                problems.append((name, "a review's pass names no model and reasoning effort, as on {model} at {effort} effort or on {model} as the agent allows: " + p[:60].strip()))
        want = [s for s in SECTIONS if (s in sections or s not in OPTIONAL) and (s != IMPACT or values.get("Specs") == "canon")]
        if sections != want:
            problems.append((name, "its sections are %s, not %s" % (", ".join(sections), ", ".join(want))))
        body = section(text, "Steering Decisions")
        for p in check_steers(body) if body is not None else []:
            problems.append((name, p))
    return len(designs), problems


def kind_of(path, skills):
    """canon, application, or None for a file of neither kind."""
    if path == "specs/AGENTS.md" or path.startswith("specs/methodology/"):
        return "canon"
    if any(path.startswith(".ai/skills/" + n + "/") for n in skills + ["lib"]):
        return "canon"
    if path.startswith("specs/application/"):
        return "application"
    return None


def check_specs(design, root):
    """-> (1, [(file name, problem)]) where one design document's Target strays from its Specs."""
    reg = root / REGISTRY
    skills = re.findall(r"^\| `([a-z0-9-]+)` \|", reg.read_text(encoding="utf-8"), re.M) if reg.exists() else []
    if not skills:
        return 0, [(REGISTRY, "no registered skills read, so a skill's files cannot be classified")]
    problems, designs = [], [read_design(design)]
    for title, fields, _, _ in designs:
        fields = dict(fields)
        value, target = fields.get("Specs"), fields.get("Target")
        if not value:
            problems.append((title, "no Specs field"))
            continue
        if not target:
            problems.append((title, "no Target field"))
            continue
        if value not in KINDS:
            problems.append((title, "Specs is not canon, application, code or neither: " + value))
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
    Spawned By and Depends On draw, and where its Status is out of step with what it
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
# citation and is not checked here; see SKILL.md, Verifying a proposal.
CITATION = re.compile(r'`([\w./-]+\.md)\s+§\s+([^`]+)`')


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
        path, target = m.group(1), " ".join(m.group(2).split())
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
    """Every check on one design: its form, its Target's kind, and what the workstack
    finds wrong with it. Any problem the form and kind checks report counts, whatever it
    is filed under, so a skills registry that cannot be read stops a stamp."""
    found = check_form(design)[1] + check_specs(design, Path.cwd())[1]
    return found + [(t, p) for t, p in check_stack(design.parent)[1] if t == design.stem]


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
    return 2 if design is None else report("check-target-kind " + design.stem, check_specs(design, Path.cwd())[1])


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
     "confirm every file a design document's Target names is of the kind its Specs declares"),
    ("--check-design", "DESIGN", check_design,
     "run every check on one design document: its form, its Target's kind, and its place in the workstack"),
    ("--check-workstack", "PLANS_DIR", check_workstack,
     "report what is out of step in the workstack: a Status out of step with what a design depends on, a Depends On naming no design, and a loop; reads the skill's plans folder, and those beside it, unless given a directory"),
    ("--show-workstack", "PLANS_DIR", show_workstack,
     "draw the workstack and list what to work next, what is blocked and what may be deleted; reads the skill's plans folder, and those beside it, unless given a directory"),
    ("--show-validation", "DESIGN", show_validation,
     "print a design document's stamped hash, its hash now, and whether it is validated, stale or never stamped"),
    ("--stamp-validation", "DESIGN", stamp_validation,
     "run every check on one design document and, if it passes, write its validation stamp; the validation review alone runs it"),
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
    args = vars(parser.parse_args(argv[1:]))
    chosen = [(run, value) for flag, _, run, _ in FLAGS for value in args[flag[2:].replace("-", "_")] or []]
    if not chosen:
        parser.print_usage(sys.stderr)
        return 2
    return max(run(value) for run, value in chosen)


if __name__ == "__main__":
    sys.stderr.write("run a skill's entry script, not this shared code: specs/methodology/skills.md § Authoring a Skill\n")
    sys.exit(2)
