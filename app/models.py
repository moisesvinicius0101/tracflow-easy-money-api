
from sqlalchemy import Column, Integer, String, Numeric, Date, Enum
from app.database import Base
import enum


class TransactionType(str, enum.Enum):
    entrada = "entrada"
    saida = "saida"


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    description = Column(String, nullable=False)
    amount = Column(Numeric(10, 2), nullable=False)

    type = Column(
        Enum(TransactionType),
        nullable=False
    )

    date = Column(Date, nullable=False)