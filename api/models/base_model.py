from sqlmodel import Field, SQLModel, Relationship
from datetime import date, datetime
from typing import List, Optional
from pydantic import validator


class Base(SQLModel):
    id: Optional[int] = Field(primary_key=True, index=True, description="Código id creado automáticamente")
    created_at: datetime = Field(default_factory=datetime.now)
    update_at: datetime = Field(default_factory=datetime.now)

    def on_update(self):
        self.update_at = datetime.now()


class Person(Base):
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