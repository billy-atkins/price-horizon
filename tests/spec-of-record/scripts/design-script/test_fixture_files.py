"""A fixture file as the design script reads one: no file of the listing of the operative files, so no spec a design
names in shorthand; canon to change; and of its own kind where a file is read by its kind. A project here holds a
fixtures' folder of its own, with a fixture file named as the project's guide is, guide.md."""
import pytest

from design_script_set import DESIGN, NAME, REPORTS, acted, design_documents as dd, held, project, spec_text

pytestmark = [pytest.mark.reads("design-script-ferry.md", "island-guide"),
              pytest.mark.reads("design-script-kept-sets.md", "fixture-file-of-one-line", "index-listing-one-file"),
              pytest.mark.reads("audit-whole-project.md", "project-registry-of-one-skill")]
FIXTURE_FILE, INDEX = "tests/spec-of-record/fixtures/guide.md", "tests/spec-of-record/fixtures/index.md"
AUDIT = REPORTS + "/audit-specs/1.md"
AUDITED = [DESIGN, "audit-specs", "Model=a model", "Effort=medium", "Led To=validating"]


def holding_a_fixture_file(work, fixtures, **placed):
    """-> the root of a project holding the guide, its registry of skills, a fixture file and the fixtures' index, with
    the further fixtures given at their paths."""
    return project(work, fixtures, {"island-guide": "docs/guide.md", "fixture-file-of-one-line": FIXTURE_FILE, "index-listing-one-file": INDEX,
                                    "project-registry-of-one-skill": "specs/methodology/skills/registered-skills.md", **placed})


@pytest.mark.parametrize("kind, listed", [
    (spec_text.OPERATIVE, ["docs/guide.md"]),
    (spec_text.FIXTURE, [FIXTURE_FILE, INDEX]),
    # a listing asked for no kind gives the operative files
    (None, ["docs/guide.md"]),
])
def test_listing_of_a_kind_gives_its_files_alone(fixtures, work, kind, listed):
    root = holding_a_fixture_file(work, fixtures)
    found = spec_text.md_files(root, kind) if kind else spec_text.md_files(root)
    assert [f.relative_to(root).as_posix() for f in found] == listed


@pytest.mark.action("--check-cited-headings")
@pytest.mark.passes
@pytest.mark.reads("design-script-designs.md", "ferry-design-citing-the-guide-in-shorthand")
def test_shorthand_names_the_one_operative_file_of_its_name(fixtures, work, monkeypatch, capsys):
    root = holding_a_fixture_file(work, fixtures, **{"ferry-design-citing-the-guide-in-shorthand": DESIGN})
    assert acted(monkeypatch, root, dd.check_cited_headings, DESIGN) == 0
    out = capsys.readouterr().out
    assert "2 citations, 0 broken" in out and "ok        guide.md" in out and "ambiguous" not in out


@pytest.mark.action("--check-target-kind")
@pytest.mark.passes
@pytest.mark.reads("design-script-fixture-files.md", "canon-design-targeting-a-fixture-file")
def test_fixture_file_in_a_canon_designs_target_passes(fixtures, work, monkeypatch, capsys):
    root = holding_a_fixture_file(work, fixtures, **{"canon-design-targeting-a-fixture-file": DESIGN})
    assert acted(monkeypatch, root, dd.check_target_kind, DESIGN) == 0
    assert "== check-target-kind %s\n0 problems" % NAME in capsys.readouterr().out


@pytest.mark.action("--check-target-kind")
@pytest.mark.reports
@pytest.mark.reads("design-script-fixture-files.md", "ferry-design-targeting-the-guide-and-a-fixture-file")
def test_fixture_file_in_a_documentation_designs_target_is_reported(fixtures, work, monkeypatch, capsys):
    root = holding_a_fixture_file(work, fixtures, **{"ferry-design-targeting-the-guide-and-a-fixture-file": DESIGN})
    before = held(root)
    assert acted(monkeypatch, root, dd.check_target_kind, DESIGN) == 1
    assert "Target names a canon-specs file in a documentation design: " + FIXTURE_FILE in capsys.readouterr().out and held(root) == before


@pytest.mark.parametrize("path, kind, sub_scope", [(FIXTURE_FILE, "fixture-files", "skills"), ("docs/guide.md", "documentation", "documentation")])
def test_file_read_by_its_kind_is_of_the_fixture_files_where_it_stands_among_them(fixtures, work, path, kind, sub_scope):
    skills = spec_text.skill_dirs(holding_a_fixture_file(work, fixtures))
    assert dd.file_kind(path, skills, ([], [])) == kind and dd.sub_scope_of(path, kind) == sub_scope


def test_fixture_file_is_canon_to_change(fixtures, work):
    assert dd.kind_of(FIXTURE_FILE, spec_text.skill_dirs(holding_a_fixture_file(work, fixtures))) == "canon-specs"


def audited(work, fixtures, monkeypatch):
    """-> the root of a project holding a canon design applying to a fixture file alone and its audit's report, stamped."""
    root = holding_a_fixture_file(work, fixtures, **{"canon-design-applying-to-a-fixture-file": DESIGN, "audit-report-finding-nothing": AUDIT})
    assert acted(monkeypatch, root, dd.stamp_settled_report, AUDIT) == 0
    return root


# @canon-spec specs/methodology/working-files/main.md § Design Log Entry § Script Checks [Name: settled-sub-scopes-keep-what-changed]
@pytest.mark.action("--log-entry")
@pytest.mark.reports
@pytest.mark.reads("design-script-fixture-files.md", "canon-design-applying-to-a-fixture-file")
@pytest.mark.reads("design-script-reports.md", "audit-report-finding-nothing")
def test_audit_entry_dropping_the_sub_scope_a_changed_fixture_file_lies_in_is_refused(fixtures, work, monkeypatch, capsys):
    root = audited(work, fixtures, monkeypatch)
    before = held(root)
    assert acted(monkeypatch, root, dd.log_entry, AUDITED + ["Settled Sub-scopes=documentation"]) == 1
    out = capsys.readouterr().out
    assert "the audit-specs entry's Settled Sub-scopes drop skills, each holding a file the design changed" in out and held(root) == before


# @canon-spec specs/methodology/working-files/main.md § Design Log Entry § Script Checks [Name: settled-sub-scopes-keep-what-changed]
@pytest.mark.action("--log-entry")
@pytest.mark.passes
@pytest.mark.reads("design-script-fixture-files.md", "canon-design-applying-to-a-fixture-file")
@pytest.mark.reads("design-script-reports.md", "audit-report-finding-nothing")
def test_audit_entry_keeping_the_sub_scope_a_changed_fixture_file_lies_in_is_appended(fixtures, work, monkeypatch, capsys):
    root = audited(work, fixtures, monkeypatch)
    assert acted(monkeypatch, root, dd.log_entry, AUDITED + ["Settled Sub-scopes=skills"]) == 0
    assert "**Settled Sub-scopes:** skills" in capsys.readouterr().out
