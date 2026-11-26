"""--log-entry: an entry written into a design's log, held to the type the canon declares, a design-reassessment entry
to its Cause, and its diagnosis to its form as the entry is appended."""
import pytest

from design_script_set import DESIGN, NAME, REPORTS, acted, design_documents as dd, held, project

pytestmark = [pytest.mark.reads("design-script-ferry.md", "island-guide")]
DIAGNOSIS = ".ai/tmp/design-specs/%s/diagnosis/1.md" % NAME
STEP_BACK = [("Cause", "step back: a run of flaws"), ("Decision", "a different approach"), ("Diagnosis", DIAGNOSIS)]
NOT_LOGGED = "== log-entry, not logged"
RULE = "[Name: diagnosis-whole-and-in-form]"


def a_project(work, fixtures, design="ferry-design-drafted", **more):
    return project(work, fixtures, {"island-guide": "docs/guide.md", design: DESIGN, **more})


def log_type():
    values, counts, kinds, _ = dd.log_type()
    return values, counts, kinds


@pytest.mark.action("--log-entry")
@pytest.mark.passes
@pytest.mark.reads("design-script-designs.md", "ferry-design-agreed-undrafted")
def test_entry_takes_its_count_and_the_version_the_log_then_gives(fixtures):
    text, block = dd.with_entry(fixtures["ferry-design-agreed-undrafted"], "plan-change", [])
    assert block.startswith("  - **Entry:** plan-change-1 \\") and "**Design Version:** 1.0.1" in block
    assert "**Version:** 1.0.1 \\" in text and text.count("**Entry:**") == 3


@pytest.mark.action("--log-entry")
@pytest.mark.passes
@pytest.mark.reads("design-script-designs.md", "ferry-design-not-started")
def test_first_entry_gives_the_design_its_log_where_the_form_puts_it(fixtures):
    text, _ = dd.with_entry(fixtures["ferry-design-not-started"], "entered", [("Reason", "taken up")])
    assert "## Design Log Entries\n\n**Records:**\n  - **Entry:** entered-1" in text
    assert text.index("## Design Log Entries") < text.index("## Out of Scope")


@pytest.mark.action("--log-entry")
@pytest.mark.passes
@pytest.mark.reads("design-script-designs.md", "ferry-design-agreed-undrafted")
def test_design_an_entry_is_appended_to_holds_its_form(fixtures, work, monkeypatch, capsys):
    root = a_project(work, fixtures, "ferry-design-agreed-undrafted")
    assert acted(monkeypatch, root, dd.log_entry, [DESIGN, "plan-change"]) == 0
    assert acted(monkeypatch, root, dd.check_design_form, DESIGN) == 0
    assert "- **Entry:** plan-change-1" in capsys.readouterr().out


@pytest.mark.action("--log-entry")
@pytest.mark.passes
@pytest.mark.reads("design-script-designs.md", "ferry-design-applying-its-goals-frame-and-steps-out-of-their-form")
def test_entry_is_appended_to_a_design_whose_other_parts_do_not_parse(fixtures, work, monkeypatch, capsys):
    root = a_project(work, fixtures, "ferry-design-applying-its-goals-frame-and-steps-out-of-their-form")
    before = (root / DESIGN).read_bytes().decode("utf-8")
    assert acted(monkeypatch, root, dd.log_entry, [DESIGN, "user-edit", "Places=docs/guide.md"]) == 0
    block = capsys.readouterr().out.split("== log-entry\n", 1)[1].rstrip("\n")
    assert block.startswith("  - **Entry:** user-edit-1 \\") and block.endswith("**Places:** docs/guide.md")
    now = (root / DESIGN).read_bytes().decode("utf-8")
    assert "**Design Version:** 1.0.1\n\n%s\n\n## Out of Scope" % block in now and now.replace("\n\n" + block, "", 1) == before


