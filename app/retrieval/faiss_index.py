"""
EDUCATIONAL DOCUMENTATION
=========================
What this file does:
This file implements a wrapper around FAISS (Facebook AI Similarity Search). It manages the storage of dense vectors (embeddings) and performs extremely fast similarity searches.

Why it is needed:
When you have millions of legal documents, comparing a user's query embedding against every single document embedding one-by-one is incredibly slow. FAISS provides optimized, mathematically clever ways to search through millions of vectors in milliseconds.

How it connects to the overall architecture:
After `embedder.py` creates embeddings for the document corpus, they are added to `faiss_index.py`. During inference, `retriever.py` uses this class to fetch the top-K most relevant document IDs for a given query embedding.
"""

import logging
import numpy as np
import os
import json
from typing import List, Tuple, Dict, Any

try:
    import faiss
except ImportError:
    faiss = None
    logging.warning("faiss not installed. FaissIndex will fail if instantiated.")

logger = logging.getLogger(__name__)

class FaissIndex:
    """
    Vector database wrapper using FAISS for storing and searching dense embeddings,
    with multi-tenant namespaces and lazy-loaded disk persistence.
    """

    def __init__(self, embedding_dimension: int, index_type: str = "Flat", base_path: str = "data/faiss"):
        self.embedding_dimension = embedding_dimension
        self.index_type = index_type
        self.base_path = base_path
        
        if faiss is None:
            raise ImportError("Please install faiss-cpu or faiss-gpu to use FaissIndex.")
            
        logger.info(f"Initializing FAISS Manager (Dim: {embedding_dimension}, Type: {index_type})")
        
        os.makedirs(self.base_path, exist_ok=True)
        
        # In-memory caches
        self.indices: Dict[str, faiss.Index] = {}
        self.doc_metadata: Dict[str, Dict[int, Dict[str, Any]]] = {}

    def _get_or_load_namespace(self, namespace: str) -> Tuple[faiss.Index, Dict[int, Dict[str, Any]]]:
        if namespace in self.indices:
            return self.indices[namespace], self.doc_metadata[namespace]
            
        # Lazy load from disk
        index_path = os.path.join(self.base_path, f"{namespace}.index")
        meta_path = os.path.join(self.base_path, f"{namespace}.json")
        
        if os.path.exists(index_path) and os.path.exists(meta_path):
            logger.info(f"Lazy loading FAISS index for namespace '{namespace}' from disk.")
            index = faiss.read_index(index_path)
            with open(meta_path, "r", encoding="utf-8") as f:
                meta_dict_str = json.load(f)
            # JSON keys are strings, convert back to int
            meta_dict = {int(k): v for k, v in meta_dict_str.items()}
            
            self.indices[namespace] = index
            self.doc_metadata[namespace] = meta_dict
        else:
            logger.info(f"Creating new FAISS index for namespace '{namespace}'.")
            if self.index_type == "Flat":
                index = faiss.IndexFlatL2(self.embedding_dimension)
            else:
                raise NotImplementedError(f"Index type '{self.index_type}' not yet implemented.")
            
            self.indices[namespace] = index
            self.doc_metadata[namespace] = {}
            
        return self.indices[namespace], self.doc_metadata[namespace]

    def save_local(self, namespace: str):
        """Persist a namespace index to disk."""
        if namespace not in self.indices:
            return
            
        index_path = os.path.join(self.base_path, f"{namespace}.index")
        meta_path = os.path.join(self.base_path, f"{namespace}.json")
        
        faiss.write_index(self.indices[namespace], index_path)
        with open(meta_path, "w", encoding="utf-8") as f:
            json.dump(self.doc_metadata[namespace], f)
        logger.info(f"Saved FAISS index for '{namespace}' to disk.")

    def add_vectors(self, namespace: str, embeddings: List[List[float]], metadata: List[Dict[str, Any]]):
        if len(embeddings) != len(metadata):
            raise ValueError("Number of embeddings must match number of metadata items.")
            
        if not embeddings:
            return

        index, meta_dict = self._get_or_load_namespace(namespace)
        
        vectors = np.array(embeddings).astype('float32')
        start_id = index.ntotal
        
        index.add(vectors)
        
        for i, meta in enumerate(metadata):
            meta_dict[start_id + i] = meta
            
        self.save_local(namespace)
        logger.info(f"Added {len(vectors)} vectors to namespace '{namespace}'. Total: {index.ntotal}")

    def search(self, namespace: str, query_embedding: List[float], top_k: int = 5, filter_metadata: Dict[str, Any] = None) -> List[Tuple[float, Dict[str, Any]]]:
        index, meta_dict = self._get_or_load_namespace(namespace)
        
        if index.ntotal == 0:
            logger.warning(f"Search called on an empty FAISS index for '{namespace}'.")
            return []
            
        query_vector = np.array([query_embedding]).astype('float32')
        
        # Over-fetch if filtering
        fetch_k = min(index.ntotal, max(top_k * 10, 50)) if filter_metadata else min(index.ntotal, top_k)
        
        distances, indices = index.search(query_vector, fetch_k)
        
        results = []
        for j in range(len(indices[0])):
            idx = indices[0][j]
            if idx != -1 and idx in meta_dict:
                dist = distances[0][j]
                meta = meta_dict[idx]
                
                # Apply metadata filter
                if filter_metadata:
                    match = True
                    for k, v in filter_metadata.items():
                        if meta.get(k) != v:
                            match = False
                            break
                    if not match:
                        continue
                        
                results.append((float(dist), meta))
                if len(results) >= top_k:
                    break
                    
        return results
