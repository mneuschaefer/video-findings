import importlib.util
import json
import os
import subprocess
import tempfile
import unittest
from pathlib import Path


MODULE_PATH = Path(__file__).parents[1] / "src" / "video_findings.py"
SPEC = importlib.util.spec_from_file_location("video_findings", MODULE_PATH)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader
import sys
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)


class PipelineTests(unittest.TestCase):
    def test_parses_vtt_and_strips_tags(self):
        content = "WEBVTT\n\n00:00:01.000 --> 00:00:02.500\n<b>No response</b>\n"
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "sample.vtt"
            path.write_text(content, encoding="utf-8")
            cues = MODULE.parse_transcript(path)
        self.assertEqual(len(cues), 1)
        self.assertEqual(cues[0].text, "No response")
        self.assertEqual(cues[0].start, 1.0)

    def test_parses_srt_numbered_blocks(self):
        content = "1\n00:00:03,000 --> 00:00:04,500\nNothing happens.\n"
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "sample.srt"
            path.write_text(content, encoding="utf-8")
            cues = MODULE.parse_transcript(path)
        self.assertEqual(cues[0].end, 4.5)

    def test_parses_teams_style_vtt_speaker_and_settings(self):
        content = (
            "WEBVTT\n\n"
            "a1\n"
            "00:00:03.000 --> 00:00:05.000 align:start position:0%\n"
            "<v Reviewer>Nothing happens after Continue.</v>\n"
        )
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "teams.vtt"
            path.write_text(content, encoding="utf-8")
            cues = MODULE.parse_transcript(path)
        self.assertEqual(cues[0].text, "Nothing happens after Continue.")

    def test_detects_spoken_usability_irritation(self):
        cues = [MODULE.Cue(2.0, 4.0, "This is not very intuitive for me.")]
        candidate = MODULE.detect_candidates(cues)[0]
        self.assertEqual(candidate.confidence, "High")

    def test_demo_has_two_groups_and_merges_repeat(self):
        transcript = Path(__file__).parents[1] / "examples" / "sample-transcript.vtt"
        candidates = MODULE.detect_candidates(MODULE.parse_transcript(transcript))
        self.assertEqual(len(candidates), 2)
        self.assertEqual(len(candidates[0].source_ranges), 2)
        self.assertEqual(len(candidates[0].windows), 2)
        self.assertEqual(candidates[0].confidence, "High")
        self.assertEqual(candidates[1].confidence, "Medium")

    def test_padding_never_creates_negative_start(self):
        cues = [MODULE.Cue(0.25, 1.0, "Nothing happens")]
        candidate = MODULE.detect_candidates(cues, padding=2.0)[0]
        self.assertEqual(candidate.windows[0]["start"], 0.0)

    def test_prepare_preserves_all_multilingual_cues(self):
        content = (
            "WEBVTT\n\n"
            "00:00:01.000 --> 00:00:02.000\n"
            "Hier reagiert die Schaltfläche nicht.\n\n"
            "00:00:03.000 --> 00:00:04.000\n"
            "ここでは画面が変わりません。\n\n"
            "00:00:05.000 --> 00:00:06.000\n"
            "هنا لا تتغير الشاشة.\n"
        )
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            transcript = root / "multilingual.vtt"
            output = root / "output"
            transcript.write_text(content, encoding="utf-8")
            args = type(
                "Args",
                (),
                {"transcript": str(transcript), "output": str(output), "video": None, "padding": 2.0},
            )()
            MODULE.prepare(args)
            payload = json.loads((output / "transcript-cues.json").read_text(encoding="utf-8"))
        self.assertEqual(len(payload["cues"]), 3)
        self.assertEqual(payload["cues"][0]["text"], "Hier reagiert die Schaltfläche nicht.")
        self.assertEqual(payload["cues"][1]["text"], "ここでは画面が変わりません。")
        self.assertEqual(payload["cues"][2]["text"], "هنا لا تتغير الشاشة.")

    def test_user_facing_scripts_are_executable(self):
        scripts = Path(__file__).parents[1] / "scripts"
        for name in (
            "analyze-recording",
            "check-environment",
            "extract-audio",
            "extract-frames",
            "package-release",
            "setup-macos",
            "transcribe-local",
        ):
            self.assertTrue(os.access(scripts / name, os.X_OK), name)

    def test_shell_scripts_have_valid_syntax(self):
        root = Path(__file__).parents[1]
        scripts = list((root / "scripts").glob("*"))
        scripts += list((root / "scripts" / "lib").glob("*.sh"))
        for script in scripts:
            if script.is_file():
                subprocess.run(["bash", "-n", script], check=True)


if __name__ == "__main__":
    unittest.main()
