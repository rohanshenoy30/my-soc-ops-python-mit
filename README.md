# 🎉 Soc Ops – Social Bingo for Mixers

**Break the ice. Have fun. Play bingo.**

Soc Ops is an interactive web-based bingo game designed to get people talking at in-person mixers, conferences, and social events. Players match their peers to custom bingo questions and race to get 5 in a row—encouraging genuine connection and conversation.

[Live Demo](#quick-start) • [Features](#features) • [Get Started](#getting-started) • [Build with Copilot](#copilot-lab)

---

## ✨ Features

🎮 **Interactive Bingo Board**  
Dynamic 5×5 bingo grid with randomized questions each game

👥 **Social Prompts**  
Icebreaker questions designed to spark conversations ("Find someone who loves karaoke", "Find someone learning to code")

⚡ **Real-Time Updates**  
HTMX-powered UI refreshes instantly without page reloads

🎯 **Instant Win Detection**  
Automatically detects bingo (5 in a row, column, or diagonal) and celebrates your win

📱 **Mobile Friendly**  
Works seamlessly on phones, tablets, and desktops—perfect for events

🔐 **Session-Based**  
Secure game state management with signed cookies; no database required

---

## 🚀 Quick Start

### Prerequisites
- Python 3.13+
- `uv` package manager

### Installation

```bash
# Clone the repo
git clone https://github.com/rohanshenoy30/my-soc-ops-python-mit
cd my-soc-ops-python-mit

# Install dependencies
uv sync

# Run the app
uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Open `http://localhost:8000` in your browser and start playing!

---

## 🎓 Copilot Lab

This project is a hands-on learning experience for **GitHub Copilot** development. Follow the guided labs to build features, customize the game, and master AI-assisted development.

### Lab Modules

| Part | Title | Learn |
|------|-------|-------|
| [**00**](https://copilot-dev-days.github.io/agent-lab-python/docs/step.html?step=00-overview) | Overview & Checklist | Project setup & prerequisites |
| [**01**](https://copilot-dev-days.github.io/agent-lab-python/docs/step.html?step=01-setup) | Setup & Context Engineering | Custom Copilot instructions |
| [**02**](https://copilot-dev-days.github.io/agent-lab-python/docs/step.html?step=02-design) | Design-First Frontend | Build UI with Copilot |
| [**03**](https://copilot-dev-days.github.io/agent-lab-python/docs/step.html?step=03-quiz-master) | Custom Quiz Master | Create AI agents with skills |
| [**04**](https://copilot-dev-days.github.io/agent-lab-python/docs/step.html?step=04-multi-agent) | Multi-Agent Development | Orchestrate multiple agents |

> 📖 Lab guides are also available offline in the [`workshop/`](workshop/) folder.

---

## 🛠 Tech Stack

- **Framework**: [FastAPI](https://fastapi.tiangolo.com/) – Fast, modern Python web framework
- **Templating**: [Jinja2](https://jinja.palletsprojects.com/) – Powerful template engine
- **Interactivity**: [HTMX](https://htmx.org/) – Dynamic UI without JavaScript
- **Session Management**: [itsdangerous](https://itsdangerous.palletsprojects.com/) – Cryptographically signed cookies
- **Styling**: Custom CSS utilities (Tailwind-inspired)

---

## 📁 Project Structure

```
app/
├── main.py              # FastAPI routes & HTMX endpoints
├── models.py            # Pydantic data models
├── game_logic.py        # Board generation & bingo detection
├── game_service.py      # Session management
├── data.py              # Question bank
├── templates/           # Jinja2 templates + HTMX partials
└── static/              # CSS & assets

tests/                   # Pytest test suite
workshop/                # Lab guides (offline)
docs/                    # Documentation
```

---

## 🧪 Development

### Run Tests
```bash
uv run pytest
```

### Lint Code
```bash
uv run ruff check .
```

### Format Code
```bash
uv run ruff format .
```

### Full Development Checklist
```bash
uv sync                  # Install dependencies
uv run ruff check .      # Lint
uv run pytest            # Test
uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000  # Run
```

---

## 🌍 Languages

- 🇬🇧 [English](README.md)
- 🇧🇷 [Português (BR)](README.pt_BR.md)
- 🇪🇸 [Español](README.es.md)

---

## 📝 Contributing

We welcome contributions! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

---

## 📄 License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

---

## 🤝 Support

Have questions? Check out [SUPPORT.md](SUPPORT.md) or open an [issue](https://github.com/rohanshenoy30/my-soc-ops-python-mit/issues).
