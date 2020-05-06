install:
	pip install --user .

test:
	pytest tests

testfast:
	pytest -q -x --ff tests

.PHONY: install test testfast
