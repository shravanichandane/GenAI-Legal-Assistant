# Data Directory
This directory holds all datasets for the LegalSight AI platform.

## Structure
```
data/
├── raw/          # Original, unprocessed datasets (CUAD, SEC filings)
├── processed/    # Cleaned, split, and ready-for-training datasets
└── embeddings/   # Pre-computed vector embeddings (FAISS indices)
```

> **Rule:** Never commit raw data to Git. Use `.gitignore` to exclude
> large files, and use DVC (Data Version Control) to track them in later tiers.
