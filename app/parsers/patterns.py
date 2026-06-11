### app/parsers/patterns.py
import re

# ---------------------------------------------------------------------------
# Legal Document Structural Patterns
# ---------------------------------------------------------------------------

# Matches: "ARTICLE IV", "Article 2", "ARTICLE IV. LIABILITY"
ARTICLE_PATTERN = re.compile(r"^article\s+([IVXLCDM]+|\d+)\.?\s*(.*)$", re.IGNORECASE)

# Matches: "SECTION 5", "Section 5. LIMITATION OF LIABILITY"
SECTION_PATTERN = re.compile(r"^section\s+(\d+)\.?\s*(.*)$", re.IGNORECASE)

# Matches: "5.", "5.1", "5.1.2" (with or without trailing titles)
NUMBERED_PATTERN = re.compile(r"^(\d+(?:\.\d+)*)\.?\s+(.*)$")

# Matches lettered subclauses: "(a)", "(B)", "a."
LETTER_PATTERN = re.compile(r"^\(([a-zA-Z])\)\s+(.*)$|^([a-zA-Z])\.\s+(.*)$")

# Matches roman numeral subclauses: "(i)", "(iv)"
ROMAN_PATTERN = re.compile(r"^\(([ivxlcdmIVXLCDM]+)\)\s+(.*)$")

# ---------------------------------------------------------------------------
# Metadata Detection Patterns
# ---------------------------------------------------------------------------

# Simple heuristic to detect if money is mentioned
MONEY_PATTERN = re.compile(r"\$|USD|EUR|GBP|£|€|dollars?|cents?", re.IGNORECASE)

# Simple heuristic to detect percentage
PERCENTAGE_PATTERN = re.compile(r"%|percent(?:age)?", re.IGNORECASE)

# Common legal parties
PARTY_PATTERN = re.compile(r"Contractor|Client|Company|Vendor|Supplier|Buyer|Seller|Party\s+[A-Z]", re.IGNORECASE)

# Simple heuristic for dates/durations
DATE_PATTERN = re.compile(r"days?|months?|years?|january|february|march|april|may|june|july|august|september|october|november|december", re.IGNORECASE)

def detect_structure(line: str) -> dict:
    """
    Evaluates a line of text against structural regex patterns.
    Returns a dictionary with the detected structure info or None.
    """
    stripped = line.strip()
    if not stripped:
        return None

    # Check Article
    match = ARTICLE_PATTERN.match(stripped)
    if match:
        return {"type": "article", "number": match.group(1), "title": match.group(2).strip(), "level": 1}

    # Check Section
    match = SECTION_PATTERN.match(stripped)
    if match:
        return {"type": "section", "number": match.group(1), "title": match.group(2).strip(), "level": 1}

    # Check Numbered (e.g., 5.1.2)
    match = NUMBERED_PATTERN.match(stripped)
    if match:
        num = match.group(1)
        # Determine depth based on the number of dots
        # e.g., "5" -> level 2, "5.1" -> level 3, "5.1.1" -> level 4
        level = num.count('.') + 2 
        return {"type": "clause", "number": num, "title": match.group(2).strip(), "level": level}

    # Check Roman Numerals first because (i) matches both letter and roman!
    match = ROMAN_PATTERN.match(stripped)
    if match:
        return {"type": "subclause_roman", "number": match.group(1), "title": match.group(2).strip(), "level": 5}

    # Check Letters
    match = LETTER_PATTERN.match(stripped)
    if match:
        num = match.group(1) or match.group(3)
        title = match.group(2) or match.group(4)
        return {"type": "subclause_letter", "number": num, "title": title.strip(), "level": 4}

    return None
