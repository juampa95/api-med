from sqlmodel import Field, SQLModel, Relationship
from datetime import date, datetime
from typing import List, Optional
from pydantic import validator
from .base_model import Person



class Doctor(Person, table=True):
    prescriptions: List["Prescription"] = Relationship(back_populates="doctor")