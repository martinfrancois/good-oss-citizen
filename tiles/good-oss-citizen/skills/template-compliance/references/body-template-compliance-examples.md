# Body/template compliance example checks

These examples are reusable expectation checks for the `template-compliance` rubric. They are intentionally written as body/template behavior cases, not as a separate executable evaluator: the helper scripts fetch data, and the agent applies the rubric.

Use these examples to sanity-check future rubric edits and review comments.

Concrete fixture files are available under `fixtures/synthetic-pr-template/`:

- Full synthetic template: `fixtures/synthetic-pr-template/templates/pr-template.md`
- Filled body files with each mutation already applied: `fixtures/synthetic-pr-template/bodies/*.md`
- Expected result buckets and body-file mapping: `fixtures/synthetic-pr-template/expected-results.json`
- Reproduction instructions: `fixtures/synthetic-pr-template/README.md`

## Synthetic PR-template cases

Baseline: start from `fixtures/synthetic-pr-template/bodies/baseline.md`, which matches `fixtures/synthetic-pr-template/templates/pr-template.md` well enough, then compare the named fixture body for each case.

### remove-unchecked-options

- Expected result: `Matches well enough`
- Mutation: remove unchecked checkbox options while keeping the selected choices clear.
- Reason: omitted unchecked options are harmless unless the template explicitly requires them to remain or the selected choice becomes unclear.
- Comment expectation: `No comment needed`.

### rename-selected-checkbox-bugfix-to-issue

- Expected result: `Slight deviation`
- Mutation: change selected `Bug fix` to selected `Issue`.
- Reason: selected checkbox labels must align with the current template. `Issue` is broader and less precise than `Bug fix`.
- Comment expectation: ask the author to align the selected change type with the template wording and include the template link.

### rename-selected-checkbox-security-hardening-to-security

- Expected result: `Slight deviation`
- Mutation: change selected `Security hardening` to selected `Security`.
- Reason: selected checkbox labels must preserve the template's meaning. `Security` is broader than `Security hardening`.
- Comment expectation: ask the author to align the selected change type with the template wording and include the template link.

### add-extra-section

- Expected result: `Matches well enough`
- Mutation: add an extra section not present in the template while leaving required template content intact.
- Reason: extra sections are not a compliance gap by themselves. The rubric checks whether the body satisfies the template, not whether it contains only template sections.
- Comment expectation: `No comment needed`.

### remove-one-required-section

- Expected result: `Slight deviation`
- Mutation: remove one required section, such as `Security Impact (required)`.
- Reason: one specific required section is missing, but the rest of the body can still mostly follow the template.
- Comment expectation: ask for the missing required section, and include the template link if the comment says to follow or align with the template.

### remove-several-required-sections

- Expected result: `Significant deviation`
- Mutation: remove several required sections, such as change type, scope, security impact, repro/verification, and human verification.
- Reason: several required sections are missing, so the author should follow the template rather than receive a long list of individual requests.
- Comment expectation: ask the author to update the body to follow the template and include the template link.

### introduce-breaking-change-contradiction

- Expected result: `Matches well enough` with a `Things to check manually` entry, or a compliance gap only if the contradiction makes a required section unreliable.
- Mutation: keep `Compatibility / Migration` filled as `Backward compatible? (Yes/No) Yes`, `Migration needed? (Yes/No) No`, but mention much earlier in `Summary` that replacing `messageBridge.rawCaption` with `messageBridge.safeCaption` is a breaking change for plugins importing the old helper.
- Reason: the body appears to fill the template, but the distant wording conflict is useful reviewer signal. Suspicious internal inconsistencies belong under manual checks unless directly supported enough to make a required section unclear, self-contradictory, or unreliable.
- Comment expectation: keep it out of the main suggested comment unless the reviewer confirms it is real and worth mentioning.

### remove-openclaw-prompt-instructions

- Expected result: `Matches well enough`
- Mutation: remove instruction-only prompt text from an OpenClaw-style PR body while keeping the actual fillable headings, labels, selected options, and answers intact. Safe-to-remove prompt text includes:
  - `Describe the problem and fix in 2–5 bullets:`
  - `If this PR fixes a plugin beta-release blocker, title it fix(<plugin-id>): beta blocker - <summary> and link the matching Beta blocker: <plugin-name> - <summary> issue labeled beta-blocker. Contributors cannot label PRs, so the title is the PR-side signal for maintainers and automation.`
  - ``For bug fixes or regressions, explain why this happened, not just what changed. Otherwise write `N/A`. If the cause is unclear, write `Unknown`.``
  - ``List user-visible changes (including defaults/config). If none, write `None`.``
- Reason: these lines are helper instructions for authors, not required filled answers. Removing helper text does not mean the template was abandoned.
- Comment expectation: `No comment needed`.

### keep-openclaw-prompt-instructions

