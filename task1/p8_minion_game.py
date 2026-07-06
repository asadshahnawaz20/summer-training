"""
Task 1 — Problem 8 (Medium): The Minion Game

HackerRank: https://www.hackerrank.com/challenges/the-minion-game/problem

Adapted as a function so it can be tested automatically.
"""

VOWELS = "AEIOU"


def minion_game(word: str) -> str:
    """Play the Minion Game on an uppercase word and return the result.

    Two players make substrings of `word`:
    - Kevin scores every substring that starts with a vowel (A, E, I, O, U).
    - Stuart scores every substring that starts with a consonant.

    A letter at index i in a word of length n starts (n - i) substrings.

    Return:
    - "Stuart <score>" if Stuart wins,
    - "Kevin <score>" if Kevin wins,
    - "Draw" if the scores are equal.

    Example: "BANANA" -> "Stuart 12".
    """
    # TODO: Add up each player's score, then return the formatted result.

    n = len(word)

    kevin_score = 0
    stuart_score = 0

    for i in range(n):
        letter = word[i]

        sub_count = n - i

        if letter in VOWELS:
            kevin_score += sub_count
        else:
            stuart_score += sub_count

    if stuart_score > kevin_score:
        return "Stuart " + str(stuart_score)
    elif kevin_score > stuart_score:
        return "Kevin " + str(kevin_score)
    else:
        return "Draw"


if __name__ == "__main__":
    print(minion_game("BANANA"))
