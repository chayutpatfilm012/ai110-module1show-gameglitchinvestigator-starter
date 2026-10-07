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

---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.
- Did AI help you design or understand any tests? How?

---

## 4. What did you learn about Streamlit and state?

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
- What is one thing you would do differently next time you work with AI on a coding task?
- In one or two sentences, describe how this project changed the way you think about AI generated code.
