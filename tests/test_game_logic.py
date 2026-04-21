from app.data import FREE_SPACE, QUESTIONS
from app.game_logic import (
    CENTER_INDEX,
    check_bingo,
    generate_board,
    get_winning_square_ids,
    toggle_square,
)
from app.models import BingoLine, BingoSquareData


class TestGenerateBoard:
    def test_board_has_25_squares(self):
        board = generate_board()
        assert len(board) == 25

    def test_center_is_free_space(self):
        board = generate_board()
        center = board[CENTER_INDEX]
        assert center.is_free_space is True
        assert center.is_marked is True
        assert center.text == FREE_SPACE

    def test_non_center_squares_are_not_free_space(self):
        board = generate_board()
        for i, square in enumerate(board):
            if i != CENTER_INDEX:
                assert square.is_free_space is False
                assert square.is_marked is False

    def test_all_questions_from_pool(self):
        board = generate_board()
        texts = {s.text for s in board if not s.is_free_space}
        assert texts.issubset(set(QUESTIONS))

    def test_squares_have_sequential_ids(self):
        board = generate_board()
        for i, square in enumerate(board):
            assert square.id == i

    def test_board_is_shuffled(self):
        """Verify two boards aren't identical (high probability)."""
        board1 = generate_board()
        board2 = generate_board()
        texts1 = [s.text for s in board1]
        texts2 = [s.text for s in board2]
        # Extremely unlikely to be identical
        assert texts1 != texts2


class TestToggleSquare:
    def test_toggle_marks_unmarked_square(self):
        board = generate_board()
        square_id = 0
        assert board[square_id].is_marked is False
        new_board = toggle_square(board, square_id)
        assert new_board[square_id].is_marked is True

    def test_toggle_unmarks_marked_square(self):
        board = generate_board()
        board = toggle_square(board, 0)
        assert board[0].is_marked is True
        board = toggle_square(board, 0)
        assert board[0].is_marked is False

    def test_toggle_does_not_affect_free_space(self):
        board = generate_board()
        new_board = toggle_square(board, CENTER_INDEX)
        assert new_board[CENTER_INDEX].is_marked is True  # Still marked

    def test_toggle_returns_new_list(self):
        board = generate_board()
        new_board = toggle_square(board, 0)
        assert board is not new_board


class TestCheckBingo:
    def _make_board(self, marked_ids: set[int]) -> list[BingoSquareData]:
        board = generate_board()
        result = []
        for square in board:
            if square.id in marked_ids or square.is_free_space:
                result.append(
                    BingoSquareData(
                        id=square.id,
                        text=square.text,
                        is_marked=True,
                        is_free_space=square.is_free_space,
                    )
                )
            else:
                result.append(square)
        return result

    def test_no_bingo_initially(self):
        board = generate_board()
        assert check_bingo(board) is None

    def test_row_bingo(self):
        # Mark first row: indices 0-4
        board = self._make_board({0, 1, 2, 3, 4})
        result = check_bingo(board)
        assert result is not None
        assert result.type == "row"
        assert result.squares == [0, 1, 2, 3, 4]

    def test_column_bingo(self):
        # Mark first column: indices 0, 5, 10, 15, 20
        board = self._make_board({0, 5, 10, 15, 20})
        result = check_bingo(board)
        assert result is not None
        assert result.type == "column"
        assert result.squares == [0, 5, 10, 15, 20]

    def test_diagonal_bingo(self):
        # Mark diagonal: 0, 6, 12, 18, 24 (12 is free space)
        board = self._make_board({0, 6, 18, 24})
        result = check_bingo(board)
        assert result is not None
        assert result.type == "diagonal"
        assert result.squares == [0, 6, 12, 18, 24]

    def test_partial_line_no_bingo(self):
        board = self._make_board({0, 1, 2, 3})  # Only 4 of 5 in first row
        assert check_bingo(board) is None


class TestGetWinningSquareIds:
    def test_none_line_returns_empty_set(self):
        assert get_winning_square_ids(None) == set()

    def test_returns_square_ids(self):
        line = BingoLine(type="row", index=0, squares=[0, 1, 2, 3, 4])
        assert get_winning_square_ids(line) == {0, 1, 2, 3, 4}


