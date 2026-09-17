---
name: video-findings
description: Use transcript cues to turn a local narrated MOV/MP4 video and optional VTT/SRT transcript into evidence-backed Markdown findings with timestamps and screenshots. Use when the visual state is necessary to understand or verify what is said, especially for product, QA, UX, requirements, support, or process review recordings; do not use for general meeting summaries.
---

# Video Findings

Create reviewable visual findings from a narrated recording. The included
profile specializes in UI reviews: treat the transcript as a search index for
the video, find likely problem moments in speech first, then inspect only small
visual windows around those moments.

Supported inputs include QuickTime Player or macOS screen recordings saved as
`.mov`, Teams recordings downloaded to the computer as `.mp4`, and ordinary
local MOV/MP4 files. A matching Teams `.vtt` or `.srt` is optional. The video
must be fully available as a local readable file; a cloud placeholder is not
enough.

## Workflow

1. Run `scripts/check-environment --video <path>` before reading the recording.
   On macOS, run `scripts/setup-macos` to show the read-only installation plan.
   Prefer an already installed MacParakeet model. Explain every missing package,
   the selected model and its reported size. Ensure one local transcription
   model is ready, but never download another when a compatible model already
   exists. Recommend the currently tested Parakeet TDT v3 on a compatible Mac;
   let the user choose another supported backend/model in the read-only plan.
   Ask before running `scripts/setup-macos --install --yes` with those same
   options.
2. Prefer a supplied `.vtt` or `.srt`, especially one downloaded with a Teams
   recording. If none exists, use `scripts/transcribe-local` or the end-to-end
   `scripts/analyze-recording`; both prefer ready local MacParakeet/Parakeet and
   fall back to ready local `whisper.cpp`. Do not upload media or transcript
   without explicit approval.
3. Run `scripts/analyze-recording --video ... --transcript ... --output ...` or
   `python3 src/video_findings.py prepare ...` to create deterministic
   `transcript-cues.json`, optional keyword leads, one initial screenshot per
   lead, and a preparation report. The default `single` frame mode keeps the
   review compact; use `--frame-mode dense` only when the user explicitly asks
   for many samples or when a timing-dependent claim requires diagnosis.
4. Read [prompts/detect-findings.md](prompts/detect-findings.md), then use the AI
   to review **every cue in the complete `transcript-cues.json` semantically**.
   Resolve vague descriptions from surrounding context. Keyword matches are
   optional hints only; they are neither findings nor a coverage boundary.
   Detect findings in any transcript language. Unless the user requested
   another language, write the findings in the dominant transcript language.
5. For each AI-selected finding, choose one timestamp that shows the most
   informative visible state and run
   `scripts/extract-frame VIDEO TIMESTAMP OUTPUT_JPG`. If the first image is
   ambiguous, inspect up to three temporary alternatives or the relevant video
   interval, then keep only the strongest representative image in the final
   report. Read [prompts/verify-evidence.md](prompts/verify-evidence.md). Use
   `scripts/extract-frames` for dense diagnosis only, not for the normal report.
   If visual evidence does not prove a claim, say so; never invent UI state
   between samples.
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
retain all supporting time ranges. Never promote a keyword match without AI
context review. Keep non-findings and missed visual-only issues visible in the
evaluation notes when testing the workflow.

## Output contract

Store the report as Markdown, machine-readable candidates/findings as JSON, and
exactly one representative image per final finding in an adjacent `assets/`
directory. Every finding must also reference the original video and give the
exact timestamp from which a reviewer can continue watching. Use relative
links for local output so the result works in GitHub and Obsidian. Additional
diagnostic frames may be generated temporarily, but include them in the final
report only when the user explicitly requests dense evidence.