@pytest.mark.action("--log-entry")
@pytest.mark.passes
@pytest.mark.parametrize("kind, fields", [
    ("plan-change", []), ("plan-approval", [("Approval", "approved and apply")]), ("design-reassessment", STEP_BACK),
    ("design-reassessment", [("Cause", "changed foundation: quay-rebuilt finished; pier-closed gone")]),
])
def test_entry_in_its_type_has_no_problem(kind, fields):
    assert dd.entry_problems(kind, fields, *log_type()) == []


@pytest.mark.action("--log-entry")
@pytest.mark.reports
@pytest.mark.parametrize("kind, fields, said", [
    ("no-such-kind", [], ["a log entry's kind is not one of"]),
    ("plan-change", [("Reason", "because")], ["a plan-change entry"]),
    ("plan-approval", [("Approval", "perhaps")], ["a plan-approval entry's Approval is not one of approved, approved and apply: perhaps"]),
    ("design-reassessment", [("Cause", "the plan went stale")] + STEP_BACK[1:], ["a design-reassessment entry's Cause is neither `changed foundation:`"]),
    ("design-reassessment", [("Cause", "step back: a hunch")] + STEP_BACK[1:], ["a design-reassessment entry's Cause is neither `changed foundation:`"]),
    ("design-reassessment", [STEP_BACK[0], STEP_BACK[2]], ["a design-reassessment entry", "Decision"]),
    ("design-reassessment", STEP_BACK[:2], ["a design-reassessment entry", "Diagnosis"]),
    ("design-reassessment", STEP_BACK[:1], ["a design-reassessment entry", "Decision", "Diagnosis"]),
])
def test_entry_out_of_its_type_is_reported(kind, fields, said):
    problems = dd.entry_problems(kind, fields, *log_type())
    assert len(problems) == 1 and all(s in problems[0] for s in said)


@pytest.mark.action("--log-entry")
@pytest.mark.reports
@pytest.mark.reads("design-script-designs.md", "ferry-design-drafted")
@pytest.mark.reads("design-script-ferry.md", "ferry-diagnosis")
@pytest.mark.parametrize("entry, said", [
    (["entered", "Reason=sent back for a rest"], "an entered entry's Reason is not one of"),
    (["reassessment", "Decision=go on"], "a `reassessment` entry, written in no entry now"),
    (["step-back", "Cuts Short=adversarial-review-1"], "a Cuts Short, written in no entry now"),
    (["self-review", "Model=a model", "Effort=medium"], "a check's entry whose report does not stand in the design's folder: " + REPORTS + "/self-review/1.md"),
    (["design-reassessment"], "a design-reassessment entry holding no Cause: it states what caused the design reassessment"),
    (["design-reassessment", "Decision=rescope", "Diagnosis=" + DIAGNOSIS], "a design-reassessment entry holding no Cause"),
    (["design-reassessment", "Cause=step back: the user's word", "Decision=carry on", "Diagnosis=" + DIAGNOSIS],
     "a design-reassessment entry's Decision is not one of rescope, split, a different approach: carry on"),
    (["design-reassessment", "Cause=changed foundation: quay-rebuilt finished", "Decision=rescope", "Diagnosis=" + DIAGNOSIS], "which --free-design alone appends"),
])
def test_entry_the_appending_refuses_writes_nothing(fixtures, work, monkeypatch, capsys, entry, said):
    root = a_project(work, fixtures, **{"ferry-diagnosis": DIAGNOSIS})
    before = held(root)
    assert acted(monkeypatch, root, dd.log_entry, [DESIGN] + entry) == 1
    out = capsys.readouterr().out
    assert NOT_LOGGED in out and said in out and held(root) == before


@pytest.mark.action("--log-entry")
@pytest.mark.reports
@pytest.mark.reads("design-script-designs.md", "ferry-design-drafted")
def test_entry_given_no_kind_is_refused(fixtures, work, monkeypatch, capsys):
    assert acted(monkeypatch, a_project(work, fixtures), dd.log_entry, [DESIGN]) == 2
    assert "--log-entry takes a design document, a kind and the kind's fields as FIELD=VALUE" in capsys.readouterr().err


