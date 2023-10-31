from sqlmodel import Field, SQLModel, Relationship
from typing import List, Optional
from pydantic import validator
from .base_model import Base
from .patients_model import Patient
from .doctor_model import Doctor
from enum import Enum

class PrescriptionStatus(str,Enum):
    CREATED = 'CREATED'
    DISPENSED = 'DISPENSED'
    APPLIED = 'APPLIED'
    DESTROYED = 'DESTROYED'



class Prescription(Base, table=True):
    code: int
    patient_id: int = Field(foreign_key="patient.id")
    doctor_id: int = Field(foreign_key="doctor.id")
    status: PrescriptionStatus = PrescriptionStatus.CREATED

    prescriptionDetails: List["PrescriptionDetails"] = Relationship(back_populates="prescription")
    patient: Patient = Relationship(back_populates="prescriptions")
    doctor: Doctor = Relationship(back_populates="prescriptions")
    stockMedicine: List["StockMedicine"] = Relationship(back_populates="prescription")
