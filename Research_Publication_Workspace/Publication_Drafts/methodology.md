# Methodology

## Datasets
Our evaluation leverages two standard legal datasets:
- **CUAD (Contract Understanding Atticus Dataset):** A corpus of commercial legal contracts annotated with expert labels for various clauses.
- **ContractNLI:** A dataset designed for document-level natural language inference on legal contracts.

## Retrieval Methods and Models
We compared two embedding models for dense retrieval:
- **MiniLM (all-MiniLM-L6-v2):** A general-purpose, lightweight embedding model optimized for speed and small memory footprint.
- **Legal-BERT (nlpaueb/legal-bert-base-uncased):** A domain-specific model pre-trained on legal text, designed to capture complex legal terminology and context.

## Indexing and Search
- **FAISS Indexing:** Used for dense vector retrieval, enabling efficient similarity search across document embeddings.
- **BM25:** A sparse, keyword-based retrieval algorithm used as our traditional baseline to contrast with dense retrieval techniques.
