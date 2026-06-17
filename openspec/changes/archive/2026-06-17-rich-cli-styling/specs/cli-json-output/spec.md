## ADDED Requirements

### Requirement: JSON output mode
The CLI SHALL support a `--json` flag on the `introspect` command that outputs structured JSON to stdout instead of styled terminal output.

#### Scenario: Successful introspection with --json
- **WHEN** user runs `okc introspect --json sqlite:///db.sqlite --out ./bundle`
- **THEN** stdout contains a single JSON object with keys: `status`, `url`, `tables`, `views`, `files`, `output_dir`, `elapsed_ms`
- **AND** `status` is `"ok"`
- **AND** `tables` and `views` contain integer counts
- **AND** `elapsed_ms` is a positive integer
- **AND** no ANSI escape codes or styled text appear in output
- **AND** exit code is 0

#### Scenario: Error with --json
- **WHEN** user runs `okc introspect --json mysql:///db --out ./bundle`
- **THEN** stdout contains a single JSON object with keys: `status`, `message`
- **AND** `status` is `"error"`
- **AND** `message` describes the failure
- **AND** exit code is 1

### Requirement: Quiet mode
The CLI SHALL support a `--quiet` flag on the `introspect` command that suppresses all stdout output.

#### Scenario: Quiet successful introspection
- **WHEN** user runs `okc introspect --quiet sqlite:///db.sqlite`
- **THEN** no output appears on stdout
- **AND** exit code is 0

#### Scenario: Quiet mode with error
- **WHEN** user runs `okc introspect --quiet mysql:///db`
- **THEN** error message still appears on stderr (quiet suppresses stdout only)
- **AND** exit code is 1

### Requirement: --quiet and --json precedence
When both `--quiet` and `--json` are passed, `--json` SHALL take precedence.

#### Scenario: Both flags passed
- **WHEN** user runs `okc introspect --quiet --json sqlite:///db.sqlite`
- **THEN** stdout contains the JSON output (not suppressed)
- **AND** exit code is 0
