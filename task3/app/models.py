from sqlmodel import SQLModel, Field


class Patient(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    age: int
    active: bool = True


class PatientCreate(SQLModel):
    id: int | None = None
    name: str
    age: int
    active: bool = True


class PatientUpdate(SQLModel):
    name: str | None = None
    age: int | None = None
    active: bool | None = None