# 🎉 Soc Ops – Social Bingo for Mixers

**Break the ice. Have fun. Play bingo.**

Soc Ops is an interactive web-based social bingo game that gets people talking at in-person mixers, conferences, and events. Players match their peers to custom icebreaker prompts and race to complete bingo patterns—encouraging genuine connection and conversation through gamification.

Built with **FastAPI**, **HTMX**, and **Jinja2** for a modern, interactive experience with zero page reloads.

**[Live Demo](#quick-start) • [How It Works](#-how-it-works) • [Game Modes](#-game-modes) • [Features](#-features) • [Get Started](#-getting-started) • [Documentation](#-documentation)**

---

## ✨ Features

🎮 **Three Game Modes**  
Choose between classic Bingo, Scavenger Hunt, or Card Deck Shuffle

📋 **Randomized Bingo Board**  
Dynamic 5×5 grid with shuffled icebreaker questions—no two games are the same

👥 **Social Icebreakers**  
25+ conversation-starting prompts: "Find someone learning to code", "Find someone who loves karaoke", etc.

⚡ **Real-Time Updates (HTMX)**  
Frictionless interactions—no page reloads, no waiting. Click, mark, win.

🎯 **Automatic Win Detection**  
Instantly recognizes 5-in-a-row patterns (rows, columns, diagonals) and celebrates your victory

📱 **Mobile-Optimized**  
Fully responsive design—plays perfectly on phones, tablets, and desktops

🌙 **1980s Arcade Aesthetic**  
Neon cyan, pink, and lime colors with glowing text, scanline effects, and retro animations

🔐 **No Backend Storage**  
Session-based state management using signed cookies—no database, no privacy concerns

✅ **Accessibility**  
Semantic HTML, ARIA labels, high contrast neon colors (WCAG compliant), keyboard navigation support

---

## 🎮 How It Works

### Game Flow
1. **Home Screen** – Player selects a game mode (Bingo, Scavenger Hunt, or Card Deck)
2. **Board Generated** – FastAPI generates a random 5×5 board from 24 icebreaker prompts
3. **Find & Mark** – Player finds other people who match the prompts and marks squares
4. **Win Condition** – Complete 5 in a row (horizontally, vertically, or diagonally)
5. **Victory Screen** – Celebrate with arcade animations and glowing effects

### Session State
- Game board, marked squares, and win status are stored in **signed cookies** (via itsdangerous)
- No database required—perfectly suited for events where you spin up/down at will
- Each player gets a unique session; board persists across page refreshes

---

## 🕹 Game Modes

### 1. **Bingo** (Classic Mode)
- Traditional 5×5 bingo board
- Find people matching each prompt and mark the square
- Win when you get 5 in a row (rows, columns, or diagonals)
- **Best for:** Large mixers, high energy

### 2. **Scavenger Hunt**
- Find as many people as possible matching all 24 prompts
- Progress meter tracks how many you've found (0/24)
- No "win" condition—more about exploration and connection
- **Best for:** Longer events, emphasis on mingling

### 3. **Card Deck Shuffle**
- Flip individual cards to reveal prompts
- Find matching people, flip pairs to keep them
- Match all pairs to complete the game
- **Best for:** Small groups, one-on-one interaction

---

## 🚀 Quick Start

### Prerequisites
- **Python 3.13+** (or your preferred version)
- **`uv` package manager** – Fast, intuitive Python project manager
  - Install: `curl -LsSf https://astral.sh/uv/install.sh | sh`

### Installation

```bash
# Clone the repository
git clone https://github.com/rohanshenoy30/my-soc-ops-python-mit
cd my-soc-ops-python-mit

# Install dependencies using uv
uv sync

# Run the development server
uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Open **`http://localhost:8000`** in your browser.

### Using Conda (Alternative)
If you prefer Conda over `uv`:

```bash
conda create -n soc-ops python=3.13
conda activate soc-ops
pip install -r requirements.txt  # Generated from pyproject.toml
uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

---

## 📁 Project Structure

```
soc-ops/
├── app/
│   ├── main.py                    # FastAPI routes & endpoints
│   ├── models.py                  # Pydantic models (GameState, GameMode, Board)
│   ├── game_logic.py              # Board generation & win detection
│   ├── game_service.py            # Session management (signed cookies)
│   ├── data.py                    # Question bank (25 prompts)
│   ├── templates/
│   │   ├── base.html              # Base template (HTML skeleton)
│   │   ├── home.html              # Landing page
│   │   ├── components/
│   │   │   ├── hero.html          # Hero section
│   │   │   ├── preview_board.html # "How to play" preview
│   │   │   ├── start_screen.html  # Mode selection
│   │   │   ├── game_screen.html   # Bingo board [HTMX swap target]
│   │   │   ├── scavenger_hunt_screen.html  # Scavenger hunt board
│   │   │   ├── card_deck_screen.html       # Card deck game
│   │   │   ├── bingo_board.html   # Reusable board component
│   │   │   ├── progress_meter.html # Progress display
│   │   │   ├── card.html          # Card deck component
│   │   │   ├── features.html      # Feature callouts
│   │   │   ├── questions.html     # Sample questions list
│   │   │   └── bingo_modal.html   # Win modal
│   │   └── ...
│   └── static/
│       ├── css/
│       │   └── app.css            # Custom arcade utilities + animations
│       ├── js/
│       │   └── htmx.min.js        # HTMX library (unmodified)
│       └── favicon.png
│
├── tests/
│   ├── test_api.py                # Integration tests (httpx.TestClient)
│   └── test_game_logic.py         # Unit tests (board generation, win detection)
│
├── workshop/                      # Offline lab guides (markdown)
│   ├── 00-overview.md
│   ├── 01-setup.md
│   ├── 02-design.md
│   ├── 03-quiz-master.md
│   ├── 04-multi-agent.md
│   └── GUIDE.md
│
├── docs/                          # Static docs (future: GitHub Pages)
│   └── step.html                  # Step-by-step guides
│
├── .github/
│   ├── workflows/
│   │   └── deploy.yml             # CI/CD pipeline (tests, lint, build)
│   ├── copilot-instructions.md    # Copilot context config
│   └── instructions/
│       ├── general.instructions.md
│       ├── css-utilities.instructions.md
│       └── frontend-design.instructions.md
│
├── pyproject.toml                 # Project metadata & dependencies (uv managed)
├── README.md                      # This file
└── ...
```

---

## 🛠 Tech Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| **Backend** | [FastAPI](https://fastapi.tiangolo.com/) | Modern Python web framework, type hints, auto-docs |
| **Templating** | [Jinja2](https://jinja.palletsprojects.com/) | Server-side templating with template inheritance |
| **Interactivity** | [HTMX](https://htmx.org/) | Dynamic UI without writing JavaScript |
| **Sessions** | [itsdangerous](https://itsdangerous.palletsprojects.com/) | Cryptographically signed cookies for session state |
| **Styling** | Custom CSS | Tailwind-inspired utility classes + arcade animations |
| **Type Safety** | [Pydantic v2](https://docs.pydantic.dev/) | Runtime data validation & IDE autocomplete |
| **Testing** | [pytest](https://pytest.org/) + [httpx](https://www.python-httpx.org/) | Fast, intuitive testing framework |
| **Linting** | [Ruff](https://docs.astral.sh/ruff/) | Blazing-fast Python linter & formatter |

---

## 🎨 Design System – 1980s Arcade Neon

Every element follows an intentional 80s arcade aesthetic:

### Colors (CSS Variables)
```css
--neon-pink:    #FF0099        /* Titles, winning states */
--neon-cyan:    #00FFFF        /* Tags, borders, text */
--neon-lime:    #00FF00        /* Marked squares, success */
--arcade-dark:  #0a0a0a        /* Main background */
--arcade-dark-2: #1a1a2e       /* Elevated surfaces */
```

### Effects
- **Glow Text:** Triple-layered text-shadow for authentic neon glow
- **Arcade Borders:** 8px thick cyan borders with inset glows
- **Scanline Overlay:** 1px horizontal lines across entire page (CRT monitor effect)
- **Animations:** Wobble, flashing, glitch, glow-pulse with `prefers-reduced-motion` support

### Typography
- **Font:** Courier Prime (monospace, bold)
- **Style:** UPPERCASE, 2px letter-spacing
- **Scale:** `.text-xs` to `.text-5xl` hierarchy

See [.github/instructions/css-utilities.instructions.md](.github/instructions/css-utilities.instructions.md) for full utility class reference.

---

## 🧪 Development

### Prerequisites
Before starting, ensure you have:
- Python 3.13+
- `uv` installed

### Standard Workflow

```bash
# 1. Install dependencies
uv sync

# 2. Run linter (must pass before commit)
uv run ruff check .

# 3. Run tests (must pass before commit)
uv run pytest

# 4. Start dev server with hot reload
uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# 5. Visit http://localhost:8000
```

### Common Commands

| Command | Purpose |
|---------|---------|
| `uv sync` | Install/update dependencies |
| `uv run pytest` | Run all tests (show coverage: `--cov=app`) |
| `uv run pytest tests/test_game_logic.py -v` | Run specific test file with verbose output |
| `uv run ruff check .` | Lint code and show violations |
| `uv run ruff format .` | Auto-format code |
| `uv run uvicorn app.main:app --reload` | Start dev server with hot reload |

### Pre-Commit Checklist (Mandatory)
```bash
# Run ALL THREE before pushing to main
uv run ruff check .      # ✅ Must pass
uv run pytest            # ✅ Must pass
uv run uvicorn app.main:app --reload  # ✅ Start & verify manually
```

---

## 🧩 Customizing Questions

The icebreaker prompts are stored in [app/data.py](app/data.py):

```python
QUESTIONS: Final[list[str]] = [
    "has a pet with a funny name",
    "prefers coffee over tea (or vice versa)",
    # ... 23 more prompts
]
```

### Add/Edit Prompts
1. Open `app/data.py`
2. Add or replace items in the `QUESTIONS` list
3. Keep exactly **24 prompts** (needed for board generation)
4. Keep prompts **20–50 characters** for best UX
5. Format: "Find someone who..." (statement form)

### Examples of Good Prompts
✅ "has beaten someone at video games"  
✅ "can play a musical instrument"  
✅ "speaks more than 2 languages"

✗ "Does your dog bite?" (yes/no question)  
✗ "Has a really incredibly long story about something" (too long)

---

## 🚢 Deployment

### Development vs. Production
This is a **full-stack Python web app**—it requires a server that can run Python/FastAPI.

**GitHub Pages alone won't work** (static hosting only). Choose an alternative:

| Platform | Cost | Setup | Best For |
|----------|------|-------|----------|
| [Railway](https://railway.app) | $5–20/mo | 2 min, auto-deploy from GitHub | Beginners, quick launches |
| [Render](https://render.com) | Free tier + $7/mo | 5 min, easy GitHub integration | Learning, small projects |
| [Fly.io](https://fly.io) | Free tier + pay-as-you-go | 10 min, Docker-native | Scalability, global deployment |
| [Heroku](https://heroku.com) | Paid only (~$7/mo+) | 5 min | Legacy choice, reliable |

### Quick Deploy to Railway
```bash
# 1. Install railway CLI: https://railway.app/cli
# 2. Login
railway login

# 3. Initialize project and deploy
railway init
railway up
```

Railway auto-detects FastAPI and deploys. Done! 🚀

---

## 🧑‍💻 Contributing

We welcome contributions! Follow these steps:

1. **Fork** the repository
2. **Create a feature branch:** `git checkout -b feature/my-feature`
3. **Make changes** and pass checks:
   ```bash
   uv run ruff check .
   uv run pytest
   ```
4. **Commit** with clear, descriptive messages
5. **Push** to your fork and open a **Pull Request**

See [CONTRIBUTING.md](CONTRIBUTING.md) for details.

---

## 📚 Documentation

### In-Repo Documentation
- [workshop/GUIDE.md](workshop/GUIDE.md) – Full workshop walkthrough (offline)
- [.github/copilot-instructions.md](.github/copilot-instructions.md) – Copilot context for development
- [.github/instructions/css-utilities.instructions.md](.github/instructions/css-utilities.instructions.md) – CSS class reference
- [.github/instructions/frontend-design.instructions.md](.github/instructions/frontend-design.instructions.md) – Design system documentation

### API Documentation
FastAPI auto-generates interactive API docs:
- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

---

## 🌍 Languages

- 🇬🇧 [English](README.md)
- 🇧🇷 [Português Brasileiro](README.pt_BR.md)
- 🇪🇸 [Español](README.es.md)

---

## 📖 Lab Guides – Learn with Copilot

This project includes interactive **GitHub Copilot** lab modules. Follow along to learn AI-assisted development:

| Lab | Topic | Learn |
|-----|-------|-------|
| **00** | [Overview & Checklist](workshop/00-overview.md) | Project structure, tasks |
| **01** | [Setup & Context Engineering](workshop/01-setup.md) | Copilot instructions, `.instructions` files |
| **02** | [Design-First Frontend](workshop/02-design.md) | Build UI with Claude, arcade aesthetic |
| **03** | [Custom Quiz Master](workshop/03-quiz-master.md) | Create agents with `.skills` |
| **04** | [Multi-Agent Development](workshop/04-multi-agent.md) | Orchestrate specialized agents |
| **05** | [Complete Workshop](workshop/05-complete.md) | End-to-end capstone project |

👉 **Start here:** [workshop/GUIDE.md](workshop/GUIDE.md)

---

## 📝 License

This project is licensed under the **MIT License**. See [LICENSE](LICENSE) for details.

---

## 🤝 Code of Conduct

We are committed to providing a welcoming and inclusive environment. See [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md).

---

## 💬 Questions or Issues?

- **Bug report?** Open an [issue](https://github.com/rohanshenoy30/my-soc-ops-python-mit/issues)
- **Feature request?** Start a [discussion](https://github.com/rohanshenoy30/my-soc-ops-python-mit/discussions)
- **Want to contribute?** See [CONTRIBUTING.md](CONTRIBUTING.md)

---

## 🎯 Project Goals

✅ **Educational** – Learn modern Python web development with Copilot  
✅ **Practical** – Deploy a real, working game for your next event  
✅ **Accessible** – Works on any device, no special requirements  
✅ **Fun** – 1980s arcade aesthetic that makes people smile  

---

**Made with ❤️ for mixers, conferences, and developers learning AI-assisted development.**
