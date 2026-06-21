# Module 1: The Data Layer & Dataset Pipeline

## 1. What it is
A dataset pipeline is an automated script that downloads, cleans, and standardizes raw data (like CUAD or SEC filings) into a uniform format that Machine Learning models can understand.

## 2. Why we need it
Legal datasets come in wildly different formats. CUAD is often in JSON format with complex annotations, while SEC filings are raw text/HTML. If we feed messy data into our Legal-BERT model later, it will learn messy patterns ("garbage in, garbage out"). We need a single source of truth.

## 3. How it works
The pipeline extracts the raw text, normalizes the legal clauses, splits the data into Training (to teach the model), Validation (to tune the model), and Testing (to grade the model) sets, and saves them efficiently using PyArrow (Parquet format).

## 4. Industry Usage
Every Big Tech company uses automated data pipelines. OpenAI, Google, and Meta have massive teams dedicated solely to data pipelines because the data *is* the model.

## 5. Alternatives
You could manually download CSVs and write ad-hoc Jupyter Notebooks. However, this is unscalable, prone to human error, and fails in production.

## 6. Resume Talking Point
*"Architected a unified ETL pipeline normalizing 5 distinct legal corpora (CUAD, LEDGAR, etc.) into a standardized PyArrow feature store, enabling reproducible model training."*

---

# Code Explanation: `dataset_pipeline.py`

*   `__init__`: Sets up the output directory structure so we have a clean place to put `.parquet` files.
*   `normalize_cuad`: This is a stub function for processing the CUAD dataset (which is originally JSON). In reality, CUAD has hundreds of nested labels. We extract only the text and the label ("Indemnification", "Termination", etc.) into a simple tabular Pandas DataFrame.
*   `train_test_split`: A standard scikit-learn function. Notice the `stratify=df['label']`. This is critical for legal AI. Some clauses (like "Force Majeure") are rare. If we don't stratify, our training set might randomly miss them entirely!
*   `to_parquet`: We save the data as Parquet rather than CSV. Parquet is columnar, compressed, and loads into ML workflows (like HuggingFace Datasets) 100x faster than CSV.

---

# Beginner Exercises
1.  **Add a function:** `normalize_sec_filings()` that takes a raw text string, splits it by the word "Section", and adds it to a pandas DataFrame.
2.  **Adjust Splits:** Change the `train_test_split` ratio to 70% Train, 15% Val, and 15% Test.

---

# Advanced Improvements (For the Future)
*   **DVC (Data Version Control):** Instead of just saving to a folder, we will eventually wrap this script in a DVC pipeline (`dvc add data/processed`). This allows us to track which version of the dataset produced which accuracy score.
*   **Data Lake Integration:** In an enterprise, `self.output_dir` would not be a local folder, but an AWS S3 bucket or a Snowflake database.

---

# Interview Preparation

### Beginner Question
**Q:** Why do we split data into Train, Validation, and Test sets?
**A:** The Train set is what the model learns from. The Validation set acts like practice quizzes while the model is learning, helping us tune hyperparameters. The Test set is the final exam; the model *never* sees it until the very end, ensuring we measure true real-world performance, not just memorization.

### Intermediate Question
**Q:** Why did you use Parquet instead of CSV for your legal dataset?
**A:** CSV is row-based and uncompressed, making it slow and heavy for large language corpora. Parquet is a columnar storage format that preserves data types (like nested JSON) and uses snappy compression. It allows ML libraries like PyArrow and HuggingFace to memory-map the data, drastically speeding up the training pipeline.

### Big Tech / Research Question
**Q:** When building the clause dataset, you mentioned stratifying the labels. What problems arise if you don't stratify highly imbalanced legal datasets like CUAD?
**A:** Legal contracts are extremely imbalanced—there are always Payment and Governing Law clauses, but rarely "Change of Control" clauses. Without stratified sampling, the random split might place all "Change of Control" clauses into the Test set and zero in the Training set. The model would never learn what that clause looks like, resulting in a 0% recall for minority classes during evaluation.
