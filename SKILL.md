---
name: video-findings
description: Turn a local narrated screen recording into timestamped findings with relevant screenshots and a reusable transcript. Use for spoken reviews, testing sessions and think-aloud walkthroughs.
license: MIT
---

# Video Findings

Turn the reviewer's spoken observations into a concise report with relevant
pictures. Use the transcript to locate moments; do not audit the whole video.

## Skill location

Treat the directory containing this `SKILL.md` as the skill root. Resolve all
bundled scripts, references and templates from that directory; never assume the
current working directory is the skill directory. Keep recordings and generated
output in the user's chosen project or output location, not inside a packaged or
shared skill installation. The complete workflow requires a local coding agent
on macOS with local file and image access, Python 3.10+, FFmpeg/FFprobe, and
either a timestamped transcript or a configured local transcriber.

## Local preferences

When the user asks to install or prepare this project, create
`.video-findings/preferences.md` from
`templates/local-preferences.example.md` if it does not exist. This is a local,
Git-ignored setup file; tell the user where it was created, but do not require
them to edit it. Do not overwrite an existing file.

When a user states a recurring project preference, offer once to save it there.
If they explicitly say to remember or save the preference, that is sufficient
authorization. Never store passwords, API keys or other secrets in this file.

## Analysis model

When the caller can choose a model or subagent for transcript and screenshot
analysis, prefer the fastest available option that can:

- use local file and image-viewing tools;
- read the complete transcript within its context window;
- merge repeated observations and produce the requested report language;
- follow the transcript-only factual boundary without adding visible but
  unspoken context.

Static image understanding is sufficient for the normal workflow; native video
analysis and a large reasoning model are not required. Use the lowest reasoning
level that remains source-faithful. One analysis agent should complete the
ordinary report; do not create further subagents unless the user requests them.

## Normal run

If `.video-findings/preferences.md` exists, read it once before starting. It may
define recurring local choices such as report language, filename, structure or
downstream format. The current prompt overrides local preferences. Do not edit
tracked repository files to save a machine- or user-specific choice. Apart from
creating the template-backed file during initial setup, change saved preferences
only when the user asks or confirms the offered change.

Run the prepared local workflow once:

```bash
skill_root="/absolute/path/to/video-findings"
"$skill_root/scripts/analyze-recording" --video "/path/recording.mov" --output "/path/to/output/review" --keyword-profile none --no-motion-scan
```

Add `--transcript "/path/transcript.vtt"` when a matching VTT/SRT is supplied.
The command checks dependencies, uses the saved local transcriber and preserves
the complete transcript under `material/`. On success, do not run another
environment check, inspect scripts or search for other models.

Read only `material/transcript-cues.json` once; do not also read the Markdown
transcript. Group concrete observations into findings, merging repeats. Select
timestamps around those observations and extract frames with:

```bash
"$skill_root/scripts/extract-frame" "/path/recording.mov" 25.5 "/path/to/output/review/material/finding-001.jpg"
```

Actually view the extracted images. Batch preparation, reading, extraction and
viewing where practical. Use this evidence rule:

- one persistent or static state: one representative image;
- two separate stable states whose comparison explains the finding: at most two
  images, such as a clear before/after pair;
- behavior that depends on motion or timing: one orientation image plus the
  optional clip offer below, never a still-image sequence as substitute proof.

Write `Video Findings.md` directly. Make each finding detailed enough that a
person can turn it into a ticket without rewatching the recording. Include,
when explicitly stated in the transcript:

- its source timestamp and a clear title;
- the action or situation that led to the issue;
- the observed behavior and practical effect;
- the reviewer's expectation and whether the issue repeated;
- the useful image or images, captioned with their timestamps.

Put the real source-video path once in the header and link the complete
`material/transcript.md`. The transcript defines the factual scope of the
finding. Use screenshots to attach evidence, not to add visible but unspoken
details, new product context or additional findings. Image captions should stay
neutral and name only the finding, timestamp and relevant control or area
already mentioned in the transcript. Treat spoken
observations as the reviewer's report rather than independently proven defects.
Do not invent steps, impact, expectations, visible behavior, causes,
requirements, environment, ownership, acceptance criteria or severity.
Do not infer the reviewer's gender. Do not add sections listing unknown causes,
responsibilities or other uncertainties unless the reviewer raised them.
For clearly timing-dependent issues such as flicker, disappearing states,
dragging behavior or repeated transitions, keep one orientation image in the
first report and record the relevant interval. Explain briefly that one frame
cannot show the full behavior, then offer to extract that interval as a short
clip with or without audio. Do not create the clip unless the user asks for it.

For a short recording with a few straightforward issues, one or two compact
paragraphs per finding are enough; completeness matters more than brevity.
Do not create a second planning document, classification pass, audit, progress
artifact or structured findings file. Check timestamps and image paths while
writing, then deliver. Do not inventory the repository before the run or reread
the finished report merely to confirm what a successful write already showed.

Use the language requested in the current prompt; otherwise use that prompt's
language. Preserve transcript quotes and visible UI labels in their source
language. Mention uncertainty only when it materially changes the finding.

The default output is the evidence-backed Markdown report above. A format
requested in the current prompt takes precedence. For a recurring personal or
machine-specific format, use `.video-findings/preferences.md`. Repository
maintainers may edit these tracked output instructions to change the published
default. Alternatively, finish the source report first and pass it to a
separate ticket or user-story skill. A downstream format must preserve the
report's source boundaries and evidence.

## Setup failures

Only if preparation fails, read [macOS setup](docs/setup-macos.md). Reuse the
saved adapter in `models/transcriber-path` or
`VIDEO_FINDINGS_TRANSCRIBER_COMMAND`; fix that concrete failure instead of
silently switching backends. Ordinary runs must never download model weights.
Before any installation or first model download, show what would be installed,
its source, destination and expected size, then obtain approval or offer manual
instructions. Do not download a different model format merely because a runtime
for an existing model is missing.

## Optional outputs

Only when requested:

- For machine-readable findings, use
  [the schema](templates/findings.schema.json).
- For ambiguous visual claims, use
  [evidence verification](prompts/verify-evidence.md).
- For selected clips or latency checks, use
  [temporal evidence](references/temporal-evidence.md).

Keep media local and obtain approval before external uploads or ticket creation.
