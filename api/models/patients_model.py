from datetime import date
from sqlmodel import Field, SQLModel, Relationship
from typing import List, Optional
from pydantic import BaseModel, validator
from api.models.base_model import Person


class Patient(Person, table=True):
    prescriptions: List["Prescription"] = Relationship(back_populates="patient")


class CreatePatient(BaseModel):
    personal_id: int
    code: Optional[int]
    name: str
    lastname: str
    birthdate: date
