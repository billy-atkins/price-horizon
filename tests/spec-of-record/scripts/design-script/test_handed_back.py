"""A cold agent's report as it is handed back and taken up: --check-handed-back, which holds its part to its form,
and --take-up-report, which writes a fingerprint of each part it wrote."""
import re

import pytest

from design_script_set import (DRAFTED, FINDING, GOAL, JUDGMENT, NAME, Project, REVIEW, RULE, SKILLS, a_report, builder_part, cold_part, passes,
    report_at, reports, shown, swap)

pytestmark = [pytest.mark.reads("design-script-ferry.md", "island-guide", "ferry-design"),
              pytest.mark.reads("design-script-reports.md", "ferry-review-report")]


# @canon-spec specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: findings-anchored-in-the-design]
# @canon-spec specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: places-in-their-form]
# @canon-spec specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: report-in-its-form]
# @canon-spec specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: report-laid-out]
# @canon-spec specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: searches-cover-their-matches]
@pytest.mark.action("--check-handed-back")
@pytest.mark.passes
@pytest.mark.reads("design-script-reports.md", "ferry-research-report")
def test_cold_part_in_its_form_passes(check):
    for skill in SKILLS:
        p = Project("handed-back")
        p.design(skill=skill, log=DRAFTED)
        for kind, which in ((REVIEW, "review"), (JUDGMENT, "research")):
            path = p.put(report_at(kind, 1, skill=skill), cold_part(a_report(which, skill=skill)))
            before = p.held(".ai")
            got = p.run("--check-handed-back", path, skill=skill)
            check("--check-handed-back of %s passes the cold agent's part of %s report, and writes nothing" % (skill, "a review's" if kind == REVIEW else "a research"),
                  passes(got, "== check-handed-back " + path, "0 problems") and p.held(".ai") == before, shown(got))


# @canon-spec specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: cold-parts-kept]
# @canon-spec specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: findings-anchored-in-the-design]
# @canon-spec specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: places-in-their-form]
# @canon-spec specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: report-in-its-form]
# @canon-spec specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: report-keys-name-records]
# @canon-spec specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: searches-cover-their-matches]
@pytest.mark.action("--check-handed-back", "--take-up-report")
@pytest.mark.reports
@pytest.mark.reads("design-script-reports.md", "ferry-self-review-report")
def test_cold_part_out_of_its_form_is_reported(check):
    whole = cold_part(a_report("review"))
    for label, text, said, rule in (
            ("whose title names another entry", swap(whole, "**Entry:** adversarial-review-1", "**Entry:** adversarial-review-7"), "its title's Entry is adversarial-review-7, not adversarial-review-1", None),
            ("whose title names another design", swap(whole, "**Design:** " + NAME, "**Design:** another-design"), "its title's Design is another-design, not " + NAME, None),
            ("holding no Reading", whole.split("## Reading")[0] + "## Findings" + whole.split("## Findings")[1], "it holds no Reading part, which its form requires of it", None),
            ("whose parts stand out of their order", whole.split("## Findings")[0] + "## Searches" + whole.split("## Searches")[1].rstrip("\n") + "\n\n## Findings" + whole.split("## Findings")[1].split("## Searches")[0], "the report", None),
            ("holding a part the form does not give", whole + "\n## Afterthoughts\n\nNone.\n", "a part the form does not give: Afterthoughts", None),
            ("whose marked Finding holds no Decision", swap(whole, "    **Decision:** the times the section gives \\\n", ""), "Finding %s holds no Decision, which its form requires where its Verdict is a mark" % FINDING, None),
            ("whose Finding holds a Verdict out of its values", swap(whole, "**Verdict:** implementation flaw", "**Verdict:** a worry"), "a worry", None),
            ("holding a part the builder writes", whole + "\n" + builder_part(a_report("review")), "a part its cold agent does not write, the builder's or the design script's: Settlement", RULE % "cold-parts-kept"),
            ("whose Finding names a goal the design does not hold", swap(whole, "    **Affected Goals:**\n      - " + GOAL, "    **Affected Goals:**\n      - guide-says-what-the-ferry-costs"),
             "Finding %s's Affected Goals names guide-says-what-the-ferry-costs, which the design %s does not hold" % (FINDING, NAME), "§ A Check's Report § Finding"),
            ("whose marked Finding names no part of the design and cites no rule", swap(whole, "    **Affected Goals:**\n      - " + GOAL + "\n\n", ""),
             "Finding %s, marked a implementation flaw, names no goal, Frame Outcome or step Objective it bears on and cites no rule it breaks" % FINDING, "§ A Check's Report § Finding"),
            ("whose Reads hold what is no citation of a place", swap(whole, "      - `docs/guide.md`\n", "      - the guide\n"), "Collecting Reads holds an item that is no citation of a place with its path: the guide", None),
            ("whose Finding lands on a change not cited with its report", swap(whole, "        **Delivers:** An Objective giving the first and the last crossing of each season.\n",
                                                                           "        **Delivers:** An Objective giving the first and the last crossing of each season.\n\n    **Lands On:** times-by-season\n"),
             "Finding %s lands on an earlier change not cited with its report: times-by-season" % FINDING, None),
            ("citing a record of a report no entry names", swap(whole, "The section names one quay and no season.", "The section names one quay and no season, as `.ai/tmp/design-specs/%s/reports/adversarial-review/9.md § Findings [Finding: reviewer-1-another]` found." % NAME),
             "in a report no entry of the design's current major version names", None),
            ("whose reviewer's Search by meaning holds more Places than its Ranking Part spans", swap(whole, "**Ranking Part:** 1 to 20", "**Ranking Part:** none"),
             "Search reviewer-1-winter-hours's Ranking Part is none, and its Places hold 1", None),
            ("whose Search holds a Snapshot that is no snapshot code", swap(whole, "**Snapshot:** 0123456789abcdef", "**Snapshot:** yesterday"), "Search reviewer-1-winter-hours's Snapshot is yesterday, not a snapshot code", None)):
        p = Project("handed-back-reports")
        p.design(log=DRAFTED)
        path = p.put(report_at(REVIEW), text)
        got = p.run("--check-handed-back", path)
        check("--check-handed-back reports a review's report " + label, reports(got, "== check-handed-back " + path, said) and (rule is None or rule in got[1]), shown(got))
        before = p.read(path)
        got = p.run("--take-up-report", path)
        check("--take-up-report does not take up a review's report %s, and writes nothing" % label,
              reports(got, "== take-up-report, not taken up " + path, said) and p.read(path) == before, shown(got))
    p = Project("handed-back-usage")
    for flag in ("--check-handed-back", "--take-up-report"):
        got = p.run(flag, p.put(report_at("self-review"), a_report("self-review")))
        check("%s takes a review's or a handed-off judgment's report alone, exit 2" % flag, got[0] == 2 and "takes a review's or a handed-off judgment's report at its path" in got[1], shown(got))


