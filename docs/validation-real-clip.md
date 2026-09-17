# Real-clip validation

This document records the reproducible result of a temporary integration test.
The source video itself is not redistributed or included in release archives.

## Source

- Title: `3 Reasons to NOT use Obsidian`
- Channel: `Demetri Panici`
- URL: `https://www.youtube.com/watch?v=UvIhFWbpqN4`
- Temporary interval: approximately `00:03:34–00:03:58`
- Purpose: validate video-only local transcription and transcript-led candidate
  extraction against a real software-review segment discussing an interface
  irritation.

## Expected validation

The local transcription should preserve a statement that the interaction is
not intuitive or is an issue. The preparation pass should turn that language
into at least one candidate window and extract beginning/middle/end evidence
frames. A human must still decide whether the frames support a concrete finding
or only a subjective usability opinion.

During the first run, the Homebrew `whisper.cpp` Metal backend aborted on the
test Mac. The CPU-only retry completed successfully. This test therefore also
became the regression case for the automatic `--no-gpu` fallback.

The clip and downloaded captions belong in a temporary directory only. They
must not be committed, packaged, or presented as project-owned sample media.

## Result

- The setup installed the missing `whisper.cpp` dependency and downloaded the
  multilingual base model.
- The Metal backend failed on the test Mac; the CPU-only retry transcribed the
  clip successfully.
- The local transcript produced one high-signal candidate around the spoken
  usability irritation.
- The pipeline extracts one representative frame per candidate by default.
  Dense start/middle/end sampling remains available for timing diagnosis.
- Visual inspection showed an existing note followed by creation of a blank
  note. This supports the interaction context but does not prove a defect.
- The final classification is a possible onboarding/editor-discoverability
  concern while preserving the specific uncertainty in the description.

The downloaded video, clipped excerpt, transcript, frames, and generated report
were removed after the run. Only this result summary belongs to the project and
release package.
