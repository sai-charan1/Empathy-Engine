# Changelog

All notable changes to this project are documented in this file.

## [1.0.0] - 2025-06-04

### Added

- `empathy_engine` package with typed configuration (`pydantic-settings`)
- Unit and API smoke tests with pytest
- GitHub Actions CI (Ruff, Black, MyPy, Pytest)
- Docker and docker-compose for local deployment
- MIT license, contributing guide, and code of conduct

### Changed

- Deterministic audio filenames via SHA-256 hash
- Structured logging for analysis and synthesis
- Health check endpoint (`GET /health`)
