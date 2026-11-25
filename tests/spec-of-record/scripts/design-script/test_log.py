"""--log-entry: an entry held to the type the canon declares, a design-reassessment entry to its Cause, and a
diagnosis to its form as its entry is appended."""
import pytest

from design_script_set import (AGREED, CHECK_FIELDS, DRAFTED, NAME, Project, ROUND_FIELDS, SKILLS, a_diagnosis, a_report, passes, report_at, reports,
    shown, swap, taken_up)

pytestmark = [pytest.mark.reads("design-script-ferry.md", "island-guide", "ferry-design")]


@pytest.mark.action("--log-entry")
@pytest.mark.passes
def test_entry_in_its_type_is_appended(check):
    p = Project("log-appended")
    design = p.design(log=AGREED)
    got = p.run("--log-entry", design, "plan-change")
    now = p.read(design)
    check("--log-entry appends an entry, its count among its kind, and writes the version the log then gives to the header",
          passes(got, "== log-entry", "- **Entry:** plan-change-1") and "**Design Version:** 1.0.1" in got[1] and "**Version:** 1.0.1 \\" in now and now.count("**Entry:**") == 3, shown(got))
    form = p.run("--check-design-form", design)
    check("and the design it wrote holds its form", passes(form, "== check-design-form", "0 problems"), shown(form))
    for skill in SKILLS:
        p = Project("log-first")
        design = p.design(skill=skill, status="not-started")
        got = p.run("--log-entry", design, "entered", "Reason=taken up", skill=skill)
        check("--log-entry of %s gives a design holding no log its log's section, where the form puts it" % skill,
              passes(got, "== log-entry", "- **Entry:** entered-1") and "## Design Log Entries\n\n**Records:**\n  - **Entry:** entered-1" in p.read(design)
              and p.read(design).index("## Design Log Entries") < p.read(design).index("## Out of Scope"), shown(got))


@pytest.mark.action("--log-entry")
@pytest.mark.reports
def test_entry_out_of_its_type_is_refused(check):
    p = Project("log-refused")
    design = p.design(log=AGREED)
    before = p.held()
    for label, args, said in (
            ("a kind its type does not give", ("no-such-kind",), "a log entry's kind is not one of"),
            ("a field its kind does not give", ("plan-change", "Reason=because"), "a plan-change entry"),
            ("a value outside its field's Values", ("plan-approval", "Approval=perhaps"), "a plan-approval entry's Approval is not one of approved, approved and apply: perhaps"),
            ("a Reason the entry reason does not take", ("entered", "Reason=sent back for a rest"), "an entered entry's Reason is not one of"),
            ("an old log's reassessment entry", ("reassessment", "Decision=go on"), "a `reassessment` entry, written in no entry now"),
            ("a Cuts Short", ("step-back", "Cuts Short=adversarial-review-1"), "a Cuts Short, written in no entry now"),
            ("a check's entry whose report does not stand", ("self-review",) + CHECK_FIELDS, "a check's entry whose report does not stand in the design's folder: " + report_at("self-review"))):
        got = p.run("--log-entry", design, *args)
        check("--log-entry refuses %s, and writes nothing" % label, reports(got, "== log-entry, not logged", said) and p.held() == before, shown(got))
    got = p.run("--log-entry", design)
    check("--log-entry given no kind says what it takes, exit 2", got[0] == 2 and "--log-entry takes a design document, a kind and the kind's fields as FIELD=VALUE" in got[1], shown(got))
    got = p.run("--log-entry", p.design(folder=".ai/plans/design-specs/archive", log=AGREED), "plan-change")
    check("--log-entry appends no entry to a design standing in no plans folder", reports(got, "== log-entry, not logged", "it stands in no plans folder"), shown(got))


# @canon-spec specs/methodology/working-files/main.md § A Diagnosis § Script Checks [Name: diagnosis-whole-and-in-form]
@pytest.mark.passes
@pytest.mark.reads("design-script-ferry.md", "ferry-diagnosis")
def test_reassessment_at_the_step_back_holds_its_fields(check):
    for skill in SKILLS:
        p = Project("reassessed")
        design = p.design(skill=skill, log=DRAFTED)
        p.put(".ai/tmp/%s/%s/diagnosis/1.md" % (skill, NAME), a_diagnosis())
        for cause in ("a run of flaws", "a run of send-backs", "passes that did not converge", "the user's word")[:4 if skill == "design-specs" else 1]:
            p.design(skill=skill, log=DRAFTED)
            got = p.run("--log-entry", design, "design-reassessment", "Cause=step back: " + cause, "Decision=rescope",
                        "Diagnosis=.ai/tmp/%s/%s/diagnosis/1.md" % (skill, NAME), skill=skill)
            now = p.read(design)
            check("--log-entry of %s appends a design-reassessment entry whose Cause is the step back %s brought the design to, with what the user decided and its diagnosis" % (skill, cause),
                  passes(got, "== log-entry", "- **Entry:** design-reassessment-1") and "**Cause:** step back: %s \\\n    **Decision:** rescope \\\n    **Diagnosis:** " % cause in now
                  and "**Version:** 2.0.0" in now, shown(got))
        form = p.run("--check-design-form", design, skill=skill)
        check("and the design of %s it wrote holds its form" % skill, passes(form, "== check-design-form", "0 problems"), shown(form))


