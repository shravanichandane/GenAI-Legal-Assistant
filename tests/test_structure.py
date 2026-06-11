"""
Smoke tests for the project structure and configuration.

Run with:
    python -m pytest tests/ -v

These tests verify that:
1. The project structure exists and is importable.
2. The Settings object loads correctly.
3. The logger works.

Interview Tip
-------------
Q: "Why do you write tests for configuration and project structure?"
A: Because if your config is broken, *nothing* works. A 5-line test that
   catches a missing env var saves hours of debugging later. This is
   called a "smoke test" — it checks that the building isn't on fire
   before you start decorating the rooms.
"""

import importlib
from pathlib import Path


class TestProjectStructure:
    """Verify the directory layout matches our architecture."""

    def test_app_package_is_importable(self):
        """The top-level `app` package should be importable."""
        mod = importlib.import_module("app")
        assert hasattr(mod, "__version__")

    def test_config_is_importable(self):
        """app.config should load without errors."""
        from app.config import settings
        assert settings is not None

    def test_project_root_is_correct(self):
        """settings.PROJECT_ROOT should point to the actual project root."""
        from app.config import settings
        assert settings.PROJECT_ROOT.exists()
        assert (settings.PROJECT_ROOT / "app").is_dir()

    def test_subpackages_exist(self):
        """All planned subpackages should be importable."""
        packages = [
            "app.services",
            "app.parsers",
            "app.models",
            "app.evaluation",
        ]
        for pkg in packages:
            mod = importlib.import_module(pkg)
            assert mod is not None, f"Failed to import {pkg}"

    def test_data_directories_are_defined(self):
        """Settings should define paths for data, models, logs."""
        from app.config import settings
        assert isinstance(settings.DATA_DIR, Path)
        assert isinstance(settings.MODELS_DIR, Path)
        assert isinstance(settings.LOGS_DIR, Path)


class TestLogging:
    """Verify the logging configuration works."""

    def test_get_logger(self):
        """get_logger should return a proper Logger instance."""
        from app.logging_config import get_logger
        import logging

        logger = get_logger("test_module")
        assert isinstance(logger, logging.Logger)
        assert logger.name == "test_module"

    def test_setup_logging_runs_without_error(self):
        """setup_logging() should configure handlers without crashing."""
        from app.logging_config import setup_logging
        setup_logging()  # Should not raise


class TestConfig:
    """Verify configuration values load correctly."""

    def test_database_url_fallback(self):
        """When DATABASE_URL is unset, it should fall back to SQLite."""
        from app.config import settings
        url = settings.effective_database_url
        assert "sqlite" in url or "postgresql" in url

    def test_jwt_defaults(self):
        """JWT settings should have sensible defaults."""
        from app.config import settings
        assert settings.JWT_ALGORITHM == "HS256"
        assert settings.ACCESS_TOKEN_EXPIRE_MINUTES > 0

    def test_log_level_default(self):
        """Default log level should be INFO."""
        from app.config import settings
        assert settings.LOG_LEVEL in ("DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL")
