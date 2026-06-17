## ADDED Requirements

### Requirement: README documents the --json flag

The README SHALL document the `--json` CLI flag in both the CLI reference table and an example, including the JSON output schema.

#### Scenario: --json flag in CLI reference table
- **WHEN** user reads the CLI reference table
- **THEN** there SHALL be a row for `--json` with description "Output structured JSON instead of styled terminal output"
- **AND** the default SHALL be documented as "off"

#### Scenario: --json example shown in code block
- **WHEN** user reads the examples section
- **THEN** there SHALL be an example using `--json` that shows the structured JSON output schema

### Requirement: README documents the --quiet flag

The README SHALL document the `--quiet` CLI flag in the CLI reference table, noting that stderr output is preserved.

#### Scenario: --quiet flag in CLI reference table
- **WHEN** user reads the CLI reference table
- **THEN** there SHALL be a row for `--quiet` with description "Suppress stdout output (stderr still flows)"
- **AND** the default SHALL be documented as "off"

### Requirement: README mentions Rich terminal output

The README SHALL mention the Rich-powered terminal output (colored indicators, spinner, elapsed time) as a feature.

#### Scenario: Rich output listed in Features
- **WHEN** user reads the Features section
- **THEN** there SHALL be a feature bullet describing styled terminal output with Rich

### Requirement: README documents python -m okc invocation

The README SHALL mention that the tool can be invoked as `python -m okc`.

#### Scenario: python -m usage in Quick Start
- **WHEN** user reads the Usage section
- **THEN** there SHALL be a note or example showing `python -m okc introspect` as an alternative to `okc introspect`

### Requirement: README mentions path traversal protection

The README SHALL mention that the generated bundle is protected against path traversal attacks.

#### Scenario: Path traversal protection noted
- **WHEN** user reads the OKF Bundle Format section
- **THEN** there SHALL be a note that bundle generation validates paths to prevent directory traversal

### Requirement: README has a CI badge

The README SHALL display a GitHub Actions badge at the top linking to the bump-version workflow.

#### Scenario: CI badge present
- **WHEN** user views the README header
- **THEN** there SHALL be a `[![CI](...)]` badge linking to `.github/workflows/bump-version.yml`
- **AND** the badge SHALL use the Shields.io format

### Requirement: README shows updated test coverage

The README test coverage table SHALL include `test_cli.py` with description "CLI flag handling (--quiet, --json, unsupported schemes, error output)".

#### Scenario: test_cli.py in coverage table
- **WHEN** user reads the test coverage table in the Development section
- **THEN** there SHALL be a row for `tests/test_cli.py` with an appropriate description

### Requirement: README architecture tree includes console.py and __main__.py

The Architecture tree diagram SHALL include the `console.py` and `__main__.py` files.

#### Scenario: console.py in architecture tree
- **WHEN** user reads the Architecture section
- **THEN** the `okc/` directory listing SHALL include `console.py`

#### Scenario: __main__.py in architecture tree
- **WHEN** user reads the Architecture section
- **THEN** the `okc/` directory listing SHALL include `__main__.py`
