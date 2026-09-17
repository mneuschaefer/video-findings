<!-- Default dossier. Follow a different output name, format, or structure when
the current prompt requests one.

Language policy:
- Report language: explicit current instruction, otherwise current prompt.
- Transcript language: source language; fallback only when prompt is unclear.
- Quote/UI language: preserve original wording unless translation is requested.
-->

# Video Findings

**Source:** {{ source }}

**Original video:** {{ original_video_link }}

**Generated:** {{ generated_at }}

**Status:** Draft — human review required

{{ summary }}

{{ findings }}

## Source material

[Open the complete timestamped transcript](material/transcript.md)

The transcript and machine-readable files under `material/` can regenerate or
reformat this dossier without transcribing the recording again.
