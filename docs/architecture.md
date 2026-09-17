# Architecture

The project has three deliberately separate layers.

1. **Local preparation layer:** probes media, optionally transcribes audio with
   a ready local Parakeet or Whisper backend, preserves the source VTT/SRT,
   exports every cue to `transcript.md` and `transcript-cues.json`, proposes
   optional keyword-led windows, extracts one initial frame per lead, and writes
   JSON/Markdown. Transcript parsing and media processing are deterministic;
   speech recognition is local model inference.
2. **Interpretation layer:** the AI reviews the complete cue manifest
   semantically in its source language. Keyword leads never define coverage.
   The skill and prompts distinguish observation, expectation, interpretation,
   and uncertainty, then select additional visual windows when required.
3. **Presentation layer:** templates produce a detailed `report.md`, reusable
   `findings.json`, and sparse evidence with one image per finding. Findings
   that depend on motion are marked `dynamic`; selected short clips are created
   only when the user asks for them. Output remains portable across GitHub,
   Obsidian, ticket formats, and other tools.

The source transcript, cue JSON, and findings JSON are stable boundaries.
Transcription backends and derived report formats can change without requiring
another transcription pass.
