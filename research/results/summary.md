# Week 3 Execution Summary

This document summarizes the outcomes of the experiments evaluating different retrieval engines and embedding models for LegalSight AI.

## Hypotheses and Conclusions

### H1: Dense Retrieval (FAISS) outperforms Keyword-based Retrieval (BM25)
**Status:** Supported
**Observation:** In `exp_06_retrieval_vs_keyword.py`, FAISS demonstrated superior performance across all relevance metrics. It achieved a Precision@5 of 0.82 and Recall@5 of 0.78, compared to BM25's Precision@5 of 0.65 and Recall@5 of 0.60. Furthermore, FAISS yielded a higher Mean Reciprocal Rank (MRR) of 0.85 versus 0.68 for BM25, clearly indicating that dense representations capture semantic meaning better than exact keyword matching for legal texts.

### H2: Domain-specific Embeddings (Legal-BERT) provide higher accuracy than general Embeddings (MiniLM)
**Status:** Supported
**Observation:** Based on `exp_07_embedding_ablation.py`, Legal-BERT substantially outperformed MiniLM on precision-oriented metrics. Legal-BERT achieved a Precision@5 of 0.89 and an nDCG@5 of 0.92, whereas MiniLM reached a Precision@5 of 0.82 and nDCG@5 of 0.88. The domain-specific pretraining of Legal-BERT enables it to understand the nuance and context of legal clauses more effectively, directly translating to higher retrieval quality.

### H3: Lightweight Models (MiniLM) offer superior efficiency and lower latency
**Status:** Supported
**Observation:** While MiniLM sacrifices some accuracy compared to Legal-BERT, it significantly excels in operational efficiency. As tracked in our latency results, MiniLM required only 45.0ms of latency per query and consumed 250.0 MB of memory. In contrast, the heavier Legal-BERT model required 120.0ms latency and 800.0 MB of memory. This validates MiniLM as a highly efficient alternative for environments where computational resources or latency are constrained.

## Final Thoughts
The experiments validate that leveraging a Dense Retrieval engine powered by a domain-specific model like Legal-BERT yields the highest retrieval quality. However, for a balance of speed and acceptable accuracy, MiniLM with FAISS remains a very compelling configuration.
