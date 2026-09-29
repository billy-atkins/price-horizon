#!/usr/bin/env python3
"""Render a Mermaid diagram to PNG so it can actually be looked at.

Hand-tracing Mermaid grammar catches parse errors and nothing else. Layout and
semantic defects survive it intact and only show up on render. This renders a
diagram to an image file, which an agent can then read back.

Renderers, tried in order:
  - mmdc (@mermaid-js/mermaid-cli), if on PATH. Local, offline, and pinnable,
    so what is rendered matches whatever version is installed. Needs Node 18+.
  - mermaid.ink over HTTPS. No install, but sends the diagram to a third party
    and runs whatever Mermaid version that service runs.

Usage:
  author-mermaid-diagram.py --render-diagrams FILE              # every mermaid block in FILE
  author-mermaid-diagram.py --render-diagrams FILE --block 2    # one block, by number (1-based)
  author-mermaid-diagram.py --list-diagrams FILE                # list blocks without rendering
  author-mermaid-diagram.py --render-diagrams - < diagram.mmd   # one diagram from stdin
  author-mermaid-diagram.py --render-diagrams FILE --output-directory path/  # default: .ai/tmp/author-mermaid-diagram

Paths are resolved against the current working directory, so run it from the
repository root (or pass --output-directory) if the default output location matters.

Markdown blockquote prefixes ("> ") are stripped, so a diagram quoted inside a
design note renders the same as one checked into a spec.

Output is named for where the diagram lives: the source path, flattened, then the
headings above the block, e.g. docs/api/overview.md under "## Diagrams" and
"### Request Flow" renders to docs_api_overview--diagrams--request-flow.png. A
name built from the file's basename alone collided: files both called overview.md
wrote to the same PNG, and rendering one deleted the other's output as stale. The
document's level-1 title is left out, since it names the same thing the path
already does.
"""

from __future__ import annotations

import argparse
import base64
import hashlib
import os
import json
import re
import shutil
import subprocess
import sys
import tempfile
import zlib
from pathlib import Path

DEFAULT_OUT_DIR = Path(".ai/tmp/author-mermaid-diagram")
FENCE = re.compile(r"^\s*(?:>\s?)*```\s*mermaid\s*$", re.IGNORECASE)
FENCE_END = re.compile(r"^\s*(?:>\s?)*```\s*$")
ANY_FENCE = re.compile(r"^\s*(?:>\s?)*```")
BLOCKQUOTE = re.compile(r"^(\s*)(?:>\s?)+")
HEADING = re.compile(r"^\s*(?:>\s?)*(#{1,6})\s+(.*?)\s*#*\s*$")
PATH_SEP = "_"      # between folder segments; slug() never produces it
SEP = "--"          # between the path and each heading; slug() never produces it
MAX_NAME = 150      # under the 255-byte name limit on Linux and macOS, and keeps the
                    # full output path under Windows' 260-character limit


def strip_blockquote(line: str) -> str:
    return BLOCKQUOTE.sub(r"\1", line)


def extract_blocks(text: str) -> list[tuple[list[str], str]]:
    """Return (heading lineage, code) for every ```mermaid block, blockquote
    prefixes removed. The lineage is the chain of headings above the block, below
    the level-1 title. Headings inside any other fenced block are ignored, since a
    `# comment` in a code sample is not a section."""
    blocks, current, other, stack = [], None, False, []
    for line in text.splitlines():
        if other:
            if FENCE_END.match(line):
                other = False
            continue
        if current is None:
            if FENCE.match(line):
                current = []
            elif ANY_FENCE.match(line):
                other = True
            elif m := HEADING.match(line):
                level = len(m.group(1))
                if level > 1:
                    stack = [(lv, h) for lv, h in stack if lv < level] + [(level, m.group(2))]
            continue
        if FENCE_END.match(line):
            blocks.append(([h for _, h in stack], "\n".join(current).rstrip()))
            current = None
        else:
            current.append(strip_blockquote(line))
    if current is not None:
        sys.stderr.write("warning: unterminated ```mermaid block; rendering it anyway\n")
        blocks.append(([h for _, h in stack], "\n".join(current).rstrip()))
    return blocks


# Windows refuses these as a file name whatever the extension: CON.png cannot exist.
RESERVED = {"CON", "PRN", "AUX", "NUL", *(f"COM{i}" for i in range(10)),
            *(f"LPT{i}" for i in range(10))}


def slug(text: str) -> str:
    """Lowercase ASCII letters, digits and single hyphens only, so a name is legal
    on every filesystem: no path separator or NUL (Linux), no colon (macOS Finder), none of
    the characters Windows forbids (<>:"/\\|?*), no spaces, and no leading dot
    (a hidden file) or leading hyphen (read as an option by command-line tools).
    Lowercase because Windows and macOS filesystems ignore case by default, so
    "Flow" and "flow" would be one file there and one render would overwrite the
    other; with no case in the name, two names differ everywhere or nowhere."""
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-") or "x"


