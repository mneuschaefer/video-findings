import importlib.util
import json
import os
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest import mock


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
        self.assertEqual(cues[0].speaker, "Reviewer")

    def test_detects_spoken_usability_irritation(self):
        cues = [MODULE.Cue(2.0, 4.0, "This is not very intuitive for me.")]
        candidate = MODULE.detect_candidates(cues)[0]
        self.assertEqual(candidate.confidence, "High")

    def test_german_keyword_profile_is_an_optional_routing_aid(self):
        cues = [MODULE.Cue(2.0, 4.0, "Hier reagiert die Schaltfläche nicht.")]
        candidates = MODULE.detect_candidates(cues, keyword_profile="de")
        self.assertEqual(len(candidates), 1)
        self.assertEqual(candidates[0].confidence, "High")
        self.assertEqual(MODULE.detect_candidates(cues, keyword_profile=None), [])

    def test_explicit_report_language_overrides_german_transcript(self):
        report_language = MODULE.select_report_language(
            current_instruction="English",
            known_user_preference="German",
            request_language="German",
            transcript_language="German",
        )
        self.assertEqual(report_language, "English")

    def test_prompt_language_precedes_known_preference_and_transcript(self):
        self.assertEqual(
            MODULE.select_report_language(
                known_user_preference="English",
                request_language="German",
                transcript_language="German",
            ),
            "German",
        )
        self.assertEqual(
            MODULE.select_report_language(
                request_language="German", transcript_language="English"
            ),
            "German",
        )

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
            payload = json.loads(
                (output / "material" / "transcript-cues.json").read_text(encoding="utf-8")
            )
            readable = (output / "material" / "transcript.md").read_text(encoding="utf-8")
            preserved_exists = (output / "material" / "transcript-source.vtt").is_file()
        self.assertEqual(len(payload["cues"]), 3)
        self.assertEqual(payload["cues"][0]["text"], "Hier reagiert die Schaltfläche nicht.")
        self.assertEqual(payload["cues"][1]["text"], "ここでは画面が変わりません。")
        self.assertEqual(payload["cues"][2]["text"], "هنا لا تتغير الشاشة.")
        self.assertIn("00:00:01.000–00:00:02.000", readable)
        self.assertIn("Hier reagiert die Schaltfläche nicht.", readable)
        self.assertIn("ここでは画面が変わりません。", readable)
        self.assertIn("هنا لا تتغير الشاشة.", readable)
        self.assertTrue(preserved_exists)

    def test_timestamped_transcript_preserves_speaker_without_inventing_context(self):
        cues = [MODULE.Cue(1.0, 2.5, "The button did not respond.", "Reviewer")]
        transcript = MODULE.render_transcript("review.vtt", cues)
        self.assertIn("**00:00:01.000–00:00:02.500** · **Reviewer**", transcript)
        self.assertIn("The button did not respond.", transcript)
        self.assertNotIn("Northstar", transcript)

    def test_single_frame_mode_writes_one_image_per_candidate(self):
        candidate = MODULE.Candidate(
            id="finding-001",
            confidence="High",
            reason="test",
            windows=[{"start": 1.0, "end": 4.0}, {"start": 10.0, "end": 12.0}],
        )
        with tempfile.TemporaryDirectory() as directory, mock.patch.object(
            MODULE.subprocess, "run"
        ) as run:
            MODULE.extract_frames(
                Path("video.mp4"), Path(directory), candidate, 20.0, "single"
            )
        self.assertEqual(candidate.frames, ["material/finding-001.jpg"])
        run.assert_called_once()

    def test_dense_frame_mode_remains_available(self):
        candidate = MODULE.Candidate(
            id="finding-001",
            confidence="High",
            reason="test",
            windows=[{"start": 1.0, "end": 4.0}, {"start": 10.0, "end": 12.0}],
        )
        with tempfile.TemporaryDirectory() as directory, mock.patch.object(
            MODULE.subprocess, "run"
        ) as run:
            MODULE.extract_frames(
                Path("video.mp4"), Path(directory), candidate, 20.0, "dense"
            )
        self.assertEqual(len(candidate.frames), 6)
        self.assertEqual(run.call_count, 6)

    def test_report_links_original_video_at_exact_start_time(self):
        candidate = MODULE.Candidate(
            id="finding-001",
            confidence="High",
            reason="test",
            windows=[{"start": 22.72, "end": 31.52}],
            frames=["material/finding-001.jpg"],
        )
        report = MODULE.render_report(
            "review.mp4", [candidate], "../../review.mp4"
        )
        self.assertIn("../../review.mp4#t=22.720", report)
        self.assertIn("continue from 00:00:22.720", report)
        self.assertIn("## 00:00:22.720 — Candidate finding 1", report)
        self.assertIn("*Image evidence · 00:00:27.120 —", report)

    def test_default_output_root_contains_one_dossier_and_material_folder(self):
        content = "WEBVTT\n\n00:00:01.000 --> 00:00:02.000\nNothing happens.\n"
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            transcript = root / "sample.vtt"
            output = root / "output"
            transcript.write_text(content, encoding="utf-8")
            args = type(
                "Args",
                (),
                {
                    "transcript": str(transcript),
                    "output": str(output),
                    "video": None,
                    "padding": 2.0,
                    "keyword_profile": "en",
                },
            )()
            MODULE.prepare(args)
            root_entries = sorted(path.name for path in output.iterdir())
            material_entries = sorted(path.name for path in (output / "material").iterdir())
        self.assertEqual(root_entries, ["Video Findings.md", "material"])
        self.assertIn("candidates.json", material_entries)
        self.assertIn("transcript-cues.json", material_entries)
        self.assertIn("transcript-source.vtt", material_entries)
        self.assertIn("transcript.md", material_entries)

    def test_user_facing_scripts_are_executable(self):
        scripts = Path(__file__).parents[1] / "scripts"
        for name in (
            "analyze-recording",
            "build-motion-index",
            "check-environment",
            "extract-audio",
            "extract-clip",
            "extract-evidence",
            "extract-frame",
            "extract-frames",
            "package-release",
            "measure-interval",
            "setup-macos",
            "transcribe-local",
        ):
            self.assertTrue(os.access(scripts / name, os.X_OK), name)

    def test_measure_interval_writes_latency_and_stabilization(self):
        root = Path(__file__).parents[1]
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "measurement.json"
            subprocess.run(
                [
                    str(root / "scripts" / "measure-interval"),
                    "--action", "00:00:12.400",
                    "--response", "13.050",
                    "--stable", "13.600",
                    "--output", str(output),
                ],
                check=True,
                capture_output=True,
                text=True,
            )
            payload = json.loads(output.read_text(encoding="utf-8"))
        self.assertEqual(payload["latency_seconds"], 0.65)
        self.assertEqual(payload["stabilization_seconds"], 0.55)

    def test_script_syntax_is_checked_from_shebang(self):
        root = Path(__file__).parents[1]
        scripts = list((root / "scripts").glob("*"))
        scripts += list((root / "scripts" / "lib").glob("*.sh"))
        for script in scripts:
            if not script.is_file():
                continue
            first_line = script.read_text(encoding="utf-8").splitlines()[0]
            if "bash" in first_line or first_line.endswith("/sh"):
                subprocess.run(["bash", "-n", script], check=True)
            elif "python" in first_line:
                subprocess.run([sys.executable, "-m", "py_compile", script], check=True)

    def test_setup_plans_one_recommended_model_and_allows_override(self):
        root = Path(__file__).parents[1]
        with tempfile.TemporaryDirectory() as directory:
            temporary = Path(directory)
            fake_parakeet = temporary / "macparakeet-cli"
            fake_parakeet.write_text(
                "#!/bin/sh\nprintf '%s\\n' "
                "'[{\"engine\":\"parakeet\",\"installed\":false,"
                "\"variant\":\"v3\",\"id\":\"parakeet-v3\","
                "\"size\":\"~465 MB\"}]'\n",
                encoding="utf-8",
            )
            fake_parakeet.chmod(0o755)
            environment = os.environ.copy()
            environment["VIDEO_FINDINGS_MACPARAKEET_CLI"] = str(fake_parakeet)
            environment["VIDEO_FINDINGS_MODEL_PATH"] = str(temporary / "missing.bin")

            recommended = subprocess.run(
                [str(root / "scripts" / "setup-macos")],
                check=True,
                capture_output=True,
                text=True,
                env=environment,
            )
            self.assertIn("recommended parakeet-v3", recommended.stdout)
            self.assertIn("download parakeet-v3 (~465 MB)", recommended.stdout)
            self.assertEqual(recommended.stdout.count("  Model:         download"), 1)

            explicit = subprocess.run(
                [
                    str(root / "scripts" / "setup-macos"),
                    "--backend",
                    "whisper",
                ],
                check=True,
                capture_output=True,
                text=True,
                env=environment,
            )
            self.assertIn("explicitly selected ggml-base.bin", explicit.stdout)
            self.assertIn("Model:         download", explicit.stdout)
            self.assertIn("142 MiB", explicit.stdout)

    def test_explicit_newer_installed_parakeet_variant_can_be_selected(self):
        root = Path(__file__).parents[1]
        with tempfile.TemporaryDirectory() as directory:
            fake_parakeet = Path(directory) / "macparakeet-cli"
            fake_parakeet.write_text(
                "#!/bin/sh\nprintf '%s\\n' "
                "'[{\"engine\":\"parakeet\",\"installed\":true,"
                "\"variant\":\"v4\",\"id\":\"parakeet-v4\"}]'\n",
                encoding="utf-8",
            )
            fake_parakeet.chmod(0o755)
            environment = os.environ.copy()
            environment["VIDEO_FINDINGS_PARAKEET_MODEL"] = "v4"
            result = subprocess.run(
                [
                    "bash",
                    "-c",
                    'source "$1"; vf_macparakeet_model "$2"',
                    "test",
                    str(root / "scripts" / "lib" / "transcription-backends.sh"),
                    str(fake_parakeet),
                ],
                check=True,
                capture_output=True,
                text=True,
                env=environment,
            )
            self.assertEqual(result.stdout.strip(), "v4")


if __name__ == "__main__":
    unittest.main()
