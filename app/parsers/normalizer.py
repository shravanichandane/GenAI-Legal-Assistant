### app/parsers/normalizer.py
import re
from typing import List

class DocumentNormalizer:
    """
    Stage 1 of the NLP Pipeline: Cleans and normalizes noisy OCR/PDF text
    before structural detection occurs.
    """
    
    @staticmethod
    def normalize(text: str) -> List[str]:
        """
        Cleans the document and splits it into logical line-blocks.
        """
        if not text:
            return []
            
        # 1. Remove carriage returns
        text = text.replace('\r', '')
        
        # 2. Fix broken paragraphs: PDF extraction often inserts arbitrary 
        # newlines in the middle of sentences.
        # If a line ends with a lowercase letter or comma, and the next line 
        # starts with a lowercase letter, they are likely the same sentence.
        # For an MVP, we split by double newlines (\n\n) to get blocks.
        
        # Replace 3+ newlines with exactly 2
        text = re.sub(r'\n{3,}', '\n\n', text)
        
        # Split by blocks (paragraphs)
        blocks = text.split('\n\n')
        
        cleaned_blocks = []
        for block in blocks:
            # Replace single newlines within a block with spaces
            block = block.replace('\n', ' ')
            
            # Remove duplicate spaces
            block = re.sub(r'\s{2,}', ' ', block)
            
            block = block.strip()
            if block:
                cleaned_blocks.append(block)
                
        return cleaned_blocks
