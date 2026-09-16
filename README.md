# Review to Issues

Turn recorded UI reviews into evidence-backed issue drafts.

A 30-minute UI review may contain five useful findings hidden inside hundreds
of conversational sentences. This toolkit uses the transcript to locate likely
problem moments, inspects only those video windows, and creates reviewable
Markdown findings with timestamps and screenshots.

It is not another meeting summarizer, and it does not pretend to create final
Jira tickets. It separates observed evidence, reviewer expectations, model
interpretation, and the human decision.

## What is included

- MP4/MOV input and optional VTT/SRT input
- local FFmpeg audio and frame extraction
- deterministic candidate windows in JSON
- beginning/middle/end frame candidates for each window
- an agent skill and prompts for evidence-aware interpretation
- Markdown report and finding templates
- a synthetic demo and repeatable tests

No Jira integration, cloud backend, Teams API, user accounts, or automatic
ticket creation are included.

## Two-minute demo

Requirements: Python 3.10+ and FFmpeg.

```bash
make test
make demo
open output/demo/report.md
```

`make demo` generates a short synthetic MP4 locally, reads the supplied VTT,
detects transcript-led candidate windows, extracts three frames per candidate,
and writes:

```text
output/demo/
├── assets/
├── candidates.json
└── report.md
```

The sample intentionally contains a clear bug, diffuse frustration, a reviewer
misconception, a visual-only issue, a repeated issue, and a harmless remark.
See [docs/evaluation.md](docs/evaluation.md) for the expected behavior.

## Use your own recording

Put files in `input/` and run:

```bash
python3 src/review_to_issues.py prepare \
  --video input/review.mp4 \
  --transcript input/review.vtt \
  --output output/my-review
```

If no transcript exists yet:

```bash
scripts/extract-audio input/review.mp4 input/review.wav
```

Transcribe the WAV with a local tool, then run `prepare`. The core deliberately
does not lock the project to one transcription model. Agents can follow
`SKILL.md` to interpret and verify the generated candidates.

## Architecture

```text
recording + transcript
        │
        ▼
deterministic cue parsing and candidate windows
        │
        ▼
local FFmpeg frame extraction
        │
        ▼
agent interpretation of transcript + selected frames
        │
        ▼
Markdown findings + JSON + human review
```

The transcript narrows the search space. The video is sampled only around
candidate moments. That makes the workflow faster, cheaper, more inspectable,
and more data-minimizing than sending every frame to a multimodal model.

## Privacy

The included scripts run locally. The whole workflow is only fully local if
transcription and interpretation are local too. Sending transcripts or frames
to a cloud model means those artifacts leave the machine. See
[docs/privacy.md](docs/privacy.md).

## Project status

This is a portfolio-ready V0 and a testable V1 foundation. The deterministic
pipeline works; nuanced finding detection and visual verification remain an
agent task so their uncertainty stays visible.

MIT licensed.

