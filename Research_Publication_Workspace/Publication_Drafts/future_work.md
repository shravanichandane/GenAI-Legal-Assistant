# Future Work

While our current evaluation establishes a strong baseline for dense retrieval in legal text, several limitations and opportunities for expansion remain.

## Limitations
- **Lack of Reranking:** The current pipeline relies solely on initial retrieval. Integrating a cross-encoder for reranking could further improve precision.
- **Single Language:** The models and datasets evaluated are restricted to English. Multilingual capabilities have not yet been explored.

## Roadmap
Our upcoming research phases will build upon these findings:
- **Week 5 (Retrieval-Augmented Generation - RAG):** Implementing a RAG pipeline to generate answers and summaries based on the retrieved legal clauses.
- **Week 6 (Fine-Tuning):** Exploring domain-specific fine-tuning of embedding models on proprietary legal data to further enhance retrieval performance.
- **Week 7 (Knowledge Graphs):** Integrating Knowledge Graphs to represent complex contractual relationships and obligations, enabling more structured and logical reasoning in retrieval tasks.
