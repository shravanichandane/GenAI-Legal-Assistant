# Results

Our experimental evidence from Week 3 and Week 4 reveals significant differences between the evaluated retrieval methods and architectures.

## Model Performance Comparison
- **Ranking Quality:** **Legal-BERT** clearly outperformed MiniLM in retrieving relevant legal clauses, demonstrating a deeper understanding of domain-specific language and context.
- **Efficiency:** **MiniLM** emerged as the winner in terms of latency and index size. Its lightweight architecture resulted in faster query processing and reduced memory overhead.

## Dense vs. Sparse Retrieval
- **FAISS vs. BM25:** Dense retrieval using FAISS consistently beat the BM25 baseline. FAISS was better able to match queries based on semantic meaning rather than exact keyword overlap, which is crucial for legal documents where terminology can vary.

## Visualizations
For detailed performance metrics, refer to our precision charts:
- ![Precision Chart](../visualizations/precision_chart.png)
- ![Recall Chart](../visualizations/recall_chart.png)
- ![Latency Comparison](../visualizations/latency_comparison.png)
