### app/parsers/document_parser.py
from typing import List, Dict, Any
from .normalizer import DocumentNormalizer
from .hierarchy_builder import HierarchyBuilder
from .clause_node import ClauseNode

class HierarchicalParser:
    """
    The orchestrator for the NLP Hierarchical Parser pipeline.
    Stages:
    1. Normalization
    2. Structural Detection & Hierarchy Building
    3. Output Generation (JSON/Objects)
    """

    @classmethod
    def parse_document(cls, raw_text: str) -> ClauseNode:
        """
        Parses raw document text and returns the root node of the document tree.
        """
        # Stage 1: Normalize
        clean_blocks = DocumentNormalizer.normalize(raw_text)
        
        # Stage 2 & 3: Detect Structure & Build Hierarchy
        builder = HierarchyBuilder()
        root_node = builder.build(clean_blocks)
        
        return root_node

    @classmethod
    def parse_to_dict(cls, raw_text: str) -> dict:
        """
        Parses a document and returns it as a structured dictionary.
        """
        root_node = cls.parse_document(raw_text)
        return root_node.to_dict()

    @classmethod
    def extract_flat_clauses(cls, raw_text: str) -> List[Dict[str, Any]]:
        """
        Parses a document and flattens the tree into a list of clauses for 
        downstream tasks that expect linear input (like LLM chunk processing).
        Excludes the root node itself.
        """
        root_node = cls.parse_document(raw_text)
        flat_nodes = root_node.flatten()
        
        # Return everything except the root node
        return [node.to_dict() for node in flat_nodes if node.level > 0]
