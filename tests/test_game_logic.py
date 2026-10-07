from streamlit.testing.v1 import AppTest
from logic_utils import check_guess

def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win
    outcome, _ = check_guess(50, 50)
    assert outcome == "Win"

def test_guess_too_high():
    # If secret is 50 and guess is 60, hint should be "Too High"
    outcome, _ = check_guess(60, 50)
    assert outcome == "Too High"

def test_guess_too_low():
    # If secret is 50 and guess is 40, hint should be "Too Low"
    outcome, _ = check_guess(40, 50)
    assert outcome == "Too Low"

def test_too_high_hint_says_go_lower():
    # Bug fix: secret 50, guess 60 should be "Too High" and tell the player to go LOWER
    outcome, message = check_guess(60, 50)
    assert outcome == "Too High"
    assert "LOWER" in message

def test_too_low_hint_says_go_higher():
    # Bug fix: secret 50, guess 40 should be "Too Low" and tell the player to go HIGHER
    outcome, message = check_guess(40, 50)
    assert outcome == "Too Low"
    assert "HIGHER" in message

def test_invalid_input_does_not_use_attempt_or_go_in_history():
    # Bug fix: "abc" should show an error, not use an attempt, and not be added to history
    at = AppTest.from_file("../app.py").run()
    at.session_state.secret = 46
    at.text_input[0].set_value("abc")
    at.button[0].click().run()
    assert at.error[0].value == "That is not a number."
    assert at.session_state.attempts == 1
    assert at.session_state.history == []
    assert at.session_state.status == "playing"
