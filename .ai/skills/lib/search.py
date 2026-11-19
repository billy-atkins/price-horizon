"""The search of Spec of Record's scope and the code, one copy the skills' scripts share
(specs/methodology/skills/authoring-a-skill.md § Authoring a Skill): who cites a place, which lines a citation names,
where a term is used, which units of code hold a structure, which places say the same as a passage, and which places
match a pattern. .ai/skills/search-spec-of-record-scope/ runs it for an agent, and another skill's script calls
`Search` directly.

Every use first checks everything the search requires and stops where any is missing (`check_requirements`). It
answers from an index kept in its skill's scratch space, built whole on first use and brought up to date by reading
only the files that changed. Every answer is written as one file in the form its skill states (`Result`).

The reading of a heading, a fenced block and a citation here is the search's own. No other script's reading is
changed by it, and it reads no version control.
"""
import ast
import hashlib
import importlib.util
import io
import os
import re
import sqlite3
import sys
import time
import tokenize
from pathlib import Path

import code_checks
import spec_text

SKILL = "search-spec-of-record-scope"
SCRATCH = ".ai/tmp/" + SKILL
MODEL = "sentence-transformers/all-MiniLM-L6-v2"
DIMENSIONS = 384
SCHEMA = "7"
RANKED = 20       # the places a search by meaning gives
CANDIDATES = 50   # the places each ranking gives the fusion
FUSION = 60       # the constant of reciprocal rank fusion
PASSAGE = 1000    # the most characters of a passage, which the model reads whole
MAX_NAME = 150    # the length the diagram skill's renders keep to, a name every system holds
FEW = 20          # the places printed with a result's name

KINDS = ("citers", "lines", "terms", "code structure", "meaning", "pattern")
STRUCTURES = ("defines", "calls", "constructs", "extends", "implements", "references", "annotated-with")


# ---------------------------------------------------------------------------------------------------------------------
# What the search requires

class Requirement:
    def __init__(self, name, why, install, present):
        self.name, self.why, self.install, self.present = name, why, install, present


def _module(name):
    return lambda root: importlib.util.find_spec(name) is not None


HOME = Path(__file__).resolve().parents[3]   # the project the search's own skill stands in, which keeps the model's files
MODEL_FOLDER = HOME / SCRATCH / "model"


def _model_present(root):
    folder = MODEL_FOLDER
    return folder.is_dir() and any(f.is_file() and f.suffix == ".onnx" for f in folder.rglob("*"))


ENTRY = "python .ai/skills/" + SKILL + "/scripts/" + SKILL + ".py"
def _sqlite_present(root):
    if not hasattr(sqlite3.Connection, "enable_load_extension"):
        return False
    try:
        sqlite3.connect(":memory:").execute("create virtual table t using fts5(x)")
    except sqlite3.Error:
        return False
    return True


REQUIREMENTS = [
    Requirement("a Python whose SQLite loads extensions and has full-text search", "the index is an SQLite database that searches text itself and loads the extension finding the nearest vectors",
                "install Python from python.org, or another build whose sqlite3 module has enable_load_extension and FTS5", _sqlite_present),
    Requirement("sqlite-vec", "finds the passages whose vectors stand nearest a passage's, inside the index",
                "python -m pip install sqlite-vec", _module("sqlite_vec")),
    Requirement("fastembed", "runs the model on this machine that turns a passage into the vector a search by meaning ranks by",
                "python -m pip install fastembed", _module("fastembed")),
    Requirement("tree-sitter", "parses code in the stack's languages into units, so code is searched as code",
                "python -m pip install tree-sitter", _module("tree_sitter")),
    Requirement("tree-sitter-typescript", "the grammar the parser reads TypeScript by",
                "python -m pip install tree-sitter-typescript", _module("tree_sitter_typescript")),
    Requirement("tree-sitter-c-sharp", "the grammar the parser reads C# by",
                "python -m pip install tree-sitter-c-sharp", _module("tree_sitter_c_sharp")),
    Requirement("the model's files", "the model " + MODEL + ", kept on this machine so a search sends no text anywhere and downloads nothing",
                ENTRY + " --install-model", _model_present),
]


def missing_requirements(root):
    return [r for r in REQUIREMENTS if not r.present(root)]


def requirements_report(root):
    """-> (the report's text, the count missing): each thing the search requires, present or missing, with why the
    search needs it and the command installing it."""
    missing = missing_requirements(root)
    out = []
    if missing:
        out.append(f"{SKILL}: the search cannot run. Of the {len(REQUIREMENTS)} things it requires, {len(missing)} {'is' if len(missing) == 1 else 'are'} missing.")
    else:
        out.append(f"{SKILL}: everything the search requires is present.")
    for r in REQUIREMENTS:
        out.append(f"  {'MISSING' if r in missing else 'present'}  {r.name}: {r.why}")
        if r in missing:
            out.append(f"           to install it: {r.install}")
    if missing:
        out.append("Every kind of search checks all of these before it reads or writes, so install each one missing, then run the search again.")
        if any(r.name == "the model's files" for r in missing) and any(r.name == "fastembed" for r in missing):
            out.append("Install fastembed before the model's files, since it downloads them.")
    return "\n".join(out), len(missing)


class MissingRequirements(Exception):
    """Raised by any use of the search where something it requires is missing, before anything is read or written."""


def check_requirements(root):
    text, count = requirements_report(root)
    if count:
        raise MissingRequirements(text)


def install_model(root):
    """Download the model's files into the skill's scratch space: the one action that reaches the network, run by the
    user's own command and never by a search."""
    if not _module("fastembed")(root):
        raise MissingRequirements(f"{SKILL}: fastembed is missing, and it downloads the model's files.\n  install it with: python -m pip install fastembed")
    from fastembed import TextEmbedding
    folder = MODEL_FOLDER
    folder.mkdir(parents=True, exist_ok=True)
    model = TextEmbedding(model_name=MODEL, cache_dir=str(folder))
    list(model.embed(["a passage"]))
    return folder


# ---------------------------------------------------------------------------------------------------------------------
# The one reading of a Markdown file: its fenced blocks, its headings and its citations

# @canon-spec specs/methodology/spec-style/markdown.md § Markdown
FENCE = re.compile(r"^(\s*)(`{3,}|~{3,})(.*)$")
HEADING = re.compile(r"^ {0,3}(#{1,6})[ \t]+(.*?)(?:[ \t]+#+)?[ \t]*$")
LINK = re.compile(r"\[(`[^`\n]+`)\]\((?:/|#)[^)\s]*\)")
# @canon-spec specs/methodology/sourcing-and-citation/writing-a-citation.md § Writing a Citation
SPAN = re.compile(r"(?<!`)(`+)(?!`)(.+?)(?<!`)\1(?!`)", re.S)
PATH = r"[\w.][\w./-]*"
CITATION = re.compile(r"^(?:(" + PATH + r") )?§ (.+)$")
WHOLE = re.compile(r"^" + PATH + r"$")
BARE = re.compile(r"(?<![\w./-])(" + PATH + r"\.[A-Za-z]+) § ")
KEYED = re.compile(r"^(.*?) \[(.*)\]$")
# @canon-spec specs/methodology/sourcing-and-citation/writing-a-citation.md § Writing a Citation § Citing From Code
ANNOTATION = re.compile(r"^\s*(?://(?![/!])|#+|--|;+|%+|<!--|/\*(?![*!]))\s*@(app|canon)-spec (\S.*?)\s*(?:-->|\*/)?\s*$")


def squeeze(text):
    """-> text with each run of white space made one space and its ends trimmed, as a form normalizes a field's input."""
    return " ".join(text.split())


def strip_links(text):
    """-> text with the link each citation carries set aside, the citation left as written."""
    return LINK.sub(r"\1", text)


