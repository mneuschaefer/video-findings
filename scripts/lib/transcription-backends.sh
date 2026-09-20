#!/usr/bin/env bash

# A saved executable takes precedence over discovery. The file is data, not shell.
vf_configured_transcriber() {
  local root=$1
  if [[ -n "${VIDEO_FINDINGS_TRANSCRIBER_COMMAND:-}" ]]; then
    printf '%s\n' "$VIDEO_FINDINGS_TRANSCRIBER_COMMAND"
  elif [[ -f "$root/models/transcriber-path" ]]; then
    head -n 1 "$root/models/transcriber-path"
  fi
}

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
import json, os, sys

try:
    models = json.load(sys.stdin)
except (json.JSONDecodeError, OSError):
    raise SystemExit(1)

installed = [
    item for item in models
    if item.get("engine") == "parakeet" and item.get("installed")
]
requested = os.environ.get("VIDEO_FINDINGS_PARAKEET_MODEL")
if requested:
    match = next(
        (
            item for item in installed
            if requested in {item.get("variant"), item.get("id")}
        ),
        None,
    )
    if match:
        print(match.get("variant") or match.get("id", "").removeprefix("parakeet-"))
        raise SystemExit(0)
    raise SystemExit(1)

selected = next((item for item in installed if item.get("selected")), None)
if selected:
    print(selected.get("variant") or selected.get("id", "").removeprefix("parakeet-"))
    raise SystemExit(0)

for preferred in ("v3", "v2", "unified"):
    match = next((item for item in installed if item.get("variant") == preferred), None)
    if match:
        print(preferred)
        raise SystemExit(0)

if installed:
    item = installed[0]
    print(item.get("variant") or item.get("id", "").removeprefix("parakeet-"))
    raise SystemExit(0)

raise SystemExit(1)
'
    return $?
  fi

  DO_NOT_TRACK=1 MACPARAKEET_TELEMETRY=0 "$cli" models list 2>/dev/null | awk '
    $NF == "yes" {
      id = ($1 == "*" ? $2 : $1)
      variant = id
      sub(/^parakeet-/, "", variant)
      requested = ENVIRON["VIDEO_FINDINGS_PARAKEET_MODEL"]
      if (requested != "" && (requested == id || requested == variant)) {
        print variant
        found = 1
        exit
      }
      if (requested == "" && $1 == "*") {
        print variant
        found = 1
        exit
      }
      if (id == "parakeet-v3") preferred = "v3"
      else if (id == "parakeet-v2" && preferred == "") preferred = "v2"
      else if (id == "parakeet-unified" && preferred == "") preferred = "unified"
      if (any == "") any = variant
    }
    END {
      if (!found && ENVIRON["VIDEO_FINDINGS_PARAKEET_MODEL"] == "") {
        if (preferred != "") print preferred
        else if (any != "") print any
      }
    }
  '
}

vf_find_whisper_cli() {
  command -v whisper-cli 2>/dev/null
}

vf_macparakeet_model_size() {
  local cli=$1
  local requested=$2
  if command -v python3 >/dev/null 2>&1; then
    DO_NOT_TRACK=1 MACPARAKEET_TELEMETRY=0 "$cli" models list --json 2>/dev/null | \
      REQUESTED_MODEL="$requested" python3 -c '
import json, os, sys

requested = os.environ["REQUESTED_MODEL"]
models = json.load(sys.stdin)
match = next(
    (
        item for item in models
        if requested in {item.get("id"), item.get("variant")}
    ),
    None,
)
if not match:
    raise SystemExit(1)
print(match.get("size") or "size not reported by MacParakeet")
'
    return $?
  fi

  DO_NOT_TRACK=1 MACPARAKEET_TELEMETRY=0 "$cli" models list 2>/dev/null | \
    awk -v requested="$requested" '
      {
        id = ($1 == "*" ? $2 : $1)
        if (id == requested) {
          for (i = 1; i < NF; i++) {
            if ($i ~ /^~?[0-9.]+$/ && $(i + 1) ~ /^(MB|GB)$/) {
              print $i " " $(i + 1)
              exit
            }
          }
        }
      }
    '
}

vf_whisper_model_path() {
  local project_dir=$1
  printf '%s\n' "${VIDEO_FINDINGS_MODEL_PATH:-$project_dir/models/ggml-base.bin}"
}
