## Why

The okc package is ready for PyPI but has never been published. Publishing needs to be automated so that every tagged release on GitHub triggers an automatic build and upload to PyPI. Additionally, the current `bump-version.yml` workflow has a version drift bug (it only updates `pyproject.toml`, not `__init__.py`), and tests never run in CI — meaning broken code could be released.

## What Changes

- Add a `publish.yml` workflow that builds and publishes to PyPI via Trusted Publishing (OIDC) on tag push
- Rename `bump-version.yml` to `release.yml` and restructure with three sequential jobs: `detect-version`, `test`, `bump`
- Add a `test` job that runs pytest before the version bump, preventing releases on broken code
- Switch `__init__.py` to read version dynamically via `importlib.metadata.version("okc")`, making `pyproject.toml` the single source of truth
- No breaking changes (the CLI behavior is unchanged)

## Capabilities

### New Capabilities

- `publish-pipeline`: Automatically build and publish okc to PyPI (via Trusted Publishing) whenever a `v*` tag is pushed to GitHub.

### Modified Capabilities

- `release-automation`: The existing `bump-version.yml` is renamed to `release.yml` and now runs tests before bumping, and the version system no longer requires manual syncing between `__init__.py` and `pyproject.toml`.

## Impact

- `src/okc/__init__.py`: 1 line changed (dynamic version via `importlib.metadata`)
- `.github/workflows/bump-version.yml`: Renamed to `release.yml`, restructured with job outputs and a test step
- `.github/workflows/publish.yml`: New file (18 lines)
- One-time config on PyPI.org: add Trusted Publisher pointing to this repo
