### app/parsers/hierarchy_builder.py
import uuid
from typing import List, Optional
from .clause_node import ClauseNode
from .patterns import detect_structure, MONEY_PATTERN, DATE_PATTERN, PARTY_PATTERN

class HierarchyBuilder:
    """
    Stage 3 of the NLP Pipeline: Builds a tree structure from sequential text blocks.
    """

    def __init__(self):
        # We start with a root document node
        self.root = ClauseNode(
            id=f"doc_{uuid.uuid4().hex[:8]}",
            type="document",
            level=0,
            text="Document Root"
        )
        # Keeps track of the last node seen at each level to attach children correctly
        self.node_stack: List[ClauseNode] = [self.root]

    def build(self, blocks: List[str]) -> ClauseNode:
        """Processes sequential text blocks into a hierarchical tree."""
        for block in blocks:
            struct_info = detect_structure(block)
            
            if struct_info:
                # We found a heading or numbered clause
                level = struct_info["level"]
                node_type = struct_info["type"]
                number = struct_info["number"]
                title = struct_info["title"]
                
                # We also want the text of the block. For a pure heading, it might be empty
                # But typically it's "1. Indemnity The contractor will..."
                # If title is long, the title IS the text.
                
                node = self._create_node(
                    type_str=node_type,
                    level=level,
                    text=block,
                    section_number=number,
                    title=title if len(title) < 100 else None
                )
                self._attach_node(node, level)
            else:
                # It's a standard paragraph belonging to the current scope
                # It belongs to whatever the last active node is, but it's a child paragraph
                current_parent = self.node_stack[-1]
                
                node = self._create_node(
                    type_str="paragraph",
                    level=current_parent.level + 1,
                    text=block
                )
                current_parent.children.append(node)

        return self.root

    def _create_node(self, type_str: str, level: int, text: str, section_number: Optional[str] = None, title: Optional[str] = None) -> ClauseNode:
        # Extract metadata
        metadata = {
            "word_count": len(text.split()),
            "contains_money": bool(MONEY_PATTERN.search(text)),
            "contains_dates": bool(DATE_PATTERN.search(text)),
            "contains_party_names": bool(PARTY_PATTERN.search(text))
        }
        
        return ClauseNode(
            id=f"node_{uuid.uuid4().hex[:8]}",
            type=type_str,
            level=level,
            text=text,
            section_number=section_number,
            title=title,
            metadata=metadata
        )

    def _attach_node(self, node: ClauseNode, level: int):
        """
        Attaches the new node to the correct parent based on its depth level.
        """
        # Pop nodes from the stack until we find a parent with a level < current node's level
        while len(self.node_stack) > 1 and self.node_stack[-1].level >= level:
            self.node_stack.pop()
            
        parent = self.node_stack[-1]
        node.parent_id = parent.id
        parent.children.append(node)
        
        # Add the new node to the stack so future children can attach to it
        self.node_stack.append(node)
