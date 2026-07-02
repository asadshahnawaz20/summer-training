from sqlmodel import SQLModel, Field


# ======================
# Patient Models
# ======================

class Patient(SQLModel, table=True):
    id: int | None = Field(
        default=None,
        primary_key=True
    )
    name: str = Field(
        min_length=1,
        max_length=100
    )
    age: int = Field(
        ge=0,
        le=120
    )
    condition: str
    risk_score: int = Field(
        ge=0,
        le=100
    )
    active: bool = True


class PatientCreate(SQLModel):
    name: str = Field(
        min_length=1,
        max_length=100
    )
    age: int = Field(
        ge=0,
        le=120
    )
    condition: str
    risk_score: int = Field(
        ge=0,
        le=100
    )
    active: bool = True


class PatientUpdate(SQLModel):
    name: str | None = None
    age: int | None = Field(
        default=None,
        ge=0,
        le=120
    )
    condition: str | None = None
    risk_score: int | None = Field(
        default=None,
        ge=0,
        le=100
    )
    active: bool | None = None


# ======================
# User Models
# ======================

class User(SQLModel, table=True):
    id: int | None = Field(
        default=None,
        primary_key=True
    )
    username: str = Field(
        index=True,
        unique=True
    )
    hashed_password: str


class UserCreate(SQLModel):
    username: str
    password: str


class UserLogin(SQLModel):
    username: str
    password: str


class UserRead(SQLModel):
    id: int
    username: str


# ======================
# JWT Token Model
# ======================

class Token(SQLModel):
    access_token: str
    token_type: str