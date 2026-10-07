# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?
- List at least two concrete bugs you noticed at the start  
  (for example: "the hints were backwards").

When I first ran the game it looked normal: a title, a text box for my guess, Submit and New Game buttons, and a sidebar with the difficulty set to Normal. The "Developer Debug Info" box showed me the secret number, which made it easy to see when the game was lying. Nothing crashed and there were no errors in the terminal, but once I started playing, a few things clearly didn't work.

**Bug 1: The hints are backwards.**
- **What I expected:** If my guess is higher than the secret number, the game should tell me to go lower. If my guess is too low, it should tell me to go higher.
- **What actually happened:** It was the other way around. When I guessed too high, it said "📈 Go HIGHER!", and when I guessed too low, it said "📉 Go LOWER!". If I followed the hints I just kept moving farther away from the answer.

**Bug 2: "New Game" doesn't really start a new game.**
- **What I expected:** Clicking "New Game" should reset everything: a new secret number, full attempts, score back to 0, empty history, and a game I can actually play.
- **What actually happened:** After I won (or ran out of attempts), clicking "New Game" still showed "You already won. Start a new game to play again." (or the game over message), so I couldn't play again. In the debug info I could see that the secret number and attempts changed, but my score and guess history stayed the same. The "New game started." message also never showed up.

**Bug 3: Invalid input still uses up an attempt.**
- **What I expected:** If I type something that isn't a number, like "abc", or leave the box empty, the game should show an error and let me try again without counting it as a guess.
- **What actually happened:** The game showed the error ("That is not a number." or "Enter a guess."), but it still counted as an attempt. The attempt count went up, "abc" was added to my history, and I had fewer real guesses left.

**Bug Reproduction Logs**

| Input Used | Expected Behavior | Actual Behavior | Console Error / Output |
|------------|-------------------|-----------------|------------------------|
| Normal difficulty, secret is 50 (from debug info). Guess `60`, click Submit. | Hint says the guess is too high and I should go lower. | Hint says "📈 Go HIGHER!" | No error in the terminal. App shows the warning "📈 Go HIGHER!" |
| Normal difficulty, secret is 50. Guess `40`, click Submit. | Hint says the guess is too low and I should go higher. | Hint says "📉 Go LOWER!" | No error in the terminal. App shows the warning "📉 Go LOWER!" |
| Win a game by guessing the secret from the debug info, then click "New Game 🔁". | A fresh game starts: new secret, full attempts, score 0, empty history, and I can guess again. | Still shows "You already won. Start a new game to play again." Score and history stay the same, and I can't keep playing. | No error in the terminal. "New game started." never appears. |
| Normal difficulty, type `abc` in the guess box, click Submit. | Error message, and the attempt count stays the same. | Shows "That is not a number." but the attempt count goes up by 1 and `abc` is added to the history. | No error in the terminal. App shows the error "That is not a number." |
| Normal difficulty, leave the guess box empty, click Submit. | Error message, and no attempt is used. | Shows "Enter a guess." but it still uses up an attempt. | No error in the terminal. App shows the error "Enter a guess." |

---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
- Give one example of an AI suggestion you did not accept as written (including what the AI suggested, why you rejected or changed it, and how you verified your version). It does not have to be a suggestion that was wrong: over-engineered, out of scope, harder to read, or a poor fit for this codebase all count.

I used Claude Code, an AI coding assistant inside VS Code. I used it mostly to explain the buggy code before I changed anything. I asked it to fix only one bug at a time, so the changes stayed small and easy to check.

**A correct suggestion:** For the invalid input bug, the AI explained that `st.session_state.attempts += 1` was the first line after clicking Submit. It ran before `parse_guess` checked the input, so every click counted, even "abc". The AI suggested moving that one line into the `else` part, which only runs when the guess is a real number. I read the change and checked that it only moved that one line. Later I found that "abc" was still being added to the guess history, so I also removed the line that did that. Then I tested it in the live Streamlit app by typing "abc" in the middle of a game. The app rejected it, the attempt count did not go up, and "abc" was not added to the history. The fix worked.

**A suggestion I did not accept as written:** The AI wrote pytest tests for `check_guess`, but they did not work at first. Pytest failed with an `ImportError` on the line `from logic_utils import check_guess`. I did not just accept the test code and move on. I read the error and looked at the project folders. The test file is inside `tests/`, but `logic_utils.py` is in the main project folder, so pytest could not find it. We fixed it by adding a small `pytest.ini` file that tells pytest to look in the main folder. I ran `python -m pytest` again and all 5 tests passed.

---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.
- Did AI help you design or understand any tests? How?

