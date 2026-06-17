## ADDED Requirements

### Requirement: Fixed navigation bar
The page SHALL include a fixed-position navigation bar at the top with a logo mark, nav links (Features, Quick Start, Docs), and a subtle backdrop blur effect. The nav MUST collapse gracefully on mobile.

#### Scenario: Nav displays on scroll
- **WHEN** user scrolls down the page
- **THEN** the nav bar remains fixed at the top with a backdrop blur effect

#### Scenario: Nav links scroll to sections
- **WHEN** user clicks a nav link
- **THEN** the page smoothly scrolls to the corresponding section

#### Scenario: Mobile nav collapses
- **WHEN** viewport width is below 768px
- **THEN** nav links are hidden behind a hamburger toggle

### Requirement: Hero section
The page SHALL include a hero section at the top with the project tagline, a one-line description, a terminal-style code snippet, and a subtle ambient radial gradient background. The hero MUST use the editorial serif font for the heading.

#### Scenario: Hero renders
- **WHEN** the page loads
- **THEN** the hero heading, tagline, and code snippet are visible with a fade-in animation

### Requirement: Section rhythm
Each section SHALL have generous vertical padding (py-24/py-32) and be separated by an ultra-light 1px border. The main content width SHALL be constrained to max-w-5xl.

#### Scenario: Sections have consistent spacing
- **WHEN** viewing the page
- **THEN** each section has large whitespace above and below with consistent horizontal padding

### Requirement: Footer
The page SHALL include a minimal footer with MIT license attribution and GitHub link.

#### Scenario: Footer renders
- **WHEN** user scrolls to bottom
- **THEN** footer displays license and GitHub link
