## Context

The `okc` CLI (`cli.py`, 95 lines) currently uses bare `print()` calls for all user-facing output — no colors, no spinners, no progress indicators, no machine-readable output. The only dependencies are `pyyaml` and `psycopg2-binary`.

The CLI has one subcommand (`introspect`) with a simple flow:

```
_create_source → list_concepts → generate_bundle → os.walk for file count
```

All output happens around this flow, never during it. Source backends and the bundle generator are completely silent.

The existing `print()` calls are in `_handle_introspect()`:

| Line | Output | Stream |
|------|--------|--------|
| 55-61 | Unsupported URL scheme error | stderr |
| 66 | "Introspecting {url}..." | stdout |
| 71 | "  Found {N} tables, {M} views" | stdout |
| 77 | "  Written {N} files to {out}" | stdout |
| 78 | "Done." | stdout |
| 80 | Generic exception error | stderr |

## Goals / Non-Goals

**Goals:**

- Add colored, styled terminal output for the `okc introspect` command
- Add a spinner during connection/introspection and generation phases
- Add Rich traceback handler for improved error diagnostics
- Add `--quiet` flag for silent operation (exit code as contract)
- Add `--json` flag for machine-readable structured output
- Keep the change minimal — one new module (~30 lines), modified `cli.py` (~+40 lines), new test file
- Maintain zero behavior changes in non-interactive modes (stdout piped to file should still work)

**Non-Goals:**

- No changes to the bundle generator or source backends — no progress callbacks, no API surface changes
- No migration to Click/Typer or any other CLI framework
- No interactive prompts or full TUI
- No styled argparse help text

## Decisions

### Decision 1: Thin wrapper module vs. inline Rich usage

**Choice**: `okc/console.py` wrapper module

**Rationale**: Five `print()` calls would be trivial to inline with Rich, but the pattern of "success checkmark", "error cross", "spinner while working" repeats and benefits from consistent styling. A 30-line wrapper gives:

- Single import in `cli.py` (`from okc.console import console, success, error, status`)
- Single point for theme changes (color scheme, prefix characters)
- Clean `--quiet` suppression via `console.quiet`
- Testable via `Console(file=StringIO())`

**Rejected**: Inlining Rich `print()` calls directly — repeated `console.print("[green]✓[/] ...")` patterns would be harder to maintain and inconsistent.

### Decision 2: Rich vs. colorama vs. ANSI escapes

**Choice**: Rich

**Rationale**:

- Rich is the de facto standard (50M+ downloads/month)
- Zero transitive dependencies
- Cross-platform terminal detection (handles Windows PowerShell, CMD, Windows Terminal)
- Spinner/progress API built in (`console.status()`)
- Traceback handler built in (`rich.traceback.install()`)
- Auto-checks if stdout is a TTY and strips styling when piped

**Rejected**: colorama (no spinners, no traceback, no tables); ANSI escapes (Windows-incompatible, error-prone); Textual (full TUI framework, overkill)

### Decision 3: `--quiet` and `--json` as mutually exclusive flags vs. combined

**Choice**: Mutually exclusive. If both are passed, `--json` takes precedence and `--quiet` is ignored.

**Rationale**: `--quiet` suppresses all stdout (stderr still flows). `--json` outputs structured data. If someone explicitly passes `--quiet`, they want silence. If they pass `--json`, they want structured data. Passing both is contradictory — preferring `--json` is the safer default (it's the richer output).

### Decision 4: JSON output format

**Choice**: Single-line JSON object per invocation, written to stdout.

**Rationale**: Single-line JSON is pipe-friendly (`okc introspect --json ... | jq .`). The schema is:

Success:
```json
{"status":"ok","url":"sqlite:///db.sqlite","tables":12,"views":3,"files":45,"output_dir":"./okf-bundle","elapsed_ms":1834}
```

Error:
```json
{"status":"error","message":"Unsupported database URL scheme: mysql://..."}
```

### Decision 5: Spinner during `generate_bundle()`

**Choice**: Indeterminate spinner with a static message, not a progress bar.

**Rationale**: `generate_bundle()` has no progress hooks — it calls `source.list_concepts()` then iterates silently. Adding a progress callback to the source/generator API is a deeper refactor. For now, a spinner that says "Generating OKF bundle..." gives sufficient feedback. If the user finds generation slow on large schemas, the callback refactor can happen separately.

### Decision 6: Rich traceback handler placement

**Choice**: Install at the top of `main()`, before any CLI logic.

**Rationale**: Catches errors early — argparse errors, URL parsing failures, import errors. One line: `from rich.traceback import install; install(show_locals=True)`. The `show_locals=True` flag displays local variable values in tracebacks, which is valuable for a developer tool.

## Risks / Trade-offs

| Risk | Likelihood | Mitigation |
|------|------------|------------|
| Rich adds ~200KB to install footprint | Low impact | OKF is already lightweight (only 2 deps). 200KB is negligible. |
| Windows terminal detection misses edge cases | Low | Rich is well-tested on Windows. If discovered, pinning a version or adding `LEGACY_WINDOWS_STUBS` env var handles it. |
| `--quiet` hides useful info users expect | Medium | `--quiet` is opt-in. Default behavior remains chatty. Documentation clarifies `--quiet` contract (exit code only). |
| `--json` schema evolves inconsistently | Medium | Only one JSON output shape exists now. If more subcommands are added, each gets its own JSON shape. No global schema needed yet. |
| Spinner output corrupts file redirects | Low | Rich auto-detects `sys.stdout.isatty()` and strips ANSI when piped. Richer `Console()` does this automatically. |

## Open Questions

- Should `--json` output go to stdout and styled output to stderr (so they can be separated)? Current plan: styled output to stdout, JSON to stdout. Use `--quiet` if you want nothing. Revisit if this causes issues in practice.
