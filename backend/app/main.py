from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database.db import engine
from app.database.base import Base
from app.routes.company_routes import router as company_router
from app.routes.residue_routes import router as residue_router
from app.routes.interest_routes import router as interest_router
from app.routes.transaction_routes import router as transaction_router
from app.routes.dashboard_routes import router as dashboard_router
from app.routes.impact_routes import router as impact_router

app = FastAPI(title="LoopIndustrial API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",
        "http://localhost:5500",
        "http://127.0.0.1:3000",
        "http://localhost:3000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

app.include_router(company_router)
app.include_router(residue_router)
app.include_router(interest_router)
app.include_router(transaction_router)
app.include_router(dashboard_router)
app.include_router(impact_router)


@app.get("/")
def home():
    return {
        "message": "LoopIndustrial API is running"
    }