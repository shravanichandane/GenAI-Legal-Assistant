from abc import ABC, abstractmethod
from typing import BinaryIO, Optional

class StorageProvider(ABC):
    """
    Abstract base class for storage providers.
    Defines the standard interface for saving, retrieving, and deleting files.
    """

    @abstractmethod
    async def upload_file(self, file_name: str, file_data: bytes, content_type: str = "application/octet-stream") -> str:
        """
        Uploads a file to the storage provider.
        
        Args:
            file_name (str): The unique name/path of the file to save.
            file_data (bytes): The binary content of the file.
            content_type (str): The MIME type of the file.
            
        Returns:
            str: The URI or path where the file is stored.
        """
        pass

    @abstractmethod
    async def download_file(self, file_name: str) -> Optional[bytes]:
        """
        Downloads a file from the storage provider.
        
        Args:
            file_name (str): The name/path of the file to retrieve.
            
        Returns:
            Optional[bytes]: The binary content of the file if found, else None.
        """
        pass

    @abstractmethod
    async def delete_file(self, file_name: str) -> bool:
        """
        Deletes a file from the storage provider.
        
        Args:
            file_name (str): The name/path of the file to delete.
            
        Returns:
            bool: True if deleted successfully, False otherwise.
        """
        pass