def markdown_lines(text):
    """-> [(line, fenced, info)] for each line of a Markdown file: whether it stands in a fenced block, its fences
    among it, and the block's info string. A fence opens on a run of three or more backticks or tildes, at any
    indentation, so one standing in a list item or a record's field is read. It closes on a run of its own character at
    least as long with nothing after it, so a fence nested in a longer one stays inside it. Front matter is read as a
    block of its own, its info `front matter`."""
    out, fence, info = [], None, ""
    lines = text.split("\n")
    front = len(lines) > 1 and lines[0].strip() == "---"
    for i, line in enumerate(lines):
        if front:
            out.append((line, True, "front matter"))
            if i > 0 and line.strip() in ("---", "..."):
                front = False
            continue
        m = FENCE.match(line)
        if fence is None:
            if m and not (m.group(2)[0] == "`" and "`" in m.group(3)):
                fence, info = m.group(2), squeeze(m.group(3)).split(" ")[0]
                out.append((line, True, info))
            else:
                out.append((line, False, ""))
        else:
            out.append((line, True, info))
            if m and m.group(2)[0] == fence[0] and len(m.group(2)) >= len(fence) and not m.group(3).strip():
                fence, info = None, ""
    return out


def markdown_headings(rows):
    """-> [(lineage, occurrence, level, line, own_end, subtree_end)], lines 1-based, ends exclusive, from the headings
    standing outside every fenced block. A level-1 heading is the file's title and opens no lineage. The whole file is
    the lineage ''. `occurrence` counts the headings sharing a lineage, the first being 1."""
    heads = []
    for i, (line, fenced, _) in enumerate(rows):
        m = None if fenced else HEADING.match(line)
        if m:
            heads.append((i + 1, len(m.group(1)), squeeze(m.group(2))))
    total = len(rows) + 1
    first = next((h[0] for h in heads if h[1] > 1), total)
    out, stack, seen = [("", 1, 0, 1, first, total)], [], {}
    for n, (line, level, title) in enumerate(heads):
        if level == 1:
            continue
        stack = stack[:level - 2]
        while len(stack) < level - 2:
            stack.append(None)
        stack.append(title)
        lineage = " § ".join(t for t in stack if t)
        own_end = heads[n + 1][0] if n + 1 < len(heads) else total
        subtree_end = next((h[0] for h in heads[n + 1:] if h[1] <= level), total)
        seen[lineage] = seen.get(lineage, 0) + 1
        out.append((lineage, seen[lineage], level, line, own_end, subtree_end))
    return out


def parse_citation(written):
    """-> (path or None for the same file, lineage, key or None) of a citation as written, its white space squeezed, or
    None where the text is no citation. A whole-file citation gives the lineage ''."""
    text = squeeze(written)
    m = CITATION.match(text)
    if m:
        target, key = m.group(2), None
        k = KEYED.match(target)
        if k:
            target, key = k.group(1), "; ".join(squeeze(p) for p in k.group(2).split(";"))
        return m.group(1), " § ".join(squeeze(s) for s in target.split("§")), key
    if WHOLE.match(text) and "/" in text:
        return text.rstrip("/"), "", None
    return None


def markdown_citations(rows, headings):
    """-> [(line, host lineage, form, fenced, written, path, lineage, key)] for each citation a Markdown file holds: a
    code span in a citation's form, one broken across lines among them, an annotation's line in a fenced block, and each
    `technical-specs` entry of the front matter, a label. A same-file citation in a fenced `markdown` block names a
    section of the file that block holds, so it is no citer of the file around it and is left out."""
    out, text = [], "\n".join(r[0] for r in rows)
    starts, at = [], 0
    for line, _, _ in rows:
        starts.append(at)
        at += len(line) + 1

    def line_of(offset):
        lo, hi = 0, len(starts) - 1
        while lo < hi:
            mid = (lo + hi + 1) // 2
            if starts[mid] <= offset:
                lo = mid
            else:
                hi = mid - 1
        return lo + 1

    def host(line):
        best = ""
        for lineage, _, _, start, _, _ in headings[1:]:
            if start <= line:
                best = lineage
        return best

    # the text outside every fenced block is read apart from each block's own text, so a fence's backticks never
    # pair with a code span's, and a span never runs across a fence
    # a fenced line is blanked to its own length, so a place in this text is the same place in the file as written
    live = "\n".join(" " * len(line) if fenced else line for line, fenced, _ in rows)
    blocks, block = [], []
    for i, (line, fenced, info) in enumerate(rows):
        if fenced and info != "front matter" and not FENCE.match(line):
            block.append(i)
        elif block:
            blocks.append(block)
            block = []
    blocks += [block] if block else []
    regions = [(live, 0)] + [("\n".join(rows[i][0] for i in b), starts[b[0]]) for b in blocks]
    spanned = set()
    for region, base in regions:
        for m in SPAN.finditer(region):
            if "\n\n" in m.group(2):
                continue
            parsed = parse_citation(m.group(2))
            if not parsed:
                continue
            line = line_of(base + m.start())
            _, fenced, info = rows[line - 1]
            spanned.add(line)
            if fenced and info == "markdown" and parsed[0] is None:
                continue
            out.append((line, host(line), "citation", int(fenced), squeeze(m.group(2)), parsed[0], parsed[1], parsed[2]))
    front = False
    for i, (line, fenced, info) in enumerate(rows):
        if info == "front matter":
            if line.strip().startswith("technical-specs:"):
                front = True
            elif front and line.strip().startswith("- "):
                path = line.strip()[2:].strip().strip("'\"")
                out.append((i + 1, "", "label", 0, path, path, "", None))
            elif not line.startswith((" ", "\t")):
                front = False
        elif fenced:
            a = ANNOTATION.match(line)
            parsed = parse_citation(a.group(2)) if a else None
            if parsed and parsed[0]:
                out.append((i + 1, host(i + 1), "annotation", 1, squeeze(a.group(2)), parsed[0], parsed[1], parsed[2]))
            elif not FENCE.match(line):
                # a citation written bare in a fenced block, as a brief writes one: where it ends is told only by the
                # headings of the file it names, so the rest of its line is kept and read against them as it is asked for
                found = list(BARE.finditer(line))
                for n, b in enumerate(found):
                    rest = squeeze(line[b.end():found[n + 1].start()] if n + 1 < len(found) else line[b.end():])
                    if rest and line[max(0, b.start() - 1):b.start()] != "`":
                        out.append((i + 1, host(i + 1), "bare", 1, squeeze(b.group(1) + " § " + rest), b.group(1), rest, None))
    return sorted(set(out), key=lambda c: tuple("" if v is None else v for v in c))


def markdown_passages(rows, headings):
    """-> [(lineage, line_start, line_end, text)]: each section's own text in passages the model reads whole, split at
    its blank lines and then at its sentences. A fenced block's lines are left out, a diagram's and an example's among
    them, since they state nothing in prose."""
    out = []
    for lineage, _, _, start, own_end, _ in headings:
        block, first = [], None
        for n in range(start, own_end + 1):
            row = rows[n - 1] if n < own_end and n - 1 < len(rows) else ("", False, "")
            live = row[0].strip() and not row[1] and not HEADING.match(row[0])
            if live:
                block.append(row[0].strip())
                first = first or n
            elif block:
                text = squeeze(strip_markup(" ".join(block)))
                for piece in split_passage(text):
                    out.append((lineage, first, n - 1, piece))
                block, first = [], None
    return out


def strip_markup(text):
    return re.sub(r"[`*|\\]+", " ", text)


def split_passage(text):
    if len(text) < 40:
        return []
    if len(text) <= PASSAGE:
        return [text]
    out, cur = [], ""
    for sentence in re.split(r"(?<=[.?!]) ", text):
        if cur and len(cur) + len(sentence) + 1 > PASSAGE:
            out.append(cur)
            cur = ""
        cur = (cur + " " + sentence).strip()
        while len(cur) > PASSAGE:
            out.append(cur[:PASSAGE])
            cur = cur[PASSAGE:]
    return out + ([cur] if len(cur) >= 40 else [])


# ---------------------------------------------------------------------------------------------------------------------
# Code read by a parser for its language