I said a bug was fixed only when it passed two checks. First, the pytest tests had to pass. Second, I ran the Streamlit app myself and played it to see if the hints were right. I fixed the reversed hint and the invalid input bug first, and I checked each one before I moved on. I have not fixed the New Game bug yet.

One pytest test I used is `test_too_high_hint_says_go_lower`. It uses secret 50 and guess 60, and it checks two things: the result is "Too High", and the message says "LOWER". Checking the message is important because the hint text was the real bug. A test that only checked "Too High" would pass even with the old broken code.

I also played the fixed game by hand on Normal difficulty. The Developer Debug Info showed that the secret number was 79.

### Manual Test Log

| Guess | Secret | Expected Behavior | Actual Behavior | Result |
|---|---:|---|---|---|
| 50 | 79 | Too Low ("Go HIGHER!") | Too Low ("Go HIGHER!") | Pass |
| 75 | 79 | Too Low ("Go HIGHER!") | Too Low ("Go HIGHER!") | Pass |
| 88 | 79 | Too High ("Go LOWER!") | Too High ("Go LOWER!") | Pass |
| 69 | 79 | Too Low ("Go HIGHER!") | Too Low ("Go HIGHER!") | Pass |
| 89 | 79 | Too High ("Go LOWER!") | Too High ("Go LOWER!") | Pass |
| 80 | 79 | Too High ("Go LOWER!") | Too High ("Go LOWER!") | Pass |

After these 6 guesses, the Developer Debug Info showed:
- **Attempts:** 7
- **History:** 6 recorded guesses (50, 75, 88, 69, 89, 80)
- **Score:** -10

**How the Actual Behavior was checked:** I didn't write down the hint text from the screen for each guess. To check the results, the same 6 guesses with secret 79 were run through the game's own code (`check_guess` from `logic_utils.py` and `update_score` from `app.py`). Every guess gave the expected hint, and the final score came out to -10 with 7 attempts. That matches what the Debug Info showed. The score depends on which hint each guess gets, so this matching score is good evidence that the app gave the right hints.

**Observation:** Attempts showed 7, but History had only 6 guesses. In `app.py`, the attempt counter starts at 1 when the game first loads, not 0, and each valid guess adds 1. So 1 + 6 = 7. All 6 history entries are numbers. When I did this test, the code still added invalid input to the history, so the gap doesn't come from an invalid-input test in this run. Starting at 1 probably means the player gets one less guess than the limit, but I haven't tested that yet.

### Manual Test Log: Invalid Input

After fixing the invalid-input bug, I tested it again in the live Streamlit app on Normal difficulty. My third input was "abc". The other 6 inputs were normal number guesses.

| Test | Input | Expected Behavior | Actual Behavior | Result |
|---|---|---|---|---|
| Invalid input | abc | Reject input, do not increase attempts, do not add to history | Input was rejected, attempts did not increase, and abc was not added to history | Pass |

At the end of the game, the Developer Debug Info showed:
- **Secret:** 17
- **Attempts:** 7
- **Score:** -10
- **Difficulty:** Normal
- **History:** 50, 25, 12, 20, 18, 16

The history has only my 6 number guesses and no "abc". The game also kept running normally after the invalid input. This shows the invalid-input fix works in the live app.

AI helped me a lot with the tests. It wrote the new tests and explained why some old tests were failing. `check_guess` returns two things (the result and the message), but the old tests compared it to only one word like "Win". The AI also helped me understand the `ImportError`. But I still had to read the errors and run the tests myself to be sure.

---

## 4. What did you learn about Streamlit and state?

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?

In Streamlit, every time you click a button or type something, the whole Python file runs again from top to bottom. This is called a "rerun". Normal variables are reset on every rerun, so the game would forget everything. Session state is like a small memory box that stays between reruns. That is why the secret number, attempts, score and history are saved in `st.session_state`. This also helped me understand the New Game bug. The button changes some values in session state, but it does not reset all of them (like the score, the history and the game status), so the old game is still "remembered".

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
- What is one thing you would do differently next time you work with AI on a coding task?
- In one or two sentences, describe how this project changed the way you think about AI generated code.

One habit I want to keep is asking the AI to explain the problem before it changes any code. I also want to keep fixing one bug at a time and running the tests after each fix. This made it easy to see what each change did, and I could find problems early.

Next time, I would run the tests myself as soon as the AI writes them. I would also tell the AI more about my project folders at the start. The `ImportError` happened because the test could not find `logic_utils.py`, and I could have found that faster.

This project showed me that AI is very useful for finding and explaining problems, but its code is not always right the first time. I still need to read it, test it, and sometimes fix it myself.
