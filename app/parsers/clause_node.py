### app/parsers/clause_node.py
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

class ClauseNode(BaseModel):
    """
    Universal representation of a semantic block in a legal document.
    This structured data replaces raw string manipulation and feeds directly
    into RAG, Legal-BERT classification, and Knowledge Graph extraction.
    """
    id: str = Field(description="Unique identifier for the node, e.g. 'sec_5_1'")
    type: str = Field(description="Type of node: 'document', 'article', 'section', 'clause', 'paragraph'")
    title: Optional[str] = Field(default=None, description="Extracted heading title, if any")
    section_number: Optional[str] = Field(default=None, description="The legal numbering, e.g. '5.1.2' or '(a)'")
    level: int = Field(description="Depth in the document tree. 0=Document, 1=Article/Section, etc.")
    parent_id: Optional[str] = Field(default=None, description="ID of the parent node to preserve hierarchy")
    text: str = Field(description="The normalized text content of this clause/paragraph")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Extracted features (word count, entities, etc.)")
    children: List['ClauseNode'] = Field(default_factory=list, description="Nested subclauses or paragraphs")

    def to_dict(self):
        """Recursively serialize the node and its children."""
        return {
            "id": self.id,
            "type": self.type,
            "title": self.title,
            "section_number": self.section_number,
            "level": self.level,
            "parent_id": self.parent_id,
            "text": self.text,
            "metadata": self.metadata,
            "children": [child.to_dict() for child in self.children]
        }

    def flatten(self) -> List['ClauseNode']:
        """Flatten the tree into a list of nodes (useful for ML pipelines that process linearly)."""
        nodes = [self]
        for child in self.children:
            nodes.extend(child.flatten())
        return nodes
