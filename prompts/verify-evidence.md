# Verify candidate evidence

Continue in the output language chosen during transcript detection. Preserve
quoted speech and visible UI text in their original language unless a
translation was explicitly requested.

Inspect the beginning, middle, and end frames for each candidate window.

- Report only visible UI facts: control state, message, page, overlay, layout,
  or visible transition between sampled frames.
- A set of identical frames can support “no visible change in sampled frames”;
  it cannot prove that no brief change happened between them.
- If the issue is timing-dependent, request a denser frame sample or inspect the
  clip rather than guessing.
- If the transcript claim conflicts with the frames, preserve both and mark the
  finding `Needs review`.
- A screenshot is useful evidence only if a reviewer can understand what it
  supports from the caption and surrounding observation.

Classify confidence as High, Medium, or Low based on combined evidence, not the
reviewer's certainty of tone.
