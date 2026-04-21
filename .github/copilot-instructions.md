---
applyTo: "**"
---

# Soc Ops – Copilot Instructions

Social Bingo game for in-person mixers (FastAPI + Jinja2 + HTMX).

## 🔴 Mandatory Before Commit

```bash
uv run ruff check .      # Lint
uv run pytest            # Test
uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000  # Run
```

All must pass. ✅

## Quick Start

```bash
uv sync                  # Install dependencies (Python 3.13+)
uv run pytest            # Run tests
uv run ruff check .      # Lint
```

## Architecture

```
app/
├── main.py              # FastAPI routes & HTMX endpoints
├── models.py            # Pydantic models
├── game_logic.py        # Board generation & bingo detection
├── game_service.py      # Session management (signed cookies)
├── data.py              # Question bank
├── templates/           # Jinja2 templates + HTMX partials
└── static/css/app.css   # Custom utility classes

tests/
├── test_api.py          # API tests (httpx + TestClient)
└── test_game_logic.py   # Unit tests
```

## Key Conventions

- **State**: `GameSession` server-side, persisted via itsdangerous cookies
- **UI Updates**: HTMX partial templates, no full page reloads
- **Styling**: Custom CSS utilities only (`.flex`, `.grid`, `.p-4`, `.bg-accent`, etc.)
- **Type Hints**: All functions & variables must be typed
- **Testing**: Use `pytest` + `httpx.TestClient`

## Design System: 1980s Arcade Neon

### Aesthetic
**Era**: 1980s arcade cabinets (Pac-Man, Donkey Kong) with neon glow effects, scanlines, and bold typography. Dark backgrounds with bright, glowing neon text. Aggressive animations (flashing, wobbling, pulsing) create an authentic arcade feel.

### Color Palette (CSS Variables)
```css
--neon-pink:       #FF0099        /* Primary accent, titles, winning states */
--neon-cyan:       #00FFFF        /* Text, borders, UI elements */
--neon-lime:       #00FF00        /* Marked squares, success states */
--neon-purple:     #9D00FF        /* Secondary accent (optional) */
--neon-orange:     #FF6600        /* Alternative accent */
--arcade-dark:     #0a0a0a        /* Main background */
--arcade-dark-2:   #1a1a2e        /* Elevated backgrounds */
--arcade-dark-3:   #16213e        /* Alternative dark shades */
```

Use via: `color: var(--neon-pink);` or apply color utilities:
- Text: `.text-neon-pink`, `.text-neon-cyan`, `.text-neon-lime`, etc.
- Glowing text: `.glow-pink`, `.glow-cyan`, `.glow-lime`

### Typography
- **Font**: Courier Prime Bold (monospace, imported from Google Fonts)
- **Style**: Uppercase, bold, letter-spacing 2px for arcade feel
- **Classes**: 
  - `.neon-text` — uppercase, bold (700), 2px letter-spacing
  - `.text-xs` through `.text-5xl` — size hierarchy
  - `.font-bold` — always use for arcade text

### Arcade Effects & Utilities

#### Borders & Frames
- `.arcade-bezel` — 8px border with cyan glow, inset shadow, 30px outer glow (cabinet frame effect)
- `.arcade-border` — 3px border with subtle cyan glow (smaller UI elements)
- `.border` — now 2px (thicker for arcade feel)

#### Glow Effects (Text)
- `.glow-pink` — electric pink text with triple-layered text-shadow glow
- `.glow-cyan` — cyan text with triple-layered text-shadow glow
- `.glow-lime` — lime green text with triple-layered text-shadow glow

#### Bingo Board Squares
- `.arcade-square-unmarked` — dark background, cyan outline, 10px inset glow
- `.arcade-square-marked` — light lime background (15% opacity), lime border, 15px glow
- `.arcade-square-winning` — light pink background (20% opacity), pink border (3px), 25px glow, pulsing animation

#### Shadow/Glow (on modern elements)
- `.shadow-sm` — now renders as cyan glow instead of subtle shadow
- `.shadow-xl` — strong cyan + pink glow for emphasis

### Animations

