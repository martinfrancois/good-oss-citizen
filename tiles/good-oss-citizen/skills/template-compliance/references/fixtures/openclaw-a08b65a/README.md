# OpenClaw pinned body/template fixtures

These fixtures make the live OpenClaw examples in `../../body-template-compliance-examples.md` reproducible even if `openclaw/openclaw` changes its templates later.

- Source repository: `openclaw/openclaw`
- Template commit: `a08b65a90a454fbfe2ea4025f5bcdab08640d983`
- Snapshot date: 2026-04-26
- Expected results file: `expected-results.json`

## Pinned template permalinks

- PR template: <https://github.com/openclaw/openclaw/blob/a08b65a90a454fbfe2ea4025f5bcdab08640d983/.github/pull_request_template.md>
- Bug report issue form: <https://github.com/openclaw/openclaw/blob/a08b65a90a454fbfe2ea4025f5bcdab08640d983/.github/ISSUE_TEMPLATE/bug_report.yml>
- Feature request issue form: <https://github.com/openclaw/openclaw/blob/a08b65a90a454fbfe2ea4025f5bcdab08640d983/.github/ISSUE_TEMPLATE/feature_request.yml>

Local copies are stored under `templates/` so reviews do not depend on live GitHub content.

## Fixture bodies

The files under `bodies/` are snapshots of the issue or PR body text used for the manual verification cases:

| Case | Live URL | Template file | Body file | Expected result |
| --- | --- | --- | --- | --- |
| `openclaw-pr-59898` | <https://github.com/openclaw/openclaw/pull/59898> | `templates/pull_request_template.md` | `bodies/pr-59898.md` | `Matches well enough` |
| `openclaw-pr-66877` | <https://github.com/openclaw/openclaw/pull/66877> | `templates/pull_request_template.md` | `bodies/pr-66877.md` | `Matches well enough` |
| `openclaw-issue-72316` | <https://github.com/openclaw/openclaw/issues/72316> | `templates/feature_request.yml` | `bodies/issue-72316.md` | `Significant deviation` |
| `openclaw-issue-72345` | <https://github.com/openclaw/openclaw/issues/72345> | `templates/bug_report.yml` | `bodies/issue-72345.md` | `Significant deviation` |
| `openclaw-pr-66663` | <https://github.com/openclaw/openclaw/pull/66663> | `templates/pull_request_template.md` | `bodies/pr-66663.md` | `Significant deviation` |

## How to execute the check

There is no deterministic semantic evaluator for these examples. To reproduce the manual verification:

1. Read `../../body-template-compliance-rubric.md`.
2. For each case in `expected-results.json`, compare the listed `bodyFile` against the listed `templateFile`.
3. Apply the rubric's body-local evidence rule: only credit information present in that body file.
4. Confirm the result bucket matches `expectedResult`.

A reviewer can also compare the pinned fixtures with current live GitHub data when investigating drift:

```bash
# From the repository root
bash tiles/good-oss-citizen/skills/recon/scripts/bash/github.sh templates-pr openclaw/openclaw
bash tiles/good-oss-citizen/skills/recon/scripts/bash/github.sh templates-issue openclaw/openclaw
bash tiles/good-oss-citizen/skills/recon/scripts/bash/github.sh body openclaw/openclaw 59898
```

If live data differs from these files, use the fixture files for regression expectations and the live data only as a new candidate example.
