import re
import json
import spacy
from typing import Dict, List, Any

# NOTE: In a real environment, you must run `python -m spacy download en_core_web_sm` first.
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    print("Warning: SpaCy model 'en_core_web_sm' not found. Please install it.")
    nlp = None

class HierarchicalLegalParser:
    """
    Parses a raw legal contract into a structured JSON hierarchy 
    (Articles -> Sections -> Clauses) using Regex.
    """
    def __init__(self):
        # Regex to catch "ARTICLE I", "SECTION 1", "1.1", etc.
        self.section_pattern = re.compile(r"^(?i)(?:ARTICLE|SECTION)\s+[IVX\d]+\.?\s*(.*?)$")
        self.subsection_pattern = re.compile(r"^\d+\.\d+\.?\s*(.*?)$")
        self.clause_pattern = re.compile(r"^\([a-z]\)\s*(.*?)$")

    def parse_document(self, text: str) -> Dict[str, Any]:
        lines = text.split("\n")
        structured_doc = {"title": "Legal Contract", "sections": []}
        current_section = None
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            # Check for high-level Section or Article
            sec_match = self.section_pattern.match(line)
            if sec_match:
                if current_section:
                    structured_doc["sections"].append(current_section)
                current_section = {"heading": line, "content": "", "entities": {}}
                continue
                
            # If no section is found yet, just append to a generic intro section
            if not current_section:
                current_section = {"heading": "PREAMBLE", "content": "", "entities": {}}
                
            # Append text to the current section
            current_section["content"] += line + " "

        # Append the final section
        if current_section:
            structured_doc["sections"].append(current_section)
            
        return structured_doc

class LegalEntityExtractor:
    """
    Extracts Named Entities (Parties, Dates, Money) from parsed clauses using SpaCy.
    """
    def extract_entities(self, text: str) -> Dict[str, List[str]]:
        if not nlp:
            return {"ORG": [], "MONEY": [], "DATE": []}
            
        doc = nlp(text)
        entities = {"ORG": [], "MONEY": [], "DATE": []}
        
        for ent in doc.ents:
            if ent.label_ in entities:
                entities[ent.label_].append(ent.text)
                
        # Deduplicate lists
        return {k: list(set(v)) for k, v in entities.items()}

if __name__ == "__main__":
    sample_text = """
    ARTICLE I
    The Contractor (Acme Corp) shall indemnify the Client for damages.
    
    SECTION 1
    The total liability shall not exceed $50,000 USD. This agreement is effective January 1, 2026.
    """
    
    # 1. Parse the hierarchy
    parser = HierarchicalLegalParser()
    parsed_json = parser.parse_document(sample_text)
    
    # 2. Extract Entities per section
    extractor = LegalEntityExtractor()
    for section in parsed_json["sections"]:
        section["entities"] = extractor.extract_entities(section["content"])
        
    print(json.dumps(parsed_json, indent=2))
