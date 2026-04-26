# Synthetic PR-template fixtures

These files turn the synthetic behavior cases from `../../body-template-compliance-examples.md` into concrete inputs.

- Full template: `templates/pr-template.md`
- Filled body files: `bodies/*.md`
- Expected result buckets: `expected-results.json`

## How to execute the check

There is no deterministic semantic evaluator for these examples. To reproduce the expectations manually:

1. Read `../../body-template-compliance-rubric.md`.
2. Compare each `bodyFile` in `expected-results.json` against `templates/pr-template.md`.
3. Apply the body-local evidence rule: only credit information present in the same body file.
4. Confirm the result bucket matches `expectedResult`.

The body files already contain the mutation described by their file name, so reviewers do not need to mentally apply changes to a baseline body.