@pytest.mark.action("--log-entry")
@pytest.mark.reports
@pytest.mark.reads("design-script-designs.md", "ferry-design-drafted")
def test_entry_to_a_design_in_no_plans_folder_is_refused(fixtures, work, monkeypatch, capsys):
    at = ".ai/plans/design-specs/archive/%s.md" % NAME
    root = project(work, fixtures, {"island-guide": "docs/guide.md", "ferry-design-drafted": at})
    assert acted(monkeypatch, root, dd.log_entry, [at, "plan-change"]) == 1
    out = capsys.readouterr().out
    assert NOT_LOGGED in out and "it stands in no plans folder" in out


# @canon-spec specs/methodology/working-files/main.md § A Diagnosis § Script Checks [Name: diagnosis-whole-and-in-form]
@pytest.mark.action("--log-entry")
@pytest.mark.passes
@pytest.mark.reads("design-script-designs.md", "ferry-design-drafted")
@pytest.mark.reads("design-script-ferry.md", "ferry-diagnosis")
@pytest.mark.parametrize("cause", ["a run of flaws", "a run of send-backs", "passes that did not converge", "the user's word"])
def test_reassessment_at_the_step_back_is_appended_with_its_decision_and_diagnosis(fixtures, work, monkeypatch, capsys, cause):
    root = a_project(work, fixtures, **{"ferry-diagnosis": DIAGNOSIS})
    entry = [DESIGN, "design-reassessment", "Cause=step back: " + cause, "Decision=rescope", "Diagnosis=" + DIAGNOSIS]
    assert acted(monkeypatch, root, dd.log_entry, entry) == 0
    now = (root / DESIGN).read_text(encoding="utf-8")
    assert "- **Entry:** design-reassessment-1" in capsys.readouterr().out and "**Version:** 2.0.0" in now
    assert "**Cause:** step back: %s \\\n    **Decision:** rescope \\\n    **Diagnosis:** %s" % (cause, DIAGNOSIS) in now
    assert acted(monkeypatch, root, dd.check_design_form, DESIGN) == 0


@pytest.mark.action("--check-design-form")
@pytest.mark.passes
@pytest.mark.reads("design-script-log.md", "log-of-a-reassessment-at-the-step-back", "log-of-a-reassessment-for-a-changed-foundation",
                   "log-of-a-reassessment-holding-no-cause", "log-of-a-reassessment-entry-of-an-old-log")
@pytest.mark.parametrize("key", ["log-of-a-reassessment-at-the-step-back", "log-of-a-reassessment-for-a-changed-foundation",
                                 "log-of-a-reassessment-holding-no-cause", "log-of-a-reassessment-entry-of-an-old-log"])
def test_log_holding_a_reassessment_in_the_form_its_cause_gives_has_no_problem(fixtures, key):
    assert dd.check_log(fixtures[key]) == []


@pytest.mark.action("--check-design-form")
@pytest.mark.reports
@pytest.mark.reads("design-script-log.md", "log-of-a-changed-foundation-holding-a-decision", "log-of-a-step-back-holding-no-diagnosis",
                   "log-of-a-reassessment-of-a-cause-in-neither-form")
@pytest.mark.parametrize("key, said", [
    ("log-of-a-changed-foundation-holding-a-decision", ["log entry design-reassessment-1: a design-reassessment entry", "Decision"]),
    ("log-of-a-step-back-holding-no-diagnosis", ["log entry design-reassessment-1: a design-reassessment entry", "Diagnosis"]),
    ("log-of-a-reassessment-of-a-cause-in-neither-form", ["log entry design-reassessment-1: a design-reassessment entry's Cause is neither `changed foundation:`"]),
])
def test_log_holding_a_reassessment_out_of_the_form_its_cause_gives_is_reported(fixtures, key, said):
    problems = dd.check_log(fixtures[key])
    assert len(problems) == 1 and all(s in problems[0] for s in said)


def diagnosed(work, fixtures, monkeypatch, design, placed, count=1, named=DIAGNOSIS):
    """-> the problems of the diagnosis a step back's design-reassessment entry names at the path given, appended to
    the design given as its count among its kind, in a project holding the design and each fixture placed."""
    root = project(work, fixtures, {"island-guide": "docs/guide.md", design: DESIGN, **placed})
    monkeypatch.chdir(root)
    return dd.diagnosis_problems(root, root / DESIGN, fixtures[design], count, dict(STEP_BACK, Diagnosis=named))


