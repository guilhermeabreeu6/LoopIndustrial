from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload

from app.database.db import get_db
from app.models.company import Company
from app.models.residue import Residue
from app.models.interest import Interest
from app.models.transaction import Transaction

from app.schemas.interest_schema import (
    InterestCreate,
    InterestStatusUpdate,
    InterestCompletion,
    InterestResponse
)
from app.auth.dependencies import get_current_company


router = APIRouter(
    prefix="/interests",
    tags=["Interests"]
)


@router.post(
    "/residues/{residue_id}",
    response_model=InterestResponse,
    status_code=status.HTTP_201_CREATED
)
def create_interest(
    residue_id: int,
    interest_data: InterestCreate,
    db: Session = Depends(get_db),
    current_company: Company = Depends(get_current_company)
):
    residue = db.query(Residue).filter(
        Residue.id == residue_id
    ).first()

    if not residue:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Residue not found."
        )

    if residue.status != "available":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This residue is not available."
        )

    if residue.company_id == current_company.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You cannot create interest in your own residue."
        )

    existing_interest = db.query(Interest).filter(
        Interest.residue_id == residue.id,
        Interest.interested_company_id == current_company.id
    ).first()

    if existing_interest:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Interest already created for this residue."
        )

    new_interest = Interest(
        message=interest_data.message,
        residue_id=residue.id,
        interested_company_id=current_company.id,
        owner_company_id=residue.company_id
    )

    db.add(new_interest)
    db.commit()
    db.refresh(new_interest)

    interest = db.query(Interest).options(
        joinedload(Interest.residue),
        joinedload(Interest.interested_company),
        joinedload(Interest.owner_company)
    ).filter(
        Interest.id == new_interest.id
    ).first()

    return interest


@router.get(
    "/sent",
    response_model=list[InterestResponse]
)
def list_sent_interests(
    db: Session = Depends(get_db),
    current_company: Company = Depends(get_current_company)
):
    interests = db.query(Interest).options(
        joinedload(Interest.residue),
        joinedload(Interest.interested_company),
        joinedload(Interest.owner_company)
    ).filter(
        Interest.interested_company_id == current_company.id
    ).order_by(
        Interest.created_at.desc()
    ).all()

    return interests


@router.get(
    "/received",
    response_model=list[InterestResponse]
)
def list_received_interests(
    db: Session = Depends(get_db),
    current_company: Company = Depends(get_current_company)
):
    interests = db.query(Interest).options(
        joinedload(Interest.residue),
        joinedload(Interest.interested_company),
        joinedload(Interest.owner_company)
    ).filter(
        Interest.owner_company_id == current_company.id
    ).order_by(
        Interest.created_at.desc()
    ).all()

    return interests


@router.patch(
    "/{interest_id}/status",
    response_model=InterestResponse
)
def update_interest_status(
    interest_id: int,
    status_data: InterestStatusUpdate,
    db: Session = Depends(get_db),
    current_company: Company = Depends(get_current_company)
):
    allowed_statuses = ["pending", "accepted", "rejected", "cancelled"]

    if status_data.status not in allowed_statuses:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid interest status."
        )

    interest = db.query(Interest).options(
        joinedload(Interest.residue),
        joinedload(Interest.interested_company),
        joinedload(Interest.owner_company)
    ).filter(
        Interest.id == interest_id
    ).first()

    if not interest:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Interest not found."
        )

    is_owner = interest.owner_company_id == current_company.id
    is_sender = interest.interested_company_id == current_company.id

    if not is_owner and not is_sender:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not allowed to update this interest."
        )

    if status_data.status in ["accepted", "rejected"] and not is_owner:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only the residue owner can accept or reject this interest."
        )

    if status_data.status == "cancelled" and not is_sender:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only the interested company can cancel this interest."
        )

    if status_data.status == "accepted":
        if interest.residue.status != "available":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="This residue is no longer available."
            )

        interest.status = "accepted"
        interest.residue.status = "reserved"

    elif status_data.status == "rejected":
        interest.status = "rejected"

    elif status_data.status == "cancelled":
        if interest.status == "accepted":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Accepted interests cannot be cancelled."
            )

        interest.status = "cancelled"

    elif status_data.status == "pending":
        interest.status = "pending"

    db.commit()
    db.refresh(interest)

    updated_interest = db.query(Interest).options(
        joinedload(Interest.residue),
        joinedload(Interest.interested_company),
        joinedload(Interest.owner_company)
    ).filter(
        Interest.id == interest.id
    ).first()

    return updated_interest


@router.patch(
    "/{interest_id}/complete",
    response_model=InterestResponse
)
def complete_interest(
    interest_id: int,
    completion_data: InterestCompletion,
    db: Session = Depends(get_db),
    current_company: Company = Depends(get_current_company)
):
    interest = db.query(Interest).options(
        joinedload(Interest.residue),
        joinedload(Interest.interested_company),
        joinedload(Interest.owner_company)
    ).filter(
        Interest.id == interest_id
    ).first()

    if not interest:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Interest not found."
        )

    if interest.owner_company_id != current_company.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only the residue owner can complete this negotiation."
        )

    if interest.status != "accepted":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only accepted interests can be completed."
        )

    if interest.residue.status != "reserved":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only reserved residues can be marked as sold."
        )

    existing_transaction = db.query(Transaction).filter(
        Transaction.interest_id == interest.id
    ).first()

    if existing_transaction:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Transaction already exists for this interest."
        )

    interest.status = "completed"
    interest.residue.status = "sold"

    new_transaction = Transaction(
        residue_id=interest.residue_id,
        interest_id=interest.id,
        seller_company_id=interest.owner_company_id,
        buyer_company_id=interest.interested_company_id,
        material_type=interest.residue.material_type,
        quantity=interest.residue.quantity,
        unit=interest.residue.unit,
        status="completed",
        final_notes=completion_data.final_notes
    )

    db.add(new_transaction)
    db.commit()
    db.refresh(interest)

    completed_interest = db.query(Interest).options(
        joinedload(Interest.residue),
        joinedload(Interest.interested_company),
        joinedload(Interest.owner_company)
    ).filter(
        Interest.id == interest.id
    ).first()

    return completed_interest