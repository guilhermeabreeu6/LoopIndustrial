from pydantic import BaseModel


class ImpactSummaryResponse(BaseModel):
    completed_transactions: int
    total_sold_quantity: float
    estimated_co2_saved_kg: float