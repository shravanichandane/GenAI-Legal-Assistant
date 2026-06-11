"""
EDUCATIONAL DOCUMENTATION
=========================
What this file does:
This file defines the `Embedder` class, which is responsible for converting raw text into dense numerical vectors (embeddings). It supports multiple pre-trained models.

Why it is needed:
Computers cannot understand raw text natively. By converting text into high-dimensional vectors, we capture semantic meaning. Texts with similar meanings will have vectors that are closer together in the vector space, enabling similarity search.

How it connects to the overall architecture:
The Embedder is the first step in the retrieval pipeline. When a user asks a question, the Embedder converts the query into a vector. Similarly, all legal documents in our corpus must first pass through this Embedder before being stored in the Vector Database (FAISS).

Beginner-Friendly Explanation:
- What is an Embedding? Imagine a map where words with similar meanings are placed close to each other. "King" and "Queen" would be near each other, while "Apple" would be far away. An embedding is a list of numbers representing coordinates on a highly complex map (often 384 or 768 dimensions).
- Phase 1 (all-MiniLM-L6-v2): A small, fast, general-purpose model. Great for getting started.
- Phase 2 (legal-bert-base-uncased): A model trained specifically on legal text. It understands legal jargon much better than a general model.

Interview Questions and Answers:
Q: Why do we use dense embeddings instead of just keyword search (like BM25)?
A: Keyword search fails when different words are used to mean the same thing (synonyms). Dense embeddings capture semantic intent, allowing the system to match "car accident" with "vehicular collision".

Q: What is the difference between Sentence Transformers and standard BERT?
A: Standard BERT produces word-level embeddings and requires significant pooling efforts to represent a whole sentence. Sentence Transformers are fine-tuned using Siamese networks to output semantically meaningful sentence-level embeddings directly.
"""

import logging
from typing import List, Union
import time

try:
    from sentence_transformers import SentenceTransformer
except ImportError:
    SentenceTransformer = None
    logging.warning("sentence-transformers not installed. Embedder will fail if instantiated without a mock.")

logger = logging.getLogger(__name__)

class Embedder:
    """
    Text embedding module supporting multiple models (Phase 1 and Phase 2).
    """

    def __init__(self, model_name: str = "sentence-transformers/all-MiniLM-L6-v2", device: str = "cpu"):
        """
        Initializes the Embedder.
        
        Args:
            model_name (str): The HuggingFace model ID to load. 
                              Default is Phase 1 model: 'sentence-transformers/all-MiniLM-L6-v2'.
                              Phase 2 model is: 'nlpaueb/legal-bert-base-uncased'.
            device (str): Device to run the model on ('cpu' or 'cuda').
        """
        self.model_name = model_name
        self.device = device
        
        logger.info(f"Initializing Embedder with model: {self.model_name} on {self.device}")
        if SentenceTransformer is None:
            raise ImportError("Please install sentence-transformers to use the Embedder.")
            
        self.model = SentenceTransformer(self.model_name, device=self.device)
        logger.info("Embedder initialized successfully.")

    def embed_texts(self, texts: Union[str, List[str]]) -> List[List[float]]:
        """
        Converts text(s) into dense vectors.
        
        Args:
            texts: A single string or a list of strings to encode.
            
        Returns:
            A list of vector embeddings (lists of floats).
        """
        start_time = time.time()
        
        if isinstance(texts, str):
            texts = [texts]
            
        logger.debug(f"Generating embeddings for {len(texts)} texts...")
        
        # encode returns a numpy array, we convert to list of lists for generic typing
        embeddings = self.model.encode(texts, convert_to_numpy=True)
        
        latency = time.time() - start_time
        logger.debug(f"Embedding generation completed in {latency:.4f} seconds.")
        
        return embeddings.tolist()
