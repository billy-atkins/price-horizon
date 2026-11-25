"""The checkout a design is worked in: its last commit, the files it holds changed, the audits its design owes, what
a Refactor and Refine cycle changed in it, its citations' links, its constructs, and its place on the machine."""
import pytest

from design_script_set import (APPLYING, DRAFTED, NAME, Project, SKILLS, a_design, git, passes, reports, shown, swap)

pytestmark = [pytest.mark.reads("design-script-ferry.md", "island-guide")]


RETITLED = "## The Ferry and Its Times"


@pytest.mark.reads("design-script-ferry.md", "ferry-design")
def test_applying_designs_citations_read_at_the_last_commit(check, fixtures):
    for skill in SKILLS:
        p = Project("applying-cited", versioned=True)
        design = p.design(skill=skill, status="applying", log=APPLYING)
        p.put("docs/guide.md", swap(fixtures["island-guide"], "## The Ferry", RETITLED) + "\n## The Harbour\n\nThe harbour was dredged last spring.\n")
        got = p.run("--check-cited-headings", design, skill=skill)
        check("--check-cited-headings of %s reports nothing of an applying design citing a heading its own apply retitled" % skill,
              passes(got, "== check-cited-headings", "1 citation, 0 broken"), shown(got))
        text = swap(a_design("harbour-cited", skill=skill, status="applying", log=APPLYING), "and `docs/guide.md § The Ferry` names", "and `docs/guide.md § The Harbour` names")
        got = p.run("--check-cited-headings", p.design("harbour-cited", skill=skill, text=text), skill=skill)
        check("--check-cited-headings of %s reports an applying design citing a heading the last commit does not hold, one its apply wrote among them" % skill,
              reports(got, "== check-cited-headings", ["BROKEN", "§ The Harbour", "no such heading", "1 broken"]), shown(got))
        (p.root / "docs/guide.md").unlink()
        got = p.run("--check-cited-headings", design, skill=skill)
        check("--check-cited-headings of %s reports nothing of an applying design citing a file its own apply removed" % skill, passes(got, "== check-cited-headings", "1 citation, 0 broken"), shown(got))


@pytest.mark.action("--check-changed-files")
@pytest.mark.passes
@pytest.mark.reports
@pytest.mark.reads("design-script-ferry.md", "ferry-design")
@pytest.mark.reads("design-script-pages.md", "notes-citing-nothing", "spring-tides-page")
def test_changed_files_within_and_outside_the_target(check, fixtures):
    for skill in SKILLS:
        p = Project("changed-files", versioned=True)
        design = p.design(skill=skill, status="applying", log=APPLYING, Target="`docs/guide.md`; `docs/tides/`")
        p.put("docs/guide.md", fixtures["island-guide"] + "\nThe first ferry leaves at seven.\n")
        p.put("docs/tides/spring.md", fixtures["spring-tides-page"])
        got = p.run("--check-changed-files", design, skill=skill)
        check("--check-changed-files of %s passes where each changed file is one the Target names, one created under a directory it names, or a working file" % skill,
              passes(got, "== check-changed-files " + NAME, "0 problems"), shown(got))
        p.put("docs/notes.md", fixtures["notes-citing-nothing"])  # a page written beside the work, outside the Target
        got = p.run("--check-changed-files", design, skill=skill)
        check("--check-changed-files of %s reports a file changed outside the Target that no entry of the log names" % skill,
              reports(got, "== check-changed-files " + NAME, ["docs/notes.md\n  changed outside the Target, and no entry of the log names it", "1 problem"]), shown(got))
        design = p.design(skill=skill, status="applying", log=APPLYING + (("user-edit", {"Places": "`docs/notes.md`"}),), Target="`docs/guide.md`; `docs/tides/`")
        got = p.run("--check-changed-files", design, skill=skill)
        check("--check-changed-files of %s marks a file changed outside the Target that a user-edit entry names, and reports nothing" % skill,
              passes(got, "== check-changed-files " + NAME, "0 problems") and "docs/notes.md\n  changed outside the Target, the user's edit" in got[1], shown(got))


