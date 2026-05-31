### backend/main.py

import sys
from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
# Ensure package imports work whether run as module or script
CURRENT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = CURRENT_DIR.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from backend.database import create_tables
from backend.routes.health import router as health_router
from backend.routes.upload import router as upload_router
from backend.routes.analyze import router as analyze_router
from backend.routes.search import router as search_router
from backend.routes.auth import router as auth_router

# Create FastAPI app
load_dotenv()

app = FastAPI(
    title="Legal Document Review Assistant API",
    description="AI-powered legal document analysis and review system",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8501"],  # Restricted to Streamlit frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(health_router, tags=["Health"])
app.include_router(auth_router, prefix="/api/auth", tags=["Authentication"])
app.include_router(upload_router, prefix="/api", tags=["Upload"])
app.include_router(analyze_router, prefix="/api", tags=["Analysis"])
app.include_router(search_router, prefix="/api", tags=["Search"])

# Create database tables on startup
@app.on_event("startup")
async def startup_event():
    create_tables()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=False)