class TestGenerateScavengerItems:
    """Tests for the scavenger hunt item generation."""

    def test_generates_24_items(self):
        from app.game_logic import generate_scavenger_items

        items = generate_scavenger_items()
        assert len(items) == 24

    def test_all_items_are_from_question_pool(self):
        from app.game_logic import generate_scavenger_items

        items = generate_scavenger_items()
        texts = {item.text for item in items}
        assert texts.issubset(set(QUESTIONS))

    def test_items_are_not_duplicated(self):
        from app.game_logic import generate_scavenger_items

        items = generate_scavenger_items()
        texts = [item.text for item in items]
        assert len(texts) == len(set(texts))

    def test_items_have_sequential_ids(self):
        from app.game_logic import generate_scavenger_items

        items = generate_scavenger_items()
        for i, item in enumerate(items):
            assert item.id == str(i) or item.id == i

    def test_items_initially_unmarked(self):
        from app.game_logic import generate_scavenger_items

        items = generate_scavenger_items()
        for item in items:
            assert item.is_marked is False

    def test_no_free_space_item(self):
        from app.game_logic import generate_scavenger_items

        items = generate_scavenger_items()
        texts = {item.text for item in items}
        assert "FREE SPACE" not in texts

    def test_items_are_shuffled(self):
        """Verify two item lists aren't identical (high probability)."""
        from app.game_logic import generate_scavenger_items

        items1 = generate_scavenger_items()
        items2 = generate_scavenger_items()
        texts1 = [item.text for item in items1]
        texts2 = [item.text for item in items2]
        # Extremely unlikely to be identical
        assert texts1 != texts2


class TestScavengerItemModel:
    """Tests for the ScavengerItem data model."""

    def test_scavenger_item_creation(self):
        from app.models import ScavengerItem

        item = ScavengerItem(id="0", text="has a pet", is_marked=False)
        assert item.id == "0"
        assert item.text == "has a pet"
        assert item.is_marked is False

    def test_scavenger_item_can_be_marked(self):
        from app.models import ScavengerItem

        item = ScavengerItem(id="0", text="has a pet", is_marked=True)
        assert item.is_marked is True


class TestGameModeModel:
    """Tests for the GameMode enum."""

    def test_game_mode_enum_exists(self):
        from app.models import GameMode

        assert hasattr(GameMode, "BINGO")
        assert hasattr(GameMode, "SCAVENGER_HUNT")

    def test_game_mode_values(self):
        from app.models import GameMode

        assert GameMode.BINGO == "bingo"
        assert GameMode.SCAVENGER_HUNT == "scavenger_hunt"


class TestGameSessionScavengerHunt:
    """Tests for GameSession scavenger hunt methods."""

    def test_start_scavenger_hunt_mode(self):
        from app.game_service import GameSession
        from app.models import GameMode

        session = GameSession()
        session.start_game(mode=GameMode.SCAVENGER_HUNT)
        assert session.game_mode == GameMode.SCAVENGER_HUNT
        assert len(session.scavenger_items) == 24

    def test_start_game_preserves_bingo_mode(self):
        from app.game_service import GameSession
        from app.models import GameMode

        session = GameSession()
        session.start_game(mode=GameMode.BINGO)
        assert session.game_mode == GameMode.BINGO
        assert len(session.board) == 25
        assert len(session.scavenger_items) == 0

    def test_handle_scavenger_toggle_marks_item(self):
        from app.game_service import GameSession
        from app.models import GameMode

        session = GameSession()
        session.start_game(mode=GameMode.SCAVENGER_HUNT)
        assert session.scavenger_items[0].is_marked is False
        session.handle_scavenger_toggle("0")
        assert session.scavenger_items[0].is_marked is True

    def test_handle_scavenger_toggle_unmarks_item(self):
        from app.game_service import GameSession
        from app.models import GameMode

        session = GameSession()
        session.start_game(mode=GameMode.SCAVENGER_HUNT)
        session.handle_scavenger_toggle("0")
        assert session.scavenger_items[0].is_marked is True
        session.handle_scavenger_toggle("0")
        assert session.scavenger_items[0].is_marked is False

    def test_handle_scavenger_toggle_multiple_items(self):
        from app.game_service import GameSession
        from app.models import GameMode

        session = GameSession()
        session.start_game(mode=GameMode.SCAVENGER_HUNT)
        session.handle_scavenger_toggle("0")
        session.handle_scavenger_toggle("5")
        session.handle_scavenger_toggle("10")
        assert session.scavenger_items[0].is_marked is True
        assert session.scavenger_items[5].is_marked is True
        assert session.scavenger_items[10].is_marked is True


class TestScavengerProgress:
    """Tests for scavenger hunt progress tracking."""

    def test_get_scavenger_progress_initial(self):
        from app.game_service import GameSession
        from app.models import GameMode

        session = GameSession()
        session.start_game(mode=GameMode.SCAVENGER_HUNT)
        marked, total = session.get_scavenger_progress()
        assert marked == 0
        assert total == 24

    def test_get_scavenger_progress_after_marking(self):
        from app.game_service import GameSession
        from app.models import GameMode

        session = GameSession()
        session.start_game(mode=GameMode.SCAVENGER_HUNT)
        session.handle_scavenger_toggle("0")
        session.handle_scavenger_toggle("5")
        marked, total = session.get_scavenger_progress()
        assert marked == 2
        assert total == 24

    def test_get_scavenger_progress_all_marked(self):
        from app.game_service import GameSession
        from app.models import GameMode

        session = GameSession()
        session.start_game(mode=GameMode.SCAVENGER_HUNT)
        for i in range(24):
            session.handle_scavenger_toggle(str(i))
        marked, total = session.get_scavenger_progress()
        assert marked == 24
        assert total == 24
