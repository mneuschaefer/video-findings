#!/usr/bin/env python3
"""Deterministic preparation pipeline for transcript-led video review."""

from __future__ import annotations

import argparse
import html
import json
import re
import subprocess
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path


TIMESTAMP_RE = re.compile(
    r"(?P<start>\d{2}:\d{2}(?::\d{2})?[.,]\d{3})\s+-->\s+"
    r"(?P<end>\d{2}:\d{2}(?::\d{2})?[.,]\d{3})"
)
STRONG_PATTERNS = (
    r"\bnothing happens\b",
    r"\bno (?:visible )?response\b",
    r"\bdoes(?:n't| not) work\b",
    r"\b(?:error|broken|stuck|failed?)\b",
    r"\bcan(?:not|'t)\b",
    r"\b(?:not|isn't|is not) (?:very )?intuitive\b",
    r"\b(?:kind of an )?issue\b",
    r"\bconfus(?:ing|ed)\b",
    r"\bdoes(?:n't| not) make sense\b",
)
EXPECTATION_PATTERNS = (r"\bi expected\b", r"\bi would expect\b", r"\bshould\b")
STOPWORDS = {
    "again", "although", "back", "clicked", "click", "does", "from", "happens",
    "have", "into", "nothing", "response", "still", "that", "this", "visible",
    "with", "would", "expected", "expect", "there", "take", "although", "design",
}


@dataclass
class Cue:
    start: float
    end: float
    text: str


@dataclass
class Candidate:
    id: str
    confidence: str
    reason: str
    excerpts: list[str] = field(default_factory=list)
    source_ranges: list[str] = field(default_factory=list)
    windows: list[dict[str, float]] = field(default_factory=list)
    frames: list[str] = field(default_factory=list)


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
        clean = html.unescape(re.sub(r"<[^>]+>", "", raw)).strip()
        if clean:
            cues.append(Cue(start, end, clean))
    if not cues:
        raise ValueError(f"No timestamped cues found in {path}")
    return cues


def cue_kind(text: str) -> tuple[str, str] | None:
    lowered = text.lower()
    if any(re.search(pattern, lowered) for pattern in STRONG_PATTERNS):
        return ("High", "concrete problem language")
    if any(re.search(pattern, lowered) for pattern in EXPECTATION_PATTERNS):
        return ("Medium", "reviewer expectation")
    return None


def content_terms(text: str) -> set[str]:
    words = set(re.findall(r"[a-z][a-z-]{2,}", text.lower()))
    return words - STOPWORDS


def related(left: Candidate, cue: Cue) -> bool:
    left_terms = content_terms(" ".join(left.excerpts))
    right_terms = content_terms(cue.text)
    latest_end = max(window["end"] for window in left.windows)
    return bool(left_terms & right_terms) and cue.start - latest_end <= 30


def detect_candidates(cues: list[Cue], padding: float = 2.0) -> list[Candidate]:
    candidates: list[Candidate] = []
    for cue in cues:
        kind = cue_kind(cue.text)
        if not kind:
            continue
        confidence, reason = kind
        merge_target = next((item for item in candidates if related(item, cue)), None)
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


def extract_frames(video: Path, output: Path, candidate: Candidate, duration: float) -> None:
    frame_dir = output / "assets"
    frame_dir.mkdir(parents=True, exist_ok=True)
    for window_number, window in enumerate(candidate.windows, 1):
        safe_end = min(window["end"], max(0.0, duration - 0.04))
        safe_start = min(window["start"], safe_end)
        window["end"] = safe_end
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
            candidate.frames.append(f"assets/{filename}")


def render_report(source: str, candidates: list[Candidate]) -> str:
    blocks: list[str] = []
    for number, candidate in enumerate(candidates, 1):
        quote = "\n> ".join(candidate.excerpts)
        images = "\n\n".join(f"![Evidence candidate]({path})" for path in candidate.frames)
        windows = ", ".join(
            f"{format_timestamp(window['start'])}–{format_timestamp(window['end'])}"
            for window in candidate.windows
        )
        blocks.append(
            f"## {number}. Candidate finding\n\n"
            f"**Status:** Needs review  \n"
            f"**Confidence:** {candidate.confidence}  \n"
            f"**Candidate windows:** {windows}  \n"
            f"**Source ranges:** {', '.join(candidate.source_ranges)}\n\n"
            f"### Observation\n\nTo be verified against the recording.\n\n"
            f"### Reviewer expectation\n\nTo be separated from observed behavior.\n\n"
            f"### Transcript evidence\n\n> {quote}\n\n"
            f"### Visual evidence candidates\n\n{images or 'No video supplied.'}\n\n"
            f"### Suggested classification\n\n{candidate.reason}; interpretation pending.\n\n"
            f"### Human decision\n\n- [ ] Confirm as issue\n- [ ] Rewrite\n- [ ] Discard\n"
        )
    return (
        "# Recorded review findings\n\n"
        f"**Source:** {source}  \n"
        f"**Generated:** {datetime.now(timezone.utc).isoformat()}  \n"
        "**Status:** Draft — human review required\n\n"
        "## Summary\n\n"
        f"{len(candidates)} transcript-led candidate group(s). These are leads, not verified defects.\n\n"
        "## Findings\n\n"
        + ("\n\n".join(blocks) if blocks else "No transcript-led candidates found.")
        + "\n\n## Evaluation notes\n\n"
        "Transcript-led detection can miss purely visual issues. Inspect false positives, "
        "misses, and frame usefulness before publishing findings.\n"
    )


def prepare(args: argparse.Namespace) -> int:
    transcript = Path(args.transcript).resolve()
    output = Path(args.output).resolve()
    video = Path(args.video).resolve() if args.video else None
    output.mkdir(parents=True, exist_ok=True)
    cues = parse_transcript(transcript)
    candidates = detect_candidates(cues, args.padding)
    if video:
        duration = video_duration(video)
        for candidate in candidates:
            extract_frames(video, output, candidate, duration)
    payload = {
        "schema_version": 1,
        "source_transcript": str(transcript),
        "source_video": str(video) if video else None,
        "candidates": [asdict(item) for item in candidates],
    }
    (output / "candidates.json").write_text(
        json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    (output / "report.md").write_text(
        render_report(video.name if video else transcript.name, candidates), encoding="utf-8"
    )
    print(f"Prepared {len(candidates)} candidate group(s) in {output}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)
    command = subparsers.add_parser("prepare", help="prepare candidate windows and evidence")
    command.add_argument("--transcript", required=True, help="VTT or SRT transcript")
    command.add_argument("--video", help="optional MP4/MOV recording")
    command.add_argument("--output", required=True, help="output directory")
    command.add_argument("--padding", type=float, default=2.0, help="seconds around cues")
    command.set_defaults(handler=prepare)
    return parser


def main() -> int:
    args = build_parser().parse_args()
    return args.handler(args)


if __name__ == "__main__":
    raise SystemExit(main())
