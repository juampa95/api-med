from sqlmodel import Field, SQLModel, Relationship
from pydantic import validator
from .base_model import Base
from typing import List
from .medicine_model import Medicine


class PrescriptionDetails(Base, table=True):
    prescription_id: int = Field(foreign_key="prescription.id")
    medicine_id: int = Field(foreign_key="medicine.id")
    qty: int
    # assigned_serials: List[str] = []

    prescription: "Prescription" = Relationship(back_populates="prescriptionDetails")
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
