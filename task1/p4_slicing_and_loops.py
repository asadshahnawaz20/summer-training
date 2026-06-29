"""
Task 1 — Slicing and Loops

Practice slicing, loops, enumerate, zip, and comprehensions.
Complete this file without using AI tools.
"""

patient_ids = [101, 102, 103, 104, 105, 106, 107]
patient_names = ["Ayesha", "Omar", "Sara", "Bilal", "Hina", "Usman", "Maha"]


def slicing_examples():
    """Return examples of list slicing."""
    first_three = patient_ids[0:3]
    last_three = patient_ids[-3:]
    reversed_ids = patient_ids[::-1]

    print("first three Ids:", first_three)
    print("sast three Ids:", last_three)
    print("reversed Ids:", reversed_ids)

    return first_three, last_three, reversed_ids


def loop_examples():
    """Practice range, enumerate, and zip."""
    for i in range(len(patient_names)):
        print(i)

    for i, name in enumerate(patient_names):
        print(i, name)

    for pid, name in zip(patient_ids, patient_names):
        print(pid, name)


def comprehension_examples():
    """Return values created using comprehensions."""
    even_patient_ids = [pid for pid in patient_ids if pid % 2 == 0]

    upper_names = [name.upper() for name in patient_names]

    print("Even IDs:", even_patient_ids)
    print("Upper names:", upper_names)

    return even_patient_ids, upper_names


if __name__ == "__main__":
    slicing_examples()
    loop_examples()
    comprehension_examples()
