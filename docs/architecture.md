# Architecture

The project has three deliberately separate layers.

1. **Local preparation layer:** probes media, optionally transcribes audio with
   `whisper.cpp`, parses VTT/SRT, proposes time windows, extracts frames, and
   writes JSON/Markdown. Transcript parsing and media processing are
   deterministic; speech recognition is local model inference.
2. **Interpretation layer:** the skill and prompts distinguish observation,
   expectation, interpretation, and uncertainty.
3. **Presentation layer:** templates keep output portable across GitHub,
   Obsidian, and other Markdown tools.

The intermediate JSON is the stable boundary. The bundled whisper.cpp wrapper
can be replaced with another timestamped VTT/SRT producer without changing the
candidate, media, or report contract.
