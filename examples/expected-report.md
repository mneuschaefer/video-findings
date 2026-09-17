# Expected demo outcome

The deterministic keyword pass should produce two optional candidate groups:

1. The two “Continue / no response” passages should be merged into one finding
   with two source ranges.
2. The logo expectation should remain a separate, lower-confidence candidate.

Diffuse frustration should not become a finding or other topic without a
concrete behavior or useful point. The visual-only spacing issue demonstrates
the known recall limit of a transcript-led workflow. The concrete preference
to retain the blue color should not become a finding, but should appear in the
final timestamped `Other topics mentioned` index.

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

Because this example contains a useful non-finding preference, the final
dossier should include a brief pointer near the beginning and place this index
after every finding:

```markdown
## Other topics mentioned

This is a short index, not a complete meeting summary.

### 00:23.000 — Retain the blue color

The reviewer likes the current blue color and would keep it.

Ask for any of these topics to be summarized separately if useful.
```
