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


def _get_game_template(game_mode: GameMode) -> str:
    """Get the appropriate template for the given game mode."""
    if game_mode == GameMode.SCAVENGER_HUNT:
        return "components/scavenger_hunt_screen.html"
    elif game_mode == GameMode.CARD_DECK_SHUFFLE:
        return "components/card_deck_screen.html"
    else:  # BINGO
        return "components/game_screen.html"


def _render_game(request: Request, session: GameSession) -> Response:
    """Render the game screen based on current session state."""
    template = _get_game_template(session.game_mode)
    return templates.TemplateResponse(request, template, {"session": session})


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
    return _render_game(request, session)


@app.post("/start/{mode}", response_class=HTMLResponse)
async def start_game_with_mode(request: Request, mode: str) -> Response:
    session = _get_game_session(request)
    try:
        game_mode = GameMode(mode)
    except ValueError:
        # Invalid mode, return error response
        return Response(
            content='{"detail":"Not Found"}',
            status_code=422,
            media_type="application/json",
        )
    session.start_game(mode=game_mode)
    return _render_game(request, session)


@app.post("/toggle/{item_id}", response_class=HTMLResponse)
async def toggle_square(request: Request, item_id: str) -> Response:
    session = _get_game_session(request)

    if session.game_mode == GameMode.BINGO:
        # For bingo, item_id is an integer index
        session.handle_square_click(int(item_id))
    else:  # SCAVENGER_HUNT
        # For scavenger hunt, item_id is a string
        session.handle_scavenger_toggle(item_id)

    return _render_game(request, session)


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


@app.post("/next-card", response_class=HTMLResponse)
async def next_card(request: Request) -> Response:
    session = _get_game_session(request)
    session.next_card()
    # Return the card component partial
    return templates.TemplateResponse(
        request, "components/card.html", {"session": session}
    )


def run() -> None:
    """Entry point for the application."""
    import uvicorn

    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
