"""--check-work, the specs' and the code's script checks run over a design's work, and a self-review over applied
work under version control, which runs it.

Those checks are the audit's, and read the canon whole, each file of it by its path. So the one project the tests of
this file share holds the whole of what FORM_FILES names, the methodology among it, taken as the tests run:
SHARED_PROJECT_TAKES says so. The search reads that project once, as test_searched.py's is read.
"""
import pytest

from design_script_set import (APPLYING, CHECK_FIELDS, FORM_FILES, GUIDE_TESTS, KEPT_RULE, NAME, SELF, SKILLS, applied, failing, kept_tests, passes,
    reports, shown, swap)

pytestmark = [pytest.mark.reads("design-script-ferry.md", "island-guide", "ferry-design"),
              pytest.mark.reads("design-script-pages.md", "walkers-notes")]

SHARED_PROJECT_TAKES = FORM_FILES


@pytest.mark.action("--check-work")
@pytest.mark.passes
def test_work_adding_no_finding_passes(check, fixtures, a_searched_project):
    for skill in SKILLS:
        p = a_searched_project("work-pass", versioned=True)
        design = p.design(skill=skill, status="applying", log=APPLYING)
        p.put("docs/guide.md", swap(fixtures["island-guide"], "north quay.", "north quay, at seven and at five."))
        got = p.run("--check-work", design, skill=skill)
        check("--check-work of %s passes work whose change adds no finding to those the scope held at the last commit" % skill,
              passes(got, "== check-work " + NAME, "0 findings new against the last commit, over 1 changed file"), shown(got))


@pytest.mark.action("--check-work")
@pytest.mark.reports
def test_finding_the_work_added_is_reported(check, fixtures, a_searched_project):
    for skill in SKILLS:
        p = a_searched_project("work-reports", versioned=True)
        design = p.design(skill=skill, status="applying", log=APPLYING)
        p.put("docs/guide.md", swap(fixtures["island-guide"], "north quay.", "north quay, as `docs/guide.md § The Harbour Master` has it."))
        got = p.run("--check-work", design, skill=skill)
        check("--check-work of %s reports a finding the scope holds now and did not hold at the last commit: a citation of a heading that does not stand" % skill,
              reports(got, "== check-work " + NAME, ["docs/guide.md:7", "The Harbour Master", "1 finding new against the last commit, over 1 changed file"]), shown(got))


# @canon-spec specs/methodology/skills/authoring-a-skill.md § Authoring a Skill § Script Checks [Name: kept-tests-pass-at-the-self-review]
@pytest.mark.action("--log-entry")
@pytest.mark.passes
@pytest.mark.reports
@pytest.mark.reads("design-script-kept-sets.md", "guide-script", "guide-set-conftest", "guide-set-tests", "fixture-file-of-one-line", "index-listing-one-file")
@pytest.mark.reads("design-script-reports.md", "ferry-self-review-report")
def test_self_review_under_version_control_runs_its_checks_and_the_kept_tests(check, fixtures, a_searched_project):
    for fails in (False, True):
        p = a_searched_project("applied-versioned", versioned=True)
        kept_tests(p, tests=failing(fixtures["guide-set-tests"]) if fails else None)
        p.commit()
        design, path = applied(p)
        p.put("docs/guide.md", swap(fixtures["island-guide"], "north quay.", "north quay, at seven and at five."))
        got = p.run("--log-entry", design, SELF, *CHECK_FIELDS)
        now = p.read(path)
        ran = "$ --check-work %s\n== check-work %s\n\n0 findings new against the last commit, over 1 changed file" % (design, NAME) in now \
            and "$ --check-kept-tests\nthe kept tests of guide, run for docs/guide.md\n$ python -B -m pytest %s\n  2 tests, %d failed\n" % (GUIDE_TESTS, fails) in now
        if fails:
            check("--log-entry refuses the entry of a self-review over an apply that changed a form alone, read from the checkout's changes, where a kept test of the script reading it fails",
                  reports(got, "== log-entry, not logged", ["%s holds a test that fails: " % GUIDE_TESTS, KEPT_RULE]) and ran, shown(got) + now[-900:])
        else:
            check("--log-entry appends it where they pass, the output of the checks over the work and of the kept tests in its report", passes(got, "== log-entry", "- **Entry:** self-review-1") and ran, shown(got) + now[-900:])
