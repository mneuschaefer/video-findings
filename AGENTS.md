# Agent guidance

This repository turns narrated videos into reviewable visual findings. Preserve
the boundary between deterministic media processing and model interpretation.

- Keep media scripts small, local-first, and dependency-light.
- Build a compact numeric motion index during the first pass without generating
  extra images or clips. Treat it as routing data, never as proof.
- Never describe a model inference as an observed fact.
- Preserve every timestamped transcript cue in both readable Markdown and
  machine-readable JSON so derived artifacts can be regenerated.
- Capture described bugs without inventing missing product context. Do not
  infer product names, requirements, severity, root cause, roles, or expected
  behavior unless the recording supports them.
- Keep `observation`, `reviewer_expectation`, `interpretation`, and
  `human_decision` separate in every finding.
- Do not create external tickets or upload media without explicit approval.
- Prefer an existing VTT/SRT transcript. Transcription is an optional adapter,
  not a core dependency.
- Require the AI to review the complete timestamped transcript semantically in
  its source language. Keyword matches are optional leads only and must never
  define coverage or become findings without contextual AI review.
- Resolve the report language from the current user instruction, known user
  preference, language of the current request, and only then the dominant
  transcript language. Keep transcript, report, and quote/UI language separate;
  preserve direct quotes and visible labels in their original language unless
  translation is requested.
- Accept local QuickTime/macOS screen recordings and downloaded Teams recording
  files. Never fetch a Teams recording from a meeting service automatically.
- Run `scripts/check-environment` before processing input. On macOS, offer
  the read-only `scripts/setup-macos` plan when dependencies are missing. Reuse
  a ready MacParakeet model before offering the Whisper fallback. State the
  chosen single-model download and its reported size; use
  `scripts/setup-macos --install --yes` only after approval. Ensure one local
  transcription model is ready, prefer the currently tested Parakeet TDT v3 on
  compatible Macs, and never download a second model unnecessarily. Preserve
  an explicit user choice of another supported backend or model.
- Run `make test` and `make demo` after behavior changes.
