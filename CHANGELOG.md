# CHANGELOG

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
