

from app.models import Transaction
from sqlalchemy.orm import Session
from app.schemas.transaction import TransactionCreate
from sqlalchemy import func
from fastapi import HTTPException


def create_transaction_service(db: Session, transaction: TransactionCreate, user_id: int):
    try:
        # Vincula a transação ao usuário logado
        transaction_model = Transaction(**transaction.model_dump(), user_id=user_id)
        db.add(transaction_model)
        db.commit()
        db.refresh(transaction_model)
        return transaction_model
    except Exception as e:
        db.rollback()
        raise e


def get_transaction_summary(db: Session, user_id: int):
    # Filtra apenas as transações do usuário
    total_entradas = (
        db.query(func.sum(Transaction.amount))
        .filter(Transaction.type == "entrada", Transaction.user_id == user_id)
        .scalar() or 0
    )
    total_saidas = (
        db.query(func.sum(Transaction.amount))
        .filter(Transaction.type == "saida", Transaction.user_id == user_id)
        .scalar() or 0
    )
    saldo_total = total_entradas - total_saidas

    return {
        "saldo_total": saldo_total,
        "entradas": total_entradas,
        "saidas": total_saidas,
    }


def get_all_transactions(db: Session, user_id: int):
    # Retorna apenas as transações do usuário logado
    return db.query(Transaction).filter(Transaction.user_id == user_id).all()


def delete_transaction_service(db: Session, transaction_id: int, user_id: int):
    transaction = (
        db.query(Transaction)
        .filter(Transaction.id == transaction_id, Transaction.user_id == user_id)
        .first()
    )

    if not transaction:
        # Esconde se existe mas é de outro usuário (segurança)
        raise HTTPException(status_code=404, detail="Transação não encontrada")

    db.delete(transaction)
    db.commit()