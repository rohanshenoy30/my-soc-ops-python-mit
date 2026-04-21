# Design Spec: Card Deck Shuffle Mode

## Overview
A new game mode where players tap a button to reveal random icebreaker questions, one card at a time. Perfect for quick rounds or ice-breaker moments at social events.

## Feature: Card Deck Shuffle

### User Flow
1. Player selects "CARD DECK" from the mode selection screen
2. Game displays a large card with a single question (from question bank)
3. Player taps the card or "NEXT CARD" button to reveal another random question
4. No "win" condition—endless card shuffling for non-stop icebreakers

### Implementation Details

#### Backend Architecture
- **New GameMode**: `CARD_DECK_SHUFFLE` enum value in `app/models.py`
- **Session State**: 
  - `card_questions: list[str]` — shuffled copy of all questions
  - `current_card_index: int` — tracks current position in deck (cycles)
- **Core Methods** in `GameSession`:
  - `get_current_card()` — returns current question text
  - `next_card()` — advances index (wraps to start at end)
- **API Endpoints**:
  - `POST /start/card_deck_shuffle` — initializes game with shuffled deck
  - `POST /next-card` — HTMX endpoint returns updated card component

#### Frontend Components
- **card.html** — Card component showing:
  - "FIND SOMEONE WHO..." text (cyan glow)
  - Current question in large, wobbling lime neon text
- **card_deck_screen.html** — Full screen layout with:
  - Header (back button, title, empty space for symmetry)
  - Instructions
  - Card display area with animation
  - "NEXT CARD" button (pink with flashing animation)

#### Visual Design (Arcade Theme)
- **Card Element**: 
  - Large 3:4 aspect ratio card
  - Pink border (4px) with intense glow
  - Dark gradient background (arcade colors)
  - Pulsing glow animation (3s cycle)
  - Flip animation on reveal (0.6s)
  - Hover scale effect
- **Question Text**: 
  - Large (3xl) lime green neon
  - Wobbling animation (2s cycle)
  - line-height 1.4 for readability
- **Button**:
  - Pink background with arcade styling
  - Flashing animation
  - Active state scale-down feedback
- **CSS Animations**:
  - `card-flip` — 3D rotation reveal effect
  - `card-glow-pulse` — intensity pulsing glow
  - `wobble` — text oscillation
  - Smooth HTMX swap (0.3s) between cards

### Styling System
- Uses CSS variables: `--neon-pink`, `--neon-cyan`, `--neon-lime`, etc.
- Arcade bezel/border classes for consistent framing
- Glow utilities for text and box-shadows
- Animation utilities for movement/effects
- Responsive layout: flexbox, centered on all screen sizes

## Implementation Checklist
- [x] Add `CARD_DECK_SHUFFLE` to GameMode enum
- [x] Extend GameSession to track card state (shuffled questions, current index)
- [x] Create `get_current_card()` and `next_card()` methods
- [x] Create `components/card.html` template (card component)
- [x] Create `components/card_deck_screen.html` template (full screen)
- [x] Add `POST /start/card_deck_shuffle` endpoint
- [x] Add `POST /next-card` HTMX endpoint
- [x] Update `_get_game_template()` to route to card deck screen
- [x] Add "CARD DECK" button to start screen
- [x] Add comprehensive CSS animations and styling
- [x] Tests passing (57/57)
- [x] Linting passing (ruff check)

## Technical Notes

### State Management
- Questions shuffled once at game start using `random.shuffle()`
- Current index cycles via modulo operator: `(index + 1) % deck_length`
- Infinite shuffle — no win state, just endless card cycles
- Cookie-based session persistence (existing session middleware)

### HTMX Integration
- "NEXT CARD" button uses `hx-post="/next-card"` 
- Target: `#card-display` (card container)
- Swap strategy: `innerHTML swap:0.3s` for smooth transition
- Server returns only the card component (partial template)

### Performance
- Single question shuffle at start (O(n) once)
- Card navigation is O(1) lookup
- No database queries per card tap
- CSS animations are GPU-accelerated

## Design Decisions

1. **Single Card Focus**: One question per screen emphasis (no multiple-choice distractions)
2. **Continuous Play**: No win condition allows party host to control session length
3. **Tap-to-Advance**: HTMX button eliminates page reloads—instant feedback
4. **Cyclic Shuffle**: Wraps to start rather than stopping at end (endless fun)
5. **Arcade Aesthetic**: Intense neon glows, pulsing animations, scanlines match project theme
6. **Large Typography**: Question text sized for visibility across mixer rooms

## Future Enhancements
- Add question difficulty levels / categories
- Track time-per-question for speedrun challenges
- Multiplayer "question duelists" mode
- Custom question deck uploads
- Category/theme filtering
- Sound effects on card reveal

---
*Last updated: 2026-04-21 — Implementation Complete*
*Status: Ready for user feedback*
