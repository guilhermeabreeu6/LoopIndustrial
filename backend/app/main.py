from fastapi import FastAPI

from app.database.db import engine
from app.database.base import Base

app = FastAPI(title="LoopIndustrial API")

Base.metadata.create_all(bind=engine)


@app.get("/")
def home():
    return {
        "message": "LoopIndustrial API is running"
    }