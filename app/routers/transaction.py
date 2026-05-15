

from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from typing import Annotated, List

from app.database import get_db
from app.models import User
from app.schemas.transaction import TransactionCreate, TransactionResponse
from app.routers.auth import get_current_user
from app.service.transaction_service import (
    create_transaction_service,
    get_transaction_summary,
    get_all_transactions,
    delete_transaction_service,
)

router = APIRouter(prefix="/transaction", tags=["transaction"])

db_dependency = Annotated[Session, Depends(get_db)]
# Toda rota agora exige usuário logado
current_user_dependency = Annotated[User, Depends(get_current_user)]


@router.post("/", response_model=TransactionResponse, status_code=status.HTTP_201_CREATED)
async def create_transaction(
    transaction: TransactionCreate,
    db: db_dependency,
    current_user: current_user_dependency,
):
    # Passa o user_id do usuário logado para o service
    return create_transaction_service(transaction=transaction, db=db, user_id=current_user.id)


@router.get("/", response_model=List[TransactionResponse])
async def read_all_transactions(
    db: db_dependency,
    current_user: current_user_dependency,
):
    # Retorna apenas as transações do usuário logado
    return get_all_transactions(db=db, user_id=current_user.id)


@router.get("/summary")
async def read_transaction_summary(
    db: db_dependency,
    current_user: current_user_dependency,
):
    # Resumo financeiro apenas do usuário logado
    return get_transaction_summary(db=db, user_id=current_user.id)


@router.delete("/{transaction_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_transaction(
    transaction_id: int,
    db: db_dependency,
    current_user: current_user_dependency,
):
    # Garante que o usuário só pode deletar suas próprias transações
    delete_transaction_service(
        transaction_id=transaction_id,
        db=db,
        user_id=current_user.id,
    )