LANGUAGES = {".py": "python", ".ts": "typescript", ".tsx": "tsx", ".cs": "c_sharp"}
# a language with no units: a file of it is one unit, and no structure is searched in it
NO_UNITS = {".yaml": "YAML", ".yml": "YAML", ".json": "JSON", ".toml": "TOML", ".ini": "INI"}
TREE_SITTER = {
    "typescript": {
        "unit": {"class_declaration": "class", "abstract_class_declaration": "class", "interface_declaration": "interface",
                 "function_declaration": "function", "method_definition": "method", "enum_declaration": "enum",
                 "type_alias_declaration": "type"},
        "call": ("call_expression", "function"), "new": ("new_expression", "constructor"),
        "extends": ("extends_clause", "extends_type_clause"), "implements": ("implements_clause",),
        "names": ("identifier", "type_identifier", "property_identifier"), "skip": ("comment", "string", "template_string"),
    },
    "c_sharp": {
        "unit": {"class_declaration": "class", "interface_declaration": "interface", "struct_declaration": "struct",
                 "record_declaration": "record", "enum_declaration": "enum", "method_declaration": "method",
                 "constructor_declaration": "constructor", "local_function_statement": "function"},
        "call": ("invocation_expression", "function"), "new": ("object_creation_expression", "type"),
        "extends": ("base_list",), "implements": ("base_list",),
        "names": ("identifier",), "skip": ("comment", "string_literal", "verbatim_string_literal", "interpolated_string_expression"),
    },
}
TREE_SITTER["tsx"] = TREE_SITTER["typescript"]


def comment_annotations(lines):
    """-> [(line, written, path, lineage, key)] for each plain comment line holding a spec annotation."""
    out = []
    for i, line in enumerate(lines, 1):
        m = ANNOTATION.match(line)
        parsed = parse_citation(m.group(2)) if m else None
        if parsed and parsed[0]:
            out.append((i, squeeze(m.group(2)), parsed[0], parsed[1], parsed[2]))
    return out


def unit_under(units, line):
    """-> the name of the unit an annotation on `line` stands over: the first unit opening after it, the run of
    annotations and comments between them passed over, or the file's own unit where none opens after it."""
    after = sorted((u for u in units if u[2] > line and u[1] != "module" and u[1] != "file"), key=lambda u: u[2])
    return after[0][0] if after else units[0][0]


def read_python(text, stem):
    """-> (units, structures, note): [(name, kind, line_start, line_end)] and [(structure, name, unit, line)]."""
    try:
        tree = ast.parse(text)
    except (SyntaxError, ValueError) as e:
        return [(stem, "file", 1, text.count("\n") + 1)], [], f"its parser could not read it: {e}"
    units, structures = [(stem, "module", 1, text.count("\n") + 1)], []

    def walk(node, unit, in_class):
        for child in ast.iter_child_nodes(node):
            here, inner = unit, in_class
            if isinstance(child, (ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)):
                kind = "class" if isinstance(child, ast.ClassDef) else ("method" if in_class else "function")
                name = (unit + "." if unit != stem else "") + child.name
                first = min([child.lineno] + [d.lineno for d in child.decorator_list])
                units.append((name, kind, first, child.end_lineno))
                structures.append(("defines", child.name, name, child.lineno))
                if isinstance(child, ast.ClassDef):
                    for base in child.bases:
                        target = base.id if isinstance(base, ast.Name) else getattr(base, "attr", None)
                        if target:
                            structures.append(("extends", target, name, child.lineno))
                here, inner = name, isinstance(child, ast.ClassDef)
            elif isinstance(child, ast.Call):
                f = child.func
                target = f.id if isinstance(f, ast.Name) else getattr(f, "attr", None)
                if target:
                    structures.append(("calls", target, unit, child.lineno))
            elif isinstance(child, ast.Name):
                structures.append(("references", child.id, unit, child.lineno))
            elif isinstance(child, ast.Attribute):
                structures.append(("references", child.attr, unit, child.lineno))
            elif isinstance(child, ast.Assign) and unit == stem:
                for t in child.targets:
                    if isinstance(t, ast.Name):
                        units.append((t.id, "constant", child.lineno, child.end_lineno))
                        structures.append(("defines", t.id, t.id, child.lineno))
            walk(child, here, inner)

    walk(tree, stem, False)
    return units, sorted(set(structures)), ""


def python_comment_lines(text):
    """-> the set of lines holding only a comment, read by Python's own tokenizer, so a string is never one."""
    out = set()
    try:
        for tok in tokenize.generate_tokens(io.StringIO(text).readline):
            if tok.type == tokenize.COMMENT and not tok.line[:tok.start[1]].strip():
                out.add(tok.start[0])
    except (tokenize.TokenError, IndentationError, SyntaxError):
        return None
    return out


_PARSERS = {}


def tree_sitter_parser(language):
    if language not in _PARSERS:
        from tree_sitter import Language, Parser
        if language in ("typescript", "tsx"):
            import tree_sitter_typescript as grammar
            pointer = grammar.language_tsx() if language == "tsx" else grammar.language_typescript()
        else:
            import tree_sitter_c_sharp as grammar
            pointer = grammar.language()
        _PARSERS[language] = Parser(Language(pointer))
    return _PARSERS[language]


def read_tree_sitter(text, stem, language):
    """-> (units, structures, note, comment lines) for a file in a language tree-sitter parses."""
    spec = TREE_SITTER[language]
    source = text.encode("utf-8")
    tree = tree_sitter_parser(language).parse(source)
    units, structures, comments = [(stem, "module", 1, text.count("\n") + 1)], [], set()

    def word(node):
        return source[node.start_byte:node.end_byte].decode("utf-8", "replace")

    def last_name(node):
        """-> the name a callee or a type is written with: its last identifier."""
        if node is None:
            return None
        if node.type in spec["names"]:
            return word(node)
        found = None
        for child in node.children:
            if child.type in spec["skip"] or child.type in ("arguments", "argument_list", "type_arguments", "type_argument_list"):
                continue
            found = last_name(child) or found
        return found

    def walk(node, unit):
        here = unit
        if node.type == "comment":
            for n in range(node.start_point[0] + 1, node.end_point[0] + 2):
                comments.add(n)
            return
        if node.type in spec["skip"]:
            return
        if node.type in spec["unit"]:
            name_node = node.child_by_field_name("name")
            if name_node is not None:
                name = (unit + "." if unit != stem else "") + word(name_node)
                units.append((name, spec["unit"][node.type], node.start_point[0] + 1, node.end_point[0] + 1))
                structures.append(("defines", word(name_node), name, node.start_point[0] + 1))
                here = name
        if node.type == spec["call"][0]:
            target = last_name(node.child_by_field_name(spec["call"][1]))
            if target:
                structures.append(("calls", target, unit, node.start_point[0] + 1))
        if node.type == spec["new"][0]:
            target = last_name(node.child_by_field_name(spec["new"][1]))
            if target:
                structures.append(("constructs", target, unit, node.start_point[0] + 1))
        for structure in ("extends", "implements"):
            if node.type in spec[structure]:
                for child in node.named_children:
                    target = last_name(child)
                    if target:
                        structures.append((structure, target, unit, node.start_point[0] + 1))
        if node.type in spec["names"]:
            structures.append(("references", word(node), unit, node.start_point[0] + 1))
        for child in node.children:
            walk(child, here)

    walk(tree.root_node, stem)
    note = "its parser met text it could not read, and what it read is listed" if tree.root_node.has_error else ""
    return units, sorted(set(structures)), note, comments


# ---------------------------------------------------------------------------------------------------------------------
# Terms

def normalize(text):
    """-> text with an identifier split into its words, at a change of case and between a letter and a digit, so
    `append_entry`, `--append-entry` and `AppendEntry` are each found by `append entry`. The index's tokenizer splits at
    every other character that is no letter or digit, and reduces each word to its stem."""
    text = re.sub(r"(?<=[a-z0-9])(?=[A-Z])", " ", text)
    return re.sub(r"(?<=[A-Z])(?=[A-Z][a-z])", " ", text)


