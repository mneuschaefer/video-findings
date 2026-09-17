# Checkout review findings

**Source:** [Narrated checkout review](https://github.com/user-attachments/assets/0862c1c1-45d2-4232-92ac-67865d407157)
The complete transcript was reviewed semantically. It supports two distinct
findings: a repeated complaint about `Continue` and a visible overlap in the
order summary.

## 00:22.720 — Continue provides no visible response

The reviewer reports that pressing `Continue` produces no visible response in
two separate attempts. In the sampled states, the checkout remains on step 2
of 3 with standard delivery selected; the button stays visible and neither an
error nor the next checkout step appears.

The recording has no visible click indicator. It therefore supports the
unchanged interface state, but it cannot prove whether the input event was
registered or establish the cause. The intended checkout navigation is also
not stated.

![Checkout remains on step 2 after the reported Continue action](assets/continue-no-response.jpg)

*Image evidence · 00:27.120 — Checkout remains on step 2 of 3 with standard
delivery selected and Continue still visible.*

Optional next step: extract finding 1 as a short clip with or without audio and
convert it to the requested ticket format.

## 01:08.720 — Discount message overlaps the order total

The reviewer describes a discount message overlapping the total and making the
final amount difficult to read. The representative image directly supports
this: `Discount applied: SAVE10` is rendered across the `Total` row and covers
both its label and amount.

The visible overlap is established, but the recording does not identify the
intended placement or duration of the message, the responsible component, or
the root cause. Those details remain open for later ticket refinement.

![The discount confirmation overlaps the total](assets/discount-overlap.jpg)

*Image evidence · 01:13.640 — The Discount applied: SAVE10 confirmation covers
the Total label and final amount.*

## Source material

[Open the complete timestamped transcript](narrated-demo-transcript.md). The
[source VTT](narrated-demo-transcript.vtt) and
[`findings.json`](narrated-demo-findings.json) are preserved for reuse.
