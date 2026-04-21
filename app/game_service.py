import random
from dataclasses import dataclass, field

from app.data import QUESTIONS
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
    card_questions: list[str] = field(default_factory=list)
    current_card_index: int = 0

    @property
    def winning_square_ids(self) -> set[int]:
        return get_winning_square_ids(self.winning_line)

    @property
    def has_bingo(self) -> bool:
        return self.game_state == GameState.BINGO

    def _reset_state(self) -> None:
        """Reset common game state fields."""
        self.winning_line = None
        self.show_bingo_modal = False

    def _is_mode_playing(self, expected_mode: GameMode) -> bool:
        """Check if the game is in PLAYING state with the expected mode."""
        return self.game_state == GameState.PLAYING and self.game_mode == expected_mode

    def start_game(self, mode: GameMode = GameMode.BINGO) -> None:
        self.game_mode = mode
        self.game_state = GameState.PLAYING
        self._reset_state()

        if mode == GameMode.BINGO:
            self.board = generate_board()
            self.scavenger_items = []
            self.card_questions = []
            self.current_card_index = 0
        elif mode == GameMode.SCAVENGER_HUNT:
            self.scavenger_items = generate_scavenger_items()
            self.board = []
            self.card_questions = []
            self.current_card_index = 0
        elif mode == GameMode.CARD_DECK_SHUFFLE:
            # Shuffle all questions for random deck
            self.card_questions = QUESTIONS.copy()
            random.shuffle(self.card_questions)
            self.current_card_index = 0
            self.board = []
            self.scavenger_items = []

    def handle_square_click(self, square_id: int) -> None:
        if not self._is_mode_playing(GameMode.BINGO):
            return
        self.board = toggle_square(self.board, square_id)

        if self.winning_line is None:
            bingo = check_bingo(self.board)
            if bingo is not None:
                self.winning_line = bingo
                self.game_state = GameState.BINGO
                self.show_bingo_modal = True

    def handle_scavenger_toggle(self, item_id: str) -> None:
        if not self._is_mode_playing(GameMode.SCAVENGER_HUNT):
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
        self._reset_state()

    def dismiss_modal(self) -> None:
        self.show_bingo_modal = False
        self.game_state = GameState.PLAYING

    def get_current_card(self) -> str:
        """Get the current card question."""
        if not self._is_mode_playing(GameMode.CARD_DECK_SHUFFLE):
            return ""
        if 0 <= self.current_card_index < len(self.card_questions):
            return self.card_questions[self.current_card_index]
        return ""

    def next_card(self) -> str:
        """Advance to the next card. Cycles back to start if at the end."""
        if not self._is_mode_playing(GameMode.CARD_DECK_SHUFFLE):
            return ""
        self.current_card_index = (self.current_card_index + 1) % len(
            self.card_questions
        )
        return self.get_current_card()


# In-memory session store keyed by session ID
_sessions: dict[str, GameSession] = {}


def get_session(session_id: str) -> GameSession:
    """Get or create a game session for the given session ID."""
    if session_id not in _sessions:
        _sessions[session_id] = GameSession()
    return _sessions[session_id]
