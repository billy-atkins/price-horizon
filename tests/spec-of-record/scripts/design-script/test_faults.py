"""The faults the design script was once found with, each put back, and the tests that then fail.

For each fault, the test copies the checkout's skills, with the files of the canon the design script reads a form
from, to a tree of its own in the file's folder within the run's folder, puts the fault back by a small edit at an
anchor, runs the fault's tests against that tree, by the runner, and requires each to fail in the check the fault
breaks. A fault whose anchor does not stand fails the test loudly. It puts back the faults of the search too,
.ai/skills/lib/search.py, into a tree holding the search's kept tests, and requires the test of them holding each to
fail in the check it breaks.

The test is slow: a run asks for it with --slow.
"""
import concurrent.futures
import shutil

import pytest

from design_script_set import (CHECKOUT, FORMS_ALONE, KEPT, LIB, SET, a_run, copy_files)

pytestmark = [pytest.mark.slow]
OWN = SET + "/"
SEARCHING = OWN + "test_searched.py::test_taken_up_report_stands_through_a_later_fix"
# Each fault: what it was; the edits putting it back into a copy of the script, each (the text standing at its anchor,
# the text put there); and the tests that then fail, each with words of the check of it the fault breaks, so a test
# failing in some other check, for some other reason, proves nothing of the fault.
FAULTS = (
    ("the old Depends On field read silently as a design's Depends On Designs",
     [('        fields = [(f["key"], " ".join(str(record_types.value_of(f)).split())) for f in block]\n    return f.stem, fields',
       '        fields = [(DEPENDS_ON if f["key"] == "Depends On" else f["key"], " ".join(str(record_types.value_of(f)).split())) for f in block]\n    return f.stem, fields')],
     [(OWN + "test_earlier.py::test_old_depends_on_field_is_reported_and_unread", "reports a design holding the old Depends On field, naming the field")]),
    ("a name of a design standing in no plans folder given a second meaning, a problem of the workstack",
     [('    problems = []\n    for n in designs:\n        problems += [(n, "its header " + fault) for fault in out_of_form[n]]\n',
       '    problems = []\n    for n in designs:\n        problems += [(n, "its header " + fault) for fault in out_of_form[n]]\n'
       '        problems += [(n, "its Depends On Designs names %s, which is no design" % d) for d, r in readings[n] if r == GONE_NAME]\n')],
     [(OWN + "test_names.py::test_workstack_checked_reads_each_name", "--check-workstack reports nothing of a design in progress after its goals naming a design standing in no plans folder")]),
    ("a freeing writing designs other than the one acted on, an archived one among them",
     [('    write_design(design, raw, text)\n    print("reassessed, its goals to agree again:\\n"',
       '    write_design(design, raw, text)\n    for other in design.parent.rglob("*.md"):\n        if other.resolve() != design.resolve():\n'
       '            other.write_bytes(other.read_bytes() + b"\\n")\n    print("reassessed, its goals to agree again:\\n"')],
     [(OWN + "test_freeing.py::test_design_is_freed_of_finished_and_gone_names", "--free-design frees a design in progress after its goals naming a design complete"),
      (OWN + "test_writes.py::test_writing_action_writes_its_own_design_alone", "--free-design of design-specs writes the design it is run on, and leaves every other design byte for byte as it was")]),
    ("a reviewer's Search, and each other check of a cold part, run again after the take-up",
     [('    taken_up = ctx["taken_up"] = cold_lines(rep, kind)\n', '    taken_up = ctx["taken_up"] = frozenset()\n')],
     [(OWN + "test_taken_up.py::test_finding_stands_though_its_goal_is_removed", "passes a taken-up report whose Finding names a goal the builder renamed while settling"),
      (SEARCHING, "runs no Search of the reviewer's again")]),
    ("a taken-up report returned to its cold agent for anything a check of the hand-back reports",
     [('    refused = unmatched_cold_parts(part_texts(text))\n    if not refused:\n        return []\n    path.write_text(cleared_report(text, kind), encoding="utf-8")',
       '    refused = unmatched_cold_parts(part_texts(text)) or handed_back_problems(root, design, kind, n, path)\n    if not refused:\n        return []\n'
       '    path.write_text(cleared_report(text, kind), encoding="utf-8")')],
     [(OWN + "test_taken_up.py::test_builders_fault_stays_with_the_builder", "refuses a taken-up report for a Finding the builder's Settlement leaves unsettled")]),
    ("an applying design's citations read against the files as its apply left them",
     [('        applying = is_applying(text)\n        kept = tuple(', '        applying = False\n        kept = tuple(')],
     [(OWN + "test_checkout.py::test_applying_designs_citations_read_at_the_last_commit", "reports nothing of an applying design citing a heading its own apply retitled")]),
    ("the research of a design approved or applying read against the files",
     [('    if not approved:\n        entries = log_entries(text)\n        read_ = research_indexes(', '    if True:\n        entries = log_entries(text)\n        read_ = research_indexes(')],
     [(OWN + "test_research.py::test_approved_designs_research_is_not_read_again", "reports nothing of the research of a design that is applying")]),
    ("a path judged by the place of its checkout, so no shorthand citation resolves in one kept under .ai/tmp/",
     [('    hits = sorted(p for p in md_files(root) if ("/" + p.relative_to(root).as_posix()).endswith(tail))\n',
       '    hits = sorted(p for p in md_files(root) if ".ai/tmp" not in p.as_posix() and ("/" + p.relative_to(root).as_posix()).endswith(tail))\n')],
     [(OWN + "test_checkout.py::test_shorthand_resolves_beneath_working_files", "resolves a file named in shorthand in a checkout standing under")]),
    ("a form read from the checkout holding the script's file",
     [('    base = Path(root) if root else next((p for p in (Path.cwd(), *Path.cwd().parents) if (p / path).exists()), Path.cwd())\n',
       '    base = Path(root) if root else Path(__file__).resolve().parents[3]\n')],
     [(OWN + "test_checkout.py::test_form_is_read_from_the_checkout_run_in", "appends an entry of a kind the canon of the checkout it is run in declares")]),
    ("the entry of a check cut short by a freeing refused, held to the goals of the major version the freeing started",
     [('        if not agreed_before(so_far + [(kind, count, {})], len(so_far), report_version(load_report(design, kind, count))):',
       '        if not agreed_before(so_far + [(kind, count, {})], len(so_far), None):')],
     [(OWN + "test_taken_up.py::test_check_cut_short_by_a_freeing_is_logged", "appends its entry after the freeing, at the version its report read")]),
    ("a loop in the check of a report's form reusing the name that holds the report's parts, so each review settled with Causes is refused",
     [('                asked, at = miss.get("Kind") == "question not asked", where + "\'s Miss " + miss.get("Miss", "")\n                for k in ("Place", "Reads"):\n'
       '                    require(cond, at, miss, k, not asked, "where its Kind is not question not asked")\n                for k in ("Question", "Answer"):\n'
       '                    require(cond, at, miss, k, asked, "where its Kind is question not asked")\n',
       '                asked, held = miss.get("Kind") == "question not asked", where + "\'s Miss " + miss.get("Miss", "")\n                for k in ("Place", "Reads"):\n'
       '                    require(cond, held, miss, k, not asked, "where its Kind is not question not asked")\n                for k in ("Question", "Answer"):\n'
       '                    require(cond, held, miss, k, asked, "where its Kind is question not asked")\n')],
     [(OWN + "test_settled.py::test_round_settled_in_its_form_passes", "passes a taken-up review's report settled with a Cause")]),
)
# The faults of the search, the search being code the skills share, which the design script runs: what each was, the
# edits putting it back into a copy of .ai/skills/lib/search.py, and words of the check that then fails, each a check
# of the one test of the search's kept tests named here.
SEARCHS_TEST = KEPT + "/scripts/search/test_checkout.py::test_a_search_runs_over_the_checkout_it_is_run_in_and_finds_the_model_in_the_main_one"
SEARCH_FAULTS = (
    ("the search's model looked for under the checkout holding its own file, so a second checkout has none",
     [('        _HOME = main_checkout(Path(__file__).resolve().parents[3])\n', '        _HOME = Path(__file__).resolve().parents[3]\n')],
     "the search whose code stands in a second checkout, a worktree, looks for its model where the main checkout keeps it"),
    ("a result's name bounded and never its whole path, so in a folder standing deep the path grows longer than a system opens",
     [('        longest = min(MAX_NAME, MAX_PATH - len(str(Path(folder).resolve())) - 1)\n', '        longest = MAX_NAME\n')],
     "a result written in a folder standing deep keeps its whole path within the longest every system opens, and is written"),
    ("a search naming no project run over the checkout holding its script's file",
     [('    root = Path(root).resolve() if root else checkout_run_in()\n', '    root = Path(root).resolve() if root else Path(__file__).resolve().parents[3]\n')],
     "a search naming no project, run in a second checkout, answers over that checkout's files and writes its result there"),
)


