#!/usr/bin/env python3
"""Deterministic preparation pipeline for transcript-led video review."""

from __future__ import annotations

import argparse
import html
import json
import re
import shutil
import subprocess
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path


TIMESTAMP_RE = re.compile(
    r"(?P<start>\d{2}:\d{2}(?::\d{2})?[.,]\d{3})\s+-->\s+"
    r"(?P<end>\d{2}:\d{2}(?::\d{2})?[.,]\d{3})"
)
VTT_SPEAKER_RE = re.compile(r"<v(?:\.[^ >]+)?\s+([^>]+)>", re.IGNORECASE)
KEYWORD_PROFILE_DIR = Path(__file__).parents[1] / "keyword_profiles"
DEFAULT_REPORT_NAME = "Video Findings.md"
DEFAULT_MATERIAL_DIR = "material"


@dataclass
class Cue:
    start: float
    end: float
    text: str
    speaker: str | None = None


@dataclass
class Candidate:
    id: str
    confidence: str
    reason: str
    excerpts: list[str] = field(default_factory=list)
    source_ranges: list[str] = field(default_factory=list)
    windows: list[dict[str, float]] = field(default_factory=list)
    frames: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class KeywordProfile:
    name: str
    strong_patterns: tuple[str, ...]
    expectation_patterns: tuple[str, ...]
    stopwords: frozenset[str]


def select_report_language(
    current_instruction: str | None = None,
    known_user_preference: str | None = None,
    request_language: str | None = None,
    transcript_language: str | None = None,
) -> str:
    """Resolve report language without treating transcript language as user intent."""
    for value in (
        current_instruction,
        request_language,
        known_user_preference,
        transcript_language,
    ):
        if value and value.strip():
            return value.strip()
    raise ValueError("A report language could not be resolved from the available context.")


def load_keyword_profile(value: str | Path | None = "en") -> KeywordProfile | None:
    """Load an optional heuristic profile; semantic AI review remains authoritative."""
    if value is None or str(value).lower() == "none":
        return None
    supplied = Path(value)
    path = supplied if supplied.is_file() else KEYWORD_PROFILE_DIR / f"{value}.json"
    if not path.is_file():
        raise ValueError(f"Keyword profile not found: {value}")
    payload = json.loads(path.read_text(encoding="utf-8"))
    try:
        return KeywordProfile(
            name=str(payload["name"]),
            strong_patterns=tuple(payload["strong_patterns"]),
            expectation_patterns=tuple(payload["expectation_patterns"]),
            stopwords=frozenset(word.lower() for word in payload.get("stopwords", [])),
        )
    except (KeyError, TypeError) as error:
        raise ValueError(f"Invalid keyword profile: {path}") from error


def timestamp_to_seconds(value: str) -> float:
    parts = value.replace(",", ".").split(":")
    if len(parts) == 2:
        minutes, seconds = parts
        return int(minutes) * 60 + float(seconds)
    hours, minutes, seconds = parts
    return int(hours) * 3600 + int(minutes) * 60 + float(seconds)


def format_timestamp(seconds: float) -> str:
    milliseconds = max(0, round(seconds * 1000))
    hours, remainder = divmod(milliseconds, 3_600_000)
    minutes, remainder = divmod(remainder, 60_000)
    secs, millis = divmod(remainder, 1000)
    return f"{hours:02d}:{minutes:02d}:{secs:02d}.{millis:03d}"


def parse_transcript(path: Path) -> list[Cue]:
    lines = path.read_text(encoding="utf-8-sig").splitlines()
    cues: list[Cue] = []
    index = 0
    while index < len(lines):
        match = TIMESTAMP_RE.search(lines[index])
        if not match:
            index += 1
            continue
        start = timestamp_to_seconds(match.group("start"))
        end = timestamp_to_seconds(match.group("end"))
        index += 1
        text_lines: list[str] = []
        while index < len(lines) and lines[index].strip():
            text_lines.append(lines[index].strip())
            index += 1
        raw = " ".join(text_lines)
        speaker_match = VTT_SPEAKER_RE.search(raw)
        speaker = html.unescape(speaker_match.group(1)).strip() if speaker_match else None
        clean = html.unescape(re.sub(r"<[^>]+>", "", raw)).strip()
        if clean:
            cues.append(Cue(start, end, clean, speaker))
    if not cues:
        raise ValueError(f"No timestamped cues found in {path}")
    return cues


def cue_kind(text: str, profile: KeywordProfile) -> tuple[str, str] | None:
    lowered = text.lower()
    if any(re.search(pattern, lowered) for pattern in profile.strong_patterns):
        return ("High", "concrete problem language")
    if any(re.search(pattern, lowered) for pattern in profile.expectation_patterns):
        return ("Medium", "reviewer expectation")
    return None


