from sqlalchemy import Column, Integer, String, Text, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database.base import Base


class Residue(Base):
    __tablename__ = "residues"

    id = Column(Integer, primary_key=True, index=True)

    title = Column(String(150), nullable=False)
    description = Column(Text, nullable=True)

    material_type = Column(String(100), nullable=False)
    quantity = Column(Float, nullable=False)
    unit = Column(String(20), nullable=False)

    city = Column(String(100), nullable=False)
    state = Column(String(2), nullable=False)

    status = Column(String(30), default="available", nullable=False)

    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    company = relationship("Company", back_populates="residues")

    interests = relationship(
        "Interest",
        back_populates="residue",
        cascade="all, delete-orphan"
    )

    transactions = relationship(
        "Transaction",
        back_populates="residue"
    )