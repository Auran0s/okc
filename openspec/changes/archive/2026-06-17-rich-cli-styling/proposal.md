## Why

The `okc introspect` CLI currently uses bare `print()` statements with no styling, no progress indicators, and no machine-readable output. For a developer tool, this means silent hangs during introspection, hard-to-read error messages, and no CI-friendly output modes. Rich is the de facto Python library for terminal styling — lightweight, cross-platform, Windows-aware.

## What Changes

- Add `rich` as a project dependency
- Create `src/okc/console.py` — a thin wrapper module providing `success()`, `error()`, `warn()`, `info()`, and a spinner `status()` context manager
- Add `--quiet` flag to `okc introspect` — suppresses all stdout output (stderr still flows); exit code is the contract
- Add `--json` flag to `okc introspect` — outputs structured JSON instead of styled text
- Replace all `print()` calls in `cli.py` with styled console methods
- Install Rich traceback handler at startup for improved error display with local variables
- Track and display elapsed time on completion
- Add CLI-level tests (`test_cli.py`) with `capsys`-based output assertions

## Capabilities

### New Capabilities

- `cli-styling`: Colored terminal output, spinner during introspection/generation, Rich traceback handler for better error display
- `cli-json-output`: Structured JSON output mode for CI and script consumption

### Modified Capabilities

<!-- No existing specs to modify -->

## Impact

- **Dependencies**: +`rich` to `pyproject.toml` (zero transitive deps, ~200KB)
- **Source**: +`src/okc/console.py` (new module, ~30 lines); modify `src/okc/cli.py` (~95 lines)
- **Tests**: +`tests/test_cli.py` (new file); no changes to existing tests
- **No changes** to source backends (`sources/`), bundle generator (`bundle/`), or ABC interfaces
