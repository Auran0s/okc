## 1. Setup

- [x] 1.1 Add `rich` to `pyproject.toml` dependencies
- [x] 1.2 Create `src/okc/console.py` with `Console` instance and helper functions (`success`, `error`, `warn`, `info`, `status`)

## 2. CLI Styling Implementation

- [x] 2.1 Install Rich traceback handler at top of `main()` in `cli.py` (`rich.traceback.install(show_locals=True)`)
- [x] 2.2 Replace unsupported URL scheme error `print()` with `console.error()` call in `_handle_introspect()`
- [x] 2.3 Add elapsed time tracking using `time.monotonic()` around the introspection flow
- [x] 2.4 Wrap the introspection phase (connecting + listing concepts) with a spinner status message
- [x] 2.5 Replace "Found N tables, M views" `print()` with `console.success()` call
- [x] 2.6 Wrap `generate_bundle()` call with a spinner status message
- [x] 2.7 Replace "Written N files" and "Done" `print()` calls with `console.success()` calls, including elapsed time
- [x] 2.8 Replace generic exception `print()` with `console.error()` call

## 3. --quiet and --json Flags

- [x] 3.1 Add `--quiet` argument to the introspect subparser
- [x] 3.2 Add `--json` argument to the introspect subparser (mutually exclusive group with `--quiet`)
- [x] 3.3 In `_handle_introspect()`, when `--quiet` is set, set `console.quiet = True`
- [x] 3.4 In `_handle_introspect()`, when `--json` is set, build and print JSON output instead of styled output
- [x] 3.5 Handle error case in `--json` mode: output `{"status":"error","message":"..."}` to stdout and exit 1
- [x] 3.6 Verify `--quiet` takes precedence over styled output but `--json` overrides `--quiet`

## 4. Testing

- [x] 4.1 Create `tests/test_cli.py` with `capsys` fixture
- [x] 4.2 Test successful styled output (colored success messages, spinner presence, elapsed time)
- [x] 4.3 Test error output (unsupported URL scheme renders in red)
- [x] 4.4 Test `--quiet` flag suppresses stdout while preserving stderr
- [x] 4.5 Test `--json` flag produces valid JSON with correct schema
- [x] 4.6 Test `--json` error case produces `{"status":"error","message":"..."}`
- [x] 4.7 Test `--quiet --json` precedence (JSON wins)
- [x] 4.8 Test that output degrades gracefully when stdout is not a TTY (no ANSI codes)

## 5. Verification

- [x] 5.1 Run existing test suite to confirm no regressions
- [x] 5.2 Run new `test_cli.py` tests
- [x] 5.3 Manual verification: run `okc introspect sqlite:///test.db` and confirm styled output
- [x] 5.4 Manual verification: run `okc introspect --json sqlite:///test.db` and pipe through `jq`
- [x] 5.5 Manual verification: run `okc introspect --quiet sqlite:///test.db` and confirm empty stdout
