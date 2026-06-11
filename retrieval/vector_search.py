import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

class SemanticLegalSearch:
    def __init__(self, model_name="nlpaueb/legal-bert-base-uncased"):
        # We use a SentenceTransformer wrapper to pool BERT outputs into fixed-size embeddings
        try:
            self.model = SentenceTransformer(model_name)
        except Exception:
            # Fallback to a fast, generic embedding model if legal-bert isn't compatible with SentenceTransformers natively
            print(f"Warning: {model_name} might not be a pure SentenceTransformer. Falling back to all-MiniLM-L6-v2.")
            self.model = SentenceTransformer('all-MiniLM-L6-v2')
            
        # FAISS Index for inner product (cosine similarity if normalized)
        self.embedding_dimension = self.model.get_sentence_embedding_dimension()
        self.index = faiss.IndexFlatIP(self.embedding_dimension)
        
        self.clause_database = []

    def build_index(self, clauses: list[str]):
        """
        Encodes a list of legal clauses and adds them to the FAISS vector database.
        """
        self.clause_database = clauses
        embeddings = self.model.encode(clauses, convert_to_numpy=True)
        
        # Normalize vectors for cosine similarity search
        faiss.normalize_L2(embeddings)
        
        self.index.add(embeddings)
        print(f"Successfully indexed {self.index.ntotal} clauses.")

    def search(self, query: str, top_k: int = 3):
        """
        Retrieves the top_k most similar clauses to the query.
        """
        query_embedding = self.model.encode([query], convert_to_numpy=True)
        faiss.normalize_L2(query_embedding)
        
        distances, indices = self.index.search(query_embedding, top_k)
        
        results = []
        for dist, idx in zip(distances[0], indices[0]):
            results.append({
                "clause": self.clause_database[idx],
                "similarity_score": float(dist)
            })
            
        return results

if __name__ == "__main__":
    search_engine = SemanticLegalSearch()
    
    sample_clauses = [
        "The receiving party shall keep all information strictly confidential.",
        "Either party may terminate this Agreement for convenience upon 30 days notice.",
        "The Vendor's total aggregate liability shall not exceed the fees paid.",
        "This Agreement shall be governed by the laws of the State of Delaware."
    ]
    
    search_engine.build_index(sample_clauses)
    
    query = "How can we end this contract?"
    print(f"\nQuery: '{query}'")
    
    results = search_engine.search(query, top_k=2)
    for i, res in enumerate(results):
        print(f"{i+1}. Score: {res['similarity_score']:.4f} | Clause: {res['clause']}")
