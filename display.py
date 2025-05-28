selection_screen = \
"""---------------------------------
SELECT AN OPTION:
    1. Start a new challenge
    2. View Scoreboard
    3. Exit
---------------------------------
"""

difficulty_select = \
"""---------------------------------
SELECT A DIFFICULTY:
    1. Easy
    2. Medium
    3. Hard
---------------------------------
"""

prompt_display = \
"""
YOUR PROMPT IS:

{prompt}

PRESS ENTER TO BEGIN AND ENTER TO END"""

score_display = \
"""
RESULTS

SCORE: {score}
ACCURACY: {accuracy}
SPEED: {speed}
"""


# TODO: Improve leaderboard layout, make it so speed / acc / score adjusts to number length

leaderboard_entry = \
"""{score:>15.3f} | {accuracy:>10.3f}% | {speed:>10.3f} | {name}"""

leaderboard_display = \
"""---------------------------------
LEADERBOARD:

    Easy

                  score |    accuracy |      speed | name
        {easy_scores}

    Medium

                  score |    accuracy |      speed | name
        {medium_scores}

    Hard
    
                  score |    accuracy |      speed | name
        {hard_scores}

---------------------------------
PRESS ENTER TO RETURN
"""