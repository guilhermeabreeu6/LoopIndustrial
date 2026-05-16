from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from app.database.db import get_db
from app.models.company import Company
from app.auth.jwt_handler import decode_access_token


security = HTTPBearer()


def get_current_company(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials.",
        headers={"WWW-Authenticate": "Bearer"},
    )

    token = credentials.credentials

    payload = decode_access_token(token)

    if payload is None:
        raise credentials_exception

    company_id = payload.get("company_id")

    if company_id is None:
        raise credentials_exception

    company = db.query(Company).filter(
        Company.id == company_id
    ).first()

    if company is None:
        raise credentials_exception

    return company