def a_tree(folder, tests=False):
    """-> a copy of the skills of the checkout the tests are run in, with the files of the canon the design script
    reads a form from, in a folder of its own: a tree a fault is put back into. tests gives it the kept tests too,
    and the files the search needs beside those it reads, its model, so the search's own tests run in it."""
    copy_files(CHECKOUT, folder, (".ai/skills",) + FORMS_ALONE + ((KEPT,) if tests else ()))
    if tests:
        import search  # the checkout's own, on the path the set's conftest.py reads the shared code by
        shutil.copytree(search.model_folder(), folder / search.SCRATCH / "model")
    return folder


def planted(tree, edits, script="design_documents.py"):
    """Put a fault back into a tree's design script, or into another script of the code the skills share -> why it
    could not be planted, or None: each anchor standing exactly once, and the script still one Python reads."""
    path = tree / LIB / script
    text = path.read_text(encoding="utf-8").replace("\r\n", "\n")
    for anchor, put in edits:
        if text.count(anchor) != 1:
            return "its anchor stands %d times in %s, not once: %s" % (text.count(anchor), script, anchor.strip().split("\n")[0][:90])
        text = text.replace(anchor, put)
    try:
        compile(text, str(path), "exec")
    except SyntaxError as wrong:
        return "the script holding it is no Python: %s" % wrong
    path.write_text(text, encoding="utf-8", newline="\n")
    return None


