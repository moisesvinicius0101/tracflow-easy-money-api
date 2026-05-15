

from pydantic import BaseModel, Field, field_validator
from datetime import date
from decimal import Decimal
from enum import Enum


class TransactionType(str, Enum):
    entrada = "entrada"
    saida = "saida"


class TransactionCreate(BaseModel):
    description: str
    amount: Decimal
    type: TransactionType
    date: date

    @field_validator("type", mode="before")
    @classmethod
    def normalize_type(cls, value):
        return value.lower()


class TransactionResponse(TransactionCreate):
    id: int = Field(gt=0)

    class Config:
        from_attributes = True