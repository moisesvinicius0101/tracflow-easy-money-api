
from sqlalchemy import Column, Integer, String, Numeric, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base
import enum
from sqlalchemy.dialects.postgresql import ENUM


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)

    transactions = relationship(
        "Transaction",
        back_populates="user"
    )


class TransactionType(enum.Enum):
    entrada = "entrada"
    saida = "saida"


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    description = Column(String, nullable=False)
    amount = Column(Numeric(10, 2), nullable=False)

    type = Column(
        ENUM(TransactionType, name="transaction_type"),
        nullable=False
    )

    date = Column(Date, nullable=False)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    user = relationship(
        "User",
        back_populates="transactions"
    )