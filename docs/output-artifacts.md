# Output artifacts

The first pass creates a sparse overview and preserves enough source material
to regenerate later reports without retranscribing the recording.

`material/findings.json` keeps `transcript_language` and `report_language`
separate. An explicit language request wins; otherwise the report uses the
language of the current prompt. Direct quotes and visible UI labels preserve
their original language unless translation is requested.

The user may request another output name, format, or folder structure. Without
such an override, the output root contains only `Video Findings.md` and the
`material/` folder.

For a local recording, the dossier header records the original video's real
system path once. Each finding uses its heading timestamp to identify the
relevant point; the default output does not construct per-finding video deep
links.

| Artifact | Purpose |
|---|---|
| `Video Findings.md` | One scrollable, detailed, human-readable dossier |
| `material/transcript-source.vtt` or `.srt` | Preserved timestamped source transcript |
| `material/transcript.md` | Complete readable transcript with timestamps and speakers when available |
| `material/transcript-cues.json` | Complete machine-readable transcript source |
| `material/candidates.json` | Optional deterministic leads for AI review |
| `material/motion-1s.tsv` | Compact numeric whole-video motion index for routing |
| `material/motion.tsv` | Detailed motion values for selected inspection windows |
| `material/findings.json` | Structured findings for regeneration and conversion |
| `material/finding-*.jpg` | One representative evidence image per final finding by default |

The report lists every described bug or actionable finding and distinguishes
reported behavior from visible verification. Unknown product names,
requirements, roles, severity, causes, or intended behavior stay unknown.
Every finding heading begins with its timestamp. One or two detailed paragraphs
provide enough context for later tickets, followed by the representative image
and a caption stating the image timestamp and visible state.
Generic Status, Confidence, and Evidence labels are omitted from the dossier.
Specific uncertainty or a reviewer-requested follow-up is included naturally
only when it adds useful information. Customize these rules in
[`../templates/dossier-guidance.md`](../templates/dossier-guidance.md).

When useful transcript content is not a finding, `findings.json` stores it in
the top-level `other_topics` array. The dossier gives one brief notice near the
beginning and lists those timestamped topics after every finding. This final
section is only an index: it uses no evidence images and does not claim to be a
complete meeting summary. The user can request a separate summary of selected
topics later. If no useful other topics exist, the array is empty and the
notice and section are omitted.

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
  --output output/material/finding-003.mp4
```

Add `--no-audio` for a silent clip. The selected finding and clip can then be
converted into a requested ticket or document format without changing the
remaining sparse overview.
