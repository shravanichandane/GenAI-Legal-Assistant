# LegalSight AI Research Platform: Master Build Guide

Welcome to your central learning hub. This document will grow as we build the platform layer by layer. 

---

## Module 1: The Data Layer & Dataset Pipeline

### 1. What it is
A dataset pipeline is an automated script that downloads, cleans, and standardizes raw data (like CUAD or SEC filings) into a uniform format that Machine Learning models can understand.

### 2. Why we need it
Legal datasets come in wildly different formats. CUAD is often in JSON format with complex annotations, while SEC filings are raw text/HTML. If we feed messy data into our Legal-BERT model later, it will learn messy patterns ("garbage in, garbage out"). We need a single source of truth.

### 3. How it works
The pipeline extracts the raw text, normalizes the legal clauses, splits the data into Training (to teach the model), Validation (to tune the model), and Testing (to grade the model) sets, and saves them efficiently using PyArrow (Parquet format).

### 4. Industry Usage
Every Big Tech company uses automated data pipelines. OpenAI, Google, and Meta have massive teams dedicated solely to data pipelines because the data *is* the model.

### 5. Alternatives
You could manually download CSVs and write ad-hoc Jupyter Notebooks. However, this is unscalable, prone to human error, and fails in production.

### 6. Resume Talking Point
*"Architected a unified ETL pipeline normalizing 5 distinct legal corpora (CUAD, LEDGAR, etc.) into a standardized PyArrow feature store, enabling reproducible model training."*

---

### Code Explanation: `dataset_pipeline.py`
*   `__init__`: Sets up the output directory structure so we have a clean place to put `.parquet` files.
*   `normalize_cuad`: This is a stub function for processing the CUAD dataset (which is originally JSON). In reality, CUAD has hundreds of nested labels. We extract only the text and the label ("Indemnification", "Termination", etc.) into a simple tabular Pandas DataFrame.
*   `train_test_split`: A standard scikit-learn function. Notice the `stratify=df['label']`. This is critical for legal AI. Some clauses (like "Force Majeure") are rare. If we don't stratify, our training set might randomly miss them entirely!
*   `to_parquet`: We save the data as Parquet rather than CSV. Parquet is columnar, compressed, and loads into ML workflows (like HuggingFace Datasets) 100x faster than CSV.

---

### Beginner Exercises
1.  **Add a function:** `normalize_sec_filings()` that takes a raw text string, splits it by the word "Section", and adds it to a pandas DataFrame.
2.  **Adjust Splits:** Change the `train_test_split` ratio to 70% Train, 15% Val, and 15% Test.

---

### Interview Preparation

**Beginner Question**
**Q:** Why do we split data into Train, Validation, and Test sets?
**A:** The Train set is what the model learns from. The Validation set acts like practice quizzes while the model is learning, helping us tune hyperparameters. The Test set is the final exam; the model *never* sees it until the very end, ensuring we measure true real-world performance, not just memorization.

**Intermediate Question**
**Q:** Why did you use Parquet instead of CSV for your legal dataset?
**A:** CSV is row-based and uncompressed, making it slow and heavy for large language corpora. Parquet is a columnar storage format that preserves data types (like nested JSON) and uses snappy compression. It allows ML libraries like PyArrow and HuggingFace to memory-map the data, drastically speeding up the training pipeline.

**Big Tech / Research Question**
**Q:** When building the clause dataset, you mentioned stratifying the labels. What problems arise if you don't stratify highly imbalanced legal datasets like CUAD?
**A:** Legal contracts are extremely imbalanced—there are always Payment and Governing Law clauses, but rarely "Change of Control" clauses. Without stratified sampling, the random split might place all "Change of Control" clauses into the Test set and zero in the Training set. The model would never learn what that clause looks like, resulting in a 0% recall for minority classes during evaluation.

---
---

## Module 2: The Data Engineering Layer (Feature Store & ETL)

### 1. What it is
The Data Engineering Layer is the bridge between raw legal documents and your ML models. It extracts metadata (like clause counts, party names, and document length) and loads it into a structured database (PostgreSQL) and a Graph Database (Neo4j). 

### 2. Why we need it
A raw legal document is just a massive string of text. To predict risk (like we will do later with XGBoost), the ML model needs structured numbers and categories (Features). The Feature Store holds these pre-calculated metrics so the model doesn't have to parse the text over and over again.

### 3. How it works (ETL Pipeline)
*   **Extract:** Read the raw contract.
*   **Transform:** Run algorithms (like SpaCy NER or regex) to count the number of clauses, find the effective date, and identify the jurisdiction.
*   **Load:** Push this clean, structured row into our PostgreSQL Feature Store.