def phrase(text):
    """-> the index's query for a phrase: its words in order, or None where it holds no word."""
    words = re.findall(r"[^\W_]+", normalize(text))
    return '"' + " ".join(words) + '"' if words else None


# ---------------------------------------------------------------------------------------------------------------------
# A search's result

class Result:
    """What a search gave, written as one file in the form `.ai/skills/search-spec-of-record-scope/SKILL.md § Search
    Result` states, the same whoever asked."""

    def __init__(self, kind, query, narrowed, run_as, completeness, places, notes=()):
        self.kind, self.query, self.narrowed, self.run_as = kind, squeeze(query), list(narrowed), run_as
        self.completeness, self.places, self.notes = completeness, list(places), list(notes)
        self.name = self.path = None

    def body(self):
        def items(values, pad="      "):
            return "".join(f"{pad}- {v}\n" for v in values)

        out = f"    **Kind:** {self.kind} \\\n    **Query:** {self.query} \\\n"
        if self.narrowed:
            out += "    **Narrowed To:**\n" + items(f"`{p}`" for p in self.narrowed) + "\n"
        out += f"    **Run As:** {self.run_as} \\\n    **Completeness:** {self.completeness} \\\n"
        out += "    **Places:**" + ("\n" + items(self.places) if self.places else " none\n")
        if self.notes:
            out += "\n    **Notes:**\n" + items(self.notes)
        return out

    def text(self):
        return ("# Search Result\n\nThe places are places to read, never findings. They are "
                + ("every place the search found." if self.completeness == "complete" else "the first of a ranking, and never every place.")
                + "\n\n**Records:**\n  - **Result:** " + self.name + " \\\n" + self.body())

    def write(self, folder):
        """Name the result from the kind of search, what was asked and its content, and write it. An earlier result of
        the same question under another name is cleared. A run that finds a file changed clears every result before it
        answers, so no result outlives the files it answered for."""
        asked = hashlib.sha256((self.kind + "\0" + self.query + "\0" + "\0".join(self.narrowed)).encode()).hexdigest()[:6]
        content = hashlib.sha256(self.body().encode()).hexdigest()[:8]
        kind = self.kind.replace(" ", "-")
        slug = re.sub(r"[^a-z0-9]+", "-", self.query.lower()).strip("-")
        room = MAX_NAME - len(kind) - len(asked) - len(content) - len(".md") - 3
        slug = slug[:room].strip("-") or "query"
        self.name = f"{kind}-{slug}-{asked}-{content}.md"
        folder.mkdir(parents=True, exist_ok=True)
        for stale in folder.glob(f"{kind}-*-{asked}-*.md"):
            if stale.name != self.name:
                stale.unlink()
        self.path = folder / self.name
        self.path.write_bytes(self.text().encode("utf-8"))
        return self.path

    @staticmethod
    def check(path):
        """-> [problems] of a result's file against the form its skill states: the name it holds is its file's, and
        the hash its name ends with is its content's, so a file whose content was changed no longer gives it."""
        path = Path(path)
        text = path.read_text(encoding="utf-8")
        m = re.search(r"^  - \*\*Result:\*\* (\S+) \\\n", text, re.M)
        if not m or not text.startswith("# Search Result\n"):
            return [f"{path.name}: it is not a search's result in the form the skill states"]
        problems = []
        if m.group(1) != path.name:
            problems.append(f"{path.name}: its Result names `{m.group(1)}`, another file")
        for field in ("Kind", "Query", "Run As", "Completeness", "Places"):
            if f"\n    **{field}:**" not in text:
                problems.append(f"{path.name}: it holds no {field}")
        content = hashlib.sha256(text[m.end():].encode()).hexdigest()[:8]
        if not path.stem.endswith("-" + content):
            problems.append(f"{path.name}: its content was changed since the search wrote it, since its name no longer ends with the hash of its content, {content}")
        return problems

    def summary(self, root):
        where = self.path.relative_to(root).as_posix() if self.path else "(not written)"
        count = len(self.places)
        out = [f"{where}", f"{count} place{'' if count == 1 else 's'}, {self.completeness}: places to read, never findings"]
        if count <= FEW:
            out += ["  " + p for p in self.places]
        return "\n".join(out)


# ---------------------------------------------------------------------------------------------------------------------
# The index and the searches

