import os
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from backend.db.init_db import seed_database
from backend.api.auth import router as auth_router
from backend.api.districts import router as districts_router
from backend.api.locations import router as locations_router
from backend.api.forecast import router as forecast_router
from backend.api.risk import router as risk_router
from backend.api.gis import router as gis_router
from backend.api.system import router as system_router
from backend.api.hazards import router as hazards_router
from backend.api.exposure import router as exposure_router
from backend.api.priority import router as priority_router
from backend.api.strategies import router as strategies_router
from backend.api.optimization import router as optimization_router
from backend.api.qubo import qubo_router
from backend.api.qaoa import qaoa_router
from backend.api.rag import router as rag_router
from backend.api.explanation import router as explanation_router
from backend.api.decision import router as decision_router
from backend.api.governance import router as governance_router

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("api_main")

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: ensure database tables & seed data are ready
    logger.info("Initializing database on startup...")
    try:
        seed_database()
    except Exception as e:
        logger.error(f"Error seeding database: {e}")
    yield
    logger.info("Shutting down Climate Risk API...")

app = FastAPI(
    title="Quantum Multi-Agent Climate Risk Intelligence API",
    description="Operational Backend for Phase O — Enterprise Decision Intelligence API & Multi-Agent Orchestration",
    version="3.0.0",
    lifespan=lifespan
)

# CORS configuration for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register Routers
app.include_router(auth_router, prefix="/auth")
app.include_router(districts_router, prefix="/districts")
app.include_router(locations_router, prefix="/locations")
app.include_router(forecast_router, prefix="/forecast")
app.include_router(risk_router, prefix="/risk")
app.include_router(gis_router, prefix="/gis")
app.include_router(system_router, prefix="/system")
app.include_router(hazards_router)
app.include_router(exposure_router)
app.include_router(priority_router)
app.include_router(strategies_router)
app.include_router(optimization_router)
app.include_router(qubo_router, prefix="/api/v1/qubo")
app.include_router(qubo_router, prefix="/qubo")
app.include_router(qaoa_router, prefix="/api/v1/qaoa")
app.include_router(qaoa_router, prefix="/qaoa")
app.include_router(rag_router)
app.include_router(explanation_router)
app.include_router(decision_router)
app.include_router(governance_router)






@app.get("/")
async def root():
    return {
        "title": "Quantum Multi-Agent Climate Risk Decision Support System API",
        "review_phase": "Review II",
        "status": "online",
        "docs_url": "/docs"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)
