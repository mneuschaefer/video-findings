---
name: review-to-issues
description: Turn a local QuickTime/macOS screen recording, downloaded Teams recording, or other MOV/MP4 UI review and optional VTT/SRT transcript into evidence-backed Markdown findings with timestamps and screenshots. Use for product, QA, UX, or requirements review recordings; do not use for general meeting summaries.
---

# Review to Issues

Create reviewable issue drafts from a UI review recording. Treat the transcript
as a search index for the video: find likely problem moments in speech first,
then inspect only small visual windows around those moments.

Supported inputs include QuickTime Player or macOS screen recordings saved as
`.mov`, Teams recordings downloaded to the computer as `.mp4`, and ordinary
local MOV/MP4 files. A matching Teams `.vtt` or `.srt` is optional. The video
must be fully available as a local readable file; a cloud placeholder is not
enough.

## Workflow

1. Run `scripts/check-environment --video <path>` before reading the recording.
   On macOS, if dependencies are missing, ask before running
   `scripts/setup-macos --install`. Installation changes the machine and the
   Whisper model download uses the network.
2. Prefer a supplied `.vtt` or `.srt`, especially one downloaded with a Teams
   recording. If none exists, use `scripts/transcribe-local` or the end-to-end
   `scripts/analyze-recording`; both use local `whisper.cpp`. Do not upload media
   or transcript without explicit approval.
3. Run `scripts/analyze-recording --video ... --transcript ... --output ...` or
   `python3 src/review_to_issues.py prepare ...` to create deterministic
   candidate windows, frames, `candidates.json`, and a draft report.
4. Read [prompts/detect-findings.md](prompts/detect-findings.md) before judging
   transcript candidates. Treat heuristic candidates as leads, not findings.
5. Inspect candidate frames and read
   [prompts/verify-evidence.md](prompts/verify-evidence.md). If frames do not
   prove a claim, say so; never invent UI state between sampled frames.
6. Write the final report using [templates/report.md](templates/report.md) and
   [templates/finding.md](templates/finding.md).

Read [docs/setup-macos.md](docs/setup-macos.md) when installing on a new Mac and
[docs/input-formats.md](docs/input-formats.md) when input origin or transcript
alignment is unclear.

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
