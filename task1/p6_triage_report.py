"""
Task 1 — Final Problem: Triage Report

Complete this file without using AI tools.
Use fake/sample data only.

Tip: collections.Counter can make counting by risk label easier, but a
plain dictionary works too — import it yourself if you want to use it.
"""

patients = [
    {"id": 1, "name": "Ayesha Khan", "age": 32, "risk_score": 72, "active": True},
    {"id": 2, "name": "Omar Ali", "age": 45, "risk_score": 88, "active": True},
    {"id": 3, "name": "Sara Ahmed", "age": 28, "risk_score": 35, "active": False},
    {"id": 4, "name": "Bilal Malik", "age": 52, "risk_score": 91, "active": True},
]


def label_risk(risk_score: int) -> str:
    """Return low, medium, or high based on risk score."""
    # TODO: Define thresholds and return label.

    if risk_score >= 75:
        label = "high"
    elif risk_score >= 50:
        label = "medium"
    else:
        label = "low"

    return label


def add_risk_labels(patient_records: list[dict]) -> list[dict]:
    """Return copies of patient records with a risk_label field added."""
    # TODO: Add risk labels without modifying original records.

    temp_list = []
    for patient in patient_records:
        new_patient = patient.copy()

        new_patient["risk_label"] = label_risk(patient["risk_score"])
        temp_list.append(new_patient)

    return temp_list


def build_triage_report(patient_records: list[dict]) -> dict:
    """Build a triage report from patient records."""
    # TODO: Build and return final report.

    data = add_risk_labels(patient_records)

    total = len(data)

    counts = {"low": 0, "medium": 0, "high": 0}

    for p in data:
        counts[p["risk_label"]] += 1

    high = []

    for pr in data:
        if pr["active"] and pr["risk_label"] == "high":
            high.append(pr)

    report = {
        "summary": {"total_patients": total},
        "risk_counts": counts,
        "active_high_risk_patients": high,
    }

    return report


if __name__ == "__main__":
    report = build_triage_report(patients)
    print(report)

    assert label_risk(80) == "high"
    assert label_risk(60) == "medium"
    assert label_risk(10) == "low"
    assert report["summary"]["total_patients"] == 4
    assert len(report["active_high_risk_patients"]) == 2
