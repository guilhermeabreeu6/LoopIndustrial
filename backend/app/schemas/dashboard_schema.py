from pydantic import BaseModel


class DashboardSummaryResponse(BaseModel):
    total_residues: int
    available_residues: int
    reserved_residues: int
    sold_residues: int
    inactive_residues: int

    sent_interests: int
    received_interests: int
    pending_received_interests: int
    accepted_received_interests: int

    completed_sales: int
    completed_purchases: int