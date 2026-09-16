---
name: review-to-issues
description: Turn a recorded UI review and optional VTT/SRT transcript into evidence-backed Markdown findings with timestamps and screenshots. Use for product, QA, UX, or requirements review recordings; do not use for general meeting summaries.
---

# Review to Issues

Create reviewable issue drafts from a UI review recording. Treat the transcript
as a search index for the video: find likely problem moments in speech first,
then inspect only small visual windows around those moments.

## Workflow

1. Run `scripts/check-environment` and report missing prerequisites.
2. Prefer a supplied `.vtt` or `.srt`. If none exists, extract audio with
   `scripts/extract-audio` and use an available local transcription tool. Do not
   upload media or transcript without explicit approval.
3. Run `python3 src/review_to_issues.py prepare ...` to create deterministic
   candidate windows, frames, `candidates.json`, and a draft report.
4. Read [prompts/detect-findings.md](prompts/detect-findings.md) before judging
   transcript candidates. Treat heuristic candidates as leads, not findings.
5. Inspect candidate frames and read
   [prompts/verify-evidence.md](prompts/verify-evidence.md). If frames do not
   prove a claim, say so; never invent UI state between sampled frames.
6. Write the final report using [templates/report.md](templates/report.md) and
   [templates/finding.md](templates/finding.md).

## Required distinctions

- **Observation:** directly supported by transcript or visible evidence.
- **Reviewer expectation:** what the reviewer says should happen.
- **Interpretation:** a tentative classification or explanation.
- **Human decision:** remains open unless the user explicitly decides it.

Use `Needs review` by default. Deduplicate repeated discussion of one issue but
retain all supporting time ranges. Keep non-findings and missed visual-only
issues visible in the evaluation notes when testing the workflow.

## Output contract

Store the report as Markdown, machine-readable candidates/findings as JSON, and
images in an adjacent `assets/` directory. Use relative links so the result
works in GitHub and Obsidian.

