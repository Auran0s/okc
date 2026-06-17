## Context

okc is a Python CLI tool with no web presence. This change introduces the project's first frontend — a single-page landing + docs site. The site will be pure HTML/CSS/JS with zero build step, hosted from `/public/` in the repo root. The design follows the Premium Utilitarian Minimalism protocol: warm monochrome palette, editorial typography, bento grid layout, subtle scroll animations, muted pastel accents.

## Goals / Non-Goals

**Goals:**
- Professional landing page that explains what okc is and why it exists
- Inline documentation covering installation, usage, backends, and OKF format
- Premium editorial aesthetic that signals quality and attention to detail
- Fully self-contained single HTML file — no build step, no framework
- Scroll-entry animations via IntersectionObserver

**Non-Goals:**
- Multi-page navigation or routing
- API calls, dynamic content, or server-side rendering
- Integration with the Python codebase (no code generation from Python)
- Authentication, user accounts, or interactive features beyond scrolling
- Full responsive redesign for tablet/mobile (basic mobile nav only)

## Decisions

| Decision | Choice | Rationale |
|---|---|---|
| Framework | None (vanilla HTML/CSS/JS) | Zero build step. No Node.js dependency in a Python repo. Single file to deploy. Protocol explicitly allows HTML + Tailwind. |
| CSS Framework | Tailwind via CDN | Enables rapid prototyping of the bento grid and design tokens without a build step. Custom config inlined via `<script>`. |
| Icons | Phosphor Icons (CDN) | Bold weight matches protocol's "technical, thicker-stroke aesthetic". CDN available. |
| Fonts | Playfair Display (Google Fonts) + system sans-serif stack | Playfair gives the editorial serif hero heading. System sans-serif stack (SF Pro / Helvetica Neue) avoids an extra font load for body text. Geist Mono (Google Fonts) for code. |
| Animations | Vanilla IntersectionObserver | Protocol bans scroll event listeners. IntersectionObserver is native, performant, and framework-free. |
| Background texture | Radial gradient + subtle CSS animation | Avoids image assets. Single `position: fixed; pointer-events: none` layer. Animation via `transform` only. |
| Hosting | Static file — deployable to GitHub Pages, Netlify, or any static host | No server requirements. Drop `public/index.html` anywhere. |
| Section imagery | Low-opacity `picsum.photos` seeded images | Adds visual depth without breaking monochrome palette. Desaturated via CSS filter or overlay. |

## Risks / Trade-offs

- **[Single-file size]** A single HTML file with all CSS and JS inline could become large. → Acceptable for a landing page. Keep JS minimal. Tailwind CDN is cached by the browser.
- **[Tailwind CDN dependency]** Relies on jsdelivr CDN availability. → Minimal risk. If CDN is down, page renders as unstyled HTML (still readable). Can vendor the file later.
- **[System fonts only for body]** No custom body font download means less visual control across OS. → Acceptable trade-off. SF Pro on macOS / Helvetica on all platforms provides a clean, premium feel. The serif hero heading (from Google Fonts) provides the editorial anchor.
- **[Google Fonts privacy]** Playfair Display loaded from Google Fonts exposes visitor IP. → Self-host on same origin if privacy is a concern. Accept for initial launch.