# @canon-spec specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: report-laid-out]
@pytest.mark.reports
def test_report_laid_out_otherwise_is_reported(check):
    whole = cold_part(a_report("review"))
    p = Project("laid-out")
    p.design(log=DRAFTED)
    for label, text in (("a field's line ending with no backslash before the field after it", swap(whole, "**Verdict:** implementation flaw \\\n", "**Verdict:** implementation flaw\n")),
                        ("no blank line after a list a field holds", swap(whole, "      - " + GOAL + "\n\n    **Description:**", "      - " + GOAL + "\n    **Description:**"))):
        path = p.put(report_at(REVIEW), text)
        got = p.run("--check-handed-back", path)
        check("--check-handed-back reports a report holding " + label, reports(got, "== check-handed-back", "specs/methodology/modeling-constructs.md § Fields\n") or
              reports(got, "== check-handed-back", "specs/methodology/spec-style/markdown.md § Blank Lines\n"), shown(got))


# @canon-spec specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: cold-parts-kept]
@pytest.mark.action("--take-up-report")
@pytest.mark.passes
@pytest.mark.reads("design-script-reports.md", "ferry-research-report")
def test_take_up_writes_each_cold_parts_fingerprint(check):
    for skill in SKILLS:
        p = Project("taken-up")
        p.design(skill=skill, log=DRAFTED)
        for kind, which, parts in ((REVIEW, "review", ("Title", "Reading", "Findings", "Searches")), (JUDGMENT, "research", ("Title", "Reading", "Searches", "Read Assessments"))):
            cold = cold_part(a_report(which, skill=skill))
            path = p.put(report_at(kind, skill=skill), cold)
            got = p.run("--take-up-report", path, skill=skill)
            now = p.read(path)
            marks = re.findall(r"^- ([A-Za-z -]+): [0-9a-f]{64}(, \d+ lines)?$", now.split("## Hand-back")[-1], re.M)
            check("--take-up-report of %s takes up %s report: it leaves each part the cold agent wrote as it was and writes a fingerprint of each" % (skill, "a review's" if kind == REVIEW else "a research"),
                  passes(got, "== take-up-report " + path, "0 problems") and now.startswith(cold.rstrip("\n") + "\n\n## Hand-back\n\n") and tuple(m[0] for m in marks) == parts
                  and [bool(m[1]) for m in marks] == [kind == REVIEW and m[0] == "Searches" for m in marks], shown(got) + now[-600:])
