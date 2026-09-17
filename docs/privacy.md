# Privacy

FFmpeg processing and the included CLI are local. Existing VTT/SRT files avoid
an unnecessary transcription step.

The end-to-end workflow is not automatically local. If a cloud transcription
service or cloud agent receives audio, transcript text, or screenshots, those
artifacts leave the machine and are subject to that provider's terms and data
handling. Obtain the necessary consent and remove sensitive data before upload.

The package contains no telemetry. When it invokes an existing MacParakeet
installation, it disables MacParakeet telemetry for that process and uses
`--no-history`. `scripts/setup-macos --install` is the explicit network
exception: when dependencies are missing, Homebrew may fetch approved packages
and the fallback path may download the selected Whisper model from the official
whisper.cpp model repository. The read-only setup plan reports this before any
change. No recording, transcript, frame, or report is sent during setup.