@pytest.mark.reads("design-script-ferry.md", "ferry-diagnosis")
def test_reassessment_without_its_cause_is_refused(check):
    p = Project("reassessed-refused")
    design = p.design(log=DRAFTED)
    p.put(".ai/tmp/design-specs/%s/diagnosis/1.md" % NAME, a_diagnosis())
    diagnosis = "Diagnosis=.ai/tmp/design-specs/%s/diagnosis/1.md" % NAME
    before = p.held()
    for label, args, said in (
            ("holding no Cause", ("Decision=rescope", diagnosis), "a design-reassessment entry holding no Cause: it states what caused the design reassessment"),
            ("holding no field at all", (), "a design-reassessment entry holding no Cause"),
            ("whose Cause is in neither form", ("Cause=the plan went stale", "Decision=rescope", diagnosis), "a design-reassessment entry's Cause is neither `changed foundation:`"),
            ("whose Cause is a step back naming nothing that brings a design to one", ("Cause=step back: a hunch", "Decision=rescope", diagnosis), "a design-reassessment entry's Cause is neither `changed foundation:`"),
            ("whose Cause is a step back and which holds no Decision", ("Cause=step back: the user's word", diagnosis), ["a design-reassessment entry", "Decision"]),
            ("whose Cause is a step back and which holds no Diagnosis", ("Cause=step back: the user's word", "Decision=rescope"), ["a design-reassessment entry", "Diagnosis"]),
            ("whose Cause is a step back and which holds neither", ("Cause=step back: the user's word",), ["a design-reassessment entry", "Decision", "Diagnosis"]),
            ("whose Decision is no design reassessment the user chooses", ("Cause=step back: the user's word", "Decision=carry on", diagnosis), "a design-reassessment entry's Decision is not one of rescope, split, a different approach: carry on"),
            ("whose Cause is a changed foundation, holding a Decision and a Diagnosis", ("Cause=changed foundation: quay-rebuilt finished", "Decision=rescope", diagnosis), "which --free-design alone appends")):
        got = p.run("--log-entry", design, "design-reassessment", *args)
        check("--log-entry refuses a design-reassessment entry %s, and writes nothing" % label, reports(got, "== log-entry, not logged", said) and p.held() == before, shown(got))


def test_form_reads_a_reassessment_by_its_cause(check):
    p = Project("reassessed-form")
    step_back = {"Cause": "step back: a run of flaws", "Decision": "split", "Diagnosis": "`.ai/tmp/design-specs/%s/diagnosis/1.md`" % NAME}
    foundation = {"Cause": "changed foundation: quay-rebuilt finished; pier-closed gone"}
    old = {"Decision": "rescope", "Diagnosis": "`.ai/tmp/design-specs/%s/diagnosis/1.md`" % NAME}
    for label, fields in (("chosen at the step back, holding its Decision and its Diagnosis", step_back), ("made for a changed foundation, holding neither", foundation),
                          ("appended before the entry held a Cause, read as one chosen at the step back", old)):
        got = p.run("--check-design-form", p.design(log=DRAFTED + (("design-reassessment", fields), ("goals-agreed", {}))))
        check("--check-design-form passes a log holding a design-reassessment entry " + label, passes(got, "== check-design-form", "0 problems"), shown(got))
    for label, fields, said in (
            ("made for a changed foundation and holding a Decision", dict(foundation, Decision="rescope"), ["log entry design-reassessment-1: a design-reassessment entry", "Decision"]),
            ("chosen at the step back and holding no Diagnosis", {"Cause": "step back: a run of flaws", "Decision": "split"}, ["log entry design-reassessment-1: a design-reassessment entry", "Diagnosis"]),
            ("whose Cause is in neither form", dict(step_back, Cause="it seemed time"), "log entry design-reassessment-1: a design-reassessment entry's Cause is neither `changed foundation:`")):
        got = p.run("--check-design-form", p.design(log=DRAFTED + (("design-reassessment", fields),)))
        check("--check-design-form reports a log holding a design-reassessment entry " + label, reports(got, "== check-design-form", said), shown(got))
    got = p.run("--check-design-form", p.design(log=DRAFTED + (("reassessment", {"Decision": "rescope", "Running Work": "none"}), ("goals-agreed", {}),
                                                         ("entered", {"Reason": "sent back for a dependency"}))))
    check("--check-design-form reads an old log's reassessment entry, and an entered entry holding a value of the earlier rules, as they were written, and reports neither",
          passes(got, "== check-design-form", "0 problems"), shown(got))


