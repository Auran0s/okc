## Context

The `okc` package is defined in `pyproject.toml` and ready to publish. Currently there's a `bump-version.yml` workflow that auto-bumps version on merge of `release/X.Y.Z` branches, but it has two issues:

1. It only updates `pyproject.toml`, missing `src/okc/__init__.py` — causing version drift
2. Tests are never run in CI — broken code can reach production

There's no PyPI publishing step at all.

The release flow needs to be: merge release branch → bump version → run tests → tag → build → publish to PyPI.

## Goals / Non-Goals

**Goals:**
- Single source of truth for version (`pyproject.toml` only)
- Tests run automatically before any version bump
- On tag push, build and publish to PyPI via Trusted Publishing (OIDC)
- Zero manual steps from merge to PyPI publication

**Non-Goals:**
- Linting, formatting, type checking (future work)
- Publishing to Test PyPI first (can be added later)
- Multi-arch wheels or platform-specific builds
- Changelog generation or release notes

## Decisions

### importlib.metadata for version discovery

`src/okc/__init__.py` switches from a hardcoded `__version__ = "0.1.0"` to:

```python
from importlib.metadata import version as _version
__version__ = _version("okc")
```

This reads from the wheel metadata at runtime. The canonical version lives only in `pyproject.toml → project.version`. When the package is freshly built (as in CI), the metadata always matches.

For local development with `pip install -e .`, the version reflects the state of `pyproject.toml` at install time. If the version changes during development, a reinstall is needed — this is standard Python practice.

### Two workflows for release + publish

```
release/0.2.0 merged to main
        │
        ▼
release.yml
  │  detect-version  →  0.2.0
  │  test            →  pytest (blocks if fails)
  └── bump           →  update pyproject, tag v0.2.0 with PAT
        │
 tag v0.2.0 pushed via PAT (triggers workflows because PAT ≠ GITHUB_TOKEN)
        │
        ▼
publish.yml
  │  build           →  python -m build
  └── publish        →  pypa/gh-action-pypi-publish via OIDC
```

Why two files instead of a single workflow? GitHub Actions jobs within a single workflow all execute against the same commit SHA. The `bump` job creates a new commit + tag, but a subsequent `publish` job wouldn't see it. Two files with a tag trigger is the standard, working pattern.

The tag push uses `${{ secrets.PAT }}` (a personal access token) rather than `GITHUB_TOKEN`. This is critical: PAT-pushed tags trigger downstream workflows, while `GITHUB_TOKEN`-pushed tags do not (GitHub's recursive trigger prevention).

### Trusted Publishing (OIDC) over API tokens

| Aspect | API Token | Trusted Publishing |
|--------|-----------|-------------------|
| Secret management | Must create, store in GH secrets, rotate | None (OIDC) |
| Security | Long-lived secret, leaked = compromise | Short-lived, per-run tokens |
| Setup effort | More (create token + configure) | 30s (select repo + workflow in PyPI UI) |
| Recommended by PyPI | — | Yes |

Trusted Publishing requires no token management. The PyPI project settings must be configured once to trust the GitHub environment `Auran0s/okc` with workflow `publish.yml`.

## Risks / Trade-offs

- **`importlib.metadata` requires local install**: Developers running `python okc/cli.py` directly without `pip install -e .` will get `PackageNotFoundError`. The package is designed to be installed, so this is acceptable.
- **No Test PyPI**: The first publish will be to real PyPI. If there's a build error, the tag already exists. Consider adding a Test PyPI step before v1.0.
- **PAT rotation**: The `secrets.PAT` must be kept valid for the tag trigger to work. If it expires, the publish workflow won't fire.
