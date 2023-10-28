from sqlmodel import Field, SQLModel, Relationship, UniqueConstraint
from enum import Enum
from typing import List, Optional
from pydantic import validator
from .base_model import Base

class MovementType(str,Enum):
    IN = 'IN'
    OUT = 'OUT'
    DEV = 'DEV'

class Medicine(Base, table=True):
    code: Optional[int]
    name: str
    drug: str
    concentration: str
    form: Optional[str]
    gtin: str
    prescriptionDetails: List["PrescriptionDetails"] = Relationship(back_populates="medicine")
    stockMedicine: List["StockMedicine"] = Relationship(back_populates="medicine")

    @validator("gtin", pre=True, always=True)
    def validate_gtin_format(cls, value):
        # Verifico que cada caracter sea un dígito numérico
        if not value.isdigit():
            raise ValueError("El GTIN debe estar conformado solo por números enteros")

        # # Esta verificacion la voy a quitar y hare que se completen con 0 hasta los 14 digitos si o si
        # # Verifico que tenga 13 o 14 dígitos
        # if len(value) != 13 and len(value) != 14:
        #     raise ValueError("El GTIN debe contener 13 o 14 dígitos")
        #
        # # Si tiene 13 dígitos, agregamos un "0" al principio
        # if len(value) == 13:
        #     value = "0" + value

        # # Esta verificacion hay que quitarla si se usa la anterior
        # Si tiene menos de 14 dígitos, agregamos ceros a la izquierda
        while len(value) < 14:
            value = "0" + value

        return value


class StockMedicine(Base, table=True):
    medicine_id: int = Field(foreign_key="medicine.id")
    movement_type: MovementType
    serial: str
    is_active: bool = True
    accumulated_stock: int

    medicine: Medicine = Relationship(back_populates="stockMedicine")

    __table_args__ = (
            UniqueConstraint('medicine_id', 'serial'),
    )

    @validator("serial", pre=True, always=True)
    def validate_serial_char(cls, value):
        if len(value) > 21:
            raise ValueError("El serial puede contener 21 caracteres")
        return value

    @validator("accumulated_stock", pre=True, always=True)
    def validate_stock(cls, value):
        if value <= 0:
            raise ValueError("El stock no puede ser menor a 0")
        return value


class LoadStockMedicine(SQLModel):
    medicine_id: int = Field(foreign_key="medicine.id")
    movement_type: MovementType = MovementType.IN
    serial: str