#### Keyframe Animations
- `glow-pulse` (2s) — fades glow intensity, simulates neon flicker
- `flashing` (0.5s) — rapid on/off, 50% opacity
- `wobble` (0.6s) — slight rotate/scale variation
- `glitch` (0.3s) — chromatic aberration with cyan/pink offset
- `scan-flicker` (0.15s) — scanline intensity flicker

#### Animation Classes
Apply via `class="animate-glow-pulse animate-flashing"` etc.
- `.animate-glow-pulse` — constant glow intensity pulse
- `.animate-flashing` — rapid blinking
- `.animate-wobble` — rotation + scale wobble
- `.animate-glitch` — offset glitch effect
- `.animate-scan-flicker` — scanline animation

#### Scanline Overlay
- **Global**: Semi-transparent horizontal lines overlay entire page via `body::before` pseudo-element
- **Effect**: Creates CRT/old monitor aesthetic, 1px lines with 2px gap, 30% opacity

### How to Use in Templates

#### Example: Arcade Button
```html
<button class="bg-accent text-gray-100 font-bold py-4 px-8 rounded text-lg 
                active:bg-neon-orange transition-all duration-150 
                animate-flashing neon-text">
    ▶ START GAME ◀
</button>
```

#### Example: Glowing Title
```html
<h1 class="text-5xl font-bold glow-pink mb-4 neon-text animate-wobble">
    SOC OPS
</h1>
```

#### Example: Arcade Card
```html
<div class="arcade-bezel p-8 rounded-lg">
    <h2 class="glow-cyan text-center neon-text">HOW TO PLAY:</h2>
    <ul class="space-y-2">
        <li class="glow-cyan">Find people who match</li>
    </ul>
</div>
```

#### Example: Bingo Grid
```html
<div class="grid grid-cols-5 gap-1">
    {% for square in board %}
    <button class="arcade-square-unmarked 
                   {% if square.is_marked %}arcade-square-marked{% endif %}
                   {% if is_winning %}arcade-square-winning{% endif %}">
        {{ square.text }}
    </button>
    {% endfor %}
</div>
```

### Accessibility

#### Reduced Motion Support
- **Automatic**: CSS includes `@media (prefers-reduced-motion: reduce)` — animations disable for users who prefer it
- **No action needed**: Framework handles via 0.01ms duration/iteration fallback

#### Color Contrast
- Neon cyan (00FFFF) on dark background (0a0a0a): High contrast ✅
- Neon pink (FF0099) on dark background: High contrast ✅
- Neon lime (00FF00) on dark background: High contrast ✅
- All colors meet WCAG AA standards for accessibility

#### Text Readability
- Glow effects use `text-shadow` (no background distortion)
- Uppercase + bold + letter-spacing improves scannability
- Use `.text-xs` to `.text-lg` for body text; avoid `.text-3xl+` for small screens

### Best Practices

1. **Consistency**: Use neon colors from CSS variables, not inline hex values
2. **Animation Restraint**: 1-2 animations per component max (avoid overwhelming)
3. **Text Hierarchy**: Titles → `.text-5xl.glow-pink.animate-wobble`; body → `.text-sm.glow-cyan`
4. **Mobile**: Test arcade borders/glows on small screens; they may need margin adjustments
5. **Performance**: Scanline overlay is static (no performance impact); test animation smoothness on older devices
6. **New Utilities**: If adding arcade effects, follow naming: `.arcade-*` for structural, `.glow-*` for text effects

### Files to Modify for Design Changes
- `app/static/css/app.css` — Color variables, animation keyframes, arcade utilities
- `app/templates/components/*.html` — Apply arcade classes to UI
- `.github/instructions/css-utilities.instructions.md` — Document new utilities added
- Update this section if adding new colors, animations, or effects

## Related Documentation

- [General Rules](instructions/general.instructions.md) — No VS Code Simple Browser
- [CSS Utilities](instructions/css-utilities.instructions.md) — Available classes & patterns
- [Frontend Design](instructions/frontend-design.instructions.md) — Avoid AI aesthetics
- [README.md](../README.md) — Project overview & workshop guides

## Agents

- `@quiz-master` — Create icebreaker questions
- `@tdd` — Test-driven development
- `@ui-review` — Design critique
- `@pixel-jam` — Visual polish

## Setup

Run `@setup` prompt for full development environment setup.
