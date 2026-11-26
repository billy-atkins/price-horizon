"""The checkout a design is worked in: its last commit, the files it holds changed, the audits its design owes, what
a Refactor and Refine cycle changed in it, its citations' links and its constructs, each action called in a project
of fixtures, under version control where the action reads its last commit."""
import pytest

from design_script_set import DESIGN, NAME, acted, committed, design_documents as dd, held, project

pytestmark = [pytest.mark.reads("design-script-ferry.md", "island-guide")]
GUIDE = {"island-guide": "docs/guide.md"}


@pytest.mark.action("--check-cited-headings")
@pytest.mark.passes
@pytest.mark.reads("design-script-designs.md", "ferry-design-applying")
@pytest.mark.reads("design-script-pages-changed.md", "guide-ferry-retitled-beside-a-harbor")
@pytest.mark.parametrize("now", ["guide-ferry-retitled-beside-a-harbor", None])
def test_applying_designs_citations_are_read_at_the_last_commit(fixtures, work, monkeypatch, capsys, now):
    root = committed(project(work, fixtures, {**GUIDE, "ferry-design-applying": DESIGN}))
    if now:
        project(work, fixtures, {now: "docs/guide.md"})
    else:
        (root / "docs/guide.md").unlink()
    assert acted(monkeypatch, root, dd.check_cited_headings, DESIGN) == 0
    assert "1 citation, 0 broken" in capsys.readouterr().out


@pytest.mark.action("--check-cited-headings")
@pytest.mark.reports
@pytest.mark.reads("design-script-designs.md", "harbor-cited-applying")
@pytest.mark.reads("design-script-pages-changed.md", "guide-ferry-retitled-beside-a-harbor")
def test_applying_design_citing_a_heading_its_apply_wrote_is_reported(fixtures, work, monkeypatch, capsys):
    at = ".ai/plans/design-specs/harbor-cited.md"
    root = committed(project(work, fixtures, {**GUIDE, "harbor-cited-applying": at}))
    project(work, fixtures, {"guide-ferry-retitled-beside-a-harbor": "docs/guide.md"})
    assert acted(monkeypatch, root, dd.check_cited_headings, at) == 1
    out = capsys.readouterr().out
    assert "BROKEN" in out and "§ The Harbor" in out and "1 broken" in out


@pytest.mark.action("--check-changed-files")
@pytest.mark.passes
@pytest.mark.reads("design-script-designs.md", "ferry-design-applying-to-the-guide-and-the-tides",
                   "ferry-design-applying-to-the-guide-and-the-tides-noting-a-user-edit")
@pytest.mark.reads("design-script-pages.md", "spring-tides-page", "notes-citing-nothing")
@pytest.mark.reads("design-script-pages-changed.md", "guide-giving-the-first-ferry")
@pytest.mark.parametrize("design, beside, marked", [
    ("ferry-design-applying-to-the-guide-and-the-tides", {}, None),
    ("ferry-design-applying-to-the-guide-and-the-tides-noting-a-user-edit", {"notes-citing-nothing": "docs/notes.md"},
     "docs/notes.md\n  changed outside the Target, the user's edit"),
])
def test_files_changed_within_the_target_or_named_by_the_log_pass(fixtures, work, monkeypatch, capsys, design, beside, marked):
    root = committed(project(work, fixtures, {**GUIDE, design: DESIGN}))
    project(work, fixtures, {"guide-giving-the-first-ferry": "docs/guide.md", "spring-tides-page": "docs/tides/spring.md", **beside})
    assert acted(monkeypatch, root, dd.check_changed_files, DESIGN) == 0
    out = capsys.readouterr().out
    assert "== check-changed-files %s\n0 problems" % NAME in out and (marked is None or marked in out)


