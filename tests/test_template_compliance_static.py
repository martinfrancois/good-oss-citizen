"""Static guards for template-compliance eval and rubric policy."""

from __future__ import annotations

import json
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
TILE_ROOT = REPO_ROOT / "tiles" / "good-oss-citizen"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_synthetic_contradiction_eval_requires_author_clarification() -> None:
    task = read(
        TILE_ROOT
        / "evals"
        / "synthetic-pr-subtle-breaking-change-template-compliance"
        / "task.md"
    )
    criteria = json.loads(
        read(
            TILE_ROOT
            / "evals"
            / "synthetic-pr-subtle-breaking-change-template-compliance"
            / "criteria.json"
        )
    )
    descriptions = "\n".join(
        f"{item['name']}\n{item['description']}" for item in criteria["checklist"]
    )
    task_lines = task.splitlines()
    breaking_line = next(
        index
        for index, line in enumerate(task_lines)
        if "breaking change for plugins importing the old helper" in line
    )
    backward_compatible_line = next(
        index
        for index, line in enumerate(task_lines[breaking_line + 1 :], start=breaking_line + 1)
        if "Backward compatible? (Yes/No) Yes" in line
    )

    assert "manual-check concept" not in task
    assert "Matches well enough" not in task
    assert "synonym" not in task.lower()
    assert "contradiction" not in task.lower()
    assert "conflict" not in task.lower()
    assert "inconsistent" not in task.lower()
    assert "ask them to revise" in task
    assert "breaking change for plugins importing the old helper" in task
    assert "Backward compatible? (Yes/No) Yes" in task
    assert backward_compatible_line - breaking_line >= 12
    assert "Result: Slight deviation" in descriptions
    assert "author needs to clarify" in descriptions
    assert "must not be `No comment needed`" in descriptions
    assert "private/manual triager note" in descriptions


def test_rubric_treats_unreliable_required_answers_as_compliance_gaps() -> None:
    rubric = read(TILE_ROOT / "skills" / "preflight" / "body-template-compliance-rubric.md")
    triage = read(TILE_ROOT / "skills" / "triage" / "SKILL.md")

    assert "makes a required section or answer unclear" in rubric
    assert "classify as `Slight deviation`, ask the author to clarify only that answer" in rubric
    assert "practical impact, scope, risk, reviewer action, or maintainer decision" in rubric
    assert "focused clarification of internally inconsistent required answers" in rubric
    assert "field is present but unreliable" in rubric
    assert "what follow-up information is needed" in rubric
    assert "contradictions that make required answers unreliable are in the main comment" in rubric
    assert "filled with an on-the-page answer stays in this bucket even when" not in rubric
    assert "Result: Slight deviation" in rubric
    assert "Things to check manually` is auxiliary" in triage
    assert "do not put the internal `Result: ...` label" in triage
    assert "stripped testing/checklist confirmation items" in triage
    assert "focused clarification of internally inconsistent required answers" in triage
    assert "start with the exact phrase `Result: Significant deviation`" not in triage
    assert "field is present but unreliable" in triage
    assert "what follow-up information is needed" in triage


def test_uncertain_inconsistencies_remain_manual_check_only() -> None:
    rubric = read(TILE_ROOT / "skills" / "preflight" / "body-template-compliance-rubric.md")

    assert "Suspicious but uncertain inconsistencies can stay in this bucket" in rubric
    assert "required template answers remain usable" in rubric
    assert "surface them in **Things to check manually** instead of the main comment" in rubric
    assert "does not make a required answer unreliable enough for the main comment" in rubric
    assert "manual-check items go in the optional snippets section, not in the main comment" in rubric
    assert "Things to check manually** is for uncertain scope or truth checks" in rubric


def test_conditionally_removable_sections_require_body_local_condition() -> None:
    rubric = read(TILE_ROOT / "skills" / "preflight" / "body-template-compliance-rubric.md")
    criteria = json.loads(
        read(TILE_ROOT / "evals" / "streamqueue-existing-pr-template-compliance" / "criteria.json")
    )
    descriptions = "\n".join(
        f"{item['name']}\n{item['description']}" for item in criteria["checklist"]
    )

    assert "conditionally removable required section" in rubric
    assert "the same body does not clearly satisfy the removal condition" in rubric
    assert "the body itself must clearly satisfy that condition" in descriptions


def test_always_on_rules_cover_existing_body_template_triage() -> None:
    rules = read(TILE_ROOT / "rules" / "good-oss-citizen.md")

    assert "even if no skill activates" in rules
    assert "MUST name the selected template path" in rules
    assert "MUST report exactly one main result label" in rules
    assert "Result: Significant deviation" in rules
    assert "NEVER list every missing checkbox or prompt" in rules
    assert "stripped testing/checklist confirmation items" in rules
    assert "direct blob URL" in rules
    assert "lacks this URL, it is incomplete" in rules
    assert "practical impact, scope, risk, reviewer action, or maintainer decision" in rules


