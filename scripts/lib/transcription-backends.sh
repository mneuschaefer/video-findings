#!/usr/bin/env bash

vf_find_macparakeet_cli() {
  if [[ -n "${VIDEO_FINDINGS_MACPARAKEET_CLI:-}" && -x "${VIDEO_FINDINGS_MACPARAKEET_CLI}" ]]; then
    printf '%s\n' "${VIDEO_FINDINGS_MACPARAKEET_CLI}"
    return 0
  fi
  if command -v macparakeet-cli >/dev/null 2>&1; then
    command -v macparakeet-cli
    return 0
  fi
  local app_cli="/Applications/MacParakeet.app/Contents/MacOS/macparakeet-cli"
  if [[ -x "$app_cli" ]]; then
    printf '%s\n' "$app_cli"
    return 0
  fi
  return 1
}

vf_macparakeet_model() {
  local cli=$1
  if command -v python3 >/dev/null 2>&1; then
    DO_NOT_TRACK=1 MACPARAKEET_TELEMETRY=0 "$cli" models list --json 2>/dev/null | python3 -c '
import json, sys

try:
    models = json.load(sys.stdin)
except (json.JSONDecodeError, OSError):
    raise SystemExit(1)

installed = [
    item for item in models
    if item.get("engine") == "parakeet" and item.get("installed")
]
selected = next((item for item in installed if item.get("selected")), None)
if selected:
    print(selected.get("variant") or selected.get("id", "").removeprefix("parakeet-"))
    raise SystemExit(0)

for preferred in ("v3", "v2", "unified"):
    match = next((item for item in installed if item.get("variant") == preferred), None)
    if match:
        print(preferred)
        raise SystemExit(0)

raise SystemExit(1)
'
    return $?
  fi

  DO_NOT_TRACK=1 MACPARAKEET_TELEMETRY=0 "$cli" models list 2>/dev/null | awk '
    /^\* parakeet-(v3|v2|unified)/ && $NF == "yes" {
      variant = $2
      sub(/^parakeet-/, "", variant)
      found = 1
      print variant
      exit
    }
    /^  parakeet-v3/ && $NF == "yes" { fallback = "v3" }
    /^  parakeet-v2/ && $NF == "yes" && fallback == "" { fallback = "v2" }
    /^  parakeet-unified/ && $NF == "yes" && fallback == "" { fallback = "unified" }
    END { if (!found && fallback != "") print fallback }
  '
}

vf_find_whisper_cli() {
  command -v whisper-cli 2>/dev/null
}

vf_whisper_model_path() {
  local project_dir=$1
  printf '%s\n' "${VIDEO_FINDINGS_MODEL_PATH:-$project_dir/models/ggml-base.bin}"
}