@pytest.mark.action("--check-changed-files")
@pytest.mark.reports
@pytest.mark.reads("design-script-designs.md", "ferry-design-applying-to-the-guide-and-the-tides")
@pytest.mark.reads("design-script-pages.md", "notes-citing-nothing")
def test_file_changed_outside_the_target_that_no_entry_names_is_reported(fixtures, work, monkeypatch, capsys):
    root = committed(project(work, fixtures, {**GUIDE, "ferry-design-applying-to-the-guide-and-the-tides": DESIGN}))
    project(work, fixtures, {"notes-citing-nothing": "docs/notes.md"})
    assert acted(monkeypatch, root, dd.check_changed_files, DESIGN) == 1
    assert "docs/notes.md\n  changed outside the Target, and no entry of the log names it" in capsys.readouterr().out


# @canon-spec specs/methodology/working-files/main.md § Design Log Entry § Script Checks [Name: audits-run-or-bypassed]
@pytest.mark.action("--check-audits")
@pytest.mark.passes
@pytest.mark.reads("design-script-designs.md", "ferry-design-applying-its-audit-bypassed", "ferry-design-applying-its-audit-run")
@pytest.mark.parametrize("design", ["ferry-design-applying-its-audit-bypassed", "ferry-design-applying-its-audit-run"])
def test_audit_run_or_bypassed_since_the_apply_passes(fixtures, work, monkeypatch, capsys, design):
    assert acted(monkeypatch, project(work, fixtures, {**GUIDE, design: DESIGN}), dd.check_audits, DESIGN) == 0
    assert "== check-audits %s\n0 problems" % NAME in capsys.readouterr().out


# @canon-spec specs/methodology/working-files/main.md § Design Log Entry § Script Checks [Name: audits-run-or-bypassed]
@pytest.mark.action("--check-audits")
@pytest.mark.reports
@pytest.mark.reads("design-script-designs.md", "ferry-design-applying", "ferry-design-applying-again-after-its-audit-bypassed")
@pytest.mark.parametrize("design", ["ferry-design-applying", "ferry-design-applying-again-after-its-audit-bypassed"])
def test_audit_owed_since_the_last_apply_is_reported(fixtures, work, monkeypatch, capsys, design):
    assert acted(monkeypatch, project(work, fixtures, {**GUIDE, design: DESIGN}), dd.check_audits, DESIGN) == 1
    assert "neither run nor bypassed since the last apply entry: the specs audit" in capsys.readouterr().out


@pytest.mark.action("--show-refactor-and-refine-of-existing-specs")
@pytest.mark.passes
@pytest.mark.reads("design-script-pages.md", "birds-spec", "birds-spec-carrying-links")
@pytest.mark.reads("design-script-pages-changed.md", "birds-spec-repeating-the-heron", "birds-spec-carrying-links-and-a-crane",
                   "birds-spec-carrying-links-its-egret-at-dusk")
@pytest.mark.parametrize("then, now, counted, lines", [
    ("birds-spec", "birds-spec-repeating-the-heron", "1 repeated, 1 lost, 1 new",
     ["repeated   The heron stands in the reeds at dusk and waits.\n           in specs/birds.md",
      "lost       The egret wades the shallows at first light alone.\n", "new        A crane flies over.\n"]),
    ("birds-spec-carrying-links", None, "0 repeated, 0 lost, 0 new", []),
    ("birds-spec-carrying-links", "birds-spec-carrying-links-and-a-crane", "0 repeated, 0 lost, 1 new",
     ["new        A crane flies over.\n           in specs/birds.md"]),
    ("birds-spec-carrying-links", "birds-spec-carrying-links-its-egret-at-dusk", "0 repeated, 1 lost, 2 new",
     ["lost       The egret wades the shallows at first light, far from the reeds of `specs/birds.md § The Heron`."]),
])
def test_refactor_and_refine_shows_each_line_repeated_lost_and_new(fixtures, work, monkeypatch, capsys, then, now, counted, lines):
    root = committed(project(work, fixtures, {then: "specs/birds.md"}))
    if now:
        project(work, fixtures, {now: "specs/birds.md"})
    assert acted(monkeypatch, root, dd.show_refactor_and_refine_of_existing_specs, "HEAD") == 0
    out = capsys.readouterr().out
    assert "== show-refactor-and-refine-of-existing-specs since HEAD" in out and counted in out
    assert all(line in out for line in lines) and "](/specs/birds.md" not in out


