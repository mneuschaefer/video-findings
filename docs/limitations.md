# Limitations

- Transcript-led search can miss purely visual problems that nobody mentions.
- A representative screenshot can miss short-lived state changes. The first
  pass marks these findings as dynamic and links the relevant interval. Extract
  a short clip with or without audio only when the user selects that finding.
- Reviewer expectations may be incorrect or outside the intended requirements.
- Keyword candidates are intentionally simple, strongest for direct English
  wording, and are not final findings. Language-independent detection requires
  semantic AI review of the complete cue manifest.
- The AI can still misunderstand ambiguous wording, mixed languages, irony, or
  domain-specific references; preserve quotes and mark uncertainty.
- Visual evidence cannot establish backend behavior or root cause.
- Final severity, acceptance criteria, ownership, and ticket creation require
  product context and human judgment.
- Never infer a product, feature, requirement, role, or root cause when the
  recording does not establish it. Preserve the speaker's wording and list the
  missing context explicitly.
