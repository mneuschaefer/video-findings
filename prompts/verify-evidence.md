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
  clip rather than guessing.
- If the transcript claim conflicts with the frames, preserve both and mark the
  finding `Needs review`.
- A screenshot is useful evidence only if a reviewer can understand what it
  supports from the caption and surrounding observation.
- Reference the original video for every finding and give the exact start
  timestamp from which the reviewer can inspect the full motion and audio.
- Include multiple screenshots in the final report only when the user
  explicitly requests dense evidence.

Classify confidence as High, Medium, or Low based on combined evidence, not the
reviewer's certainty of tone.
