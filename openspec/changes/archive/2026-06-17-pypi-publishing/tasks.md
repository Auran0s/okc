## 1. Single Source of Truth for Version

- [x] 1.1 Make `__init__.py` read version dynamically via `importlib.metadata`

## 2. Release Workflow

- [x] 2.1 Rename `bump-version.yml` → `release.yml`
- [x] 2.2 Restructure into jobs: `detect-version` (with outputs), `test` (pytest), `bump` (version bump + tag + PR)

## 3. Publish Workflow

- [x] 3.1 Create `publish.yml` with `build` job (python -m build) and `publish` job (Trusted Publishing)
