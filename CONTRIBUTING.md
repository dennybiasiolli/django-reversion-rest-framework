# Contributing guidelines

This package has been created using python 3.11.6.

## Creating environment with uv and enabling it

```sh
uv sync
source .venv/bin/activate
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
uv build
```


## Publish official package

```sh
uv publish
```