# @canon-spec specs/methodology/working-files/main.md § Design Log Entry § Script Checks [Name: audits-run-or-bypassed]
@pytest.mark.action("--check-audits")
@pytest.mark.passes
@pytest.mark.reports
@pytest.mark.reads("design-script-ferry.md", "ferry-design")
def test_audits_run_bypassed_or_owed(check):
    for skill in SKILLS:
        p = Project("audits")
        got = p.run("--check-audits", p.design(skill=skill, status="applying", log=APPLYING), skill=skill)
        check("--check-audits of %s reports a design that changed a file of a sub-scope and whose log records neither the specs audit's run nor its bypass since its apply" % skill,
              reports(got, "== check-audits " + NAME, "neither run nor bypassed since the last apply entry: the specs audit, .ai/skills/audit-specs/"), shown(got))
        got = p.run("--check-audits", p.design(skill=skill, status="applying", log=APPLYING + (("audit-bypass", {"Audit": "specs"}),)), skill=skill)
        check("--check-audits of %s passes a design whose log records the user's bypass of the audit" % skill, passes(got, "== check-audits " + NAME, "0 problems"), shown(got))
        got = p.run("--check-audits", p.design(skill=skill, status="applying", log=APPLYING + (("audit-specs", {"Design Version": "1.0.1"}),)), skill=skill)
        check("--check-audits of %s passes a design whose log records the audit's run" % skill, passes(got, "== check-audits " + NAME, "0 problems"), shown(got))
        got = p.run("--check-audits", p.design(skill=skill, status="applying", log=APPLYING + (("audit-bypass", {"Audit": "specs"}), ("entered", {"Reason": "sent back"}), ("plan-approval", {"Approval": "approved"}), ("apply", {}))), skill=skill)
        check("--check-audits of %s reports a design whose audit was bypassed before its last apply entry alone" % skill, reports(got, "== check-audits " + NAME, "neither run nor bypassed since the last apply entry"), shown(got))


@pytest.mark.action("--show-refactor-and-refine-of-existing-specs")
@pytest.mark.passes
@pytest.mark.reads("design-script-pages.md", "birds-spec")
def test_refactor_and_refine_shows_what_changed(check, fixtures):
    p = Project("refactor-and-refine", canon=False)
    home = p.put("specs/birds.md", fixtures["birds-spec"])
    git(p.root, "init", "-q")
    p.commit()
    p.put(home, swap(p.read(home), "The egret wades the shallows at first light alone.\n", "The heron stands in the reeds at dusk and waits.\n\nA crane flies over.\n"))
    got = p.run("--show-refactor-and-refine-of-existing-specs", "HEAD")
    check("--show-refactor-and-refine-of-existing-specs lists each line now repeated, lost and new since the baseline, with the file holding it",
          passes(got, "== show-refactor-and-refine-of-existing-specs since HEAD", "1 repeated, 1 lost, 1 new")
          and "repeated   The heron stands in the reeds at dusk and waits.\n           in " + home in got[1]
          and "lost       The egret wades the shallows at first light alone.\n" in got[1] and "new        A crane flies over.\n" in got[1], shown(got))


@pytest.mark.action("--show-refactor-and-refine-of-existing-specs")
@pytest.mark.passes
@pytest.mark.reads("design-script-pages.md", "birds-spec-carrying-links")
def test_refactor_and_refine_over_specs_carrying_links_shows_the_change_alone(check, fixtures):
    p = Project("refactor-and-refine-links", canon=False)
    home = p.put("specs/birds.md", fixtures["birds-spec-carrying-links"])
    git(p.root, "init", "-q")
    p.commit()
    got = p.run("--show-refactor-and-refine-of-existing-specs", "HEAD")
    check("--show-refactor-and-refine-of-existing-specs shows no line of a spec whose citations carry links as lost or as new where nothing changed since the baseline",
          passes(got, "== show-refactor-and-refine-of-existing-specs since HEAD", "0 repeated, 0 lost, 0 new"), shown(got))
    p.put(home, p.read(home) + "\nA crane flies over.\n")  # the cycle adds one line, and changes no other
    got = p.run("--show-refactor-and-refine-of-existing-specs", "HEAD")
    check("and, a cycle adding one line, shows that line as new and no line as lost, each side read with its citations' links set aside",
          passes(got, "== show-refactor-and-refine-of-existing-specs since HEAD", "0 repeated, 0 lost, 1 new") and "new        A crane flies over.\n           in " + home in got[1]
          and "lost " not in got[1] and "](/specs/birds.md" not in got[1], shown(got))
    p.put(home, swap(p.read(home), "The egret wades the shallows at first light", "The egret wades the shallows at dusk"))  # and changes a line carrying a link
    got = p.run("--show-refactor-and-refine-of-existing-specs", "HEAD")
    check("and shows a changed line carrying a link once as lost and once as new, as its citation is written",
          passes(got, "== show-refactor-and-refine-of-existing-specs since HEAD", "0 repeated, 1 lost, 2 new")
          and "lost       The egret wades the shallows at first light, far from the reeds of `specs/birds.md § The Heron`." in got[1], shown(got))


