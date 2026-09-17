# macOS setup

## Supported setup

The package is designed for a local, writable checkout on macOS. It is tested
primarily on Apple Silicon. Intel Macs can run the deterministic pipeline but
local transcription may be slower.

Required for all runs:

- Python 3.10 or newer; the project uses only the standard library;
- FFmpeg and FFprobe;
- read access to the local input file;
- write access to the repository's `input/`, `output/`, and `models/` folders.

Required only when no VTT/SRT transcript is available:

- either MacParakeet with an already downloaded Parakeet model (preferred), or
  `whisper.cpp` with a local GGML Whisper model (fallback).

Video Findings checks the standalone `macparakeet-cli` and the CLI bundled in
`/Applications/MacParakeet.app`. When both its CLI and a local Parakeet model
are ready, that installation is reused without downloading another speech
model. The transcription wrapper disables MacParakeet telemetry for its runs
and uses `--no-history`, so those jobs are not added to MacParakeet history.

## Safe setup behavior

Run a read-only check first:

```bash
./scripts/setup-macos
```

Install the approved core dependencies and single selected model only after
reviewing the requested changes:

```bash
./scripts/setup-macos --install
```

In an interactive terminal this asks for confirmation. An agent or other
non-interactive caller must stop after showing the plan and obtain explicit
approval before using:

```bash
./scripts/setup-macos --install --yes
```

The install mode:

1. detects a ready MacParakeet/Parakeet installation first;
2. prints the complete plan before changing anything;
3. requires an existing Homebrew installation only when formulae are missing;
4. requests only missing core formulae;
5. reuses an existing compatible model or downloads exactly the one model in
   the approved plan;
6. validates commands, model readability, and project write access;
7. runs a short local transcription smoke test when a backend is ready. If the Whisper Metal/GPU
   backend fails, the wrapper retries with `whisper.cpp --no-gpu`.

If neither Parakeet nor a complete local Whisper setup is ready, setup plans
exactly one model so video-only transcription works. With MacParakeet present,
the default is the currently tested Parakeet TDT v3. Without MacParakeet, the
default is the Whisper `base` fallback. Choose a different plan before approval
when another model better fits the machine or language:

```bash
./scripts/setup-macos --backend parakeet --parakeet-model parakeet-v3
./scripts/setup-macos --backend whisper --model small
```

The corresponding `--install` invocation must use the same options. The setup
never downloads more than one speech model.

It does not install Homebrew automatically, request administrator privileges,
upload media, or modify shell startup files. When Homebrew is missing, it stops
and points to `https://brew.sh`.

The additional speech-model download is **0 MiB when a compatible model is
already installed**. Otherwise exactly one model is downloaded. MacParakeet
currently reports Parakeet TDT v3 at ~465 MB. The default Whisper fallback
`base` is 142 MiB; the smallest opt-in alternative is `tiny` 75 MiB, followed
by `small` 466 MiB, `medium` 1.5 GiB, and full `large` 2.9 GiB. Start with Parakeet v3, or
Whisper `base` when MacParakeet is unavailable. Move to a larger or newer
compatible model only when the machine, language, or transcript quality calls
for it. Homebrew may separately fetch missing Python, FFmpeg, or `whisper.cpp`
bottles and system-specific dependencies; the read-only plan lists the exact
formulae separately from the one model download.
The Whisper sizes come from the official
[whisper.cpp model table](https://github.com/ggml-org/whisper.cpp#memory-usage).

Parakeet TDT v3 is the currently tested and preferred backend. This is a
baseline rather than a permanent version lock. A newer model exposed by
`macparakeet-cli models list` can be selected in the plan before installation:

```bash
./scripts/setup-macos --backend parakeet --parakeet-model NEW_MODEL_ID
```

To select a compatible model that is already installed, use:

```bash
export VIDEO_FINDINGS_PARAKEET_MODEL="NEW_VARIANT"
```

The setup will not search for or switch to a newer model by itself. A compatible
existing Whisper GGML model can likewise be supplied through
`VIDEO_FINDINGS_MODEL_PATH`. This allows deliberate upgrades without turning
ordinary setup into an automatic multi-model download.
For current upstream Parakeet variants, see FluidAudio's
[ASR model guide](https://github.com/FluidInference/FluidAudio/blob/main/Documentation/Models.md).

Automatic selection prefers Parakeet. Override it for one run when needed:

```bash
VIDEO_FINDINGS_TRANSCRIBER=parakeet ./scripts/transcribe-local input.mov output.vtt
VIDEO_FINDINGS_TRANSCRIBER=whisper ./scripts/transcribe-local input.mov output.vtt
```

Choose a different model when needed:

```bash
./scripts/setup-macos --install --backend whisper --model small
export VIDEO_FINDINGS_MODEL_PATH="$PWD/models/ggml-small.bin"
```

The default base model keeps setup reasonably small. A larger multilingual
model can improve difficult audio at the cost of download size, memory, and
runtime.

Force the CPU path when a Mac has a known Metal/backend incompatibility:

```bash
export VIDEO_FINDINGS_NO_GPU=1
```

After an actual GPU backend failure, the wrapper stores the project-local marker
`models/.force-cpu` and uses the stable CPU path on later runs. Set
`VIDEO_FINDINGS_USE_GPU=1` for one run if you intentionally want to retry the
GPU backend after an upgrade.

## File permissions and local availability

Files stored in iCloud Drive, OneDrive, or another sync service must be fully
downloaded before analysis. A placeholder may exist in Finder while FFprobe
still cannot read it.

Check a specific input before processing:

```bash
./scripts/check-environment --require-transcription --video "/path/review.mov"
```

The check verifies that the file is readable, FFprobe can parse it, the local
model is readable, and output folders are writable.
