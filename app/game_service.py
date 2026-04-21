from dataclasses import dataclass, field

from app.game_logic import (
    check_bingo,
    generate_board,
    generate_scavenger_items,
    get_winning_square_ids,
    toggle_square,
)
from app.models import (
    BingoLine,
    BingoSquareData,
    GameMode,
    GameState,
    ScavengerItem,
)


@dataclass
class GameSession:
    """Holds the state for a single game session."""

    game_state: GameState = GameState.START
    game_mode: GameMode = GameMode.BINGO
    board: list[BingoSquareData] = field(default_factory=list)
    scavenger_items: list[ScavengerItem] = field(default_factory=list)
    winning_line: BingoLine | None = None
    show_bingo_modal: bool = False

    @property
    def winning_square_ids(self) -> set[int]:
        return get_winning_square_ids(self.winning_line)

    @property
    def has_bingo(self) -> bool:
        return self.game_state == GameState.BINGO

    def start_game(self, mode: GameMode = GameMode.BINGO) -> None:
        self.game_mode = mode
        self.game_state = GameState.PLAYING
        self.winning_line = None
        self.show_bingo_modal = False

        if mode == GameMode.BINGO:
            self.board = generate_board()
            self.scavenger_items = []
        else:  # SCAVENGER_HUNT
            self.scavenger_items = generate_scavenger_items()
            self.board = []

    def handle_square_click(self, square_id: int) -> None:
        if self.game_state != GameState.PLAYING or self.game_mode != GameMode.BINGO:
            return
        self.board = toggle_square(self.board, square_id)

        if self.winning_line is None:
            bingo = check_bingo(self.board)
            if bingo is not None:
                self.winning_line = bingo
                self.game_state = GameState.BINGO
                self.show_bingo_modal = True

    def handle_scavenger_toggle(self, item_id: str) -> None:
        if (
            self.game_state != GameState.PLAYING
            or self.game_mode != GameMode.SCAVENGER_HUNT
        ):
            return
        self.scavenger_items = [
            item.model_copy(update={"is_marked": not item.is_marked})
            if item.id == item_id
            else item
            for item in self.scavenger_items
        ]

    def get_scavenger_progress(self) -> tuple[int, int]:
        """Return (marked_count, total_count) for scavenger hunt."""
        total = len(self.scavenger_items)
        marked = sum(1 for item in self.scavenger_items if item.is_marked)
        return (marked, total)

    def reset_game(self) -> None:
        self.game_state = GameState.START
        self.board = []
        self.scavenger_items = []
        self.game_mode = GameMode.BINGO
        self.winning_line = None
        self.show_bingo_modal = False

    def dismiss_modal(self) -> None:
        self.show_bingo_modal = False
        self.game_state = GameState.PLAYING


# In-memory session store keyed by session ID
_sessions: dict[str, GameSession] = {}


def get_session(session_id: str) -> GameSession:
    """Get or create a game session for the given session ID."""
    if session_id not in _sessions:
        _sessions[session_id] = GameSession()
    return _sessions[session_id]
