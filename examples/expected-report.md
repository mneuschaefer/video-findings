# Expected demo outcome

The deterministic keyword pass should produce two optional candidate groups:

1. The two “Continue / no response” passages should be merged into one finding
   with two source ranges.
2. The logo expectation should remain a separate, lower-confidence candidate.

Diffuse frustration should not become a finding without a concrete behavior.
The visual-only spacing issue demonstrates the known recall limit of a
transcript-led workflow. The harmless color remark should be excluded.

The generated report is only a preparation artifact. The agent must also review
the complete `material/transcript-cues.json`, including wording not caught by keyword
matching, inspect the selected frames, and write the final findings in the
transcript language unless another output language was requested.

The completed first pass preserves the full transcript as source VTT, readable
Markdown, and cue JSON under `material/`. It produces one detailed root-level
`Video Findings.md`, reusable `material/findings.json`, and one captioned
representative image per finding. Findings that depend
on timing or motion are marked `dynamic`; clips are offered and generated only
after the user selects a finding.
