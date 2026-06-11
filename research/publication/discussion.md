# Discussion

The comparative evaluation highlights a classic trade-off between retrieval effectiveness and operational efficiency in legal contract intelligence.

## Effectiveness vs. Efficiency
Legal-BERT's superior ranking quality makes it the ideal choice for applications where precision and thorough understanding of legal text are paramount, such as high-stakes contract review. However, its larger model size and slower inference times present challenges for real-time or resource-constrained environments.

Conversely, MiniLM provides a highly efficient alternative. Its lower latency and smaller index footprint are beneficial for initial screening tasks or systems prioritizing speed and scalability, though this comes at the cost of reduced retrieval accuracy on complex legal queries.

## Implications for Legal AI
The superiority of FAISS over BM25 underscores the necessity of semantic search in the legal domain. Traditional keyword matching is often insufficient due to the nuanced and highly variable nature of legal drafting. Domain-specific dense retrieval models are essential for bridging the semantic gap in legal contract analysis.
