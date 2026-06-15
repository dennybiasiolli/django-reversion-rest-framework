style-fix:
	uv run --frozen isort .
	uv run --frozen black .
	uv run --frozen flake8

style-check:
	uv run --frozen pylint --errors-only --recursive=y src
	uv run --frozen pylint --load-plugins pylint_django --django-settings-module=test_project.settings --errors-only --recursive=y tests
	uv run --frozen isort --check-only .
	uv run --frozen black --check --diff .
	uv run --frozen flake8

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