def result_of(cases, test):
    """-> (the outcome, what it reported) the report of a run gives of a test named by its file and its function."""
    name = test.split("::")[1]
    found = [case for case in cases or [] if case["test"].split("::")[1] == name]
    return (found[0]["outcome"], found[0]["said"]) if len(found) == 1 else (None, "")


def test_each_fault_put_back_fails_its_tests(check, shared_folder):
    tests = list(dict.fromkeys(test for _, _, holding in FAULTS for test, _ in holding))
    clean = a_tree(shared_folder / "c", tests=True)
    script = (clean / LIB / "design_documents.py").read_bytes()
    why = planted(clean, [("a line that stands nowhere in the design script", "")])
    check("a fault whose anchor does not stand in the script is not planted, and says so, the script left as it was",
          bool(why) and "stands 0 times" in why and (clean / LIB / "design_documents.py").read_bytes() == script, why)
    status, cases, out = a_run(CHECKOUT, shared_folder / "r", tests, tree=clean)
    check("run against a copy of the tree holding no fault, each of those tests passes, so none fails for the copy alone",
          status == 0 and [result_of(cases, test)[0] for test in tests] == ["passed"] * len(tests), out[-3000:])

    def put_back(numbered):
        n, (what, edits, holding) = numbered
        tree = clean if SEARCHING in [test for test, _ in holding] else a_tree(shared_folder / ("t%d" % n))
        why = planted(tree, edits)
        if why:
            return [("NOT PLANTED, so nothing is proved of it: %s: %s" % (what, why), False, "")]
        status, cases, out = a_run(CHECKOUT, shared_folder / ("r%d" % n), [test for test, _ in holding], tree=tree)
        made = []
        for test, symptom in holding:
            outcome, said = result_of(cases, test)
            made.append(("put back, %s, the test fails, in the check the fault breaks: %s" % (what, test.split("::")[1]),
                         status == 1 and outcome == "failed" and "checks did not hold" in said and symptom in said,
                         "the run against the tree holding the fault gave exit %s and the test %s, where a check holding `%s` was to fail:\n%s" % (status, outcome, symptom, (said or out)[-1500:])))
        return made

    # the faults of the search, each put back in turn into the copy holding the kept tests and the search's model, and
    # taken out again: the search's kept tests, run in that copy, test that copy's search
    status, cases, out = a_run(clean, shared_folder / "s", [SEARCHS_TEST])
    check("run in the copy holding no fault, the test of the search's kept tests holding the search's faults passes", status == 0 and result_of(cases, SEARCHS_TEST)[0] == "passed", out[-2000:])
    searching = clean / LIB / "search.py"
    held = searching.read_bytes()
    for n, (what, edits, symptom) in enumerate(SEARCH_FAULTS):
        why = planted(clean, edits, "search.py")
        if why:
            check("NOT PLANTED, so nothing is proved of it: %s: %s" % (what, why), False)
            continue
        status, cases, out = a_run(clean, shared_folder / ("s%d" % n), [SEARCHS_TEST])
        searching.write_bytes(held)
        outcome, said = result_of(cases, SEARCHS_TEST)
        check("put back, %s, the search's kept test fails, in the check the fault breaks: %s" % (what, symptom),
              status == 1 and outcome == "failed" and "checks did not hold" in said and symptom in said,
              "the run in the tree holding the fault gave exit %s and the test %s, where the check `%s` was to fail:\n%s" % (status, outcome, symptom, (said or out)[-1500:]))
    check("each fault of the search taken out again, the copy's search stands as the checkout's", searching.read_bytes() == held)

    # the fault whose test a real search answers is planted last, in the copy holding the search's model
    apart = [(n, fault) for n, fault in enumerate(FAULTS) if SEARCHING not in [test for test, _ in fault[2]]]
    last = [(n, fault) for n, fault in enumerate(FAULTS) if SEARCHING in [test for test, _ in fault[2]]]
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        for made in list(pool.map(put_back, apart)) + [put_back(fault) for fault in last]:
            for label, holds, detail in made:
                check(label, holds, detail)
