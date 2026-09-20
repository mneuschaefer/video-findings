# Validated local transcription — 2026-09-20

Host: Apple M4, macOS, Swift 6.3.3. Runtime: standalone FluidAudio v0.15.8
(commit `87a39dfe4068fef0f1c69bfe704b2b3ef4fbc5bc`). Model: already installed
Parakeet TDT v3 CoreML bundle, including `JointDecisionv3.mlmodelc`.
No new model weights were needed for this working path.

| Measurement | Observed wall time |
|---|---:|
| One-time runtime build | 139.63 s |
| First configuration/transcription check on 82 s video | 17.88 s |
| Subsequent `analyze-recording` on 82 s video | 1.82 s |
| German synthetic speech, 8.81 s | 0.41 s |

The subsequent full preparation includes environment check, audio extraction,
fresh transcription, VTT validation, transcript artifacts, candidate grouping
and motion index. It does not include the agent's final semantic review,
image selection or finished findings report. FluidAudio reported 0.543 s of
ASR processing within that 1.82 s wall time. Timings come from `/usr/bin/time -p`
and the runtime's processing output. These are single observations on one Mac,
not a guarantee or a comparison against visual-only analysis.

The fresh English VTT preserved all narrated observations in 13 timestamped
cues. The German synthetic sample reproduced all three input sentences:

> Dies ist ein Test der deutschen Spracherkennung. Ich drücke auf Weiter, aber
> die Seite reagiert nicht. Die Fehlermeldung verdeckt den Gesamtbetrag.

This verifies English and German smoke-test behavior, not broad multilingual
accuracy. The first configuration check saved `models/transcriber-path` only
after successful timestamped transcription. The following worked directly:

```bash
./scripts/analyze-recording --video assets/narrated-demo.mp4 --output output/validated-local
```

`setup-macos` then reported the saved transcriber and planned no further model
installation. Build commands explicitly disabled keychain and netrc access.
The adapter uses FluidAudio's local-only loader; absent model components fail
locally. See [setup](setup-macos.md#existing-fluidaudio-coreml-models).
