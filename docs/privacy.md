# Privacy

FFmpeg processing and the included CLI are local. Existing VTT/SRT files avoid
an unnecessary transcription step.

The end-to-end workflow is not automatically local. If a cloud transcription
service or cloud agent receives audio, transcript text, or screenshots, those
artifacts leave the machine and are subject to that provider's terms and data
handling. Obtain the necessary consent and remove sensitive data before upload.

The repository performs no network calls and contains no telemetry.

