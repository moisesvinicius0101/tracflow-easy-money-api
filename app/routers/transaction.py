

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.transaction import TransactionCreate, TransactionResponse
from typing import Annotated, List

from app.service.transaction_service import (
    create_transaction_service,
    get_transaction_summary,
    get_all_transactions,
    delete_transaction_service
)

router = APIRouter(prefix="/transaction", tags=["transaction"])

db_dependency = Annotated[Session, Depends(get_db)]


@router.post("/", response_model=TransactionResponse, status_code=status.HTTP_201_CREATED)
async def create_transaction(transaction: TransactionCreate, db: db_dependency):
    return create_transaction_service(transaction=transaction, db=db)


@router.get("/", response_model=List[TransactionResponse])
async def read_all_transactions(db: db_dependency):
    return get_all_transactions(db)


@router.get("/summary")
async def read_transaction_summary(db: db_dependency):
    return get_transaction_summary(db)


@router.delete("/{transaction_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_transaction(transaction_id: int, db: db_dependency):
    delete_transaction_service(transaction_id=transaction_id, db=db)