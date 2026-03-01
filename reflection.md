TF Weekly Task:

Phase 1: Glitch Hunt (Spot Check)
[x] Run the Streamlit game once
[x] Identify at at least 4 bugs
- debug says secret is 24, my guess was 50, it told me to higher LOL, same with vice versa
- why is hard 1-50 while normal is 1-100?
- New game button does not work 
- +5 score if the code return "too high" while -5 if the code returns too low
[x] Trace the bug across files
- *Higher and lower* - in the check_guess function (lines 32-47)
- *Difficulty range difference* - in the get_range_for_difficulty (lines 4-11)
- *New game button* - in the New_game function  (lines 134-138)
- *Scores exploit* - In the update_score function (lines 50-65)
[x] Be prepared to explain the failure clearly
- *Higher and lower* - the logic for if guess > secret returns "go lower". this means a logic error because if a guess is higher than the secret the function should say "go lower" 
- *Difficulty range* it doesnt make sense that the range for hard is 1-50 while the range for normal is 1-100.
- *new game button* whenever you click on a "new game" it does not reset the guesses or allow you to enter. It does give a new number to guess but the game itself doesnt allow you to guess that it is. 
- *scores exploit* if you consistently have a "go higher" result, it adds +5 to the score whereas if you have a "go lower" result, it -5 to the score.


Phase 2: Investigate and Repair (Assigned)
[x] Fix 2 bugs end‑to‑end
- I fixed the new game button & Difficulty range
[x] Review at least one AI-generated edit
- When I asked claud how to fix a certain code it was the guess> secret thing, it gave me the longer answer vs just switching the Less than or bigger than sign. 
[x] Generate pytest cases and run pytest successfully
test_glitchy_guesser.py
[x] Draft a short guiding hint they would give a student
- When you write code, you should try seeing things in the pov of the user not the program, for example for the guess> secret, think a bit more about what that would result in.


Phase 3: Reflection and README (Review)
[x] Skim reflection prompts
[x] Understand expected depth for support
