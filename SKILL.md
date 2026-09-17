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
   source artifacts under `material/` and one initial `Video Findings.md` at
   the output root. Use `--keyword-profile de`, `en`, a compatible JSON profile
   path, or `none` when useful. Profiles only improve routing; they never
   restrict the complete semantic review. The motion index creates no
   screenshots or clips and is a routing aid, not proof of a defect.
   These transcript artifacts are the reusable source from which reports can be
   regenerated later. The default `single` frame mode keeps the review compact;
   use `--frame-mode dense` only when the user explicitly asks for many samples
   or when a timing-dependent claim requires diagnosis.
4. Read [prompts/detect-findings.md](prompts/detect-findings.md), then use the AI
   to review **every cue in the complete
   `material/transcript-cues.json` semantically**.
   Capture every described bug or actionable finding, including claims that
   visual evidence cannot fully confirm, and mark their evidentiary status.
   Stay close to the speaker's wording. Never invent a product name, feature,
   user role, requirement, severity, root cause, or expected behavior when the
   recording does not establish it. Keyword matches are optional hints only;
   they are neither findings nor a coverage boundary. Detect findings in any
   transcript language. Use a report language explicitly requested in the
   current prompt; otherwise use the language of that prompt. Only when the
   prompt language is genuinely unclear may a known user preference and then
   the dominant transcript language act as fallbacks. Never let the transcript
   override the language of a clear current prompt.
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
6. Unless the prompt requests another name, layout, or artifact set, replace
   the preparation dossier with one detailed root-level `Video Findings.md`
   using
   [templates/report.md](templates/report.md) and
   [templates/finding.md](templates/finding.md). Write `material/findings.json`
   according to [templates/findings.schema.json](templates/findings.schema.json)
   and keep transcripts, machine-readable data, motion indexes, and images in
   `material/`. Link the full transcript from the dossier. Derived reports may
   be regenerated from the material folder and original recording without
   retranscribing the source.

Read [docs/setup-macos.md](docs/setup-macos.md) when installing on a new Mac and
[docs/input-formats.md](docs/input-formats.md) when input origin or transcript
alignment is unclear.

## Required distinctions

Keep three language concepts separate:

- **Transcript language:** the language spoken in the source recording.
- **Report language:** an explicit current instruction, otherwise the language
  of the current prompt; older preferences and transcript language are only
  fallbacks when the prompt is unclear.
- **Quote/UI language:** direct quotes and visible labels remain in their
  original language unless the user requests translation.

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

## Default dossier contract

Treat this as a default, not a restriction. Follow any output language, file
name, format, or folder structure requested in the current prompt. Otherwise,
the output root contains exactly one user-facing file:

- `Video Findings.md`: the complete, scrollable findings dossier;
- `material/`: every supporting artifact, including the complete transcript,
  cue JSON, structured findings, motion indexes, and exactly one representative
  image per final finding by default.

Avoid additional root-level files. A selected dynamic evidence package may use
one additional folder below `material/`, but keep navigation shallow unless the
user requests another structure.

In the dossier, begin every finding heading with its exact timestamp, followed
by a concise title. Give each finding one or two substantive paragraphs that
stay close to what was said and what is visibly supported. The prose must be
detailed enough to create later tickets or other artifacts, while naming any
uncertainty instead of filling missing product context.

Place the representative image directly inside its finding. Follow it with a
caption containing the image timestamp and a short, concrete description of
what is visible. A bare image path or unexplained screenshot is not useful
evidence. Link the exact point in the original video. Direct quotes are
optional in the dossier because the full transcript is linked; whenever quotes
or visible UI text are included, preserve their original language unless the
user asks for translation.

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
