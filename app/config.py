"""
Application configuration management.

Centralises all environment variables, secrets, and runtime settings into a
single Pydantic ``Settings`` object so that nothing is scattered across files.

Usage
-----
    from app.config import settings

    print(settings.DATABASE_URL)
    print(settings.GOOGLE_API_KEY)
"""

import os
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv

# ---------------------------------------------------------------------------
# Load .env from project root (one level above `app/`)
# ---------------------------------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parent.parent
ENV_PATH = PROJECT_ROOT / "backend" / ".env"
load_dotenv(ENV_PATH)

# If a root-level .env exists, load that too (takes precedence)
ROOT_ENV = PROJECT_ROOT / ".env"
if ROOT_ENV.exists():
    load_dotenv(ROOT_ENV, override=True)


class Settings:
    """Centralised, type-safe configuration for the entire application.

    All values are read from environment variables at import time so they
    can be overridden in CI/CD, Docker, and Streamlit Cloud without touching
    code.
    """

    # ── Project Paths ──────────────────────────────────────────────────
    PROJECT_ROOT: Path = PROJECT_ROOT
    DATA_DIR: Path = PROJECT_ROOT / "data"
    MODELS_DIR: Path = PROJECT_ROOT / "models"
    LOGS_DIR: Path = PROJECT_ROOT / "logs"
    NOTEBOOKS_DIR: Path = PROJECT_ROOT / "notebooks"

    # ── Database ───────────────────────────────────────────────────────
    DATABASE_URL: Optional[str] = os.getenv("DATABASE_URL")

    @property
    def effective_database_url(self) -> str:
        """Return the database URL, falling back to local SQLite."""
        if self.DATABASE_URL:
            return self.DATABASE_URL
        db_path = self.PROJECT_ROOT / "backend" / "legal_docs.db"
        return f"sqlite:///{db_path.as_posix()}"

    # ── AI / LLM ──────────────────────────────────────────────────────
    GOOGLE_API_KEY: Optional[str] = os.getenv("GOOGLE_API_KEY")
    LLM_MODEL_NAME: str = os.getenv("LLM_MODEL_NAME", "gemini-1.5-flash")

    # ── Auth / JWT ────────────────────────────────────────────────────
    JWT_SECRET_KEY: str = os.getenv(
        "JWT_SECRET_KEY",
        "CHANGE_ME_IN_PRODUCTION_USE_A_LONG_RANDOM_STRING",
    )
    JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(
        os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "1440")
    )

    # ── Server ────────────────────────────────────────────────────────
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8000"))
    ALLOWED_ORIGIN: Optional[str] = os.getenv("ALLOWED_ORIGIN")

    # ── Logging ───────────────────────────────────────────────────────
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")

    def __repr__(self) -> str:
        return (
            f"<Settings db={'postgres' if self.DATABASE_URL else 'sqlite'} "
            f"llm={'enabled' if self.GOOGLE_API_KEY else 'disabled'}>"
        )


# Singleton instance — import this everywhere
settings = Settings()