# @canon-spec specs/methodology/working-files/main.md § A Diagnosis § Script Checks [Name: diagnosis-whole-and-in-form]
@pytest.mark.action("--log-entry")
@pytest.mark.passes
@pytest.mark.reads("design-script-designs.md", "ferry-design-drafted")
@pytest.mark.reads("design-script-ferry.md", "ferry-diagnosis")
@pytest.mark.reads("design-script-taken-up.md", "ferry-design-freed-of-a-complete-design")
@pytest.mark.reads("design-script-log.md", "ferry-diagnosis-of-the-second-reassessment")
@pytest.mark.parametrize("design, diagnosis, count", [
    ("ferry-design-drafted", "ferry-diagnosis", 1),
    ("ferry-design-freed-of-a-complete-design", "ferry-diagnosis-of-the-second-reassessment", 2),
])
def test_diagnosis_whole_and_in_form_has_no_problem(fixtures, work, monkeypatch, design, diagnosis, count):
    assert diagnosed(work, fixtures, monkeypatch, design, {diagnosis: DIAGNOSIS}, count) == []


# @canon-spec specs/methodology/working-files/main.md § A Diagnosis § Script Checks [Name: diagnosis-whole-and-in-form]
@pytest.mark.action("--log-entry")
@pytest.mark.passes
@pytest.mark.reads("design-script-taken-up.md", "ferry-design-freed-of-a-complete-design")
@pytest.mark.reads("design-script-log.md", "ferry-diagnosis-of-the-second-reassessment")
def test_first_diagnosis_of_a_design_freed_before_is_appended_with_its_second_reassessment(fixtures, work, monkeypatch, capsys):
    root = a_project(work, fixtures, "ferry-design-freed-of-a-complete-design", **{"ferry-diagnosis-of-the-second-reassessment": DIAGNOSIS})
    entry = [DESIGN, "design-reassessment"] + ["%s=%s" % f for f in STEP_BACK]
    assert acted(monkeypatch, root, dd.log_entry, entry) == 0
    assert "- **Entry:** design-reassessment-2" in capsys.readouterr().out
    assert "**Version:** 3.0.0" in (root / DESIGN).read_text(encoding="utf-8")


# @canon-spec specs/methodology/working-files/main.md § A Diagnosis § Script Checks [Name: diagnosis-whole-and-in-form]
@pytest.mark.action("--log-entry")
@pytest.mark.reports
@pytest.mark.reads("design-script-designs.md", "ferry-design-drafted")
@pytest.mark.reads("design-script-ferry.md", "ferry-diagnosis")
@pytest.mark.reads("design-script-log.md", "ferry-diagnosis-holding-no-scope", "ferry-diagnosis-its-scope-holding-no-answer",
                   "ferry-diagnosis-naming-the-fourth-reassessment", "ferry-diagnosis-its-flaw-naming-another-root-cause",
                   "ferry-diagnosis-its-flaw-perhaps-still-applying", "ferry-diagnosis-its-flaw-no-longer-applying",
                   "ferry-diagnosis-its-root-cause-holding-no-account")
