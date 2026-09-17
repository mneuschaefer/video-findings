# Architecture

The project has three deliberately separate layers.

1. **Local preparation layer:** probes media, optionally transcribes audio with
   a ready local Parakeet or Whisper backend, parses VTT/SRT, exports every cue
   to `transcript-cues.json`, proposes optional keyword-led windows, extracts
   one initial frame per lead, and writes JSON/Markdown. Transcript parsing and media processing are
   deterministic; speech recognition is local model inference.
2. **Interpretation layer:** the AI reviews the complete cue manifest
   semantically in its source language. Keyword leads never define coverage.
   The skill and prompts distinguish observation, expectation, interpretation,
   and uncertainty, then select additional visual windows when required.
3. **Presentation layer:** templates keep output portable across GitHub,
   Obsidian, and other Markdown tools.

The cue and candidate JSON files are the stable boundary. Transcription backends
can change without coupling them to semantic detection, media extraction, or
the final report contract.
