import re
import string
import logging
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

class LegalTextPreprocessor:
    """
    A unified preprocessing pipeline for legal texts. 
    Standardizes how we clean contracts, terms of service, and NDAs 
    before passing them to ML models.
    """
    
    def __init__(self, lowercase: bool = True, remove_punctuation: bool = False, remove_numbers: bool = False):
        """
        Configures the preprocessing steps.
        
        Args:
            lowercase (bool): Whether to convert text to lowercase.
            remove_punctuation (bool): Whether to strip all punctuation.
            remove_numbers (bool): Whether to remove numerical digits.
        """
        self.lowercase = lowercase
        self.remove_punctuation = remove_punctuation
        self.remove_numbers = remove_numbers
        
    def clean_text(self, text: str) -> str:
        """
        Applies configured cleaning steps to a single string of text.
        
        Args:
            text (str): The raw legal text.
            
        Returns:
            str: The cleaned legal text.
        """
        if not isinstance(text, str):
            logger.warning(f"Expected string for preprocessing, got {type(text)}. Returning empty string.")
            return ""
            
        # 1. Lowercasing
        if self.lowercase:
            text = text.lower()
            
        # 2. Removing numbers (often useless for semantic understanding, though sometimes important in contracts)
        if self.remove_numbers:
            text = re.sub(r'\d+', ' ', text)
            
        # 3. Removing punctuation
        if self.remove_punctuation:
            text = text.translate(str.maketrans('', '', string.punctuation))
            
        # 4. Standardizing whitespace (removing extra spaces, tabs, newlines)
        text = re.sub(r'\s+', ' ', text).strip()
        
        return text

    def batch_clean(self, texts: List[str]) -> List[str]:
        """
        Cleans a list of strings efficiently.
        """
        return [self.clean_text(t) for t in texts]