def source_prefix(path: Path) -> str:
    """The source path, relative to the working directory where possible, as one
    filename-safe string: docs/api/overview.md -> docs_api_overview. Folders are
    joined by an underscore, which slug() never produces, so a hyphen inside a
    name cannot be mistaken for a folder boundary: a/b-c.md -> a_b-c, while
    a-b/c.md -> a-b_c."""
    try:
        rel = Path(os.path.relpath(path.resolve(), Path.cwd()))
    except ValueError:  # on another drive, on Windows
        rel = path.resolve()
    parts = [p for p in rel.with_suffix("").parts if p not in ("..", ".", rel.anchor)]
    return PATH_SEP.join(slug(p) for p in parts)


def output_names(prefix: str, blocks: list[tuple[list[str], str]]) -> list[str]:
    """One PNG name per block, unique within the file. Blocks sharing a heading
    lineage, or sitting under no heading at all, are told apart by position."""
    stems = [SEP.join([prefix] + [slug(h) for h in lineage]) for lineage, _ in blocks]
    total = {s: stems.count(s) for s in stems}
    seen: dict[str, int] = {}
    names = []
    for s in stems:
        if total[s] > 1:
            seen[s] = seen.get(s, 0) + 1
            s = f"{s}{SEP}{seen[s]}"
        if len(s) > MAX_NAME:
            digest = hashlib.sha1(s.encode()).hexdigest()[:8]
            s = f"{s[:MAX_NAME - 10]}{SEP}{digest}"
        if s.upper() in RESERVED:
            s = f"{s}-diagram"
        names.append(f"{s}.png")
    return names


def render_local(code: str, out: Path) -> bool:
    mmdc = shutil.which("mmdc") or shutil.which("mmdc.cmd")
    if not mmdc:
        return False
    with tempfile.NamedTemporaryFile("w", suffix=".mmd", delete=False, encoding="utf-8") as fh:
        fh.write(code)
        src = Path(fh.name)
    try:
        proc = subprocess.run(
            [mmdc, "-i", str(src), "-o", str(out), "-b", "white"],
            capture_output=True, text=True, timeout=120,
        )
        if proc.returncode != 0:
            sys.stderr.write(f"mmdc failed, falling back to mermaid.ink:\n{proc.stderr.strip()}\n")
            return False
        return out.exists()
    except Exception as exc:  # noqa: BLE001 - any local failure just means fall back
        sys.stderr.write(f"mmdc error, falling back to mermaid.ink: {exc}\n")
        return False
    finally:
        src.unlink(missing_ok=True)


def render_remote(code: str, out: Path, attempts: int = 2) -> tuple[bool, str]:
    """Render via mermaid.ink. Returns (ok, reason) where reason is '', 'invalid'
    when the service rejected the diagram, or 'unreachable' when the network did.
    The distinction matters: 'invalid' means fix the diagram, 'unreachable' means
    it simply has not been checked yet."""
    import urllib.error
    import urllib.request

    payload = json.dumps({"code": code}).encode()
    deflate = zlib.compressobj(9, zlib.DEFLATED, 15)
    packed = deflate.compress(payload) + deflate.flush()
    token = base64.urlsafe_b64encode(packed).decode().rstrip("=")
    url = f"https://mermaid.ink/img/pako:{token}?type=png"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})

    for attempt in range(1, attempts + 1):
        try:
            with urllib.request.urlopen(req, timeout=40) as resp:
                data = resp.read()
        except urllib.error.HTTPError as exc:
            detail = ""
            try:
                detail = exc.read().decode("utf-8", "replace")[:400]
            except Exception:  # noqa: BLE001
                pass
            sys.stderr.write(
                f"mermaid.ink rejected the diagram (HTTP {exc.code}); it most likely "
                f"does not parse.\n{detail}\n"
            )
            return False, "invalid"
        except Exception as exc:  # noqa: BLE001
            if attempt < attempts:
                sys.stderr.write(f"mermaid.ink did not respond ({exc}); retrying.\n")
                continue
            sys.stderr.write(f"mermaid.ink unreachable after {attempts} attempts: {exc}\n")
            return False, "unreachable"

        if not data.startswith(b"\x89PNG"):
            sys.stderr.write("mermaid.ink returned something that is not a PNG.\n")
            return False, "invalid"
        out.write_bytes(data)
        return True, ""

    return False, "unreachable"


