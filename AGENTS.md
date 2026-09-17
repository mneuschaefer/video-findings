# Agent guidance

This repository turns narrated videos into reviewable visual findings. Preserve
the boundary between deterministic media processing and model interpretation.

- Keep media scripts small, local-first, and dependency-light.
- Never describe a model inference as an observed fact.
- Keep `observation`, `reviewer_expectation`, `interpretation`, and
  `human_decision` separate in every finding.
- Do not create external tickets or upload media without explicit approval.
- Prefer an existing VTT/SRT transcript. Transcription is an optional adapter,
  not a core dependency.
- Accept local QuickTime/macOS screen recordings and downloaded Teams recording
  files. Never fetch a Teams recording from a meeting service automatically.
- Run `scripts/check-environment` before processing input. On macOS, offer
  the read-only `scripts/setup-macos` plan when dependencies are missing. Reuse
  a ready MacParakeet model before offering the Whisper fallback. State the
  approximate download and warn that Homebrew dependencies may require several
  gigabytes; use `scripts/setup-macos --install --yes` only after approval.
- Run `make test` and `make demo` after behavior changes.
