from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import or_

from app.database.db import get_db
from app.models.company import Company
from app.models.transaction import Transaction
from app.schemas.transaction_schema import TransactionResponse
from app.auth.dependencies import get_current_company


router = APIRouter(
    prefix="/transactions",
    tags=["Transactions"]
)


@router.get(
    "",
    response_model=list[TransactionResponse]
)
def list_my_transactions(
    db: Session = Depends(get_db),
    current_company: Company = Depends(get_current_company)
):
    transactions = db.query(Transaction).options(
        joinedload(Transaction.residue),
        joinedload(Transaction.seller_company),
        joinedload(Transaction.buyer_company)
    ).filter(
        or_(
            Transaction.seller_company_id == current_company.id,
            Transaction.buyer_company_id == current_company.id
        )
    ).order_by(
        Transaction.completed_at.desc()
    ).all()

    return transactions


@router.get(
    "/sales",
    response_model=list[TransactionResponse]
)
def list_my_sales_transactions(
    db: Session = Depends(get_db),
    current_company: Company = Depends(get_current_company)
):
    transactions = db.query(Transaction).options(
        joinedload(Transaction.residue),
        joinedload(Transaction.seller_company),
        joinedload(Transaction.buyer_company)
    ).filter(
        Transaction.seller_company_id == current_company.id
    ).order_by(
        Transaction.completed_at.desc()
    ).all()

    return transactions


@router.get(
    "/purchases",
    response_model=list[TransactionResponse]
)
def list_my_purchase_transactions(
    db: Session = Depends(get_db),
    current_company: Company = Depends(get_current_company)
):
    transactions = db.query(Transaction).options(
        joinedload(Transaction.residue),
        joinedload(Transaction.seller_company),
        joinedload(Transaction.buyer_company)
    ).filter(
        Transaction.buyer_company_id == current_company.id
    ).order_by(
        Transaction.completed_at.desc()
    ).all()

    return transactions