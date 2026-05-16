from datetime import datetime
from pydantic import BaseModel, Field


class InterestCompanyResponse(BaseModel):
    id: int
    company_name: str
    email: str
    city: str
    state: str
    industry: str

    class Config:
        from_attributes = True


class InterestResidueResponse(BaseModel):
    id: int
    title: str
    material_type: str
    quantity: float
    unit: str
    city: str
    state: str
    status: str

    class Config:
        from_attributes = True


class InterestCreate(BaseModel):
    message: str | None = Field(None, max_length=1000)


class InterestStatusUpdate(BaseModel):
    status: str = Field(..., min_length=2, max_length=30)


class InterestCompletion(BaseModel):
    final_notes: str | None = Field(None, max_length=1000)


class InterestResponse(BaseModel):
    id: int
    message: str | None
    status: str

    residue_id: int
    interested_company_id: int
    owner_company_id: int

    created_at: datetime

    residue: InterestResidueResponse | None = None
    interested_company: InterestCompanyResponse | None = None
    owner_company: InterestCompanyResponse | None = None

    class Config:
        from_attributes = True