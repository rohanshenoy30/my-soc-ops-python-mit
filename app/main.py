import uuid
from pathlib import Path

from fastapi import FastAPI, Request, Response
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware

from app.game_service import GameSession, get_session
from app.models import GameMode, GameState

BASE_DIR = Path(__file__).resolve().parent

app = FastAPI(title="Soc Ops - Social Bingo")
app.add_middleware(SessionMiddleware, secret_key="soc-ops-secret-key")
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")

templates = Jinja2Templates(directory=BASE_DIR / "templates")


def _get_game_session(request: Request) -> GameSession:
    """Get or create a game session using cookie-based sessions."""
    if "session_id" not in request.session:
        request.session["session_id"] = uuid.uuid4().hex
    return get_session(request.session["session_id"])


@app.get("/", response_class=HTMLResponse)
async def home(request: Request) -> Response:
    session = _get_game_session(request)
    return templates.TemplateResponse(
        request,
        "home.html",
        {"session": session, "GameState": GameState, "GameMode": GameMode},
    )


@app.post("/start", response_class=HTMLResponse)
async def start_game(request: Request) -> Response:
    session = _get_game_session(request)
    session.start_game()
    template = (
        "components/scavenger_hunt_screen.html"
        if session.game_mode == GameMode.SCAVENGER_HUNT
        else "components/game_screen.html"
    )
    return templates.TemplateResponse(request, template, {"session": session})


@app.post("/start/{mode}", response_class=HTMLResponse)
async def start_game_with_mode(request: Request, mode: str) -> Response:
    session = _get_game_session(request)
    game_mode = GameMode(mode)
    session.start_game(mode=game_mode)
    template = (
        "components/scavenger_hunt_screen.html"
        if game_mode == GameMode.SCAVENGER_HUNT
        else "components/game_screen.html"
    )
    return templates.TemplateResponse(request, template, {"session": session})


@app.post("/toggle/{item_id}", response_class=HTMLResponse)
async def toggle_square(request: Request, item_id: str) -> Response:
    session = _get_game_session(request)

    if session.game_mode == GameMode.BINGO:
        # For bingo, item_id is an integer index
        session.handle_square_click(int(item_id))
        template = "components/game_screen.html"
    else:  # SCAVENGER_HUNT
        # For scavenger hunt, item_id is a string
        session.handle_scavenger_toggle(item_id)
        template = "components/scavenger_hunt_screen.html"

    return templates.TemplateResponse(request, template, {"session": session})


@app.post("/reset", response_class=HTMLResponse)
async def reset_game(request: Request) -> Response:
    session = _get_game_session(request)
    session.reset_game()
    return templates.TemplateResponse(
        request,
        "components/start_screen.html",
        {"session": session, "GameState": GameState},
    )


@app.post("/dismiss-modal", response_class=HTMLResponse)
async def dismiss_modal(request: Request) -> Response:
    session = _get_game_session(request)
    session.dismiss_modal()
    return templates.TemplateResponse(
        request, "components/game_screen.html", {"session": session}
    )


def run() -> None:
    """Entry point for the application."""
    import uvicorn

    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
