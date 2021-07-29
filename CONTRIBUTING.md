# Contributing guidelines

This package has been created using python 3.9.5.

## Creating environment with pyenv

```sh
pyenv install 3.9.5
pyenv virtualenv 3.9.5 django-reversion-rest-framework
pyenv local django-reversion-rest-framework
```

## Running tests

    ```sh
    tests/manage.py test tests
    ```


## Build the package

    ```sh
    rm -rf dist
    pip install --upgrade build
    python -m build
    ```


## Publish test package

    ```sh
    pip install --upgrade twine
    python -m twine upload --repository testpypi dist/*
    ```


## Publish official package

    ```sh
    pip install --upgrade twine
    python -m twine upload dist/*
    ```
