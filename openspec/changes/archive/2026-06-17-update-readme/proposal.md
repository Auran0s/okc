## Why

The README.md is the project's front door, but it has drifted out of sync with the codebase. Several features already implemented (JSON output mode, quiet mode, Rich terminal styling, path traversal protection) are not documented. The README's structure also lags behind current best practices — it lacks badges, shields, a well-organized CLI reference, and a polished presentation consistent with modern open-source Python tools.

## What Changes

- Add badges and shields (CI status, Python version, license) for a stronger first impression
- Document the `--json` flag for structured JSON output, including example usages
- Document the `--quiet` flag for suppressing stdout
- Document the Rich terminal output features (colored output, spinners, elapsed time)
- Document `python -m okc` invocation
- Add a note about path traversal protection in bundle generation
- Update the Architecture tree to include `console.py` and `__main__.py`
- Update the test coverage table to include `test_cli.py` (CLI flag tests)
- Add a GitHub Actions CI badge referencing the bump-version workflow
- General polish: align tone and structure with modern README conventions (badges, admonitions, concise tables)

None of these changes modify the CLI behavior or the project's capabilities — this is purely a documentation and presentation update.

## Capabilities

### New Capabilities

- `readme-documentation`: Document existing README gaps — CLI flags (`--json`, `--quiet`), Rich output, path traversal protection, updated architecture, CI badge, `python -m okc` usage, and test coverage.

### Modified Capabilities

- `cli-json-output`: No spec-level requirement changes — only README documentation of existing behavior.
- `cli-styling`: No spec-level requirement changes — only README documentation of existing behavior.

## Impact

- **Affected files**: `README.md` (the only file that changes)
- **No API changes**: The CLI interface and behavior remain untouched
- **No dependency changes**: All features being documented are already implemented and tested
