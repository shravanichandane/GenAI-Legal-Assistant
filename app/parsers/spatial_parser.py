import io
import logging
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

class SpatialParser:
    """
    Parses a PDF document into spatial clauses (paragraphs) using pdfplumber.
    Returns a list of dictionaries, each containing the clause text and its overall bounding box.
    """
    
    @classmethod
    def parse_pdf(cls, pdf_bytes: bytes, x_tolerance=3, y_tolerance=3, max_line_gap=10) -> List[Dict[str, Any]]:
        clauses = []
        try:
            import pdfplumber
        except ImportError:
            logger.error("pdfplumber is not installed.")
            return []
            
        try:
            with pdfplumber.open(io.BytesIO(pdf_bytes)) as pdf:
                for page_num, page in enumerate(pdf.pages, 1):
                    # extract_words returns [{"text": "abc", "x0": ..., "top": ..., "x1": ..., "bottom": ...}, ...]
                    words = page.extract_words(
                        x_tolerance=x_tolerance, 
                        y_tolerance=y_tolerance, 
                        keep_blank_chars=True
                    )
                    
                    if not words:
                        continue
                        
                    # Sort words by top (y-coordinate) then x0 (x-coordinate) to read left-to-right, top-to-bottom
                    words.sort(key=lambda w: (w['top'], w['x0']))
                    
                    blocks = []
                    current_block_words = []
                    
                    for word in words:
                        if not current_block_words:
                            current_block_words.append(word)
                            continue
                            
                        last_word = current_block_words[-1]
                        
                        # Calculate vertical gap
                        # If the word is on the same line, vertical_gap will be negative or very small.
                        # If it's on the next line within a paragraph, it's usually < max_line_gap.
                        # If it's a new paragraph, the gap is usually > max_line_gap.
                        vertical_gap = word['top'] - last_word['bottom']
                        
                        if vertical_gap < max_line_gap:
                            current_block_words.append(word)
                        else:
                            blocks.append(current_block_words)
                            current_block_words = [word]
                            
                    if current_block_words:
                        blocks.append(current_block_words)
                        
                    # Convert word blocks into clause dictionaries with overall bounding box
                    for block in blocks:
                        text = " ".join([w['text'] for w in block]).strip()
                        if not text:
                            continue
                            
                        # Overall bounding box is the min/max of all words in the block
                        x0 = min([w['x0'] for w in block])
                        top = min([w['top'] for w in block])
                        x1 = max([w['x1'] for w in block])
                        bottom = max([w['bottom'] for w in block])
                        
                        clauses.append({
                            "text": text,
                            "boundingBox": {
                                "x0": float(x0),
                                "top": float(top),
                                "x1": float(x1),
                                "bottom": float(bottom),
                                "pageNumber": page_num
                            }
                        })
        except Exception as e:
            logger.error(f"Failed to parse spatial PDF: {e}")
            
        return clauses
