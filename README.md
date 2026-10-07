# 🎮 Game Glitch Investigator: The Impossible Guesser

## 🚨 The Situation

You asked an AI to build a simple "Number Guessing Game" using Streamlit.
It wrote the code, ran away, and now the game is unplayable. 

- You can't win.
- The hints lie to you.
- The secret number seems to have commitment issues.

## 🛠️ Setup

1. Install dependencies: `pip install -r requirements.txt`
2. Run the broken app: `python -m streamlit run app.py`

## 🕵️‍♂️ Your Mission

1. **Play the game.** Open the "Developer Debug Info" tab in the app to see the secret number. Try to win.
2. **Find the State Bug.** Why does the secret number change every time you click "Submit"? Ask ChatGPT: *"How do I keep a variable from resetting in Streamlit when I click a button?"*
3. **Fix the Logic.** The hints ("Higher/Lower") are wrong. Fix them.
4. **Refactor & Test.** - Move the logic into `logic_utils.py`.
   - Run `pytest` in your terminal.
   - Keep fixing until all tests pass!

## 📝 Document Your Experience

**What the game is for:** It's a number guessing game made with Streamlit. The game picks a secret number and you try to guess it. After each guess it gives you a hint to go higher or lower, and you have a limited number of attempts.

**Bugs I found:**
- **The hints were backwards.** If you guessed too high, the game told you to go HIGHER, and if you guessed too low, it told you to go LOWER.
- **Invalid input used up an attempt.** If you typed something that wasn't a number (like `abc`) or left the box empty, the game showed an error but still counted it as an attempt.

**How I fixed them:**
- I swapped the hint messages in `check_guess`. Now "Too High" says "Go LOWER!" and "Too Low" says "Go HIGHER!"
- I moved the line that adds an attempt so it only runs after the guess is checked and turns out to be a real number. I also stopped invalid input from being added to the guess history.
- I moved `check_guess` out of `app.py` into `logic_utils.py`, and `app.py` now imports it from there.
- I added pytest tests in `tests/test_game_logic.py` for a winning guess, a too-high guess, and a too-low guess.

**How I used AI:** I used an AI coding assistant to:
- understand what the buggy logic was doing
- fix the reversed high/low hints
- fix invalid input being counted as an attempt
- move the core logic into `logic_utils.py`
- write the pytest tests and debug them

Not everything the AI gave me worked the first time. At one point pytest failed with an `ImportError` on `from logic_utils import check_guess`. I had to look at the project folders and how the import was set up to figure out why the tests couldn't find `logic_utils.py`. The fix was adding a `pytest.ini` file, and I ran the tests again to check that it actually worked.

I didn't just accept whatever the AI suggested. I read each change, checked that it only touched what it was supposed to, and ran the tests myself before committing.

## 📸 Demo Walkthrough

Steps 1–4 come from a real game I played on Normal difficulty. The "Developer Debug Info" section showed the secret number was **79**.

1. **Start the game.** Run `python -m streamlit run app.py` and open the app in your browser.
2. **Guess too low.** I guessed `50`, then `75`, then `69`. Each one is "Too Low", so the hint says "Go HIGHER!"
3. **Guess too high.** I guessed `88`, then `89`, then `80`. Each one is "Too High", so the hint says "Go LOWER!"
4. **Check the Debug Info.** After my 6 guesses (in the order 50, 75, 88, 69, 89, 80), it showed Attempts: 7, History with 6 guesses, and Score: -10.

5. **Type something that isn't a number.** I tested this in a different game where the secret was 17. My third input was `abc`. The game rejected it, the attempt count didn't go up, `abc` was not added to the history, and the game kept going. At the end, the Debug Info showed Attempts: 7, Score: -10, and History: 50, 25, 12, 20, 18, 16, so only my 6 number guesses were saved.

Step 6 explains what the code does. I didn't do it in my test games.

6. **Guess the right number.** The game shows balloons and a "You won!" message with the secret number and your final score. After that, clicking Submit says "You already won. Start a new game to play again."

**Screenshot** *(optional)*: <!-- Insert a screenshot of your fixed, winning game here -->

## 🧪 Test Results

```
> python -m pytest -v
collected 6 items

tests/test_game_logic.py::test_winning_guess PASSED                      [ 16%]
tests/test_game_logic.py::test_guess_too_high PASSED                     [ 33%]
tests/test_game_logic.py::test_guess_too_low PASSED                      [ 50%]
tests/test_game_logic.py::test_too_high_hint_says_go_lower PASSED        [ 66%]
tests/test_game_logic.py::test_too_low_hint_says_go_higher PASSED        [ 83%]
tests/test_game_logic.py::test_invalid_input_does_not_use_attempt_or_go_in_history PASSED [100%]

============================== 6 passed in 0.75s ==============================
```

## 🚀 Stretch Features

- [ ] [If you choose to complete Challenge 4, describe the Enhanced UI changes here — a screenshot is optional]