class Search:
    """The search over one project. `Search(root)` checks everything the search requires, then brings the index up to
    date. `cover`, given by a test, names the files to cover in place of the canon's listing."""

    def __init__(self, root, cover=None, scratch=None, quiet=False):
        self.root = Path(root).resolve()
        check_requirements(self.root)
        self.scratch = Path(scratch) if scratch else self.root / SCRATCH
        self.cover, self.quiet, self.embedder = cover, quiet, None
        self.read_count, self.built, self.seconds, self._lineages = 0, False, 0.0, {}
        self.scratch.mkdir(parents=True, exist_ok=True)
        self.db = self._open()
        self.update()

    # -- the files a search covers

    def covered(self):
        """-> [path from the root] of every file the search covers: the files of each kind the canon names for the
        scope, the working files aside, read from the scope's own listing, and the stack's code roots less the paths
        it excludes. It reads no version control. A cache a tool leaves among them is not listed."""
        if self.cover is not None:
            return sorted(self.cover)
        out = set()
        # @canon-spec specs/methodology/scope/what-spec-of-record-governs.md § What Spec of Record Governs
        for place in spec_text.scope_paths(self.root):
            base = self.root / place
            if base.is_file():
                out.add(place)
            elif base.is_dir():
                out.update(self._under(base))
        stack = code_checks.code_roots(self.root)
        if stack:
            out.update(rel for _, rel in code_checks.code_files(self.root, *stack) if "__pycache__" not in rel.split("/"))
        return sorted(out)

    def _under(self, base):
        for folder, folders, files in os.walk(base):
            folders[:] = sorted(d for d in folders if d != "__pycache__")
            for name in sorted(files):
                if not name.endswith((".pyc", ".pyo")):
                    yield (Path(folder) / name).relative_to(self.root).as_posix()

    # -- the index

    def _open(self):
        import sqlite_vec
        db = sqlite3.connect(self.scratch / "index.sqlite")
        db.enable_load_extension(True)
        sqlite_vec.load(db)
        db.enable_load_extension(False)
        db.execute("create table if not exists meta(key text primary key, value text)")
        row = db.execute("select value from meta where key='schema'").fetchone()
        if not row or row[0] != SCHEMA + "/" + MODEL:
            for (name,) in db.execute("select name from sqlite_master where type='table' and name not like 'sqlite_%' and name != 'meta'").fetchall():
                try:
                    db.execute(f"drop table if exists {name}")
                except sqlite3.OperationalError:
                    pass
            db.executescript(f"""
                create table files(path text primary key, sha text, size integer, mtime_ns integer);
                create table contents(sha text primary key, kind text, language text, note text);
                create table lines(sha text, n integer, text text, fenced integer, primary key(sha, n));
                create virtual table terms using fts5(norm, sha unindexed, n unindexed, tokenize='porter unicode61');
                create virtual table term_pairs using fts5(norm, sha unindexed, n unindexed, tokenize='porter unicode61');
                create table headings(sha text, lineage text, occurrence integer, level integer, line integer, own_end integer, subtree_end integer);
                create table citations(sha text, line integer, host text, form text, fenced integer, written text, path text, lineage text, key text, unit text);
                create table units(sha text, name text, kind text, line_start integer, line_end integer);
                create table structures(sha text, structure text, name text, unit text, line integer);
                create table passages(id integer primary key, sha text, lineage text, line_start integer, line_end integer, text text, text_sha text);
                create virtual table passage_terms using fts5(norm, pid unindexed, tokenize='porter unicode61');
                create table embeddings(text_sha text primary key, vector blob);
                create virtual table passage_vectors using vec0(embedding float[{DIMENSIONS}] distance_metric=cosine);
                create index files_sha on files(sha);
                create index headings_sha on headings(sha);
                create index citations_target on citations(path, lineage);
                create index citations_sha on citations(sha);
                create index structures_name on structures(name, structure);
                create index passages_sha on passages(sha);
                create index passages_text on passages(text_sha);
                create table term_rows(sha text, name text, first integer, last integer);
                create index term_rows_sha on term_rows(sha);
                create index units_sha on units(sha);
                create index structures_sha on structures(sha);
            """)
            db.execute("insert or replace into meta values('schema', ?)", (SCHEMA + "/" + MODEL,))
            db.commit()
            self.built = True
        return db

    def update(self):
        """Bring the index up to date: a file is read only where its size or the time it was changed differs from what
        the index holds, and parsed only where its content is new to the index."""
        started = time.perf_counter()
        db, held = self.db, {p: (sha, size, mtime) for p, sha, size, mtime in self.db.execute("select path, sha, size, mtime_ns from files")}
        listed, new, left = self.covered(), [], set()
        for rel in listed:
            try:
                stat = (self.root / rel).stat()
            except OSError:
                continue
            was = held.get(rel)
            if was and was[1] == stat.st_size and was[2] == stat.st_mtime_ns:
                continue
            data = (self.root / rel).read_bytes()
            self.read_count += 1
            sha = hashlib.sha256(data.replace(b"\r\n", b"\n")).hexdigest()
            if not db.execute("select 1 from contents where sha=?", (sha,)).fetchone():
                self._index(sha, rel, data)
                new.append(sha)
            if was:
                left.add(was[0])
            db.execute("insert or replace into files values(?,?,?,?)", (rel, sha, stat.st_size, stat.st_mtime_ns))
        gone = set(held) - set(listed)
        left.update(held[p][0] for p in gone)
        db.executemany("delete from files where path=?", [(p,) for p in gone])
        if self.read_count or gone:
            # only the content a changed or removed file held is looked at again, so this costs what changed
            for sha in left:
                if not db.execute("select 1 from files where sha=? limit 1", (sha,)).fetchone():
                    self._drop(sha)
            self._embed(new)
            for stale in (self.scratch / "results").glob("*.md"):
                stale.unlink()
        db.commit()
        self.seconds = time.perf_counter() - started
        if not self.quiet:
            if self.built:
                print(f"index: built whole from {len(listed)} files in {self.seconds:.1f} seconds", file=sys.stderr)
            else:
                print(f"index: {len(listed)} files covered, {self.read_count} read again, {self.seconds:.2f} seconds", file=sys.stderr)

    def _drop(self, sha):
        """Take out of the index what one content gave, no file holding that content any more."""
        db = self.db
        passages = db.execute("select id, text_sha from passages where sha=?", (sha,)).fetchall()
        db.executemany("delete from passage_vectors where rowid=?", [(pid,) for pid, _ in passages])
        db.executemany("delete from passage_terms where rowid=?", [(pid,) for pid, _ in passages])
        for name, first, last in db.execute("select name, first, last from term_rows where sha=?", (sha,)).fetchall():
            db.execute(f"delete from {name} where rowid between ? and ?", (first, last))
        for table in ("contents", "lines", "term_rows", "headings", "citations", "units", "structures", "passages"):
            db.execute(f"delete from {table} where sha=?", (sha,))
        db.executemany("delete from embeddings where text_sha=? and not exists (select 1 from passages where text_sha=?)", [(ts, ts) for ts in {ts for _, ts in passages}])

    def _terms(self, name, sha, rows):
        """Index the words of a content's lines under row numbers of its own run, kept so the rows are found again by
        their numbers when the content leaves the index."""
        db = self.db
        first = (db.execute("select value from meta where key=?", (name,)).fetchone() or ("0",))[0]
        first = int(first) + 1
        db.executemany(f"insert into {name}(rowid, norm, sha, n) values(?,?,?,?)", [(first + i, norm, sha, n) for i, (norm, n) in enumerate(rows)])
        if rows:
            db.execute("insert into term_rows values(?,?,?,?)", (sha, name, first, first + len(rows) - 1))
            db.execute("insert or replace into meta values(?,?)", (name, str(first + len(rows) - 1)))

    def _index(self, sha, rel, data):
        db, suffix, stem = self.db, Path(rel).suffix.lower(), Path(rel).stem
        try:
            text = data.decode("utf-8-sig").replace("\r\n", "\n").replace("\r", "\n")
        except UnicodeDecodeError:
            db.execute("insert into contents values(?,?,?,?)", (sha, "binary", "", "it is no text, and nothing in it is searched"))
            return
        lines = text.split("\n")
        kind, language, note, fenced = "text", "", "", [0] * len(lines)
        if suffix == ".md":
            kind = "markdown"
            rows = markdown_lines(strip_links(text))
            fenced = [int(r[1]) for r in rows]
            heads = markdown_headings(rows)
            db.executemany("insert into headings values(?,?,?,?,?,?,?)", [(sha,) + h for h in heads])
            db.executemany("insert into citations values(?,?,?,?,?,?,?,?,?,'')", [(sha,) + c for c in markdown_citations(rows, heads)])
            db.executemany("insert into passages(sha, lineage, line_start, line_end, text, text_sha) values(?,?,?,?,?,?)",
                           [(sha, p[0], p[1], p[2], p[3], hashlib.sha256(p[3].encode()).hexdigest()) for p in markdown_passages(rows, heads)])
        elif suffix in LANGUAGES or suffix in NO_UNITS or self._is_code(rel):
            kind, language = "code", LANGUAGES.get(suffix, "")
            comments = None
            if language == "python":
                units, structures, note = read_python(text, stem)
                comments = python_comment_lines(text)
            elif language:
                units, structures, note, comments = read_tree_sitter(text, stem, language)
            else:
                units, structures = [(stem, "file", 1, len(lines))], []
                note = (f"{NO_UNITS[suffix]} has no units, so the file is one unit and no structure is searched in it" if suffix in NO_UNITS
                        else f"the search has no parser for a {suffix or 'file of this kind'} file, so the file is one unit and no structure is searched in it")
            db.executemany("insert into units values(?,?,?,?,?)", [(sha,) + u for u in units])
            db.executemany("insert into structures values(?,?,?,?,?)", [(sha,) + s for s in structures])
            for line, written, path, lineage, key in comment_annotations(lines):
                if comments is not None and line not in comments:
                    continue
                db.execute("insert into citations values(?,?,?,?,?,?,?,?,?,?)", (sha, line, "", "annotation", 0, written, path, lineage, key, unit_under(units, line)))
            if language == "python":
                try:
                    for node in ast.walk(ast.parse(text)):
                        doc = ast.get_docstring(node) if isinstance(node, (ast.Module, ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)) else None
                        for piece in split_passage(squeeze(doc)) if doc else []:
                            first = getattr(node, "lineno", 1)
                            db.execute("insert into passages(sha, lineage, line_start, line_end, text, text_sha) values(?,?,?,?,?,?)",
                                       (sha, "", first, first + doc.count("\n") + 1, piece, hashlib.sha256(piece.encode()).hexdigest()))
                except (SyntaxError, ValueError):
                    pass
        db.execute("insert into contents values(?,?,?,?)", (sha, kind, language, note))
        db.executemany("insert into lines values(?,?,?,?)", [(sha, i + 1, line, fenced[i]) for i, line in enumerate(lines)])
        self._terms("terms", sha, [(normalize(line), i + 1) for i, line in enumerate(lines) if line.strip()])
        self._terms("term_pairs", sha, [(normalize(line + " " + lines[i + 1]), i + 1) for i, line in enumerate(lines[:-1]) if line.strip() and lines[i + 1].strip()])
        db.executemany("insert into passage_terms(rowid, norm, pid) values(?,?,?)",
                       [(pid, normalize(t), pid) for pid, t in db.execute("select id, text from passages where sha=?", (sha,)).fetchall()])

    def _is_code(self, rel):
        if self.cover is not None:
            return Path(rel).suffix.lower() not in ("", ".txt")
        if self._roots is None:
            stack = code_checks.code_roots(self.root)
            self._roots = stack[0] if stack else []
        return rel.startswith(".ai/skills/") and "/scripts/" in rel or any(rel.startswith(r + "/") for r in self._roots)

    _roots = None

    def _embed(self, new):
        """Give each passage of the contents new to the index its vector: a text the index already holds a vector for
        is not run through the model again."""
        db, todo = self.db, {}
        for sha in new:
            for text, text_sha in db.execute("select text, text_sha from passages where sha=? and text_sha not in (select text_sha from embeddings)", (sha,)):
                todo[text_sha] = text
        if todo:
            db.executemany("insert or replace into embeddings values(?,?)", list(zip(todo, self._vectors(list(todo.values())))))
        for sha in new:
            db.execute("insert into passage_vectors(rowid, embedding) select p.id, e.vector from passages p join embeddings e on e.text_sha = p.text_sha where p.sha=?", (sha,))

    def _vectors(self, texts):
        import sqlite_vec
        if self.embedder is None:
            from fastembed import TextEmbedding
            os.environ.setdefault("HF_HUB_OFFLINE", "1")
            self.embedder = TextEmbedding(model_name=MODEL, cache_dir=str(MODEL_FOLDER), local_files_only=True)
        return [sqlite_vec.serialize_float32([float(x) for x in v]) for v in self.embedder.embed(texts)]

    # -- helpers the searches share

    def _narrow(self, narrowed):
        return [p.replace("\\", "/").strip("/") for p in narrowed or []]

    def _within(self, path, narrowed):
        return not narrowed or any(path == n or path.startswith(n + "/") for n in narrowed)

    def _place(self, path, line, end=None):
        """-> a place to read: a citation of the section or the file holding the line, with its lines."""
        row = self.db.execute("select h.lineage from files f join headings h on h.sha = f.sha where f.path=? and h.line<=? and h.lineage != '' "
                              "order by h.line desc limit 1", (path, line)).fetchone()
        cite = path + (" § " + row[0] if row else "")
        return f"`{cite}` " + (f"line {line}" if end in (None, line) else f"lines {line}-{end}")

    def _finish(self, result):
        result.write(self.scratch / "results")
        return result

    def _resolve(self, citation):
        """-> (path, lineage, key, why): the place a citation names among the files covered, or why it names none."""
        parsed = parse_citation(citation.strip().strip("`"))
        if not parsed:
            return None, None, None, "it is not in a citation's form"
        path, lineage, key = parsed
        if path is None:
            return None, None, None, "it names no file, and a search has no file of its own to read a same-file citation against"
        if not self.db.execute("select 1 from files where path=? or path like ?", (path, path + "/%")).fetchone():
            return path, lineage, key, f"`{path}` is not among the files the search covers"
        if lineage and not self.db.execute("select 1 from files f join headings h on h.sha=f.sha where f.path=? and h.lineage=?", (path, lineage)).fetchone():
            return path, lineage, key, f"`{path}` holds no section `{lineage}`"
        return path, lineage, key, None

    # -- who cites a place

    def citers(self, citation, narrowed=None):
        return self._finish(self._citing(citation, narrowed))

    def _citing(self, citation, narrowed=None):
        """-> the result of a search for the places citing a place, not yet written as a file."""
        narrowed = self._narrow(narrowed)
        path, lineage, key, why = self._resolve(citation)
        if why and path is None:
            return Result("citers", citation, narrowed, "as asked", "complete", [], [f"the citation does not resolve: {why}"])
        columns = "select f.path, c.line, c.form, c.fenced, c.written, coalesce(c.path, f.path), c.lineage, c.key, c.unit from citations c join files f on f.sha = c.sha "
        rows = sorted(set(
            self.db.execute(columns + "where c.path = ?", (path,)).fetchall()
            + self.db.execute(columns + "where c.path > ? and c.path < ?", (path + "/", path + "0")).fetchall()
            + self.db.execute(columns + "where c.path is null and c.sha in (select sha from files where path = ?)", (path,)).fetchall()),
            key=lambda r: (r[0], r[1], r[4], r[2]))
        places, notes, related = [], [], []
        for host, line, form, fenced, written, target, tl, tk, unit in rows:
            if not self._within(host, narrowed):
                continue
            how = None
            if form == "bare":
                tl, tk = self._bare(target, tl)
                if tl is None:
                    continue
                written = target + " § " + tl + (f" [{tk}]" if tk else "")
            if target == path and tl == lineage and (tk or None) == key:
                how = "cites it"
            elif target == path and tl == lineage and key and not tk:
                how = "cites the section holding it"
            elif form == "label" and target == path and not lineage:
                how = "cites it"
            elif target == path and tl == lineage and key is None and tk:
                how = f"cites a part of it, `[{tk}]`"
            elif target == path and lineage and tl.startswith(lineage + " § "):
                how = "cites a section within it"
            elif target == path and lineage and tl and lineage.startswith(tl + " § "):
                how = "cites a section above it"
            elif target == path and lineage and not tl:
                how = "cites its file"
            elif target == path and not lineage and tl:
                how = "cites a section within it"
            elif target != path and target.startswith(path + "/"):
                how = "cites a file within it"
            if how is None:
                continue
            place = self._place(host, line)
            marks = [m for m in ("a `technical-specs` label, not a citation" if form == "label" else "",
                                 f"an annotation over the unit `{unit}`" if form == "annotation" and unit else ("an annotation" if form == "annotation" else ""),
                                 "stands in a fenced block" if fenced else "") if m]
            if how == "cites it":
                places.append(place)
                if marks:
                    notes.append(f"{place}: {', '.join(marks)}")
            else:
                related.append(f"{place}: {how}{', ' + ', '.join(marks) if marks else ''}, as `{written}`")
        if why:
            notes.insert(0, f"the citation does not resolve: {why}")
        if related:
            notes.append("Related places, each told apart from the places citing it:")
            notes += related
        return Result("citers", citation, narrowed, "as asked", "complete", places, notes)

    def _bare(self, path, rest):
        """-> (lineage, key) a citation written bare names: the longest heading path of the file it names that the rest
        of its line opens with, and the key standing in brackets right after it, or (None, None) where it opens with
        none."""
        if path not in self._lineages:
            self._lineages[path] = sorted((r[0] for r in self.db.execute(
                "select distinct h.lineage from files f join headings h on h.sha=f.sha where f.path=? and h.lineage != ''", (path,))), key=len, reverse=True)
        for lineage in self._lineages[path]:
            if rest == lineage or (rest.startswith(lineage) and not (rest[len(lineage)].isalnum() or rest[len(lineage):].startswith(" § "))):
                key = re.match(r" \[([^\]]*)\]", rest[len(lineage):])
                return lineage, ("; ".join(squeeze(p) for p in key.group(1).split(";")) if key else None)
        return None, None

    # -- which lines a citation names

    def lines(self, citation, narrowed=None):
        path, lineage, key, why = self._resolve(citation)
        if why:
            return self._finish(Result("lines", citation, [], "as asked", "complete", [], [f"the citation does not resolve: {why}"]))
        if (self.root / path).is_dir():
            return self._finish(Result("lines", citation, [], "as asked", "complete", [f"`{path}/`"], ["it names a folder, which holds no lines of its own"]))
        heads = self.db.execute("select h.lineage, h.occurrence, h.level, h.line, h.own_end, h.subtree_end from files f join headings h on h.sha=f.sha "
                                "where f.path=? order by h.line", (path,)).fetchall()
        total = self.db.execute("select count(*) from files f join lines l on l.sha=f.sha where f.path=?", (path,)).fetchone()[0]
        if not heads:
            return self._finish(Result("lines", citation, [], "as asked", "complete", [f"`{path}` lines 1-{total}"]))
        mine = [h for h in heads if h[0] == lineage]
        head, notes = mine[0], []
        if len(mine) > 1:
            notes.append(f"the path stands {len(mine)} times in the file, and the first is the one a citation names")
        cite = f"`{path}{' § ' + lineage if lineage else ''}`"
        places = []
        if key:
            span = self._part(path, head, key)
            if not span:
                return self._finish(Result("lines", citation, [], "as asked", "complete", [], [f"the citation does not resolve: {cite} holds no part `[{key}]`"]))
            places.append(f"`{path} § {lineage} [{key}]` " + (f"line {span[0]}" if span[0] == span[1] else f"lines {span[0]}-{span[1]}"))
            notes.append(f"{cite} lines {head[3]}-{head[5] - 1}: the section holding the part")
        else:
            places.append(f"{cite} lines {head[3]}-{head[4] - 1}")
            if lineage and head[5] != head[4]:
                notes.append(f"{cite} lines {head[3]}-{head[5] - 1}: its whole subtree")
        segments = lineage.split(" § ") if lineage else []
        for depth in range(len(segments) - 1, -1, -1):
            above = " § ".join(segments[:depth])
            h = next((x for x in heads if x[0] == above), None)
            if h is None:
                continue
            label = f"`{path}{' § ' + above if above else ''}`"
            if depth == len(segments) - 1 and above:
                notes.append(f"{label} lines {h[3]}-{h[5] - 1}: its parent whole")
            if h[4] > h[3]:
                notes.append(f"{label} lines {h[3]}-{h[4] - 1}: " + ("its file's text before its first section" if not above else "an ancestor's text before its first child heading"))
        return self._finish(Result("lines", citation, [], "as asked", "complete", places, notes))

    def _part(self, path, head, key):
        """-> (first line, last line) of the keyed part a citation names within a section: a record, by its
        identifying fields, or a table's row, by the columns its key names."""
        pairs = [tuple(squeeze(x) for x in p.split(":", 1)) for p in key.split("; ") if ":" in p]
        if not pairs:
            return None
        rows = [(n, strip_links(text)) for n, text in self.db.execute(
            "select l.n, l.text from files f join lines l on l.sha=f.sha where f.path=? and l.n>=? and l.n<? order by l.n", (path, head[3], head[5]))]
        table = None
        if "." in pairs[0][0]:
            table = pairs[0][0].split(".", 1)[0]
            pairs = [(k.split(".", 1)[-1], v) for k, v in pairs]
        field = re.compile(r"^(\s*)(- )?\*\*" + re.escape(pairs[0][0]) + r":\*\* (.*?)(?: \\)?$")
        for i, (n, text) in enumerate(rows):
            m = None if table else field.match(text)
            if m and m.group(2) and squeeze(m.group(3)) == pairs[0][1]:
                indent, end = len(m.group(1)), n
                for n2, t2 in rows[i + 1:]:
                    if t2.strip() and len(t2) - len(t2.lstrip()) <= indent:
                        break
                    if t2.strip():
                        end = n2
                item = "\n".join(t for nn, t in rows if n <= nn <= end)
                if all(re.search(r"\*\*" + re.escape(k) + r":\*\* " + re.escape(v) + r"(?: \\)?\s*$", item, re.M) for k, v in pairs[1:]):
                    return n, end
        named, header = None, None
        for n, text in rows:
            t = re.match(r"^\*\*Table Name:\*\* (.*?)(?: \\)?$", text.strip())
            if t:
                named = squeeze(t.group(1))
            if not text.strip().startswith("|"):
                header = None
                continue
            cells = [squeeze(c) for c in text.strip().strip("|").split("|")]
            if header is None:
                header = cells
                continue
            if set(text.strip()) <= set("|-: "):
                continue
            if table and named != table:
                continue
            if all(k in header and header.index(k) < len(cells) and cells[header.index(k)].strip("`") == v.strip("`") for k, v in pairs):
                return n, n
        return None

    # -- where a term is used

    def other_names(self, term):
        """-> the other names the glossary gives a term: its abbreviation and each name its entry is also called."""
        rows = self.db.execute("select l.text from files f join lines l on l.sha=f.sha where f.path='specs/methodology/glossary/glossary.md' and l.text like '|%'").fetchall()
        wanted = squeeze(term).lower()
        for (text,) in rows:
            cells = [squeeze(c) for c in strip_links(text).strip().strip("|").split("|")]
            if len(cells) < 3 or cells[0] in ("Term", "") or set(cells[0]) <= set("-: "):
                continue
            names = [cells[0]] + ([cells[1]] if cells[1] else [])
            also = re.search(r"Also called ([^.]*)\.", cells[2])
            names += [squeeze(n) for n in also.group(1).split(",")] if also else []
            if wanted in [n.lower() for n in names]:
                return [n for n in names if n.lower() != wanted]
        return []

    def terms(self, term, narrowed=None):
        narrowed = self._narrow(narrowed)
        forms = [squeeze(term)] + self.other_names(term)
        found = {}
        for form in forms:
            query = phrase(form)
            if not query:
                continue
            alone = set(self.db.execute("select f.path, t.n from terms t join files f on f.sha = t.sha where terms match ?", (query,)))
            # a phrase standing only where a line is read with the line after it is broken across the two
            broken = {(path, n) for path, n in self.db.execute("select f.path, t.n from term_pairs t join files f on f.sha = t.sha where term_pairs match ?", (query,))
                      if (path, n) not in alone and (path, n + 1) not in alone}
            for path, n in alone | broken:
                if self._within(path, narrowed):
                    found.setdefault((path, n), form)
        places = [self._place(path, n) for path, n in sorted(found)]
        run = ("each form searched as a phrase, every word reduced to its stem and every identifier split into its words: "
               + ", ".join(f"`{f}`" for f in forms) + (". The glossary gives the term no other name" if len(forms) == 1 else ". The names after the first are the glossary's other names for it"))
        return self._finish(Result("terms", term, narrowed, run, "complete", places))

    # -- which places match a pattern

    def pattern(self, expression, narrowed=None):
        narrowed = self._narrow(narrowed)
        regex = re.compile(expression, re.M)
        places = []
        for path, sha in self.db.execute("select path, sha from files order by path").fetchall():
            if not self._within(path, narrowed):
                continue
            lines = [r[0] for r in self.db.execute("select text from lines where sha=? order by n", (sha,))]
            if not lines:
                continue
            text, starts, at = "\n".join(lines), [], 0
            for line in lines:
                starts.append(at)
                at += len(line) + 1
            seen = set()
            for m in regex.finditer(text):
                first = max(i for i, s in enumerate(starts) if s <= m.start()) + 1
                last = max(i for i, s in enumerate(starts) if s <= max(m.start(), m.end() - 1)) + 1
                if (first, last) not in seen:
                    seen.add((first, last))
                    places.append(self._place(path, first, last))
        return self._finish(Result("pattern", expression, narrowed, "as asked, in Python's `re` syntax with `^` and `$` matching at each line, over each file's whole text. A pattern is for a fault of form: a term, a citer or a structure has a search of its own",
                                   "complete", places))

    # -- which units of code hold a structure

    def code_structure(self, structure, name, narrowed=None):
        narrowed = self._narrow(narrowed)
        if structure not in STRUCTURES:
            raise ValueError(f"no structure `{structure}`: a structure is one of {', '.join(STRUCTURES)}")
        places, notes = [], []
        if structure == "annotated-with":
            rows = self.db.execute("select f.path, c.line, c.unit, c.written from citations c join files f on f.sha=c.sha where c.form='annotation' and c.fenced=0 "
                                   "and c.written like ? order by f.path, c.line", ("%" + name + "%",)).fetchall()
            for path, line, unit, written in rows:
                if self._within(path, narrowed):
                    places.append(f"`{path}` line {line}")
                    notes.append(f"`{path}` line {line}: the unit `{unit}`, annotated with `{written}`")
        else:
            wanted = [structure] + (["calls"] if structure == "constructs" else [])
            classes = {r[0] for r in self.db.execute("select distinct s.name from structures s join units u on u.sha=s.sha and u.name=s.unit "
                                                     "where s.structure='defines' and u.kind in ('class','struct','record')")}
            rows = self.db.execute(f"select f.path, s.line, s.unit, s.structure, c.language from structures s join files f on f.sha=s.sha join contents c on c.sha=s.sha "
                                   f"where s.name=? and s.structure in ({','.join('?' * len(wanted))}) order by f.path, s.line, s.unit", [name] + wanted).fetchall()
            seen = set()
            for path, line, unit, found, language in rows:
                if not self._within(path, narrowed) or (path, line, unit) in seen:
                    continue
                if structure == "constructs" and found == "calls" and not (name in classes or (language == "python" and name[:1].isupper())):
                    continue
                seen.add((path, line, unit))
                places.append(f"`{path}` line {line}")
                notes.append(f"`{path}` line {line}: the unit `{unit}`")
            if structure in ("extends", "implements") and any(r[4] == "c_sharp" for r in rows):
                notes.append("C#'s syntax does not tell a class extended from an interface implemented, so each name in a type's base list is listed for both.")
        blind = self.db.execute("select f.path, c.note from files f join contents c on c.sha=f.sha where c.kind='code' and c.note != '' order by f.path").fetchall()
        blind = [(p, n) for p, n in blind if self._within(p, narrowed)]
        if blind:
            notes.append("Files no structure was searched in, or not wholly:")
            notes += [f"`{p}`: {n}" for p, n in blind]
        run = "as asked, matched on the name as the code writes it, in no comment and no string. The answer holds what the syntax shows, and is blind to a call made by reflection or by a name built as the code runs"
        return self._finish(Result("code structure", f"{structure} {name}", narrowed, run, "complete", places, notes))

    # -- which places say the same as a passage

    def meaning(self, passage, narrowed=None):
        narrowed = self._narrow(narrowed)
        asked, own, notes = squeeze(passage.strip("`")) if passage.strip().startswith("`") else squeeze(passage), None, []
        texts = [asked]
        if parse_citation(asked) and parse_citation(asked)[0]:
            path, lineage, key, why = self._resolve(asked)
            if why:
                return self._finish(Result("meaning", passage, narrowed, "as asked", "ranked", [], [f"the citation does not resolve: {why}"]))
            own = (path, lineage)
            texts = [r[0] for r in self.db.execute("select p.text from passages p join files f on f.sha=p.sha where f.path=? and p.lineage=? order by p.line_start", (path, lineage))]
            if not texts:
                return self._finish(Result("meaning", passage, narrowed, "as asked", "ranked", [], ["the place it names holds no passage of prose to compare"]))
        scores = {}
        for text, vector in zip(texts, self._vectors(texts)):
            by_words = []
            words = re.findall(r"[^\W_]+", normalize(text))
            if words:
                query = " OR ".join('"' + w + '"' for w in dict.fromkeys(words))
                by_words = [r[0] for r in self.db.execute("select pid from passage_terms where passage_terms match ? order by bm25(passage_terms) limit ?", (query, CANDIDATES * 4))]
            by_vectors = [r[0] for r in self.db.execute("select rowid from passage_vectors where embedding match ? and k = ? order by distance", (vector, CANDIDATES * 4))]
            for ranking in (by_words, by_vectors):
                rank = 0
                for pid in ranking:
                    path, lineage = self.db.execute("select f.path, p.lineage from passages p join files f on f.sha=p.sha where p.id=? order by f.path limit 1", (pid,)).fetchone() or (None, None)
                    if path is None or not self._within(path, narrowed) or (path, lineage) == own:
                        continue
                    rank += 1
                    if rank > CANDIDATES:
                        break
                    scores[pid] = scores.get(pid, 0.0) + 1.0 / (FUSION + rank)
        places, seen = [], set()
        for pid in sorted(scores, key=lambda p: (-scores[p], p)):
            for path, start, end in self.db.execute("select f.path, p.line_start, p.line_end from passages p join files f on f.sha=p.sha where p.id=? order by f.path", (pid,)):
                place = self._place(path, start, end)
                if place not in seen and self._within(path, narrowed):
                    seen.add(place)
                    places.append(place)
            if len(places) >= RANKED * 2:
                break
        if own:
            citing = {p.split("` ")[0] for p in self._citing(f"{own[0]}{' § ' + own[1] if own[1] else ''}").places}
            apart = [p for p in places if p.split("` ")[0] in citing]
            places = [p for p in places if p not in apart]
            if apart:
                notes.append("Places whose section cites the passage's own, listed apart, since each may rely on it and not restate it:")
                notes += apart
        places = places[:RANKED]
        run = (f"each passage of what was asked ranked against every passage by its words and by the vectors of the model `{MODEL}`, run on this machine, the two rankings fused, and the first {RANKED} given")
        return self._finish(Result("meaning", passage, narrowed, run, "ranked", places, notes))


