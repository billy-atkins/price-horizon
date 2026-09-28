#!/usr/bin/env python3
"""Checks that what a proposal quotes and what it cites actually exist.

A proposal that says "replace X with Y" is applicable only if X appears in the
target file, exactly, once. This verifies that before review, rather than
discovering it at apply time when the edit silently fails or lands elsewhere.

Separate modes, because a proposal makes separate kinds of claim about a file,
and a checker catching only quoted text lets a wrong heading through unnoticed:

  anchors    quoted text exists, exactly once, in the file named
  citations  every `path.md § A § B` in the proposal resolves to that heading

Standard library only. See SKILL.md for the manifest format.
"""

import re
import sys
from pathlib import Path

USAGE = """usage: design-specs.py anchors <manifest|->
       design-specs.py citations <proposal.md>

  anchors    Verifies each anchor in the manifest appears exactly once in its file.

             Manifest format: a line beginning "--- " names a file; every line up
             to the next "--- " is one anchor, verbatim. Lines beginning "#"
             before the first "--- " are comments. Pass - for stdin.

  citations  Verifies every cross-file citation in the proposal resolves to a
             real heading lineage. A same-file citation is skipped: a proposal is
             not the file it cites into, so a bare section token has no referent
             to check against.
"""

# `path/to/file.md § Parent § Child`. A span carrying no path is a same-file
# citation and is not checked here; see USAGE.
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


def main(argv):
    if len(argv) != 3 or argv[1] not in ("anchors", "citations"):
        sys.stderr.write(USAGE)
        return 2

    if argv[1] == "citations":
        try:
            results = check_citations(argv[2], Path.cwd())
        except OSError as exc:
            sys.stderr.write("cannot read proposal: %s\n" % exc)
            return 2
        if not results:
            sys.stderr.write("no cross-file citations found\n")
            return 2
        width = max(len(p) for _, p, _, _ in results)
        failed = 0
        for ok, path, target, note in results:
            if not ok:
                failed += 1
            print("%-9s %-*s  § %s" % ("ok" if ok else "BROKEN", width, path, target))
            if note:
                print("%s\\- %s" % (" " * 10, note))
        print(
            "\n%d citation%s, %d broken"
            % (len(results), "" if len(results) == 1 else "s", failed)
        )
        return 1 if failed else 0

    source = argv[2]
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

    root = Path.cwd()
    failed = 0
    width = max(len(p) for p, _ in entries)

    for path, anchor in entries:
        status, detail = check(path, anchor, root)
        if status != "ok":
            failed += 1
        preview = collapse(anchor)[:52] or "(empty)"
        line = "%-9s %-*s  %s" % (status, width, path, preview)
        if detail:
            line += "\n%s\\- %s" % (" " * 10, detail)
        print(line)

    print(
        "\n%d anchor%s, %d failed"
        % (len(entries), "" if len(entries) == 1 else "s", failed)
    )
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
