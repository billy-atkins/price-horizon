"""The audit's actions over a small project of fixtures on disk: checking the scope, listing the candidates for the
reading audits, and checking the layout of given files; and the entry script's wiring, taking an action's flag,
reaching its unit and exiting as it says."""
import argparse
import subprocess
import sys

import pytest

from audit_set import ENTRY, entry_script, layout, project

pytestmark = [pytest.mark.reads("audit-whole-project.md", "project-specs-index", "project-methodology-index", "project-skills-index",
                                "project-glossary-index", "project-registry-of-three-skills", "project-glossary-of-one-term",
                                "project-skill-file", "project-ignore-file", "project-scope-index", "project-skipped-steps",
                                "project-working-files-index", "project-working-files", "project-spec-style-index",
                                "project-clear-prose", "project-finished-style", "project-register", "project-audit-skill",
                                "project-verify-skill", "project-moorings", "project-moorings-numbered",
                                "project-moorings-counting-boats", "project-moorings-with-no-blank-line")]
# a project breaking no rule holds each table of its data the audit reads, each of the harbor's own
PROJECT = {"project-specs-index": "specs/index.md", "project-methodology-index": "specs/methodology/index.md",
           "project-skills-index": "specs/methodology/skills/index.md", "project-glossary-index": "specs/methodology/glossary/index.md",
           "project-registry-of-three-skills": "specs/methodology/skills/registered-skills.md",
           "project-glossary-of-one-term": "specs/methodology/glossary/glossary.md", "project-skill-file": ".ai/skills/harbor-guide/SKILL.md",
           "project-ignore-file": ".gitignore", "project-scope-index": "specs/methodology/scope/index.md",
           "project-skipped-steps": "specs/methodology/scope/rules-and-skills.md",
           "project-working-files-index": "specs/methodology/working-files/index.md",
           "project-working-files": "specs/methodology/working-files/main.md",
           "project-spec-style-index": "specs/methodology/spec-style/index.md",
           "project-clear-prose": "specs/methodology/spec-style/clear-prose.md",
           "project-finished-style": "specs/methodology/spec-style/what-a-finished-spec-reads-like.md",
           "project-register": "specs/methodology/external-references.md",
           "project-audit-skill": ".ai/skills/audit-specs/SKILL.md", "project-verify-skill": ".ai/skills/verify-spec-implementation/SKILL.md"}


def harbor(work, fixtures, moorings="project-moorings"):
    """-> a project breaking no rule the audit checks, its moorings file the fixture given."""
    return project(work, fixtures, {**PROJECT, moorings: "specs/moorings.md"})


def every_path(path):
    return True


def run(action, root, *values, detail=False):
    return action(argparse.Namespace(detail=detail), root, every_path, list(values) or None)


@pytest.mark.action("--check-scope")
@pytest.mark.passes
def test_checking_a_project_breaking_no_rule_finds_nothing(fixtures, work, capsys):
    assert run(entry_script().check_scope, harbor(work, fixtures)) == 0
    assert capsys.readouterr().out.strip().endswith("0 findings across 18 files")


@pytest.mark.action("--check-scope")
@pytest.mark.reports
def test_checking_a_project_reports_each_finding_under_its_rule(fixtures, work, capsys):
    assert run(entry_script().check_scope, harbor(work, fixtures, "project-moorings-numbered")) == 1
    out = capsys.readouterr().out
    assert "\nsourcing-and-citation/titling-a-heading.md § Titling a Heading\n  specs/moorings.md\n    heading carries an ordinal: 1. Swinging Moorings\n" in out
    assert out.strip().endswith("1 finding across 18 files")


@pytest.mark.action("--list-candidates")
@pytest.mark.passes
def test_listing_candidates_in_a_project_holding_none_lists_no_place(fixtures, work, capsys):
    assert run(entry_script().list_candidates, harbor(work, fixtures), detail=True) == 0
    assert [line for line in capsys.readouterr().out.split("\n") if line.startswith("  ")] == []


