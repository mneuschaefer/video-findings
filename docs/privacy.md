# Privacy

FFmpeg processing and the included CLI are local. Existing VTT/SRT files avoid
an unnecessary transcription step.

The end-to-end workflow is not automatically local. If a cloud transcription
service or cloud agent receives audio, transcript text, or screenshots, those
artifacts leave the machine and are subject to that provider's terms and data
handling. Obtain the necessary consent and remove sensitive data before upload.

Analysis commands perform no network calls and the package contains no
telemetry. `scripts/setup-macos --install` is the explicit exception: Homebrew
may fetch packages and the script downloads the selected Whisper model from the
official whisper.cpp model repository. No recording, transcript, frame, or
report is sent during setup.
