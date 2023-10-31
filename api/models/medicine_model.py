from sqlmodel import Field, SQLModel, Relationship, UniqueConstraint
from enum import Enum
from typing import List, Optional
from pydantic import validator
from .base_model import Base


class Status(str,Enum):
    AVAILABLE = 'AVAILABLE'
    DISPENSED = 'DISPENSED'
    APPLIED = 'APPLIED'
    DESTROYED = 'DESTROYED'


class MoveType(str, Enum):
    IN = 'IN'
    OUT = 'OUT'
    RETURN = 'RETURN'
    DESTROY = 'DESTROY'
    DISPENSE = 'DISPENSE'



class Medicine(Base, table=True):
    """
    Clase para crear medicamentos. Relacionada con el stock, prescripciones, etc.
    """
    provider_code: Optional[str]
    name: str
    drug: str
    concentration: str
    gtin: str
    form: Optional[str]
    stock: int = 0
    prescriptionDetails: List["PrescriptionDetails"] = Relationship(back_populates="medicine")
    stockMedicine: List["StockMedicine"] = Relationship(back_populates="medicine")

    @validator("stock", pre=True, always=True)
    def validate_stock(cls, value):
        if value < 0:
            raise ValueError("El stock no puede ser menor a 0")
        return value

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
    """
    Clase para ingresar al stock medicamentos unicos con un serial y medicine_id unicos.
    Tambien tendremos el estado actual de cada medicamento, que eso se modificara desde
    el back en funcion de los movimientos que quedaran registrados en la tabla StockMovements.
    En caso de que el medicamento tenga estatus DISPENSED o APPLIED deberia indicar la receta
    a la cual esta asignado.
    """
    medicine_id: int = Field(foreign_key="medicine.id")
    prescription_id: Optional[int] = Field(foreign_key="prescription.id")
    status: Status
    serial: str

    prescription: "Prescription" = Relationship(back_populates="stockMedicine")
    medicine: Medicine = Relationship(back_populates="stockMedicine")
    stockMovements: List["StockMovements"] = Relationship(back_populates="stockmedicine")

    __table_args__ = (
            UniqueConstraint('medicine_id', 'serial'),
    )

    @validator("serial", pre=True, always=True)
    def validate_serial_char(cls, value):
        if len(value) > 21:
            raise ValueError("El serial puede contener 21 caracteres")
        return value


class StockMovements(Base, table=True):
    """
    En esa tabla, quedara un registro del movimiento de cada medicamento segun su id y serial.
    Sirve para dar una trazabilidad a los medicamentos.
    """
    stock_medicine_id: int = Field(foreign_key='stockmedicine.id')
    movement_type: MoveType = Field(default=MoveType.IN)

    stockmedicine: StockMedicine = Relationship(back_populates="stockMovements")


class LoadStockMedicine(SQLModel):
    medicine_id: int = Field(foreign_key="medicine.id")
    status: Status = Status.AVAILABLE
    movement_type: MoveType = MoveType.IN
    serial: List[str]


class DispenseMedicine(SQLModel):
    """
    Objeto utilizado para enviar informacion de los medicamentos incluidos en una receta,
    ofrece dos modos de funcionamiento \n
    1- En el body enviar una lista vacia, esto asignara los medicamentos mas antiguos a la receta. \n
    2- En el body enviar una lista de DispenseMedicine, esto asignara a la receta el/los medicamentos segun el serial enviado
    """
    medicine_id: int = Field(foreign_key="medicine.id")
    serials: List[str]