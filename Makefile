.PHONY: check test demo clean

PYTHON ?= python3

check:
	./scripts/check-environment

test:
	$(PYTHON) -m unittest discover -s tests -v

demo: check
	./scripts/generate-demo-video examples/generated/demo-review.mp4
	$(PYTHON) src/review_to_issues.py prepare \
		--video examples/generated/demo-review.mp4 \
		--transcript examples/sample-transcript.vtt \
		--output output/demo

clean:
	rm -rf output/demo examples/generated __pycache__ src/__pycache__ tests/__pycache__

