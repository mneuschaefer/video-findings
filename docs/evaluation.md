# Synthetic demo evaluation

The 26-second demo transcript contains six deliberately different situations.

| Situation | Expected pipeline behavior |
|---|---|
| Clear spoken bug | Candidate finding |
| Diffuse frustration | Exclude without concrete behavior |
| Possibly wrong reviewer expectation | Candidate, low/medium confidence |
| Purely visual problem | Missed by transcript-led detection; document limit |
| Repeated same issue | Merge, retain both time ranges |
| Harmless positive remark | Exclude |

Success is not “find everything.” Success is producing a small, inspectable set
of leads while making false positives, misses, and evidence limits visible.

