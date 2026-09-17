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

Install missing dependencies only after reviewing the requested changes:

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
4. requests only missing `python` and `ffmpeg` formulae, plus `whisper.cpp`
   only when no ready local transcription backend exists;
5. downloads the selected Whisper model from the official whisper.cpp model
   repository on Hugging Face only for that fallback path;
6. validates commands, model readability, and project write access;
7. runs a short local transcription smoke test. If the Whisper Metal/GPU
   backend fails, the wrapper retries with `whisper.cpp --no-gpu`.

It does not install Homebrew automatically, request administrator privileges,
upload media, or modify shell startup files. When Homebrew is missing, it stops
and points to `https://brew.sh`.

The default Whisper `base` model is about 142 MB. Other documented model sizes
range from roughly 75 MB to several gigabytes. Homebrew may update package
metadata and install or upgrade transitive dependencies; depending on what is
already present, the total network and disk requirement can range from hundreds
of megabytes to several gigabytes. The read-only setup plan makes this risk
visible before approval, although Homebrew determines the exact dependency set.

Automatic selection prefers Parakeet. Override it for one run when needed:

```bash
VIDEO_FINDINGS_TRANSCRIBER=parakeet ./scripts/transcribe-local input.mov output.vtt
VIDEO_FINDINGS_TRANSCRIBER=whisper ./scripts/transcribe-local input.mov output.vtt
```

Choose a different model when needed:

```bash
./scripts/setup-macos --install --model small
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
