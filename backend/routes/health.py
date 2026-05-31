### backend/routes/health.py

from fastapi import APIRouter
import os
from dotenv import load_dotenv

load_dotenv()

router = APIRouter()

@router.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "Legal Document Review Assistant",
        "version": "1.0.0"
    }