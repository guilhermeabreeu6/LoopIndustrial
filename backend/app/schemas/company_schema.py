from datetime import datetime
from pydantic import BaseModel, EmailStr, Field


class CompanyCreate(BaseModel):
    company_name: str = Field(..., min_length=2, max_length=150)
    email: EmailStr
    password: str = Field(..., min_length=6, max_length=100)
    city: str = Field(..., min_length=2, max_length=100)
    state: str = Field(..., min_length=2, max_length=2)
    industry: str = Field(..., min_length=2, max_length=100)


class CompanyLogin(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=6, max_length=100)


class CompanyResponse(BaseModel):
    id: int
    company_name: str
    email: EmailStr
    city: str
    state: str
    industry: str
    created_at: datetime

    class Config:
        from_attributes = True