- Expected result: `Matches well enough`
- Mutation: leave OpenClaw-style instruction-only prompt text in the filled PR body while also providing substantive answers under the relevant headings or labels.
- Reason: the rubric should not require authors to delete helper instructions. Kept prompt text is harmless when the requested answer is still clear.
- Comment expectation: `No comment needed`.

### remove-fillable-os-field-label

- Expected result: `Slight deviation`
- Mutation: remove an important fillable field label such as `- OS:` from a required environment/details section.
- Reason: unlike helper instructions, a fillable field label identifies required information. Removing it should be flagged when the required information is not clearly provided elsewhere in the same body.
- Comment expectation: ask for the missing field or equivalent required information, and include the template link if asking the author to align with the template.

## Synthetic Yes/No field cases

Baseline: the template contains the required field label `New permissions/capabilities? (Yes/No)`.

### yesno-field-answer-without-option-hint

- Expected result: `Matches well enough`
- Body text: `New permissions/capabilities? Yes`
- Reason: the answer preserves the field label's meaning and clearly selects one allowed value even though the `(Yes/No)` hint was removed.
- Comment expectation: `No comment needed`.

### yesno-field-answer-with-option-hint

- Expected result: `Matches well enough`
- Body text: `New permissions/capabilities? (Yes/No) Yes`
- Reason: the template's option hint remains and the author adds a clear allowed answer.
- Comment expectation: `No comment needed`.

### yesno-field-empty

- Expected result: `Slight deviation`
- Body text: `New permissions/capabilities? (Yes/No)`
- Reason: the field is present but unanswered.
- Comment expectation: ask the author to answer the required `New permissions/capabilities? (Yes/No)` field.

### yesno-field-placeholder-left-as-answer

- Expected result: `Slight deviation`
- Body text: `New permissions/capabilities? (Yes/No) Yes/No`
- Reason: repeating the placeholder/options is not a selected answer.
- Comment expectation: ask the author to choose `Yes` or `No`.

### yesno-field-invalid-answer

- Expected result: `Slight deviation`
- Body text: `New permissions/capabilities? (Yes/No) Test`
- Reason: `Test` is not one of the required `Yes` / `No` values.
- Comment expectation: ask the author to choose `Yes` or `No`.

## Pinned OpenClaw verification fixtures

These expectations were first checked against live `openclaw/openclaw` bodies and templates on 2026-04-26, then snapshotted so future reviews do not drift when OpenClaw changes its templates or issue/PR bodies.

Fixture directory: `fixtures/openclaw-a08b65a/`

Pinned template commit: `a08b65a90a454fbfe2ea4025f5bcdab08640d983`

Pinned template permalinks:

- PR template: <https://github.com/openclaw/openclaw/blob/a08b65a90a454fbfe2ea4025f5bcdab08640d983/.github/pull_request_template.md>
- Bug report issue form: <https://github.com/openclaw/openclaw/blob/a08b65a90a454fbfe2ea4025f5bcdab08640d983/.github/ISSUE_TEMPLATE/bug_report.yml>
- Feature request issue form: <https://github.com/openclaw/openclaw/blob/a08b65a90a454fbfe2ea4025f5bcdab08640d983/.github/ISSUE_TEMPLATE/feature_request.yml>

Expected results:

- `openclaw/openclaw#59898`: `Matches well enough` using `fixtures/openclaw-a08b65a/templates/pull_request_template.md` and `fixtures/openclaw-a08b65a/bodies/pr-59898.md`
- `openclaw/openclaw#66877`: `Matches well enough` using `fixtures/openclaw-a08b65a/templates/pull_request_template.md` and `fixtures/openclaw-a08b65a/bodies/pr-66877.md`
- `openclaw/openclaw#72316`: `Significant deviation` using `fixtures/openclaw-a08b65a/templates/feature_request.yml` and `fixtures/openclaw-a08b65a/bodies/issue-72316.md`
- `openclaw/openclaw#72345`: `Significant deviation` using `fixtures/openclaw-a08b65a/templates/bug_report.yml` and `fixtures/openclaw-a08b65a/bodies/issue-72345.md`
- `openclaw/openclaw#66663`: `Significant deviation` using `fixtures/openclaw-a08b65a/templates/pull_request_template.md` and `fixtures/openclaw-a08b65a/bodies/pr-66663.md`

How to reproduce:

1. Read `body-template-compliance-rubric.md`.
2. For each case in `fixtures/openclaw-a08b65a/expected-results.json`, compare the listed body file against the listed template file.
3. Apply the body-local evidence rule: only credit information present in the same body file.
4. Confirm the result bucket matches `expectedResult`.

The `fixtures/openclaw-a08b65a/README.md` file also includes live helper commands for comparing these snapshots to current GitHub data. If live data differs from the snapshots, use the snapshot files as the regression expectations and treat the live data as a new candidate example.
