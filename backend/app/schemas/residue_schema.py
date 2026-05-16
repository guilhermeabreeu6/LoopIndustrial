from datetime import datetime
from pydantic import BaseModel, Field


class ResidueCompanyResponse(BaseModel):
    id: int
    company_name: str
    city: str
    state: str
    industry: str

    class Config:
        from_attributes = True


class ResidueCreate(BaseModel):
    title: str = Field(..., min_length=2, max_length=150)
    description: str | None = Field(None, max_length=1000)

    material_type: str = Field(..., min_length=2, max_length=100)
    quantity: float = Field(..., gt=0)
    unit: str = Field(..., min_length=1, max_length=20)

    city: str = Field(..., min_length=2, max_length=100)
    state: str = Field(..., min_length=2, max_length=2)


class ResidueUpdate(BaseModel):
    title: str | None = Field(None, min_length=2, max_length=150)
    description: str | None = Field(None, max_length=1000)

    material_type: str | None = Field(None, min_length=2, max_length=100)
    quantity: float | None = Field(None, gt=0)
    unit: str | None = Field(None, min_length=1, max_length=20)

    city: str | None = Field(None, min_length=2, max_length=100)
    state: str | None = Field(None, min_length=2, max_length=2)
    status: str | None = Field(None, min_length=2, max_length=30)


class ResidueResponse(BaseModel):
    id: int
    title: str
    description: str | None

    material_type: str
    quantity: float
    unit: str

    city: str
    state: str
    status: str

    company_id: int
    created_at: datetime

    company: ResidueCompanyResponse | None = None

    class Config:
        from_attributes = True