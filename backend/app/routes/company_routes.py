from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.db import get_db
from app.models.company import Company
from app.schemas.company_schema import CompanyCreate, CompanyLogin, CompanyResponse
from app.auth.hashing import hash_password, verify_password
from app.auth.jwt_handler import create_access_token
from app.auth.dependencies import get_current_company


router = APIRouter(
    prefix="/companies",
    tags=["Companies"]
)


@router.post(
    "/register",
    response_model=CompanyResponse,
    status_code=status.HTTP_201_CREATED
)
def register_company(company_data: CompanyCreate, db: Session = Depends(get_db)):
    existing_company = db.query(Company).filter(
        Company.email == company_data.email
    ).first()

    if existing_company:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email is already registered."
        )

    new_company = Company(
        company_name=company_data.company_name,
        email=company_data.email,
        hashed_password=hash_password(company_data.password),
        city=company_data.city,
        state=company_data.state.upper(),
        industry=company_data.industry
    )

    db.add(new_company)
    db.commit()
    db.refresh(new_company)

    return new_company


@router.post("/login")
def login_company(company_data: CompanyLogin, db: Session = Depends(get_db)):
    company = db.query(Company).filter(
        Company.email == company_data.email
    ).first()

    if not company:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password."
        )

    if not verify_password(company_data.password, company.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password."
        )

    access_token = create_access_token(
        data={
            "sub": company.email,
            "company_id": company.id
        }
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


@router.get("/me", response_model=CompanyResponse)
def get_logged_company(current_company: Company = Depends(get_current_company)):
    return current_company