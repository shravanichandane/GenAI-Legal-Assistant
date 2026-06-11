# Interview Questions: Vector Search & Information Retrieval

Test your understanding of modern retrieval systems with these 5 deep machine learning interview questions. These questions are designed to push beyond basic definitions and explore the engineering trade-offs required in production AI systems.

---

### Question 1: The Pitfalls of Lexical Search in Specialized Domains
**"Why might BM25 fail or underperform on a specialized corpus like legal retrieval, and how would you mitigate this?"**

**What the interviewer is looking for:**
* Understanding of the vocabulary gap. Legal professionals often use highly specific terminology (e.g., "res ipsa loquitur," "certiorari") that a layperson querying the system might not use (e.g., "the thing speaks for itself," "appeal to higher court").
* BM25 relies on exact lexical matching. If the user's vocabulary doesn't match the document's vocabulary, the score is zero.
* Mitigation: Discussing **Hybrid Search**. Using embeddings to catch the semantic intent (bridging the vocabulary gap) while keeping BM25 to catch exact citations, statute numbers, or highly specific names that embeddings might smooth over.

### Question 2: Trade-offs in Approximate Nearest Neighbors (ANN)
**"When configuring a FAISS index, you have to choose between flat (exact) search, IVF (Inverted File Index), and HNSW (Hierarchical Navigable Small World). How do you decide which to use?"**

**What the interviewer is looking for:**
* **Flat/L2:** Used when absolute 100% recall is strictly required and the dataset is small enough (usually < 100k-500k vectors) that exact distance calculation doesn't cause unacceptable latency.
* **IVF:** Used when memory is a constraint. It clusters vectors into Voronoi cells, reducing the search space, but requires training and tuning the number of probes (`nprobe`). It's a great balance of speed and memory.
* **HNSW:** Used when blazing-fast latency is the top priority and memory is abundant. It builds a multi-layered graph but consumes significantly more RAM than IVF.

### Question 3: The Curse of Dimensionality
**"Most modern embeddings are highly dimensional (e.g., 768 or 1536 dimensions). How does the 'Curse of Dimensionality' affect distance metrics like Euclidean distance, and why is Cosine Similarity often preferred for text embeddings?"**

**What the interviewer is looking for:**
* As dimensions increase, the Euclidean distance between any two random points tends to converge, making it harder to distinguish "close" vectors from "far" vectors (the volume of the space grows exponentially).
* Text embeddings represent the *direction* of meaning. Cosine similarity measures the angle between vectors, ignoring their magnitude. 
* Mentioning that if vectors are L2-normalized, Euclidean distance and Cosine similarity rank vectors in the exact same order.

### Question 4: Handling Document Length in Vector Search
**"You have a legal document that is 50 pages long. How do you embed this for a vector database? If you chunk it, how do you handle the loss of global context?"**

**What the interviewer is looking for:**
* Acknowledging that embedding models have maximum token limits (e.g., 512 for BERT, 8192 for modern OpenAI models) and that embedding a massive document dilutes the semantic signal.
* Explaining **Chunking Strategies:** Overlapping chunks to prevent cutting concepts in half.
* **Global Context Solutions:** 
  1. *Parent-Child indexing:* Embedding the chunks, but retrieving the parent document.
  2. *Summary embeddings:* Generating an AI summary of the whole document and embedding the summary alongside the chunks.
  3. Adding metadata (title, chapter, case name) to the text of every chunk before embedding it.

### Question 5: BM25 Saturation vs. Term Frequency
**"Explain the concept of 'Term Frequency Saturation' in BM25. Why is this mathematically more sound for document retrieval than the linear Term Frequency used in standard TF-IDF?"**

**What the interviewer is looking for:**
* TF-IDF scales linearly. If document A has the word "fraud" 5 times, and document B has it 50 times, TF-IDF might consider B ten times more relevant.
* BM25 applies an asymptotic curve. The relevance score increases quickly for the first few occurrences of the word, but then flattens out. 
* The intuition: Once a document mentions a keyword 5 or 6 times, we already know the document is about that topic. Mentioning it 100 more times does not make it 100 times more relevant; it just means it's a longer or more repetitive document.
