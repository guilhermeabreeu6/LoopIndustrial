from sqlalchemy.orm import declarative_base

Base = declarative_base()

from app.models.company import Company
from app.models.residue import Residue
from app.models.interest import Interest
from app.models.transaction import Transaction