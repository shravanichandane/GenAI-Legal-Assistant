# Week 4 Experiment Findings: Embedding Dimension & Top-K Sensitivity Analysis

## 1. Embedding Dimension Analysis (MiniLM vs Legal-BERT)
We compared two embedding models: MiniLM (384 dimensions) and Legal-BERT (768 dimensions) to evaluate the tradeoff between retrieval quality and system efficiency.

**Key Findings:**
- **Retrieval Quality:** Legal-BERT significantly outperforms MiniLM across all quality metrics (Precision@5: 0.76 vs 0.65; Recall@5: 0.82 vs 0.70; MRR: 0.79 vs 0.68; nDCG@5: 0.81 vs 0.72). Its domain-specific pretraining and larger dimensionality allow it to capture nuanced legal semantics more effectively.
- **Efficiency and Resource Cost:** The performance gain of Legal-BERT comes at a noticeable computational cost. It exhibits over 2x the retrieval latency (28.1ms vs 12.4ms), requires more than double the memory (256.0MB vs 120.5MB), and doubles the index size (90.4MB vs 45.2MB).
- **Conclusion:** For applications where high accuracy on complex legal language is critical, Legal-BERT is the preferred choice, provided the infrastructure can support the higher memory and latency footprint. MiniLM remains a viable lightweight alternative for resource-constrained environments.

## 2. Top-K Sensitivity Analysis
We evaluated the system's performance across various Top-K retrieval sizes (K = 1, 3, 5, 10, 20).

**Key Findings:**
- **Precision vs Recall Tradeoff:** As K increases, Recall@K improves dramatically (from 0.30 at K=1 to 0.92 at K=20), while Precision@K degrades (from 0.85 at K=1 to 0.45 at K=20). This is expected, as retrieving more documents increases the chance of finding all relevant ones, but also introduces more noise.
- **Latency Impact:** Retrieval latency scales sub-linearly with K, increasing from 20.1ms at K=1 to 35.2ms at K=20. The latency cost of retrieving more documents is relatively modest, suggesting the vector database handles larger K values efficiently.
- **Optimal K Value:** K=5 appears to offer a solid balance (Precision: 0.72, Recall: 0.70), but if downstream tasks (like a generative LLM) can handle larger contexts and filter out noise, pushing K to 10 might be optimal to maximize recall (0.85).

## Overall Conclusion
The experiments demonstrate that moving to a domain-specific, higher-dimension embedding (Legal-BERT) significantly boosts retrieval quality for legal texts, albeit with increased resource demands. Furthermore, tuning the Top-K parameter allows us to balance the precision-recall tradeoff according to the downstream application's context window and noise tolerance, with K=5 to K=10 emerging as a sweet spot.
