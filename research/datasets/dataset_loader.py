from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
import logging

# Configure logger for this module
logger = logging.getLogger(__name__)

class DatasetLoader(ABC):
    """
    Abstract base class defining the standard interface for all dataset loaders 
    in the LegalSight AI Research Platform.
    
    By enforcing this interface, we ensure that any new dataset added to the 
    platform can be swapped in without changing the downstream training code.
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize the dataset loader with optional configuration.
        
        Args:
            config (Dict): Configuration parameters (e.g., file paths, batch size).
        """
        self.config = config or {}
        self.data = None
        self.is_loaded = False
        self.is_preprocessed = False

    @abstractmethod
    def load(self) -> None:
        """
        Loads the raw dataset from disk or remote source into memory.
        Must be implemented by subclasses.
        """
        pass

    @abstractmethod
    def preprocess(self) -> None:
        """
        Applies necessary cleaning and transformations to the raw data.
        Must be implemented by subclasses.
        """
        pass

    @abstractmethod
    def train_split(self) -> Any:
        """
        Returns the training split of the dataset.
        
        Returns:
            Any: The training data (e.g., PyTorch Dataset, HuggingFace Dataset).
        """
        pass

    @abstractmethod
    def validation_split(self) -> Any:
        """
        Returns the validation split of the dataset.
        
        Returns:
            Any: The validation data.
        """
        pass

    @abstractmethod
    def test_split(self) -> Any:
        """
        Returns the test split of the dataset.
        
        Returns:
            Any: The testing data.
        """
        pass