@pytest.mark.action("--list-candidates")
@pytest.mark.reports
def test_listing_candidates_lists_each_table_of_words_the_project_holds_none_of(fixtures, work, capsys):
    placed = {k: p for k, p in PROJECT.items() if k not in ("project-clear-prose", "project-finished-style")}
    assert run(entry_script().list_candidates, project(work, fixtures, {**placed, "project-moorings": "specs/moorings.md"}), detail=True) == 0
    out = capsys.readouterr().out
    assert "  specs/methodology/spec-style/clear-prose.md:0  [missing table]\n    no Clear Prose tables of words to read the prose against\n" in out
    assert ("  specs/methodology/spec-style/what-a-finished-spec-reads-like.md:0  [missing table]\n"
            "    no table of a finished spec's phrases to read the specs against\n") in out


@pytest.mark.action("--list-candidates")
@pytest.mark.reports
def test_listing_candidates_lists_a_count_and_a_direction_where_they_stand(fixtures, work, capsys):
    assert run(entry_script().list_candidates, harbor(work, fixtures, "project-moorings-counting-boats")) == 0
    out = capsys.readouterr().out
    numbers = out.split("Candidates for the Ordinals and counts audit: numbers")[1].split("\nCandidates")[0]
    direction = out.split("text pointed at by direction")[1].split("\nCandidates")[0]
    assert "specs/moorings.md:3" in numbers and "specs/moorings.md:3" in direction


@pytest.mark.action("--check-layout")
@pytest.mark.passes
def test_checking_the_layout_of_a_file_in_form_finds_nothing(fixtures, work, capsys):
    root = harbor(work, fixtures)
    assert run(entry_script().check_layout, root, str(root / "specs/moorings.md")) == 0
    assert capsys.readouterr().out.strip() == "0 findings over 1 file"


@pytest.mark.action("--check-layout")
@pytest.mark.reports
def test_checking_the_layout_reports_a_blank_line_missing(fixtures, work, capsys):
    root = harbor(work, fixtures, "project-moorings-with-no-blank-line")
    assert run(entry_script().check_layout, root, str(root / "specs/moorings.md")) == 1
    out = capsys.readouterr().out
    assert "specs/moorings.md:2  spec-style/markdown.md § Blank Lines\n  a blank line missing between a heading and a paragraph" in out


@pytest.mark.action("--check-layout")
@pytest.mark.reports
def test_checking_the_layout_leaves_the_rules_it_read_as_they_were(fixtures, work, capsys):
    root = harbor(work, fixtures, "project-moorings-with-no-blank-line")
    before = list(layout.rules()[1])
    assert run(entry_script().check_layout, root, str(root / "specs/moorings.md")) == 1
    assert layout.rules()[1] == before


@pytest.mark.action("--check-layout")
@pytest.mark.reports
def test_checking_the_layout_refuses_a_file_that_is_not_there(fixtures, work):
    root = harbor(work, fixtures)
    with pytest.raises(SystemExit, match="--check-layout names no file"):
        run(entry_script().check_layout, root, str(root / "specs/tides.md"))


@pytest.mark.action("--check-scope")
@pytest.mark.reports
def test_the_entry_script_takes_a_flag_reaches_its_action_and_exits_as_it_says(fixtures, work):
    root = harbor(work, fixtures, "project-moorings-numbered")
    done = subprocess.run([sys.executable, "-B", str(ENTRY), "--check-scope", "--root", str(root)],
                          capture_output=True, text=True, encoding="utf-8")
    assert done.returncode == 1 and "heading carries an ordinal: 1. Swinging Moorings" in done.stdout


@pytest.mark.action("--check-scope")
@pytest.mark.reports
@pytest.mark.parametrize("given, said", [
    ([], "usage: audit-specs.py"),
    (["--check-scope", "--root", "elsewhere"], "holds no specs/ directory"),
])
def test_the_entry_script_refuses_a_run_it_cannot_make(work, given, said):
    done = subprocess.run([sys.executable, "-B", str(ENTRY)] + given, capture_output=True, text=True, encoding="utf-8", cwd=work)
    assert done.returncode == 2 and said in done.stderr
