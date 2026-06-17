## Context

The README.md at the project root is the primary documentation surface for users and contributors. It currently describes the core introspection functionality but omits several features that have been implemented in the codebase. The project also lacks visual indicators (badges) that help users quickly assess project health and requirements.

All features to be documented already exist in `src/okc/cli.py`, `src/okc/console.py`, `src/okc/bundle/generator.py`, and `tests/test_cli.py`. No new code needs to be written — only the README needs updating.

## Goals / Non-Goals

**Goals:**
- Add project badges (CI, Python version, license) at the top of the README
- Document the `--json` CLI flag and its JSON output schema
- Document the `--quiet` CLI flag
- Document Rich terminal output features (spinners, colors, elapsed time)
- Document `python -m okc` as an alternative invocation
- Add a note about path traversal protection in bundle generation
- Update the Architecture tree to reflect `console.py` and `__main__.py`
- Update the test coverage table to include `test_cli.py`
- Add a GitHub Actions CI badge linked to the bump-version workflow

**Non-Goals:**
- No changes to CLI behavior, source code, or tests
- No new features or dependencies
- No changes to the OKF bundle output format
- No restructuring of the project layout

## Decisions

- **Badge source**: Use `https://img.shields.io` (Shields.io) for badges — standard in the Python ecosystem, zero-dependency, and matches the inspirational READMEs provided.
- **CI badge target**: Link to the GitHub Actions workflow at `.github/workflows/bump-version.yml`. While this workflow handles version bumps, it serves as a proxy CI badge until a dedicated build/test workflow is added.
- **Admonition style**: Use GitHub-native admonition syntax (`> [!NOTE]`, `> [!TIP]`, `> [!IMPORTANT]`) — already used in the current README, fully compatible with GFM rendering.
- **Architecture diagram**: Keep the existing text-based tree, updated with new files. A Mermaid diagram would add visual polish but increases maintenance burden for a small project.
- **CLI reference table**: Extend the existing table with `--json` and `--quiet` rows rather than creating a new section, maintaining the current README's compact structure.

## Risks / Trade-offs

- **Stale badges**: Badges rely on GitHub Actions workflow status. If the workflow is renamed or removed, the badge will break. Acceptable risk for a single-developer project.
- **README length**: Adding documentation for `--json`/`--quiet`/Rich output will increase the README from ~214 lines to ~260 lines. The inspirational READMEs (400-1200 lines) suggest this is within a reasonable range.
