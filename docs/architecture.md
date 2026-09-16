# Architecture

The project has three deliberately separate layers.

1. **Deterministic layer:** parses VTT/SRT, proposes time windows, extracts
   frames, and writes JSON/Markdown without a model dependency.
2. **Interpretation layer:** the skill and prompts distinguish observation,
   expectation, interpretation, and uncertainty.
3. **Presentation layer:** templates keep output portable across GitHub,
   Obsidian, and other Markdown tools.

The intermediate JSON is the stable boundary. A future transcription backend,
multimodal model, launcher, or ticket exporter can be replaced without changing
the media scripts or report contract.

