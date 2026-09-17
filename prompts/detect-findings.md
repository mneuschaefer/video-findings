# Detect transcript-led finding candidates

Read the complete timestamped transcript, preferably `transcript-cues.json`, as
a search index, not as proof that a defect exists. Detect findings semantically
in any language. Never use the bundled keyword candidates as a coverage
boundary: they are optional efficiency hints and may miss non-English wording.

## Output language

Use an output language explicitly requested by the user. Otherwise, write
finding titles, explanations, statuses, and decisions in the dominant language
of the recording or transcript. If the recording switches languages, use the
language of each relevant passage unless that would make the report confusing;
in that case use the dominant language consistently. Preserve transcript quotes
and visible UI labels in their original language unless the user asks for a
translation.

For each possible finding:

1. Quote or closely paraphrase the smallest relevant passage.
2. Capture a time window with context before and after the statement.
3. Separate what the reviewer observed from what they expected.
4. Mark vague frustration as weak evidence unless a concrete behavior is named.
5. Treat statements such as “I expected” as expectations, not product truth.
6. Merge repeated discussion of the same behavior while retaining every time
   range.
7. Exclude harmless commentary and general preferences unless they imply an
   actionable usability concern.

Return candidate findings only. Visual verification happens separately.