@pytest.mark.parametrize("placed, said", [
    ({}, "the design-reassessment entry's Diagnosis names no diagnosis standing in the design's folder"),
    ({"ferry-diagnosis-holding-no-scope": DIAGNOSIS}, "the diagnosis"),
    ({"ferry-diagnosis-its-scope-holding-no-answer": DIAGNOSIS}, "its Scope holds Question, not its Question and its Answer"),
    ({"ferry-diagnosis-naming-the-fourth-reassessment": DIAGNOSIS}, "its Design Reassessment is design-reassessment-4, not design-reassessment-1, the entry naming it"),
    ({"ferry-diagnosis-its-flaw-naming-another-root-cause": DIAGNOSIS}, "names the Root Cause another-cause, which the diagnosis does not hold"),
    ({"ferry-diagnosis-its-flaw-perhaps-still-applying": DIAGNOSIS}, "Still Applies is neither yes nor no: perhaps"),
    ({"ferry-diagnosis-its-flaw-no-longer-applying": DIAGNOSIS}, "no longer applies, and holds no Why Not"),
    ({"ferry-diagnosis-its-root-cause-holding-no-account": DIAGNOSIS}, "Root Cause one-season-assumed holds no Account"),
])
def test_diagnosis_missing_or_out_of_its_form_is_reported(fixtures, work, monkeypatch, placed, said):
    problems = diagnosed(work, fixtures, monkeypatch, "ferry-design-drafted", placed)
    assert any(said in p for p in problems) and all(RULE in p for p in problems)


# @canon-spec specs/methodology/working-files/main.md § A Diagnosis § Script Checks [Name: diagnosis-whole-and-in-form]
@pytest.mark.action("--log-entry")
@pytest.mark.reports
@pytest.mark.reads("design-script-designs.md", "ferry-design-drafted")
@pytest.mark.reads("design-script-ferry.md", "ferry-diagnosis")
def test_diagnosis_numbered_other_than_its_count_among_the_diagnoses_is_reported(fixtures, work, monkeypatch):
    second = DIAGNOSIS.replace("1.md", "2.md")
    problems = diagnosed(work, fixtures, monkeypatch, "ferry-design-drafted", {"ferry-diagnosis": second}, named=second)
    assert len(problems) == 1 and "is %s, not %s, diagnosis 1 of the diagnoses" % (second, DIAGNOSIS) in problems[0] and RULE in problems[0]


# @canon-spec specs/methodology/working-files/main.md § A Diagnosis § Script Checks [Name: diagnosis-whole-and-in-form]
@pytest.mark.action("--log-entry")
@pytest.mark.passes
@pytest.mark.reports
@pytest.mark.reads("design-script-log.md", "ferry-design-drafted-its-review-logged", "ferry-diagnosis-its-flaw-citing-another-finding")
@pytest.mark.reads("design-script-ferry.md", "ferry-diagnosis")
@pytest.mark.reads("design-script-reports.md", "ferry-review-report")
@pytest.mark.parametrize("diagnosis, problems", [
    ("ferry-diagnosis", []),
    ("ferry-diagnosis-its-flaw-citing-another-finding",
     ["%s: it leaves out adversarial-review/1.md [Finding: reviewer-1-last-crossing-in-winter], a finding of its flaw set (%s)" % (DIAGNOSIS, dd.DIAGNOSIS_RULE)]),
])
def test_diagnosis_holds_a_flaw_for_each_finding_its_designs_checks_kept_as_one(fixtures, work, monkeypatch, diagnosis, problems):
    placed = {diagnosis: DIAGNOSIS, "ferry-review-report": REPORTS + "/adversarial-review/1.md"}
    assert diagnosed(work, fixtures, monkeypatch, "ferry-design-drafted-its-review-logged", placed) == problems


# @canon-spec specs/methodology/working-files/main.md § A Diagnosis § Script Checks [Name: diagnosis-whole-and-in-form]
@pytest.mark.action("--log-entry")
@pytest.mark.reports
@pytest.mark.reads("design-script-designs.md", "ferry-design-drafted")
@pytest.mark.reads("design-script-log.md", "ferry-diagnosis-its-flaw-no-longer-applying")
def test_entry_of_a_diagnosis_out_of_its_form_is_refused_and_writes_nothing(fixtures, work, monkeypatch, capsys):
    root = a_project(work, fixtures, **{"ferry-diagnosis-its-flaw-no-longer-applying": DIAGNOSIS})
    before = held(root)
    assert acted(monkeypatch, root, dd.log_entry, [DESIGN, "design-reassessment"] + ["%s=%s" % f for f in STEP_BACK]) == 1
    out = capsys.readouterr().out
    assert NOT_LOGGED in out and "no longer applies, and holds no Why Not" in out and RULE in out and held(root) == before
