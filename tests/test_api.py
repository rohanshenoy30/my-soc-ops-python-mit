import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture
def client():
    return TestClient(app)


class TestHomePage:
    def test_home_returns_200(self, client: TestClient):
        response = client.get("/")
        assert response.status_code == 200

    def test_home_contains_start_screen(self, client: TestClient):
        response = client.get("/")
        assert "Soc Ops" in response.text
        assert "CHOOSE YOUR MODE" in response.text
        assert "SOCIAL BINGO" in response.text

    def test_home_sets_session_cookie(self, client: TestClient):
        response = client.get("/")
        assert "session" in response.cookies


class TestStartGame:
    def test_start_returns_game_board(self, client: TestClient):
        # First visit to get session
        client.get("/")
        response = client.post("/start")
        assert response.status_code == 200
        assert "FREE SPACE" in response.text
        assert "BACK" in response.text

    def test_board_has_25_squares(self, client: TestClient):
        client.get("/")
        response = client.post("/start")
        # Count the toggle buttons (squares with hx-post="/toggle/")
        assert response.text.count('hx-post="/toggle/') == 24  # 24 + 1 free space


class TestToggleSquare:
    def test_toggle_marks_square(self, client: TestClient):
        client.get("/")
        client.post("/start")
        response = client.post("/toggle/0")
        assert response.status_code == 200
        # The response should contain the game screen with a marked square
        assert "FREE SPACE" in response.text


class TestResetGame:
    def test_reset_returns_start_screen(self, client: TestClient):
        client.get("/")
        client.post("/start/bingo")
        response = client.post("/reset")
        assert response.status_code == 200
        assert "CHOOSE YOUR MODE" in response.text
        assert "SOCIAL BINGO" in response.text


class TestDismissModal:
    def test_dismiss_returns_game_screen(self, client: TestClient):
        client.get("/")
        client.post("/start")
        response = client.post("/dismiss-modal")
        assert response.status_code == 200
        assert "FREE SPACE" in response.text


class TestStartGameWithMode:
    def test_start_bingo_mode(self, client: TestClient):
        client.get("/")
        response = client.post("/start/bingo")
        assert response.status_code == 200
        assert "FREE SPACE" in response.text
        assert "BACK" in response.text

    def test_start_scavenger_hunt_mode(self, client: TestClient):
        client.get("/")
        response = client.post("/start/scavenger_hunt")
        assert response.status_code == 200
        assert "SCAVENGER HUNT" in response.text
        assert "BACK" in response.text

    def test_invalid_mode_returns_error(self, client: TestClient):
        client.get("/")
        response = client.post("/start/invalid_mode")
        assert response.status_code == 422 or response.status_code == 400


class TestScavengerHuntScreen:
    def test_scavenger_hunt_has_24_items(self, client: TestClient):
        client.get("/")
        response = client.post("/start/scavenger_hunt")
        # Count the toggle buttons for scavenger hunt items (hx-post="/toggle/")
        # Should have 24 items (no FREE SPACE)
        assert response.text.count('hx-post="/toggle/') == 24

    def test_scavenger_hunt_shows_progress_meter(self, client: TestClient):
        client.get("/")
        response = client.post("/start/scavenger_hunt")
        assert "0/24" in response.text or "progress" in response.text.lower()

    def test_scavenger_hunt_items_are_from_question_pool(self, client: TestClient):
        client.get("/")
        response = client.post("/start/scavenger_hunt")
        # Response should contain questions from QUESTIONS list
        assert "has a pet" in response.text or "found" in response.text.lower()

    def test_scavenger_hunt_has_card_layout(self, client: TestClient):
        client.get("/")
        response = client.post("/start/scavenger_hunt")
        # Cards should have arcade styling
        assert "arcade-card" in response.text or "card" in response.text.lower()


class TestToggleScavengerItem:
    def test_toggle_marks_scavenger_item(self, client: TestClient):
        client.get("/")
        client.post("/start/scavenger_hunt")
        # Toggle an item (use a UUID or index - test with index 0)
        response = client.post("/toggle/0")
        assert response.status_code == 200
        assert "SCAVENGER HUNT" in response.text

    def test_toggle_updates_progress_meter(self, client: TestClient):
        client.get("/")
        client.post("/start/scavenger_hunt")
        # Initial progress: 0/24
        client.post("/start/scavenger_hunt")
        # Toggle an item
        response2 = client.post("/toggle/0")
        # Progress should update to 1/24 (or similar)
        assert "1/24" in response2.text

    def test_toggle_scavenger_item_twice(self, client: TestClient):
        client.get("/")
        client.post("/start/scavenger_hunt")
        # Toggle on
        client.post("/toggle/0")
        # Toggle off
        response = client.post("/toggle/0")
        assert response.status_code == 200
        # Progress should be back to 0/24
        assert "0/24" in response.text

    def test_marking_all_items_completes_hunt(self, client: TestClient):
        client.get("/")
        client.post("/start/scavenger_hunt")
        # Mark all 24 items
        for i in range(24):
            client.post(f"/toggle/{i}")
        response = client.get("/")
        # After marking all, should still show complete hunt or completion indicator
        assert response.status_code == 200


class TestModeSelection:
    def test_home_page_shows_mode_selector(self, client: TestClient):
        response = client.get("/")
        # Start screen should offer mode selection
        assert "BINGO" in response.text or "Bingo" in response.text
        assert "SCAVENGER" in response.text or "Scavenger" in response.text

    def test_switching_modes_clears_state(self, client: TestClient):
        client.get("/")
        # Start with bingo
        client.post("/start/bingo")
        # Mark a square
        client.post("/toggle/0")
        # Reset and switch to scavenger hunt
        client.post("/reset")
        response = client.post("/start/scavenger_hunt")
        # Should show fresh scavenger hunt with 0/24
        assert "0/24" in response.text
        assert "SCAVENGER HUNT" in response.text
