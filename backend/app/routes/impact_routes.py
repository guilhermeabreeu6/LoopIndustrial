from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import or_

from app.database.db import get_db
from app.models.company import Company
from app.models.transaction import Transaction
from app.schemas.impact_schema import ImpactSummaryResponse
from app.auth.dependencies import get_current_company
from app.services.impact_service import calculate_estimated_co2_saved


router = APIRouter(
    prefix="/impact",
    tags=["Impact"]
)


@router.get(
    "/summary",
    response_model=ImpactSummaryResponse
)
def get_impact_summary(
    db: Session = Depends(get_db),
    current_company: Company = Depends(get_current_company)
):
    transactions = db.query(Transaction).filter(
        or_(
            Transaction.seller_company_id == current_company.id,
            Transaction.buyer_company_id == current_company.id
        ),
        Transaction.status == "completed"
    ).all()

    completed_transactions = len(transactions)
    total_sold_quantity = 0
    estimated_co2_saved_kg = 0

    for transaction in transactions:
        total_sold_quantity += transaction.quantity

        estimated_co2_saved_kg += calculate_estimated_co2_saved(
            material_type=transaction.material_type,
            quantity=transaction.quantity
        )

    return {
        "completed_transactions": completed_transactions,
        "total_sold_quantity": round(total_sold_quantity, 2),
        "estimated_co2_saved_kg": round(estimated_co2_saved_kg, 2)
    }