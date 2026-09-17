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

- `whisper.cpp` and its `whisper-cli` binary;
- a local GGML Whisper model. The setup script defaults to multilingual
  `ggml-base.bin`.

## Safe setup behavior

Run a read-only check first:

```bash
./scripts/setup-macos
```

Install missing dependencies only after reviewing the requested changes:

```bash
./scripts/setup-macos --install
```

The install mode:

1. requires an existing Homebrew installation;
2. requests only missing `python`, `ffmpeg`, or `whisper.cpp` formulae;
3. downloads the selected Whisper model from the official whisper.cpp model
   repository on Hugging Face;
4. validates commands, model readability, and project write access.
5. runs a short local transcription smoke test. If the Metal/GPU backend fails,
   the wrapper retries with `whisper.cpp --no-gpu`.

It does not install Homebrew automatically, request administrator privileges,
upload media, or modify shell startup files. When Homebrew is missing, it stops
and points to `https://brew.sh`.

Homebrew may update its package metadata and install or upgrade transitive
dependencies as part of a normal formula installation. Review Homebrew's plan
before approving the command.

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