def content_terms(text: str, profile: KeywordProfile) -> set[str]:
    words = set(re.findall(r"[^\W\d_][\w-]{2,}", text.lower(), re.UNICODE))
    return words - profile.stopwords


def related(left: Candidate, cue: Cue, profile: KeywordProfile) -> bool:
    left_terms = content_terms(" ".join(left.excerpts), profile)
    right_terms = content_terms(cue.text, profile)
    latest_end = max(window["end"] for window in left.windows)
    return bool(left_terms & right_terms) and cue.start - latest_end <= 30


def detect_candidates(
    cues: list[Cue],
    padding: float = 2.0,
    keyword_profile: str | Path | KeywordProfile | None = "en",
) -> list[Candidate]:
    profile = (
        keyword_profile
        if isinstance(keyword_profile, KeywordProfile)
        else load_keyword_profile(keyword_profile)
    )
    if profile is None:
        return []
    candidates: list[Candidate] = []
    for cue in cues:
        kind = cue_kind(cue.text, profile)
        if not kind:
            continue
        confidence, reason = kind
        merge_target = next(
            (item for item in candidates if related(item, cue, profile)), None
        )
        source_range = f"{format_timestamp(cue.start)}–{format_timestamp(cue.end)}"
        window = {"start": max(0.0, cue.start - padding), "end": cue.end + padding}
        if merge_target:
            merge_target.excerpts.append(cue.text)
            merge_target.source_ranges.append(source_range)
            merge_target.windows.append(window)
            if confidence == "High":
                merge_target.confidence = "High"
            continue
        candidates.append(
            Candidate(
                id=f"finding-{len(candidates) + 1:03d}",
                confidence=confidence,
                reason=reason,
                excerpts=[cue.text],
                source_ranges=[source_range],
                windows=[window],
            )
        )
    return candidates


