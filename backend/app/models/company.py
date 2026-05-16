from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database.base import Base


class Company(Base):
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True, index=True)

    company_name = Column(String(150), nullable=False)
    email = Column(String(150), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)

    city = Column(String(100), nullable=False)
    state = Column(String(2), nullable=False)
    industry = Column(String(100), nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    residues = relationship(
        "Residue",
        back_populates="company",
        cascade="all, delete-orphan"
    )

    sent_interests = relationship(
        "Interest",
        foreign_keys="Interest.interested_company_id",
        back_populates="interested_company",
        cascade="all, delete-orphan"
    )

    received_interests = relationship(
        "Interest",
        foreign_keys="Interest.owner_company_id",
        back_populates="owner_company",
        cascade="all, delete-orphan"
    )

    sales_transactions = relationship(
        "Transaction",
        foreign_keys="Transaction.seller_company_id",
        back_populates="seller_company"
    )

    purchase_transactions = relationship(
        "Transaction",
        foreign_keys="Transaction.buyer_company_id",
        back_populates="buyer_company"
    )