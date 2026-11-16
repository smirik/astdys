install:
	uv sync

test: install
	uv run flake8 --count
	uv run black . --check
	uv run pytest -v tests

test-only:
	uv run pytest -v tests

build:
	rm -rf dist/
	uv build

# The PyPI token: UV_PUBLISH_TOKEN=pypi-... make publish (or --token)
publish-test: build
	uv publish --publish-url https://test.pypi.org/legacy/

publish: build
	uv publish

clean:
	rm -f cache/allnum.cat
	rm -f cache/solar.bin
	rm -f cache/*.csv
	rm -f cache/*.png

cache-clear:
	rm -f cache/*.csv
	rm -f cache/*.png
