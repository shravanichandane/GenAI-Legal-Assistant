"""
EDUCATIONAL DOCUMENTATION
=========================
What this file does:
This file implements the `Retriever` class, which acts as the orchestrator for the retrieval phase. It connects the `Embedder` and the `FaissIndex` to provide a clean, single-entrypoint API for searching documents based on text queries.

Why it is needed:
Separation of concerns. The Embedder only cares about making vectors. The FAISS index only cares about storing math vectors. The rest of the application (like the UI or the LLM generation step) shouldn't need to manually pass vectors around. The Retriever hides this complexity.

How it connects to the overall architecture:
It is the main interface for Module 1.4. The Generation module (LLM) will call `retriever.retrieve(query)` to get context before writing an answer.

Beginner-Friendly Explanation:
Think of the Retriever as the Librarian. 
1. You give the Librarian a question: "What are the penalties for breach of contract?"
2. The Librarian uses a translator (Embedder) to turn your English question into 'math coordinates'.
3. The Librarian goes into the warehouse of filing cabinets (FAISS Index).
4. They find the folders closest to those coordinates.
5. They hand you back the actual documents, sorted by relevance.

Interview Questions and Answers:
Q: What happens if the FAISS index goes out of sync with the main SQL database of documents?
A: This is a classic distributed systems problem known as the "Dual Write" problem. Typically, this is solved by using an event-driven architecture (like Kafka) where document updates emit events that asynchronously update both the SQL DB and the Vector DB, or by using modern databases (like pgvector) that store both natively.

Q: How do you handle documents that are too long for the embedder's maximum context length?
A: We use Chunking. A long legal document is split into smaller paragraphs (chunks) of e.g., 500 words. Each chunk is embedded separately. During retrieval, we might find multiple chunks from the same document.
"""

import logging
import time
from typing import List, Dict, Any
from .embedder import Embedder
from .faiss_index import FaissIndex
from .metrics import RetrievalMetrics

logger = logging.getLogger(__name__)

class Retriever:
    """
    High-level Retrieval pipeline combining Embedding and FAISS search.
    """

    def __init__(self, embedder: Embedder, faiss_index: FaissIndex):
        """
        Initializes the Retriever.
        
        Args:
            embedder: An instance of the Embedder class.
            faiss_index: An instance of the FaissIndex class.
        """
        self.embedder = embedder
        self.faiss_index = faiss_index
        logger.info("Retriever pipeline initialized.")

    def add_documents(self, documents: List[str], metadata: List[Dict[str, Any]] = None):
        """
        Embeds texts and stores them in the index.
        
        Args:
            documents: List of text strings to index.
            metadata: Optional list of metadata dictionaries. If None, mock metadata is created.
        """
        logger.info(f"Adding {len(documents)} documents to the retriever...")
        if metadata is None:
            metadata = [{"text": doc, "id": i} for i, doc in enumerate(documents)]
        else:
            # Ensure text is in metadata for retrieval later
            for i, doc in enumerate(documents):
                if "text" not in metadata[i]:
                    metadata[i]["text"] = doc

        embeddings = self.embedder.embed_texts(documents)
        self.faiss_index.add_vectors(embeddings, metadata)
        logger.info("Documents successfully added to the index.")

    def retrieve(self, query: str, top_k: int = 5) -> Dict[str, Any]:
        """
        Retrieves the most relevant documents for a given query.
        
        Args:
            query: The search string.
            top_k: The number of results to return.
            
        Returns:
            A dictionary containing the retrieved documents and the latency.
        """
        start_time = time.time()
        
        # 1. Embed the query
        query_embedding = self.embedder.embed_texts(query)[0]
        
        # 2. Search FAISS
        results = self.faiss_index.search(query_embedding, top_k=top_k)
        
        latency = time.time() - start_time
        logger.info(f"Retrieved {len(results)} results in {latency:.4f} seconds.")
        
        # Format output
        formatted_results = []
        for dist, meta in results:
            formatted_results.append({
                "score": dist,
                "metadata": meta
            })
            
        return {
            "query": query,
            "results": formatted_results,
            "latency_seconds": latency
        }
