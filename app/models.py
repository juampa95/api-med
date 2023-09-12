from sqlmodel import Field, SQLModel, Relationship
from datetime import date, datetime
from typing import List, Optional
from pydantic import validator


class Base(SQLModel):
    id: Optional[int] = Field(primary_key=True, index=True, description="Código id creado automáticamente")


class BaseModel(SQLModel):
    created_at: datetime = Field(default_factory=datetime.now)
    update_at: datetime = Field(default_factory=datetime.now)

    def on_update(self):
        self.update_at = datetime.now()


class Person(BaseModel):
    personal_id: int = Field(...,  description="Identificación personal. Debe tener 8 números")
    code: Optional[int] = Field(description="código interno que identifique a la persona")
    name: str
    lastname: str
    birthdate: date = Field(..., description="Fecha de nacimiento en formato yyyy-mm-dd")

    @validator("personal_id", pre=True, always=True)
    def validate_personal_id(cls, value):
        if not (1000000 <= value <= 99999999):
            raise ValueError("Personal ID must have between 7 and 8 digits")
        return value


class Medicine(BaseModel, table=True):
    id: Optional[int] = Field(primary_key=True, index=True)
    code: Optional[int]
    name: str
    drug: str
    concentration: str
    form: str
    gtin: str
    prescriptionDetails: List["PrescriptionDetails"] = Relationship(back_populates="medicine")

    @validator("gtin", pre=True, always=True)
    def validate_gtin_format(cls, value):
        # Verifico que cada caracter sea un dígito numérico
        if not value.isdigit():
            raise ValueError("El GTIN debe estar conformado solo por números enteros")

        # Verifico que tenga 13 o 14 dígitos
        if len(value) != 13 and len(value) != 14:
            raise ValueError("El GTIN debe contener 13 o 14 dígitos")

        # Si tiene 13 dígitos, agregamos un "0" al principio
        if len(value) == 13:
            value = "0" + value

        return value


class Patient(Person, table=True):
    id: Optional[int] = Field(primary_key=True)
    prescriptions: List["Prescription"] = Relationship(back_populates="patient")


class Doctor(Person, table=True):
    id: Optional[int] = Field(primary_key=True)
    prescriptions: List["Prescription"] = Relationship(back_populates="doctor")


class Prescription(BaseModel, table=True):
    id: Optional[int] = Field(primary_key=True)
    code: int
    patient_id: int = Field(foreign_key="patient.id")
    doctor_id: int = Field(foreign_key="doctor.id")

    prescriptionDetails: List["PrescriptionDetails"] = Relationship(back_populates="prescription")
    patient: Patient = Relationship(back_populates="prescriptions")
    doctor: Doctor = Relationship(back_populates="prescriptions")


class PrescriptionDetails(BaseModel, table=True):
    id: Optional[int] = Field(primary_key=True)
    prescription_id: int = Field(foreign_key="prescription.id")
    medicine_id: int = Field(foreign_key="medicine.id")
    qty: int

    prescription: Prescription = Relationship(back_populates="prescriptionDetails")
    medicine: Medicine = Relationship(back_populates="prescriptionDetails")

    @validator("qty", pre=True, always=True)
    def validate_qty(cls, value):
        if value <= 0:
            raise ValueError("La cantidad debe ser un número positivo mayor a 0")
        return value


class PrescriptionDetailsResponse(Base):
    code: int
    recipe_created_at: str
    patient: dict
    doctor: dict
    recipe: List[dict]
