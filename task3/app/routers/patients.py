from fastapi import APIRouter, HTTPException, Query, status, Depends
from sqlmodel import Session, select

from app.database import get_session
from app.models import Patient, PatientCreate, PatientUpdate

router = APIRouter(
    prefix="/patients",
    tags=["patients"],
)


@router.get(
    "/",
    response_model=list[Patient],
    summary="Get all patients",
    description="Returns all patients. You can optionally filter by active status and limit the number of results.",
)
def get_patients(
    active: bool | None = Query(
        default=None,
        description="Filter patients by active status.",
    ),
    limit: int | None = Query(
        default=None,
        description="Maximum number of patients to return.",
    ),
    session: Session = Depends(get_session),
) -> list[Patient]:

    statement = select(Patient)
    patients = session.exec(statement).all()

    if active is not None:
        patients = [
            patient
            for patient in patients
            if patient.active == active
        ]

    if limit is not None:
        patients = patients[:limit]

    return patients


@router.get(
    "/{patient_id}",
    response_model=Patient,
    summary="Get patient by ID",
    description="Returns a single patient if it exists.",
)
def get_patient(
    patient_id: int,
    session: Session = Depends(get_session),
) -> Patient:

    patient = session.get(Patient, patient_id)

    if not patient:
        raise HTTPException(
            status_code=404,
            detail="Patient not found",
        )

    return patient


@router.post(
    "/",
    response_model=Patient,
    status_code=status.HTTP_201_CREATED,
    summary="Create a patient",
    description="Creates a new patient.",
)
def create_patient(
    patient_data: PatientCreate,
    session: Session = Depends(get_session),
) -> Patient:

    patient = Patient.model_validate(patient_data)

    session.add(patient)
    session.commit()
    session.refresh(patient)

    return patient


@router.put(
    "/{patient_id}",
    response_model=Patient,
    summary="Update a patient",
    description="Replaces all information of an existing patient.",
)
def update_patient(
    patient_id: int,
    updated_patient: PatientCreate,
    session: Session = Depends(get_session),
) -> Patient:

    patient = session.get(Patient, patient_id)

    if not patient:
        raise HTTPException(
            status_code=404,
            detail="Patient not found",
        )

    patient.name = updated_patient.name
    patient.age = updated_patient.age
    patient.active = updated_patient.active

    session.add(patient)
    session.commit()
    session.refresh(patient)

    return patient


@router.patch(
    "/{patient_id}",
    response_model=Patient,
    summary="Partially update a patient",
    description="Updates one or more fields of an existing patient.",
)
def patch_patient(
    patient_id: int,
    updated_data: PatientUpdate,
    session: Session = Depends(get_session),
) -> Patient:

    patient = session.get(Patient, patient_id)

    if not patient:
        raise HTTPException(
            status_code=404,
            detail="Patient not found",
        )

    patient_data = updated_data.model_dump(exclude_unset=True)

    for key, value in patient_data.items():
        setattr(patient, key, value)

    session.add(patient)
    session.commit()
    session.refresh(patient)

    return patient


@router.delete(
    "/{patient_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a patient",
    description="Deletes a patient by ID.",
)
def delete_patient(
    patient_id: int,
    session: Session = Depends(get_session),
):

    patient = session.get(Patient, patient_id)

    if not patient:
        raise HTTPException(
            status_code=404,
            detail="Patient not found",
        )

    session.delete(patient)
    session.commit()

    return None