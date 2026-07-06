"""
Task 1 — Problem 9 (Medium): Word Order

HackerRank: https://www.hackerrank.com/challenges/word-order/problem

Adapted as a function so it can be tested automatically.
"""

sample_words = ["bcdef", "abcdefg", "bcde", "bcdef"]


def word_order(words: list[str]) -> tuple[int, list[int]]:
    """Return the count of distinct words and how many times each appears."""
    word_counts = {}

    for word in words:
        if word in word_counts:
            word_counts[word] += 1
        else:
            word_counts[word] = 1

    distinct_count = len(word_counts)
    counts = list(word_counts.values())

    return distinct_count, counts


if __name__ == "__main__":
    distinct_count, counts = word_order(sample_words)
    print(distinct_count)
    print(counts)
