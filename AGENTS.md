# Agent guidance

This repository turns narrated screen recordings into reviewable findings.

- Follow `SKILL.md` for user-facing analysis. Keep ordinary runs short: one
  preparation pass, one complete transcript read, targeted images, one report.
- If `.video-findings/preferences.md` exists, read it once before the run.
  Current user instructions override it. Keep machine- and user-specific
  preferences in this ignored directory instead of editing tracked files.
- Keep media scripts local-first, deterministic and dependency-light. Preserve
  every transcript cue in readable Markdown and machine-readable JSON.
- Never turn model inference into observed fact or invent product context,
  requirements, severity, root cause, ownership or expected behavior.
- Keep derived artifacts under `material/` and one user-facing
  `Video Findings.md` at the output root unless the user requests otherwise.
- Do not create external tickets or upload media without explicit approval.
- Prefer a supplied VTT/SRT. Otherwise reuse the verified configured local
  adapter. Ordinary runs must not search for replacements or download models.
  For setup failures follow `docs/setup-macos.md`; show source, destination and
  expected size and obtain approval before installing or downloading anything.
- Accept local macOS/QuickTime and downloaded meeting recordings; never fetch a
  meeting recording from a service automatically.
- Run `make test` and `make demo` after behavior changes.