@pytest.mark.action("--show-refactor-and-refine-of-existing-specs")
@pytest.mark.reports
def test_refactor_and_refine_refuses_no_commit(check):
    p = Project("refactor-and-refine-refused", versioned=True)
    got = p.run("--show-refactor-and-refine-of-existing-specs", "no-such-commit")
    check("--show-refactor-and-refine-of-existing-specs refuses a baseline that is no commit, exit 2", got[0] == 2 and "no such commit: no-such-commit" in got[1], shown(got))
    p = Project("refactor-and-refine-no-git")
    got = p.run("--show-refactor-and-refine-of-existing-specs", "HEAD")
    check("--show-refactor-and-refine-of-existing-specs refuses a project under no version control, exit 2", got[0] == 2 and "run it from the repository's root" in got[1], shown(got))


@pytest.mark.action("--refresh-links")
@pytest.mark.reports
@pytest.mark.reads("design-script-pages.md", "notes-citing-the-ferry")
def test_links_are_written(check, fixtures):
    p = Project("links", canon=False)
    p.put("docs/notes.md", fixtures["notes-citing-the-ferry"])
    got = p.run("--refresh-links", p.root)
    check("--refresh-links writes the link a citation lacks, and says how many files it changed",
          passes(got, "== refresh-links", "1 files changed") and "[`docs/guide.md § The Ferry`](/docs/guide.md#the-ferry)" in p.read("docs/notes.md"), shown(got) + p.read("docs/notes.md"))


@pytest.mark.action("--refresh-links")
@pytest.mark.passes
@pytest.mark.reads("design-script-pages.md", "notes-citing-the-ferry")
def test_current_links_are_left(check, fixtures):
    p = Project("links-current", canon=False)
    # the page's one citation given its link, so no link is left to write
    p.put("docs/notes.md", swap(fixtures["notes-citing-the-ferry"], "`docs/guide.md § The Ferry`", "[`docs/guide.md § The Ferry`](/docs/guide.md#the-ferry)"))
    before = p.held("docs")
    got = p.run("--refresh-links", p.root)
    check("--refresh-links changes no file whose every citation carries its link", passes(got, "== refresh-links", "0 files changed") and p.held("docs") == before, shown(got))


@pytest.mark.action("--check-constructs")
@pytest.mark.passes
@pytest.mark.reads("design-script-record-parts.md", "hours-decision-table")
def test_construct_in_its_form_passes(check, fixtures):
    p = Project("constructs")
    path = p.put("docs/guide.md", swap(fixtures["island-guide"], "The ferry leaves from the north quay.\n", "The ferry leaves from the north quay.\n\n" + fixtures["hours-decision-table"]))
    got = p.run("--check-constructs", path)
    check("--check-constructs passes a file in scope whose Decision Table holds its form", passes(got, "== check-constructs docs/guide.md", "0 findings"), shown(got))


@pytest.mark.action("--check-constructs")
@pytest.mark.reports
@pytest.mark.reads("design-script-ferry.md", "ferry-design")
@pytest.mark.reads("design-script-record-parts.md", "hours-decision-table")
def test_construct_out_of_its_form_is_reported(check, fixtures):
    p = Project("constructs-reports")
    table = swap(fixtures["hours-decision-table"], "**Hit Policy:** First", "**Hit Policy:** Whenever")  # a Hit Policy the construct does not give
    path = p.put("docs/guide.md", swap(fixtures["island-guide"], "The ferry leaves from the north quay.\n", "The ferry leaves from the north quay.\n\n" + table))
    got = p.run("--check-constructs", path)
    check("--check-constructs reports a Decision Table whose Hit Policy is none the construct gives", reports(got, "== check-constructs docs/guide.md", ["docs/guide.md:", "Hit Policy", "1 finding"]), shown(got))
    got = p.run("--check-constructs", p.design(log=DRAFTED))
    check("--check-constructs refuses a design document, whose Drafts the validation review checks, exit 2", got[0] == 2 and "no file in scope; a design's Drafts are checked by --check-design" in got[1], shown(got))