### 4. Industry Usage
Enterprise AI teams (like Uber or Airbnb) rely entirely on Feature Stores. When a model needs to make a real-time prediction, it queries the Feature Store instead of computing the features from scratch, saving crucial milliseconds.

### 5. Alternatives
You could calculate features "on-the-fly" right before passing them to the model. However, this is computationally expensive. If 1,000 users upload contracts, your server would crash trying to compute NLP metrics 1,000 times concurrently.

### 6. Resume Talking Point
*"Built an automated ETL pipeline integrating raw contract data with a PostgreSQL feature store and Neo4j Knowledge Graph, decoupling data processing from real-time model inference."*

---

### Architecture Diagram
```text
[Raw Contract PDF] 
       ↓
[ETL Python Script] 
       ├───> Extract Metadata (Word count, Section count)
       ├───> Extract Entities (Apple Inc, Delaware)
       ↓
[PostgreSQL Feature Store] 
(Table: contract_features)
```

---

### Code Explanation: `data_engineering/etl_pipeline.py`
*   `create_engine`: We use SQLAlchemy to open a connection to our relational database. In your case, this connects directly to your Neon PostgreSQL instance.
*   `extract_metadata`: This is the "Transform" step of ETL. Right now, it counts "SECTION" and "ARTICLE" keywords. In the future, we will swap this with a sophisticated NLP model.
*   `to_sql(table_name, ...)`: This is the "Load" step. It takes our pandas DataFrame containing the newly extracted features and securely pushes it to the database table. 

---

### Beginner Exercises
1.  **Add a feature:** Modify `extract_metadata` to also return the `"word_count"` of the raw text.
2.  **Add a feature:** Add a boolean feature `"contains_indemnification"` that returns `True` if the word "indemnify" is in the text.

---

### Advanced Improvements
*   **Apache Airflow:** Instead of running this Python script manually, we would schedule it using Airflow to automatically process any new contracts dropped into an Amazon S3 bucket at midnight every day.

---

### Interview Preparation

**Beginner Question**
**Q:** What does ETL stand for, and what does each step do?
**A:** Extract (pulling data from a source), Transform (cleaning and calculating new features), and Load (pushing the structured data into a database).

**Intermediate Question**
**Q:** What is a Feature Store, and why did you implement one?
**A:** A Feature Store is a centralized repository for storing pre-calculated ML features. We implemented it so our Risk Prediction models can instantly query metrics (like historical liability counts) without having to re-parse the heavy contract text at inference time, ensuring low latency.

**Big Tech / Research Question**
**Q:** How do you handle schema evolution in your ETL pipeline if the legal team decides they want to start tracking a new metadata field, like "Governing Law"?
**A:** We would use a database migration tool like Alembic. The ETL script's `extract_metadata` function would be updated to output the new field, and we would run an `ALTER TABLE` migration on the PostgreSQL Feature Store to accept the new column. For historical data, we would trigger a backfill job in Airflow to re-process old contracts and populate the missing "Governing Law" values.

## Module 4: Knowledge Graph Layer

### 1. Concept
A Knowledge Graph (KG) represents entities and their relationships. In our legal assistant, it links documents, clauses, and metadata (like risk levels or clause types). This allows for complex querying, such as "Find all high-risk termination clauses in vendor agreements."

### 2. Architecture
- **Nodes**: Documents, Clauses, Entities (Organizations, Dates).
- **Edges (Relationships)**: CONTAINS (Document -> Clause), MENTIONS (Clause -> Entity).
- **Database**: Neo4j, queried using Cypher.
- **Python Driver**: `neo4j` library to connect and execute writes/reads.

### 3. Code Explanation
- `LegalGraphBuilder`: Connects to Neo4j using credentials.
- `_create_document_node` & `_create_clause_node`: Uses Cypher `MERGE` to prevent duplicate nodes.
- `_create_relationship`: Connects the `Document` node to its respective `Clause` node using the `[:CONTAINS]` relationship.
- `build_graph`: Iterates over documents and clauses to populate the graph in a session transaction.

### 4. Exercises
- **Basic**: Modify the script to add an `Entity` node (e.g., "Company A") and link it to a document via a `SIGNED_BY` relationship.
- **Intermediate**: Write a Cypher query in Python to retrieve all clauses of type "CONFIDENTIALITY" that belong to a specific document.
- **Advanced**: Implement a graph retrieval function that uses LangChain's `GraphCypherQAChain` to answer natural language questions.

