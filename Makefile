.PHONY: check setup install test demo package clean

PYTHON ?= python3

check:
	./scripts/check-environment

setup:
	./scripts/setup-macos

install:
	./scripts/setup-macos --install

test:
	$(PYTHON) -m unittest discover -s tests -v

demo: check
	./scripts/generate-demo-video examples/generated/demo-review.mp4
	./scripts/analyze-recording \
		--video examples/generated/demo-review.mp4 \
		--transcript examples/sample-transcript.vtt \
		--output output/demo

package:
	./scripts/package-release

clean:
	rm -rf output/demo examples/generated __pycache__ src/__pycache__ tests/__pycache__