@pytest.mark.reads("design-script-ferry.md", "ferry-design")
@pytest.mark.reads("design-script-pages.md", "guide-draft")
def test_shorthand_resolves_beneath_working_files(check, fixtures):
    for under in (None, ".ai/tmp/worktrees/elsewhere"):
        p = Project("place", under=under)
        p.put(".ai/tmp/design-specs/scratch/guide.md", fixtures["guide-draft"])
        design = p.design(text=swap(a_design(log=DRAFTED), "and `docs/guide.md § The Ferry` names", "and `guide.md § The Ferry` names"))
        got = p.run("--check-cited-headings", design)
        check("--check-cited-headings resolves a file named in shorthand in a checkout %s, a file of the same name among the skills' own output aside"
              % ("standing under `%s` of another folder" % under if under else "standing anywhere"),
              passes(got, "== check-cited-headings", "2 citations, 0 broken") and "ok        guide.md" in got[1], shown(got))
        form = p.run("--check-design-form", design)
        names = p.run("--check-design-names", design)
        check("and the design's form and its names read the same there", passes(form, "== check-design-form", "0 problems") and passes(names, "== check-design-names", "0 problems"), shown(form) + shown(names))


@pytest.mark.reads("design-script-ferry.md", "ferry-design")
def test_form_is_read_from_the_checkout_run_in(check):
    kinds = "| `apply` | none | none | as applying begins |\n"
    p = Project("form-run-in")
    home = "specs/methodology/working-files/main.md"
    p.put(home, swap(p.read(home), kinds, kinds + "| `ferry-sailed` | none | none | as the ferry sails |\n"))
    design = p.design(log=DRAFTED)
    got = p.run("--log-entry", design, "ferry-sailed")
    check("--log-entry appends an entry of a kind the canon of the checkout it is run in declares, whichever checkout holds the script's own file",
          passes(got, "== log-entry", "- **Entry:** ferry-sailed-1"), shown(got))
    form = p.run("--check-design-form", design)
    check("and --check-design-form reads the log it wrote by the same canon", passes(form, "== check-design-form", "0 problems"), shown(form))
    p = Project("form-as-it-stands")
    got = p.run("--log-entry", p.design(log=DRAFTED), "ferry-sailed")
    check("--log-entry refuses the same kind in a checkout whose canon declares none such", reports(got, "== log-entry, not logged", "a log entry's kind is not one of"), shown(got))


@pytest.mark.action("--check-design-form")
@pytest.mark.passes
@pytest.mark.reports
@pytest.mark.reads("design-script-ferry.md", "ferry-design")
def test_form_is_read_from_no_folder_above_the_project_run_in(check):
    # each project stands beneath the checkout the tests are run in, whose own canon holds every form
    for versioned in (True, False):
        under = "under version control of its own" if versioned else "under no version control"
        p = Project("forms-of-its-own", versioned=versioned)
        design = p.design(log=DRAFTED)
        got = p.run("--check-design-form", design)
        check("--check-design-form, run at the root of a project %s holding the files a form is read from, reads the project's forms and passes a design in its form" % under,
              passes(got, "== check-design-form " + NAME, "0 problems"), shown(got))
        if versioned:
            got = p.run("--check-design-form", "../" + design, inside="docs")
            check("and, run from a folder inside that project, reads the forms from the project's root, and passes the same design",
                  passes(got, "== check-design-form " + NAME, "0 problems"), shown(got))
        p = Project("no-canon", versioned=versioned, canon=False)
        got = p.run("--check-design-form", p.design(log=DRAFTED))
        check("--check-design-form, run in a project %s holding no file of the canon, reports that design's forms as ones it cannot read, and reads none from the checkout the project stands beneath" % under,
              reports(got, "== check-design-form " + NAME, ["no file declares the", "the layout check reads no Decision Table of where a blank line falls in spec-style/markdown.md § Blank Lines"])
              and "0 problems" not in got[1], shown(got))
