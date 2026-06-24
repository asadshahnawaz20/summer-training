"""
Task 1 — Patient Summary

Complete this file without using AI tools.
Use fake/sample data only.
"""

patients = [
    {"id": 1, "name": "Ayesha Khan", "age": 32, "condition": "diabetes", "active": True},
    {"id": 2, "name": "Omar Ali", "age": 45, "condition": "hypertension", "active": True},
    {"id": 3, "name": "Sara Ahmed", "age": 28, "condition": "asthma", "active": False},
    {"id": 4, "name": "Bilal Malik", "age": 52, "condition": "diabetes", "active": True},
]


def total_patients(patient_records):
    """Return the total number of patients."""
    return len(patient_records)


def average_age(patient_records):
    """Return the average patient age."""
    tot_age = 0
    count = 0

    for pr in patient_records:
        tot_age += pr["age"]
        count += 1

    avg = tot_age / count

    return avg

def count_active_patients(patient_records):
    """Return the number of active patients."""
    count = 0

    for pr in patient_records:
        if pr['active'] == True:
            count += 1
    
    return count


def unique_conditions(patient_records):
    """Return a sorted list of unique conditions."""
    all_conditions = []

    for pr in patient_records:
        all_conditions.append(pr['condition'])

    unique_list = list(set(all_conditions))
    unique_list.sort()

    return unique_list


def count_by_condition(patient_records):
    """Return a dictionary containing patient count by condition."""
    result = {}

    for pr in patient_records:
        cond = pr["condition"]

        if cond in result:
            result[cond] = result[cond] + 1
        else:
            result[cond] = 1

    return result


if __name__ == "__main__":
    print(total_patients(patients))
    print(average_age(patients))
    print(count_active_patients(patients))
    print(unique_conditions(patients))
    print(count_by_condition(patients))
