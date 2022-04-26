.PHONY: tests doc clean lint quick_tests
PROJECT=ghtc

lint:
	mypy --show-error-codes --ignore-missing-imports $(PROJECT)
	flake8 --max-line-length 88 --ignore=D100,D101,D102,D103,D104,D107,D106,D105,W503,E203 $(PROJECT)
	black --check $(PROJECT)

tests: lint
	export PYTHONPATH=".:${PYTHONPATH}"; pytest

black:
	black $(PROJECT)

coverage:
	export PYTHONPATH=".:${PYTHONPATH}"; pytest --cov=$(PROJECT) tests/
	export PYTHONPATH=".:${PYTHONPATH}"; pytest --cov=$(PROJECT) --cov-report=html tests/
