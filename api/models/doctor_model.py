from sqlmodel import Field, SQLModel, Relationship
from datetime import date, datetime
from typing import List, Optional
from pydantic import BaseModel, validator
from .base_model import Person


class Doctor(Person, table=True):
    prescriptions: List["Prescription"] = Relationship(back_populates="doctor")


class CreateDoctor(BaseModel):
    personal_id: int
    code: Optional[int]
    name: str
    lastname: str
    birthdate: date
