import os
import aiofiles
from typing import Optional
from pathlib import Path

from app.storage.base import StorageProvider

class LocalStorageProvider(StorageProvider):
    """
    Storage provider for local file system.
    Primarily used for development and testing.
    """

    def __init__(self, base_path: str = "./uploads"):
        self.base_path = Path(base_path)
        # Ensure the base directory exists
        self.base_path.mkdir(parents=True, exist_ok=True)

    async def upload_file(self, file_name: str, file_data: bytes, content_type: str = "application/octet-stream") -> str:
        file_path = self.base_path / file_name
        # Ensure parent directories exist if file_name includes paths
        file_path.parent.mkdir(parents=True, exist_ok=True)
        
        async with aiofiles.open(file_path, 'wb') as f:
            await f.write(file_data)
            
        return str(file_path.absolute())

    async def download_file(self, file_name: str) -> Optional[bytes]:
        file_path = self.base_path / file_name
        if not file_path.exists():
            return None
            
        async with aiofiles.open(file_path, 'rb') as f:
            return await f.read()

    async def delete_file(self, file_name: str) -> bool:
        file_path = self.base_path / file_name
        if file_path.exists():
            os.remove(file_path)
            return True
        return False
