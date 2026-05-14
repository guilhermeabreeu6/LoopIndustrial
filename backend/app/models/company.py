from sqlalchemy import Column, Integer, String, DateTime
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