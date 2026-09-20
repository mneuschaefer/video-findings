# Verify candidate evidence

Optional deeper investigation only. The ordinary report follows SKILL.md and
does not require this additional verification pass. It uses one representative
image per finding by default.

Continue in the output language chosen during transcript detection. Preserve
quoted speech and visible UI text in their original language unless a
translation was explicitly requested.

Select the timestamp that makes the observed state easiest to understand. When
one frame is not enough to choose confidently, inspect up to three temporary
alternatives or play the relevant video interval. Apply this output rule:

- one persistent or static state: retain the strongest single screenshot;
- two separate stable states whose comparison explains the finding: retain at
  most two screenshots as a clear pair;
- motion- or timing-dependent behavior: retain one orientation screenshot and
  use the optional clip offer below.

- Report only visible UI facts: control state, message, page, overlay, layout,
  or visible transition between sampled frames.
- Multiple inspected frames can support “no visible change in sampled frames”;
  they cannot prove that no brief change happened between them.
- If the issue is timing-dependent, inspect the source interval rather than
  guessing. Mark the final finding as `dynamic`, keep one orientation image
  in the first report, and offer an optional short clip with or without audio.
  Do not create or embed that clip during the first pass.
- If the transcript claim conflicts with the frames, preserve both and describe
  that conflict naturally in the finding.
- A screenshot is useful evidence only if a reviewer can understand what it
  supports from the caption and surrounding observation.
- Give every finding the exact start timestamp from which the reviewer can
  inspect the full motion and audio. Put the real local source-video path once
  in the dossier header; do not add a video deep link to every finding.
- Include a second screenshot only when comparing two separately stable states
  explains the finding without depending on the transition between them. Do not
  use a series of stills as a substitute for offering a clip when the behavior
  is inherently dynamic.

For every clearly dynamic finding, include a simple follow-up action such as:

> This behavior depends on motion. If useful, ask me to extract the relevant
> interval as a short clip with or without audio.

The user may request a selected finding with or without audio. Extract only the
requested interval and keep all other findings in sparse overview form.

For the default dossier, place the one image or justified two-image comparison
directly under the finding prose. Add captions with exact image timestamps and
concrete descriptions of what is visible. Do not present an unexplained
screenshot as evidence. Keep direct quotes and visible UI text in their original
language unless the user requests translation.
