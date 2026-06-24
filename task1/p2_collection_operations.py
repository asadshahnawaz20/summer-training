"""
Task 1 — Collection Operations

Practice lists, tuples, and sets.
Complete this file without using AI tools.
"""

# Sample data — do not edit.
sample_conditions = ["diabetes", "asthma", "hypertension"]
primary_conditions = {"diabetes", "asthma", "hypertension"}
follow_up_conditions = {"asthma", "cardiac", "diabetes"}


def list_operations(conditions: list[str]) -> list[str]:
    """Return a new, sorted list after adding and removing a condition.

    Steps:
    - Work on a copy so the input list is not modified.
    - Add "cardiac".
    - Remove "asthma".
    - Return the list sorted alphabetically.
    """
    temp_list = conditions.copy()
    temp_list.append("cardiac")
    temp_list.remove("asthma")
    temp_list.sort()
    return temp_list


def set_operations(primary: set[str], follow_up: set[str]) -> dict[str, set[str]]:
    """Return common, all-unique, and primary-only conditions.

    Return a dictionary with these keys:
    - "common": conditions in both sets
    - "all_unique": every condition across both sets
    - "only_primary": conditions in primary but not in follow_up
    """

    common = primary.intersection(follow_up)
    all_unique = primary.union(follow_up)
    only_primary = primary.difference(follow_up)

    result = {
        "common": common,
        "all_unique": all_unique,
        "only_primary": only_primary,
    }

    return result


if __name__ == "__main__":
    print(list_operations(sample_conditions))
    print(set_operations(primary_conditions, follow_up_conditions))
