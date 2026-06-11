"""
Module 1.4: Semantic Retrieval Foundation

This package contains the core components for building the vector search
and retrieval capabilities of the LegalSight AI Research Platform.
"""

from .embedder import Embedder
from .faiss_index import FaissIndex
from .retriever import Retriever
from .reranker import CrossEncoderReranker
from .metrics import RetrievalMetrics

__all__ = [
    "Embedder",
    "FaissIndex",
    "Retriever",
    "CrossEncoderReranker",
    "RetrievalMetrics"
]