def render(code: str, out: Path) -> tuple[str | None, str]:
    """Returns (renderer_used, failure_reason)."""
    out.parent.mkdir(parents=True, exist_ok=True)
    if render_local(code, out):
        return "mmdc (local)", ""
    ok, reason = render_remote(code, out)
    return ("mermaid.ink (remote)", "") if ok else (None, reason)


def load(file):
    """-> (blocks, prefix), or an exit status: the mermaid blocks FILE holds, or the
    diagram stdin carries when FILE is -, and the prefix their renders are named with."""
    if file == "-":
        return [([], sys.stdin.read())], "stdin"
    path = Path(file)
    if not path.exists():
        sys.stderr.write(f"no such file: {path}\n")
        return 2
    text = path.read_text(encoding="utf-8")
    blocks = extract_blocks(text) if "```" in text else [([], text)]
    if not blocks:
        sys.stderr.write("no ```mermaid blocks found\n")
        return 1
    return blocks, source_prefix(path)


def list_diagrams(file) -> int:
    loaded = load(file)
    if isinstance(loaded, int):
        return loaded
    blocks, prefix = loaded
    for i, ((lineage, code), name) in enumerate(zip(blocks, output_names(prefix, blocks)), 1):
        where = " > ".join(lineage) or "(no heading)"
        print(f"{i}: {where}  ({len(code.splitlines())} lines)\n   -> {name}")
    return 0


def render_diagrams(file, block, out_dir) -> int:
    loaded = load(file)
    if isinstance(loaded, int):
        return loaded
    blocks, prefix = loaded
    names = output_names(prefix, blocks)
    if block is None:
        wanted = list(enumerate(zip(blocks, names), 1))
    elif 1 <= block <= len(blocks):
        wanted = [(block, (blocks[block - 1], names[block - 1]))]
    else:
        sys.stderr.write(f"--block {block} out of range; the file has {len(blocks)}\n")
        return 2

    out_dir = Path(out_dir)

    # Clear this source's previous renders before writing new ones. Without this a
    # block that has since been deleted leaves its PNG behind, and the next reader
    # has no way to tell a current diagram from one that no longer exists anywhere.
    # Matching on the full flattened path, never the basename, is what keeps this
    # from deleting another file's renders.
    out_dir.mkdir(parents=True, exist_ok=True)
    for old in list(out_dir.glob(f"{prefix}.png")) + list(out_dir.glob(f"{prefix}{SEP}*.png")):
        old.unlink(missing_ok=True)

    invalid, unreachable = 0, 0
    for i, ((_, code), name) in wanted:
        out = out_dir / name
        via, reason = render(code, out)
        if via:
            print(f"rendered block {i} via {via}\n  {out.resolve()}")
        elif reason == "invalid":
            print(f"block {i} DOES NOT PARSE ({name})")
            invalid += 1
        else:
            print(f"block {i} NOT CHECKED, no renderer reachable ({name})")
            unreachable += 1

    if invalid:
        print(f"\n{invalid} diagram(s) failed to parse. Fix the source; see the errors above.")
    if unreachable:
        print(
            f"\n{unreachable} diagram(s) could not be rendered because no renderer was "
            "reachable. This says nothing about whether they are correct: they are "
            "unverified, not wrong. Do not describe them as checked."
        )
    return 1 if (invalid or unreachable) else 0


def main() -> int:
    # Actions are flags per specs/methodology/skills.md § Authoring a Skill.
    ap = argparse.ArgumentParser(description="Render Mermaid diagrams to PNG.", allow_abbrev=False)
    ap.add_argument("--render-diagrams", metavar="FILE", action="append",
                    help="render every mermaid block in FILE, a markdown or .mmd file, to PNG; - reads one diagram "
                         "from stdin; repeat it for more files")
    ap.add_argument("--list-diagrams", metavar="FILE", action="append",
                    help="list FILE's mermaid blocks and the name each renders to, without rendering; repeat it for more files")
    ap.add_argument("--block", type=int, metavar="N",
                    help="with a single --render-diagrams, render only block N, 1-based, as --list-diagrams numbers them")
    ap.add_argument("--output-directory", metavar="DIR", default=str(DEFAULT_OUT_DIR), help="the directory renders are written to")
    args = ap.parse_args()
    renders, lists = args.render_diagrams or [], args.list_diagrams or []
    if not (renders or lists):
        ap.print_usage(sys.stderr)
        return 2
    if args.block is not None and len(renders) != 1:
        sys.stderr.write("--block narrows a single --render-diagrams\n")
        return 2
    if (renders + lists).count("-") > 1:
        sys.stderr.write("stdin can be read by one action per run\n")
        return 2
    status = 0
    for file in lists:
        status = max(status, list_diagrams(file))
    for file in renders:
        status = max(status, render_diagrams(file, args.block, args.output_directory))
    return status


if __name__ == "__main__":
    raise SystemExit(main())
