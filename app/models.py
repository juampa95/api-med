from sqlmodel import Field, SQLModel, Relationship
from datetime import date, datetime
from typing import List, Optional


class Base(SQLModel):
    id: Optional[int] = Field(primary_key=True, index=True)


class BaseModel(SQLModel):
    created_at: datetime = Field(default_factory=datetime.now)
    update_at: datetime = Field(default_factory=datetime.now)

    def on_update(self):
        self.update_at = datetime.now()


class Person(BaseModel):
    personal_id: int
    code: Optional[int]
    name: str
    lastname: str
    birthdate: date


class Medicine(BaseModel, table=True):
    id: Optional[int] = Field(primary_key=True, index=True)
    code: Optional[int]
    name: str
    drug: str
    concentration: str
    form: str
    gtin: str
    prescriptionDetails: List["PrescriptionDetails"] = Relationship(back_populates="medicine")


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



class PrescriptionDetailsResponse(BaseModel):
    id: int
    qty: int
    prescription_id: int
    medicine_id: int
    prescription: dict
    medicine: dict
