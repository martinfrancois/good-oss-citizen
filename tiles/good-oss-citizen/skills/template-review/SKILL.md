---
name: template-review
description: Reviews an already-open GitHub issue or pull request against the repository's detected GitHub template and drafts a maintainer-friendly follow-up. Use when the user asks "does this issue/PR follow the template?", "review this open PR body", "check template adherence", or wants a suggested comment for an existing GitHub issue or PR. GitHub only for now.
---

# Template Review

GitHub only. Do not use this skill for GitLab, local-only drafts, or offline markdown files.

Before scoring, read `references/judging-rules.md` in this skill directory.

Helper script path: `bash .tessl/tiles/tessl-labs/good-oss-citizen/skills/recon/scripts/bash/github.sh`

## Step 1: Detect the relevant template

- For issues:
```bash
bash .tessl/tiles/tessl-labs/good-oss-citizen/skills/recon/scripts/bash/github.sh issue-templates OWNER/REPO [intent]
```
- For pull requests:
```bash
bash .tessl/tiles/tessl-labs/good-oss-citizen/skills/recon/scripts/bash/github.sh pr-templates OWNER/REPO [intent]
```

Use the selected template from the helper output. If multiple templates fit and the selection is genuinely ambiguous, say so explicitly.

## Step 2: Read the linked body

```bash
bash .tessl/tiles/tessl-labs/good-oss-citizen/skills/recon/scripts/bash/github.sh linked-body OWNER/REPO NUMBER
```

Apply the **body-only credit rule**:
- Only credit information that appears in the same linked issue or PR body.
- Do **not** count issue comments, review comments, commit messages, code diffs, linked issues, or discussion elsewhere as satisfying a template field.
- If the same body contains the answer under a different heading or in freeform prose, credit it as already present elsewhere in the same linked body and do not ask for it again.

## Step 3: Compare body vs template

- Separate **real template compliance gaps** from **things to check manually**.
- A missing required section, missing required detail, wrong template choice, or mismatched checkbox label is a compliance gap.
- A checkbox that may be inaccurate but cannot be proven from the body alone belongs under manual checks, not missing information.
- Tighten checkbox review: the checked label must align with the body text around it. If the body says docs-only change but the author checked a bug-fix box, that is a gap.

## Step 4: Produce exactly this structure

```md
## Template Review: <owner/repo>#<number>

- Result: Matches well enough | Slight deviation | Significant deviation
- Template found: <selected path or none detected>
- Template compliance gaps:
- Information already present elsewhere in the same linked body:
- Genuinely missing information:
- Things to check manually:
- Suggested comment:
- Optional manual snippets:
```

## Step 5: Draft the suggested comment carefully

- Follow the **net-new-only comment rule**: ask only for information or fixes that are genuinely missing or misaligned.
- Do not re-ask for details already present elsewhere in the same linked body.
- Keep the comment short, specific, and respectful of maintainer time.
- If you ask the author to follow or align with the template, include a direct link to the selected template file on the default branch.
- Do not post the comment. Draft only for human review.

## Step 6: If no template is found

Say that no GitHub template was detected on the default branch. Do not invent a template. Limit the review to obvious completeness problems in the linked body.
