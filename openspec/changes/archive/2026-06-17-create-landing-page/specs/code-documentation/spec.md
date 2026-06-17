## ADDED Requirements

### Requirement: Installation code block
The Quick Start section SHALL display the pip installation command in a styled code block with monospace font, light gray background, 8px border-radius, and 1px border.

#### Scenario: Code block renders
- **WHEN** viewing the Quick Start section
- **THEN** the installation command is rendered in a monospace code block with proper syntax styling

### Requirement: Usage code block
The Quick Start section SHALL display an `okc introspect` example command and its output directory tree in a monospace code block.

#### Scenario: Usage code block renders
- **WHEN** viewing the Quick Start section
- **THEN** the introspection command and output tree are displayed in a styled code block

### Requirement: Backends comparison table
The page SHALL display a two-column section for supported backends (SQLite, PostgreSQL) with URL scheme examples. Each backend entry SHALL include an inline kbd-style tag for its URL protocol.

#### Scenario: Backends section displays
- **WHEN** viewing the Backends section
- **THEN** SQLite and PostgreSQL are shown with URL examples, each with a monospace kbd tag

### Requirement: OKF format documentation
The page SHALL display the OKF document structure (directory tree) and YAML frontmatter example in styled code blocks.

#### Scenario: OKF format renders
- **WHEN** viewing the OKF Format section
- **THEN** the directory tree and YAML frontmatter are displayed in styled code blocks with proper formatting