def test_rubric_preserves_observed_template_audit_distinctions() -> None:
    rubric = read(TILE_ROOT / "skills" / "preflight" / "body-template-compliance-rubric.md")

    assert "Do not use `Matches well enough` just because a reviewer can infer missing information" in rubric
    assert "Credit only information that appears in the same issue or PR body being checked" in rubric
    assert "information already present elsewhere in the same body" in rubric
    assert "Do not treat visible unchecked options as a problem" in rubric
    assert "Ignore differences in unchecked options unless they make the selected choices unclear" in rubric
    assert "do not list, analyze, or comment on harmless unchecked-option drift" in rubric
    assert "not compliance gaps, not manual checks, and not useful explanation" in rubric
    assert "Compare selected labels against the current template" in rubric
    assert "broader, narrower, less precise, or ambiguous" in rubric
    assert "Suspicious checkbox selections" in rubric
    assert "selected `Feature` checkbox appears next to a body that only describes a bug fix" in rubric
    assert "if `Feature` is selected but the body describes only a bug fix" in rubric
    assert "Name the selected checkbox directly in the manual-check item" in rubric
    assert "When two body statements can reasonably both be true" in rubric
    assert "if the practical impact is only uncertain, route it to manual checks" in rubric
    assert "Optional comment snippets for manual use" in rubric
    assert "Always report exactly one main result label" in rubric
    assert "Template compliance gaps" in rubric
    assert "Genuinely missing information" in rubric
    assert "Always use the word `template`, never `form`" in rubric
    assert "Avoid weak phrasing like `Would you mind`, `If you want`, or `You may want`" in rubric
    assert "do not put the internal `Result: ...` label inside the contributor-facing comment" in rubric
    assert "AI Assistance / AI disclosure section" in rubric
    assert "primary compliance gap" in rubric
    assert "field is present but unreliable" in rubric
    assert "what follow-up information is needed" in rubric


def test_triage_no_template_and_no_post_rules_are_explicit() -> None:
    triage = read(TILE_ROOT / "skills" / "triage" / "SKILL.md")
    rules = read(TILE_ROOT / "rules" / "good-oss-citizen.md")

    assert "check whether the PR body follows the repository's pull request template" in triage
    assert "quick check on this open issue" in triage
    assert "body is good enough" in triage
    assert "proceed directly to Step 6" in triage
    assert "write `triage_comment.md` in the workspace root" in triage
    assert "`triage_comment.md`" in rules
    assert "separate from judging whether the body is good or bad" in triage
    assert "no repository template to grade it against" in triage
    assert "explicitly say you did not post it" in triage
    assert "decline to post it" in triage
    assert "their action and their voice" in triage
    assert "I did not post this to GitHub" in triage


def test_propose_and_preflight_preserve_template_selection_and_disclosure_format() -> None:
    propose = read(TILE_ROOT / "skills" / "propose" / "SKILL.md")
    preflight = read(TILE_ROOT / "skills" / "preflight" / "SKILL.md")

    assert "name the candidate paths you considered" in propose
    assert "note any labels the contributor should apply through the GitHub UI" in propose
    assert "If `disclosure-format.data.format` is `code_block`" in propose
    assert "fenced code block in that declared format" in propose
    assert "Do not leave empty bullets" in propose
    assert "Not provided yet" in propose
    assert "name every candidate template path returned by the helper" in propose
    assert "including non-selected templates such as bug reports when drafting a feature request" in propose
    assert "explicitly tell the contributor which labels from front matter to apply through the GitHub UI" in propose
    assert "Template selected: <path> because <reason>" in propose
    assert "Candidate templates considered: <path>, <path>, ..." in propose
    assert "GitHub UI labels to apply: <labels from front matter>" in propose
    assert "Template selected: <path> fetched with templates-issue" in propose
    assert "Unknown from report" in propose
    assert "first use concrete values available from the task, local context, or repository metadata" in propose
    assert "Python version from the local runtime" in propose
    assert "package version from `pyproject.toml`" in propose
    assert "Avoid `Not provided yet` wording" in propose
    assert "For voluntary disclosure or any non-`code_block` project format" in propose
    assert "Never wrap voluntary disclosure in triple backticks" in propose
    assert "must not appear between any ``` fence lines" in propose
    assert "write them as normal Markdown bullets or lines under `## AI Disclosure`, not inside ``` fences" in propose
    assert "list the candidate template paths considered" in preflight
    assert "include the explicit because-clause" in preflight
    assert "Template selected: <path> because <reason>" in preflight
    assert "Candidate templates considered: <path>, <path>, ..." in preflight
    assert "Remove template helper comments and instructional placeholders" in preflight


