"""Static coverage for the template-compliance skill registration and docs."""

from __future__ import annotations

import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
TILE_ROOT = REPO_ROOT / "tiles" / "good-oss-citizen"


def test_template_compliance_registered_with_reference() -> None:
    tile = json.loads((TILE_ROOT / "tile.json").read_text())
    assert tile["skills"]["template-compliance"]["path"] == "skills/template-compliance/SKILL.md"

    readme = (TILE_ROOT / "README.md").read_text()
    assert "template-compliance" in readme
    assert "23 commands" in readme
    assert "~8k tokens for core skill files" in readme

    rules = (TILE_ROOT / "rules" / "good-oss-citizen.md").read_text()
    assert "templates-pr`, `body`, `file`" in rules

    skill = (TILE_ROOT / "skills" / "template-compliance" / "SKILL.md").read_text()
    assert "references/body-template-compliance-rubric.md" in skill
    for rare_reference in (
        "references/body-template-compliance-examples.md",
        "fixtures/",
        "evals/",
    ):
        assert rare_reference not in skill
    assert "templates-issue" in skill
    assert "templates-pr" in skill
    assert "github.sh body" in skill
    assert "Information already present elsewhere in the same body" in skill
    assert "Before counting or selecting issue templates" in skill
    assert ".github/ISSUE_TEMPLATE/config.yml" in skill
    assert "treat the repository as having no issue template" in skill


def test_template_compliance_rubric_names_expected_output_buckets() -> None:
    rubric = (
        TILE_ROOT
        / "skills"
        / "template-compliance"
        / "references"
        / "body-template-compliance-rubric.md"
    ).read_text()
    for text in (
        "Matches well enough",
        "Slight deviation",
        "Significant deviation",
        "Template compliance gaps",
        "Information already present elsewhere in the same body",
        "Genuinely missing information",
        "Things to check manually",
        "Optional comment snippets for manual use",
        "No comment needed",
        "select one",
        "select all that apply",
        "materially different",
        "Quote both the template label and the actual selected label",
        "Use the title only to select a template or detect inconsistencies",
        "Do not give credit for chat context",
        "Always use the word `template`, never `form`",
        "four-backtick markdown block",
    ):
        assert text in rubric
    assert "body" in rubric.lower()


def test_template_compliance_examples_cover_existing_edge_cases() -> None:
    examples = (
        TILE_ROOT
        / "skills"
        / "template-compliance"
        / "references"
        / "body-template-compliance-examples.md"
    ).read_text()
    for text in (
        "fixtures/synthetic-pr-template/templates/pr-template.md",
        "fixtures/synthetic-pr-template/expected-results.json",
        "remove-unchecked-options",
        "rename-selected-checkbox-bugfix-to-issue",
        "rename-selected-checkbox-security-hardening-to-security",
        "add-extra-section",
        "remove-one-required-section",
        "remove-several-required-sections",
        "introduce-breaking-change-contradiction",
        "openclaw/openclaw#59898",
        "openclaw/openclaw#66877",
        "openclaw/openclaw#72316",
        "openclaw/openclaw#72345",
        "openclaw/openclaw#66663",
        "fixtures/openclaw-a08b65a/expected-results.json",
        "a08b65a90a454fbfe2ea4025f5bcdab08640d983",
        "https://github.com/openclaw/openclaw/blob/a08b65a90a454fbfe2ea4025f5bcdab08640d983/.github/pull_request_template.md",
        "Matches well enough",
        "Slight deviation",
        "Significant deviation",
        "Things to check manually",
        "No comment needed",
        "Backward compatible? (Yes/No) Yes",
        "messageBridge.rawCaption",
        "messageBridge.safeCaption",
    ):
        assert text in examples


def test_template_compliance_synthetic_fixtures_are_reproducible() -> None:
    fixture_root = (
        TILE_ROOT
        / "skills"
        / "template-compliance"
        / "references"
        / "fixtures"
        / "synthetic-pr-template"
    )
    expected = json.loads((fixture_root / "expected-results.json").read_text())
    assert expected["templateFile"] == "templates/pr-template.md"
    assert (fixture_root / expected["templateFile"]).exists()
    case_ids = {case["id"] for case in expected["cases"]}
    assert {
        "remove-unchecked-options",
        "rename-selected-checkbox-bugfix-to-issue",
        "rename-selected-checkbox-security-hardening-to-security",
        "add-extra-section",
        "remove-one-required-section",
        "remove-several-required-sections",
        "introduce-breaking-change-contradiction",
        "remove-openclaw-prompt-instructions",
        "keep-openclaw-prompt-instructions",
        "remove-fillable-os-field-label",
        "yesno-field-empty",
    }.issubset(case_ids)
    for case in expected["cases"]:
        assert (fixture_root / case["bodyFile"]).exists(), case
        assert case["expectedResult"] in {
            "Matches well enough",
            "Slight deviation",
            "Significant deviation",
        }
        assert isinstance(case.get("expectedManualCheck", False), bool)

    readme = (fixture_root / "README.md").read_text()
    assert "How to execute the check" in readme
    assert "mutation described by their file name" in readme