### 5. Improvements
- Use batching (`UNWIND`) in Cypher queries for large datasets instead of iterating in Python.
- Add graph embeddings (Node2Vec) to represent graph structures in the vector space for hybrid retrieval.

### 6. Interview Questions
- *How does a knowledge graph improve RAG compared to standard vector search?*
- *Explain the difference between `MATCH` and `MERGE` in Cypher.*
- *How would you handle schema evolution in a property graph like Neo4j?*

## Module 5: Deep Learning Layer

### 1. Concept
Pre-trained models like BERT understand general language, but legal text contains specific jargon. Fine-tuning involves taking a model pre-trained on legal text (Legal-BERT) and training it further on our specific task (e.g., clause classification or risk scoring) using labeled data.

### 2. Architecture
- **Base Model**: `nlpaueb/legal-bert-base-uncased`.
- **Tokenizer**: Converts text into token IDs that the model understands.
- **Classification Head**: A linear layer on top of BERT's pooled output to predict labels.
- **Trainer**: Hugging Face API to abstract the training loop.

### 3. Code Explanation
- `Dataset.from_dict`: Creates a Hugging Face dataset from raw texts and labels.
- `tokenize_function`: Pads and truncates texts to a fixed length (128 tokens) so they can be batched as tensors.
- `AutoModelForSequenceClassification`: Loads Legal-BERT with a fresh classification head for 3 labels.
- `TrainingArguments` & `Trainer`: Configures hyperparameters (learning rate, epochs, batch size) and executes the training loop.
- `save_pretrained`: Saves the weights and tokenizer for later inference.

### 4. Exercises
- **Basic**: Change the script to perform binary classification (e.g., "High Risk" vs "Low Risk").
- **Intermediate**: Implement an evaluation metrics function using the `evaluate` library to calculate accuracy and F1 score during training.
- **Advanced**: Write a custom PyTorch training loop instead of using the Hugging Face `Trainer` to have granular control.

### 5. Improvements
- Use LoRA (Low-Rank Adaptation) or PEFT to fine-tune the model efficiently without updating all base model weights.
- Integrate MLflow or Weights & Biases (W&B) to track experiments, loss curves, and metrics.

### 6. Interview Questions
- *Why use Legal-BERT instead of standard BERT for this project?*
- *What is the purpose of the `[CLS]` token in BERT for classification tasks?*
- *How would you handle class imbalance if you have very few "High Risk" clauses?*

---

## Module 6: The Retrieval Layer (Semantic Search & RAG)

### 1. Concept
Traditional keyword search (BM25) fails when lawyers search for "How to end the contract" but the document says "Termination for convenience." The Retrieval Layer converts sentences into high-dimensional vectors (Embeddings). Concepts with similar meanings are mapped close together in this mathematical space.

### 2. Architecture
- **Embedding Model**: `SentenceTransformers` (converting text to float arrays).
- **Vector Database**: `FAISS` (Facebook AI Similarity Search) or `Pinecone`.
- **Search Metric**: Cosine Similarity / Inner Product.

### 3. Code Explanation: `retrieval/vector_search.py`
- `SentenceTransformer`: Loads the embedding model.
- `faiss.IndexFlatIP`: We use Inner Product. Because we use `faiss.normalize_L2`, the Inner Product is mathematically identical to Cosine Similarity.
- `build_index`: Encodes the legal clauses and pushes them into the FAISS index in RAM.
- `search`: Converts the user query into a vector and finds the Nearest Neighbors (the most semantically similar clauses).

### 4. Exercises
- **Basic**: Change the query in the script to "Where are disputes resolved?" and see if it can retrieve a Governing Law clause.
- **Intermediate**: Save the FAISS index to disk using `faiss.write_index(self.index, "legal.index")` so you don't have to rebuild it every time.
- **Advanced**: Implement a Hybrid Search combining FAISS semantic search with BM25 keyword search.

### 5. Improvements
- Use a dedicated Vector DB like Pinecone or Qdrant for cloud scalability.
- Add Re-ranking (e.g., Cohere Rerank) to re-order the top 10 FAISS results for maximum accuracy.

### 6. Interview Questions
- *What is the difference between Dense Retrieval (FAISS) and Sparse Retrieval (TF-IDF/BM25)?*
- *Why must you normalize your vectors before using Inner Product to calculate Cosine Similarity in FAISS?*

---

## Module 7: Agentic AI Layer (Multi-Agent Verification)

