## Why

okc is a developer tool with no web presence — no landing page, no docs site, no way for potential users to discover, evaluate, or learn about it outside of the raw README on GitHub. A single-page landing + docs site hosted at `okc.dev` (or via GitHub Pages) would give the project a professional public face, lower the barrier to understanding what it does, and serve as a canonical reference for the OKF specification and CLI usage.

## What Changes

- Create `/public/index.html` — a single-file, fully self-contained landing page and docs site
- Add Tailwind CSS (CDN), Phosphor Icons (CDN), and custom fonts (Google Fonts) for styling
- Implement scroll-entry animations via vanilla JS IntersectionObserver
- Add a subtle ambient radial gradient background motion effect
- No build step, no framework — pure HTML/CSS/JS

## Capabilities

### New Capabilities
- `landing-page-layout`: Overall page chrome — fixed navbar, hero, section rhythm, footer
- `feature-presentation`: Bento grid of okc feature cards with icons and accent colors
- `code-documentation`: CLI usage examples, installation commands, backends table, OKF format reference
- `visual-design-system`: Premium Utilitarian Minimalist aesthetic — custom typography, warm monochrome palette, muted pastel accents, scroll animations

### Modified Capabilities
- None — no existing specs to modify

## Impact

- New `/public/` directory at repo root (no existing code to modify)
- No changes to Python source code, tests, or dependencies
- No breaking changes
