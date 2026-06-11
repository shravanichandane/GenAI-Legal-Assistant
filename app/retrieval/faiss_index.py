"""
EDUCATIONAL DOCUMENTATION
=========================
What this file does:
This file implements a wrapper around FAISS (Facebook AI Similarity Search). It manages the storage of dense vectors (embeddings) and performs extremely fast similarity searches.

Why it is needed:
When you have millions of legal documents, comparing a user's query embedding against every single document embedding one-by-one is incredibly slow. FAISS provides optimized, mathematically clever ways to search through millions of vectors in milliseconds.

How it connects to the overall architecture:
After `embedder.py` creates embeddings for the document corpus, they are added to `faiss_index.py`. During inference, `retriever.py` uses this class to fetch the top-K most relevant document IDs for a given query embedding.

Beginner-Friendly Explanation:
- What is FAISS? A library by Facebook for efficient similarity search of dense vectors.
- What is Cosine Similarity / L2 Distance? Vectors are points in space. L2 Distance measures the straight-line distance between two points. Inner Product (which correlates with Cosine Similarity for normalized vectors) measures the angle between them. Smaller angle = more similar meaning.
- Index: A data structure that stores the vectors in a way that makes searching them fast.

Interview Questions and Answers:
Q: What is the difference between IndexFlatL2 and IndexIVFFlat in FAISS?
A: IndexFlatL2 performs an exact nearest neighbor search by comparing the query against every vector (brute force). It's highly accurate but slow for huge datasets. IndexIVFFlat divides the vector space into clusters (cells) and only searches the clusters closest to the query, providing an Approximate Nearest Neighbor (ANN) search which is much faster but slightly less accurate.

Q: Why might we normalize embeddings before putting them into FAISS?
A: If we normalize vectors to unit length, the L2 distance rank mathematically becomes equivalent to Cosine Similarity rank. This is often preferred in NLP tasks.
"""

import logging
import numpy as np
from typing import List, Tuple, Dict, Any

try:
    import faiss
except ImportError:
    faiss = None
    logging.warning("faiss not installed. FaissIndex will fail if instantiated.")

logger = logging.getLogger(__name__)


class FaissIndex:
    """
    Vector database wrapper using FAISS for storing and searching dense embeddings.
    """

    def __init__(self, embedding_dimension: int, index_type: str = "Flat"):
        """
        Initialize the FAISS index.
        
        Args:
            embedding_dimension (int): The size of the embedding vectors (e.g., 384 for MiniLM).
            index_type (str): Type of FAISS index. 'Flat' uses exact L2 search.
        """
        self.embedding_dimension = embedding_dimension
        self.index_type = index_type
        
        if faiss is None:
            raise ImportError("Please install faiss-cpu or faiss-gpu to use FaissIndex.")
            
        logger.info(f"Initializing FAISS Index (Dim: {embedding_dimension}, Type: {index_type})")
        
        # IndexFlatL2 is exact search (brute-force) based on Euclidean distance.
        if index_type == "Flat":
            self.index = faiss.IndexFlatL2(embedding_dimension)
        else:
            raise NotImplementedError(f"Index type '{index_type}' not yet implemented in this module.")
            
        # Metadata storage mapping FAISS internal ID to actual document ID/content
        self.doc_metadata: Dict[int, Dict[str, Any]] = {}

    def add_vectors(self, embeddings: List[List[float]], metadata: List[Dict[str, Any]]):
        """
        Adds vectors and their metadata to the index.
        
        Args:
            embeddings: List of vectors to add.
            metadata: List of dictionaries containing document metadata (e.g., doc_id, text).
        """
        if len(embeddings) != len(metadata):
            raise ValueError("Number of embeddings must match number of metadata items.")
            
        vectors = np.array(embeddings).astype('float32')
        
        # The starting ID for these new vectors
        start_id = self.index.ntotal
        
        # Add to FAISS index
        self.index.add(vectors)
        
        # Store metadata
        for i, meta in enumerate(metadata):
            self.doc_metadata[start_id + i] = meta
            
        logger.info(f"Added {len(vectors)} vectors to FAISS index. Total vectors: {self.index.ntotal}")

    def search(self, query_embedding: List[float], top_k: int = 5) -> List[Tuple[float, Dict[str, Any]]]:
        """
        Searches the index for the most similar vectors to the query.
        
        Args:
            query_embedding: The dense vector representation of the query.
            top_k: Number of results to return.
            
        Returns:
            List of tuples: (distance_score, metadata_dict)
        """
        if self.index.ntotal == 0:
            logger.warning("Search called on an empty FAISS index.")
            return []
            
        query_vector = np.array([query_embedding]).astype('float32')
        
        # Perform search
        distances, indices = self.index.search(query_vector, top_k)
        
        results = []
        for j in range(len(indices[0])):
            idx = indices[0][j]
            if idx != -1 and idx in self.doc_metadata: # -1 means not enough results
                dist = distances[0][j]
                meta = self.doc_metadata[idx]
                results.append((float(dist), meta))
                
        return results
