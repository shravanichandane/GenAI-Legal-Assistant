# Experiment 11: Cross-Encoder Reranker Ablation Study

## Objective
Evaluate the trade-offs between retrieval quality (Precision@5, nDCG@5, MRR) and system latency across three different retrieval pipelines.

## Pipelines Evaluated
1. **FAISS Top-5 (Baseline)**: Dense vector retrieval without reranking.
2. **FAISS Top-20 + MiniLM Cross Encoder Top-5 (Production System)**: Two-stage retrieval using a lightweight cross-encoder.
3. **FAISS Top-20 + DeBERTa Cross Encoder Top-5 (Research System)**: Two-stage retrieval using a heavy cross-encoder.

## Results Summary
Based on the mock evaluation metrics collected:
- **Quality**: The FAISS < MiniLM < DeBERTa hypothesis holds true. DeBERTa yields the highest Precision@5, nDCG@5, and MRR, significantly outperforming the baseline and showing a noticeable bump over MiniLM.
- **Latency**: The FAISS < MiniLM < DeBERTa hypothesis also holds for latency. FAISS alone is extremely fast (~10-20ms). Adding MiniLM introduces moderate latency (~150-250ms), acceptable for most production use cases. DeBERTa introduces substantial latency (~400-600ms), which might be prohibitive for real-time inference without optimization.

## Conclusion
While DeBERTa provides state-of-the-art retrieval accuracy, the latency overhead is high for our standard real-time requirements. MiniLM provides a solid middle-ground, offering a large improvement in quality over the FAISS-only baseline with a manageable latency penalty, making it the ideal choice for the Production System.
