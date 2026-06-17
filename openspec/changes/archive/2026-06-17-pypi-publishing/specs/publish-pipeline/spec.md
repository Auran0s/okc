## MODIFIED Requirements

### Requirement: Version is single-sourced in pyproject.toml

The system SHALL read the package version from `pyproject.toml` only, using `importlib.metadata.version("okc")` at runtime.

#### Scenario: CLI --version displays correct version
- **WHEN** the package is installed and `okc --version` is run
- **THEN** the displayed version SHALL match the `version` field in `pyproject.toml`

## ADDED Requirements

### Requirement: Tests run before version bump

When a `release/X.Y.Z` branch is merged to `main`, the release workflow SHALL run all pytest tests before bumping the version.

#### Scenario: Tests pass, version is bumped
- **WHEN** tests pass
- **THEN** the version SHALL be bumped and a `vX.Y.Z` tag SHALL be created

#### Scenario: Tests fail, version is not bumped
- **WHEN** tests fail
- **THEN** the workflow SHALL fail and no version bump or tag SHALL occur

### Requirement: Published on tag push via Trusted Publishing

When a `v*` tag is pushed to GitHub, the system SHALL build the package and publish it to PyPI using Trusted Publishing (OIDC).

#### Scenario: Tag pushed, package published
- **WHEN** a `vX.Y.Z` tag is pushed
- **THEN** the package SHALL be built via `python -m build` and published to PyPI via `pypa/gh-action-pypi-publish`

#### Scenario: Untagged push does not publish
- **WHEN** a push to any branch occurs without a `v*` tag
- **THEN** the publish workflow SHALL NOT run
