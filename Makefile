.PHONY: setup
setup:
	@uv sync
	@uv run pre-commit install

.PHONY: test
t test: setup
	uv run pytest

.PHONY: lint
lint: setup
	uv run pyrefly check
	uv run ruff check --fix

.PHONY: clean
clean:
	rm -rf build/ dist/ *.egg-info
	find $(CURDIR) -name "*.py[co]" -delete
	find $(CURDIR) -name "*.orig" -delete
	find $(CURDIR) -name "__pycache__" | xargs rm -rf

VERSION	?= minor

.PHONY: version
version:
	uv run bump2version $(VERSION)
	git checkout master
	git pull
	git merge develop
	git checkout develop
	git push origin develop master
	git push --tags

.PHONY: minor
minor:
	make version VERSION=minor

.PHONY: patch
patch:
	make version VERSION=patch

.PHONY: major
major:
	make version VERSION=major

.PHONY: upload
upload: clean
	uv build
	uv publish
