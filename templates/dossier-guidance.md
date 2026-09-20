# Dossier writing guidance

This tracked file defines the repository default for how `Video Findings.md`
summarizes a recording. Use `.video-findings/preferences.md` for recurring
personal or machine-specific choices; change this file only to update the
published default. Instructions in the current prompt take precedence.

## Default finding

- Start the heading with the exact timestamp and a short descriptive title.
- Write one or two compact paragraphs with enough detail to become a ticket.
- Include the narrated trigger or action, observed behavior, practical effect,
  expectation and repetition only when the transcript states them.
- Stay close to the recording. Do not invent product names, requirements,
  severity, causes, ownership, or intended behavior.
- Embed one representative image for a persistent or static state. Use exactly
  two only when comparing two separately stable states explains the finding,
  such as a clear before/after pair that does not depend on the transition.
  Caption each with its source timestamp and what is visible. Pictures orient
  the reader; they need not prove every spoken claim. Attribute unverified
  behavior to the reviewer instead of auditing it.
- Use screenshots as attached evidence, not as a source for unspoken visible
  details, extra findings or product context. Keep captions neutral.
- Refer to the person neutrally as the reviewer unless the source identifies
  them. Do not add boilerplate sections about unknown causes or ownership.
- Put the real local source-video path once in the dossier header. Use the
  timestamp in the finding heading instead of a per-finding video deep link.
- Keep quotes and visible UI text in their original language unless translation
  is requested. Direct quotes are optional because the transcript is linked.

## Include only when relevant

Add a natural sentence—not a separate metadata field—when:

- speech is difficult to understand;
- the visible state contradicts the narration or is materially ambiguous;
- important product context is missing and affects interpretation;
- the reviewer explicitly says that something needs another check;
- a dynamic interval or follow-up clip would materially help.

For clearly dynamic behavior such as flicker, disappearing states, dragging or
repeated transitions, keep one orientation image in the first report. State
briefly that one frame cannot show the full behavior and offer to extract the
relevant interval as a short clip with or without audio. Create that clip only
after the user asks for it.

## Other topics mentioned

If the transcript contains useful ideas, reminders, preferences, future work,
or unrelated discussion that is not a finding:

- add one short pointer near the beginning of the dossier;
- place a separate `Other topics mentioned` section after every finding;
- give each topic a timestamp, concise title, and short neutral description;
- do not require a screenshot or turn the section into a meeting summary;
- summarize those topics further only when requested.

Omit the pointer and section when no useful other topics exist. Do not retain
filler or vague asides merely to prove that every sentence was classified.

## Omit by default

- Status labels such as `Needs review`;
- generic confidence ratings;
- generic evidence labels;
- repeated warnings that every finding should be read again;
- transcript quotations that add no information beyond the description.
- disclaimers merely because a screenshot cannot prove an interaction;
- a duplicate structured JSON report unless requested.
