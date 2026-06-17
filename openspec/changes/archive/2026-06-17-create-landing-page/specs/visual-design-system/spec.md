## ADDED Requirements

### Requirement: Typography hierarchy
The page SHALL use an editorial serif font for the hero heading (Playfair Display, letter-spacing: -0.02em, line-height: 1.1) and a geometric sans-serif font (SF Pro Display / Helvetica Neue) for body text. Monospace (Geist Mono / SF Mono) SHALL be used for code blocks and kbd elements. Body text MUST NOT be #000000; use #2F3437 with 1.6 line-height.

#### Scenario: Hero heading uses serif font
- **WHEN** viewing the hero section
- **THEN** the main heading is rendered in Playfair Display with tight tracking and tight line-height

#### Scenario: Body text uses sans-serif
- **WHEN** viewing body paragraphs
- **THEN** they are rendered in SF Pro Display / Helvetica Neue with #2F3437 color and 1.6 line-height

#### Scenario: Code uses monospace
- **WHEN** viewing code blocks and kbd elements
- **THEN** they are rendered in a monospace font

### Requirement: Color palette
The page SHALL use a warm monochrome palette: background #F7F6F3, cards #FFFFFF, borders #EAEAEA, body text #2F3437, secondary text #787774. Accent colors SHALL only appear as muted pastel backgrounds for icons and tags: #FDEBEC/#9F2F2D (red), #E1F3FE/#1F6C9F (blue), #EDF3EC/#346538 (green), #FBF3DB/#956400 (yellow).

#### Scenario: Color palette applied globally
- **WHEN** viewing any section
- **THEN** the warm bone background, white card surfaces, and light gray borders are consistently applied

### Requirement: Scroll entry animations
Content sections SHALL fade in with translateY(12px) → translateY(0) + opacity 0 → 1 over 600ms with cubic-bezier(0.16, 1, 0.3, 1) using IntersectionObserver. Grid items SHALL have staggered 80ms cascade delays.

#### Scenario: Sections animate on scroll
- **WHEN** user scrolls to a new section
- **THEN** it fades in gently with the defined bezier curve and duration

#### Scenario: Cards stagger in sequence
- **WHEN** grid items enter the viewport
- **THEN** each item animates with an 80ms delay relative to its index

### Requirement: Ambient background motion
The hero section SHALL have a single, very slow-moving radial gradient blob (animation-duration 20s+, opacity 0.02-0.04) on a position: fixed, pointer-events: none layer.

#### Scenario: Ambient blob animates
- **WHEN** viewing the hero section
- **THEN** a subtle warm radial gradient drifts slowly in the background

### Requirement: Iconography
All icons SHALL use Phosphor Icons Bold or Fill weight with consistent stroke width. No generic thin-line icon libraries.

#### Scenario: Icons use Phosphor Bold weight
- **WHEN** viewing icons on the page
- **THEN** they are rendered in Phosphor Bold or Fill weight with consistent styling
