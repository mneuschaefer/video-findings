# Detect transcript-led finding candidates

Read the timestamped transcript as a search index, not as proof that a defect
exists.

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

