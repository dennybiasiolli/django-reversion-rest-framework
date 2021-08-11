pyenv-init:
	pyenv install 3.9.5
	pyenv virtualenv 3.9.5 django-reversion-rest-framework
	pyenv local django-reversion-rest-framework

test:
	python tests/manage.py test tests

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
