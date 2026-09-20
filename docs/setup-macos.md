# macOS setup

## Recommended one-time setup on Apple Silicon

### Existing FluidAudio CoreML models

This path has been [validated locally on an Apple M4](validated-local-transcription.md)
with the 82-second English demo and a short German speech sample.

If compatible Parakeet CoreML models already exist, reuse them with the standalone
FluidAudio CLI. Do not install MLX-format weights just because a CLI is missing.
No MacParakeet or VoiceInk app is required. After approval for runtime setup:

```bash
git clone --depth 1 --branch v0.15.8 https://github.com/FluidInference/FluidAudio.git models/FluidAudio-runtime
swift build --package-path models/FluidAudio-runtime -c release \
  --product fluidaudiocli --disable-default-traits --disable-keychain --disable-netrc
./scripts/configure-transcriber ./scripts/transcribe-fluidaudio \
  --test-media assets/narrated-demo.mp4
```

This downloads and builds runtime source/dependencies, not model weights. The
public build needs no GitHub credentials: keychain/netrc access is explicitly
disabled. Swift may still fetch its declared text-processing binary artifact
(about 49 MB) despite disabled default traits.

The adapter uses `--local-model-dir`, whose loader fails on missing components
instead of downloading replacements. Its default model directory is
`~/Library/Application Support/FluidAudio/Models/parakeet-tdt-0.6b-v3`.
This is a default location, not proof of compatibility: v0.15.8 requires the
v3 joint component `JointDecisionv3.mlmodelc` and matching vocabulary. Point
`VIDEO_FINDINGS_FLUIDAUDIO_MODEL` at the actual compatible directory when needed;
`VIDEO_FINDINGS_FLUIDAUDIO_CLI` selects an existing CLI build. Preserve nondefault
settings in the user's environment or an adapter executable before registration.
Existing incomplete/older bundles need an explicit compatibility decision,
never a silent download. Runtime files remain local and are excluded from releases.

### New setup without reusable CoreML models

Already have a timestamped VTT/SRT? Use it directly. Already have a working
local transcriber? Reuse it. No particular app or model is required.

For a new Apple Silicon setup, [Parakeet MLX](https://github.com/senstella/parakeet-mlx)
is a practical option with local multilingual transcription and VTT output.
It needs FFmpeg, its Python dependencies, and MLX-format model weights. Existing
FluidAudio CoreML files are a different format and cannot replace those weights.
Intel Macs can use the existing Whisper path described below.

**Before installing:** the assistant must show one concrete plan with packages,
model, download sources, target locations, and expected download sizes. If the
size is unknown, say so; model downloads can be large. Ask for approval once,
or let the user run the commands themselves. Reading this guide is not approval.
Do not invoke first-run download commands during ordinary dependency checks.

After approval, with `uv` and FFmpeg available:

```bash
uv tool install parakeet-mlx==0.5.2
HF_HUB_DISABLE_XET=1 parakeet-mlx assets/narrated-demo.mp4 \
  --model mlx-community/parakeet-tdt-0.6b-v3 \
  --output-format vtt --output-dir output/transcription-check
```

The second command downloads approximately 2.51 GB of model weights (plus
small configuration files) on first use from Hugging Face and
transcribes the bundled demo. Packages live in uv's tool environment (`uv tool
dir`); weights normally live under `~/.cache/huggingface/hub`, unless Hugging Face
cache variables override it. Python/runtime dependencies take additional space;
uv reports their downloads separately. `HF_HUB_DISABLE_XET=1` uses the standard
HTTP download route; it does not alter the model or transcription quality.
Resolve these actual destinations in the plan.
For model sizes and files, consult the
[model repository](https://huggingface.co/mlx-community/parakeet-tdt-0.6b-v3/tree/main).
If uv or FFmpeg is missing, include it in the same approval plan rather than
assuming it is installed. Installation details are in the upstream link above.

Verify offline reuse and save the adapter once:

```bash
./scripts/configure-transcriber ./scripts/transcribe-parakeet-mlx \
  --test-media assets/narrated-demo.mp4
```

This tests fresh transcription with downloads disabled, validates timestamped
output, and only then writes `models/transcriber-path`. That machine-local file
is excluded from Git and release archives. Subsequent recordings use:

```bash
./scripts/analyze-recording --video /path/to/review.mov --output output/review
```

Normal Parakeet MLX runs enforce `HF_HUB_OFFLINE=1`. A missing model causes an
error, not a download or a backend change. Language is detected automatically.
The wrapper finds `parakeet-mlx` on PATH or in `~/.local/bin`; a nonstandard
location can be set with `VIDEO_FINDINGS_MLX_CLI`. `VIDEO_FINDINGS_MLX_MODEL`
selects another compatible cached model. Preserve any such overrides in the
user's environment or a small adapter executable and verify them before saving.

Any other local backend can be saved using the same configuration command. Its
adapter must accept `INPUT OUTPUT_VTT [LANGUAGE]`, write valid nonempty VTT,
return nonzero on failure, and never install or download during ordinary runs.
The generic wrapper cannot enforce offline behavior inside third-party adapters;
verify their offline settings during setup. It invokes the saved file directly,
without evaluating shell command text. A broken saved path needs repair or
reconfiguration. It must not cause a fresh search or automatic installation.

## Legacy built-in setup

The following describes the existing MacParakeet/Whisper installer. It is an
alternative, not a prerequisite for the configured adapter above. If an adapter
is saved, the default setup checks it and does not plan another model download.

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

- a callable compatible local transcription tool and a readable model.

The bundled transcription wrapper currently supports the standalone
`macparakeet-cli`, the CLI bundled in `/Applications/MacParakeet.app`, and
`whisper.cpp`. A compatible external adapter may also be used when explicitly
configured. Before installing anything, the agent should quietly inspect the
backend's own model listing and common local locations such as the project
`models/` directory and
`~/Library/Application Support/FluidAudio/Models/`. These are discovery hints,
not a fixed list of supported model names or versions.

When both a callable tool and a compatible model are ready, reuse them without
another speech-model download. A model directory without a callable tool is a
reusable asset, but not a ready automatic transcription path. In that case,
offer once to help install a compatible local tool or let the user provide a
timestamped transcript from an existing application. Do not replace the model
automatically. When the wrapper invokes MacParakeet, it disables telemetry for
that process and uses `--no-history`.

## Safe setup behavior

Run a read-only check first:

```bash
./scripts/setup-macos
```

The setup script reports only the backends it can install or call itself. Its
fallback proposal is not evidence that no compatible model exists elsewhere.
Review any discovered external models before accepting the plan.

Install the approved core dependencies and at most one selected model only
after reviewing the requested changes:

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
