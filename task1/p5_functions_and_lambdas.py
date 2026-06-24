"""
Task 1 — Functions and Lambda Functions

Practice reusable functions, type hints, and lambda functions.
Complete this file without using AI tools.
"""

patients = [
    {"name": "ayesha khan", "height_m": 1.65, "weight_kg": 68, "active": True},
    {"name": "omar ali", "height_m": 1.78, "weight_kg": 82, "active": False},
    {"name": "sara ahmed", "height_m": 1.60, "weight_kg": 54, "active": True},
]


def calculate_bmi(weight_kg: float, height_m: float) -> float:
    """Calculate BMI."""
    # TODO: Implement BMI formula.
    
    bmi = weight_kg / (height_m * height_m)
    return round(bmi, 2) # 


def classify_bmi(bmi: float) -> str:
    """Return BMI category."""
    # TODO: Return underweight, normal, overweight, or obese.
    
    if bmi < 18.5:
        category = "underweight"
    elif bmi < 25:
        category = "normal"
    elif bmi < 30:
        category = "overweight"
    else:
        category = "obese"
 
    return category


def format_name(name: str) -> str:
    """Convert a name to title case."""
    # TODO: Format name.
    
    n_name = name.title()
    return n_name


def get_active_patients(patient_records: list[dict]) -> list[dict]:
    """Return active patients only."""
    # TODO: Filter active patients.
    patients_active = []
    for patient in patient_records:
        
        if patient["active"] == True:
            
            patients_active.append(patient)
    
    return patients_active


def sort_patients_by_weight(patient_records: list[dict]) -> list[dict]:
    """Return patients sorted by weight using a lambda."""
    # TODO: Sort patients by weight_kg.

    patients_sorted = sorted(
        patient_records,
        key=lambda patient: patient["weight_kg"]
    )

    return patients_sorted


if __name__ == "__main__":
    # TODO: Call your functions and print useful output.

    bmi_temp = calculate_bmi(68, 1.65)

    print("bmi:", bmi_temp)
    print("Category:", classify_bmi(bmi_temp))

    print(format_name("ayesha khan"))

    print(get_active_patients(patients))

    print(sort_patients_by_weight(patients))

