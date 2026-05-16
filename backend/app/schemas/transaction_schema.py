from datetime import datetime
from pydantic import BaseModel


class TransactionCompanyResponse(BaseModel):
    id: int
    company_name: str
    email: str
    city: str
    state: str
    industry: str

    class Config:
        from_attributes = True


class TransactionResidueResponse(BaseModel):
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


class TransactionResponse(BaseModel):
    id: int

    residue_id: int
    interest_id: int

    seller_company_id: int
    buyer_company_id: int

    material_type: str
    quantity: float
    unit: str

    status: str
    final_notes: str | None

    completed_at: datetime

    residue: TransactionResidueResponse | None = None
    seller_company: TransactionCompanyResponse | None = None
    buyer_company: TransactionCompanyResponse | None = None

    class Config:
        from_attributes = True