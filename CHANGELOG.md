# CHANGELOG

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
