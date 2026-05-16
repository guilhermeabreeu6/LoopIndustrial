from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.db import get_db
from app.models.company import Company
from app.models.residue import Residue
from app.models.interest import Interest
from app.models.transaction import Transaction
from app.schemas.dashboard_schema import DashboardSummaryResponse
from app.auth.dependencies import get_current_company


router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"]
)


@router.get(
    "/summary",
    response_model=DashboardSummaryResponse
)
def get_dashboard_summary(
    db: Session = Depends(get_db),
    current_company: Company = Depends(get_current_company)
):
    total_residues = db.query(Residue).filter(
        Residue.company_id == current_company.id
    ).count()

    available_residues = db.query(Residue).filter(
        Residue.company_id == current_company.id,
        Residue.status == "available"
    ).count()

    reserved_residues = db.query(Residue).filter(
        Residue.company_id == current_company.id,
        Residue.status == "reserved"
    ).count()

    sold_residues = db.query(Residue).filter(
        Residue.company_id == current_company.id,
        Residue.status == "sold"
    ).count()

    inactive_residues = db.query(Residue).filter(
        Residue.company_id == current_company.id,
        Residue.status == "inactive"
    ).count()

    sent_interests = db.query(Interest).filter(
        Interest.interested_company_id == current_company.id
    ).count()

    received_interests = db.query(Interest).filter(
        Interest.owner_company_id == current_company.id
    ).count()

    pending_received_interests = db.query(Interest).filter(
        Interest.owner_company_id == current_company.id,
        Interest.status == "pending"
    ).count()

    accepted_received_interests = db.query(Interest).filter(
        Interest.owner_company_id == current_company.id,
        Interest.status == "accepted"
    ).count()

    completed_sales = db.query(Transaction).filter(
        Transaction.seller_company_id == current_company.id,
        Transaction.status == "completed"
    ).count()

    completed_purchases = db.query(Transaction).filter(
        Transaction.buyer_company_id == current_company.id,
        Transaction.status == "completed"
    ).count()

    return {
        "total_residues": total_residues,
        "available_residues": available_residues,
        "reserved_residues": reserved_residues,
        "sold_residues": sold_residues,
        "inactive_residues": inactive_residues,
        "sent_interests": sent_interests,
        "received_interests": received_interests,
        "pending_received_interests": pending_received_interests,
        "accepted_received_interests": accepted_received_interests,
        "completed_sales": completed_sales,
        "completed_purchases": completed_purchases
    }