import os
import logging
from app.storage.base import StorageProvider
from app.storage.local_storage import LocalStorageProvider
from app.storage.r2_storage import R2StorageProvider

logger = logging.getLogger(__name__)

def get_storage_provider() -> StorageProvider:
    """
    Factory function to instantiate and return the appropriate StorageProvider
    based on the environment configuration.
    
    Uses 'STORAGE_BACKEND' environment variable.
    Defaults to 'local' if not specified.
    """
    backend = os.getenv("STORAGE_BACKEND", "local").lower()
    
    if backend == "r2":
        try:
            logger.info("Initializing R2StorageProvider")
            return R2StorageProvider()
        except ValueError as e:
            logger.error(f"Failed to initialize R2StorageProvider: {e}. Falling back to LocalStorageProvider.")
            return LocalStorageProvider()
    else:
        logger.info("Initializing LocalStorageProvider")
        return LocalStorageProvider()
