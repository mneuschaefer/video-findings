---
name: video-findings
description: Turn a local narrated MOV/MP4 video and optional VTT/SRT transcript into a complete timestamped transcript, evidence-backed findings, and reusable Markdown/JSON artifacts. Use whenever spoken content and the matching visual state should be preserved, reviewed, or transformed into structured results.
---

# Video Findings

Create reusable source artifacts and reviewable visual findings from a narrated
recording. Treat the complete transcript as an index for the video, find
relevant moments in speech, and inspect the matching visual windows. The skill
can be used for UI reviews, demonstrations, research sessions, support cases,
process reviews, recorded discussions, or other recordings where speech and
visual context belong together.

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
   `transcript.md`, `transcript-cues.json`, an archived source VTT/SRT, optional
   keyword leads, a compact numeric `motion-1s.tsv`, one initial screenshot per
   lead, and a preparation report. The motion index creates no screenshots or
   clips and is a routing aid, not proof of a defect.
   These transcript artifacts are the reusable source from which reports can be
   regenerated later. The default `single` frame mode keeps the review compact;
   use `--frame-mode dense` only when the user explicitly asks for many samples
   or when a timing-dependent claim requires diagnosis.
4. Read [prompts/detect-findings.md](prompts/detect-findings.md), then use the AI
   to review **every cue in the complete `transcript-cues.json` semantically**.
   Capture every described bug or actionable finding, including claims that
   visual evidence cannot fully confirm, and mark their evidentiary status.
   Stay close to the speaker's wording. Never invent a product name, feature,
   user role, requirement, severity, root cause, or expected behavior when the
   recording does not establish it. Keyword matches are optional hints only;
   they are neither findings nor a coverage boundary. Detect findings in any
   transcript language. Unless the user requested another language, write the
   findings in the dominant transcript language.
5. For each AI-selected finding, choose one timestamp that shows the most
   informative visible state and run
   `scripts/extract-frame VIDEO TIMESTAMP OUTPUT_JPG`. If the first image is
   ambiguous, inspect up to three temporary alternatives or the relevant video
   interval, then keep only the strongest representative image in the final
   report. Read [prompts/verify-evidence.md](prompts/verify-evidence.md). Use
   `scripts/extract-frames` for dense diagnosis only, not for the normal report.
   If visual evidence does not prove a claim, say so; never invent UI state
   between samples. Mark timing-dependent findings as `dynamic`, record the
   most appropriate internal mode, and offer a
   short follow-up clip instead of creating it automatically. When the user
   selects a finding, read
   [references/temporal-evidence.md](references/temporal-evidence.md) and run
   `scripts/extract-evidence` with the appropriate mode. Preserve audio by
   default or add `--no-audio` when requested. Natural requests such as "Give
   me the clip for finding 3 and put it into my ticket format" are sufficient
   selection. Use `scripts/measure-interval` after inspecting source-timed
   evidence when latency or stabilization must be quantified.
6. Write a detailed final `report.md` using
   [templates/report.md](templates/report.md) and
   [templates/finding.md](templates/finding.md). Also write `findings.json`
   according to [templates/findings.schema.json](templates/findings.schema.json)
   so other tools can reuse the results. Link the full `transcript.md` from the
   report. Derived reports may be regenerated from `transcript-cues.json` and
   the original recording without retranscribing the source.

Read [docs/setup-macos.md](docs/setup-macos.md) when installing on a new Mac and
[docs/input-formats.md](docs/input-formats.md) when input origin or transcript
alignment is unclear.

## Required distinctions

- **Observation:** directly supported by transcript or visible evidence.
- **Reviewer expectation:** what the reviewer says should happen.
- **Interpretation:** a tentative classification or explanation.
- **Human decision:** remains open unless the user explicitly decides it.
- **Unknown context:** product, feature, requirement, cause, or intent that the
  recording does not establish. Leave it unknown instead of completing it from
  plausibility.

Use `Needs review` by default. Deduplicate repeated discussion of one issue but
retain all supporting time ranges. Never promote a keyword match without AI
context review. Keep non-findings and missed visual-only issues visible in the
evaluation notes when testing the workflow.

## Output contract

The standard output directory contains:

- `transcript-source.vtt` or `transcript-source.srt`: preserved timestamped
  source transcript;
- `transcript.md`: complete, readable transcript with every cue and timestamp;
- `transcript-cues.json`: complete machine-readable transcript source;
- `motion-1s.tsv`: compact whole-video routing index without extra images;
- `motion.tsv` and `motion-summary.json`: detailed numeric motion data;
- `candidates.json`: optional deterministic leads;
- `report.md`: detailed human-readable findings report;
- `findings.json`: reusable structured findings;
- `assets/`: exactly one representative image per final finding by default.

Every finding references the original video, gives the exact timestamp from
which a reviewer can continue watching, and includes the smallest relevant
transcript evidence. Use relative links so the result works in GitHub and
Obsidian. Additional diagnostic frames may be generated temporarily, but
include them in the final report only when the user explicitly requests dense
evidence.

The first pass is a sparse "where to find what" overview. It does not create
clips automatically. Mark findings whose meaning depends on timing or motion as
`dynamic`, and offer per-finding extraction with or without audio. After a user
selects findings, create only those clips and reformat the selected findings for
the requested ticket, issue tracker, document, or other destination. See
[docs/output-artifacts.md](docs/output-artifacts.md) for the artifact contract
and clip example.

## Recording responsibility

Assume the user has handled any notice or permission required for recording
participants. When a meeting or group session is recorded, the recommended
practice is to tell participants that recording is taking place. This is a
usage note, not a workflow blocker or a reason to stop analysis. Uploading any
recording or derived artifact to an external service still requires explicit
approval.
