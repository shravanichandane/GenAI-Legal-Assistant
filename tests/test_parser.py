### tests/test_parser.py
import pytest
from app.parsers.document_parser import HierarchicalParser
from app.parsers.normalizer import DocumentNormalizer
from app.parsers.patterns import detect_structure

def test_normalizer_removes_broken_newlines():
    raw_pdf_text = "This is a sentence that was\nbroken by a PDF extractor.\n\nBut this is a new paragraph."
    blocks = DocumentNormalizer.normalize(raw_pdf_text)
    
    assert len(blocks) == 2
    assert blocks[0] == "This is a sentence that was broken by a PDF extractor."
    assert blocks[1] == "But this is a new paragraph."

def test_detect_structure_article():
    res = detect_structure("ARTICLE IV. CONFIDENTIALITY")
    assert res["type"] == "article"
    assert res["number"] == "IV"
    assert res["level"] == 1

def test_detect_structure_section():
    res = detect_structure("Section 5. Limitation of Liability")
    assert res["type"] == "section"
    assert res["number"] == "5"
    assert res["level"] == 1

def test_detect_structure_nested_numbering():
    res = detect_structure("5.1.2 Indemnity Exceptions")
    assert res["type"] == "clause"
    assert res["number"] == "5.1.2"
    assert res["level"] == 4  # 2 dots + 2 = 4

def test_detect_structure_letter_and_roman():
    res1 = detect_structure("(a) First exception")
    assert res1["type"] == "subclause_letter"
    assert res1["number"] == "a"
    assert res1["level"] == 4
    
    res2 = detect_structure("(iii) Third condition")
    assert res2["type"] == "subclause_roman"
    assert res2["number"] == "iii"
    assert res2["level"] == 5

def test_abbreviation_not_split():
    # If we used text.split('.'), this would break.
    # The normalizer uses \n\n, so it stays whole.
    text = "The company, Acme Inc., is based in the U.S.A. and operates globally."
    blocks = DocumentNormalizer.normalize(text)
    assert len(blocks) == 1
    assert "Acme Inc., is based in the U.S.A." in blocks[0]

def test_hierarchical_parser_integration():
    mock_contract = """
ARTICLE I

1.1 Definitions
The following terms have these meanings:

(a) "Agreement" means this document.

(b) "Party" means either client or vendor.

Section 2. Liability
In no event shall liability exceed $50,000.
"""
    
    root = HierarchicalParser.parse_document(mock_contract)
    
    assert root.type == "document"
    assert len(root.children) == 2 # ARTICLE I and Section 2
    
    article1 = root.children[0]
    assert article1.type == "article"
    assert article1.section_number == "I"
    assert len(article1.children) == 1 # 1.1 Definitions
    
    def_clause = article1.children[0]
    assert def_clause.section_number == "1.1"
    assert len(def_clause.children) == 2 # (a) + (b)
    assert "The following terms have these meanings" in def_clause.text
    
    assert def_clause.children[0].type == "subclause_letter"
    assert def_clause.children[0].section_number == "a"
    
    section2 = root.children[1]
    assert section2.type == "section"
    assert section2.section_number == "2"
    
    # Check metadata extraction
    assert section2.metadata["contains_money"] is True

def test_flatten_clauses():
    text = "Section 1\n\n1.1 Test"
    flat = HierarchicalParser.extract_flat_clauses(text)
    assert len(flat) == 2
    assert flat[0]["type"] == "section"
    assert flat[1]["type"] == "clause"
