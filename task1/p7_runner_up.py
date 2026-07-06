"""
Task 1 — Problem 7 (Easy): Find the Runner-Up Score

HackerRank: https://www.hackerrank.com/challenges/find-second-maximum-number-in-a-list/problem

Adapted as a function so it can be tested automatically.
"""

sample_scores = [2, 3, 6, 6, 5]


def find_runner_up(scores: list[int]) -> int | None:
    unique_scores = sorted(set(scores))

    if len(unique_scores) < 2:
        return None

    return unique_scores[-2]


if __name__ == "__main__":
    print(find_runner_up(sample_scores))
