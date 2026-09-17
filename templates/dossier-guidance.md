# Dossier writing guidance

This file is the user-editable default for how `Video Findings.md` summarizes a
recording. Change it for a recurring personal or team workflow. Instructions in
the current prompt take precedence.

## Default finding

- Start the heading with the exact timestamp and a short descriptive title.
- Write one or two substantive paragraphs rather than a stack of metadata.
- Combine what is visible, how the reviewer describes it, what they expect or
  intend to do, and any relevant surrounding context.
- Stay close to the recording. Do not invent product names, requirements,
  severity, causes, ownership, or intended behavior.
- Embed one representative image and caption it with its exact timestamp and a
  concrete description of what is visible.
- Link the corresponding point in the original video.
- Keep quotes and visible UI text in their original language unless translation
  is requested. Direct quotes are optional because the transcript is linked.

## Include only when relevant

Add a natural sentence—not a separate metadata field—when:

- speech is difficult to understand;
- the visible state is ambiguous or does not verify the spoken claim;
- important product context is missing and affects interpretation;
- the reviewer explicitly says that something needs another check;
- a dynamic interval or follow-up clip would materially help.

## Other topics mentioned

If the transcript contains useful ideas, reminders, preferences, future work,
or unrelated discussion that is not a finding:

- add one short pointer near the beginning of the dossier;
- place a separate `Other topics mentioned` section after every finding;
- give each topic a timestamp, concise title, and short neutral description;
- do not require a screenshot or turn the section into a meeting summary;
- offer to summarize selected topics separately if the user wants them.

Omit the pointer and section when no useful other topics exist. Do not retain
filler or vague asides merely to prove that every sentence was classified.

## Omit by default

- Status labels such as `Needs review`;
- generic confidence ratings;
- generic evidence labels;
- repeated warnings that every finding should be read again;
- transcript quotations that add no information beyond the description.