### 1. Concept
A single LLM prompt often hallucinates or makes mistakes (like the "Heading Sensitivity" bug we saw in your UI snapshot). Agentic AI breaks the problem down. One agent extracts data, one classifies it, and a "Critic Agent" argues against the classification to ensure it is grounded in evidence.

### 2. Architecture
- **State Machine**: Using libraries like `LangGraph` to route data.
- **Extractor Agent**: Pulls out hard facts (Money, Names).
- **Classifier Agent**: Makes a prediction (e.g., LIMITATION_OF_LIABILITY).
- **Critic Agent**: Verifies the prediction against the extracted facts.

### 3. Code Explanation: `agentic_ai/workflow.py`
- `state (Dict)`: This dictionary acts as the "Memory" flowing between the agents.
- `ExtractorAgent`: Uses rules or small models to find specific entities.
- `ClassifierAgent`: Predicts the clause type. Notice it sets a `confidence` score.
- `CriticAgent`: Acts as a guardrail. It checks if the Classifier's prediction makes logical sense given the Extractor's findings. If a clause is flagged as a Liability Limitation but no monetary amount was extracted, the Critic rejects it!

### 4. Exercises
- **Basic**: Add a `ReflectionAgent` class that prints out the final state and suggests a human review if `verification_status` is REJECTED.
- **Intermediate**: Connect the ExtractorAgent to the SpaCy `LegalEntityExtractor` we built in Module 3.
- **Advanced**: Migrate this raw Python state machine into a true `langgraph.graph.StateGraph`.

### 5. Improvements
- Agentic RAG: If the Critic Agent rejects the classification, it can loop back to the Retrieval Layer to fetch more context from the legal playbook before trying again.

### 6. Interview Questions
- *What is the primary benefit of a Multi-Agent system over a single large LLM prompt?*
- *In LangGraph, what is the role of the "State", and why must state updates be carefully managed?*
- *How does the Critic Agent reduce hallucinations in enterprise AI systems?*

---

## Module 8: Risk Intelligence Layer
**Goal:** Implement an XGBoost machine learning model to predict risk levels from clause text.

1. **Concept:** Risk prediction requires moving beyond rules to ML-based classification using historical data.
2. **Context:** XGBoost is a powerful gradient boosting algorithm that excels at structured tabular data and vectorized text.
3. **Implementation:** Create `risk_model.py` using `TfidfVectorizer` for text embedding and `xgboost.XGBClassifier` for predicting LOW/MEDIUM/HIGH risk.
4. **Data:** Training requires a dataset of legal clauses with known risk labels (0=LOW, 1=MEDIUM, 2=HIGH).
5. **Evaluation:** Use `classification_report` to measure Precision, Recall, and F1-score of the model on validation data.
6. **Saving/Loading:** Use `joblib` to persist both the trained vectorizer and the XGBoost model to disk (`models/` directory) for production use.
7. **Inference:** In `predict_risk`, transform the incoming text, run `predict_proba` to get a confidence score alongside the risk category.
8. **Integration:** Connect this module to the analysis pipeline so that every clause processed receives a statistically backed risk score.

## Module 9: Explainable AI Layer
**Goal:** Provide transparency into *why* the Risk Intelligence model made a specific prediction.

1. **Concept:** Black-box models like XGBoost can be hard to trust in legal tech; Explainable AI (XAI) tools like SHAP demystify them.
2. **Context:** SHAP (SHapley Additive exPlanations) uses game theory to assign an importance value to each feature (word) for a given prediction.
3. **Implementation:** Create `shap_explainer.py` using `shap.TreeExplainer` which is optimized for tree-based models like XGBoost.
4. **Attribution:** Transform the clause text, compute SHAP values, and map them back to the vocabulary features from the `TfidfVectorizer`.
5. **Multiclass Handling:** Extract the SHAP values corresponding specifically to the predicted class to explain *why* it chose that label.
6. **Formatting:** Rank the words by their absolute SHAP contribution to highlight the most impactful terms (e.g., "indemnify", "breach").
7. **UI Surfacing:** Return a structured list of top contributing words and their weights to be displayed in the Streamlit frontend.
8. **Trust:** Showing the lawyer exactly which words triggered a "HIGH RISK" prediction builds user trust and confidence in the AI system.

## Module 10: MLOps Layer