def video_duration(video: Path) -> float:
    result = subprocess.run(
        [
            "ffprobe", "-v", "error", "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1", str(video),
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    return float(result.stdout.strip())


def extract_frames(
    video: Path,
    output: Path,
    candidate: Candidate,
    duration: float,
    frame_mode: str = "single",
) -> None:
    frame_dir = output / DEFAULT_MATERIAL_DIR
    frame_dir.mkdir(parents=True, exist_ok=True)
    safe_windows: list[dict[str, float]] = []
    for window in candidate.windows:
        safe_end = min(window["end"], max(0.0, duration - 0.04))
        safe_start = min(window["start"], safe_end)
        window["start"] = safe_start
        window["end"] = safe_end
        safe_windows.append(window)

    if frame_mode == "single":
        window = max(safe_windows, key=lambda item: item["end"] - item["start"])
        second = (window["start"] + window["end"]) / 2
        filename = f"{candidate.id}.jpg"
        destination = frame_dir / filename
        subprocess.run(
            [
                "ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
                "-ss", f"{second:.3f}", "-i", str(video), "-frames:v", "1",
                "-q:v", "2", str(destination),
            ],
            check=True,
        )
        candidate.frames.append(f"{DEFAULT_MATERIAL_DIR}/{filename}")
        return

    for window_number, window in enumerate(safe_windows, 1):
        safe_start = window["start"]
        safe_end = window["end"]
        points = {
            "start": safe_start,
            "middle": (safe_start + safe_end) / 2,
            "end": safe_end,
        }
        for label, second in points.items():
            filename = f"{candidate.id}-w{window_number:02d}-{label}.jpg"
            destination = frame_dir / filename
            subprocess.run(
                [
                    "ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
                    "-ss", f"{second:.3f}", "-i", str(video), "-frames:v", "1",
                    "-q:v", "2", str(destination),
                ],
                check=True,
            )
            candidate.frames.append(f"{DEFAULT_MATERIAL_DIR}/{filename}")


def render_report(
    source: str,
    candidates: list[Candidate],
    source_path: str | None = None,
) -> str:
    blocks: list[str] = []
    for number, candidate in enumerate(candidates, 1):
        quote = " ".join(candidate.excerpts)
        images = "\n\n".join(f"![Evidence candidate]({path})" for path in candidate.frames)
        watch_from = min(window["start"] for window in candidate.windows)
        heading_timestamp = (
            candidate.source_ranges[0].split("–", 1)[0]
            if candidate.source_ranges
            else format_timestamp(watch_from)
        )
        representative_time = (
            max(candidate.windows, key=lambda item: item["end"] - item["start"])["start"]
            + max(candidate.windows, key=lambda item: item["end"] - item["start"])["end"]
        ) / 2
        image_caption = (
            f"*Image evidence · {format_timestamp(representative_time)} — "
            "Representative frame from the interval associated with the "
            "reviewer's comment.*"
        )
        blocks.append(
            f"## {heading_timestamp} — Candidate finding {number}\n\n"
            f"The reviewer comments: “{quote}”\n\n"
            f"{images or 'No video supplied.'}\n\n"
            f"{image_caption if images else ''}\n"
        )
    return (
        "# Video Findings\n\n"
        f"**Source:** {source}  \n"
        + (f"**Original video:** `{source_path}`  \n" if source_path else "")
        + f"**Generated:** {datetime.now(timezone.utc).isoformat()}  \n"
        "*Automatically prepared transcript-led overview.*\n\n"
        "## Summary\n\n"
        f"{len(candidates)} transcript-led candidate group(s) were found.\n\n"
        "## Findings\n\n"
        + ("\n\n".join(blocks) if blocks else "No transcript-led candidates found.")
        + "\n"
    )


def render_transcript(source: str, cues: list[Cue]) -> str:
    blocks: list[str] = []
    for cue in cues:
        speaker = f" · **{cue.speaker}**" if cue.speaker else ""
        blocks.append(
            f"**{format_timestamp(cue.start)}–{format_timestamp(cue.end)}**"
            f"{speaker}\n\n{cue.text}"
        )
    return (
        "# Full timestamped transcript\n\n"
        f"**Source:** {source}  \n"
        f"**Generated:** {datetime.now(timezone.utc).isoformat()}  \n"
        "**Coverage:** Every timestamped cue from the source transcript\n\n"
        "This transcript is the reusable source for reports and other derived "
        "artifacts. It preserves the source language and does not add product "
        "context.\n\n"
        + "\n\n".join(blocks)
        + "\n"
    )


def prepare(args: argparse.Namespace) -> int:
    transcript = Path(args.transcript).resolve()
    output = Path(args.output).resolve()
    video = Path(args.video).resolve() if args.video else None
    output.mkdir(parents=True, exist_ok=True)
    material = output / DEFAULT_MATERIAL_DIR
    material.mkdir(parents=True, exist_ok=True)
    cues = parse_transcript(transcript)
    transcript_copy = material / f"transcript-source{transcript.suffix.lower()}"
    if transcript != transcript_copy:
        shutil.copy2(transcript, transcript_copy)
    cue_payload = {
        "schema_version": 1,
        "source_transcript": str(transcript),
        "source_transcript_file": transcript_copy.name,
        "cues": [asdict(cue) for cue in cues],
    }
    (material / "transcript-cues.json").write_text(
        json.dumps(cue_payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    (material / "transcript.md").write_text(
        render_transcript(transcript.name, cues), encoding="utf-8"
    )
    keyword_profile = getattr(args, "keyword_profile", "en")
    profile = load_keyword_profile(keyword_profile)
    candidates = detect_candidates(cues, args.padding, profile)
    if video:
        duration = video_duration(video)
        for candidate in candidates:
            extract_frames(
                video,
                output,
                candidate,
                duration,
                getattr(args, "frame_mode", "single"),
            )
    payload = {
        "schema_version": 1,
        "source_transcript": str(transcript),
        "source_video": str(video) if video else None,
        "keyword_profile": profile.name if profile else None,
        "candidates": [asdict(item) for item in candidates],
    }
    (material / "candidates.json").write_text(
        json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    (output / DEFAULT_REPORT_NAME).write_text(
        render_report(
            video.name if video else transcript.name,
            candidates,
            str(video) if video else None,
        ),
        encoding="utf-8",
    )
    print(
        f"Prepared {len(cues)} transcript cue(s) and "
        f"{len(candidates)} heuristic candidate group(s) in {output}"
    )
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)
    command = subparsers.add_parser("prepare", help="prepare candidate windows and evidence")
    command.add_argument("--transcript", required=True, help="VTT or SRT transcript")
    command.add_argument("--video", help="optional MP4/MOV recording")
    command.add_argument("--output", required=True, help="output directory")
    command.add_argument("--padding", type=float, default=2.0, help="seconds around cues")
    command.add_argument(
        "--keyword-profile",
        default="en",
        help="optional built-in profile (en/de), JSON profile path, or none",
    )
    command.add_argument(
        "--frame-mode",
        choices=("single", "dense"),
        default="single",
        help="one representative image per heuristic lead (default) or three per window",
    )
    command.set_defaults(handler=prepare)
    return parser


def main() -> int:
    args = build_parser().parse_args()
    return args.handler(args)


if __name__ == "__main__":
    raise SystemExit(main())