# ---------------------------------------------------------------------------------------------------------------------
# The entry script's actions

USAGE = f"""usage: {SKILL}.py ACTION [--paths PATH ...]

Each action answers one question over the files of Spec of Record's scope and the code, and writes its result as a
file under {SCRATCH}/results/. Every search first checks everything the search requires.

  --show-citers CITATION                 every place citing a section, a keyed part or a file
  --show-lines CITATION                  the lines a citation names
  --show-term-uses TERM                  every place using a word, a phrase or an identifier, in every form it takes
  --show-code-structure STRUCTURE NAME   every unit of code holding a structure: {', '.join(STRUCTURES)}
  --show-similar-passages PASSAGE        the places stating the same as a passage, or as a cited section, in other words
  --show-pattern-matches EXPRESSION      every place a regular expression matches, for a fault of form
  --check-requirements                   what the search requires, and whether each is present
  --check-result FILE                    whether a result's file is in its form and its content is as the search wrote it
  --install-model                        download the model's files, the one action that reaches the network

  --paths PATH ...                       answer over these files and folders alone
"""


def main(argv, root=None):
    root = Path(root).resolve() if root else Path(__file__).resolve().parents[3]
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8")
    args = list(argv[1:])
    narrowed = []
    if "--paths" in args:
        at = args.index("--paths")
        narrowed = [a for a in args[at + 1:] if not a.startswith("--")]
        del args[at:at + 1 + len(narrowed)]
        if not narrowed:
            print(USAGE)
            return 2
    arity = {"--show-citers": 1, "--show-lines": 1, "--show-term-uses": 1, "--show-code-structure": 2, "--show-similar-passages": 1,
             "--show-pattern-matches": 1, "--check-requirements": 0, "--install-model": 0, "--check-result": 1}
    if not args or args[0] not in arity or len(args) != 1 + arity[args[0]]:
        print(USAGE)
        return 2
    action, values = args[0], args[1:]
    if action == "--check-result":
        if not Path(values[0]).is_file():
            print(f"{SKILL}: no file {values[0]}")
            return 2
        problems = Result.check(values[0])
        print("\n".join(problems) if problems else f"{Path(values[0]).name}: a search's result in its form, its content as the search wrote it")
        return 1 if problems else 0
    if action == "--check-requirements":
        text, count = requirements_report(root)
        print(text)
        return 1 if count else 0
    try:
        if action == "--install-model":
            print(f"{SKILL}: the model's files are in {install_model(root).relative_to(HOME).as_posix()}")
            return 0
        search = Search(root)
        if action == "--show-citers":
            result = search.citers(values[0], narrowed)
        elif action == "--show-lines":
            result = search.lines(values[0], narrowed)
        elif action == "--show-term-uses":
            result = search.terms(values[0], narrowed)
        elif action == "--show-code-structure":
            result = search.code_structure(values[0], values[1], narrowed)
        elif action == "--show-similar-passages":
            result = search.meaning(values[0], narrowed)
        else:
            result = search.pattern(values[0], narrowed)
    except MissingRequirements as e:
        print(e)
        return 1
    except (ValueError, re.error) as e:
        print(f"{SKILL}: {e}")
        return 2
    print(result.summary(root))
    for note in result.notes[:FEW] if len(result.places) <= FEW else []:
        print("  note: " + note)
    return 0
