from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database.base import Base


class Interest(Base):
    __tablename__ = "interests"

    id = Column(Integer, primary_key=True, index=True)

    message = Column(Text, nullable=True)
    status = Column(String(30), default="pending", nullable=False)

    residue_id = Column(Integer, ForeignKey("residues.id"), nullable=False)
    interested_company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)
    owner_company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    residue = relationship("Residue", back_populates="interests")

    interested_company = relationship(
        "Company",
        foreign_keys=[interested_company_id],
        back_populates="sent_interests"
    )

    owner_company = relationship(
        "Company",
        foreign_keys=[owner_company_id],
        back_populates="received_interests"
    )

    transaction = relationship(
        "Transaction",
        back_populates="interest",
        uselist=False
    )