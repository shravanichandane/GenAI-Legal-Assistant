import time
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse

# Setup structured python logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
)
logger = logging.getLogger("legalsight_api")

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup actions
    logger.info("Starting up LegalSight AI API...")
    # Setup DB connections, external API clients, etc., here.
    from app.db.database import engine, Base
    from app.db import models
    import sqlalchemy.exc
    from sqlalchemy import text
    try:
        Base.metadata.create_all(bind=engine)
    except sqlalchemy.exc.ProgrammingError as e:
        if "DatatypeMismatch" in str(e):
            logger.warning("Schema mismatch detected (likely from an old deploy). Wiping database using CASCADE...")
            with engine.begin() as conn:
                conn.execute(text("DROP SCHEMA public CASCADE;"))
                conn.execute(text("CREATE SCHEMA public;"))
            Base.metadata.create_all(bind=engine)
        else:
            raise e
    yield
    # Shutdown actions
    logger.info("Shutting down LegalSight AI API...")
    # Close connections here.

app = FastAPI(
    title="LegalSight AI API",
    description="Backend API for the GenAI Legal Assistant.",
    version="1.0.0",
    lifespan=lifespan
)

# Middleware configuration
app.add_middleware(
    TrustedHostMiddleware, 
    allowed_hosts=["*"] # In production, restrict this to specific domains, e.g., ["api.legalsight.com", "localhost"]
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, restrict this to frontend origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Optional: Time elapsed middleware for observability
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    logger.info(f"{request.method} {request.url.path} - completed in {process_time:.4f}s")
    return response


# --- Observability Endpoints ---

@app.get("/health", tags=["Observability"])
async def health_check():
    """Liveness probe to check if the application is running."""
    return {"status": "ok", "service": "legalsight-api"}

@app.get("/ready", tags=["Observability"])
async def readiness_check():
    """
    Readiness probe to check if the application is ready to receive traffic.
    In a real app, this should check DB connectivity, Redis, etc.
    """
    # Example: check_db_connection()
    return {"status": "ready"}

@app.get("/metrics", tags=["Observability"])
async def metrics():
    """
    Endpoint for scraping metrics (e.g., Prometheus).
    Normally integrated with a library like prometheus_client.
    """
    return JSONResponse(
        content={"message": "Metrics endpoint placeholder. Integrate prometheus_client for real metrics."},
        status_code=200
    )


from app.api.routers import contracts, playbooks, research
from app.auth.router import router as auth_router

app.include_router(auth_router, prefix="/api/v1/auth", tags=["Auth"])
app.include_router(contracts.router, prefix="/api/v1/contracts", tags=["Contracts"])
app.include_router(playbooks.router, prefix="/api/v1/playbooks", tags=["Playbooks"])
app.include_router(research.router, prefix="/api/v1/research", tags=["Research"])

@app.get("/", tags=["Root"])
async def root():
    return {"message": "Welcome to the LegalSight AI API"}

if __name__ == "__main__":
    import uvicorn
    # Typically run via `uvicorn main:app --host 0.0.0.0 --port 8000`
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
