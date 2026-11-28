"""The check that code names the canon by a spec annotation alone: the unit reading a Python file's comments and
docstrings, given the canon's files as a list, and the checks of the tests' folder carrying it over the kept tests'
code. The canon is the tide tables' two files the fixtures give, so no test reads the project's own.
"""
import pytest

from design_script_set import design_documents

import code_checks

pytestmark = [pytest.mark.reads("design-script-kept-sets.md", "canon-of-the-tide-tables", "code-naming-the-canon-in-annotations-alone",
                                "code-naming-a-section-after-code", "code-naming-a-canon-file-by-its-name",
                                "code-naming-a-canon-path-on-a-line-of-its-own")]
RULE = ("specs/methodology/sourcing-and-citation/writing-a-citation.md § Writing a Citation § Citing From Code"
        " § Script Checks [Name: canon-named-only-in-an-annotation]")


def named(fixtures, key):
    return code_checks.canon_named_outside_an_annotation("tides.py", fixtures[key], fixtures["canon-of-the-tide-tables"].split())


# @canon-spec specs/methodology/sourcing-and-citation/writing-a-citation.md § Writing a Citation § Citing From Code § Script Checks [Name: canon-named-only-in-an-annotation]
@pytest.mark.action("--check-kept-tests")
@pytest.mark.passes
def test_code_naming_the_canon_in_annotations_alone_passes(fixtures):
    assert named(fixtures, "code-naming-the-canon-in-annotations-alone") == []


# @canon-spec specs/methodology/sourcing-and-citation/writing-a-citation.md § Writing a Citation § Citing From Code § Script Checks [Name: canon-named-only-in-an-annotation]
@pytest.mark.action("--check-kept-tests")
@pytest.mark.reports
@pytest.mark.parametrize("key, line", [
    ("code-naming-a-section-after-code", 1),
    ("code-naming-a-canon-file-by-its-name", 2),
    ("code-naming-a-canon-path-on-a-line-of-its-own", 1),
])
def test_canon_named_outside_an_annotation_is_reported_on_its_line(fixtures, key, line):
    assert [n for n, _ in named(fixtures, key)] == [line]


# @canon-spec specs/methodology/sourcing-and-citation/writing-a-citation.md § Writing a Citation § Citing From Code § Script Checks [Name: canon-named-only-in-an-annotation]
@pytest.mark.action("--check-kept-tests")
@pytest.mark.reports
def test_checks_of_the_tests_folder_report_a_test_naming_the_canon(fixtures, work):
    place = work / "tests/spec-of-record/scripts/tides/test_tides.py"
    place.parent.mkdir(parents=True)
    place.write_text(fixtures["code-naming-a-section-after-code"], encoding="utf-8")
    found = design_documents.tests_folder_problems(work, None)
    assert [rule for rule, msg in found if "test_tides.py line 1 names the canon outside a spec annotation" in msg] == [RULE]
