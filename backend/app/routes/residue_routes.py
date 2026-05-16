from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import or_

from app.database.db import get_db
from app.models.company import Company
from app.models.residue import Residue
from app.schemas.residue_schema import ResidueCreate, ResidueUpdate, ResidueResponse
from app.auth.dependencies import get_current_company


router = APIRouter(
    prefix="/residues",
    tags=["Residues"]
)


@router.post(
    "",
    response_model=ResidueResponse,
    status_code=status.HTTP_201_CREATED
)
def create_residue(
    residue_data: ResidueCreate,
    db: Session = Depends(get_db),
    current_company: Company = Depends(get_current_company)
):
    new_residue = Residue(
        title=residue_data.title,
        description=residue_data.description,
        material_type=residue_data.material_type,
        quantity=residue_data.quantity,
        unit=residue_data.unit,
        city=residue_data.city,
        state=residue_data.state.upper(),
        company_id=current_company.id
    )

    db.add(new_residue)
    db.commit()
    db.refresh(new_residue)

    return new_residue


@router.get(
    "",
    response_model=list[ResidueResponse]
)
def list_available_residues(
    search: str | None = Query(None, min_length=2, max_length=100),
    material_type: str | None = Query(None, min_length=2, max_length=100),
    city: str | None = Query(None, min_length=2, max_length=100),
    state: str | None = Query(None, min_length=2, max_length=2),
    min_quantity: float | None = Query(None, gt=0),
    status_value: str = Query("available", min_length=2, max_length=30),
    db: Session = Depends(get_db)
):
    query = db.query(Residue).options(
        joinedload(Residue.company)
    )

    if status_value:
        query = query.filter(Residue.status == status_value)

    if search:
        search_pattern = f"%{search}%"

        query = query.filter(
            or_(
                Residue.title.ilike(search_pattern),
                Residue.description.ilike(search_pattern),
                Residue.material_type.ilike(search_pattern),
                Residue.city.ilike(search_pattern),
                Residue.state.ilike(search_pattern)
            )
        )

    if material_type:
        query = query.filter(Residue.material_type.ilike(f"%{material_type}%"))

    if city:
        query = query.filter(Residue.city.ilike(f"%{city}%"))

    if state:
        query = query.filter(Residue.state == state.upper())

    if min_quantity:
        query = query.filter(Residue.quantity >= min_quantity)

    residues = query.order_by(
        Residue.created_at.desc()
    ).all()

    return residues


@router.get(
    "/my-residues",
    response_model=list[ResidueResponse]
)
def list_my_residues(
    db: Session = Depends(get_db),
    current_company: Company = Depends(get_current_company)
):
    residues = db.query(Residue).options(
        joinedload(Residue.company)
    ).filter(
        Residue.company_id == current_company.id
    ).order_by(
        Residue.created_at.desc()
    ).all()

    return residues


@router.put(
    "/{residue_id}",
    response_model=ResidueResponse
)
def update_residue(
    residue_id: int,
    residue_data: ResidueUpdate,
    db: Session = Depends(get_db),
    current_company: Company = Depends(get_current_company)
):
    residue = db.query(Residue).options(
        joinedload(Residue.company)
    ).filter(
        Residue.id == residue_id
    ).first()

    if not residue:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Residue not found."
        )

    if residue.company_id != current_company.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not allowed to update this residue."
        )

    update_data = residue_data.model_dump(exclude_unset=True)

    if "state" in update_data and update_data["state"]:
        update_data["state"] = update_data["state"].upper()

    for field, value in update_data.items():
        setattr(residue, field, value)

    db.commit()
    db.refresh(residue)

    return residue


@router.patch(
    "/{residue_id}/status",
    response_model=ResidueResponse
)
def update_residue_status(
    residue_id: int,
    status_value: str,
    db: Session = Depends(get_db),
    current_company: Company = Depends(get_current_company)
):
    allowed_statuses = ["available", "reserved", "sold", "inactive"]

    if status_value not in allowed_statuses:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid status."
        )

    residue = db.query(Residue).options(
        joinedload(Residue.company)
    ).filter(
        Residue.id == residue_id
    ).first()

    if not residue:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Residue not found."
        )

    if residue.company_id != current_company.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not allowed to update this residue."
        )

    residue.status = status_value

    db.commit()
    db.refresh(residue)

    return residue


@router.delete(
    "/{residue_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_residue(
    residue_id: int,
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

    if residue.company_id != current_company.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not allowed to delete this residue."
        )

    db.delete(residue)
    db.commit()

    return None


@router.get(
    "/{residue_id}",
    response_model=ResidueResponse
)
def get_residue_by_id(
    residue_id: int,
    db: Session = Depends(get_db)
):
    residue = db.query(Residue).options(
        joinedload(Residue.company)
    ).filter(
        Residue.id == residue_id
    ).first()

    if not residue:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Residue not found."
        )

    return residue