def test_synthetic_checkbox_eval_covers_selected_vs_unchecked_semantics_without_prompt_leak() -> None:
    task = read(
        TILE_ROOT
        / "evals"
        / "synthetic-pr-checkbox-label-drift-template-compliance"
        / "task.md"
    )
    criteria = json.loads(
        read(
            TILE_ROOT
            / "evals"
            / "synthetic-pr-checkbox-label-drift-template-compliance"
            / "criteria.json"
        )
    )
    descriptions = "\n".join(
        f"{item['name']}\n{item['description']}" for item in criteria["checklist"]
    )

    assert "Result: Slight deviation" not in task
    assert "Things to check manually" not in task
    assert "unchecked options may remain" not in task
    assert "Bug fix" in task
    assert "Issue" in task
    assert "Refactor required for the fix" in task
    assert "Refactor" in task
    assert "visible unchecked options" in descriptions
    assert "unchecked `Chore/infra` became unchecked `CI`" in descriptions
    assert "selected `Issue` does not preserve the meaning of template label `Bug fix`" in descriptions
    assert "selected `Refactor` does not preserve the meaning of `Refactor required for the fix`" in descriptions
    assert "Things to check manually" in descriptions


def test_synthetic_manual_check_eval_covers_non_actionable_scope_signal() -> None:
    task = read(
        TILE_ROOT
        / "evals"
        / "synthetic-pr-uncertain-scope-manual-check-template-compliance"
        / "task.md"
    )
    criteria = json.loads(
        read(
            TILE_ROOT
            / "evals"
            / "synthetic-pr-uncertain-scope-manual-check-template-compliance"
            / "criteria.json"
        )
    )
    descriptions = "\n".join(
        f"{item['name']}\n{item['description']}" for item in criteria["checklist"]
    )

    assert "Result: Matches well enough" not in task
    assert "Things to check manually" not in task
    assert "manual-check" not in task
    assert "No comment needed" not in task
    assert "- [x] Feature" in task
    assert "Keeps the editor UI and save flow unchanged" in task
    assert "internal debug payload" in task
    assert "Result: Matches well enough" in descriptions
    assert "No comment needed" in descriptions
    assert "Things to check manually" in descriptions
    assert "not in the main contributor-facing comment" in descriptions
    assert "does not accuse the author of an incorrect selection" in descriptions


def test_synthetic_external_context_eval_covers_body_boundary_without_prompt_leak() -> None:
    task = read(
        TILE_ROOT
        / "evals"
        / "synthetic-pr-external-context-significant-template-compliance"
        / "task.md"
    )
    criteria = json.loads(
        read(
            TILE_ROOT
            / "evals"
            / "synthetic-pr-external-context-significant-template-compliance"
            / "criteria.json"
        )
    )
    descriptions = "\n".join(
        f"{item['name']}\n{item['description']}" for item in criteria["checklist"]
    )

    assert "Result: Significant deviation" not in task
    assert "Template compliance gaps" not in task
    assert "Genuinely missing information" not in task
    assert "linked issue and review thread" in task
    assert "root cause, risk analysis, human verification, and checklist status" in task
    assert "Evaluates the PR body itself as the compliance unit" in descriptions
    assert "external context must not receive template-compliance credit" in criteria["context"]
    assert "Distinguishes same-body information from external context" in descriptions
    assert "https://github.com/example/queuekeeper/blob/trunk/.github/PULL_REQUEST_TEMPLATE.md" in descriptions
    assert "Uses structured analysis separate from the comment" in descriptions


if __name__ == "__main__":
    test_synthetic_contradiction_eval_requires_author_clarification()
    test_rubric_treats_unreliable_required_answers_as_compliance_gaps()
    test_uncertain_inconsistencies_remain_manual_check_only()
    test_conditionally_removable_sections_require_body_local_condition()
    test_always_on_rules_cover_existing_body_template_triage()
    test_rubric_preserves_observed_template_audit_distinctions()
    test_triage_no_template_and_no_post_rules_are_explicit()
    test_propose_and_preflight_preserve_template_selection_and_disclosure_format()
    test_synthetic_checkbox_eval_covers_selected_vs_unchecked_semantics_without_prompt_leak()
    test_synthetic_manual_check_eval_covers_non_actionable_scope_signal()
    test_synthetic_external_context_eval_covers_body_boundary_without_prompt_leak()
