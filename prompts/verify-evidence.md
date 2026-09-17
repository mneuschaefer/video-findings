# Verify candidate evidence

Continue in the output language chosen during transcript detection. Preserve
quoted speech and visible UI text in their original language unless a
translation was explicitly requested.

The final report should normally contain exactly one representative screenshot
per finding. Select the timestamp that makes the observed state easiest to
understand. When one frame is not enough to choose confidently, inspect up to
three temporary alternatives or play the relevant video interval, then retain
only the strongest screenshot in the report.

- Report only visible UI facts: control state, message, page, overlay, layout,
  or visible transition between sampled frames.
- Multiple inspected frames can support “no visible change in sampled frames”;
  they cannot prove that no brief change happened between them.
- If the issue is timing-dependent, request a denser frame sample or inspect the
  source interval rather than guessing. Mark the final finding as `dynamic` and
  offer an optional short clip; do not create or embed that clip during the
  first pass.
- If the transcript claim conflicts with the frames, preserve both and describe
  that conflict naturally in the finding.
- A screenshot is useful evidence only if a reviewer can understand what it
  supports from the caption and surrounding observation.
- Reference the original video for every finding and give the exact start
  timestamp from which the reviewer can inspect the full motion and audio.
- Include multiple screenshots in the final report only when the user
  explicitly requests dense evidence.

For every dynamic finding, include a simple follow-up action such as:

> Ask: "Extract finding 3 as a short clip with audio and convert it to my ticket
> format."

The user may request a selected finding with or without audio. Extract only the
requested interval and keep all other findings in sparse overview form.

For the default dossier, keep one representative image directly under the
finding prose. Add a caption with the exact image timestamp and a concrete
description of what is visible. Do not present an unexplained screenshot as
evidence. Keep direct quotes and visible UI text in their original language
unless the user requests translation.