# @canon-spec specs/methodology/working-files/main.md § A Diagnosis § Script Checks [Name: diagnosis-whole-and-in-form]
@pytest.mark.reports
@pytest.mark.reads("design-script-ferry.md", "ferry-diagnosis")
def test_diagnosis_is_held_to_its_form(check):
    path = ".ai/tmp/design-specs/%s/diagnosis/1.md" % NAME
    args = ("design-reassessment", "Cause=step back: a run of flaws", "Decision=a different approach", "Diagnosis=" + path)
    whole = a_diagnosis()
    for label, text, said in (
            ("that does not stand in the design's folder", None, "the design-reassessment entry's Diagnosis names no diagnosis standing in the design's folder"),
            ("holding no Scope", whole.split("## Scope")[0], "the diagnosis"),
            ("whose Scope holds no Answer", whole.split("**Answer:**")[0].rstrip(" \\\n") + "\n", "its Scope holds Question, not its Question and its Answer"),
            ("naming an entry other than the one naming it", swap(whole, "design-reassessment-1", "design-reassessment-4"), "its Design Reassessment is design-reassessment-4, not design-reassessment-1, the entry naming it"),
            ("whose Flaw names a Root Cause it does not hold", swap(whole, "**Root Cause:** one-season-assumed\n\n## Root", "**Root Cause:** another-cause\n\n## Root"), "names the Root Cause another-cause, which the diagnosis does not hold"),
            ("whose Flaw says neither that it still applies nor that it does not", swap(whole, "**Still Applies:** yes", "**Still Applies:** perhaps"), "Still Applies is neither yes nor no: perhaps"),
            ("whose Flaw no longer applies and says not why", swap(whole, "**Still Applies:** yes", "**Still Applies:** no"), "no longer applies, and holds no Why Not"),
            ("whose Root Cause holds no Account", swap(whole, " \\\n    **Account:** The rebuilt goals name each season.", ""), "Root Cause one-season-assumed holds no Account")):
        p = Project("diagnosis")
        design = p.design(log=DRAFTED)
        if text is not None:
            p.put(path, text)
        before = p.held()
        got = p.run("--log-entry", design, *args)
        check("--log-entry refuses the design-reassessment entry of a diagnosis " + label,
              reports(got, "== log-entry, not logged", [said, "[Name: diagnosis-whole-and-in-form]"]) and p.held() == before, shown(got))
    p = Project("diagnosis-second")
    design = p.design(log=DRAFTED)
    p.put(".ai/tmp/design-specs/%s/diagnosis/2.md" % NAME, whole)
    got = p.run("--log-entry", design, *args[:3], "Diagnosis=.ai/tmp/design-specs/%s/diagnosis/2.md" % NAME)
    check("--log-entry refuses a diagnosis numbered other than its count among the diagnoses the design's entries name",
          reports(got, "== log-entry, not logged", "not .ai/tmp/design-specs/%s/diagnosis/1.md, diagnosis 1 of the diagnoses" % NAME), shown(got))
    p = Project("diagnosis-after-a-freeing")
    design = p.design(log=DRAFTED + (("design-reassessment", {"Cause": "changed foundation: quay-rebuilt finished"}), ("goals-agreed", {}), ("plan-change", {})))
    p.put(path, swap(whole, "design-reassessment-1", "design-reassessment-2"))
    got = p.run("--log-entry", design, *args)
    check("--log-entry numbers a diagnosis among the diagnoses, so the first diagnosis of a design freed once before is diagnosis 1 of entry design-reassessment-2",
          passes(got, "== log-entry", "- **Entry:** design-reassessment-2") and "**Version:** 3.0.0" in p.read(design), shown(got))


# @canon-spec specs/methodology/working-files/main.md § A Diagnosis § Script Checks [Name: diagnosis-whole-and-in-form]
@pytest.mark.passes
@pytest.mark.reports
@pytest.mark.reads("design-script-ferry.md", "ferry-diagnosis")
@pytest.mark.reads("design-script-reports.md", "ferry-review-report")
def test_diagnosis_leaving_out_a_flaw_is_refused(check):
    p = Project("diagnosis-flaws")
    design = p.design(log=DRAFTED)
    taken_up(p, "adversarial-review", a_report("review"))
    got = p.run("--log-entry", design, "adversarial-review", *ROUND_FIELDS)
    path = ".ai/tmp/design-specs/%s/diagnosis/1.md" % NAME
    args = ("design-reassessment", "Cause=step back: a run of flaws", "Decision=rescope", "Diagnosis=" + path)
    p.put(path, swap(a_diagnosis(), "reviewer-1-last-crossing-in-winter", "reviewer-1-another-finding"))
    refused = p.run("--log-entry", design, *args)
    check("--log-entry refuses a diagnosis leaving out a finding a Settlement of the design's checks kept as a flaw",
          got[0] == 0 and reports(refused, "== log-entry, not logged", "it leaves out adversarial-review/1.md [Finding: reviewer-1-last-crossing-in-winter], a finding of its flaw set"), shown(got) + shown(refused))
    p.put(path, a_diagnosis())
    got = p.run("--log-entry", design, *args)
    check("--log-entry appends the entry of a diagnosis holding a Flaw for each finding of its flaw set", passes(got, "== log-entry", "- **Entry:** design-reassessment-1"), shown(got))
