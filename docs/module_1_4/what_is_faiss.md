# What is FAISS?

Welcome to the world of vector databases! If you have ever wondered how AI applications like ChatGPT or LegalSight AI can quickly search through millions of documents to find exactly what you need, the answer lies in vector search and libraries like FAISS.

## The Problem with Traditional Search
Traditional databases search for exact keyword matches. If you search for "automobile," a traditional database might completely miss a document that only uses the word "car." 

To solve this, modern AI systems convert text into **embeddings**—lists of numbers (vectors) that capture the underlying meaning of the text. But searching through millions of these high-dimensional vectors to find the most similar ones is computationally expensive.

## Enter Vector Databases
A vector database is specialized software designed to store, manage, and search vector embeddings efficiently. They allow us to find the "closest" vectors in a high-dimensional space, which translates to finding the most semantically similar pieces of information.

## Exact Retrieval vs. ANN (Approximate Nearest Neighbors)

When searching for the closest vectors, we have two main approaches:

### 1. Exact Search (k-Nearest Neighbors - kNN)
In an exact search, we calculate the distance (e.g., Euclidean distance or Cosine similarity) between our query vector and **every single vector** in the database.
* **Pros:** Guaranteed to find the absolute closest matches. 100% accurate.
* **Cons:** Extremely slow and computationally expensive. If you have a billion documents, you have to do a billion calculations for every single search query.

### 2. Approximate Nearest Neighbors (ANN)
To make search blazing fast, we use ANN algorithms. Instead of checking every single vector, ANN uses clever data structures (like graphs, trees, or quantization) to narrow down the search space and only check the most likely candidates.
* **Pros:** Lightning-fast, even with billions of vectors. Uses less memory.
* **Cons:** Trades a tiny bit of accuracy for a massive boost in speed. You might get the 2nd best match instead of the absolute best, but in practice, the results are almost indistinguishable.

## What is FAISS?
**FAISS (Facebook AI Similarity Search)** is a highly optimized, open-source library developed by Meta (Facebook) AI. It is the gold standard for performing ANN searches.

FAISS provides a variety of indexing methods that let developers choose the perfect balance between:
1. **Speed:** How fast the search executes.
2. **Memory:** How much RAM the index consumes.
3. **Accuracy:** How close the results are to the true nearest neighbors.

In LegalSight AI, we use FAISS to quickly search through mountains of legal documents by finding the vectors that are closest to the user's query, ensuring fast and relevant legal research!
