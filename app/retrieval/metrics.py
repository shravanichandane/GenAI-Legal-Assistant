"""
EDUCATIONAL DOCUMENTATION
=========================
What this file does:
This file implements `RetrievalMetrics`, a utility class containing mathematical formulas to evaluate how good our search engine actually is. It calculates Precision@K, Recall@K, Mean Reciprocal Rank (MRR), and measures Latency.

Why it is needed:
In AI engineering, "vibes" aren't enough. We need quantitative numbers to prove that Phase 2 (Legal-BERT) is actually better than Phase 1 (MiniLM). If we tweak the system, these metrics tell us if we improved or degraded performance.

How it connects to the overall architecture:
This is part of the evaluation and testing pipeline. We run offline test datasets containing queries and known relevant document IDs through our Retriever, and use this file to score the results.

Beginner-Friendly Explanation:
- Precision@K: Out of the top K documents we returned, how many were ACTUALLY relevant? (Quality of results)
- Recall@K: Out of ALL the relevant documents that exist in the database, what percentage did we manage to find in our top K? (Completeness of results)
- MRR (Mean Reciprocal Rank): How far down the list was the FIRST relevant result? If it was #1, score is 1. If it was #2, score is 1/2. If #3, 1/3. Higher is better. 
- nDCG@K: Normalized Discounted Cumulative Gain. Rewards systems that put the most relevant results at the very top of the list, rather than just anywhere in the Top K.
- Hit Rate@K: A binary score (1 or 0). Did we find AT LEAST ONE relevant document in the Top K?
- Latency & Memory: How fast did the code run, and how much RAM did the index consume? (Measured via `psutil`).

Interview Questions and Answers:
Q: What is the difference between Precision and Recall?
A: Precision asks "How much of the stuff I gave you is useful?" Recall asks "How much of the useful stuff did I actually manage to find?" There is usually a trade-off between the two.

Q: Why do we use Precision@K instead of standard Precision for search engines?
A: In standard classification, you evaluate all predictions. In search, users rarely look past the first page (Top K, usually K=5 or 10). If the 100th result is relevant, it doesn't matter because the user won't see it. We only care about the quality of the Top K results shown to the user.
"""

from typing import List, Set
import time
import functools

class RetrievalMetrics:
    """
    Utility class for calculating standard information retrieval metrics.
    """

    @staticmethod
    def precision_at_k(retrieved_ids: List[str], relevant_ids: Set[str], k: int) -> float:
        """
        Calculates Precision@K.
        
        Args:
            retrieved_ids: List of document IDs returned by the system.
            relevant_ids: Set of document IDs known to be relevant (ground truth).
            k: The cutoff rank.
            
        Returns:
            Precision@K score (0.0 to 1.0)
        """
        if not retrieved_ids or k <= 0:
            return 0.0
            
        top_k_retrieved = retrieved_ids[:k]
        relevant_retrieved = sum(1 for doc_id in top_k_retrieved if doc_id in relevant_ids)
        
        return relevant_retrieved / k

    @staticmethod
    def recall_at_k(retrieved_ids: List[str], relevant_ids: Set[str], k: int) -> float:
        """
        Calculates Recall@K.
        
        Args:
            retrieved_ids: List of document IDs returned by the system.
            relevant_ids: Set of document IDs known to be relevant (ground truth).
            k: The cutoff rank.
            
        Returns:
            Recall@K score (0.0 to 1.0)
        """
        if not relevant_ids:
            return 0.0 # Avoid division by zero if there's no ground truth
            
        top_k_retrieved = retrieved_ids[:k]
        relevant_retrieved = sum(1 for doc_id in top_k_retrieved if doc_id in relevant_ids)
        
        return relevant_retrieved / len(relevant_ids)

    @staticmethod
    def mean_reciprocal_rank(retrieved_ids: List[str], relevant_ids: Set[str]) -> float:
        """
        Calculates Reciprocal Rank. For Mean Reciprocal Rank (MRR), average this across multiple queries.
        
        Args:
            retrieved_ids: List of document IDs returned by the system, ordered by rank.
            relevant_ids: Set of document IDs known to be relevant.
            
        Returns:
            Reciprocal Rank score (0.0 to 1.0)
        """
        for rank, doc_id in enumerate(retrieved_ids, start=1):
            if doc_id in relevant_ids:
                return 1.0 / rank
        return 0.0

    @staticmethod
    def ndcg_at_k(retrieved_ids: List[str], relevant_ids: Set[str], k: int) -> float:
        """
        Calculates Normalized Discounted Cumulative Gain at K (nDCG@K).
        Assumes binary relevance (1 if relevant, 0 otherwise).
        """
        import math
        if not retrieved_ids or k <= 0 or not relevant_ids:
            return 0.0
            
        dcg = 0.0
        for i, doc_id in enumerate(retrieved_ids[:k]):
            if doc_id in relevant_ids:
                dcg += 1.0 / math.log2(i + 2)  # +2 because index is 0-based and we start at log2(2)
                
        # Ideal DCG (IDCG) - best possible ranking
        idcg = 0.0
        for i in range(min(len(relevant_ids), k)):
            idcg += 1.0 / math.log2(i + 2)
            
        return dcg / idcg if idcg > 0 else 0.0

    @staticmethod
    def hit_rate_at_k(retrieved_ids: List[str], relevant_ids: Set[str], k: int) -> int:
        """
        Calculates Hit Rate@K (1 if at least one relevant document is found in top K, else 0).
        """
        if not retrieved_ids or k <= 0:
            return 0
        
        for doc_id in retrieved_ids[:k]:
            if doc_id in relevant_ids:
                return 1
        return 0

    @staticmethod
    def calculate_latency(func):
        """
        A decorator to measure the execution time of retrieval functions.
        """
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            start = time.perf_counter()
            result = func(*args, **kwargs)
            end = time.perf_counter()
            latency = end - start
            # Assuming the func returns a dictionary or we want to log it
            return result, latency
        return wrapper
