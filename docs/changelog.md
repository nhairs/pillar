# Change Log

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.4.0](https://github.com/nhairs/pillar/compare/v0.3.0...v0.4.0) - 2025-11-01

### Added

- Support for Python 3.13, 3.14 and PyPy 3.10, 3.11.

### Changed

- Logging mixin classes now set default `stacklevel` to `2` so that logging calls reference
  the correct calling line (rather than the pillar module).

### Fixed

- Application file loggers correctly use `file_max_size` and `file_backup_count` from `LoggingManifest`.

### Removed

- Support for Python 3.7.


### Development Changes

- Tests are now run using UV (rather than in a docker container)
- Black formatter now uses pyproject config
- Orjson is not installed in PyPy environments
- Version removed from `docker-compose.yml`


## [0.3.0](https://github.com/nhairs/pillar/compare/v0.2.0...v0.3.0) - 2024-08-29

### Added

- Allow loading config files from directory (`ConfigLoader.load_config_directory` and `--config-dir`)
- Add example applications (`examples/`)
  - `config_loading.py` requires config arguments and prints the loaded config.
  - `log_levels.py` prints sample log messages.

## [0.2.0](https://github.com/nhairs/pillar/compare/v0.1.0...v0.2.0) - 2024-01-23

### Added

- Add functions for getting logger names based on class / instance.
- Expose `get_logger` on logging mixin classes.

## 0.1.0 - 2023-12-30

- Initial release
