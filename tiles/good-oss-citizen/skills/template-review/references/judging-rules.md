# Template review judging rules

Use this rubric when producing the output for `template-review`.

## Result thresholds

- **Matches well enough**
  - The correct template was found or the default selection is reasonable.
  - No major required section is missing.
  - Any issues are minor wording or placement cleanups.
- **Slight deviation**
  - The body mostly follows the template but misses one or two required items, leaves a section weakly answered, or uses a mismatched checkbox label.
  - A maintainer could probably fix it with a short follow-up comment.
- **Significant deviation**
  - Multiple required sections are missing, the wrong template appears to have been used, or the body is so compressed that maintainers would have to reconstruct the request.

## Bucket rules

- **Template compliance gaps**
  - Definite problems visible from the template and the same linked body.
  - Examples: missing reproduction steps, missing testing section, wrong checkbox selected, omitted required heading.
- **Information already present elsewhere in the same linked body**
  - The answer exists, but not under the expected heading or format.
  - Mention it so the reviewer can avoid asking for it again.
- **Genuinely missing information**
  - Information the template asks for that does not appear anywhere in the same body.
- **Things to check manually**
  - Facts that cannot be verified from the body alone.
  - Examples: whether tests actually ran, whether a CLA was signed, whether a checked box is truthful, whether linked screenshots still reproduce the problem.

## Checkbox alignment rules

- A checked box only counts if the label matches the surrounding narrative.
- If the author checked multiple mutually exclusive boxes, flag the conflict as a compliance gap.
- If the label is correct but the truth depends on evidence outside the body, keep it under manual checks.

## Suggested comment rules

- Ask only for net-new information or net-new alignment fixes.
- If you mention template alignment, include a direct GitHub blob URL in this form:

```text
https://github.com/OWNER/REPO/blob/DEFAULT_BRANCH/PATH/TO/TEMPLATE
```

- Prefer a comment that acknowledges already-provided context before asking for missing pieces.
- Keep optional manual snippets narrowly targeted. They should help the author patch one section, not rewrite the whole body unless the result is `Significant deviation`.
