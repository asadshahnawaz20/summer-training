"""
Task 1 — Problem 7 (Easy): Find the Runner-Up Score

HackerRank: https://www.hackerrank.com/challenges/find-second-maximum-number-in-a-list/problem

Adapted as a function so it can be tested automatically.
"""

sample_scores = [2, 3, 6, 6, 5]


def find_runner_up(scores: list[int]) -> int:
    """Return the runner-up score: the second highest *distinct* value.

    Example: [2, 3, 6, 6, 5] -> 5 (6 is the highest, 5 is the runner-up).
    """
    # TODO: Remove duplicate scores, then return the second largest value.

    unique_scores = list(set(scores))

    unique_scores.sort()

    return unique_scores[-2]


if __name__ == "__main__":
    print(find_runner_up(sample_scores))