**8-Step Teaching Note:**
1. **Goal:** Track model experiments, prompts, and data versions systematically to ensure reproducibility.
2. **Context:** In GenAI, prompts and configurations change frequently; MLflow helps log these changes alongside DVC for data versioning.
3. **Key Components:** `MLOpsTracker` class encapsulating MLflow APIs for logging params, metrics, and artifacts.
4. **Implementation Step:** We check for the availability of `mlflow` and safely fall back to mock logging if not present.
5. **DVC Integration:** We log the DVC data commit hash as a tag in MLflow to link model runs directly to specific dataset versions.
6. **Execution:** Initialize `tracker = MLOpsTracker()`, then call `tracker.start_run()`, `log_params()`, and `log_metrics()` around your evaluation loop.
7. **Best Practice:** Keep the tracking layer decoupled. If MLflow crashes or isn't installed, it shouldn't break the main application pipeline.
8. **Next Steps:** Link the metrics generated from the Evaluation Layer (Module 11) to be automatically logged via this MLOps Tracker.

## Module 11: Evaluation Layer

**8-Step Teaching Note:**
1. **Goal:** Establish a rigorous benchmark framework to evaluate the Legal Assistant's extraction and classification capabilities.
2. **Context:** LLMs can be unpredictable. Standardizing evaluation using Precision, Recall, and F1 ensures we measure true performance improvements.
3. **Key Components:** `BenchmarkFramework` using `scikit-learn` to calculate standard NLP/ML metrics.
4. **Implementation Step:** We provide `evaluate_classification` for categorical tasks (like Clause Type) and `evaluate_risk_scoring` for numerical tasks.
5. **Handling Imbalance:** Legal datasets often have highly skewed classes (e.g., many "General" clauses, few "Indemnity"). We use `macro` averaging for fairer assessment.
6. **Execution:** `run_benchmark_suite()` takes a dataset and a generic `predict_fn` (which could be an LLM chain) to easily run bulk evaluations.
7. **Best Practice:** Always log evaluation metrics back to the MLOps Layer (MLflow) to track model drift over time.
8. **Next Steps:** Integrate this benchmark suite with a CI/CD pipeline to automatically run regression tests on new prompt changes.

## Module 12: Analytics Layer
**1. Purpose:** Provide a real-time Streamlit dashboard to monitor system KPIs, errors, and performance metrics.
**2. Core Concepts:** Data visualization, interactive web apps, metric tracking.
**3. Key Components:** `dashboard.py` (Streamlit UI layout, KPI metrics, charts).
**4. Dependencies:** `streamlit`, `pandas`, `plotly`.
**5. Implementation Steps:** Load metrics data, layout columns for KPIs, render time-series plots, render error distribution pie charts.
**6. Common Pitfalls:** Blocking the main thread with heavy data processing; not handling empty data gracefully.
**7. Testing Strategy:** Provide mock/dummy dictionaries to the render function to verify UI component rendering.
**8. Success Metrics:** Dashboard loads within 2 seconds, accurately reflects the provided dictionary state, and charts are interactive.

## Module 13: Benchmark Layer
**1. Purpose:** Automate the execution of performance evaluations across different models or configurations.
**2. Core Concepts:** Throughput measurement, latency tracking, automated experimentation.
**3. Key Components:** `run_experiments.py` (BenchmarkRunner class, time tracking, result serialization).
**4. Dependencies:** `time`, `json`, `logging`.
**5. Implementation Steps:** Initialize endpoints, mock dataset loading, iterate over inputs simulating inference, calculate throughput, and export to JSON.
**6. Common Pitfalls:** Neglecting network latency overhead in measurements; failing to warm up models before timing.
**7. Testing Strategy:** Run with a small dummy dataset and verify that the output JSON contains expected keys (duration, throughput).
**8. Success Metrics:** Script completes without errors, produces a well-structured JSON artifact, and accurately captures relative performance differences.

## Module 14: Research Layer
**1. Purpose:** Automatically generate a formalized LaTeX research paper summarizing findings and results.
**2. Core Concepts:** Automated reporting, LaTeX templating, string formatting.
**3. Key Components:** `generate_paper.py` (LaTeX string template, file I/O).
**4. Dependencies:** Standard Python libraries (`os`).
**5. Implementation Steps:** Define paper metadata (title, abstract), construct LaTeX document string, and write to a `.tex` file.
**6. Common Pitfalls:** Unescaped LaTeX special characters (like `%` or `&`) in the dynamic text causing compilation errors.
**7. Testing Strategy:** Generate a sample paper and attempt to compile it using `pdflatex` to ensure valid syntax.
**8. Success Metrics:** A `.tex` file is created with correct structure, valid sections, and properly injected dynamic content.
