pyenv-init:
	pyenv install 3.11.6
	pyenv virtualenv 3.11.6 django-reversion-rest-framework
	pyenv local django-reversion-rest-framework

style-fix:
	isort .
	black .
	flake8

style-check:
	pylint --errors-only --recursive=y src
	pylint --load-plugins pylint_django --django-settings-module=test_project.settings --errors-only --recursive=y tests
	isort --check-only .
	black --check --diff .
	flake8

test:
	python tests/manage.py test tests

test-coverage:
	coverage run tests/manage.py test tests
	coverage report -m
	coverage html
	coverage xml

build:
	rm -rf dist
	pip install --upgrade build
	python -m build

publish-test:
	pip install --upgrade twine
	python -m twine upload --repository testpypi dist/*

publish:
	pip install --upgrade twine
	python -m twine upload dist/*
