import torch
from torch.utils.data import Dataset
from typing import Dict, List

class LegalDataset(Dataset):
    """
    PyTorch Dataset tailored for CUAD-style legal document processing.
    
    Designed to be compatible with HuggingFace's Trainer, expecting
    tokenized encodings (input_ids, attention_mask) and corresponding labels.
    """
    def __init__(self, encodings: Dict[str, List[List[int]]], labels: List[int]):
        """
        Initializes the dataset with tokenized encodings and labels.
        
        Args:
            encodings (Dict[str, List[List[int]]]): A dictionary of encoded text 
                (e.g., 'input_ids' and 'attention_mask').
            labels (List[int]): Ground truth labels for classification.
        """
        self.encodings = encodings
        self.labels = labels

    def __getitem__(self, idx: int) -> Dict[str, torch.Tensor]:
        """
        Fetches the tensor representations for a given example.
        
        Args:
            idx (int): Index of the dataset item to retrieve.
            
        Returns:
            Dict[str, torch.Tensor]: Dictionary mapping input keys to their respective tensors.
        """
        # Convert list of integers to PyTorch tensors
        item = {key: torch.tensor(val[idx]) for key, val in self.encodings.items()}
        item['labels'] = torch.tensor(self.labels[idx], dtype=torch.long)
        return item

    def __len__(self) -> int:
        """Returns the total size of the dataset."""
        return len(self.labels)
