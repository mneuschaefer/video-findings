# Agent guidance

This repository turns recorded UI reviews into reviewable findings. Preserve
the boundary between deterministic media processing and model interpretation.

- Keep media scripts small, local-first, and dependency-light.
- Never describe a model inference as an observed fact.
- Keep `observation`, `reviewer_expectation`, `interpretation`, and
  `human_decision` separate in every finding.
- Do not create external tickets or upload media without explicit approval.
- Prefer an existing VTT/SRT transcript. Transcription is an optional adapter,
  not a core dependency.
- Run `make test` and `make demo` after behavior changes.

