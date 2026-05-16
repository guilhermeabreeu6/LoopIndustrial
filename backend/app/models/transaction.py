from sqlalchemy import Column, Integer, String, Text, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database.base import Base


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)

    residue_id = Column(Integer, ForeignKey("residues.id"), nullable=False)
    interest_id = Column(Integer, ForeignKey("interests.id"), nullable=False)

    seller_company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)
    buyer_company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)

    material_type = Column(String(100), nullable=False)
    quantity = Column(Float, nullable=False)
    unit = Column(String(20), nullable=False)

    status = Column(String(30), default="completed", nullable=False)
    final_notes = Column(Text, nullable=True)

    completed_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    residue = relationship("Residue", back_populates="transactions")
    interest = relationship("Interest", back_populates="transaction")

    seller_company = relationship(
        "Company",
        foreign_keys=[seller_company_id],
        back_populates="sales_transactions"
    )

    buyer_company = relationship(
        "Company",
        foreign_keys=[buyer_company_id],
        back_populates="purchase_transactions"
    )