def test_template_compliance_openclaw_fixtures_are_reproducible() -> None:
    fixture_root = (
        TILE_ROOT
        / "skills"
        / "template-compliance"
        / "references"
        / "fixtures"
        / "openclaw-a08b65a"
    )
    expected = json.loads((fixture_root / "expected-results.json").read_text())
    assert expected["sourceRepository"] == "openclaw/openclaw"
    assert expected["templateCommit"] == "a08b65a90a454fbfe2ea4025f5bcdab08640d983"
    assert expected["templatePermalinks"]["pullRequest"].startswith(
        "https://github.com/openclaw/openclaw/blob/a08b65a90a454fbfe2ea4025f5bcdab08640d983/"
    )
    assert len(expected["cases"]) == 5
    for case in expected["cases"]:
        assert (fixture_root / case["templateFile"]).exists(), case
        assert (fixture_root / case["bodyFile"]).exists(), case
        assert case["expectedResult"] in {
            "Matches well enough",
            "Slight deviation",
            "Significant deviation",
        }
        assert case["liveUrl"].startswith("https://github.com/openclaw/openclaw/")

    readme = (fixture_root / "README.md").read_text()
    assert "How to execute the check" in readme
    assert "If live data differs from these files" in readme


def test_template_compliance_examples_cover_prompt_text_removal() -> None:
    examples = (
        TILE_ROOT
        / "skills"
        / "template-compliance"
        / "references"
        / "body-template-compliance-examples.md"
    ).read_text()
    for text in (
        "remove-openclaw-prompt-instructions",
        "keep-openclaw-prompt-instructions",
        "remove-fillable-os-field-label",
        "Describe the problem and fix in 2–5 bullets:",
        "If this PR fixes a plugin beta-release blocker",
        "Contributors cannot label PRs",
        "For bug fixes or regressions, explain why this happened",
        "List user-visible changes (including defaults/config)",
        "- OS:",
        "helper instructions",
        "fillable field label identifies required information",
    ):
        assert text in examples


def test_template_compliance_examples_cover_yes_no_required_fields() -> None:
    examples = (
        TILE_ROOT
        / "skills"
        / "template-compliance"
        / "references"
        / "body-template-compliance-examples.md"
    ).read_text()
    for text in (
        "yesno-field-answer-without-option-hint",
        "yesno-field-answer-with-option-hint",
        "yesno-field-empty",
        "yesno-field-placeholder-left-as-answer",
        "yesno-field-invalid-answer",
        "New permissions/capabilities? Yes",
        "New permissions/capabilities? (Yes/No) Yes",
        "New permissions/capabilities? (Yes/No) Yes/No",
        "New permissions/capabilities? (Yes/No) Test",
        "not one of the required `Yes` / `No` values",
    ):
        assert text in examples


def test_template_compliance_rubric_covers_yes_no_required_fields() -> None:
    rubric = (
        TILE_ROOT
        / "skills"
        / "template-compliance"
        / "references"
        / "body-template-compliance-rubric.md"
    ).read_text()
    for text in (
        "required inline fields with option hints",
        "New permissions/capabilities? (Yes/No)",
        "New permissions/capabilities? Yes",
        "New permissions/capabilities? (Yes/No) Yes",
        "repeats the placeholder/options as the answer",
        "outside the listed options",
    ):
        assert text in rubric


def test_template_compliance_evals_cover_existing_body_reviews() -> None:
    eval_root = TILE_ROOT / "evals"
    expected = {
        "streamqueue-existing-issue-template-compliance": (
            "github.sh body good-oss-citizen/demo-streamqueue 2",
            "Slight deviation",
            "Environment",
        ),
        "streamqueue-existing-pr-template-compliance": (
            "github.sh body good-oss-citizen/demo-streamqueue 8",
            "Significant deviation",
            "AI Assistance",
        ),
        "synthetic-pr-subtle-breaking-change-template-compliance": (
            "introduce-breaking-change-contradiction.md",
            "Things to check manually",
            "messageBridge.rawCaption",
        ),
    }
    for name, required_texts in expected.items():
        task = (eval_root / name / "task.md").read_text()
        criteria = json.loads((eval_root / name / "criteria.json").read_text())
        assert "Do not post anything to GitHub" in task
        criteria_text = json.dumps(criteria)
        for text in required_texts:
            assert text in criteria_text


def main() -> int:
    """Run the static checks without requiring pytest in CI."""
    test_template_compliance_registered_with_reference()
    test_template_compliance_rubric_names_expected_output_buckets()
    test_template_compliance_examples_cover_existing_edge_cases()
    test_template_compliance_synthetic_fixtures_are_reproducible()
    test_template_compliance_openclaw_fixtures_are_reproducible()
    test_template_compliance_examples_cover_prompt_text_removal()
    test_template_compliance_examples_cover_yes_no_required_fields()
    test_template_compliance_rubric_covers_yes_no_required_fields()
    test_template_compliance_evals_cover_existing_body_reviews()
    print("template-compliance static checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
