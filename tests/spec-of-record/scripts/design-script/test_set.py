"""What the set says of its script: FORM_FILES, held to the code the skills share and to the set's own files as they
stand, so what a project of the set is given of the canon is what runs the set's tests.

No entry script reaches this, so the tests read the shared code's and the set's own source.
"""
import ast
import re

from design_script_set import (CHECKOUT, COMPARISON, FORMS_ALONE, FORM_FILES, LIB, Project, SET, within_form_files)

CANON_FILE = re.compile(r"specs/(?:AGENTS\.md|architecture\.md|index\.md|main\.md|methodology(?:/[\w/.-]*)?)")


def canon_paths(folder, pattern):
    """-> {a path of the canon: [where the code holds it]} for each string of the Python files of a folder that is the
    path of a file or a folder of the canon and nothing more, a path the code reads or copies the file by. A path with
    a section after it names a rule in a message, a path in a docstring describes, and a path a comparison tests
    another path against sorts files by their kind: none of the three reads the file."""
    out = {}
    for module in sorted((CHECKOUT / folder).glob(pattern)):
        tree = ast.parse(module.read_text(encoding="utf-8"))
        compared = {id(n) for node in ast.walk(tree) if isinstance(node, ast.Compare) for n in ast.walk(node)}
        described = {id(n.body[0].value) for n in ast.walk(tree) if isinstance(n, (ast.Module, ast.FunctionDef, ast.ClassDef)) and n.body
                     and isinstance(n.body[0], ast.Expr) and isinstance(n.body[0].value, ast.Constant)}
        for node in ast.walk(tree):
            if isinstance(node, ast.Constant) and isinstance(node.value, str) and CANON_FILE.fullmatch(node.value) and id(node) not in compared | described:
                out.setdefault(node.value, []).append("%s line %d" % (module.name, node.lineno))
    return out


def test_each_file_of_the_canon_the_shared_code_reads_lies_within_form_files(check):
    # a path the code holds for a file the specs may hold and this checkout's do not, as specs/main.md, names no file
    # a project could be given: it is held to FORM_FILES from the day the file stands
    read = {path: where for path, where in canon_paths(LIB, "*.py").items() if (CHECKOUT / path).exists()}
    check("the code the skills share holds the paths of files of the canon to read them by", len(read) >= 3, read)
    for path, where in sorted(read.items()):
        check("the shared code reads %s, which lies within FORM_FILES" % path, within_form_files(path), "its path is held at " + ", ".join(where))
    for path in FORM_FILES:
        stands = (CHECKOUT / path).is_dir() if path.endswith("/") else (CHECKOUT / path).is_file()
        check("FORM_FILES names %s, which stands in the checkout" % path, stands)
    declared = {getattr(node.targets[0], "id", "") for node in ast.parse((CHECKOUT / COMPARISON).read_text(encoding="utf-8")).body if isinstance(node, ast.Assign)}
    check("the kept comparison names no files of its own as its script's: the set's conftest.py names them", not declared & {"SCRIPT_FILES", "FORM_FILES", "ACTIONS_IN"}, sorted(declared))


def test_no_project_is_given_a_file_of_the_canon_form_files_does_not_name(check):
    for path in FORMS_ALONE:
        check("%s, which a project takes where it needs the forms alone, lies within FORM_FILES and stands" % path, within_form_files(path) and (CHECKOUT / path).is_file())
    # each path of the canon the set's own code holds, to copy into a project or to change in one, that stands in
    # the checkout: a path that does not stand there names a file a test wrote for its own project
    held = {path: where for path, where in canon_paths(SET, "*.py").items() if (CHECKOUT / path).exists()}
    check("the set's code holds paths of the canon to give a project", set(FORM_FILES) <= set(held), sorted(held))
    for path, where in sorted(held.items()):
        check("the set's code holds %s, which lies within FORM_FILES" % path, within_form_files(path), "its path is held at " + ", ".join(where))
    try:
        Project("given more", canon=("specs/application/index.md",))
        refused = "the project was made"
    except AssertionError as said:
        refused = str(said)
    check("the builder of a project refuses a file of the specs FORM_FILES does not name", "FORM_FILES does not name: specs/application/index.md" in refused, refused)
