# Contributing guidelines

This package has been created using python 3.9.5.

## Creating environment with pyenv

```sh
pyenv install 3.9.5
pyenv virtualenv 3.9.5 django-reversion-rest-framework
pyenv local django-reversion-rest-framework
pip install -e .
pip install -r requirements_dev.txt
```

## Fixing code style

```sh
make style-fix
```


## Running tests

```sh
tests/manage.py test tests
# or
make style-check
make test
```


## Build the package

```sh
rm -rf dist
pip install --upgrade build
python -m build
```


## Publish test package

```sh
twine upload --repository testpypi dist/*
```


## Publish official package

```sh
twine upload dist/*
```
