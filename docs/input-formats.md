# Input formats

## QuickTime and macOS screen recordings

QuickTime Player and macOS Screenshot (`Shift-Command-5`) commonly create MOV
files. They can be used directly when the recording is saved locally and
contains the narration that should drive transcript search.

```bash
./scripts/analyze-recording \
  --video "/path/QuickTime Screen Recording.mov" \
  --output output/quicktime-review
```

If the recording has no microphone or system audio, local transcription cannot
recover reviewer intent. The deterministic media tools still work, but a
transcript-first finding pass needs a separate timestamped transcript.

## Downloaded Microsoft Teams recordings

Download the recording to the Mac first. This package does not connect to the
Teams API, SharePoint, or OneDrive.

Use a separately downloaded VTT/SRT when it begins at the same recording start:

```bash
./scripts/analyze-recording \
  --video "/path/Teams Review.mp4" \
  --transcript "/path/Teams Review.vtt" \
  --output output/teams-review
```

Teams-style VTT speaker tags and cue settings are accepted. If the transcript
was edited, clipped, or exported from a different version of the recording,
verify timestamp alignment before trusting screenshots.

Without a transcript, omit `--transcript`; local `whisper.cpp` transcription is
used.

## Other local recordings

MOV and MP4 are the supported public contract. FFmpeg may read additional
containers, but they are not part of the tested interface. Convert unusual
formats to H.264/AAC MP4 before reporting a portability bug.

