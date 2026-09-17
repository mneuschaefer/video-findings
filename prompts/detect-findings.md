# Detect transcript-led finding candidates

Read the complete timestamped transcript, preferably
`material/transcript-cues.json`, as
a search index, not as proof that a defect exists. Detect findings semantically
in any language. Never use the bundled keyword candidates as a coverage
boundary: they are optional efficiency hints and may miss non-English wording.
When `motion-1s.tsv` is available, use it as a compact routing signal for
transcript-aligned state changes. Motion peaks are not findings and do not prove
that a defect occurred.

## Output language

Resolve the report language in this order:

1. the current user instruction;
2. the language of the current prompt/request;
3. a known user language preference only when the prompt language is unclear;
4. the dominant transcript language as the final fallback.

The transcript language describes the source; it does not override the user's
report language. Preserve transcript quotes and visible UI labels in their
original language unless the user asks for a translation. If the recording
switches languages, preserve each quoted passage in its source language while
keeping the report prose consistent.

The user may override the dossier name, structure, format, or artifact set in
the current prompt. Otherwise produce the default single-file dossier described
in `SKILL.md`.

For each possible finding:

1. Quote or closely paraphrase the smallest relevant passage.
2. Capture a time window with context before and after the statement.
3. Separate what the reviewer observed from what they expected.
4. Include each described bug even when it cannot be confirmed visually in the
   first pass. Label it as reported, unverified, or `Needs review` instead of
   silently dropping it.
5. Stay close to the speaker's wording. Use neutral terms such as "the reviewed
   interface" when the product, feature, user role, or intended behavior is not
   established.
6. Do not infer severity, root cause, requirements, ownership, or expected
   behavior from plausibility. Write "Not stated" or identify the context as
   unknown.
7. Mark vague frustration as weak evidence unless a concrete behavior is named.
8. Treat statements such as “I expected” as expectations, not product truth.
9. Classify the evidence need as `static` or `dynamic`. Use `dynamic` when the
   claim depends on timing, motion, audio, a transition, flicker, latency,
   dragging, or a short-lived intermediate state. When dynamic, also choose the
   most likely internal mode: `interaction`, `flicker`, `latency`,
   `audio-visual`, or `slow4x`.
10. Merge repeated discussion of the same behavior while retaining every time
   range.
11. Exclude harmless commentary and general preferences unless they imply an
   actionable usability concern.

Return candidate findings only. The first pass is a "where to find what"
overview. Visual verification happens separately and uses one representative
image per finding by default.