@pytest.mark.action("--show-refactor-and-refine-of-existing-specs")
@pytest.mark.reports
@pytest.mark.parametrize("versioned, baseline, said", [
    (True, "no-such-commit", "no such commit: no-such-commit"),
    (False, "HEAD", "run it from the repository's root"),
])
def test_refactor_and_refine_refuses_what_it_cannot_read(fixtures, work, monkeypatch, capsys, versioned, baseline, said):
    root = project(work, fixtures, GUIDE)
    if versioned:
        committed(root)
    assert acted(monkeypatch, root, dd.show_refactor_and_refine_of_existing_specs, baseline) == 2
    assert said in capsys.readouterr().err


@pytest.mark.action("--refresh-links")
@pytest.mark.reports
@pytest.mark.reads("design-script-pages.md", "notes-citing-the-ferry")
def test_link_a_citation_lacks_is_written(fixtures, work, monkeypatch, capsys):
    root = project(work, fixtures, {**GUIDE, "notes-citing-the-ferry": "docs/notes.md"})
    assert acted(monkeypatch, root, dd.refresh_links, str(root)) == 0
    assert "1 files changed" in capsys.readouterr().out
    assert "[`docs/guide.md § The Ferry`](/docs/guide.md#the-ferry)" in (root / "docs/notes.md").read_text(encoding="utf-8")


@pytest.mark.action("--refresh-links")
@pytest.mark.passes
@pytest.mark.reads("design-script-pages-changed.md", "notes-citing-the-ferry-by-its-link")
def test_current_links_are_left(fixtures, work, monkeypatch, capsys):
    root = project(work, fixtures, {**GUIDE, "notes-citing-the-ferry-by-its-link": "docs/notes.md"})
    before = held(root)
    assert acted(monkeypatch, root, dd.refresh_links, str(root)) == 0
    assert "0 files changed" in capsys.readouterr().out and held(root) == before


@pytest.mark.action("--check-constructs")
@pytest.mark.passes
@pytest.mark.reads("design-script-pages-changed.md", "guide-holding-the-hours-table")
def test_construct_in_its_form_passes(fixtures, work, monkeypatch, capsys):
    root = project(work, fixtures, {"guide-holding-the-hours-table": "docs/guide.md"})
    assert acted(monkeypatch, root, dd.check_constructs, "docs/guide.md") == 0
    assert "== check-constructs docs/guide.md" in capsys.readouterr().out


@pytest.mark.action("--check-constructs")
@pytest.mark.reports
@pytest.mark.reads("design-script-pages-changed.md", "guide-holding-a-table-of-no-hit-policy-given")
def test_construct_out_of_its_form_is_reported(fixtures, work, monkeypatch, capsys):
    root = project(work, fixtures, {"guide-holding-a-table-of-no-hit-policy-given": "docs/guide.md"})
    assert acted(monkeypatch, root, dd.check_constructs, "docs/guide.md") == 1
    out = capsys.readouterr().out
    assert "a Hit Policy that is none of DMN's: Whenever" in out and "1 finding" in out


@pytest.mark.action("--check-constructs")
@pytest.mark.reports
@pytest.mark.reads("design-script-designs.md", "ferry-design-drafted")
def test_design_document_is_refused_by_the_construct_checks(fixtures, work, monkeypatch, capsys):
    root = project(work, fixtures, {**GUIDE, "ferry-design-drafted": DESIGN})
    assert acted(monkeypatch, root, dd.check_constructs, DESIGN) == 2
    assert "no file in scope; a design's Drafts are checked by --check-design" in capsys.readouterr().err
