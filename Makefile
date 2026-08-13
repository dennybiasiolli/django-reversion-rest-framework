style-fix:
	uv run --frozen ruff check --fix .
	uv run --frozen ruff format .

style-check:
	uv run --frozen ruff check .
	uv run --frozen ruff format --check .

test:
	uv run --frozen python tests/manage.py test tests

test-coverage:
	uv run --frozen coverage run tests/manage.py test tests
	uv run --frozen coverage report -m
	uv run --frozen coverage html
	uv run --frozen coverage xml

clean:
	rm -rf dist/ docs/_build/

build: clean
	uv build

publish: build
	uv publish

publish-test: build
	uv publish --publish-url https://test.pypi.org/legacy/
