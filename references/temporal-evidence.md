# Temporal evidence

Read this reference when a finding depends on motion, timing, audio, an
interaction sequence, or a short-lived visual state. The normal first pass
still uses one representative image per finding.

## First-pass routing

Use `motion-1s.tsv` as a compact index, not as proof of a defect. Compare its
peaks with the complete transcript and the original video. Read detailed
`motion.tsv` values only around relevant intervals.

Classify the internal evidence need as:

| Mode | Use for |
|---|---|
| `static` | Persistent layout, copy, visible state, or small text |
| `interaction` | Click sequences, dragging, focus changes, menus, and transitions |
| `flicker` | Alternating frames or sub-second intermediate states |
| `latency` | Delay between an action, first response, and stable state |
| `audio-visual` | Meaning depends on hearing the narration while watching the interval |
| `slow4x` | A short state needs slower playback for human or model inspection |

The public report may group every non-static mode under `Dynamic`. Store the
more precise mode in `findings.json` when it is known.

## Extraction rules

- Preserve the original recording.
- Never turn a low-frame-rate proxy into apparent 60 fps evidence.
- Re-extract selected dynamic intervals from the original video.
- Cap interaction and latency clips at 30 fps.
- Cap flicker clips at 60 fps, but never above the source frame rate.
- Slow playback by changing timestamps, not by claiming interpolated frames as
  new evidence.
- Crop the relevant region before scaling when small UI details matter.
- Keep audio for audio-visual evidence; otherwise follow the user's choice.
- A QuickTime click highlight is recording metadata, not an application
  control, placeholder, or visual defect.

Run an adaptive package only after the user selects a finding:

```bash
scripts/extract-evidence \
  --video recording.mov \
  --start 00:01:08.720 \
  --end 00:01:18.560 \
  --mode interaction \
  --output output/evidence/finding-003
```

Add `--no-audio` for a silent attachment or `--crop X:Y:W:H` for a relevant
screen region. The package includes the clip or representative frame, contact
sheets, interval motion data, and `evidence.json`.

## Measurements

Motion peaks help locate candidate boundaries but do not identify semantic
events on their own. Inspect the source-timed evidence, select the visible
action, first response, and optional stable state, then calculate the interval:

```bash
scripts/measure-interval \
  --action 12.400 \
  --response 13.050 \
  --stable 13.600 \
  --output output/evidence/finding-003/measurement.json
```

Report the measurement basis and retain uncertainty when event boundaries are
ambiguous. A few still frames cannot prove latency or flicker.

## Optional external video analysis

Use an external native-video model only for a selected short interval when
local evidence remains ambiguous. Ask for explicit approval before uploading
the clip. Do not hard-code a provider or model in the skill; choose a current
compatible service at the time of use and keep the local transcript timestamps
and source evidence as the reference.
