"""A fixture file as the design script reads one: no file of the listing of the operative files, so no spec a design
names in shorthand; canon to change; and of its own kind where a file is read by its kind.

A project here holds a fixtures' folder of its own, with a fixture file named as the project's guide is: guide.md.
"""
import pytest

from design_script_set import (APPLYING, DRAFTED, KEPT, NAME, Project, ROUND_FIELDS, a_clean_report, a_design, design_documents, passes, report_at,
    reports, shown, spec_text, swap)

pytestmark = [pytest.mark.reads("design-script-ferry.md", "island-guide", "ferry-design"),
              pytest.mark.reads("design-script-kept-sets.md", "fixture-file-of-one-line", "index-listing-one-file")]
FIXTURE_FILE, INDEX = KEPT + "/fixtures/guide.md", KEPT + "/fixtures/index.md"


def a_project_holding_a_fixture_file(fixtures):
    p = Project("fixture-files")
    p.put(FIXTURE_FILE, fixtures["fixture-file-of-one-line"])
    p.put(INDEX, fixtures["index-listing-one-file"])
    return p


@pytest.mark.action("--check-cited-headings")
@pytest.mark.passes
def test_listing_gives_no_fixture_file_and_shorthand_names_the_spec(check, fixtures):
    p = a_project_holding_a_fixture_file(fixtures)
    listed = lambda kind: [f.relative_to(p.root).as_posix() for f in spec_text.md_files(p.root, kind)]
    operative, fixture = listed(spec_text.OPERATIVE), listed(spec_text.FIXTURE)
    check("the listing of the operative files gives the guide and each file a form is read from, and no fixture file",
          "docs/guide.md" in operative and "specs/methodology/working-files/main.md" in operative and not [f for f in operative if f.startswith(KEPT + "/")], operative)
    check("the listing asked for the fixture files gives the files of the fixtures' folder alone", fixture == [FIXTURE_FILE, INDEX], fixture)
    check("and a listing asked for no kind gives the operative files", [f.relative_to(p.root).as_posix() for f in spec_text.md_files(p.root)] == operative)
    # the design names the guide in shorthand, by the name the fixture file carries too
    design = p.design(text=swap(a_design(log=DRAFTED), "and `docs/guide.md § The Ferry` names", "and `guide.md § The Ferry` names"))
    got = p.run("--check-cited-headings", design)
    check("--check-cited-headings resolves a file named in shorthand to the one operative file of that name, a fixture file of the same name standing in the project",
          passes(got, "== check-cited-headings", "2 citations, 0 broken") and "ok        guide.md" in got[1] and "ambiguous" not in got[1], shown(got))


# @canon-spec specs/methodology/working-files/main.md § Design Log Entry § Script Checks [Name: settled-sub-scopes-keep-what-changed]
@pytest.mark.action("--check-target-kind")
@pytest.mark.passes
@pytest.mark.reports
@pytest.mark.reads("design-script-reports.md", "audit-report-finding-nothing")
def test_fixture_file_is_canon_to_change_and_of_its_own_kind_to_read(check, fixtures):
    p = a_project_holding_a_fixture_file(fixtures)
    got = p.run("--check-target-kind", p.design(log=DRAFTED, Kind="canon-specs", Target="`%s`" % FIXTURE_FILE))
    check("--check-target-kind passes a canon design whose Target names a fixture file", passes(got, "== check-target-kind " + NAME, "0 problems"), shown(got))
    got = p.run("--check-target-kind", p.design(log=DRAFTED, Target="`docs/guide.md`; `%s`" % FIXTURE_FILE))
    check("--check-target-kind reports a fixture file in a documentation design's Target, as a file a canon design changes",
          reports(got, "== check-target-kind " + NAME, "Target names a canon-specs file in a documentation design: " + FIXTURE_FILE), shown(got))
    skills = spec_text.skill_dirs(p.root)
    check("where a file is read by its kind a fixture file is of the fixture files, and it lies in the sub-scope of the skills",
          design_documents.kind_of(FIXTURE_FILE, skills) == "canon-specs" and design_documents.file_kind(FIXTURE_FILE, skills, ([], [])) == "fixture-files"
          and design_documents.sub_scope_of(FIXTURE_FILE, "fixture-files") == "skills" and design_documents.file_kind("docs/guide.md", skills, ([], [])) == "documentation",
          design_documents.file_kind(FIXTURE_FILE, skills, ([], [])))
    # an audit's entry of a design that changed a fixture file alone keeps the sub-scope the file lies in
    design = p.design(status="applying", log=APPLYING, Kind="canon-specs", Target="`%s`" % FIXTURE_FILE)
    p.put(report_at("audit-specs"), a_clean_report("audit-specs"))
    got = p.run("--log-entry", design, "audit-specs", *ROUND_FIELDS, "Settled Sub-scopes=documentation")
    check("--log-entry refuses an audit's entry whose Settled Sub-scopes drop the skills, where the design changed a fixture file",
          reports(got, "== log-entry, not logged", "the audit-specs entry's Settled Sub-scopes drop skills, each holding a file the design changed"), shown(got))
    got = p.run("--log-entry", design, "audit-specs", *ROUND_FIELDS, "Settled Sub-scopes=skills")
    check("and appends one keeping them", passes(got, "== log-entry", "**Settled Sub-scopes:** skills"), shown(got))
