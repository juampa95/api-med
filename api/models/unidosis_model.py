from sqlmodel import Field, SQLModel
from datetime import datetime
from typing import Optional
from pydantic import validator
from .medicine_model import Medicine


class Base2(SQLModel):
    id: Optional[int] = Field(primary_key=True, index=True, description="Código id creado automáticamente")


class BaseModel2(Base2):
    created_at: datetime = Field(default_factory=datetime.now)
    update_at: datetime = Field(default_factory=datetime.now)

    def on_update(self):
        self.update_at = datetime.now()


class UnidosisMedicine(BaseModel2, table=True):
    visual_config1: Optional[str] = Field(default="")
    visual_config2: Optional[str] = Field(default="")
    visual_config3: Optional[str] = Field(default="")
    visual_config4: Optional[str] = Field(default="")
    adv1: Optional[bool] = Field(default=False)
    adv2: Optional[bool] = Field(default=False)
    adv3: Optional[bool] = Field(default=False)
    adv4: Optional[bool] = Field(default=False)
    adv5: Optional[bool] = Field(default=False)
    tac: Optional[bool] = Field(default=False)
    pregnancy_cat: Optional[str]

    medicine_id: int = Field(foreign_key=Medicine.id, nullable=False)


    @validator("pregnancy_cat", pre=True, always=False)
    def validate_pregnacy_cat(cls, value):
        if len(value) > 4:
            raise ValueError("La categoria de embarazo puede tener un maximo de 3 caracteres")
        value = str.capitalize(value)
        return value
