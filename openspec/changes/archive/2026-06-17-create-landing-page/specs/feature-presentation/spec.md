## ADDED Requirements

### Requirement: Bento grid feature cards
The page SHALL display okc features in an asymmetrical CSS grid (bento layout) with 4 cards. Each card MUST have a 1px solid border, 8px border-radius, generous internal padding, a Phosphor Bold icon with muted pastel background, and a heading + description.

#### Scenario: Cards display in bento grid
- **WHEN** user scrolls to the Features section
- **THEN** 4 feature cards appear in an asymmetric grid layout with staggered fade-in animations

#### Scenario: Card hover effect
- **WHEN** user hovers over a card
- **THEN** the card shows a subtle shadow shift (0 2px 8px rgba(0,0,0,0.04)) over 200ms

### Requirement: Each card uses a distinct pastel accent
Each feature card icon background SHALL use one of the four defined muted pastel colors (pale red, blue, green, yellow) with matching text color.

#### Scenario: Pastel accent applies correctly
- **WHEN** viewing the feature cards
- **THEN** each card has a pastel icon background and matching accent color unique from the other cards
