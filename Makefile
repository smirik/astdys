test:
	poetry run flake8 --count
	poetry run black . --check
	poetry run pytest -v tests

test-only:
	poetry run pytest -v tests

publish-test:
	poetry build
	poetry config repositories.testpypi https://test.pypi.org/legacy/
	poetry publish -r testpypi

publish:
	poetry publish --build

clean:
	rm -f cache/allnum.cat
	rm -f cache/solar.bin
	rm -f cache/*.csv
	rm -f cache/*.png

cache-clear:
	rm -f cache/*.csv
	rm -f cache/*.png
