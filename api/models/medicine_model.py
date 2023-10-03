from sqlmodel import Field, SQLModel, Relationship
from typing import List, Optional
from pydantic import validator
from .base_model import Base



class Medicine(Base, table=True):
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