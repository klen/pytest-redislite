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

VPART	?= minor
MAIN_BRANCH = master
STAGE_BRANCH = develop

.PHONY: release
# target: release - Bump version
release:
	git checkout $(MAIN_BRANCH)
	git pull
	git checkout $(STAGE_BRANCH)
	git pull
	uvx bump-my-version bump $(VPART)
	uv lock
	@VERSION="$$(uv version --short)"; \
		{ \
			printf 'build(release): %s\n\n' "$$VERSION"; \
			printf 'Changes:\n\n'; \
			git log --oneline --pretty=format:'%s [%an]' $(MAIN_BRANCH)..$(STAGE_BRANCH) | grep -Evi 'github|^Merge' || true; \
		} | git commit -a -F -
	git checkout $(MAIN_BRANCH)
	git merge $(STAGE_BRANCH)
	git checkout $(STAGE_BRANCH)
	git merge $(MAIN_BRANCH)
	@VERSION="$$(uv version --short)"; \
		git tag -a "$$VERSION" -m "$$VERSION"; \
		git push --atomic origin $(STAGE_BRANCH) $(MAIN_BRANCH) "refs/tags/$$VERSION"
	@echo "Release process complete for `uv version --short`"

.PHONY: minor
minor: release

.PHONY: patch
patch:
	make release VPART=patch

.PHONY: major
major:
	make release VPART=major

version v:
	uv version --short
