"""
Reranker module for LegalSight AI.

This module implements the Cross-Encoder Reranker.

Educational Context: Bi-Encoders vs. Cross-Encoders
===================================================
In modern semantic search systems, retrieval typically happens in a two-stage pipeline:

1. Stage 1: Retrieval (Bi-Encoder)
   Bi-Encoders (like the ones used to create FAISS embeddings) process the query and the 
   document separately to create dense vector representations. The similarity is then computed 
   using a fast metric like cosine similarity or dot product. 
   - Pros: Extremely fast because document embeddings can be pre-computed and stored in a vector database.
   - Cons: Less accurate because the model never sees the query and document together; it can't 
     perform deep semantic comparisons between specific words in the query and the document.

2. Stage 2: Reranking (Cross-Encoder)
   Cross-Encoders process the query and the document *together* simultaneously in the transformer network.
   The input format is typically [CLS] Query [SEP] Document [SEP].
   - Pros: Highly accurate. The attention mechanism operates across both the query and document, 
     capturing deep interactions, nuances, and contextual relevance.
   - Cons: Computationally expensive. We cannot precompute embeddings because the output depends 
     on the joint query-document pair. Therefore, it's too slow to run on millions of documents.

Architecture of LegalSight AI:
- We use a Bi-Encoder (via FAISS) to quickly retrieve the top-N (e.g., 100) candidate documents.
- We then pass these top-N candidates to the Cross-Encoder (this module) to compute highly accurate 
  relevance scores and return the final top-K (e.g., 5) documents to the user or generation module.
"""

from typing import List, Dict, Any, Union
import numpy as np

try:
    from sentence_transformers import CrossEncoder
except ImportError:
    CrossEncoder = None
    print("Warning: sentence_transformers is not installed. CrossEncoderReranker will not work.")


class CrossEncoderReranker:
    """
    A cross-encoder based reranker to re-score and re-order candidate documents retrieved 
    by an initial retrieval phase (like FAISS).
    """

    # Supported model names
    MODELS = {
        "production": "cross-encoder/ms-marco-MiniLM-L-6-v2",
        "research": "cross-encoder/nli-deberta-v3-small"
    }

    def __init__(self, mode: str = "production", max_length: int = 512, device: str = None):
        """
        Initialize the CrossEncoderReranker.

        Args:
            mode (str): Mode for the cross-encoder model to use. 
                        Can be 'production' or 'research'.
            max_length (int): Maximum sequence length for the cross-encoder.
            device (str, optional): Device to run the model on ('cuda', 'cpu', 'mps'). 
                                    Defaults to None (auto-detects based on sentence_transformers).
        """
        if CrossEncoder is None:
            raise ImportError("Please install sentence-transformers to use the CrossEncoderReranker. "
                              "`pip install sentence-transformers`")
            
        if mode.lower() not in self.MODELS:
            raise ValueError(f"Invalid mode '{mode}'. Supported modes are: {list(self.MODELS.keys())}")
            
        actual_model_name = self.MODELS[mode.lower()]
        
        # Initialize the SentenceTransformers CrossEncoder
        self.model = CrossEncoder(
            actual_model_name,
            max_length=max_length,
            device=device
        )
        self.model_name = actual_model_name

    def rerank(self, query: str, documents: List[Union[str, Dict[str, Any]]], top_k: int = 5) -> List[Union[str, Dict[str, Any]]]:
        """
        Rerank a list of documents based on their cross-encoder score with the query.

        Args:
            query (str): The user query.
            documents (List[Union[str, Dict]]): A list of candidate documents. 
                Can be a list of strings (texts) or a list of dictionaries. 
                If dictionaries, they must contain a 'text', 'content', or 'metadata'->'text' key.
            top_k (int, optional): The number of top documents to return. Defaults to 5.

        Returns:
            List[Union[str, Dict]]: The top_k documents sorted by relevance score (descending).
                If the input was dictionaries, the returned dictionaries will have a new 'rerank_score' key.
        """
        if not documents:
            return []
            
        # Extract text from documents if they are dictionaries
        texts_to_score = []
        for doc in documents:
            if isinstance(doc, dict):
                text = doc.get("text") or doc.get("content")
                if text is None and "metadata" in doc and isinstance(doc["metadata"], dict):
                    text = doc["metadata"].get("text")
                if text is None:
                    raise ValueError("Document dictionary must contain a 'text', 'content', or 'metadata'->'text' key.")
                texts_to_score.append(text)
            elif isinstance(doc, str):
                texts_to_score.append(doc)
            else:
                raise TypeError("Documents must be strings or dictionaries containing text.")

        # Prepare pairs for the cross-encoder: [[query, doc1], [query, doc2], ...]
        pairs = [[query, text] for text in texts_to_score]
        
        # Calculate scores
        # The cross encoder predicts a relevance score for each pair
        scores = self.model.predict(pairs)
        
        # Create a list of indices sorted by score in descending order
        # np.argsort returns ascending order, so we reverse it with [::-1]
        sorted_indices = np.argsort(scores)[::-1]
        
        # Select the top_k indices
        top_k_indices = sorted_indices[:top_k]
        
        # Prepare the final reranked list
        reranked_docs = []
        for idx in top_k_indices:
            doc = documents[idx]
            score = float(scores[idx])
            
            if isinstance(doc, dict):
                # Create a copy to avoid mutating the original
                doc_copy = doc.copy()
                doc_copy["rerank_score"] = score
                reranked_docs.append(doc_copy)
            else:
                # If it's just a string, return dict with text and score
                reranked_docs.append({
                    "text": doc,
                    "rerank_score": score
                })
                
        return reranked_docs
