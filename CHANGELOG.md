# CHANGELOG

## [Unreleased]

### Fixed

- history/deleted `field_dict` now applies the view's `serializer_class` even
    when the model has unique constraints; intermediate deserialization no longer
    runs create/update uniqueness validators that would fail for existing rows (#141)
- intermediate history deserialization normalizes reversion attnames (e.g. `related_id`)
    to model field names so FK/relation labels in `serializer_class` work in `field_dict`

## [4.1.0]

### Added

- new `RestoreMixin` with a POST `restore/<version_pk>/` action
    for restoring deleted model instances from version history (#4)
- filtering support for `history` and `deleted` endpoints (#13)
    via query parameters: `user`, `date_created`, `date_created__gt`,
    `date_created__gte`, `date_created__lt`, `date_created__lte`

### Changed

- `HistoryModelViewSet` now includes `RestoreMixin`
    (adds `deleted`, `restore` endpoints alongside existing ones)
- updated dev dependencies: black 26.5.1, isort 8.0.1, pylint 4.0.6,
    sqlparse 0.5.5

## [4.0.0]

### Potentially BREAKING CHANGES

- removed deprecated classes: `BaseHistoryModelMixin`, `HistoryOnlyMixin`,
    `DeletedOnlyMixin`, `ReadOnlyHistoryModel`, `HistoryModelMixin`.
    Use `BaseHistoryMixin`, `HistoryMixin`, `DeletedMixin`, and `RevertMixin` instead

### Changed

- moved `_build_serializer` from `HistoryMixin` to `BaseHistoryMixin`,
    allowing `DeletedMixin` to work independently without requiring `HistoryMixin`
- removed unreachable `version_pk` validation in `revert` action
    (URL regex already guarantees a valid value)
- removed redundant `setup.cfg` (all metadata is in `pyproject.toml`)
- used `uv run` consistently in all Makefile targets
- added Python version classifiers (3.10-3.14) and Django REST Framework classifier
- added installation instructions and mixin usage example to README
- updated CONTRIBUTING.md, removed outdated boilerplate from test project settings
- added tests for revert error handling and unauthenticated access (22 → 26 tests)
- improved test coverage from 98% to 99%

## [3.0.0]

### Potentially BREAKING CHANGES

- dropped support for python 3.9
- added support for python 3.13 and 3.14

## [2.0.0]

### Potentially BREAKING CHANGES

- dropped support for python 3.8

## [1.2.0]

### Changed

- Chore: set default Python version to 3.11

## [1.1.2]

### Changed

- Fix: support custom parameters defined in urlconf (#30 by @gsfish)

## [1.1.1]

### Changed

- Displaying deprecation warning only when subclassing a deprecated class

## [1.1.0]

### Changed

- `BaseHistoryModelMixin` has been renamed to `BaseHistoryMixin`
    and will be removed in the next version

- `HistoryOnlyMixin` has been renamed to `HistoryMixin`
    and will be removed in the next version

- `DeletedOnlyMixin` has been renamed to `DeletedMixin`
    and will be removed in the next version

- `ReadOnlyHistoryModel` will be removed in the next version.
    Please use `HistoryMixin` and `DeletedMixin` for the same behaviour


## [1.0.1]

### Changed

- dropped support for python < 3.8
- mixins: returning the base `field_dict` in case of errors during serialization (#14)
    
    This happens when trying to serialize an history object with only a selected
    list of fields.


## [1.0.0]

### Potentially BREAKING CHANGES

- now `field_dict` is serialized using the original serializer,
    check desired behavior when updating

### Added

- mixins: serializing `field_dict` field using the original serializer
    (#12 thanks to @gecBurton)
- tests: test case for `deleted` pagination
- tests: test case for serialization

### Changed

- mixins: handling pagination in `deleted` action (#12)


## [0.5.0]

### Added

- mixins: adding a `version` action for getting a specific version of the history
    (#10 thanks to @gecBurton)
- tests: test case for `history` pagination

### Changed

- mixins: handling pagination in `history` action (#10 thanks to @gecBurton)
- mixins: sorting `history` by `-revision__date_created` (#10 thanks to @gecBurton)


## [0.4.0]

### Added

- mixins: splitting in coherent mixins and adding tests (#7)

### Changed

- fix: url_path for revert action from `aaaa/<version_pk>` to `revert/<version_pk>` (#4)


## [0.3.1]

### Changed

- viewsets: Update viewsets to use mixins (#3 thanks to @anudeepsamaiya)


## [0.3.0]

### Added

- viewsets: `/deleted/` endpoint inside `HistoryModelViewSet`


## [0.2.0]

### Added

- viewsets: allowing users to customize the `version_serializer` of `HistoryModelViewSet`


## [0.1.0]

### Added

- viewsets: `/<pk>/history/` endpoint inside `HistoryModelViewSet`
