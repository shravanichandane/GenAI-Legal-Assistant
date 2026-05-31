# Supports PostgreSQL (production) and SQLite (local dev fallback)
### backend/database.py

import os
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# Load environment variables from backend/.env
load_dotenv()

# Read DATABASE_URL from environment; fall back to SQLite for local dev
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    BASE_DIR = Path(__file__).resolve().parent
    DB_PATH = BASE_DIR / "legal_docs.db"
    DATABASE_URL = f"sqlite:///{DB_PATH.as_posix()}"

# Create the engine with appropriate connect_args
if DATABASE_URL.startswith("sqlite"):
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
else:
    engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_tables():
    Base.metadata.create_all(bind=engine, checkfirst=True)
