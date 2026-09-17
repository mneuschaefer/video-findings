# Output artifacts

The first pass creates a sparse overview and preserves enough source material
to regenerate later reports without retranscribing the recording.

`findings.json` keeps `transcript_language` and `report_language` separate.
The report language follows the current user instruction, known preference,
current request language, and only then the transcript language. Direct quotes
and visible UI labels preserve their original language unless translation is
requested.

| Artifact | Purpose |
|---|---|
| `transcript-source.vtt` or `.srt` | Preserved timestamped source transcript |
| `transcript.md` | Complete readable transcript with timestamps and speakers when available |
| `transcript-cues.json` | Complete machine-readable transcript source |
| `candidates.json` | Optional deterministic leads for AI review |
| `motion-1s.tsv` | Compact numeric whole-video motion index for routing |
| `motion.tsv` | Detailed motion values for selected inspection windows |
| `report.md` | Detailed human-readable report, close to the spoken claims |
| `findings.json` | Structured findings for regeneration and conversion |
| `assets/` | One representative evidence image per final finding by default |

The report lists every described bug or actionable finding and distinguishes
reported behavior from visible verification. Unknown product names,
requirements, roles, severity, causes, or intended behavior stay unknown.

Each finding has an `evidence_need` value:

- `static`: one representative image normally provides enough orientation;
- `dynamic`: the claim depends on motion, timing, audio, or an intermediate
  state. The first pass still includes only one image and the source interval.

Dynamic findings may additionally use `interaction`, `flicker`, `latency`,
`audio-visual`, or `slow4x` as an internal extraction mode. Read
[`../references/temporal-evidence.md`](../references/temporal-evidence.md) before
creating an evidence package.

For a selected dynamic finding, use:

```bash
scripts/extract-clip \
  --video recording.mov \
  --start 00:01:08.720 \
  --end 00:01:18.560 \
  --output output/finding-003.mp4
```

Add `--no-audio` for a silent clip. The selected finding and clip can then be
converted into a requested ticket or document format without changing the
remaining sparse overview.
